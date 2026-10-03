---
name: data-analytics
description: Route durable data modeling, analytics engineering, and data-science analysis; not for model-training systems or generic application architecture.
---

# Data And Analytics

Choose one primary mode and read only its workflow. Add a second mode only when the requested deliverable crosses its boundary.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `data-modeling` | Design entities, schemas, ownership, indexes, retention, migrations, backfills, or consistency. | [Data modeling](references/workflows/data-modeling.md) |
| `analytics-engineering` | Define metric contracts, semantic layers, BI transformations, freshness, or dashboard validation. | [Analytics engineering](references/workflows/analytics-engineering.md) |
| `data-science-workflows` | Frame analyses or experiments and assess provenance, leakage, uncertainty, and reproducibility. | [Data-science workflows](references/workflows/data-science-workflows.md) |

Do not load sibling workflows or artifacts prospectively. Preserve grain, lineage, provenance, uncertainty, and owner-controlled migration or release decisions.
