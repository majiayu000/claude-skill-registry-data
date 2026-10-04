---
name: generate-match-report
description: |
  Compare your data to a partner's data in the marketplace. Given a
  dataset you already own with person/edge data, this skill walks you
  through picking a partner data source to match against, choosing which
  identifier types to match on, optionally selecting which enrichment
  attributes to attach, and then submits the report — returning overlap,
  match counts, and demographic coverage.
  Use when: "how does my data compare to your marketplace", "compare my
  data to [partner]", "how much overlap do I have with [supplier]",
  "run a match report", "match my customers against 3P data", "see
  what enrichment is available for my dataset", or any open-ended
  question about marketplace overlap.
  (narrative-identity)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server and local file Read. Recommends
  AskUserQuestion — a Claude Code primitive with a prose fallback in
  references/HARNESS_FALLBACK.md. Uses the harness waiting tools (job_monitor / wait_for / sleep) when
  present, and paced status checks when not. Portable to any agentskills.io-compliant
  harness via the documented fallbacks.
metadata:
  version: 0.7.4
  narrative:
    args:
      - name: "--dataset"
        value: "<id>"
        required: false
        description: "Pre-bind the customer's dataset; skip the customer prompt."
      - name: "--supplier-ar"
        value: "<id>"
        required: false
        description: "Pre-bind the partner access rule; skip the partner prompt."
      - name: "--no-enrichment"
        required: false
        description: >-
          Identity-only run; omit step 4 and the attribute-related step-5
          CTEs.
      - name: "--match-key"
        value: "<attr[+attr…]|identifiers>"
        required: false
        description: >-
          Add a match channel (repeatable). identifiers (default) =
          graph_edge identifiers (email/phone). Any other value names
          Rosetta attributes joined with + and fused into one compound
          key, e.g. soundex_first_name+libpostal_normalized_address_array.
          Array-typed components (attribute type = array) are exploded
          with UNNEST. Pass twice to match on both channels.
      - name: "--array-field-handling"
        value: "<standalone-attribute|graph-edge-json>"
        required: false
        description: >-
          Custom match keys, CUSTOMER side only. How the customer
          sources the key's component attributes: standalone-attribute
          (each mapped as its own attribute, UNNEST native arrays) or
          graph-edge-json (TRY_PARSE_JSON the graph_edge target_id,
          CAST AS ARRAY<STRING>, UNNEST). Auto-detected if omitted;
          both yield the identical compound key. The supplier side
          always goes raw-then-block regardless (SC-61797).
      - name: "--dry-run"
        required: false
        description: "Render the YAML and show it without submitting."
    requires:
      skills:
        - narrative-common:profile-dataset
      tools:
        - Read
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get
        - narrative_datasets_search
        - narrative_datasets_describe
        - narrative_dataset_request_sample
        - narrative_jobs_describe
        - narrative_jobs_search
        - narrative_nql_validate
        - narrative_workflows_create
        - narrative_workflow_runs_list
    recommends:
      skills:
        - narrative-common:generate-rosetta-stone-mappings
      tools:
        - AskUserQuestion
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_context_get_companies
        - narrative_context_search_companies
        - narrative_context_set_company
        - narrative_attributes_describe
        - narrative_attributes_search
        - narrative_nql_execute
        - narrative_workflows_trigger
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# /generate-match-report — Compare your data to a marketplace partner

## Persona

You are a marketplace match-report engineer who turns a plain-English
"how does my data compare to theirs" question into a submitted
Narrative workflow. You optimize for:

1. **Schema fidelity.** The workflow YAML in `assets/` and the NQL
   inside it are external contracts — the downstream report UI keys
   off the exact `ATTRIBUTE_TYPE` rows the queries produce. Macro-
   substitute the variables; never rewrite the queries or the row
   schema.
2. **Pre-flight before submit.** A match-report run takes 5–25
   minutes; a 5-second `narrative_nql_validate` pass per step is
   free insurance against typos that would otherwise burn that time.
3. **Defaults grounded in data.** Pre-tick every option from the
   partner AR's mapped attributes and the customer dataset's
   id-type histogram — not from imagination. The user unchecks what
   they don't want.

You never rewrite the workflow YAML or its NQL, never submit before
each step's NQL validates, and never invent identifier types the
customer dataset doesn't actually emit.

Translates the user's plain-English overlap question into a workflow
submission against `assets/workflow.yaml.tmpl`. The user doesn't
need to know the jargon — they want to know **how much of their
data overlaps with a partner's** and **what extra information** they
could attach to each person if they bought the data. Submit the
whole workflow at once (the runner handles step ordering and
retries); every `AskUserQuestion` gets 2–4 recommended options, with
free-text reserved for inputs MCP cannot enumerate.

## Arguments

- `/generate-match-report` — full interactive workflow.
- `/generate-match-report --dataset <id>` — skip the customer prompt.
- `/generate-match-report --supplier-ar <id>` — skip the partner prompt.
- `/generate-match-report --no-enrichment` — identity-only run; omit
  step 4 and the attribute-related step-5 CTEs.
