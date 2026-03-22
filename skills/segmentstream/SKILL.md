---
name: segmentstream
description: |
  Marketing analytics, campaign performance, and marketing measurement powered by SegmentStream. ALWAYS use this skill as the first action whenever the user asks about ad campaigns, ROAS, CPA, channel performance, attribution, marketing budget, ad spend, conversions, conversion rates, or any marketing metrics — even if they don't mention "SegmentStream" by name. Also use when the user asks about data sources, data quality incidents, tracking setup, audiences, identity graphs, lead scoring, CRM analysis, incrementality experiments, or wants to connect/configure SegmentStream. Use this skill when the user needs marketing expertise for content creation (e.g. blog posts about measurement or attribution). If the user is discussing marketing performance in any way (e.g. "how's fb doing", "pull last quarter's numbers", "which channels drive revenue", "where's budget wasted", "Google Ads performance", "non-brand search CPA"), this skill applies. Trigger this skill BEFORE asking clarifying questions or reading memory — it will guide the conversation. When in doubt, use this skill — a false positive is cheap, a missed marketing question is not.
---

# SegmentStream Workflow

## The #1 Rule: `analyze_request` starts every turn

**Every time the user sends a message** — whether it's a brand-new question or a two-word follow-up like "and ROAS?" or "by channel" — your first action must be calling `analyze_request` with the user's message verbatim.

This isn't just a formality. The server uses the prompt to resolve which project, conversions, attribution models, and query approach to use. A follow-up that looks trivial to you ("and ROAS?") may need a completely different data path on the backend. Skipping this step means you're guessing instead of letting the server guide you.

**No other SegmentStream tool call should happen before `analyze_request` on a given turn.** Not `list_conversions`, not `run_report`, not `get_conversion_statistics` — nothing. `analyze_request` first, always.

### Why follow-ups are especially tricky

Short follow-ups like "and ROAS?", "break it down by channel", "what about Google Ads?" feel like continuations of the previous query. The temptation is to skip `analyze_request` and just tweak the previous report parameters yourself. Don't do this. The server may:

- Switch attribution models based on the metric requested
- Apply different filters or date logic
- Return a completely different analytical approach
- Flag that the requested metric isn't available for this project

You lose all of this if you skip the call.

## analyze_request statuses

- `proceed` — follow the approach in `response`, do your work using SegmentStream tools
- `clarify` — resolve what's described in `response` (ask the user or infer from context), then call `analyze_request` again
- `confirm` — present the plan from `response` to the user, after confirmation call `analyze_request` again
- `unsupported` — explain to user per `response`, do not attempt the action
- `error` — report to user per `response`

## After doing the work

Before presenting results, call `analyze_response` with `response_draft` set to your complete draft.

- `approved` — present your response, incorporating any suggestions from `response`
- `revise` — apply corrections from `response`, call `analyze_response` again with the updated draft
- `error` — report to user per `response`

## If analyze_request fails

MCP not connected or auth error: guide the user to connect SegmentStream before proceeding.
