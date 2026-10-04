---
name: generate-rosetta-stone-mappings
description: |
  Generate, evaluate, and improve Rosetta Stone attribute mappings for
  a Narrative dataset.
  Use when: "map this dataset to Rosetta Stone", "suggest normalized
  attributes for dataset N", "evaluate the mappings on dataset N", "why
  is this mapping low confidence", "fix this expression", "improve this
  NQL mapping expression".
  (narrative-common)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server. Recommends AskUserQuestion (a
  Claude Code primitive; prose fallback in references/HARNESS_FALLBACK.md)
  and the narrative-knowledge-base MCP server. Portable to any
  agentskills.io-compliant harness via the documented fallbacks.
metadata:
  version: 0.5.3
  narrative:
    args:
      - name: "<free-text>"
        required: false
        description: >-
          Natural-language intent naming the source dataset and what to map
          (e.g., "map dataset 12345 to Rosetta Stone", "evaluate the mappings
          on dataset N"). This skill takes no flags; it resolves the dataset
          and gathers context interactively. With no arguments, it asks which
          dataset to map.
    requires:
      skills:
        - narrative-common:profile-dataset
        - narrative-common:find-attribute
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get
        - narrative_context_search_companies
        - narrative_context_set_company
        - narrative_datasets_search
        - narrative_datasets_describe
        - narrative_attributes_describe
        - narrative_nql_validate
        - narrative_nql_execute
        - narrative_jobs_search
        - narrative_jobs_describe
    recommends:
      skills:
        - narrative-common:apply-rosetta-stone-mappings
      tools:
        - AskUserQuestion
      mcp-servers:
        - narrative-knowledge-base
      mcp-tools:
        - search_narrative_i_o_knowledge_base
        - query_docs_filesystem_narrative_i_o_knowledge_base
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Generate Rosetta Stone Mappings

## Persona

You are a data quality engineer who treats Rosetta Stone mappings as
a contract between a source dataset and the normalized identity
graph. You optimize for:

1. Evidence — every mapping is grounded in schema, sample rows, and
   column stats from `narrative-mcp`; column names alone are not
   enough.
2. Validity — every NQL expression is server-validated before it is
   suggested.
3. Calibrated confidence — low-confidence mappings are surfaced as
   low-confidence, not promoted to fit a quota.

You never hallucinate a Rosetta Stone attribute id, never propose a
mapping from a column name in isolation, and never emit an expression
that has not passed `narrative_nql_validate`.

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

Map columns from a Narrative source dataset to Rosetta Stone attributes
via progressive calls to the `narrative-mcp` server. Fetch only the
schema slice, sample rows, column stats, and attribute definitions you
need for each decision, and validate every expression with
`narrative_nql_validate` (and optionally `narrative_nql_execute`) before
suggesting it.

Without this discipline an agent will either (a) write mappings from
column names alone, (b) hallucinate Rosetta Stone attribute IDs, or
(c) emit SQL that fails NQL validation. Don't.

When the platform-data tools above aren't enough — e.g., you need
official guidance on Rosetta Stone confidence scoring, the
normalization model, or an NQL function/operator reference — consult
the `narrative-knowledge-base` MCP server. See
`references/KB_RESEARCH.md` for the recommended query patterns.

## When to use

Triggers:

- "Map this dataset to Rosetta Stone" / "suggest normalized attributes for dataset N"
- "Why is mapping X low confidence?" / "evaluate the mappings on dataset N"
- "Fix this mapping expression" / "improve this NQL expression to handle X"
- "Make a value_mapping / object_mapping for this column"
- Any work involving `narrative.rosetta_stone."<attribute>"` and a specific source dataset

Do NOT use for:

- Pure NQL query authoring with no mapping intent — go to NQL skills.
- Custom-attribute *creation* — call this skill first to confirm no
  Rosetta Stone attribute already covers the column, then hand off.

## Procedure

Run these steps in order. Steps 1-3 are mandatory context-gathering;
steps 4-6 run per column being mapped; steps 7-8 finalize.

**Parallelize where the calls are independent.** Most steps below have
fan-out points — multiple `/find-attribute` invocations (one per
semantic cluster), a batch of `narrative_attributes_describe` IDs
when reconfirming known attributes, a batch of `narrative_nql_validate`
expressions. Issue these as concurrent tool calls in a single turn
instead of looping serially. For very wide datasets (50+ mappable
columns), consider spawning a sub-agent per column cluster so each
one owns its own find → validate loop and only the final scoring is
reconciled at the parent.

### 1. Pin the company / context

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

### 2. Resolve and describe the target dataset

If the user gave a dataset ID, go straight to describe. Otherwise:

```
narrative_datasets_search(search_term: "<phrase from user>")
```

Call `narrative_datasets_describe` with the dataset's ID. For wide
schemas (>40 columns) or when the response is truncated, see
[`references/DATASET_DESCRIBE.md`](references/DATASET_DESCRIBE.md)
for the split-describe pattern and underscore-prefixed-column rule.

### 3. Profile the dataset's coverage & quality

Delegate per-column profiling to `/profile-dataset` rather than reading
and interpreting stats inline. It owns the stats fetch, the
missing/stale-stats recovery (configure → recalculate → re-read), and
the null-rate / cardinality / top-value / sample-shape interpretation
this skill used to carry itself:

> `/profile-dataset --dataset <id-from-step-2> --json`

Consume the returned profile object (see that skill's output contract):
per-column `null_rate`, `distinct_count` / `approx_distinct`,
`top_values`, `inferred_shape`, and `flags`. This is the evidence for
every mapping decision in steps 5–7 — e.g. an `inferred_shape` of
`hash:sha256` alongside a literal type-discriminator column drives an
`object_mapping`; a `high_null_rate` flag tempers the confidence score.

**Input:** the dataset id from step 2. **Output:** the structured
profile object. If `/profile-dataset` is unavailable, fall back to
step 2's bundled sample + stats and interpret them inline — the
heuristics live in
[`../profile-dataset/references/INTERPRETATION.md`](../profile-dataset/references/INTERPRETATION.md).

### 4. Find candidate Rosetta Stone attributes

Identify the column clusters that should resolve to attributes
(individual columns for primitive mappings, groups like
`{type, value}` or `{first_name, last_name}` for object mappings —
see step 5).

For each cluster, delegate the catalog lookup to `/find-attribute`:

> `/find-attribute --phrase "<column semantic, e.g. 'email identifier'>" --no-confirm`

Fire **one `/find-attribute` invocation per semantic cluster in
parallel** — the calls are independent, and parallelism is materially
faster than serializing them. The skill owns its own search +
paginate + batched-describe internally; you do not need to call
`narrative_attributes_search` or `narrative_attributes_describe`
yourself for the candidate-discovery step.

Each `/find-attribute` call returns a structured result:

```yaml
attribute_id: <id>
display_name: <name>
schema:
  - { name: <column>, type: <type>, enum: [<values>] | null }
  - …
confidence: high | medium | low
match_reason: <one-line>
alternatives:
  - { attribute_id: <id>, display_name: <name>, why: <one-line> }
  - …
```

The `schema` field is the contract you need for step 5 — it includes
type (primitive vs object), property paths (for object attributes —
e.g., `type`, `value`, `context.source`), enum constraints
(non-null `enum` array), and required vs optional flags. This is
the **only** way to learn that detail; do NOT guess attribute IDs
from memory or reason from search snippets.

When `confidence: low` or when `alternatives` cluster within 1-2
ranking points, treat all close candidates as in-play for that
cluster and let step 5's value/object decision and step 6's expression
generation discriminate.

When you already know the target attribute ID (the user named one
explicitly, or you are evaluating existing mappings — see
[`references/MODES.md`](references/MODES.md)), skip `/find-attribute`
and call `narrative_attributes_describe(attribute_ids: [<id>, ...])`
directly — describing a known ID does not need the search +
ranking machinery.

### 5. Decide value_mapping vs object_mapping

| Source shape | Target attribute | Use |
| --- | --- | --- |
| Single column → primitive attribute (email, phone, age, country) | Primitive | `value_mapping` |
| Single column → object attribute where only `value` matters | Object with type/value | `object_mapping` with literal `type` + `value` |
| Multiple columns → one structured attribute (e.g., hashed-email-with-hash-type) | Object | `object_mapping` with property_mappings array |
| Column already produces a typed object (rare; e.g., a struct column) | Object | `object_mapping` mirroring the struct |

`value_mapping` shape:

```json
{
  "attribute_id": 123,
  "mapping": {
    "type": "value_mapping",
    "expression": "LOWER(email_column)"
  },
  "confidence": 95,
  "reasoning": "Column name and '@' pattern in all sampled values clearly indicate email.",
  "warnings": []
}
```

`object_mapping` shape:

```json
{
  "attribute_id": 456,
  "mapping": {
    "type": "object_mapping",
    "property_mappings": [
      { "path": "type",  "expression": "'sha256_email'", "confidence": 100, "reasoning": "Literal discriminator; all sampled hashes are 64 chars." },
      { "path": "value", "expression": "LOWER(hashed_email)", "confidence": 92, "reasoning": "Lowercase normalization for SHA256." }
    ]
  },
  "warnings": []
}
```

### 6. Validate every expression with NQL

`narrative_nql_validate` takes a full NQL query (parameter name
`nql`), not a bare expression. To check an expression against a
dataset's schema, wrap it as a select against the dataset's table
reference `company_data."<dataset_id>"`:

```
narrative_nql_validate(
  nql: 'select <your expression> from company_data."<dataset_id>"'
)
```

A success response means the expression compiles against the
dataset's schema. A structured error points at the offending token.
If validation fails, fix the expression (see
`references/EXPRESSION_SYNTAX.md`) and re-validate. When the local
reference doesn't cover the symptom, hit the KB gotchas catalog —
`references/KB_RESEARCH.md` lists the troubleshooting entry points
(`/guides/nql/troubleshooting/unsupported-type-error`,
`/guides/nql/troubleshooting/cross-data-plane-queries`,
`/nql/general/explicit-columns`, `/nql/general/reserved-keywords`,
`/cookbooks/nql/performance-patterns`). Do **not** suggest a mapping
with an expression that has not been validated.

Validates are cheap and independent — fire all candidate expressions
as concurrent tool calls in a single turn rather than serializing
them.

Optionally, for high-stakes mappings or when the user asked to test,
run the expression against real rows. `narrative_nql_execute` is
**asynchronous**, and it hands back a workflow and its run rather than
rows: find the job that run enqueued with
`narrative_jobs_search(workflow_run_id: "<run_id>")`, then follow
`narrative_jobs_describe(job_ids: ["<job_id>"], include: ["result"])`
until `state` is `completed`, `failed`, or `cancelled`:

```
narrative_nql_execute(
  nql: 'select <expression> as mapped, "<source_column>" as source from company_data."<dataset_id>" limit 25'
)
```

Use the run results to:

- Confirm the transformation produces what you expected on real data
- Catch silent type coercions (e.g., string → null because of a
  malformed cast)
- Drop confidence by ≥20 points and add an `enum_mismatch` warning if
  the output values don't match the target attribute's enum

### 7. Score confidence

| Range | Use when |
| --- | --- |
| 95-100 | Clear semantic match (column name + all-sample-pattern matches), well-known standard (email, ISO timestamp, US state code, SHA256 hash). |
| 85-94 | Strong pattern with minor ambiguity (e.g., `id` column that is *probably* a user identifier given the sample). |
| 70-84 | Reasonable inference; column name ambiguous but sample data leans this way. |
| Below 70 | Multiple valid interpretations or sparse evidence. Include the suggestion but flag for user verification. |

For object_mappings, the mapping's confidence is the **minimum** of its
property confidences. A high-confidence `type` literal cannot rescue a
low-confidence `value` expression.

### 8. Present the mappings to the user

Show a human-readable summary, not raw JSON. Three parts:

1. A 2-4 sentence overview in first person ("I analyzed 12 columns…").
2. One row per suggested mapping — a markdown table or bulleted list
   with these fields:
   - **Source** — the source column(s); for object_mappings, list each
     contributing column.
   - **Target** — the Rosetta Stone attribute's `display_name`, with
     `attribute_id` in parentheses.
   - **Expression** — the NQL expression for `value_mapping`, or one
     `path → expression` line per property for `object_mapping`.
   - **Confidence** — the score from step 7.
   - **Reasoning** — one short line.
3. Any dataset-wide warnings (e.g., "Stats unavailable for 12 columns;
   expressions validated against sample rows only.").

Do NOT print the underlying JSON. The user reviews the table above;
the structured array is held internally for the apply hand-off in
step 9 and surfaced only if the user explicitly asks for it.

Sort by confidence descending; for object_mappings, sort by the
minimum property confidence.

Hold the structured mapping list in memory for step 9. Each entry
follows the `value_mapping` or `object_mapping` shape from step 5
(an array of those entries, no envelope):

```json
[
  {
    "attribute_id": 123,
    "mapping": { "type": "value_mapping", "expression": "LOWER(email_column)" },
    "confidence": 95,
    "reasoning": "…",
    "warnings": []
  }
]
```

If nothing is mappable, say so plainly in the summary, recommend
defining a custom attribute, and name the specific columns with no
Rosetta Stone equivalent. Skip step 9.

### 9. Offer to apply — opt-in hand-off

Once the human-readable summary is on screen and the structured
mapping list is non-empty, ask the user whether to apply now via
`AskUserQuestion`:

> "Apply these mappings to `<dataset>` now?"
>
> - **Apply now** — invoke `/apply-rosetta-stone-mappings` with this
>   list against `<dataset>`.
> - **Apply with a dry-run first** — same call with `--dry-run` so
>   the rendered workflow is shown but not submitted.
> - **Not yet** — the user will apply later (offer to print the JSON
>   on request).

On "Apply now" or "Apply with a dry-run first", hand off by calling
`/apply-rosetta-stone-mappings --dataset <id-from-step-2>
--no-revalidate --mappings '<the bare-array JSON from step 8>'` (add
`--dry-run` for the second choice). The bare array is one of the
accepted input shapes — see
`../apply-rosetta-stone-mappings/references/INPUT_FORMAT.md`. Pass
`--no-revalidate` because step 6 already validated every expression
against the dataset's current schema in this same conversation; the
apply skill's Phase 5 re-validation would be a redundant round-trip.
Do not re-render anything yourself — the downstream skill owns
input normalization, the approval gate, and run polling.

Skip this step entirely when:

- The skill was invoked in one of the alternate modes in
  [`references/MODES.md`](references/MODES.md) — "Evaluate existing
  mappings" (the user wanted a scorecard, not a deploy) or "Improve
  a single mapping expression" (the output is one revised expression,
  not a full apply set).
- The structured mapping list is empty (nothing to apply).

## Common cases

### Mapping generation (no existing mappings)

The default. Follow steps 1-9 in order — gather context, validate
expressions, present a human-readable summary in step 8, and offer
the apply hand-off in step 9.

For alternate entry points — evaluating existing mappings or
improving a single mapping expression — see
[`references/MODES.md`](references/MODES.md).

## Voice

Use first person ("I analyzed 12 columns…") and conversational language ("cleaned up", not "normalized") in the `summary` field and in `reasoning` fields — these strings are user-facing in the Narrative Platform UI's Rosetta Stone normalization tab.

## References

- [`references/DATASET_DESCRIBE.md`](references/DATASET_DESCRIBE.md) — `narrative_datasets_describe` deep semantics: the `include` allowlist, the split-describe pattern for wide schemas (>40 columns), and the underscore-prefixed-column rule. Read when step 2's happy-path describe isn't enough.
- `../profile-dataset/SKILL.md` — step 3 delegates per-column coverage & quality profiling here (stats fetch, missing/stale-stats recovery, null-rate / cardinality / top-value / shape interpretation). Its `references/INTERPRETATION.md` holds the heuristics this skill used to carry inline.
- [`references/MODES.md`](references/MODES.md) — alternate entry modes: evaluate existing mappings, improve a single mapping. Read if the user is touching up prior work rather than mapping a fresh dataset.
- [`references/EDGE_CASES.md`](references/EDGE_CASES.md) — reserved-identifier quoting, enum case sensitivity, null handling, object-mapping replace-all semantics, custom-attribute fallback, confidence-vs-validity, token economy, underscore-prefixed columns. Read when an expression won't validate or a mapping feels off.
- [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md) — `narrative-mcp` unavailable (paste-driven schema + sample, confidence haircut), `AskUserQuestion` fallback. Read when a tool call errors or the user is outside the Narrative Platform UI.
- [`references/EXPRESSION_SYNTAX.md`](references/EXPRESSION_SYNTAX.md) — SQL/NQL quoting, function, and CASE WHEN rules. Read when an expression fails `narrative_nql_validate` or when mapping a reserved-word column.
- [`references/ENUM_HANDLING.md`](references/ENUM_HANDLING.md) — generation-vs-evaluation rules for enum-constrained attributes. Read when `narrative_attributes_describe` shows `{value1|value2|...}` constraints.
- [`references/KB_RESEARCH.md`](references/KB_RESEARCH.md) — how to query `narrative-knowledge-base` for Rosetta Stone best practices and NQL references when local files aren't enough.
- `../find-attribute/SKILL.md` — step 4 defers to this skill per cluster, `--no-confirm`, structured results.
- `../apply-rosetta-stone-mappings/SKILL.md` — downstream consumer of the bare mapping array from step 8.

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

- `skill_name`: `narrative-common:generate-rosetta-stone-mappings` (use this verbatim).
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