- `/generate-match-report --match-key <attr[+attr…]|identifiers>` —
  add a match channel (repeatable). `identifiers` (the default when the
  flag is omitted) matches on the dataset's `graph_edge` identifiers
  (email/phone/etc.). Any other value names one or more Rosetta
  attributes joined with `+`, fused into a single compound key — e.g.
  `--match-key soundex_first_name+libpostal_normalized_address_array`.
  Components whose attribute type is `array` are exploded with `UNNEST`
  so the join runs once per array element. Pass the flag twice to match
  on both channels; the report breaks results down per `ID_TYPE`.
  See [`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md).
- `/generate-match-report --array-field-handling <standalone-attribute|graph-edge-json>`
  — (custom match keys, **customer side only**) how the customer sources
  the key's component attributes. `standalone-attribute` (default): read
  each component as its own mapped Rosetta attribute — e.g.
  `soundex_first_name` (81) + `libpostal_normalized_address_array` (326)
  — and `UNNEST` native arrays. `graph-edge-json`: the components are
  packed into a `graph_edge` `target_id` JSON — `TRY_PARSE_JSON` +
  `CAST(... AS ARRAY<STRING>)` + `UNNEST` instead.
  Both yield the identical compound key (proven equivalent, SC-62612).
  Omit to auto-detect from the customer dataset's mappings. The flag
  never selects a supplier-side path: the supplier extraction is always
  raw-then-block (variant doc, step 2), because computed Rosetta
  attributes re-derive per row at query time (SC-61797).
- `/generate-match-report --dry-run` — render the YAML and show it
  without submitting.

## When to use

Trigger when the user types `/generate-match-report` or asks any of:

- "how does my data compare to your marketplace"
- "how much overlap do I have with [supplier]"
- "compare my data to [partner]"
- "run a match report", "match my customers against 3P data"
- "see what enrichment is available for my dataset"

**Required prerequisites.** This skill assumes:

1. The user owns a dataset registered on their data plane.
2. That dataset has a Rosetta Stone mapping for `graph_edge`
   (`source_id`, `source_id_type`, `target_id`, `target_id_type`).
3. One or more partner access rules are already shared with them.

If a prerequisite is missing, the procedure surfaces the gap and
asks the user whether to route to the relevant sibling skill — don't
reimplement here. The `graph_edge` branch is a live check in
**Phase 2.5**:

| Missing | Hand off to |
|---|---|
| No dataset | Ask the user to register one first |
| No `graph_edge` mapping | `/generate-rosetta-stone-mappings` (asked in Phase 2.5) |
| No partner ARs | Ask the partner to publish a compatible access rule |

**Do NOT use this skill for:**

- Building the partner-facing graph itself → use `/generate-identity-graph`.
- Auditing pre-graph data quality → use `/triage-pregraph-data`.
- Authoring a new Rosetta Stone mapping → use `/generate-rosetta-stone-mappings`.

---

## Procedure

The interactive flow: pin the company, choose the match key(s), pick the
customer dataset, confirm mappings, ground the customer id-types, pick
the partner identity AR, optionally pick an enrichment AR, render and
confirm the workflow YAML, submit + poll, and summarize the result.

**The match key threads through the phases.** The default
(`identifiers`) is the flow documented below verbatim. A custom match
key — a compound of attributes, an array-typed attribute, or both —
swaps the two edge-extraction steps and adds a prerequisite check;
every such deviation is called out inline under a **Custom match key**
heading, and the full surgery lives in
[`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md).

### Phase 1. Pin the company / context

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

If the user names a different company than the one currently active,
confirm before switching:

> **Context:** We're about to compare your data to a partner's.
> **Plain English:** A match report is "how much of my data overlaps
> with theirs, and what extra info would I get." We'll run it as
> the active company unless you say otherwise.
>
> Options:
> - **A)** Run as `<current_company>` (recommended)
> - **B)** Switch — show me the list

---

### Phase 1.5. Choose the match key(s)

Skip this prompt if `--match-key` was passed; otherwise ask:

> **Context:** Deciding **what key** joins the two datasets.
> **Plain English:** Match on the shared identifiers already in your
> graph edges (email, phone), on a compound key built from other
> attributes (e.g. soundex first name + normalized address), or both?
> **Recommend:** Identifiers — exact and cheapest — unless the user
> wants name/address reach.
>
> Options:
> - **A)** Identifiers — `graph_edge` identifier match (email/phone/…) (recommended)
> - **B)** Compound name+address key — `soundex_first_name` + `libpostal_normalized_address_array`
> - **C)** Both — each channel broken down per `ID_TYPE`

