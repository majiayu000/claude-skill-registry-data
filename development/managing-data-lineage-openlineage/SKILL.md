---
name: managing-data-lineage-openlineage
description: Capture and use data lineage with OpenLineage and Marquez — emitting run/job/dataset events from Airflow, dbt, and Spark, column-level lineage, and using lineage for impact analysis, debugging, and backfill scoping. Use when setting up data lineage, integrating OpenLineage, tracing what a change breaks downstream, or scoping the blast radius of an incident.
---

# Managing Data Lineage with OpenLineage

## When to use

- Setting up automated lineage across Airflow, dbt, and Spark.
- Answering "what breaks if I change this table?" (impact analysis).
- Scoping an incident's blast radius or a backfill's downstream footprint.
- Do NOT use for in-project dbt lineage only (dbt docs cover that; use this for
  cross-tool, cross-system lineage).

## Core model

OpenLineage describes each pipeline run as **Job** (the transformation), **Run**
(one execution), and **Datasets** (inputs/outputs), optionally with **column-level**
mappings. Emitters send these events to a backend (e.g. Marquez) that builds the
graph.

## Workflow

```
- [ ] Add the OpenLineage integration to each producer (Airflow/dbt/Spark)
- [ ] Point emitters at a collector (Marquez or vendor endpoint)
- [ ] Verify jobs/datasets/edges appear with column-level detail where supported
- [ ] Use the graph for impact analysis before changes
- [ ] Use it during incidents to scope downstream impact and backfills
```

1. **Instrument producers.** Airflow (OpenLineage provider), dbt
   (`dbt-ol`/native), and Spark (OpenLineage listener) emit events automatically —
   prefer these over hand-rolled lineage.
2. **Centralize.** Send events to Marquez or a lineage platform so the whole graph
   is queryable in one place.
3. **Validate coverage** — confirm datasets, edges, and column-level lineage render
   for critical flows.
4. **Impact analysis** — before changing/deprecating a table, traverse downstream
   to find affected models, dashboards, and owners.
5. **Incident scoping** — from a bad source dataset, list every downstream consumer
   to size the fix and the backfill.

## Patterns

**Airflow emission** — enable the OpenLineage provider and set the transport
endpoint via env/config; DAG runs then emit job/dataset events without code
changes.

**Use lineage to scope a backfill** — the set of downstream datasets reachable from
the corrected table is exactly the set that must be reprocessed
(pairs with `designing-backfills-and-replays`).

**Column-level lineage** — when a single column is wrong, column mappings pinpoint
which downstream columns depend on it, narrowing the investigation.

## Common pitfalls

- **Manual lineage docs** — drift immediately; use automated emitters.
- **Partial instrumentation** — gaps make the graph misleading; instrument every
  producer in a critical path.
- **Lineage without ownership** — knowing what breaks is only useful if you can
  find who to tell; attach owners to datasets.
- **Ignoring column-level lineage** where available — table-level alone forces
  broad, slow investigations.
- **Treating lineage as a diagram, not a tool** — wire it into change review and
  incident response, not just a wiki page.
