# JSX Report Format (Cowork)

When running in Cowork, generate a single-file React component instead of an HTML file. Cowork renders JSX artifacts inline with React 18, Tailwind CSS, Recharts, shadcn/ui, and Lucide icons pre-loaded.

## Component Structure

```jsx
export default function ReportName() {
  // Data arrays defined inline
  const channelData = [ ... ];
  const dailyData = [ ... ];

  return (
    <div className="min-h-screen bg-black text-[#EDEDED] font-sans">
      {/* Top bar */}
      <div className="flex items-center justify-between px-5 py-2.5 bg-[#111] border-b border-white/[0.08]">
        <span className="text-xs font-medium">Report Title</span>
        <span className="text-[10px] font-mono text-[#555] uppercase tracking-wider">16 March 2026</span>
      </div>

      {/* Report body */}
      <div className="max-w-[1200px] mx-auto">
        {/* Sections go here */}
      </div>

      {/* Bottom bar */}
      <div className="px-5 py-2 bg-[#111] border-t border-white/[0.08]">
        <span className="text-[10px] font-mono text-white/30 uppercase tracking-wider">Generated via SegmentStream MCP</span>
      </div>
    </div>
  );
}
```

## Design Tokens (Tailwind classes)

Map the HTML template's CSS variables to Tailwind:

| Token | Tailwind class |
|---|---|
| `--bg-primary` (#000) | `bg-black` |
| `--bg-secondary` (#0A0A0A) | `bg-[#0A0A0A]` |
| `--bg-code` (#111) | `bg-[#111]` |
| `--text-primary` (#EDEDED) | `text-[#EDEDED]` |
| `--text-secondary` (#888) | `text-[#888]` |
| `--text-muted` (#555) | `text-[#555]` |
| `--accent` (#6366F1) | `text-indigo-500` or `text-[#6366F1]` |
| `--border` | `border-white/[0.08]` |
| `--positive` (#10B981) | `text-emerald-400` |
| `--negative` (#EF4444) | `text-red-400` |
| `--warning` (#F59E0B) | `text-amber-400` |

## Component Patterns

### KPI Grid

```jsx
const kpis = [
  { label: 'Ad Spend', value: '£38.8k', change: '+2% YoY', type: 'neutral' },
  { label: 'Sessions', value: '218k', change: '+79% YoY', type: 'positive' },
];

<div className="flex flex-wrap gap-3 justify-center my-6">
  {kpis.map(kpi => (
    <div key={kpi.label} className="flex-[0_1_calc(33.333%-8px)] min-w-[200px] bg-[#111] border border-white/[0.08] rounded-xl p-5">
      <div className="text-[9px] font-mono uppercase tracking-widest text-white/30 mb-2">{kpi.label}</div>
      <div className="text-2xl font-semibold font-mono tracking-tight">{kpi.value}</div>
      <div className={`text-[11px] font-mono mt-1.5 ${
        kpi.type === 'positive' ? 'text-emerald-400' :
        kpi.type === 'negative' ? 'text-red-400' : 'text-[#555]'
      }`}>{kpi.change}</div>
    </div>
  ))}
</div>
```

### Data Table

```jsx
<div className="bg-[#111] border border-white/[0.08] rounded-xl overflow-hidden my-4">
  <table className="w-full text-[13px]">
    <thead>
      <tr className="border-b border-white/[0.08]">
        <th className="text-left px-4 py-3 text-[10px] font-mono font-medium uppercase tracking-wider text-white/30">Channel</th>
        <th className="text-right px-4 py-3 text-[10px] font-mono font-medium uppercase tracking-wider text-white/30">Cost</th>
      </tr>
    </thead>
    <tbody>
      {rows.map(row => (
        <tr key={row.name} className="border-b border-white/[0.02] hover:bg-[#161616]">
          <td className="px-4 py-2.5">{row.name}</td>
          <td className="px-4 py-2.5 text-right font-mono">{row.cost}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

Note: First column (channel names) uses sans-serif (default). Numeric columns add `font-mono`.

### Timeseries Chart (Recharts)

Recharts is pre-loaded in Cowork. Import from the global scope:

```jsx
const { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } = Recharts;

<div className="bg-[#111] border border-white/[0.08] rounded-xl p-5 my-4">
  <ResponsiveContainer width="100%" height={280}>
    <LineChart data={dailyData}>
      <CartesianGrid stroke="rgba(255,255,255,0.04)" />
      <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#555' }} />
      <YAxis yAxisId="left" tick={{ fontSize: 10, fill: '#555' }} />
      <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 10, fill: '#10B981' }} />
      <Tooltip
        contentStyle={{ background: '#111', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8, fontSize: 12 }}
        labelStyle={{ color: '#888' }}
      />
      <Legend />
      <Line yAxisId="left" type="monotone" dataKey="sessions" stroke="#6366F1" strokeWidth={2} dot={{ r: 3 }} name="Sessions" />
      <Line yAxisId="right" type="monotone" dataKey="conversions" stroke="#10B981" strokeWidth={2} dot={{ r: 3 }} name="Conv. observed" />
      <Line yAxisId="right" type="monotone" dataKey="projected" stroke="#F59E0B" strokeWidth={1.5} strokeDasharray="6 4" dot={{ r: 2 }} name="Conv. projected" />
    </LineChart>
  </ResponsiveContainer>
</div>
```

Chart color rule: every line must be a **distinct color**. Never use the same color for two series.

### Callout

```jsx
<div className={`bg-[#111] border border-white/[0.08] border-l-[3px] rounded-r-xl p-4 my-5 ${
  type === 'positive' ? 'border-l-emerald-400' :
  type === 'negative' ? 'border-l-red-400' :
  type === 'warning' ? 'border-l-amber-400' : 'border-l-indigo-500'
}`}>
  <div className="font-semibold text-sm mb-1">{title}</div>
  <div className="text-sm text-[#888] leading-relaxed">{body}</div>
</div>
```

### Tag

```jsx
<span className={`inline-block font-mono text-[11px] px-2 py-0.5 rounded ${
  type === 'positive' ? 'bg-emerald-400/10 text-emerald-400' :
  type === 'negative' ? 'bg-red-400/10 text-red-400' :
  type === 'warning' ? 'bg-amber-400/10 text-amber-400' : 'bg-indigo-500/15 text-indigo-500'
}`}>{value}</span>
```

### Progress Bar (Maturation)

```jsx
<div className="w-[72px] h-1.5 bg-white/[0.04] rounded-full overflow-hidden inline-block align-middle ml-2">
  <div className="h-full rounded-full bg-indigo-500" style={{ width: `${percent}%` }} />
</div>
```

## Channel Icons

For ad platform icons in JSX, use Lucide icons as approximations or inline SVG paths from `references/channel-icons.md`. Wrap in a flex container:

```jsx
<td>
  <div className="flex items-center gap-2">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="#4285F4">...</svg>
    <span>P Max - Google Ads</span>
  </div>
</td>
```

## Constraints

- Single file only — no imports from local paths
- No localStorage/sessionStorage
- No external API calls or fetch
- Available libraries: React 18, Tailwind, Recharts, shadcn/ui, Lucide
- All data must be hardcoded in the component
