---
name: schema-guard
description: Check a proposed API or data contract against the current contract, real sample payloads, and a compatibility policy, and gate publication behind a refusable verdict with native digest evidence.
---

# Schema Guard

Schema Guard decides whether a proposed contract change can move forward
without silently breaking callers. It compares the current and proposed JSON
Schema contracts field by field, validates every supplied sample payload
against the proposed contract, applies the caller's compatibility policy, and
either refuses or emits a gated publish proposal. It never publishes anything
itself.

## Procedure

1. Native `data.digest` binds the exact current schema, proposed schema, and
   sample set before any judgment, so the verdict is tied to specific bytes.
2. Deterministic comparison walks both contracts: removed fields, type changes,
   fields that became required, new required fields, and narrowed enums are
   breaking; additive optional fields and expanded enums are notes.
3. Every sample payload is validated against the proposed contract. Coverage is
   reported honestly: paths no sample exercises are flagged, not assumed
   covered.
4. The policy decides the verdict. Breaking changes are refused unless
   `breaking_allowed` is explicitly true, and policy `required_fields` must
   exist in the proposed contract.
5. A compatible verdict emits a `proposal` with the three digests and changed
   paths, gated on a schema publisher or human approver. A refused verdict
   emits no proposal. `live_write_performed` is always false.

Invalid requests refuse with `policy_result: invalid_input` and findings rather
than guessing. Missing required inputs fail at admission.

## Output

`schema_check` (`runx.schema_check.v1`) carries `decision`, `policy_result`,
`breaking_changes`, per-sample `validation_results`, `migration_notes`
including coverage, the gated `proposal` or null, and `validation`.

Inputs are `current_schema`, `proposed_schema`, `sample_payloads`, and
`compatibility_policy`.
