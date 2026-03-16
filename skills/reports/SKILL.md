---
name: Campaign Reports
description: This skill should be used when the user asks about "campaign performance", "show ROAS", "channel analysis", "report", "how are my ads doing", "cost per acquisition", "conversion data", "marketing dashboard", "ad spend", or any question about advertising metrics, campaign results, or channel comparison. Provides querying patterns and interpretation guidance for SegmentStream reports.
---

# Campaign Reports

Query and interpret campaign performance data from SegmentStream. This skill covers discovering available reports, fetching tabular and chart data, filtering and sorting results, and presenting actionable insights to the user.

## Key Tools

### Discovery

- **`list_active_projects()`** -- Retrieve the user's SegmentStream projects. Every subsequent call requires a `projectId`.
- **`list_conversions(projectId)`** -- List conversion definitions (e.g., Purchase, Lead, Signup). Each has an `id` and `name`.
- **`list_attribution_models(projectId)`** -- List attribution models (e.g., Last non-direct click, First click, ML-based). Each has an `id` and `name`.
- **`list_custom_dimensions(projectId)`** -- Discover project-specific custom dimensions (channel groupings, product categories, etc.). Custom dimensions use IDs like `custom_dimension_xxx`.

### Querying

- **`get_report_table(projectId, params)`** -- Primary tool. Fetch tabular data with dimensions, metrics, filters, date ranges, and sorting. Use `format: "csv"` (the default) for compact output.
- **`get_report_chart(projectId, params)`** -- Fetch time-series data for trend visualization. Supports granularity: Day, Week, Month, Hour.
- **`download_report_csv(projectId, params)`** -- Export data as a CSV file. Returns a job ID; poll with `get_download_job` for the download URL.
- **`get_report_dimension_values(projectId, ...)`** -- Retrieve available values for a dimension (useful for discovering filter options like campaign names or countries).

## Workflow

### Step 1 -- Resolve project

Before calling any SegmentStream MCP tool, verify tools are available via `ToolSearch`. If `mcp__segmentstream__*` tools are not found, stop and direct the user to run `/segmentstream:setup` which handles the MCP connectivity flow.

Call `list_active_projects()` to get the `projectId`. If the user has multiple projects, ask which one to use.

### Step 2 -- Determine conversion and attribution model

Report queries fall into two categories:

**Cost-only queries** (spend, CPC, impressions, clicks, sessions) do not require the user to choose a conversion or attribution model. Examples: "How much did we spend on Google Ads last month?", "What's our CPC trend?", "Show clicks by campaign." Skip straight to Step 3.

**Attribution-dependent queries** require a specific conversion and attribution model. This includes any query that involves ROAS, CPA, conversions, revenue, or any period-over-period performance comparison (week-over-week, month-over-month) — because comparing "performance" implicitly means comparing conversions and revenue, not just cost. Examples: "What's our ROAS by channel?", "Show conversions by campaign", "Which campaigns have the best CPA?", "How did we perform week over week?", "Compare this month to last month."

For attribution-dependent queries, resolve conversion and attribution model before building any query:

1. **Check saved defaults.** Read `.claude/segmentstream.local.md` and look for `defaults` in the active project's config (`conversionId`, `attributionModelId`). Resolve names by looking up the IDs in the project's `conversions` and `attributionModels` arrays.
2. **Propose or ask.** If defaults exist, propose them: "Your defaults are **Purchase** conversion with **ML Attribution** -- shall I use those?" If no defaults exist, call `list_conversions(projectId)` and `list_attribution_models(projectId)`, present the options, and ask the user to choose.
3. **Match explicit intent.** If the user's request names a conversion (e.g., "show me purchase ROAS"), match it and confirm rather than asking open-ended. Still confirm the attribution model.
4. **Never assume silently.** Even when reusing saved preferences, state the choice explicitly before running the query: "Using **Purchase** conversion with **ML Attribution** model."

For the complete dimension and metric vocabulary, see `references/dimensions-metrics.md`.

### Step 3 -- Choose dimensions and build the query

Include only the dimensions and metrics the user's question requires. Unnecessary fields increase response size and slow things down.

Default `date_range` to last 30 days if the user does not specify.

**Dimensions:**
- If the user specifies a breakdown (e.g., "by campaign", "by country"), use the corresponding dimension.
- If the user does not specify a breakdown, default to `channel` (Channel). For drill-down follow-ups, the natural secondary dimension is `campaign_name`.
- Before running the query, state the planned dimensions and confirm: "I'll break this down by **Channel** (`channel`). Want a different breakdown?"
- "Total conversions" with no breakdown is valid -- use zero dimensions, but confirm that's intended.