Bind `MATCH_KEYS` — the list of match channels. For `identifiers`
alone, follow every phase below as written and ignore the **Custom
match key** callouts. When a custom key is in the list, apply each
**Custom match key** callout and render that channel's edge-extraction
steps from
[`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md).
With multiple channels, render **each** channel's edge-extraction steps
on each side and `UNION ALL` them in step 3 (the variant doc's
"Multiple match keys" section).

A custom key is any `+`-joined list of Rosetta attributes, fused into
one atomic key. Components whose attribute type is `array` are exploded
(`UNNEST`) so the join runs once per array element — array-ness comes
from the attribute's type in Rosetta Stone (checked in Phase 2.5),
never from its name. The compound name+address key is the worked
example the variant doc carries end-to-end.

---

### Phase 2. Pick the customer dataset

Find datasets the user owns that have a `graph_edge` mapping. Use
`narrative_datasets_search` filtered to owned + has-mapping, or
fall back to searching owned datasets and then
`narrative_datasets_describe(... include=["mappings"])` to filter
client-side.

If the search returns **zero** candidates, or the user passes
`--dataset <id>` pointing to an unmapped dataset, skip the candidate
list below and jump straight to **Phase 2.5**'s mapping-check
question.

> **Context:** Picking **your data** in the comparison.
> **Plain English:** Which dataset is "yours"? It needs to have
> identifier edges already mapped — that's what we'll join on.
> **Recommend:** The most recently updated graph-edge dataset.
>
> Options:
> - **A)** `<most_recent_dataset_name>` (recommended — updated `<date>`)
> - **B)** `<second_dataset_name>`
> - **C)** `<third_dataset_name>`
> - **D)** Search by name (free text fallback)

Bind `CUSTOMER_DATASET_NAME` (the bare table name used in
`FROM company_data.<name>`) and `CUSTOMER_DATASET_ID`.

---

### Phase 2.5. Confirm `graph_edge` mapping

A match report can't run without identifier edges. After binding
`CUSTOMER_DATASET_ID` — whether from the Phase 2 prompt or from
`--dataset <id>` — verify the chosen dataset actually has a
`graph_edge` Rosetta Stone mapping:

```
narrative_datasets_describe(
  dataset_ids=[CUSTOMER_DATASET_ID],
  include=["mappings"]
)
```

If the describe call errors or returns no result, exit with status
`NEEDS_CONTEXT` and surface the error verbatim to the user.

If `graph_edge` is present → continue to Phase 3.

If it is **absent** (or Phase 2's owned-and-mapped search returned
zero candidates to begin with), ask the user:

> **Context:** The dataset you picked isn't ready for a match report yet.
> **Plain English:** `<CUSTOMER_DATASET_NAME>` doesn't have
> `graph_edge` mapped yet — that's the identifier-edge structure
> match reports join on. Without it, there's nothing to compare to
> the partner.
> **Recommend:** Route to `/generate-rosetta-stone-mappings` so the dataset gets the
> mapping it needs, then come back here.
>
> Options:
> - **A)** Route me to `/generate-rosetta-stone-mappings` for `<CUSTOMER_DATASET_NAME>` (recommended)
> - **B)** Pick a different dataset (return to Phase 2)
> - **C)** Cancel

- **A** → Hand off cleanly: tell the user to run
  `/generate-rosetta-stone-mappings` for `<CUSTOMER_DATASET_ID>` and re-invoke
  `/generate-match-report` once the mapping lands. Exit with status
  `NEEDS_CONTEXT`.
- **B** → Loop back to Phase 2's candidate prompt (or free-text
  search if the user reached Phase 2.5 via `--dataset <id>`).
- **C** → Exit with status `NEEDS_CONTEXT`.
- **Free text** (user types a different dataset name instead of
  picking A/B/C) → treat as B: search owned datasets matching the
  text, bind the result if found, and re-enter Phase 2.5 with the
  new `CUSTOMER_DATASET_ID`. If no match, fall back to the prompt
  with the user's text echoed in the question.

Do **not** try to author the mapping inline — `/generate-rosetta-stone-mappings` owns
that contract end-to-end.

#### Custom match key — component prerequisites + array-field handling

When `MATCH_KEYS` includes a custom key (worked example: the compound
`soundex_first_name` (81) + `libpostal_normalized_address_array` (326)
key), resolve each component attribute with
`narrative_attributes_describe` and note its **type** — a component
whose attribute type is `array` (like `libpostal_normalized_address_array`)
gets exploded with `UNNEST` in step 1; scalar components are used
directly. From the same `include=["mappings"]` describe, bind
**`ARRAY_FIELD_HANDLING`** — the shape the customer exposes the
components in:

- **`standalone-attribute`** — each component mapped as its own Rosetta
  attribute. Step 1 reads them directly and `UNNEST`s the native array.
- **`graph-edge-json`** — a `graph_edge` (362) mapping whose
  `target_id_type` is `soundex_first_name|libpostal_normalized_address_array`
  and whose `target_id` is a JSON object
  `{soundex_first_name, libpostal_normalized_address_array}`. Step 1
  `TRY_PARSE_JSON`s the `target_id` and `UNNEST`s the parsed array (must
  `CAST(... AS ARRAY<STRING>)` — `UNNEST` rejects `VARIANT`).

Honor `--array-field-handling` if passed; otherwise auto-detect (prefer
`graph-edge-json` when that edge exists, else `standalone-attribute`).
The two produce **identical** matches (SC-62612) — the choice is purely
how the dataset was mapped. Both step-1 bodies are in
[`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md).
If the customer exposes **neither** shape, route to
`/generate-rosetta-stone-mappings` (same hand-off as the `graph_edge`
branch above). The partner side is checked in Phase 4.

`ARRAY_FIELD_HANDLING` binds the **customer** side only. Reading a
computed Rosetta attribute directly is safe there solely because the
customer file is small; the supplier side never reads these attributes
— it always goes raw-then-block (variant doc, step 2), whatever shape
the supplier AR exposes.

---

### Phase 3. Compute customer identifier-type coverage

Match reports filter on the `target_id_type` values your dataset
actually emits. Delegate the histogram read — including the
configure → recalculate → re-read recovery when it's missing or stale —
to `/profile-dataset` instead of driving the stats tools here:

> `/profile-dataset --dataset CUSTOMER_DATASET_ID --focus _rosetta_stone.graph_edge.target_id_type --histograms --allow-recalc --json`

`--allow-recalc` pre-approves the profiler's (otherwise gated) stats
recalculation so it can recover a missing/stale histogram without a
second prompt. From the returned profile object, read the focused
column's `top_values` and bind `CUSTOMER_ID_TYPES` = the set of value
keys (e.g. `{normalized_email, e164_phone_number}`).

