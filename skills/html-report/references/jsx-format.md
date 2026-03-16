# JSX Report Format (Cowork)

Generate a single-file React component. Cowork renders it inline with React 18, Tailwind CSS, Recharts, shadcn/ui, and Lucide pre-loaded.

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

## Charts (Recharts)

Use Recharts for any timeseries or comparison charts. Dark theme config:
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
- Available: React 18, Tailwind, Recharts, shadcn/ui, Lucide
