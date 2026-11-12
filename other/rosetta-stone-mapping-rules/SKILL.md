---
name: rosetta-stone-mapping-rules
description: |
  The rules for mapping a Narrative dataset's columns to Rosetta Stone
  attributes: choosing the attribute, mapping the source of a derivation,
  value_mapping vs object_mapping, discriminators, validating each
  expression with NQL, and scoring confidence. No flow of its own; the
  skills that generate or infer mappings read it.
  Use when: another skill tells you to apply the mapping rules, "which
  Rosetta Stone attribute should this column map to", "is this mapping
  expression right".
  (narrative-common)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server. Recommends the
  narrative-knowledge-base MCP server. Portable to any
  agentskills.io-compliant harness.
metadata:
  version: 0.1.0
  narrative:
    requires:
      skills:
        - narrative-common:find-attribute
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_attributes_describe
        - narrative_nql_validate
    recommends:
      mcp-servers:
        - narrative-knowledge-base
      mcp-tools:
        - narrative_derivations_describe
        - search_narrative_i_o_knowledge_base
        - query_docs_filesystem_narrative_i_o_knowledge_base
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Rosetta Stone Mapping Rules

## Persona

You are a data quality engineer who treats Rosetta Stone mappings as
a contract between a source dataset and the normalized identity
graph. You never hallucinate a Rosetta Stone attribute id, never
propose a mapping from a column name in isolation, and never emit an
expression that has not passed `narrative_nql_validate`.

## How to use this skill

These are the rules for turning a dataset's columns into mappings. The
skill that sent you here owns the flow: how it reads the dataset, and
how it presents or returns the mappings. Apply sections 1-4 to each
column cluster, using the schema, sample rows and column stats that
skill gathered.

When the platform-data tools aren't enough — e.g., you need official
guidance on Rosetta Stone confidence scoring, the normalization model,
or an NQL function/operator reference — consult the
`narrative-knowledge-base` MCP server. See
[`references/KB_RESEARCH.md`](references/KB_RESEARCH.md) for the
recommended query patterns.

## 1. Find candidate Rosetta Stone attributes

Identify the column clusters that should resolve to attributes
(individual columns for primitive mappings, groups like
`{type, value}` or `{first_name, last_name}` for object mappings —
see section 2).

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

The `schema` field is the contract you need for section 2 — it includes
type (primitive vs object), property paths (for object attributes —
e.g., `type`, `value`, `context.source`), enum constraints
(non-null `enum` array), and required vs optional flags. This is
the **only** way to learn that detail; do NOT guess attribute IDs
from memory or reason from search snippets.

When `confidence: low` or when `alternatives` cluster within 1-2
ranking points, treat all close candidates as in-play for that
cluster and let sections 2 and 3 discriminate.

When you already know the target attribute ID (it was named
explicitly, or you are checking an existing mapping), skip `/find-attribute`
and call `narrative_attributes_describe(attribute_ids: [<id>, ...])`
directly — describing a known ID does not need the search +
ranking machinery.

### Map every attribute the column holds

A column can hold several attributes. Each attribute is queried on its
own, and a dataset that isn't mapped to one doesn't answer queries for
it unless a derivation rule fills it in. So map every attribute whose
description and enum the values meet, on the rows where they meet it.
Some of the shapes this takes:

- **Parts of one value.** A `geo_location` of `US>TX>623` holds a
  country, a state and a DMA: map `iso_3166_1_country`,
  `usps_state_abbreviation` and `designated_market_area`.
- **The same value, two attributes.** A `sex` column of `M`/`F` fits
  both `hl7_gender` and `iab_gender`, and no rule derives one from the
  other: map both.
- **The same value on a subset of rows.** `state` ("a state or region
  within a country") takes the second part from every row (`TX`, `ON`,
  `H9`). `usps_state_abbreviation` takes it from the `US` rows only, and
  no rule derives one from the other, so map both:

```sql
CASE WHEN geo_location LIKE 'US>%'
  THEN SUBSTRING_INDEX(SUBSTRING_INDEX(geo_location, '>', 2), '>', -1) END
```

Leaving out the rows that don't hold an attribute isn't filtering (see
"Transform values; don't filter them"). A value on a `US` row that the
enum doesn't list, such as `AE`, stays.

Each mapping has to be right on its own: an attribute the values only
loosely match is a wrong mapping, not an extra one. And when a
derivation rule reaches an attribute from another mapping, the rule
covers it (next section).

### Map the source of a derivation, not what it derives

Derivation rules compute one attribute from another, up to three rules
deep. A dataset mapped to `raw_email` also answers queries for
`normalized_email` and the email hashes, so mapping the same column to
those as well adds nothing. It also does harm. A stored mapping
replaces the rule for its attribute on that dataset, and the
attributes further down are then derived from the stored mapping
instead. An inferred `normalized_email` that cleans addresses up
differently from the rule changes every hash derived after it.

Once every cluster has its candidates, describe them all in one call:

```
narrative_attributes_describe(attribute_ids: [<id>, ...])
```