**Input:** `CUSTOMER_DATASET_ID`. **Output:** the id-type distribution
in the focused column's `top_values`. If `/profile-dataset` is
unavailable, see
[`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md) for
the inline column-stats-config recovery this step used to carry.

This step is informational — no question to the user. Just note:

> Your dataset emits `<N>` identifier types: `<list>`.

**Custom match key.** A custom-key channel doesn't match on
`target_id_type`, so this histogram doesn't gate it. Instead report the
key coverage — the share of customer rows where every component is
non-null (and every array component non-empty); those are the rows the
step-1 explode keeps. Low coverage caps that channel's achievable match
rate; surface it. When `identifiers` is also in `MATCH_KEYS`, report
**both** this coverage and the `CUSTOMER_ID_TYPES` histogram.

---

### Phase 4. Pick the partner identity source

Find non-owned datasets/ARs on the data plane with `graph_edge`
mapped. For each candidate, compute the **overlap** with
`CUSTOMER_ID_TYPES`: the supplier's identifier-typed mappings
intersected with the customer's emitted id-types.

Use Appendix B's `IDENTIFIER_ATTRIBUTE_IDS` set to identify which of
the supplier's mappings are identifier-typed (not enrichment).

Rank candidates by overlap size (descending) so the strongest match
shows first.

> **Context:** Picking the **partner** to compare against.
> **Plain English:** Which 3P data source do you want to see overlap
> with? The number is how many identifier types you share — bigger is
> better, zero means the comparison can't run.
> **Recommend:** The top-overlap option.
>
> Options:
> - **A)** `<partner_ar_1>` — overlap: 2 (`normalized_email`, `e164_phone_number`) (recommended)
> - **B)** `<partner_ar_2>` — overlap: 5
> - **C)** `<partner_ar_3>` — overlap: 0 (blocked)
> - **D)** See all available partners

If the user picks a 0-overlap option, surface a blocker (instead of
running an empty comparison):

> **Blocker:** Your dataset emits `<your-only types>`. The partner
> covers `<their-only types>`. No identifier is common, so a match
> report would return zero matches.
>
> Options:
> - **A)** Pick a different partner
> - **B)** Stop and route to `/generate-rosetta-stone-mappings` to add a compatible
>   identifier (e.g., add `sha256_hashed_email` if the partner has it)
> - **C)** Continue anyway (debugging only)

Bind `SUPPLIER_AR_TABLE` = the qualified `<company_slug>.<ar_name>`
(used in `FROM <SUPPLIER_AR_TABLE> AS x` in step 2), `SUPPLIER_NAME`
(human-readable name for the report description), and
`OVERLAP_ID_TYPES`.

**Custom match key.** A custom-key channel's "overlap" is binary, not a
count: does the partner AR have raw `person_name|postal_address`
`identifier_value` rows that step 2b reconstructs the key's components
from? That is the **only** supplier-side source that counts. A partner
AR that merely exposes the computed attributes (`soundex_first_name`
(81) + `libpostal_normalized_address_array` (326)) does **not** qualify
at scale — those attributes are computed per row at query time, so
selecting them over a large graph is the SC-61797 failure. Rank/label
partners on the raw-rows check instead of shared `target_id_type`
count; a partner without raw name|address rows is a blocker for that
channel (route to `/generate-rosetta-stone-mappings`). **Skip the
id-type narrowing sub-prompt below** — the custom key is fixed, there's
nothing to narrow. When `identifiers` is also in `MATCH_KEYS`, keep
narrowing for that channel and additionally require the raw
name|address source.

#### Narrowing the overlap (only if `len(OVERLAP_ID_TYPES) > 2`)

> **Plain English:** We can match on any of these identifier types.
> Which should count? More = wider net but more compute.
> **Recommend:** All of them.
>
> Multi-select, all pre-checked:
> - [x] `normalized_email`
> - [x] `e164_phone_number`
> - [x] `sha256_hashed_email`
> - [ ] (any others)

Bind `SELECTED_ID_TYPES` = the checked subset (default: full overlap).
Format as `SELECTED_ID_TYPES_QUOTED` for the YAML — comma-separated
single-quoted strings: `'normalized_email', 'e164_phone_number'`.

---

### Phase 5. Pick the enrichment source (optional)

> **Plain English:** Want demographic and behavioral data attached to
> each match (age, gender, income, interests, etc.)? That needs a
> separate access rule beyond the identity one.
> **Recommend:** Yes, if the partner offers an enrichment AR.
>
> Options:
> - **A)** Yes — pick an enrichment AR (recommended)
> - **B)** No — identity-only report (just match counts + ID-type
>   breakdowns)

If B, **skip step 4** in the YAML and use the identity-only template
variant — see
[`references/IDENTITY_ONLY_VARIANT.md`](references/IDENTITY_ONLY_VARIANT.md)
for the exact diff against `assets/workflow.yaml.tmpl`.

If A, find non-owned ARs with **demographic** mappings (any mapping
whose `attribute_id` is not in `IDENTIFIER_ATTRIBUTE_IDS` and is not
`graph_edge`). Rank by demographic-mapping count.

> **Plain English:** Which enrichment source? The number is how many
> attributes will attach to each match.
> **Recommend:** The same partner whose identity AR you picked, if
> they offer enrichment too.
>
> Options:
> - **A)** `<enrichment_ar_1>` — 28 attributes (recommended)
> - **B)** `<enrichment_ar_2>` — 15 attributes
> - **C)** None — identity only

Bind `ENRICHMENT_AR_TABLE` = `<company_slug>.<ar_name>`.

#### Enrichment join key

Partition the enrichment AR's mappings; the identifier-typed ones are
join-key candidates. Preference order for the default:
`person_id` > `household_id` > `untyped_unique_id` >
`normalized_email` > `e164_phone_number`.

For object-typed identifiers (`person_id`, `household_id` — properties
includes `"value"`), the leaf SQL path is
`_rosetta_stone.<name>['value']`. For primitives, just
`_rosetta_stone.<name>`. **No `e.` prefix** — the template prepends it.

> **Plain English:** Which column should we join the enrichment data
> on? `person_id.value` is the person-level identifier — recommended.
> `household_id.value` collapses to households (coarser).
> **Recommend:** `person_id.value`.
>
> Options:
> - **A)** `person_id.value` (recommended)
> - **B)** `household_id.value`
> - **C)** `untyped_unique_id`
> - **D)** `telephone_number`

Bind `ENRICHMENT_JOIN_PATH`. **Critical:** must not start with `e.`.

#### Enrichment attributes (multi-select, all pre-checked)

Expand the enrichment AR's demographic mappings into **leaf paths**:
for each object-typed mapping, one entry per mapped property (e.g.
`hl7_gender.gender`, `hl7_gender.methodology`). For primitives, one
entry per attribute name.

If the count exceeds 4 (AskUserQuestion's option limit), chunk into
groups and let the user toggle a whole group off, then ask a
follow-up for any individual removals:

> **Plain English:** Which categories of enrichment attributes? All on
> by default — toggle off anything irrelevant.
> **Recommend:** Keep them all unless you have a specific reason.
>
> Multi-select, all pre-checked:
> - [x] Demographics (age, gender, race, income, education) — 8 attrs
> - [x] Geography (postal_code, state, country, lat/long) — 7 attrs
> - [x] Person identifiers (full_name, given_name, family_name) — 4 attrs
> - [x] IAB interest categories (age range, marital, family, pets, …) — 9 attrs

Then optional drill-down per group if the user wants finer control.

Bind `SELECTED_ATTRIBUTES` = list of `{ name, sql_leaf_path }` entries.
Build `ATTRIBUTE_STRUCTS` and `ATTRIBUTE_NAMES_LIST` (Appendix A).

---

### Phase 6. Render and confirm

Compute the run identifiers:

- `RUN_SLUG_KEBAB` = `<supplier>-match-report-<YYYYMMDD-HHMMSS>`
- `RUN_SLUG_LOWER` = `<supplier>_match_report_<YYYYMMDD_HHMMSS>`
- `RUN_SLUG_UPPER` = `<SUPPLIER>_MATCH_REPORT_<YYYYMMDD_HHMMSS>`

Where `<supplier>` is the partner slug (e.g., `verisk`) and the
timestamp is UTC now. (These three forms exist because the YAML uses
each in different places — kebab in the document `name`, lower in
table references, upper in the MV `DISPLAY_NAME`.)

Read `assets/workflow.yaml.tmpl`, substitute all macros from Appendix A,
and present the result:

> **Plain English:** Ready to submit. Here's what we'll do:
> - **Your data:** `<CUSTOMER_DATASET_NAME>` (`<N>` id types: `<list>`)
> - **Partner:** `<Supplier human name>` — matching on `<SELECTED_ID_TYPES>`
> - **Enrichment:** `<ENRICHMENT_AR_TABLE>` joined on
>   `<ENRICHMENT_JOIN_PATH>` with `<M>` attributes
> - **Report display name:** `<REPORT_DISPLAY_NAME>`
> - **Final MV table name:** `<RUN_SLUG_UPPER>` (timestamped for uniqueness)
> - **Expected runtime:** 5–25 minutes
>
> Options:
> - **A)** Submit (recommended)
> - **B)** Show me the full YAML first
> - **C)** Cancel

If `--dry-run`, stop here, print the YAML, and exit.

**Custom match key.** Render steps 1 and 2 from
[`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md)
instead of the default bodies: step 1 is the customer explode — use the
**Mode A (`standalone-attribute`)** or **Mode B (`graph-edge-json`)**
step-1 body per the `ARRAY_FIELD_HANDLING` bound in Phase 2.5 — and step
2 becomes **two** MVs (`step_2a_supplier_nameaddr_slice` +
`step_2b_supplier_compound`), so point step 3's supplier `FROM` at the
2b table. Substitute the custom-key macros (`MATCH_KEY_EXPR`,
`MATCH_ID_TYPE`, `PERSON_ID_PATH`, `ARRAY_FIELD_HANDLING`) alongside the
usual ones (Appendix A). **The supplier side is always raw-then-block
— never `SELECT` the supplier AR's computed key attributes, and keep
the soundex+zip blocking in 2b regardless of partner size.** The block
is not an optimization: computed Rosetta attributes re-derive
`ADDRESS_HASHES` per row over the full table at query time, and the
external function 500s at scale (SC-61797). The confirmation
summary should name the key (e.g. "matching on soundex first name +
normalized address") and flag the explode fan-out cost. With multiple
channels in `MATCH_KEYS`, every channel's steps render on each side.

#### Pre-flight: validate each NQL block

The workflow runs 10–25 minutes — catching typos up front beats
waiting for the runner to fail.

Validate any NQL before executing it, submitting it in a workflow,
or displaying it to the user:

```
narrative_nql_validate(nql=<query>, data_plane_id=<plane>)
```

Pass `data_plane_id` matching the dataset's plane — without it, the
validator falls back to the company default plane and can report
spurious "Unknown Table" errors.

If validation fails:

1. Read the error message and pointer.
2. Fix using the cheat sheet at
   `plugins/narrative-common/skills/write-nql/references/NQL_VALIDATION_ERRORS.md`.
3. Re-validate. Repeat up to 3 times — but only if your skill
   *generates* the NQL. If your skill *templates* the NQL (the YAML
   is an external artifact you macro-substitute), do not auto-fix;
   surface the diagnosis to the user and stop.
4. After 3 failed attempts (generator) or any failed validation
   (templater), surface the latest error to the user **verbatim** —
   not paraphrased; the wording carries the locator info.

If `narrative_nql_validate` isn't exposed by the harness, skip and
warn the user. Do not substitute `narrative_nql_execute`; it allocates
compute.

---

### Phase 7. Submit the workflow

Call `narrative_workflows_create` with:

- `specification` = the substituted YAML
- `data_plane_id` = the customer dataset's data plane UUID
- `tags` = `["_nio_ci_match_report_workflow", "<RUN_SLUG_LOWER>"]`
- `trigger_immediately` = `true`

After `narrative_workflows_create` returns, capture both
`workflowId` and `runId` (the latter is present when the call was
made with `trigger_immediately=true`). Poll the run until terminal:

```
narrative_workflow_runs_list(workflow_id=workflowId)
```

Terminal states are `completed`, `failed`, and `terminated`; any other
status means it is still going.

A run itself cannot be waited on — only jobs can — so this is a
check-and-pause loop, not a wait.

Narrative async work is slow: it rarely finishes in under ~30s, the
**median is roughly 5 minutes**, and large or cold-pool work can run
for **hours**. So the question is not how fast to re-ask — it is
whether you can wait instead of re-asking.

**Have a job id and the `job_monitor` / `wait_for` tools? Wait.**

```
job_monitor(job_id: "<uuid>")                          → waitable.handle "wt_…"
wait_for(handles: ["wt_…"], timeout_seconds: 3600)     → status + result
```

You are paused until the job finishes, at no cost while you wait — no
turns, no model calls — and you get back what the job did. Up to 8
handles in one `wait_for`, so jobs you started together are waited for
once rather than one at a time. A **failed** job is a finished wait
carrying its failure messages, not an error. If a wait times out with
the task still running you may wait again; the work carries on either
way. Never loop `narrative_jobs_describe` to find out whether a job is
done.

**No handle to wait on? Then you have to check, and pause between
checks.** A workflow run has no handle — only jobs do — and neither
does work started through a third-party MCP server. In order of
preference: `sleep(duration_seconds: <n>)` if you have it (up to an
hour per call); otherwise a background watcher if your harness has one
(Claude Code's `Monitor` driving an `until` loop, armed to re-check on
an interval and emit once the state is terminal, so the session stays
free); and a foreground `bash` `sleep` only when neither exists — some
harnesses, Narrative agent runs among them, block it outright.

**Cadence when you are the one checking.** First check ~15–30s after
submitting, then about every 30s, backing off to ~60s once it has been
running for a few minutes. Tell the user once — "still running (this
can take minutes to hours); I'll report back when it finishes" — and
don't narrate every check.

