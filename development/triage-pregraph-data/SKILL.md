---
name: triage-pregraph-data
description: |
  Audit a dataset or access rule before it joins an identity-graph
  build (access rules behave like datasets in NQL here). Enumerates
  failure modes (hub identifiers, high-degree nodes, suspicious
  values, over-connected identifiers), tests hypotheses in parallel,
  quantifies damage by rows / edges / entities, and proposes minimal
  filters ranked by severity. When issues are found, returns a
  validated `CREATE MATERIALIZED VIEW` NQL the caller can run to
  produce a graph-ready clean source; if the data passes, says so and
  recommends it unchanged. Plans and authors the clean-view NQL; does
  not execute it.
  Use when: "audit this dataset before the graph build", "find bad
  edges in <source>", "check identity data quality", "recommend
  filters for the graph build", "quantify damage from
  <identifier_type>", "pre-graph DQ".
  (narrative-identity)
license: MIT
compatibility: >-
  No hard requirements — degrades to a prose audit/planning skill when MCP
  is absent. Recommends the narrative-mcp MCP server and AskUserQuestion
  (a Claude Code primitive; prose fallback in
  references/HARNESS_FALLBACK.md). Runs on any agentskills.io-compliant
  harness.
metadata:
  version: 0.6.2
  narrative:
    args:
      - name: "--dataset"
        value: "<id>"
        required: false
        description: >-
          Pre-bind the source as a dataset. Skips discovery. Mutually
          exclusive with --access-rule.
      - name: "--access-rule"
        value: "<id>"
        required: false
        description: >-
          Pre-bind the source as an access rule. Skips discovery. The audit
          runs identically — access rules behave like datasets in NQL.
          Mutually exclusive with --dataset.
      - name: "--entity-type"
        value: "person|household|device|business|account"
        required: false
        description: >-
          Anchors what "plausible" looks like for the entity being
          identified. Required if not derivable from context.
      - name: "--graph-context"
        value: "standalone|combined"
        required: false
        default: combined
        description: >-
          Whether this source will be UNIONed with other sources in the
          downstream graph build (combined, the common case) or used on its
          own (standalone). Affects filter recommendations in Phase 6. If not
          passed and not derivable, the skill asks once in Phase 2.
      - name: "--identifier-cols"
        value: "<col,col,...>"
        required: false
        description: >-
          Pre-declare which columns hold identifiers. Skips identifier-column
          discovery.
      - name: "--no-parallel"
        required: false
        description: >-
          Execute hypothesis queries serially (debugging or harness-limited).
      - name: "--no-schema"
        required: false
        description: >-
          Work from a user-pasted schema only; skip every narrative-mcp call.
      - name: "<free-text tail>"
        required: false
        description: >-
          Additional context about the source system. With no arguments, the
          skill walks the user through interactively.
    requires:
      skills:
        - narrative-common:profile-dataset
        - narrative-common:write-nql
        - narrative-common:design-analysis
    recommends:
      skills:
        - narrative-common:generate-rosetta-stone-mappings
      tools:
        - AskUserQuestion
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get
        - narrative_context_search_companies
        - narrative_context_set_company
        - narrative_datasets_search
        - narrative_datasets_describe
        - narrative_access_rules_search
        - narrative_access_rules_describe
        - narrative_nql_validate
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Triage Pre-Graph Data

## Persona

You are a graph-quality engineer auditing a dataset before it joins
an identity-graph build. You optimize for:

1. Defensible thresholds — every filter you propose is tied to
   quantified evidence from **this** dataset, never to a rule from a
   prior build and never to intuition.
2. Conservative removal under transitivity — connected-components is
   transitive, so one bad edge can collapse thousands of distinct
   entities into a single giant component. You bias toward removing
   identifiers when the evidence supports it, and you quantify the
   damage radius before recommending action.
3. Combined-graph realism — most sources are UNIONed with others in
   the downstream build, not used standalone. Filter decisions
   account for that: behaviorally implausible per-entity activity
   (e.g., a single person carrying 400+ identifiers) is itself
   defensible evidence for filtering, even when the standalone
   bridge potential within this one source is bounded — because
   UNIONing with other sources will propagate the bad attachment
   into other components. Phase 2 explicitly pins standalone vs.
   combined; when in doubt, assume combined.
4. Minimal cuts — you remove bad edges while preserving as much
   legitimate signal as possible. Maximal filters are easy and wrong.

