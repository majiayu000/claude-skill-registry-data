---
name: source-and-provenance
description: "Use when attaching sources, definitions and lineage to a figure, table, KPI or report claim: source system, query or metric id, retrieval time and timezone, unit, denominator, aggregation window, filters, transformations, version and run id, plus a methodology note. Also use when a figure must be reproducible later, when data was refreshed after a report went out, or when an agent cites who or what produced a number or an explanation."
license: CC-BY-4.0
---

# Source and provenance

A reader who doubts a number must be able to find where it came from, what
exactly it measures, and what was done to it, without asking the author.
A figure that cannot be traced cannot be corrected.

## What every figure carries

| Field | Example |
|---|---|
| Source system | order-service; finance-service; Google Ads API via the ad-data pipeline |
| Query / metric id | `weekly_paid_orders` v3 |
| Retrieved at (with timezone) | 2026-10-05 06:00 CEST |
| Coverage | ISO weeks 36–40, 2026; all regions |
| Unit | orders; € excl. VAT; % of consultations |
| Denominator (rates) | design consultations held in the same week |
| Aggregation | count per ISO week, Europe/Berlin |
| Filters / exclusions | test orders and staff orders excluded |
| Transformations | none / 7-day rolling mean / deflated to 2026 € with CPI |
| Version / run | report run `report-2026-W40`; model `orders-forecast` v3 |

Readers see a short **source line** (`chart-text-wsj-like`); the full record lives in the
artifact manifest and the report's methodology note.

## Rules

1. **Record at extraction, not afterwards.** Provenance is captured when the
   data is pulled, by the code that pulls it, not reconstructed from memory.
2. **Definitions travel with the data.** Unit, denominator and aggregation are
   attributes of the column, not a footnote someone may drop.
3. **Frozen vs refreshed.** A sent report's figures come from a frozen
   snapshot. A later re-query is a new analysis with its own timestamp; never
   silently overwrite what recipients saw. If numbers changed, say what
   changed and why ("finance restated September after late refunds").
4. **Keep "where the number came from" apart from "who explained it".**
   A value cites the query that computed it. An explanation written by an
   agent cites the run that wrote it, and nothing in that citation may
   suggest the agent produced the value. If nobody knows which run wrote an
   explanation, leave it uncited rather than naming a default author.
5. **Identity is content, not location.** Identify a figure by spec hash and
   data hash (artifact id), not by a URL or file path.
6. **Methodology note for every report.** Sources, coverage dates,
   definitions, steps, exclusions, known limitations, what was not checked.
   Template: `references/methodology-note.md`.
7. **Synthetic or example data says so** in its provenance and caption.
8. **Permissions before provenance.** Filtering by recipient permission
   happens before view data is prepared; provenance must not leak the
   existence of restricted data (a query name can be sensitive).

## ieeVisualizer support

- `Provenance(source, query, retrieved_at, source_version, timezone, run_id,
  notes, extra)` on every `DataSnapshot`; `DatasetRef(kind, id, query,
  version, retrieved_at, columns)` for external data.
- Columns carry `unit`, `description`, `denominator`, `aggregation`, `dtype`.
- `DataSnapshot.content_hash()` hashes values and their meaning, not the
  provenance; `spec_hash(spec)` hashes the canonical spec.
- `artifacts.export()` writes `spec.json`, `spec.resolved.json` (when refs were
  resolved), and `manifest.json` with per-dataset hashes, provenance, column
  meaning, render variants, warnings and library versions; `artifact_id` is
  content-addressed and never depends on a path or URL.
- Templates stamp `metadata["template"]` with name, version, all parameters
  and the input hash. Put the report run id in `spec.metadata` too.
- Not enforced: that provenance fields are filled. An empty `source` passes
  validation. The skill is the guard: treat a missing `source`,
  `retrieved_at` or `timezone` as a blocker for any figure that leaves the
  workspace.

## Good / bad

Bad caption: "Source: internal data."
Good: "Source: order service, query weekly_paid_orders v3, retrieved
5 Oct 2026 06:00 CEST. Weeks are ISO weeks in Berlin time. Test orders
excluded."

Bad: the weekly report is re-generated on Monday with refreshed data and the
September figures quietly change.
Good: the original artifact is kept; the new one notes "September revenue
restated from €182,400 to €184,100 (late refunds, finance, 12 Oct)".

## Checklist

- [ ] Source, query/metric id, retrieved-at with timezone recorded at extraction.
- [ ] Unit, denominator, aggregation set on each column.
- [ ] Filters, exclusions and transformations listed.
- [ ] Report run id and model/template versions recorded.
- [ ] Short source line on the figure; full record in the manifest.
- [ ] Frozen snapshot kept; restatements announced.
- [ ] Explanations cite the producing run; no fallback author.
- [ ] Methodology note written.

Adapted in part from ieeVisualizer's own docs (MIT), jamditis
`data-journalism` (MIT) and K-Dense `scientific-writing` (MIT); changed:
rewritten for figure and report provenance, ieeVisualizer mapping added.
Sources and licences: `SOURCES.md`.