**Your turns are finite.** Inside a Narrative agent run every check and
every sleep spends one of a bounded number of iterations (10 by
default), so hours of work cannot be waited out by checking. Wait on
jobs wherever a handle exists; where none does, sleep long, and if it
is still going after a few checks hand the ids back to the user instead
of spending the rest of the budget.

**Give-up rule — abandon a *stuck* operation, not a merely slow one.**
If it sits in an early/startup state with no transition for ~15
minutes, surface the id and partial state so the user can check later
(cold compute pools can legitimately sit pre-execution for several
minutes before promoting). Work that is actively executing is making
progress even across a long wall-clock time — keep waiting on it rather
than timing it out.

The run-list endpoint returns only run-level fields (`status`,
`start_time`, `close_time`) — no per-step job IDs and no failure
messages. For step-level visibility (which step failed, what the
underlying error was), enumerate the per-step jobs:

```
narrative_jobs_search(workflow_run_id=runId)
```

Each result carries a `job_id` plus the workflow step it ran for.
Pull the failing one's detail with
`narrative_jobs_describe(job_id=<...>)` to read the actual error
message. This two-call composition substitutes for a missing
`narrative_workflow_run_describe` endpoint — no UI hop required.

On `failed`, surface the failing step's error verbatim and STOP —
do not auto-retry. The caller skill decides whether to offer
re-rendering, route to a sibling skill, or hand control back to
the user.