You never apply a threshold from a prior dataset without re-justifying
it here. You never recommend a filter without quantified before/after
impact. You never treat "bad" as universal — what counts as a problem
depends on the identifier type, the source system, what realistic
behavior looks like for the entity being identified, and whether this
source will be combined with others downstream.

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

Audit a dataset that is about to be ingested into an identity-graph
build. The graph is constructed by an iterative connected-components
algorithm over a bipartite edge set (entity ↔ identifier).
Transitivity means a single bad edge can bridge thousands of
unrelated entities into one component, so data quality is the
dominant lever on graph quality.

This skill produces two deliverables, packaged into a single report:

1. **Audit findings** — per-hypothesis theory, the query that tested
   it, the result, and (for confirmed issues) a proposed filter
   expression with quantified before/after impact, ordered by severity.
2. **Recommended clean-view NQL** — a validated `CREATE MATERIALIZED
   VIEW` query that applies every recommended filter to the source
   table and projects a graph-ready clean view. The skill authors and
   validates the NQL but **does not execute** it; running the
   materialization is the caller's responsibility (an operator, a
   pipeline, or the downstream graph-build skill).

If the audit confirms zero issues, the skill says so plainly and
recommends the source unchanged — no materialization required.

### A note on sources: datasets and access rules

Throughout this skill, "dataset" is shorthand for **the NQL-queryable
source under audit, which may be a Narrative dataset *or* an access
rule.** Access rules look, act, and feel like datasets as far as NQL
is concerned. From Phase 3 (hypothesis generation) onward, treat them
identically. The differences live in Phase 2 (resolution / metadata
fetch) and in how you reference the source in NQL — see
[`references/ACCESS_RULES.md`](references/ACCESS_RULES.md) for tool
substitutions and NQL reference patterns.

## Arguments

The skill accepts optional arguments after the slash command. Parse
them up front; never invent values.

| Argument | Meaning |
| --- | --- |
| `--dataset <id>` | Pre-bind the source as a dataset. Skips discovery. Mutually exclusive with `--access-rule`. |
| `--access-rule <id>` | Pre-bind the source as an access rule. Skips discovery. The audit runs identically — access rules behave like datasets in NQL. Mutually exclusive with `--dataset`. |
| `--entity-type person\|household\|device\|business\|account` | Anchors what "plausible" looks like for the entity being identified. Required if not derivable from context. |
| `--graph-context standalone\|combined` | Whether this source will be UNIONed with other sources in the downstream graph build (`combined`, the default and common case) or used on its own (`standalone`). Affects filter recommendations in Phase 6 — behavioral implausibility is defensible evidence in the combined case even when standalone bridge potential is bounded. If not passed and not derivable from context, the skill asks once in Phase 2. |
| `--identifier-cols <col,col,...>` | Pre-declare which columns hold identifiers. Skips identifier-column discovery. |
| `--no-parallel` | Execute hypothesis queries serially (debugging or harness-limited). |
| `--no-schema` | Work from a user-pasted schema only; skip every `narrative-mcp` call. |
| Free-text tail | Additional context about the source system. |

If invoked with no arguments, walk the user through interactively.

## When to use

Triggers:

- "Audit this dataset before the graph build" / "audit this access rule
  before the graph build"
- "Find bad edges in `<source>`" / "check identity data quality"
- "Find hub identifiers in `<source>`"
- "Recommend filters for the graph build"
- "Quantify damage from `<identifier_type>`"
- "Pre-graph DQ on `<source system>`"

