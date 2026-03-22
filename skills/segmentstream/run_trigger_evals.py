#!/usr/bin/env python3
"""Run trigger evaluations for plugin skills using --plugin-dir.

Unlike the standard run_eval.py (which creates isolated command files),
this script loads the full plugin context so Claude sees MCP tools,
competing skills, and the real environment.

Usage:
    python3 run_trigger_evals.py [--workers 5] [--runs 1] [--timeout 45]
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent.parent  # agent-skills/
EVAL_FILE = Path(__file__).resolve().parent / "trigger-evals.json"


SKILL_NAMES = ["segmentstream"]  # skill names to detect as triggers


def run_single_query(query: str, timeout: int, max_turns: int = 3) -> bool:
    """Run a single query and return whether a segmentstream skill triggered.

    Uses stream-json to detect Skill tool calls specifically, avoiding false
    positives from non-skill tool use (Write, Read, Bash, etc.).

    max_turns=3 gives Claude room to read memory/config before triggering the
    skill, without running the full workflow.
    """
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = [
        "claude", "-p", query,
        "--plugin-dir", str(PLUGIN_DIR),
        "--output-format", "stream-json",
        "--verbose",
        "--max-turns", str(max_turns),
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, env=env,
        )

        # Parse stream-json events looking for Skill tool calls
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Check assistant messages for Skill tool calls
            if event.get("type") == "assistant":
                message = event.get("message", {})
                for content in message.get("content", []):
                    if content.get("type") != "tool_use":
                        continue
                    tool_name = content.get("name", "")
                    tool_input = content.get("input", {})
                    if tool_name == "Skill":
                        skill = tool_input.get("skill", "")
                        if any(s in skill for s in SKILL_NAMES):
                            return True

        return False
    except subprocess.TimeoutExpired:
        print(f"  Warning: timeout for: {query[:60]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  Warning: {e} for: {query[:60]}", file=sys.stderr)
        return False


def run_eval(eval_set: list[dict], workers: int, runs: int, timeout: int) -> dict:
    """Run all queries and return results."""
    results = []
    query_triggers: dict[str, list[bool]] = {}
    query_items: dict[str, dict] = {}

    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for _ in range(runs):
                future = executor.submit(run_single_query, item["query"], timeout)
                future_to_info[future] = item

        for future in as_completed(future_to_info):
            item = future_to_info[future]
            q = item["query"]
            query_items[q] = item
            query_triggers.setdefault(q, [])
            try:
                query_triggers[q].append(future.result())
            except Exception as e:
                print(f"  Warning: {e}", file=sys.stderr)
                query_triggers[q].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers) if triggers else 0
        should = item["should_trigger"]
        passed = (trigger_rate >= 0.5) if should else (trigger_rate < 0.5)
        results.append({
            "query": query,
            "should_trigger": should,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": passed,
        })

    # Sort: should-trigger first, then should-not
    results.sort(key=lambda r: (not r["should_trigger"], r["query"]))

    pos = [r for r in results if r["should_trigger"]]
    neg = [r for r in results if not r["should_trigger"]]
    tp = sum(r["triggers"] for r in pos)
    pos_runs = sum(r["runs"] for r in pos)
    fn = pos_runs - tp
    fp = sum(r["triggers"] for r in neg)
    neg_runs = sum(r["runs"] for r in neg)
    tn = neg_runs - fp

    total = tp + tn + fp + fn
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0

    return {
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["pass"]),
            "failed": sum(1 for r in results if not r["pass"]),
        },
        "metrics": {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "accuracy": round(accuracy, 3),
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evals with --plugin-dir")
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers (default: 5)")
    parser.add_argument("--runs", type=int, default=1, help="Runs per query (default: 1)")
    parser.add_argument("--timeout", type=int, default=45, help="Timeout per query in seconds")
    parser.add_argument("--eval-file", type=str, default=str(EVAL_FILE), help="Path to eval JSON")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_file).read_text())
    print(f"Running {len(eval_set)} queries ({args.runs} runs each, {args.workers} workers)", file=sys.stderr)

    t0 = time.time()
    output = run_eval(eval_set, args.workers, args.runs, args.timeout)
    elapsed = time.time() - t0

    # Print results to stderr
    m = output["metrics"]
    s = output["summary"]
    print(f"\nResults: {s['passed']}/{s['total']} passed in {elapsed:.1f}s", file=sys.stderr)
    print(f"Precision={m['precision']:.0%} Recall={m['recall']:.0%} Accuracy={m['accuracy']:.0%}", file=sys.stderr)
    print(f"TP={m['tp']} FP={m['fp']} TN={m['tn']} FN={m['fn']}", file=sys.stderr)
    print(file=sys.stderr)

    for r in output["results"]:
        status = "PASS" if r["pass"] else "FAIL"
        rate = f"{r['triggers']}/{r['runs']}"
        print(f"  [{status}] rate={rate} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    # Print JSON to stdout
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