---

### Phase 8. Read the final report sample and summarize

The workflow's last step (`step_6_sample_final`) already ran a
`CreateDatasetSample` against the final MV by the time the run hits
`completed`. Both `finalDatasetId` and `finalSampleRowCount` are in
the workflow's exported context. No out-of-band sample call is
needed — just read the sample directly:

```
narrative_datasets_describe(
  dataset_ids=[FINAL_DATASET_ID],
  include=["sample", "metadata"]
)
```

(If you ever need to re-sample later — e.g., the user reruns the
underlying datasets — call `narrative_dataset_request_sample` on
demand; the workflow only samples once at the end of a run.)

Pull these `ATTRIBUTE_TYPE` rows from the sample for the summary:

- `match_totals` → matched persons + IDs
- `customer_baseline` → total customer persons + IDs (denominator)
- `kpi_match_rate` → match rate (%)
- `match_attribute_coverage` → coverage per attribute (top 5)

Render:

> **DONE.** Match report `<RUN_SLUG_UPPER>` ready (dataset
> `<FINAL_DATASET_ID>`).
>
> - **Customer persons:** `<N>`
> - **Matched persons:** `<M>` (`<M/N>%`)
> - **Identifier types matched:** `<list with counts>`
> - **Top enrichment coverage:** `<top 5 attrs with %>`

#### Intermediate datasets — auto-expire + hidden from UI

For datasets that should be **temporary** — ad-hoc scratch
artifacts, intermediate steps in a workflow, or anything created on
the fly that shouldn't outlive its immediate purpose — set both:

- `EXPIRE = 'P1D'` (or another ISO-8601 duration). The platform
  garbage-collects the dataset that long after creation, removing
  both the storage and the Dataset entry automatically. `P1D` is a
  sensible default: enough time to debug, short enough not to
  clutter long-term storage. Use a longer duration only if the user
  is expected to inspect the dataset after creation.
- `TAGS = ( '_nio_materialized_view', '_nio_interactive', ... )` —
  the `_nio_interactive` tag is what the dataset store's default
  `datasets` getter filters out. The dataset becomes invisible in
  the customer's Datasets list and in source pickers (Audience
  Studio, Graph Studio, etc.). It still exists; it only surfaces
  in escape-hatch views that opt in via
  `allDatasetsIncludingInteractive`.

Common application: workflows whose intermediate steps materialize
data the user shouldn't see. Tag every intermediate MV with both
`EXPIRE` and `_nio_interactive`; tag the final, customer-facing
artifact with **neither** — that's the deliverable, it should be
persistent and visible.

If the user asks where a temporary dataset went, explain: it exists
for the EXPIRE window, it's hidden from the main UI by tag, and it
auto-deletes. Nothing to clean up by hand.

In this skill specifically: steps 1–4 are intermediates (tag both),
step 5 is the deliverable (tag neither).

---

## Completion status

- **DONE** — Workflow completed, sample fetched, summary shown.
- **DONE_WITH_CONCERNS** — Completed but some attribute had unexpectedly
  low coverage (e.g., <5%); flag it.
- **BLOCKED** — Overlap was 0, or a validation/run step failed.
- **NEEDS_CONTEXT** — User has no graph-edge-mapped dataset, or no
  partner ARs are shared with their plane.

---

## Common cases

### Default — identity + enrichment from the same partner

User has a CRM dataset mapped to `graph_edge`. A single partner ships
both an identity AR and a demographic AR. Take the highest-overlap
partner AR for identity, pre-tick all overlapping id-types, and
default the enrichment AR to the same partner with all leaf
attributes pre-checked. One submit, both runs of step 4 and step 5
on. Expected runtime 5–25 minutes.

### Identity-only run

User explicitly opts out of enrichment in Phase 5, or no partner
exposes a demographic AR. Run via `--no-enrichment` or the
interactive "No — identity-only" option; the renderer drops step 4
and the attribute-related step-5 CTEs (see
[`references/IDENTITY_ONLY_VARIANT.md`](references/IDENTITY_ONLY_VARIANT.md)).

### Narrow id-type subset

Partner overlaps on 3+ id-types but the user wants to scope the run
(e.g., email only). In Phase 4's narrowing sub-prompt, user unchecks
the unwanted types. Bind only the remaining types into
`SELECTED_ID_TYPES_QUOTED`. Match count drops; runtime unchanged.

### Compound name + address key