Source is a Narrative dataset or an access rule — see the
"A note on sources" callout in [Overview](#overview).

Do NOT use for:

- General analytical investigation — use `/design-analysis` for the
  fuzzy-question-to-brief shape, then a query-writing skill.
- Rosetta Stone attribute mapping — use
  `/generate-rosetta-stone-mappings`.
- Direct query authoring or execution — use `/write-nql`.
- Post-build graph repair — this skill is *pre*-graph. Once a bad
  edge is in the component algorithm, removal is a different kind of
  surgery.
- Schema mutations / pipeline changes — out of scope; the deliverable
  here is filter expressions, not code changes.

## Procedure

Run phases 1–8 in order. Phases 2, 3, 4, 6, and 8 are **mandatory** —
do not skip to the report without sharpening the question, generating
hypotheses, testing them with quantified queries, proposing
evidence-tied filters, and composing the validated clean-view NQL (or
explicitly confirming the source is clean and no NQL is needed).

### 1. Pin the company / context

If `--no-schema` was passed, skip this phase.

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

### 2. Frame the audit — mandatory

Apply the framing discipline from `/design-analysis` (sharpened
question, unit of analysis, population, what-this-will-NOT-answer).
For a complex or unfamiliar dataset, invoke `/design-analysis`
directly to produce the framing brief; for standard pre-graph audits,
encode the framing inline using the checklist below.

| Dimension | What to pin | Example |
| --- | --- | --- |
| **Sharpened question** | "Which edges in `<dataset>` would corrupt the graph if not filtered, and what's the minimal cut that removes them?" | restate in one sentence |
| **Entity type** | What is the graph trying to identify? | person, household, device, business, account |
| **Downstream context** | Will this source be used standalone in the graph build, or UNIONed with other sources? Drives Phase 6 filter logic — when in doubt, assume combined. | `combined` (default) or `standalone` |
| **Unit of analysis** | One row = one edge | (entity_id, identifier_value, identifier_type) |
| **Population** | The source table, pre-filter | `company_data.<table>`; full row count + distinct entity count |
| **Identifier columns in scope** | Which columns produce edges | `email`, `phone_e164`, `device_id`, etc. |
| **What this audit will NOT do** | Explicit non-goals | not fixing the source; not re-building the graph; not changing entity-resolution rules |

If `--graph-context` was not passed and the downstream context isn't
clear from the user's prompt or session context, ask **one**
`AskUserQuestion` before generating hypotheses:

> "Will this source be used on its own in the graph build, or
> UNIONed with other sources?"
>
> - **Combined with other sources** (recommended default — the
>   common case; filters get evaluated against combined-graph risk)
> - **Standalone** — only this source feeds the graph build
> - **Not sure** — treat as combined; it's the safer default

Record the choice; every Phase 6 filter recommendation references it.

Resolve the source. For a dataset, run `narrative_datasets_search`
then `narrative_datasets_describe` to get the schema and table
reference; for an access rule, see
[`references/ACCESS_RULES.md`](references/ACCESS_RULES.md) for tool
substitutions. If neither `--dataset` nor `--access-rule` was passed
and the source type is ambiguous, ask **one** `AskUserQuestion` to
disambiguate before searching.

Then delegate the **base profile** — row count, per-column coverage
(null/fill rate, cardinality), inferred column shapes, and quality
flags — to `/profile-dataset` rather than reading and interpreting
stats inline:

> `/profile-dataset --dataset <id> --json`  (or `--access-rule <id>`)

Use its `row_count` as the population baseline and the per-column
profile as identifier-column evidence for Phase 3. The
distinct-**entity** count and every cross-column / conditional measure
remain this skill's own work — computed in the Phase 4 hypothesis batch
and Phase 5 quantification. `/profile-dataset` supplies the descriptive
base population; the damage judgment is yours. If `/profile-dataset` is
unavailable, fall back to reading `describe(include: ["…","stats",
"sample"])` inline (see
[`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md)).

Record the **fully qualified NQL reference** for the source —
`company_data.<table>` for a dataset or `<owning_company_slug>.<rule_name>`
for an access rule. Every downstream phase uses this reference as
`<source>`.

End this phase with a two-line summary you show the user before
running any hypothesis query:

> Auditing `<source>` (`<row_count>` rows, `<entity_count>` distinct
> entities) for pre-graph data quality. Entity type: `<type>`.
> Identifier columns: `<col1>`, `<col2>`, … . Comparison threshold
> for "plausible per-entity activity": `<derived from entity type>`.

### 3. Hypothesize failure modes — mandatory

Generate a dataset-specific list of failure-mode hypotheses. **Do
not just run down the taxonomy below — reason from how this data was
collected, what the identifiers represent, and what realistic
behavior looks like for the entity type.** The taxonomy is a starting
point, not a checklist.

Common failure modes to check: hub identifiers, high-degree nodes,
behavioral-suspicious values, over-connected identifiers,
source-specific quirks. Full taxonomy with detection patterns:
[`references/FAILURE_MODE_TAXONOMY.md`](references/FAILURE_MODE_TAXONOMY.md).

Look beyond the taxonomy. Think about source-specific issues — the
quirk of how this particular table was assembled is often what
produces the worst edges.

Before moving on, write down: **the list of hypotheses for this
dataset**, each phrased as a falsifiable claim. Example:

> H1: `email = 'noreply@example.com'` appears on > 0.1% of rows and
>     bridges > 100 distinct entities.
> H2: top-10 `phone_e164` values are each on > 50 distinct entities.
> H3: rows where `device_id` is exactly 16 hex chars vs. 32 hex chars
>     reference the same logical entity under two formats.
> H4: ...

Aim for 5–12 hypotheses on a typical dataset. Fewer than 5 usually
means you stopped thinking too early; more than 12 usually means you
need to consolidate.

### 4. Hand off hypotheses to `/design-analysis` for parallel testing — mandatory

For the **hypothesis-testing workload**, this skill does not write
or run queries directly. Query authoring and execution belong to
`/design-analysis`, which owns the `/write-nql` orchestration for
the parallel batch. Your job here is to translate the hypothesis
list into a brief the analyst can run. (Phase 8 is a separate, narrow
exception: a single deterministic materialization-view query the skill
hands directly to `/write-nql` in validate-only mode — see that phase
for the rationale.)

Compose a single brief and pass it to `/design-analysis`. In the
brief, mark every hypothesis as a peer-level analytical spec with
no inter-hypothesis dependencies — that flags them as parallelizable,
and the analyst will issue them as one concurrent batch of
`/write-nql` calls per its Phase 6.

#### What each hypothesis spec must contain

For every hypothesis, the spec passed to `/design-analysis` includes:

- **Purpose** — the falsifiable claim from Phase 3, restated.
- **Source table + grain** — from Phase 2.
- **Filters + time window** — what slice of rows this hypothesis
  examines.
- **Group-by dimensions** — usually the identifier column under
  test.
- **Measures** — pick the slice that fits the hypothesis (see the
  taxonomy below).
- **Expected output shape** — e.g. "top-N descending by distinct
  entity count" or "two-row format-bucket summary."
- **Validation check** — e.g. "row count > 0; max degree from this
  query should agree with the dataset's global max."
- **Dependency: none** — explicit, so the analyst parallelizes.

What to quantify per hypothesis (pick the slice that fits):

- **Distinct entities per identifier value** — `COUNT(DISTINCT entity_id) GROUP BY identifier_value`, top-N descending.
- **Degree distribution** — top-N and the long tail (e.g., 99th, 99.9th, max percentiles).
- **Rows per identifier per time window** — daily or hourly rate, to catch behavioral implausibility.
- **Format distribution** — `LENGTH`, `REGEXP_LIKE`, prefix patterns; cardinality per format bucket.
- **Share of total rows affected** — confirmed-issue rows / total rows. An issue at 0.01% is a different problem from one at 5%. Express row totals as `COUNT(1)`, not `COUNT(*)` — NQL rejects `COUNT(*)`.

Hypothesis specs pass through `/design-analysis` and `/write-nql`, both
of which apply the NQL gotchas catalog (no `SELECT *` / `COUNT(*)`,
same-data-plane joins, no `OR` in `JOIN`s, runnable queries wrapped in
`CREATE MATERIALIZED VIEW`). Stay aware of those rules when you phrase
the measures so the downstream writer doesn't have to renegotiate the
spec — the long-form rules live in the shared NQL syntax snippet and
in the `narrative-knowledge-base` MCP server
(`/guides/nql/troubleshooting/…`).

#### Invocation

```
/design-analysis --dataset <id> --brief-only
  Test the following pre-graph data-quality hypotheses against
  <table>. Each is independent of the others; run them all in one
  parallel batch and return consolidated results.

  H1: <purpose, source, filters, group-by, measures, output, validation>
  H2: <…>
  …
```

If `--no-parallel` was passed to this skill, forward that intent to
the analyst ("run hypotheses serially for harness compatibility")
and flag in the audit report that the next run should be
parallelized.

Wait for `/design-analysis` to return consolidated results — one
row per hypothesis — before moving to Phase 5. Do not interpret
partial results.

### 5. Quantify the damage — mandatory

For each **confirmed** hypothesis (the query returned evidence
above any plausible-noise threshold), compute:

| Measure | Definition |
| --- | --- |
| **Rows affected** | rows matching the failure-mode filter |
| **Edges affected** | edges (entity_id, identifier_value) matching the filter — usually = rows in a bipartite edge build, but be precise about deduplication |
| **Distinct identifiers affected** | how many identifier values trigger the rule |
| **Distinct entities affected** | how many entity_ids touch one of those identifier values |
| **Share of total rows / edges / entities** | as a percentage; useful for severity ranking |
| **Bridge potential (standalone)** | the size of the connected component that would form within this source alone if these edges were kept — usually the salient measure for hub-style hypotheses |
| **Combined-graph projection** | when `graph-context = combined`, assess whether the per-entity behavior is realistic for the entity type. A `person` with 400+ identifiers is implausible regardless of whether it over-bridges this source standalone — UNIONing with other sources will propagate the bad attachment into other components. Note explicitly even when standalone bridge potential is small. Skip when `graph-context = standalone`. |

Quantify before recommending. An unquantified hunch is not a finding.

### 6. Propose a filter — mandatory, per confirmed issue

For each confirmed issue, propose a filter expression against the
source table. Filters must:

1. **Be defensible** — the threshold ties to evidence from Phase 5,
   not intuition or prior datasets. Cite the rows/edges/entities
   numbers in the rationale. **In the combined-graph case (the
   default `graph-context`), behavioral implausibility is itself
   defensible evidence**: per-entity activity that's unrealistic for
   the entity type (a `person` with 400+ identifiers, a `device`
   with degree > 1, a `household` carrying 50 phones) justifies a
   filter even when standalone bridge potential within this source
   is bounded — because UNIONing with other sources will spread the
   bad attachment. Cite the behavioral threshold and the realistic
   benchmark.
2. **Be minimal** — remove the bad edges and as little else as
   possible. Maximal filters (drop the whole identifier column,
   drop every value with degree > 1) are usually wrong.
3. **Be reported with impact** — before/after row counts, edges
   removed (estimate or exact), distinct entities preserved.

Filter expression format: plain-English filter against the source
table that a query writer can translate to NQL.

Worked example — hub identifier (applies under either context):

> Filter `H1`: exclude rows where `LOWER(email) IN ('noreply@example.com',
> 'test@example.com', 'foo@bar.baz')`.
> Impact: removes 8,421 rows (0.42%); preserves 1,997,580 rows.
> Removes 1 hub identifier worth 8,421 edges.
> Rationale: each of the listed values has > 500 distinct entities,
> none of which co-occur with each other on any other identifier —
> these are sentinels, not real bridges.

Worked example — long-tail high-degree persons in the combined-graph
case (this is the canonical "looks fine standalone, dangerous when
combined" pattern):

> Filter `H2`: exclude rows where `person_id IN (SELECT person_id
> FROM <source> GROUP BY person_id HAVING COUNT(1) >= 100)`.
> Impact: removes ~5M edges (~0.2%); preserves ~2.66B edges.
> Rationale: the top 100 persons in this source carry 401–554
> identifiers each (max: 554). Within this source alone the bridge
> potential is bounded because identifier_values are unique here,
> but `graph-context = combined` — these persons will be UNIONed
> with edges from other sources, and a single `person` carrying 400+
> identifiers is behaviorally implausible (a real person carries on
> the order of 5–20). Once combined, those over-attached persons
> become bridges into other components. Filter at the source.

If `graph-context = standalone`, the same finding would warrant **no
filter** — the standalone bridge potential is the only thing that
matters and it's bounded here. Always state explicitly which context
the recommendation hinges on.

If a hypothesis is **disproven** (the data does not support it), say
so explicitly and do not propose a filter. Disproven hypotheses go
in the report so the next audit doesn't re-test them blindly.

### 7. Draft the audit report — mandatory

Draft the report using the template at
[`references/REPORT_TEMPLATE.md`](references/REPORT_TEMPLATE.md).
Fill in the headings + tables; the template handles structure. Order
findings **by severity (rows / edges / entities affected,
descending)** per the user's explicit ask. The "Recommended
clean-view NQL" block is filled in by Phase 8 — leave it as a
placeholder for now.

The findings are the audit's diagnostic deliverable; the clean-view
NQL (Phase 8) is its operational deliverable. Both ship together in
the final report.

### 8. Compose the recommended clean-view NQL — mandatory

The caller needs an actionable artifact, not just a list of filters in
prose. Phase 8 converts the consolidated filter set into a validated
`CREATE MATERIALIZED VIEW` query that anyone (operator, pipeline, or
the downstream graph-build skill) can run to produce a graph-ready
clean source.

#### Branch on findings

- **Zero confirmed issues** (every hypothesis disproven, or every
  confirmed issue has impact below the noise threshold you set in
  Phase 2): **skip the NQL composition**. In the report's
  "Recommended clean-view NQL" section, write exactly:

  > The source passed the audit. No materialization is required;
  > `<source>` is graph-ready as-is. Pass it to the graph build
  > directly.

  `<source>` is the fully qualified NQL reference recorded in Phase 2
  — `company_data.<table>` for a dataset, `<owning_company_slug>.<rule_name>`
  for an access rule. Stop. Do not invoke `/write-nql`.

- **One or more confirmed issues**: continue to the next step.

#### Hand off to `/write-nql` (validate-only)

Invoke `/write-nql --no-explain` with the brief at
[`references/CLEAN_VIEW_NQL_PROMPT.md`](references/CLEAN_VIEW_NQL_PROMPT.md).
That reference covers the pre-flight filter consolidation (dedupe,
keep-predicate phrasing, explicit column projection), the verbatim
prompt body, and the post-flight validation loop. If the source is
an access rule, also see
[`references/ACCESS_RULES.md`](references/ACCESS_RULES.md) for the
invocation delta (drop `--dataset`, swap the source reference, adjust
the view name).

#### Embed in the report

Replace the Phase 7 "Recommended clean-view NQL" placeholder with
the fill-in block from
[`references/REPORT_TEMPLATE.md`](references/REPORT_TEMPLATE.md)
— the verbatim NQL plus the estimated-impact bullets (rows kept /
removed, entities preserved, hub components prevented).

The NQL block is the final hand-off. This skill does not run it, does
not schedule it, and does not trigger the graph build.

## References

- [`references/ACCESS_RULES.md`](references/ACCESS_RULES.md) — dataset-vs-access-rule tool substitutions, NQL reference patterns, sample/stats workarounds, and Phase 8 invocation deltas. Read in Phase 2 if the source is (or might be) an access rule.
- [`references/FAILURE_MODE_TAXONOMY.md`](references/FAILURE_MODE_TAXONOMY.md) — full 8-row starter taxonomy with detection patterns and graph-quality impact. Read in Phase 3 when generating hypotheses.
- [`references/COMMON_CASES.md`](references/COMMON_CASES.md) — per-graph-type hypothesis starters (person, device, CRM). Read when scoping the audit to confirm which failure modes to prioritize for the specific graph shape.
- [`references/REPORT_TEMPLATE.md`](references/REPORT_TEMPLATE.md) — verbatim markdown skeleton for the Phase 7 audit report, plus the Phase 8 fill-in block for the clean-view NQL.
- [`references/CLEAN_VIEW_NQL_PROMPT.md`](references/CLEAN_VIEW_NQL_PROMPT.md) — Phase 8 brief body for `/write-nql --no-explain`, pre-flight checklist, and post-flight validation loop.
- [`references/EDGE_CASES.md`](references/EDGE_CASES.md) — no-identifier datasets, all-unique identifiers, low row counts, mixed grains, evidence-free thresholds, oversized filters, overlapping hypotheses, post-build invocations, zero-issue outcomes, unvalidatable materialization queries. Read when the dataset doesn't fit the audit's assumptions.
- [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md) — `narrative-mcp` / `/design-analysis` / `/write-nql` unavailable, `AskUserQuestion` fallback. Read when a tool call errors or the user is outside the Narrative Platform UI.
- `docs/authoring-skills.md` — house conventions this skill follows.
- `plugins/narrative-common/skills/design-analysis/` — Phase 4 hypothesis-testing handoff; orchestrates the parallel `/write-nql` batch.
- `plugins/narrative-common/skills/write-nql/` — Phase 8 direct call (validate-only); reached transitively via `/design-analysis` for Phase 4.
- `plugins/narrative-common/skills/generate-rosetta-stone-mappings/` — run first if identifier columns aren't yet mapped.
- `plugins/narrative-common/skills/profile-dataset/` — Phase 2 delegates the base profile (row count, per-column coverage, quality flags) here instead of reading stats inline.

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

- `skill_name`: `narrative-identity:triage-pregraph-data` (use this verbatim).
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
