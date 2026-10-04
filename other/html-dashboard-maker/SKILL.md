---
name: html-dashboard-maker
description: "Designs and builds interactive dashboards as a single self-contained HTML file with charts, KPI cards, filters, drill-down, responsive layout, and polished styling, which runs without a server and can be shared as one file. Plans audience, key questions, chart types, and layout before coding, using only data the user provides. Use when the user asks for a dashboard, KPI overview, metrics page, interactive report, or wants their data turned into shareable charts in HTML."
---

# HTML Dashboard Maker

You design and build interactive dashboards that live in one HTML file: charts, filters, a responsive layout, and clean professional styling, with no server needed and nothing to install, so the user can pass the file around as is. The data and the business context always come from the user. Work out what the dashboard has to show before you touch any code, because choosing the right visuals first is what saves costly rework later.

Run through the stages below for every dashboard request, in order.

## Stage 1: Pin down the requirements

Get clarity on these points before you build:

- **Who reads it.** Executives want headlines and trends, analysts want filters and drill-down, and operations teams want live status.
- **What it must answer.** Agree on the 3-5 questions the dashboard exists to answer. Tie every chart to at least one of them; a chart that answers nothing is just visual clutter.
- **Where the data comes from.** Find out what data exists, how often it is updated, and whether this is a one-off snapshot or something that will refresh.
- **How interactive it should be.** A static view, a filterable one, or full interactivity with cross-filtering.
- **How it will be shared.** As a file, embedded in a page, or shown in a meeting.

## Stage 2: Match each chart to the data relationship

Picking the wrong chart type is the most frequent dashboard mistake. Use this lookup:

| What the data shows | Use | Don't use |
|---|---|---|
| **Change over time** (continuous) | Line chart | Pie chart; bar chart across many time periods |
| **Comparison between categories** | Bar chart, horizontal when labels are long, otherwise vertical | Pie chart with more than 5 categories |
| **Share of a total**, few categories (≤5) | Donut chart or stacked bar | Pie chart with lots of thin slices |
| **Share of a total**, many categories | Stacked bar or treemap | Pie chart |
| **Distribution** of one variable | Histogram or box plot | Bar chart of the raw values |
| **Correlation** between two variables | Scatter plot | Dual-axis line chart (misleading) |
| **Ranking** | Horizontal bar chart sorted from highest to lowest | Bar charts left unsorted |
| **One KPI or headline figure** | Big-number card with a trend indicator | Any chart; it's overkill for one value |
| **Geography** | Choropleth or bubble map | Tables of region codes |
| **Flow or funnel** | Funnel chart or Sankey diagram | Stacked bar |

Rules that never bend:

- No 3D charts, ever. They warp perception and contribute no information.
- No dual-axis charts unless both axes are clearly labeled and both begin at zero. Most of them mislead, suggesting a correlation that is really an artifact of arbitrary scaling.
- Bar and area charts always have axes that begin at zero, because a truncated axis exaggerates differences.
- Spend color on purpose: use it to highlight the signal, not to decorate. Keep red/amber/green for genuine status indicators only.

## Stage 3: Lay out the page

Structure the page as an inverted pyramid, with the most important content at the top:

1. **KPI cards:** 3-6 headline metrics, each with a trend indicator (↑ ↓ →), so the reader can tell at a glance how things stand right now.
2. **Primary charts:** 1-2 large charts that address the most important questions, such as the main trend, the main comparison, or the primary breakdown.
3. **Supporting charts:** 2-4 smaller charts that add context, drill-down, or secondary dimensions.
4. **Detail table** (optional): a filterable table for readers who want to see the underlying numbers.

Keep these layout principles in mind:

- Cap the dashboard at 8-10 visual elements. Beyond that, nothing stands out.
- Place related charts next to each other, grouping them by topic rather than by chart type.
- Align widths consistently on a grid of 2, 3, or 4 columns.
- Treat white space as something that helps. A crowded dashboard communicates nothing clearly.

## Stage 4: Build the HTML file

Deliver one self-contained HTML file that relies only on technologies native to the browser.

**Charts.** Default to Chart.js loaded from a CDN for standard charts; it is light, thoroughly documented, and covers most dashboard needs. For more complex visuals (Sankey, treemap, geographic), use the matching Chart.js plugin or D3.js.

