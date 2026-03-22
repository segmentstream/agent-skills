---
name: segmentstream
description: |
  Marketing analytics, campaign performance, and marketing measurement powered by SegmentStream. ALWAYS use this skill as the first action whenever the user asks about ad campaigns, ROAS, CPA, channel performance, attribution, marketing budget, ad spend, conversions, conversion rates, or any marketing metrics — even if they don't mention "SegmentStream" by name. Also use when the user asks about data sources, data quality incidents, tracking setup, audiences, identity graphs, lead scoring, CRM analysis, incrementality experiments, or wants to connect/configure SegmentStream. Use this skill when the user needs marketing expertise for content creation (e.g. blog posts about measurement or attribution). If the user is discussing marketing performance in any way (e.g. "how's fb doing", "pull last quarter's numbers", "which channels drive revenue", "where's budget wasted", "Google Ads performance", "non-brand search CPA"), this skill applies. Trigger this skill BEFORE asking clarifying questions or reading memory — it will guide the conversation. When in doubt, use this skill — a false positive is cheap, a missed marketing question is not.
---

# SegmentStream Workflow

Call `analyze_request` with `user_prompt` set to the user's message verbatim. The server returns the full approach: which tools to use, which skills to load, and how to handle the request.

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