The default `include` returns each attribute's `derivations` lines:
`derives X` means a rule computes X from this attribute, possibly
through others, and `derived from Y` means this attribute is computed
from Y. Then, for each column:

- **Map it to the attribute closest to the root that the column
  holds.** An `email` column of plain addresses maps to `raw_email`
  only. That is usually the raw, free-form attribute: you read the
  column into it, and the rules derive the normalized and structured
  attributes from it. Choose the mappings that let the rules give the
  dataset the most attributes.
- **Map the specific attribute, and let a rule give the general one.**
  `sha256_hashed_email` derives `hashed_email` with `type`
  `sha256_email`, so a column of SHA-256 hashes maps to
  `sha256_hashed_email`, not to `hashed_email`. The specific attribute
  says what the value is; the general one needs a `type` to say it, and
  no rule runs back from it. If two attributes ever derive each other,
  map the more specific one for the same reason.
- **A column can hold different specific attributes on different
  rows.** A `device_id` column next to a `platform` column holds IDFAs
  on `ios` rows and Android advertising ids on `android` rows. When
  `apple_idfa` and `android_advertising_id` each derive
  `mobile_id_unique_identifier`, map the column twice, each on its
  rows, and let the rules give the general id:

```sql
-- apple_idfa.value
CASE WHEN LOWER(platform) = 'ios' THEN TRIM(device_id) END
-- android_advertising_id.value
CASE WHEN LOWER(platform) = 'android' THEN LOWER(TRIM(device_id)) END
```

  Without those rules, map `mobile_id_unique_identifier` once, with its
  `type` taken from `platform`.
- **Drop a candidate that another candidate on the same columns
  derives.** If `email` has the candidates `raw_email` and
  `normalized_email`, keep `raw_email`. The dataset's existing
  mappings count too: when `email` already maps to `raw_email`, don't
  propose `normalized_email` for it.
- **Leave a derived column unmapped when the dataset maps its
  source.** A stored mapping replaces the rule on every row of the
  dataset, not only where the stored value exists. Next to an `email`
  column mapped to `raw_email`, an `email_sha256` column of stored
  hashes stays unmapped: mapping it would drop the hashes the rule
  computes from `email`. Don't fold the rule into the mapping either,
  as in `COALESCE(email_sha256, SHA2(NORMALIZE_EMAIL(email), 256))`;
  that copies a formula the rule owns.
- **Map a derived attribute directly only when the dataset has nothing
  it derives from.** A dataset of stored hashes and no plain addresses
  maps its hash column to `sha256_hashed_email`.
- **When a rule fits the data poorly, say so instead of adding a
  mapping.** The `telephone_number` → `e164_phone_number` rule only
  handles numbers that start with `+`. Put that in the `telephone_number`
  mapping's `warnings`; don't add an `e164_phone_number` mapping from
  the same column.

To read what a rule computes, call
`narrative_derivations_describe(derivation_ids: [<id>])` with the
derivation id from the line.

## 2. Decide value_mapping vs object_mapping

