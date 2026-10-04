---
name: thalarch-spec
description: >
  Turns broad feature or architecture requests into an executable acceptance contract.
  Use for multi-file features, refactors, migrations, architecture work, ambiguous behavior,
  or whenever implementation could succeed technically while missing the user's actual intent.
---

# Thalarch Spec

Treat requirements as testable constraints, not prose.

## Build the acceptance matrix

For each user requirement record:
- ID;
- observable behavior;
- scope;
- proof;
- non-goal;
- dependency;
- ambiguity/ruling.

Separate:
- functional behavior;
- compatibility;
- error behavior;
- performance constraints;
- UI/UX constraints;
- external-action constraints.

## Clarify only material ambiguity

Ask only if different interpretations would materially change the outcome and no
safe reversible default exists.

Otherwise record a ruling with:
`Ruling — reason — cost if wrong`.

## Cross-artifact consistency

Before implementation, check:
- no requirement is missing a planned task;
- no planned task exists without a requirement or justified engineering necessity;
- tests actually prove the requirement they claim to cover;
- two tasks do not define conflicting interfaces.

## Output

The specification should be compact enough to hand directly to a cold verifier.