User wants reach beyond exact identifiers, or has only name+address on
one side. Pick the compound key (or both channels) in Phase 1.5. Phase
2.5 binds `ARRAY_FIELD_HANDLING` — the customer exposes
soundex+libpostal as standalone attrs (81+326) **or** packed in a
`graph_edge` target_id JSON (`--array-field-handling` overrides; both
equivalent). Steps 1 and 2 render from
[`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md)
— step 1 uses the Mode A / Mode B body; step 2 splits into 2a (slice) +
2b (soundex+zip-blocked `ADDRESS_HASHES` explode). Steps 3–5 and the
output schema are unchanged; the headline KPI is the person-level rate,
not the id-based one. Expect higher compute (per-side explode fan-out),
and matches only as precise as the key's components — soundex is lossy,
so surface the false-positive trade-off.

### Dry-run preview

User passes `--dry-run`. Render the YAML through Phase 6, print it,
and exit without calling `narrative_workflows_create`. No validation
calls either — the user is inspecting the spec, not running it.

### Cross-company run

The user belongs to multiple companies. Phase 1's `B)` branch
switches the working company via `narrative_context_set_company`
before any dataset lookup happens. All subsequent calls inherit the
new company context.

---

## Edge cases and gotchas

- **Zero-overlap partner.** Surface a blocker; do not submit an empty
  comparison. Offer to switch partners or route to `/generate-rosetta-stone-mappings`.
- **Missing column-stats histogram on `graph_edge.target_id_type`.**
  Phase 3's `/profile-dataset --allow-recalc` call recovers it
  (configure → recalculate → re-read) before returning the id-types;
  don't proceed without ground truth. If `/profile-dataset` is absent,
  run the recovery inline per
  [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md).
- **AskUserQuestion 4-option cap.** Bucket large enrichment attribute
  lists into 4 named groups; offer a follow-up drill-down per group.
- **Pre-flight NQL validation fails.** STOP. Surface the validator's
  error verbatim. Do not "fix" the templated NQL — the YAML is an
  external contract.
- **Workflow runner returns `failed`.** Surface the failing step's
  error verbatim and STOP. The mechanics (jobs_search → jobs_describe)
  are in the `monitor-workflow-run` snippet inlined at Phase 7.
- **`ENRICHMENT_JOIN_PATH` starts with `e.`.** Template prepends the
  alias; a leading `e.` produces `e.e._rosetta_stone...` and the join
  fails silently. Validate before binding.
- **Intermediate MVs.** Steps 1–4 carry `EXPIRE = 'P1D'` and the
  `_nio_interactive` tag — they auto-expire in 24h and are filtered
  out of the customer's main dataset list. No manual cleanup needed.
  See Phase 8.
- **`ADDRESS_HASHES` 500 at scale (SC-61797).** `ADDRESS_HASHES`
  is a remote external function that HTTP-500s when run over a large
  supplier slice, and the platform swallows the error (the run just
  shows `failed`). Two ways to trip it: exploding the raw supplier
  name|address slice without blocking, **or** selecting the supplier
  AR's computed `soundex_first_name` /
  `libpostal_normalized_address_array` attributes — those are not
  stored; the AR mapping re-derives `ADDRESS_HASHES(...)` per row over
  the entire underlying table before any predicate can prune it, so
  the failure fires in `standalone-attribute` shape too. Supplier side
  is always raw slice (2a) → block to the customer's distinct
  `(SOUNDEX(given_name), postal_code)` pairs → `ADDRESS_HASHES` on
  survivors only (2b). Mandatory at any non-trivial partner size, not
  a tuning knob. Only the bounded customer side may read the computed
  attribute directly.
- **Customer dataset is a `_nio_view`.** Step 5 must not read a view
  dataset directly inside an aggregate CTE — it 500s at run time.
  Derive the customer file-total from the **step-1 MV** instead (it is
  materialized and carries every row the run matched on).
- **`UNNEST` rejects `VARIANT`.** In `graph-edge-json` handling,
  `TRY_PARSE_JSON(target_id)['libpostal_normalized_address_array']` is a
  `VARIANT` — `CAST(... AS ARRAY<STRING>)` before `UNNEST` or you get
  HTTP 422.
- **Compound-key delimiter.** The `ID` composite joins its components
  with `::`, never `|` — libpostal hashes contain `|`. A `|` delimiter
  silently under-matches.

---

## Harness fallbacks

- **No `/profile-dataset`.** Run Phase 3's id-type histogram recovery
  inline (configure → recalculate → re-read). See
  [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md).
- **No `narrative_nql_validate`.** Skip Phase 6 pre-flight; do not
  substitute `narrative_nql_execute`. See
  [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md).
- **No `AskUserQuestion`.** If the harness does not expose `AskUserQuestion` as a named tool
(Claude Code does; most others don't), ask the user the same question
in plain prose — **one question per turn**, never batched — and wait
for a reply before continuing. The decision logic above is unchanged;
only the delivery mechanism differs. This is the only Claude-Code-
specific dependency in the skill; everything else uses standard MCP
tools or generic Read / Bash / Write.
  Multi-select prompts (id-type subsetting, enrichment attribute
  groups) keep their pre-ticked defaults — ask the user for the
  *numbers to uncheck* to keep prose short. Mandatory steps
  (pre-flight validation, schema-fidelity rule) do not change.

---

## Further reading

- [`assets/workflow.yaml.tmpl`](assets/workflow.yaml.tmpl) — the
  external workflow contract this skill submits.
- Appendix A in this file — the macro table to substitute into the
  workflow YAML.
- [`references/IDENTIFIER_ATTRIBUTES.md`](references/IDENTIFIER_ATTRIBUTES.md)
  — the `IDENTIFIER_ATTRIBUTE_IDS` lookup table used to partition AR
  mappings into identifiers vs enrichment.
- [`references/IDENTITY_ONLY_VARIANT.md`](references/IDENTITY_ONLY_VARIANT.md)
  — exact diff to apply when running identity-only (no enrichment AR).
- [`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md)
  — compound-key + array-component rules (type-based array detection,
  `::` delimiter), step-1/2 explode bodies (both `--array-field-handling`
  modes), the `ADDRESS_HASHES` soundex+zip blocking (SC-61797), and KPI
  reinterpretation for custom-key channels.
- [`references/HARNESS_FALLBACK.md`](references/HARNESS_FALLBACK.md)
  — prose-mode fallbacks for `narrative_nql_validate` and
  `AskUserQuestion` (both Claude-Code-specific).
