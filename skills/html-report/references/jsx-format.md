# JSX Report Format (Cowork)

Generate a single-file React component. Cowork renders it inline with React 18, Tailwind CSS, shadcn/ui, Lucide, and charting libraries pre-loaded.

## Brand Identity

Apply these constraints. Everything else — layout, spacing, component choice — use your best design judgment with the available libraries.

**Color palette (dark theme):**
- Background: `bg-black` (page), `bg-[#0A0A0A]` (content area), `bg-[#111]` (cards/headers)
- Text: `text-[#EDEDED]` (primary), `text-[#888]` (secondary), `text-[#555]` (muted)
- Accent: `text-indigo-500` / `bg-indigo-500` — used sparingly for interactive elements and key highlights
- Borders: `border-white/[0.08]` (default), `border-white/[0.15]` (hover)
- Status: `text-emerald-400` (positive), `text-red-400` (negative), `text-amber-400` (warning)

**Typography:**
- Body text: default sans-serif (Tailwind's `font-sans`)
- Data values, KPI numbers, table headers: `font-mono`
- Table body: first column (labels/names) stays sans-serif, numeric columns use `font-mono`

**Frame:**
- Top bar: `bg-[#111]` with report title left, date right, border-b
- Bottom bar: `bg-[#111]` with "Generated via SegmentStream MCP" in small mono uppercase, border-t
- Content area: `bg-[#0A0A0A]`, max-w `1200px` centered

## Charts

Four charting libraries are available. Pick the best fit for each visualization:

| Library | Import | Best For |
|---------|--------|----------|
| **Recharts** (default) | `import { LineChart, XAxis, ... } from "recharts"` | Standard line/bar/area/pie — React-native, declarative |
| **D3** | `import * as d3 from "d3"` | Custom/non-standard visualizations — heatmaps, Sankey, force graphs |
| **Plotly** | `import * as Plotly from "plotly"` | Interactive dashboards — hover, zoom/pan, scatter, 3D |
| **Chart.js** | `import * as Chart from "chart.js"` | Canvas-based — performant for large datasets (1000+ points) |

**Default to Recharts** for most reports. Use D3/Plotly/Chart.js only when the visualization genuinely needs their capabilities.

### Recharts dark theme config

- Grid: `stroke="rgba(255,255,255,0.04)"`
- Axis ticks: `fontSize: 10, fill: '#555'`
- Tooltip: dark background (`#111`), subtle border

**Color rule: every line/series must be a distinct color.** Never reuse a color, even with different dash patterns.
- Primary metric: `#6366F1` (indigo)
- Positive/actual: `#10B981` (green)
- Projected/estimated: `#F59E0B` (amber)
- Negative: `#EF4444` (red)
- Comparison/previous: `#888` dashed

## Channel Icons

Read `references/channel-icons.md` for inline SVG icons of ad platforms. Only ad platforms (Google Ads, Meta, Microsoft, TikTok, LinkedIn, Pinterest, Reddit, X, Snapchat, Awin) get icons. Other channels (Organic Search, Direct, Email, etc.) render as plain text.

## Constraints

- `export default function ComponentName()` — single file, no local imports
- All data hardcoded as arrays/objects inside the component
- No localStorage, no fetch, no external API calls
- Available: React 18, Tailwind, Recharts, D3, Plotly, Chart.js, shadcn/ui, Lucide
