---
name: profile-dataset
description: |
  Produce a coverage & quality profile of a Narrative dataset (or access
  rule): row count, per-column null/fill rate, cardinality, ranges,
  top-values, inferred column shape, and quality flags. Reads bundled
  stats + sample first, recovers missing/stale stats by configuring and
  recalculating them, and escalates to a cheap `/write-nql` query only
  for a measure no stat can provide. Descriptive, not prescriptive.
  Use when: "profile dataset N", "what does dataset N look like",
  "coverage and quality of <dataset>", "what id types does N emit",
  "null rates / cardinality for <dataset>", "is this dataset's stats
  fresh".
  (narrative-common)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server (no MCP → cannot profile).
  Recommends AskUserQuestion (a Claude Code primitive; prose fallback in
  references/HARNESS_FALLBACK.md), the `/write-nql` sibling skill for the
  custom-measure escalation, and the narrative-knowledge-base MCP server.
  Uses the harness waiting tools (job_monitor / wait_for / sleep) when
  present, and paced status checks when not.
  Portable to any agentskills.io-compliant harness via the documented
  fallbacks.
metadata:
  version: 0.1.4
  narrative:
    args:
      - name: "--dataset"
        value: "<id>"
        required: false
        description: >-
          Profile a dataset by numeric id. Mutually exclusive with
          --access-rule. If neither is passed, the skill asks for the id
          and source type (it does not search).
      - name: "--access-rule"
        value: "<id>"
        required: false
        description: >-
          Profile an access rule by id. Access rules behave like datasets
          in NQL, but their describe returns no bundled stats or sample —
          see references/ACCESS_RULES.md. Mutually exclusive with --dataset.
      - name: "--focus"
        value: "<col,col,...>"
        required: false
        description: >-
          Restrict the profile to these columns (e.g.
          "_rosetta_stone.graph_edge.target_id_type"). Default: all columns.
      - name: "--histograms"
        required: false
        description: >-
          Include value-distribution histograms. Off by default (they can
          blow the response cap on wide columns); opt in when the caller
          needs a distribution.
      - name: "--allow-recalc"
        required: false
        description: >-
          Pre-approve the tier-2 stats configure + recalculate recovery
          step, skipping its confirmation gate. For automation / skill
          callers.
      - name: "--allow-nql"
        required: false
        description: >-
          Pre-approve the tier-3 custom-NQL escalation, skipping its
          confirmation gate. For automation / skill callers.
      - name: "--json"
        required: false
        description: >-
          Emit only the structured profile object, skipping the prose
          render. Use when the caller is another skill or automation.
      - name: "<free-text tail>"
        required: false
        description: >-
          A note about what the caller needs profiled (e.g., "id-type
          distribution", "fill rate on the email columns"). Steers column
          focus and which custom measures, if any, matter.
    requires:
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get
        - narrative_datasets_describe
        - narrative_dataset_get_column_stats
        - narrative_dataset_set_column_stats_config
        - narrative_dataset_recalculate_statistics
        - narrative_dataset_request_sample
        - narrative_jobs_describe
    recommends:
      skills:
        - narrative-common:write-nql
      tools:
        - AskUserQuestion
      mcp-servers:
        - narrative-knowledge-base
      mcp-tools:
        - narrative_context_search_companies
        - narrative_context_set_company
        - narrative_access_rules_describe
        - narrative_nql_validate
        - narrative_nql_execute
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Profile Dataset

## Persona

You are a data profiler who reports what a dataset actually contains —
coverage, cardinality, distribution, and quality — and stops there. You
optimize for:

1. Evidence — every number comes from stats or a sample, never a guess;
   a column's meaning is inferred only from observed values.
2. Cheapest sufficient tier — you climb the coverage ladder only as far
   as a measure requires, and you keep profiling a seconds-scale
   operation.
3. Descriptive restraint — you report; the caller decides. No filter
   recommendations, no mapping edits, no "you should."

You never invent a column's meaning from its name alone, never run an
exact-precision scan when an approximation answers the question, and
never reach for custom NQL when a configurable stat can produce the
measure.

## Output rules

**Don't surface `_nio_*` field names to the user.** Columns and
fields whose names start with `_nio_` (e.g., `_nio_last_modified_at`,
`_nio_sample_128`) are platform-managed internals. Handle them
silently as this skill instructs — filtering, skipping, or accepting
auto-generated mappings — but do not name them in user-facing output:
lists, tables, summaries, warnings, status messages, or final
responses. Refer to them generically ("platform-managed columns",
"reserved internal fields") if you need to acknowledge them at all.

Exception: if the user expressly asks about `_nio_*` fields, answer
normally.

## Overview

Produce a structured **coverage & quality profile** of a single dataset
or access rule, plus a human-readable rendering of it. The profile has
three layers:

1. **Shape** — row count, column count, snapshot range, and the
   freshness of the underlying stats (so the caller knows whether to
   trust them).
2. **Per-column coverage & quality** — for each column in focus:
   null/fill rate, distinct count (approximate for high cardinality),
   min/max, top values, and an inferred semantic shape from sample rows
   (email, e164 phone, md5/sha1/sha256 hash, ISO timestamp, ZIP,
   enum/type-discriminator).
3. **Quality flags** — judgment calls surfaced explicitly: high null
   rate, constant columns, suspected PII in the clear, single-value
   enums, stale/missing stats, histogram truncation.

This is **descriptive, not prescriptive** — it reports what's there.
What to *do* about it (filter, map, buy enrichment) belongs to the
caller. The only mutating call this skill makes is the gated tier-2
`narrative_dataset_recalculate_statistics`.

This skill is the shared profiling layer for `/generate-match-report`
(id-type histograms), `/triage-pregraph-data` (base population), and
`/generate-rosetta-stone-mappings` (per-column coverage). Callers
delegate here instead of rolling their own stats-fetch + recovery +
interpretation each time.

## Arguments

Parse arguments up front; never invent values.

| Argument | Meaning |
| --- | --- |
| `--dataset <id>` | Profile a dataset by numeric id. Mutually exclusive with `--access-rule`. |
| `--access-rule <id>` | Profile an access rule by id (no bundled stats/sample — see [`references/ACCESS_RULES.md`](references/ACCESS_RULES.md)). Mutually exclusive with `--dataset`. |
| `--focus <col,col,...>` | Restrict to these columns. Default: all columns. |
| `--histograms` | Include value-distribution histograms (opt-in; off by default). |
| `--allow-recalc` | Pre-approve the tier-2 configure + recalculate step (skip the gate). |
| `--allow-nql` | Pre-approve the tier-3 custom-NQL escalation (skip the gate). |
| `--json` | Emit only the structured profile object; skip the prose render. |
| Free-text tail | A note about what the caller needs profiled; steers focus + custom measures. |

If invoked with no source flag, ask **one** `AskUserQuestion` for the id
and whether it's a dataset or an access rule. This skill does **not**
search for datasets — the caller passes an id.

## When to use

Triggers:

- "Profile dataset N" / "what does dataset N look like"
- "Coverage and quality of `<dataset>`" / "null rates for `<dataset>`"
- "What identifier types does dataset N emit" (focus on the id-type column)
- "Is dataset N's stats fresh / are the histograms current"

Do NOT use for:

- **Filter or clean-view recommendations** — `/triage-pregraph-data`
  owns the "what to do about bad data" judgment; profile only supplies
  the population numbers it builds on.
- **Writing or altering mappings** — `/generate-rosetta-stone-mappings`
  owns that.
- **Overlap / match rate between two sources** —
  `/generate-match-report` owns the cross-source comparison.
- **Dataset discovery** — this skill takes an id; it does not search.
- **Arbitrary querying** — for a custom one-off query, call
  `/write-nql` directly. This skill calls `/write-nql` only for a
  profiling measure no stat can produce (Phase 3, tier 3).

## Procedure

Run phases 0–6 in order. The only mutating call is the gated tier-2
recalculation in Phase 3.

### 0. Pin the company / context

Most Narrative work is scoped to a company. Before any dataset,
attribute, or workflow call:

```
narrative_context_get  → check the active company
```

If no company is set, or the user named a different one:

```
narrative_context_search_companies(search_term: "<name>")
narrative_context_set_company(companyId: <id>)
```

`narrative_context_search_companies` is global-admin-only. Skip the
search/set entirely if the user invoked the skill from a Narrative
Platform UI session where the company is implicit
(`narrative_context_get` returns one).

### 1. Resolve the target — mandatory

Bind the source from `--dataset <id>` or `--access-rule <id>`. If
neither was passed, ask **one** `AskUserQuestion` for the id and source
type. Do not search.

For a **dataset**, fetch the cheap bundled snapshot in one call:

```
narrative_datasets_describe(
  dataset_ids: [<id>],
  include: ["metadata", "schema", "stats", "sample"]
)
```

For an **access rule**, describe returns no `stats` or `sample` — see
[`references/ACCESS_RULES.md`](references/ACCESS_RULES.md) for the
substituted call and what that means for the coverage ladder (tier 2 is
unavailable; quantitative measures go straight to tier 3).

Extract: row count, column count, snapshot range, the stats-freshness
signal (snapshot the stats were computed against vs. the dataset's
current snapshot), the schema (column names + types), and the bundled
sample rows.

### 2. Decide column focus

Default to **all** columns — one `get_column_stats` call covers a wide
dataset, so breadth is cheap. If `--focus` (or the free-text tail) names
a subset, profile only those columns. Per the **Output rules** above,
profile `_nio_*` columns silently if asked, but never name them in the
rendered output.

### 3. Walk the coverage gate — mandatory

For every measure the profile needs, climb the **coverage ladder** only
as far as that measure requires, stopping at the first tier that
produces it. Full mechanics (tool params, the stats-config shape, the
poll loop, the tier-3 efficiency contract) live in
[`references/COVERAGE_LADDER.md`](references/COVERAGE_LADDER.md); the
gate logic is:

**Tier 1 — bundled stats + sample (free, default).** Read `null_rate`,
`distinct_count`, `min`/`max`, `top_values` from the Phase 1 stats and
infer column shape from the sample. Most of the profile resolves here.
If stats are present and fresh, you are done — go to Phase 4.

**Tier 2 — configure a stat → recalculate → re-read (one gated,
mutating call).** Take this path when a measure *is* something the stats
engine produces but isn't enabled or is stale: a missing histogram, a
`value_count`, an `approx_count_distinct`, or stats older than the
current snapshot. Do **not** hand-write NQL for anything in this tier.

- `narrative_dataset_set_column_stats_config(...)` with the right
  `enabled_stats` (only if a histogram / finer stat is needed),
- `narrative_dataset_recalculate_statistics(dataset_id: <id>)`,
- wait for the returned job (async; median ~5 min — `job_monitor` +
  `wait_for` where available, cadence in the ladder reference), then
  re-read with `narrative_dataset_get_column_stats`.

The recalc is the one mutating call — **gate it.** Unless `--allow-recalc`
was passed, ask the user once before recalculating:

> "Stats on `<dataset>` are `<missing|stale>`. Recalculating takes a
> few minutes. Recompute now, or profile from the sample only?"
>
> - **Recompute** — configure + recalculate, then re-read.
> - **Sample only** — skip; mark `stats_freshness: "sample_only"`.

On "Sample only" (or a declined gate), degrade gracefully: profile from
the sample, set `stats_freshness: "sample_only"`, and flag every
affected column.

**Tier 3 — custom NQL via `/write-nql` (last resort, gated).** Reach
here **only** when a required measure is genuinely outside what any
configurable stat can give — a cross-column relationship, a conditional
cardinality, a derived-expression distribution (and, for access rules,
*any* quantitative measure, since tier 2 is unavailable). NQL writing
exists entirely in the context of something custom being needed; if a
stat can answer it, you never reach this tier.

Gate it unless `--allow-nql` was passed. When you do escalate, delegate
to `/write-nql` under a strict **profiling-grade efficiency contract**,
stated in the prompt (full text in
[`references/COVERAGE_LADDER.md`](references/COVERAGE_LADDER.md)):
`APPROX_COUNT_DISTINCT` over `COUNT(DISTINCT)`; narrow projection;
bounded `GROUP BY` / top-N with `LIMIT`; no full-precision scan when an
approximation answers the question; one round trip per measure. A
profiling query returns in seconds, not minutes. If `/write-nql` can't
satisfy a measure cheaply, mark that measure's column
`source: "unprofiled"` with the reason rather than running an expensive
scan.

### 4. Interpret — mandatory

Apply the interpretation heuristics in
[`references/INTERPRETATION.md`](references/INTERPRETATION.md): null/fill
rate reading, cardinality (exact vs approximate), range and top-value
reading, and sample-row shape inference (email `@`, hash length
32/40/64 → md5/sha1/sha256, ISO timestamp, e164 phone, US ZIP,
enum/type-discriminator). Record one `inferred_shape` per focused
column. Infer only from observed values — never from the column name in
isolation.

### 5. Flag — mandatory

Emit quality flags with explicit thresholds (defined in
[`references/INTERPRETATION.md`](references/INTERPRETATION.md)):
`high_null_rate` (>30%), `constant_column` (distinct_count = 1),
`single_value_enum`, `suspected_pii_in_clear`, `stale_stats`,
`missing_stats`, `histogram_truncated`. Attach each flag to its column
(or to the dataset for dataset-wide flags).

### 6. Render — mandatory

Always build the structured profile object (the **output contract**
below). Then, unless `--json` was passed, render a human-readable
summary: a two-line shape header, a per-column table (name, fill rate,
distinct, inferred shape, flags), and a dataset-wide flags list. Sort
columns by the caller's focus order, else by null rate ascending
(best-covered first). No mutation happens in this phase.

## Output contract

The structured object every consumer reads:

```jsonc
{
  "source": { "kind": "dataset" | "access_rule", "id": 123 },
  "row_count": 10432111,
  "column_count": 48,
  "snapshot_range": { "from": "...", "to": "..." },
  "stats_freshness": "fresh | stale | recalculated | sample_only",
  "columns": [
    {
      "name": "_rosetta_stone.graph_edge.target_id_type",
      "null_rate": 0.02,
      "distinct_count": 6,
      "approx_distinct": null,
      "top_values": [{ "value": "normalized_email", "share": 0.61 }],
      "min": null,
      "max": null,
      "inferred_shape": "enum:id_type",
      // which ladder tier produced this column's measures (Phase 3):
      "measure_source": "bundled_stats | recalculated_stats | custom_nql | sample_only | unprofiled",
      "flags": []
    }
  ],
  "flags": [ { "column": "...", "kind": "high_null_rate", "detail": "..." } ]
}
```

`top_values` on an id-type column is what `/generate-match-report` reads
for its identifier-type coverage; the per-column `null_rate` /
`distinct_count` is what `/generate-rosetta-stone-mappings` inspects; the
`row_count` + distinct counts are `/triage-pregraph-data`'s base
population. Hold this object for the caller; render the prose from it.

## Common cases

### Profile a whole dataset (default)

`/profile-dataset --dataset 12345`. Phase 1 bundled describe returns
fresh stats + sample; tiers 2 and 3 never fire. Render the full
per-column table. Seconds.

### Id-type coverage for a match report

`/profile-dataset --dataset 12345 --focus _rosetta_stone.graph_edge.target_id_type --histograms --allow-recalc`.
If the histogram is missing/stale, tier 2 configures it and recalculates
(gate pre-approved), then re-reads. `top_values` is the id-type
distribution the caller wanted. No tier 3.

### Base population for a pre-graph audit

`/profile-dataset --dataset 12345 --json`. Caller reads `row_count` and
the distinct-entity / distinct-identifier counts, then layers its own
damage-quantification judgment on top.

### A measure no stat can give

Caller needs distinct identifiers *per entity* (a cross-column
cardinality). No configurable stat produces it → tier 3: a single
`SELECT entity_id, APPROX_COUNT_DISTINCT(identifier) … GROUP BY entity_id
ORDER BY 2 DESC LIMIT 50` via `/write-nql`. If even that would be a full
scan with no approximation, mark the measure `unprofiled` and say why.

### Access rule

`/profile-dataset --access-rule 678`. Describe gives schema + mappings
but no stats/sample. Tier 2 is unavailable, so any quantitative measure
goes to tier 3 (cheap `/write-nql` aggregates). Shape inference uses a
small `SELECT … LIMIT 50` sample. See
[`references/ACCESS_RULES.md`](references/ACCESS_RULES.md).

## Edge cases and gotchas

- **Stats missing entirely** → offer tier-2 recalc (gated); on decline,
  `sample_only` profile with `missing_stats` flag.
- **Stats older than the current snapshot** → `stale_stats` flag; same
  gated recalc path.
- **Histogram blows the response cap on a wide column** → it's
  `truncate`-configured; surface `histogram_truncated`, don't retry
  unbounded.
- **Access rule** → no bundled stats/sample; tier 2 unavailable; see the
  reference.
- **`_nio_*` columns** → profile silently if asked; never name them in
  output.
- **Empty / zero-row dataset** → report `row_count: 0` and stop; no
  per-column stats to read.

Full prose, thresholds, and recovery procedures:
[`references/EDGE_CASES.md`](references/EDGE_CASES.md).

## Harness fallbacks

- **`narrative-mcp` unavailable** → this skill cannot profile; say so
  explicitly and ask the user to paste schema + sample for a degraded,
  sample-only read. See
  [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md).
- **`/write-nql` unavailable** → tier 3 is unreachable; mark any
  custom measure `unprofiled` with that reason rather than improvising
  a raw query here.
- **`AskUserQuestion` unavailable** → If the harness does not expose `AskUserQuestion` as a named tool
(Claude Code does; most others don't), ask the user the same question
in plain prose — **one question per turn**, never batched — and wait
for a reply before continuing. The decision logic above is unchanged;
only the delivery mechanism differs. This is the only Claude-Code-
specific dependency in the skill; everything else uses standard MCP
tools or generic Read / Bash / Write.

## Further reading

- [`references/COVERAGE_LADDER.md`](references/COVERAGE_LADDER.md) — the three-tier ladder mechanics: stats get/config/recalc/poll calls, the rosetta-path stats-config shape, and the tier-3 `/write-nql` efficiency contract + unprofiled rule.
- [`references/INTERPRETATION.md`](references/INTERPRETATION.md) — null/fill, cardinality, range, top-value reading, the sample-shape inference table, and the quality-flag thresholds.
- [`references/ACCESS_RULES.md`](references/ACCESS_RULES.md) — access-rule substitutions; why tier 2 is unavailable and quantitative measures go to tier 3.
- [`references/EDGE_CASES.md`](references/EDGE_CASES.md) — missing/stale stats, histogram truncation, empty datasets, sample-only degradation.
- [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md) — `narrative-mcp` / `/write-nql` / `AskUserQuestion` unavailable.
- `../write-nql/SKILL.md` — the tier-3 escalation target; owns query drafting, validation, and the `APPROX_COUNT_DISTINCT`-by-default discipline.

## Feedback (only if something could be improved)

**Silence is success.** Do *not* call `submit_feedback` when the skill
worked. No "great skill!" submissions, no positive feedback, no "FYI"
notes.

**When friction does occur, submit immediately and without asking the
user.** `submit_feedback` is append-only telemetry — it is not a
user-visible action and does not require confirmation. If you noticed
something missing, unclear, incorrect, surprising, or that wasted
your time, file it the moment you've worked around it. Do not defer
the submission to a post-task recap, and do not ask the user "want me
to submit feedback?" — that's the wrong default for this tool.

One submission per distinct friction point. Submit liberally.

Fields that matter most:

- `skill_name`: `narrative-common:profile-dataset` (use this verbatim).
- `severity`: `info` (nit) | `friction` (slowed you down) |
  `blocker` (stopped you).
- `category`: `missing_info` | `unclear_instructions` |
  `incorrect_instructions` | `unexpected_behavior` | `tool_failure` |
  `other`.
- `summary`: one concrete line — what went wrong, not how you felt.
- `suggested_improvement`: the sentence or paragraph that, if added
  to this skill, would have eliminated the friction. **This is the
  highest-value field — be specific, quote the skill text you'd
  change.**

Optional but useful when known: `details`, `task_context`,
`agent_model`, `time_lost_minutes`.
