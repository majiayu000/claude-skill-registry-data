---
name: design
description: Use when styling Fusionaly UI components, pages, or charts - applies the Fusionaly design system with black/white palette and brand accents
---

# Fusionaly Design System

## Philosophy

Clean, minimal, professional. Black and white foundation with purposeful color accents. No gray noise - use black with opacity for subtlety.

## Color Palette

### Primary

| Name | Value | Usage |
|------|-------|-------|
| **Black** | `#000000` | Text, borders, buttons, backgrounds |
| **White** | `#FFFFFF` | Backgrounds, text on dark |

### Brand Accents

| Name | Value | Tailwind | Usage |
|------|-------|----------|-------|
| **Green** | `#00D678` | `text-[#00D678]` | Success, growth, positive metrics, SQL syntax |
| **Cyan** | `#00D1FF` | `text-[#00D1FF]` | Links, charts, data visualization |
| **Orange** | `#FF7733` | `text-[#FF7733]` | Warnings, alerts, third chart color |

### Opacity Scale (NO gray-* classes)

| Instead of | Use |
|------------|-----|
| `bg-gray-50` | `bg-black/5` |
| `bg-gray-100` | `bg-black/5` or `bg-black/10` |
| `bg-gray-200` | `bg-black/10` |
| `text-gray-400` | `text-black/40` |
| `text-gray-500` | `text-black/50` or `text-black/60` |
| `text-gray-600` | `text-black/60` or `text-black/70` |
| `text-gray-700` | `text-black/70` or `text-black/80` |
| `border-gray-200` | `border-black/10` |
| `border-gray-300` | `border-black/20` |
| `hover:bg-gray-50` | `hover:bg-black/5` |

## Components

### Buttons

```tsx
// Primary (solid black)
<Button className="bg-black text-white hover:bg-black/80">
  Action
</Button>

// Secondary (outline)
<Button variant="outline" className="border-black text-black hover:bg-black hover:text-white">
  Secondary
</Button>

// Ghost
<Button variant="ghost" className="text-black/60 hover:text-black hover:bg-black/5">
  Ghost
</Button>

// Disabled
<Button disabled className="bg-black/20 text-black/40 cursor-not-allowed">
  Disabled
</Button>
```

### Cards

```tsx
// Standard card
<div className="bg-white border border-black rounded-lg overflow-hidden">
  <div className="px-6 py-4 border-b border-black/10">
    <h3 className="text-base font-medium text-black">Title</h3>
  </div>
  <div className="p-4">
    Content
  </div>
</div>
```

### Form Inputs

```tsx
<input
  className="w-full border border-black/20 rounded-lg px-3 py-2 text-sm
             focus:outline-none focus:border-black focus:ring-1 focus:ring-black
             disabled:bg-black/5 disabled:cursor-not-allowed"
/>
```

### Code Blocks (SQL)

```tsx
// SQL display - green on black
<pre className="bg-black rounded p-3 overflow-x-auto font-mono text-xs leading-relaxed text-[#00D678] whitespace-pre-wrap">
  {sql}
</pre>
```

### Tables

```tsx
<table className="w-full border-collapse">
  <thead>
    <tr className="border-b border-black/10 bg-black/5">
      <th className="py-2 px-3 text-left text-xs font-medium text-black/60 uppercase tracking-wider">
        Header
      </th>
    </tr>
  </thead>
  <tbody className="bg-white divide-y divide-black/10">
    <tr className="hover:bg-black/5">
      <td className="py-2 px-3 text-sm">Cell</td>
    </tr>
  </tbody>
</table>
```

### Collapsible Details

```tsx
<details className="group">
  <summary className="cursor-pointer text-xs text-black/50 hover:text-black flex items-center font-medium outline-none">
    <svg className="w-3 h-3 mr-1.5 group-open:rotate-90 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
    View Details
  </summary>
  <div className="mt-3 p-3 bg-black/5 rounded-lg">
    Content
  </div>
</details>
```

## Charts

### Color Sequence

```tsx
const CHART_COLORS = ["#00D1FF", "#00D678", "#FF7733"];

const getDynamicColor = (index: number): string => {
  return CHART_COLORS[index % CHART_COLORS.length];
};
```

### Recharts Styling

```tsx
<BarChart data={data}>
  <CartesianGrid strokeDasharray="3 3" opacity={0.4} />
  <XAxis
    tick={{ fill: "#374151", fontSize: 10 }}
  />
  <YAxis
    tick={{ fill: "#374151", fontSize: 10 }}
    allowDecimals={false}
  />
  <Tooltip
    contentStyle={{
      backgroundColor: "#FFFFFF",
      border: "1px solid #E5E7EB",
      borderRadius: "6px",
      boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.1)",
    }}
  />
  <Bar dataKey="value" fill="#00D678" />
</BarChart>
```

## Chip/Tag Buttons

```tsx
// Example question chips
<button className="text-xs px-3 py-1.5 bg-black text-white hover:bg-black/80 rounded transition-colors">
  Example
</button>

// Follow-up suggestion chips
<button className="text-xs px-3 py-1.5 border border-black/20 text-black hover:border-black hover:bg-black/5 rounded transition-colors">
  Suggestion
</button>
```

## Typography

| Element | Classes |
|---------|---------|
| Page title | `text-2xl font-bold text-black` |
| Section header | `text-sm font-medium text-black/70 uppercase tracking-wide` |
| Card title | `text-base font-medium text-black` |
| Body text | `text-sm text-black` |
| Muted text | `text-sm text-black/60` |
| Small muted | `text-xs text-black/50` |

## Icons

Use Lucide React icons. Size conventions:

| Context | Size |
|---------|------|
| Button inline | `h-3.5 w-3.5` |
| Action button | `h-4 w-4` |
| Section header | `h-5 w-5` or `h-6 w-6` |

## Spacing

- Card padding: `px-6 py-4` (header), `p-4` or `p-6` (content)
- Section gaps: `gap-4` or `gap-6`
- Inline element gaps: `gap-1`, `gap-1.5`, `gap-2`

## Don'ts

- No `gray-*` classes - use `black/*` opacity
- No colored backgrounds for cards - use white with black border
- No gradients
- No shadows except subtle on selected states (`shadow-sm`)
- No decorative colors - accents are functional
