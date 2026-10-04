---
name: schema-catalog-sync-guard
description: Detect and explain drift between DSDS TypeScript schema definitions and canonical catalogue CSV references. Use when auditing coverage, finding missing component/event/policy definitions, and proposing reconciliation updates.
---

# Schema Catalog Sync Guard

## Overview
Check whether schema types and canonical catalogue entries still match. Report drift with concrete fixes and priority.

## Workflow

1. Parse schema surface
- Extract component unions, event types, policy/invariant definitions, and scenario constants from schema.

2. Parse catalogue surface
- Extract canonical entities from taxonomy, events, failures, invariants, patterns, and scenarios CSV files.

3. Compare and classify drift
- Find missing-in-schema and missing-in-catalog entries.
- Detect naming inconsistencies and semantic mismatches.

4. Prioritize fixes
- Mark critical drift that can break simulation correctness first.
- Mark documentation-only drift separately.

5. Produce reconciliation plan
- Provide exact file targets and suggested edits.
- Include validation checks to prevent future drift.

## Output format
1. `Coverage summary`
2. `Critical drift findings`
3. `Non-critical drift findings`
4. `Reconciliation actions`
5. `Preventive checks`

## References
- Read `references/drift-check-rules.md` for comparison rules.
- Use these repo sources:
- `schema/complete_simulator_schema.ts`
- `canonical-catalogue/*.csv`
- `schema/README.md`
