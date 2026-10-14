---
name: behavior-characterization
description: "Trigger: behavior characterization, observable behavior. Record what legacy code does today."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.1.0"
  status: testing
---

# Behavior Characterization
Detect what the system does today without judging whether it is ideal.

## Observable signals

- Return values.
- Exceptions and error codes.
- Side effects and state changes.
- Persistence writes/reads.
- Published events.
- Relevant logs.
- External calls.
- Edge conditions and branch behavior.
- Implicit business rules.

Every behavior claim needs code evidence or must be marked as a hypothesis.

## Characterization method

- Write an assertion expected to fail, run it, and read the actual value from the failure message; anchor that value as the expected result. The test documents what the code does, not what it should do.
- Characterize only the zone the plan will touch (targeted characterization), not the whole unit by default.

## Bugs found while characterizing

Characterize the bug as-is: the test anchors today's wrong output. Never fix it in the same step — record it, finish the safety net, and schedule the fix as a follow-up behavior change to run with the net in place.
