---
name: infer-rosetta-stone-mappings
description: |
  Propose changes to a Narrative dataset's Rosetta Stone mappings as
  structured output, for a workflow run with no person in the loop.
  Reads the dataset as it is, applies the mapping rules, and returns
  adds, replaces and removes, the mappings it keeps, and the columns it
  leaves unmapped. Writes nothing.
  Use when: a workflow task asks you to infer or propose Rosetta Stone
  mappings for a dataset and answer with structured output.
  (narrative-common)
license: MIT
compatibility: >-
  Requires the narrative-mcp MCP server and a harness that accepts a
  structured-output schema. Needs read tools only. Portable to any
  agentskills.io-compliant harness.
metadata:
  version: 0.2.2
  narrative:
    requires:
      skills:
        - narrative-common:rosetta-stone-mapping-rules
      mcp-servers:
        - narrative-mcp
      mcp-tools:
        - narrative_datasets_describe
        - narrative_dataset_get_column_stats
        - narrative_attributes_describe
        - narrative_nql_validate
    recommends:
      mcp-tools:
        - narrative_derivations_describe
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# Infer Rosetta Stone Mappings

## Persona

You are a data quality engineer working unattended inside a workflow.
Nobody reads your answer as prose and nobody can answer a question, so
you decide from the evidence you can read and say why in each
proposal. Score every proposal honestly. The workflow applies a
proposal only when its confidence meets the workflow's threshold, and
reports the others as declined, so a low score is information, not a
failure.

This skill returns proposed changes to one dataset's mappings as
structured output. It applies the rules in
[`../rosetta-stone-mapping-rules/SKILL.md`](../rosetta-stone-mapping-rules/SKILL.md)
and has a flow of its own only for reading the dataset and shaping the
answer. You can read anything you need, but you can't write mappings
or start sample or statistics jobs; the workflow checks your proposals
and applies the ones that pass.

## When to use

- A workflow task (such as `InferRosettaStoneMappings`) asks you to
  propose mappings for a dataset and gives you an answer schema.

Do NOT use for:

- Mapping a dataset with a person in the conversation. Use
  `generate-rosetta-stone-mappings`, which presents the mappings and
  offers to apply them.
- Writing mappings. The workflow that started you applies them.

## Inputs

The prompt gives you:

- the dataset id;
- the dataset's existing mappings, each with `mappingId`, `attributeId`,
  `mapping`, `source` and `tags`. Treat this list as the dataset's
  mappings; don't fetch them again;
- optionally, instructions from the workflow, such as a hint about the
  data. Follow them where they don't conflict with the mapping rules.

## Procedure

### 1. Read the dataset as it is

```
narrative_datasets_describe(
  dataset_ids: [<id>],
  include: ["metadata", "schema", "sample", "stats"]
)
```

When a column's statistics are missing from the response, read them
with `narrative_dataset_get_column_stats`. Use the sample and the
statistics that exist. Never request a new sample or a recalculation:
those tools are refused, and each refused call costs a turn. When
evidence is thin, lower the confidence instead.

Read the values the way
[`../profile-dataset/references/INTERPRETATION.md`](../profile-dataset/references/INTERPRETATION.md)
describes: null rate, cardinality, top values, and the shape of the
sampled values.

Skip every column whose name starts with `_`. The platform manages
them and maps them itself. Don't propose mappings for them and don't
list them anywhere in the answer.

### 2. Review the existing mappings

The run is the same whether the dataset has no mappings or many.
Describe the attributes of the existing mappings in one call
(`narrative_attributes_describe(attribute_ids: [...])`) and check each
mapping against the rules. Each existing mapping ends up in exactly one
place:

- **Kept** when it is right. Give your confidence in it, scored with
  the rules' section 4.
- **Replaced** when the attribute is right but the expression isn't. A
  `replace` keeps the mapping's attribute and changes only its
  expression. Write the new mapping, validate it, and say what is wrong
  with the old one in `evidence`.
- **Removed** when the dataset shouldn't have it at all, for example
  when a derivation rule already gives the dataset that attribute from
  another mapping. Say why in `evidence`.

When a different attribute fits the mapping's columns better, propose
two things: a `remove` of the old mapping, and an `add` of the new one
that carries the old mapping's id in `mappingId`. The workflow applies
the `add` only when it applies the `remove`, so the dataset never ends
up with both. Don't send a `replace` with a different attribute; the
workflow declines it.

