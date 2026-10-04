---
name: faithfulness-review
description: "Check every generated profile rule against the source for being stronger than its evidence (over-claim), and write a faithfulness report. v0 compares rules vs raw source text; v1 vs evidence records."
---

## Purpose

Catch the main LLM failure mode in distillation: a generated rule that is **stronger, broader,
or more certain than the source supports**. Produce `reports/faithfulness-report.yaml`
validated by `validate_faithfulness_report.py`.

## Input

- `profile.yaml` — the rules to check: `quality_bar[]`, `forbidden_behaviours[]`,
  `outputs.modes[].trigger`, and any imperative rule text.
- `sources/markdown/<id>.md` — the source text (load via `source_text.load_source_texts`).
- `sources/anchors/<id>.anchors.jsonl` — real anchor IDs for `source_anchors`.
- (v1, after Step 3) `evidence/evidence-records.yaml` — compare rules against evidence records
  instead of raw text for sharper claim-strength findings.

## Procedure

For each profile rule:

1. Locate the supporting passage(s) in the source (section/page granularity is acceptable;
   record real anchor IDs and `support_granularity`).
2. Compare the rule's **claim strength** to the source on the five-level ordering:
   - `EXACT_SUPPORT` — rule matches the source.
   - `WITHIN_SCOPE` — valid inference from the source.
   - `SCOPE_BROADENED` — more general/universal than the source warrants (WiCE Partially-Supported).
   - `HEDGING_REMOVED` — source hedges (`may`, `often`, `in this context`); rule asserts absolutely (Janus Framing).
   - `CONTRADICTED` — rule opposes the source.
   Also tag `distortion`: `scope_broadened` / `hedge_removed` / `specificity_inflated` (Janus
   Specificity = numeric-precision inflation) / `none`.
3. Choose an `action`: `downgrade` (weaken to match), `remove`, `add_condition`, or
   `accept_with_note`. **A `CONTRADICTED` finding may never be `accept_with_note`.**
   **Source-of-truth precedence exception:** before flagging a rule for `downgrade`/`remove`,
   check the profile's `source_of_truth_policy.precedence`. When a rule diverges from the
   *ingested* source but matches a source the precedence policy names as canonical (e.g. an
   official docs site that supersedes a summary/cheat-sheet for version-specific facts), the
   rule is **correct** and the ingested source is the one in error. Record the divergence
   verdict honestly, but set `action: accept_with_note` with a note citing the precedence rule —
   do not downgrade a rule to match a source the package itself treats as non-authoritative.
4. Compare at **sentence/claim granularity**, never document-level. Check against **exact
   source spans** (anchors), not a vague recollection. Do **not** use model confidence as a
   faithfulness signal.

## Output

Write `reports/faithfulness-report.yaml` per `schemas/faithfulness-report-v1.schema.json`:
fields `rule_ref`, optional `triplet`, `verdict`, `distortion`, `source_anchors`,
`support_granularity`, `severity`, `action`, `note`.

### Schema constraints (the file is `additionalProperties: false` — get these exact)

The validator (`validate_faithfulness_report.py`) is strict, so unknown keys and
out-of-enum values **fail the gate**, not warn. Two mistakes are common on a first pass:

- **No top-level keys beyond `schema_version`, `subagent_slug`, `findings`.** Do not add a
  roll-up `summary:` block (counts/worst-verdict) — it is rejected as an unexpected property.
  Put any narrative in a leading YAML comment instead.
- **`support_granularity` is `section` | `page` | `heading` only** — there is no `document`
  token. A finding grounded in a topic's absence across the whole source (a scope-boundary or
  evidence-gap rule) still anchors at `section`; this is deliberate (compare at section
  granularity, never document-level).

Per-finding closed enums:

| Field | Required | Allowed values |
|-------|----------|----------------|
| `rule_ref` | yes | a real field path in `profile.yaml` (e.g. `quality_bar[2]`, `outputs.modes[review].trigger`) |
| `verdict` | yes | `EXACT_SUPPORT` `WITHIN_SCOPE` `SCOPE_BROADENED` `HEDGING_REMOVED` `CONTRADICTED` |
| `action` | yes | `downgrade` `remove` `add_condition` `accept_with_note` |
| `distortion` | no | list of `scope_broadened` `hedge_removed` `specificity_inflated` `none` |
| `support_granularity` | no | `section` `page` `heading` |
| `severity` | no | `high` `medium` `low` |

## Caveat

Over-claim detection is original engineering composed from WiCE / Janus / RefChecker — there is
no validated off-the-shelf model. Be conservative: when unsure whether a rule exceeds its
evidence, flag `SCOPE_BROADENED`/`HEDGING_REMOVED` for review rather than passing it.
