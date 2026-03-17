# Quality Scenarios for html-report Skill

## How to Use

Run each scenario WITH and WITHOUT the skill loaded. Compare outputs.
- WITHOUT: `claude -p "<scenario>" --no-skills`
- WITH: `claude -p "<scenario>"`

Check outputs against the acceptance criteria for each scenario.

## Scenario 1: Basic Channel Report
**Prompt:** "Generate a performance report for last month showing Google Ads, Meta Ads, and TikTok by channel with cost, sessions, conversions, CPA, and ROAS"

**Acceptance Criteria:**
- [ ] Uses dark theme (black background, #0A0A0A content area)
- [ ] KPI cards for totals (3-4 cards in a row)
- [ ] Comparison table with current vs previous period
- [ ] Delta badges with correct color semantics (green=good, red=bad, CPA decrease=green)
- [ ] Channel icons for ad platforms (inline SVG, not text placeholders)
- [ ] Mono font for all numeric data
- [ ] SegmentStream branding (logo, "Generated via SegmentStream MCP" footer)
- [ ] Self-contained HTML (no external CSS/font/script imports)

## Scenario 2: Chart + Table Combination
**Prompt:** "Create a report with a timeseries chart showing daily cost trend for the last 30 days, plus a campaign-level breakdown table"

**Acceptance Criteria:**
- [ ] Chart uses correct color palette (#6366F1 primary, grid stroke rgba(255,255,255,0.04))
- [ ] Chart rendered as inline SVG (HTML) or Recharts (JSX)
- [ ] Axis labels use mono font, font-size 10, fill #555
- [ ] Legend row above the chart with colored swatches
- [ ] Table uses .data-table class with proper header/body styling
- [ ] Numeric columns right-aligned with .num class
- [ ] Both components wrapped in proper containers (.chart-wrapper, .data-table-wrapper)

## Scenario 3: Minimal Report (Edge Case)
**Prompt:** "Just show me total cost and ROAS for last week, nothing fancy"

**Acceptance Criteria:**
- [ ] Still uses the full report frame (topbar, bottombar)
- [ ] Uses KPI cards even for just 2 metrics
- [ ] Doesn't skip branding or dark theme
- [ ] No unnecessary components (no table if not asked for)
- [ ] File saved to .artifacts/ with descriptive filename

## Scenario 4: JSX Format
**Prompt:** "Generate a React component showing channel performance with a bar chart and comparison table"

**Acceptance Criteria:**
- [ ] Uses Recharts for charts (not inline SVG)
- [ ] Tailwind classes for styling (bg-black, bg-[#0A0A0A], etc.)
- [ ] Single default export function
- [ ] Dark theme via Tailwind
- [ ] All data hardcoded inside component (no fetch calls)
- [ ] No external imports except pre-loaded libraries (React, Recharts, shadcn/ui, Lucide)
- [ ] Top bar with title and date, bottom bar with SegmentStream attribution
- [ ] Mono font on numeric values (font-mono class)

## Scenario 5: Comparison Report (Period-over-Period)
**Prompt:** "Create a month-over-month comparison report showing how each channel performed this month vs last month"

**Acceptance Criteria:**
- [ ] Comparison table with current value and previous value visible per metric
- [ ] Delta badges/tags with percentage change
- [ ] Correct color semantics for inverted metrics (CPA up = bad = red, CPA down = good = green)
- [ ] Total/summary row at top or bottom with heavier visual separation
- [ ] KPI cards at top showing aggregated totals with change indicators
- [ ] Channel icons for ad platforms in table rows

## Scenario 6: Drill-Down Report
**Prompt:** "Show channel performance with expandable rows - click a channel to see its campaigns"

**Acceptance Criteria:**
- [ ] Uses interactive expand/collapse mechanism (details/summary or JS toggle)
- [ ] Chevron or indicator rotates/changes on expand
- [ ] Channel icons in parent rows
- [ ] Campaign rows indented or visually nested under parent channel
- [ ] Parent row shows aggregated channel metrics
- [ ] Expanded campaigns show individual campaign metrics
- [ ] Consistent dark theme and mono font for all numeric data
