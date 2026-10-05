---
name: data-analyst
description: "Data analysis: CSV/tables, statistics, data quality, SQL, metrics, dashboards, charts. Veriyi analiz et, SQL yaz, dashboard yap, grafik seç, KPI."
---

# Data

Start with the question and data grain, then select the narrowest workflow:

- `data-analysis` for exploration, statistics, trend/metric diagnosis, and quality-aware findings;
- `sql-analytics` for analytical SQL and query review;
- `data-visualization` for charts and quantitative figures;
- `data-dashboard` for decision-oriented KPI surfaces;
- `data-context` for schema, metric, lineage, and semantic documentation.

When the active host provides a managed analytics capability, use it rather than duplicating its connector-specific instructions. Otherwise remain host-neutral, preserve data provenance, surface missingness/uncertainty, and never turn correlation into a causal claim.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `data-analysis` | Perform defensible exploratory, descriptive, statistical, or diagnostic analysis on structured data. | [MODULE.md](modules/data-analysis/MODULE.md) |
| `data-context` | Create or repair a durable data context containing schema, grain, metric definitions, lineage, ownership, freshness, and quality caveats. | [MODULE.md](modules/data-context/MODULE.md) |
| `data-dashboard` | Plan, build, review, or improve a decision-focused dashboard with metric definitions, owners, filters, freshness, alerts, and validation. | [MODULE.md](modules/data-dashboard/MODULE.md) |
| `data-visualization-playbook` | Apply a concise decision-focused playbook to design, implement, critique, or validate charts with correct encodings, annotations, accessibility, and source context. | [MODULE.md](modules/data-visualization-playbook/MODULE.md) |
| `sql-analytics-workflow` | Design, review, debug, or explain analytical SQL with correct grain, joins, filters, time logic, performance awareness, and validation. | [MODULE.md](modules/sql-analytics-workflow/MODULE.md) |