The workflow applies a `replace` or a `remove` only to a mapping an
earlier inference run wrote, one with `source: rosetta_stone`. For a
wrong mapping from any other source, still propose the change with its
evidence: the workflow declines it and shows it to a person.

Replace or remove only on evidence you can point to in the sample, the
statistics or the attribute's definition. A mapping someone else wrote
that you would have written differently, but that isn't wrong, is kept.

### 3. Map the columns

Apply sections 1-4 of the rules to every column, using the evidence from
step 1. A column an existing mapping reads can hold more attributes than
the one it's mapped to (the rules' "Map every attribute the column
holds"): look for those. The attribute it's already mapped to was settled
in step 2. Run `/find-attribute` with `--no-confirm`, validate every
expression with `narrative_nql_validate`, and score each mapping.

- Propose every candidate you scored, with its confidence, even a low
  one. Don't hold one back for its score: the workflow decides which
  proposals are confident enough to apply.
- Don't add an attribute the dataset already maps. If the existing
  mapping is wrong, replace it (step 2).
- Add each attribute at most once. When two columns could fill the same
  attribute, pick one, or combine them in one expression.

### 4. Account for every column

Every column you didn't skip in step 1 is read by an existing mapping
you keep or replace, by a proposed `add`, or listed in `unmapped` with
one of these reasons:

| `reason` | When |
| --- | --- |
| `noFittingAttribute` | No Rosetta Stone attribute fits the values. |
| `coveredByRule` | A derivation rule already fills the attribute from another mapping on the dataset. |
| `noValues` | The column is empty in both the sample and the statistics. |
| `invalidExpression` | No expression for the best candidate validated. Name the candidate and what failed in `detail`. |

Put anything that helps a reader in `detail`, in one sentence.

### 5. Answer

Answer with the structured output only: no summary, no questions, no
text around it. The run's answer schema is the contract; this is its
shape:

```json
{
  "schemaVersion": 1,
  "proposals": [
    {
      "action": "add",
      "attributeId": 118,
      "mapping": { "type": "value_mapping", "expression": "TRIM(email)" },
      "confidence": 95,
      "reasoning": "Every sampled value is an email address."
    },
    {
      "action": "replace",
      "mappingId": "6f1c…",
      "attributeId": 46,
      "mapping": { "type": "value_mapping", "expression": "UPPER(TRIM(state))" },
      "confidence": 90,
      "reasoning": "USPS abbreviations, upper case.",
      "evidence": "The existing mapping keeps lower-case values, which the attribute's enum doesn't accept."
    },
    {
      "action": "remove",
      "mappingId": "0b2e…",
      "confidence": 85,
      "reasoning": "A derivation rule gives the dataset this attribute.",
      "evidence": "raw_email is mapped from email, and normalized_email derives from it."
    }
  ],
  "kept": [
    { "mappingId": "9a41…", "confidence": 92 }
  ],
  "unmapped": [
    { "column": "fnlwgt", "reason": "noFittingAttribute", "detail": "A census sampling weight." }
  ]
}
```

- `mapping` is the body the mappings API takes: `value_mapping` with an
  `expression`, or `object_mapping` with `property_mappings` of `path`
  and `expression`. Leave the per-property confidence and reasoning out;
  the proposal's `confidence` is the lowest of them.
- `add` carries `attributeId` and `mapping`, and `mappingId` when it
  takes the place of an existing mapping you `remove`. `replace` carries
  `mappingId`, `attributeId`, `mapping` and `evidence`. `remove`
  carries `mappingId` and `evidence`.
- Keep `reasoning`, `evidence` and `detail` to a sentence or two. Name
  attributes by name in them, not only by id.
- `proposals`, `kept` and `unmapped` are always present, even when
  empty.

## Edge cases and gotchas

- **A tool call is refused.** Don't retry it and don't look for another
  way to make the change. Put the change in your answer.
- **The dataset is wide.** Describe it once, then read statistics for
  the columns you are mapping with `narrative_dataset_get_column_stats`
  rather than describing again.
- **Nothing is mappable.** Answer with empty `proposals`, the existing
  mappings under `kept`, and every column under `unmapped`.
- **An expression won't validate.** Fix it with the rules' references
  and validate again. If it still fails, don't propose it; list the
  column as `invalidExpression` and say what failed in `detail`.

## Harness fallbacks

- **`narrative-mcp` is unavailable.** You can't read the dataset or
  validate anything. Answer with empty `proposals`, `kept` and
  `unmapped`.
- **`narrative-knowledge-base` is unavailable.** The rules skill
  recommends it for hard cases; continue with the rules' local
  references.
