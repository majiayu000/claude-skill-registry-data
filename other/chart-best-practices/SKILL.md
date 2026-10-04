---
name: chart-best-practices
description: Generate chart JSON blocks for dashboard rendering. Use when visual comparisons help explain data — quality rankings, cost comparisons, Pareto frontiers.
---

# Chart Best Practices Skill

Charts render from JSON code blocks. Three supported schemas:

## Bar / Line
```json
{
  "type": "bar",
  "labels": ["Model A", "Model B", "Model C"],
  "datasets": [{"label": "Quality (0-100)", "data": [53, 51, 48]}]
}
```
- `labels` and `datasets[].data` must be the same length
- Use `"type": "line"` for trends over time

## Scatter (Pareto frontier, quality-vs-cost)
```json
{
  "type": "scatter",
  "datasets": [{
    "label": "Models",
    "data": [
      {"x": 25.0, "y": 53, "label": "Claude Opus 4.6"},
      {"x": 5.0,  "y": 51, "label": "Claude Sonnet 4.6"},
      {"x": 1.5,  "y": 47, "label": "GPT-4o"}
    ]
  }]
}
```
- No `labels` array needed — each point carries its own `label`
- Tooltip auto-shows the point's `label` field
- `x` = cost/speed, `y` = quality score

## Log-scale scatter (cost spans orders of magnitude)
Add `options.scales` to switch any axis to log scale:
```json
{
  "type": "scatter",
  "options": {
    "scales": {
      "x": {"type": "log", "min": 0.1},
      "y": {"beginAtZero": true}
    }
  },
  "datasets": [{"label": "Models", "data": [{"x": 0.2, "y": 40, "label": "Cheap model"}, {"x": 25, "y": 53, "label": "Expensive model"}]}]
}
```

## Rules
1. **No callback functions** — `"callback": "value => ..."` will be stripped. Use static `min`/`max`/`beginAtZero` instead.
2. **No `plugins.tooltip.callbacks`** — tooltips on scatter use the `label` field automatically.
3. Keep labels short. Use `data[].label` on scatter points for hover text.
4. Prefer bar/line for ranked comparisons, scatter for two-metric trade-offs (Pareto).
5. Always include text explanation — never emit a chart as the only output.
