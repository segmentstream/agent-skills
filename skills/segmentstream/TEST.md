# Testing the segmentstream skill

## Why standard skill-creator scripts don't work

This skill is part of a plugin. Two things break with the standard skill-creator toolchain:

1. **`run_eval.py`** creates isolated command files in `.claude/commands/` without loading MCP tools
   or plugin context. Claude sees the command but has no SegmentStream tools, so it answers marketing
   queries directly (~4% recall). Always use `--plugin-dir` instead.

2. **`run_loop.py` / `improve_description.py`** call `anthropic.Anthropic()` directly, which requires
   `ANTHROPIC_API_KEY`. Claude Code Max authenticates via OAuth — no API key is available in the
   subprocess environment. Use `claude -p` for any LLM calls instead.

## Trigger evals

Test queries are in `trigger-evals.json` (24 should-trigger, 10 should-not-trigger).

### Run the eval script

```bash
python3 run_trigger_evals.py [--workers 5] [--runs 3] [--timeout 90]
```

The script uses `claude -p --plugin-dir --output-format stream-json --verbose --max-turns 3`
and parses the event stream to detect `Skill` tool calls containing "segmentstream".

### Detection logic

The script looks for `Skill` tool calls in `stream-json` assistant messages:

- Claude calls `Skill` with a skill name containing "segmentstream" → **triggered**
- Claude responds without any such `Skill` call → **not triggered**

`--max-turns 3` gives Claude room to read memory/config before triggering the skill.
`--max-turns 1` is too restrictive — Claude sometimes reads memory files first, using up its only turn.

Simple `stop_reason == "tool_use"` detection is insufficient — it counts ANY tool use (Write, Read, etc.)
as a trigger, producing false positives on coding queries.

### Manual single-query test

```bash
CLAUDECODE= claude -p "<query>" \
  --plugin-dir /path/to/agent-skills \
  --output-format stream-json --verbose \
  --max-turns 3
```

`CLAUDECODE=` strips the env var that prevents nesting `claude -p` inside a Claude Code session.

### Known limitations

- **Follow-up queries without context** (e.g. "break it down by week") can't trigger in `-p` mode
  because there's no conversation history. These work in interactive sessions.
- **Queries with competing instructions** (e.g. "conversion rate dropped — check the frontend code")
  may not trigger when the non-marketing instruction dominates. In interactive sessions, Claude
  would likely handle both aspects.
- **Memory can compete with skill triggers.** If a memory file (e.g. "ask about attribution model")
  matches the query, Claude may follow the memory guidance and respond directly without triggering
  the skill. This is correct multi-turn behavior but looks like a miss in single-prompt mode.

### Baseline (2026-03-22)

Precision=100% Recall=92% Accuracy=94% (32/34 passed, 3 runs per query)

## Workflow evals

Test cases are in `evals.json`. These test that once the skill triggers, Claude follows the
analyze_request/analyze_response protocol:

```bash
CLAUDECODE= claude -p "<prompt>" \
  --plugin-dir /path/to/agent-skills \
  --output-format stream-json --verbose \
  --max-turns 10
```

Key assertions: first SegmentStream MCP call is `analyze_request`, and `analyze_response` is called
before the final output.