**Metrics go into two separate arrays** -- `attribution_metrics` (traffic/cost data like `cost`, `clicks`, `cpc`) and `conversion_metrics` (attributed data like `conversions`, `roas`, `cpa`). The tool schema has the full list of allowed values for each.

**`attributed_conversions` is required** when requesting any `conversion_metrics`. Always specify `conversion_metrics` explicitly -- omitting it returns all available metrics, producing oversized responses.

### Step 4 -- Present results

Parse the response and present data in a clear table format. Always add interpretation and actionable insights -- do not just dump raw numbers. Suggest follow-up analyses when relevant.

### Step 5 -- Save preferences

After a successful attribution-dependent report, update the active project's `defaults` in `.claude/segmentstream.local.md` with the `conversionId` and `attributionModelId` that were used. This ensures the next report query can propose them as defaults. Only update if the user explicitly chose or confirmed -- do not save unconfirmed defaults.

## Common Query Patterns

### Channel performance overview

Break down by `channel` to compare cost, conversions, and ROAS across channels. Start here for a high-level view before drilling into specific campaigns.

### Campaign deep-dive

Break down by `campaign_name` with filters on `ad_platform` to see which campaigns within a platform are performing best. Sort by cost (descending) to focus on the biggest spenders.

### Period-over-period comparison

Use `comparison_date_range` alongside `date_range` to compare two time periods. The response includes both intervals, making it easy to calculate changes. Useful for "how did this month compare to last month?" questions.

### Daily trends

Use `get_report_chart` with the desired granularity (`day`, `week`, `month`) to see how metrics evolve over time. Ideal for spotting spend anomalies, conversion drops, or seasonal patterns.

### Country or region breakdown

Use `country` or `region` as a dimension to see geographic performance. Combine with filters to focus on specific markets.

### Device analysis

Use `device` as a dimension to compare performance across desktop, mobile, and tablet.

## Filters and Sorting

The `get_report_table` tool schema documents the full filter and sorting syntax, including all operators and structure. Key tips:

- Use `get_report_dimension_values` to discover available filter values when unsure of exact spellings.
- Combine filter conditions with `{ "and": [...] }` or `{ "or": [...] }`.
- When sorting by conversion metrics, `attributed_conversion_id` must match an `id` from `attributed_conversions`.

## Interpreting Attribution Data

### ML-attributed conversions vs last-click

SegmentStream uses machine learning to attribute conversions across the full customer journey, not just the last click. This means numbers will differ from what ad platforms report. ML attribution typically assigns more credit to upper-funnel channels (display, video, social) and less to bottom-funnel channels (brand search, retargeting) compared to last-click.

### ROAS interpretation

What counts as "good" ROAS depends entirely on profit margins and the business model. A 5x ROAS might be excellent for a high-margin SaaS product but barely break-even for a low-margin retailer. Always consider the business context before making recommendations.

Do not compare ML-attributed ROAS directly with platform-reported ROAS (Google Ads, Meta, etc.). The two use fundamentally different attribution methodologies and will rarely align.

### Event-time vs conversion-time attribution

Metrics come in two flavors:
- **Event-time** (`conversions`, `conversion_value`, `roas`) -- attributes the conversion to the date it occurred.
- **Conversion-time** (`conversions_by_conv_time`, `conversion_value_by_conv_time`) -- attributes the conversion to the date of the converting session.

Event-time is more intuitive for day-to-day reporting. Conversion-time is useful for evaluating campaign launch effectiveness.

### Cost data completeness

Some advertising platforms have delayed cost imports. If recent days show zero cost but have clicks/sessions, the cost data may not have synced yet. Flag this to the user rather than drawing conclusions from incomplete data.

## Best Practices

1. **Always specify date ranges.** Default to the last 30 days if the user does not specify.
2. **Start broad, then drill down.** Begin with channel-level performance, then zoom into campaigns or ad groups based on what stands out.
3. **Add interpretation.** Raw numbers without context are not useful. Explain what the data means and what actions to consider.
4. **Use tables for comparisons.** Structured tables make it easy to compare channels, campaigns, or time periods.
5. **Suggest follow-ups.** After presenting results, suggest the next analysis that would deepen the insight.
6. **Request only needed fields.** Keep queries minimal -- fewer dimensions and metrics mean faster, more focused results.

## References

For the complete list of available dimensions and metrics with descriptions, example values, and usage guidance, consult `references/dimensions-metrics.md`.