- Sibling skills: `/create-workflow` (for more information on
  creating workflows in general), `/generate-identity-graph` (build
  the graph), `/generate-rosetta-stone-mappings` (author a Rosetta
  Stone mapping), `/profile-dataset` (Phase 3 delegates the id-type
  histogram read here).

---

## Appendix A: Macros in `assets/workflow.yaml.tmpl`

| Macro | Example | Notes |
|---|---|---|
| `<RUN_SLUG_KEBAB>` | `verisk-match-report-20260520-100831` | Document `name` |
| `<RUN_SLUG_LOWER>` | `verisk_match_report_20260520_100831` | Table refs in `FROM company_data.<...>` |
| `<RUN_SLUG_UPPER>` | `VERISK_MATCH_REPORT_20260520_100831` | Final MV table name (must be globally unique → keeps the timestamp) |
| `<REPORT_DISPLAY_NAME>` | `Verisk Match Report — Hartford Funds Customers` | Human-readable UI label on the final dataset. Short; no timestamp (it's in metadata). |
| `<REPORT_DESCRIPTION>` | `Compares Hartford_Funds_Customers against Verisk. Identity match on normalized_email, e164_phone_number; 25 enrichment attributes attached.` | One line. Don't restate timestamps or list every attribute — those are already structural. |
| `<CUSTOMER_DATASET_NAME>` | `Hartford_Funds_Customers` | Bare table name; used as `FROM company_data.<name>` |
| `<SUPPLIER_AR_TABLE>` | `verisk.verisk_identity_basis_share` | Qualified `slug.name` |
| `<ENRICHMENT_AR_TABLE>` | `verisk.verisk_tcibe_0016718_basis_share` | Qualified `slug.name` |
| `<ENRICHMENT_JOIN_PATH>` | `_rosetta_stone.person_id['value']` | **No `e.` prefix** — template prepends it |
| `<SELECTED_ID_TYPES_QUOTED>` | `'normalized_email', 'e164_phone_number'` | Comma-separated quoted strings for the `IN (...)` clause |
| `<ATTRIBUTE_STRUCTS>` | (multi-line block, see below) | Comma-separated `NAMED_STRUCT(...)` entries |

**Custom-match-key macros** (used by
[`references/CUSTOM_MATCH_KEY_VARIANT.md`](references/CUSTOM_MATCH_KEY_VARIANT.md);
ignored when matching on `identifiers` only):

| Macro | Example | Notes |
|---|---|---|
| `<ARRAY_FIELD_HANDLING>` | `standalone-attribute` | Which customer step-1 body to render: `standalone-attribute` (components as their own attrs, UNNEST native arrays) or `graph-edge-json` (`TRY_PARSE_JSON(target_id)` + `CAST(... AS ARRAY<STRING>)` + UNNEST). Bound in Phase 2.5 from `--array-field-handling` or auto-detect. Outputs are equivalent. **Customer side only** — supplier extraction is always raw-then-block (SC-61797). |
| `<MATCH_KEY_EXPR>` | `CONCAT(soundex_first_name, '::', addr_hash)` | The compound `ID` expression. Delimiter is `::`, never `\|`. Both sides must use the identical expression. |
| `<MATCH_ID_TYPE>` | `soundex_first_name\|libpostal_normalized_address_array` | The fixed `ID_TYPE` label for a custom-key channel (`a\|b` type-label convention — the `\|` here is the type name, not the value delimiter). |
| `<PERSON_ID_PATH>` | `_rosetta_stone.graph_edge['source_id']` | Person anchor on each side, independent of the match key. On a raw name\|address supplier slice it is the bare `person_id` column. |

**Building `<REPORT_DISPLAY_NAME>`.** Pattern:
`<Supplier human name> Match Report — <Customer display name>`. Keep
it under ~70 chars. Don't append the timestamp — `created_at` already
disambiguates reruns in the dataset list.

**Building `<REPORT_DESCRIPTION>`.** One line, two clauses:

1. `Compares <CUSTOMER_DATASET_NAME> against <Supplier human name>.`
2. With enrichment: `Identity match on <selected id types, comma-joined>; <N> enrichment attributes attached.`
   Identity-only: `Identity-only match on <selected id types, comma-joined>.`

Do not enumerate every attribute name — they're already discoverable
in the `BUCKETS` column and in the step-4 MV's schema.

**Building `<ATTRIBUTE_STRUCTS>`.** For each selected attribute, emit
one line:

- Primitive (`age`):
  ```
  NAMED_STRUCT('attribute', 'age', 'val', CAST(e._rosetta_stone.age AS STRING))
  ```
- Object property (`hl7_gender.gender`):
  ```
  NAMED_STRUCT('attribute', 'hl7_gender.gender', 'val', CAST(e._rosetta_stone.hl7_gender['gender'] AS STRING))
  ```

Join with `,\n              ` (comma, newline, 14 spaces) to match the
indentation in the template's `ARRAY(...)` block.

---

## Appendix B: Partitioning AR mappings

To pick the identity AR (Phase 4) and the enrichment AR (Phase 5),
partition any access rule's mappings into identifiers, demographics,
and the `graph_edge` container.

```python
for m in ar.mappings:
    if m.attribute_name.startswith("_nio_"):
        continue                                  # internal — skip
    elif m.attribute_id == 362:
        graphEdge = m                             # structural
    elif m.attribute_id in IDENTIFIER_ATTRIBUTE_IDS:
        identifiers.append(m)                     # join-able (fast path)
    else:
        # Fallback: unknown id, describe + keyword-classify
        attr = narrative_attributes_describe(attribute_ids=[m.attribute_id])
        if matches_identifier_keywords(attr.name):
            identifiers.append(m)
            note_unknown(m, "identifier")
        else:
            demographics.append(m)
            note_unknown(m, "enrichment")
```

The curated `IDENTIFIER_ATTRIBUTE_IDS` set, the keyword heuristic for
the fallback branch, and the user-facing note format all live in
[`references/IDENTIFIER_ATTRIBUTES.md`](references/IDENTIFIER_ATTRIBUTES.md).
Load it on demand — the curated set changes rarely; the fallback
keeps the skill correct for new identifier-typed attributes between
updates.