| Source shape | Target attribute | Use |
| --- | --- | --- |
| Single column → primitive attribute (email, phone, age, country) | Primitive | `value_mapping` |
| Single column → object attribute where only `value` matters | Object with type/value | `object_mapping` with `value`, and a `type` set where `value` is |
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
      { "path": "type",  "expression": "CASE WHEN hashed_email IS NOT NULL THEN 'sha256_email' END", "confidence": 100, "reasoning": "Discriminator, set only where there is a hash; all sampled hashes are 64 chars." },
      { "path": "value", "expression": "LOWER(hashed_email)", "confidence": 92, "reasoning": "Lowercase normalization for SHA256." }
    ]
  },
  "warnings": []
}
```

### Set a discriminator only where there is a value

A property that says what the value is (`type`, `ad_platform`, a
`context` naming the source) belongs to the value. On a row with no
value it would describe nothing, and the row would still read as a
data point of that kind. So give it the same condition as the value:
NULL wherever the value is NULL. Some examples:

- **A blank id.** `person_id` from `member_id`:

```
value: NULLIF(TRIM(member_id), '')
type:  CASE WHEN NULLIF(TRIM(member_id), '') IS NOT NULL THEN 'person_id' END
```

- **A value on some rows only.** `apple_idfa` from a mixed `device_id`
  column takes the same `platform` condition in both properties:

```
value: CASE WHEN LOWER(platform) = 'ios' THEN TRIM(device_id) END
type:  CASE WHEN LOWER(platform) = 'ios' THEN 'idfa' END
```

- **A constant that isn't called `type`.** A Facebook ad report's
  `campaign` mapping sets `ad_platform` only where `campaign_id` is:
  `CASE WHEN campaign_id IS NOT NULL THEN 'facebook' END`.

### Don't repeat the attribute's validations

The platform applies an attribute's `validations` every time it reads a mapped
value: a value that fails any of them becomes NULL, and a query that requires
the property filters on them. `$this` in a validation is the mapped value.

Read them from the `schema` section of
`narrative_attributes_describe(attribute_ids: [<id>, ...])`:

- **Scalar attribute:** a `- validations:` line. `age` has
  `- validations: $this >= 0`.
- **Object attribute:** a `"validations"` array on the property, inside the
  `properties` JSON. `md5_hashed_email` has
  `"validations": ["$this.\"value\" RLIKE '^[a-f0-9]{32}$'"]` on `value`.
- **Property that references another attribute:** describe returns it with
  that attribute's type filled in, its validations included. Read them there;
  no extra call is needed.

Then:

- **Don't copy a validation into the expression.** `LOWER(email_md5)` is
  enough; `CASE WHEN LOWER(email_md5) RLIKE '^[a-f0-9]{32}$' THEN
  LOWER(email_md5) END` gives the same values and only makes the mapping
  longer. The same goes for a blank check: `raw_email` has
  `"validations": ["TRIM($this.\"value\") <> ''"]` on `value`, so
  `TRIM(email)` is enough, and `NULLIF(TRIM(email), '')` repeats it.
- **Do transform values so they pass.** A validation only rejects; it doesn't
  fix. Lower-case a hex hash or a device id the validation expects in lower
  case, or every upper-case value turns into NULL.
- **A check that chooses between source columns isn't a repeat.**
  `CASE WHEN <col_a is valid> THEN col_a WHEN <col_b is valid> THEN col_b END`
  picks a different column on some rows without it. Keep it.
- **Only some properties have validations.** Read them before relying on
  them. A property without one keeps whatever value the expression gives it.

### Transform values; don't filter them

An expression says how to read the column as the attribute: trim, change
case, parse, pad, convert units, extract a part, translate the dataset's
codes into the attribute's enum. It doesn't drop values because they look
invalid or look like placeholders. Deciding what to reject is the
attribute's job.

- **No validity checks.** Don't wrap the value in a format check such as
  `CASE WHEN TRIM(email) RLIKE '^[^@ ]+@[^@ ]+[.][^@ ]{2,}$' THEN TRIM(email) END`.
  It runs on every row, and it withdraws raw data the attribute may
  accept. If the attribute has no validation for clearly broken values, map
  them anyway and name the missing validation in `warnings`.
- **Keep values that look like placeholders.** `0000000000`, an all-zero
  device id, the hash of `''`, `-` or `?` stay as they are, unless the
  attribute's description or validations state a convention for them.
  Mention them in `warnings` when they are common.
- **Trim with `TRIM`, and keep other whitespace.** `TRIM(col)` removes
  surrounding spaces. A tab or other whitespace around a value is raw data;
  don't strip it with a regex.
- **A blank string isn't a value.** Turn it into NULL with
  `NULLIF(TRIM(col), '')`, unless the attribute already has a validation
  that rejects a blank (see "Don't repeat the attribute's validations").
- **No backslash escapes in string literals.** `'\s'`, `'\d'` and `'\w'`
  reach Spark as the bare letters `s`, `d` and `w`, so
  `REGEXP_REPLACE(email, '^\s+|\s+$', '')` strips the letter `s` from
  `susan@example.com`, and validation doesn't catch it. Write a character
  class instead: `[0-9]` for a digit, `[ ]` for a space. See
  [`references/EXPRESSION_SYNTAX.md`](references/EXPRESSION_SYNTAX.md).

## 3. Validate every expression with NQL

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

## 4. Score confidence

| Range | Use when |
| --- | --- |
| 95-100 | Clear semantic match (column name + all-sample-pattern matches), well-known standard (email, ISO timestamp, US state code, SHA256 hash). |
| 85-94 | Strong pattern with minor ambiguity (e.g., `id` column that is *probably* a user identifier given the sample). |
| 70-84 | Reasonable inference; column name ambiguous but sample data leans this way. |
| Below 70 | Multiple valid interpretations or sparse evidence. Include the suggestion but flag for user verification. |

For object_mappings, the mapping's confidence is the **minimum** of its
property confidences. A high-confidence `type` literal cannot rescue a
low-confidence `value` expression.


## References

- [`references/EDGE_CASES.md`](references/EDGE_CASES.md) — reserved-identifier quoting, enum case sensitivity, null handling, object-mapping replace-all semantics, custom-attribute fallback, confidence-vs-validity, token economy, underscore-prefixed columns. Read when an expression won't validate or a mapping feels off.
- [`references/EXPRESSION_SYNTAX.md`](references/EXPRESSION_SYNTAX.md) — SQL/NQL quoting, function, and CASE WHEN rules. Read when an expression fails `narrative_nql_validate` or when mapping a reserved-word column.
- [`references/ENUM_HANDLING.md`](references/ENUM_HANDLING.md) — generation-vs-evaluation rules for enum-constrained attributes. Read when `narrative_attributes_describe` shows `{value1|value2|...}` constraints.
- [`references/KB_RESEARCH.md`](references/KB_RESEARCH.md) — how to query `narrative-knowledge-base` for Rosetta Stone best practices and NQL references when local files aren't enough.
- `../find-attribute/SKILL.md` — section 1 defers to this skill per cluster, `--no-confirm`, structured results.

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

- `skill_name`: `narrative-common:rosetta-stone-mapping-rules` (use this verbatim).
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