**Skeleton:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Dashboard Title]</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>/* All styles inline */</style>
</head>
<body>
  <!-- KPI cards -->
  <!-- Charts -->
  <!-- Filters -->
  <script>/* All logic inline */</script>
</body>
</html>
```

**Default styling**, unless the user asks for something else:

| Element | Default |
|---|---|
| Typeface | The native system stack, `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` |
| Backgrounds | `#f8f9fa` (light gray) for the page, `#ffffff` for the chart cards |
| Card shadow | `box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.06)` |
| Colors | A sequential or categorical palette with enough contrast; the default categorical set is `['#2563eb', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#0891b2']` |
| Dark mode | A `prefers-color-scheme: dark` media query that inverts the backgrounds and adjusts the chart colors |
| Responsiveness | CSS grid or flexbox, with breakpoints at 768px and 1200px |

## Stage 5: Layer in interactivity

Add interaction in tiers, going as far as the Stage 1 requirements call for.

**Tier 1, tooltips (include them every time)**
- Hovering over or tapping any data point reveals its exact value, its label, and its context.
- Numbers are shown with sensible precision and locale-aware separators.

**Tier 2, filters (include them when the data has dimensions worth slicing)**
- Dropdown or toggle filters on the key dimensions, such as date range, category, or segment.
- A filter change updates every chart at once (cross-filtering).
- The active filter state is always clearly visible, so the reader knows exactly what they are looking at.
- A "Reset filters" action is available.

**Tier 3, drill-down (include it for audiences who care about detail)**
- Clicking a chart element filters the other charts to that value.
- An expandable data table sits below the charts.

**Filter pattern to implement:**
```javascript
const rawData = [/* full dataset */];
let filteredData = [...rawData];

function applyFilters() {
  filteredData = rawData.filter(row => {
    // Apply each active filter
    return matchesAllFilters(row);
  });
  updateAllCharts(filteredData);
}
```

Keep the complete dataset in JavaScript and do the filtering in the browser. Up to 50,000 rows, any modern browser handles this without performance trouble.

## Formatting numbers and dates

Apply the same formatting everywhere on the dashboard:

- **Currency:** the locale's symbol, 2 decimal places, and a thousands separator, e.g. €1,234.56.
- **Percentages:** 1 decimal place with a % sign, e.g. 12.3%.
- **Large numbers:** shortened with a suffix, e.g. 1.2M or 45.6K.
- **Dates:** chosen for the audience, ISO for technical readers and a localized form for business readers, e.g. 2025-03-15 or 15 Mar 2025.
- **Negative values:** parentheses or a minus sign, whichever you choose, used consistently, e.g. (1,234) or -1,234.
- **Null or missing values:** an explicit label and never an empty cell, e.g. "No data" or "—".

## Patterns you decline to build

Don't produce any of the following unless the user explicitly asks for it and accepts the drawback:

| Pattern | What's wrong with it | Do this instead |
|---|---|---|
| **Rainbow color schemes** | Color carries meaning, so arbitrary colors only add noise | Sequential palette for ordered data, categorical palette for groups |
| **Pie charts with more than 5 slices** | People can't compare the angles of small slices accurately | Horizontal bar chart |
| **Dual-axis charts** | Two arbitrary y-axis scales suggest a correlation that isn't there | Two separate charts, or normalize both to a common scale |
| **No title or date on the dashboard** | Once a screenshot is shared, the context is gone | Always show the dashboard title, the data-as-of date, and the active filters |
| **Unlabeled axes** | Readers are left guessing what the numbers mean | Give every axis a name and a unit |
| **Truncated y-axis on bar charts** | Small differences look big | Begin bar and area charts at zero |
| **Too many decimals** | Something like "Revenue: $1,234,567.89" on a chart spanning $10M | Round to a precision that means something |

## Ground rules

- Never make up data. If the user hasn't supplied data yet, build the dashboard structure with placeholder labels.
- Never pull in external resources apart from CDN-hosted charting libraries (Chart.js, D3.js). Once loaded, the dashboard has to keep working offline.
- Always show the data-as-of date; without one, nobody can judge how reliable the dashboard is.
- Tag what you deliver: `[From user data]` for sourced values, `[Design recommendation]` for layout guidance, and `[Placeholder — replace with your data]` for anything still waiting on real data.
