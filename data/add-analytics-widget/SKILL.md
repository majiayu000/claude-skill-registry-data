---
name: add-analytics-widget
description: Add an analytics chart or metric card to a dashboard or report page. Handles the API aggregation query, react-query hook, and Recharts visualization. Use when building analytics features.
---

# add-analytics-widget

Creates a complete analytics widget: backend aggregation query → API endpoint → react-query hook → Recharts visualization. Follows the project's chart conventions (ChartContainer, design tokens).

## Inputs to gather

- **Widget name** — e.g., "revenue-by-source", "lead-conversion-funnel", "agent-radar"
- **Chart type** — bar, line, area, pie, radar, table, KPI card
- **Data source** — which tables to query (leads, deals, properties, etc.)
- **Dimensions** — group by what (source, agent, month, city, stage)
- **Measures** — count, sum, avg on which fields
- **Target page** — where to display (dashboard, reports, team, custom)

## Steps

1. **Create the API endpoint** at the relevant route file:
   ```typescript
   router.get("/analytics/{widget-name}", authenticateToken, async (req, res) => {
     const orgId = req.user?.organizationId;
     const period = req.query.period as string || "month";
     // Prisma groupBy or raw SQL aggregation
     const data = await prisma.deals.groupBy({
       by: ["stage"],
       where: { organizationId: orgId, createdAt: { gte: periodStart } },
       _count: true,
       _sum: { agreedPrice: true },
     });
     res.json(data);
   });
   ```

2. **Create the react-query hook** using `/add-react-query`.

3. **Build the chart component:**
   ```tsx
   import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
   import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
   import { CHART_COLORS } from "@/config/design-tokens";
   ```

4. **Follow chart conventions:**
   - Wrap in `<ChartContainer config={{} as ChartConfig}>` 
   - Use `CHART_COLORS` from design tokens — never hardcode colors
   - Use `<ChartTooltip content={<ChartTooltipContent />} />` — never nest tooltips
   - Set `style={{ direction: "ltr" }}` on chart container (Recharts is LTR)
   - Arabic labels in tooltips and legends

5. **Add to the target page** inside a Card with CardHeader + CardTitle.

## Verification checklist

- [ ] API returns correct aggregated data
- [ ] Chart renders with correct data
- [ ] Uses design tokens for colors (not hardcoded)
- [ ] Chart tooltips work (hover shows values)
- [ ] Responsive: chart resizes on window change
- [ ] RTL: chart container has `direction: ltr`, labels are Arabic
- [ ] `/typecheck` passes

## Anti-patterns

- Don't nest `<ReTooltip>` inside `<ChartTooltip>` — use `<ChartTooltip content={<ChartTooltipContent />} />` directly
- Don't use `ResponsiveContainer` manually — `ChartContainer` already includes it
- Don't hardcode hex colors — use `CHART_COLORS` or `CHART_COLOR_ARRAY`
- Don't run expensive aggregations without date filtering — always accept a period parameter
