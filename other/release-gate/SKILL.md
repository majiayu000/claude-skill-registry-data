---
name: release-gate
description: Validate a phase or release candidate before handoff.
disable-model-invocation: true
---

# Release Gate Skill

Run or document:

1. `cmake --preset debug`
2. `cmake --build --preset debug`
3. `ctest --preset debug --output-on-failure`
4. Forsetti compliance script.
5. Relevant targeted tests.
6. Static grep for forbidden provider-era routes or direct AI execution paths when applicable.
7. Package/build smoke checks in release phase only.

Reject completion if any acceptance criterion is unproven.
