---
name: test-strategy
description: Choose the right tests for a change, write diagnostic failures, handle legacy code and flaky suites, and report coverage gaps honestly.
---

# Test strategy: prove behaviour at the cheapest useful layer

- Test observable behaviour and contracts, not private structure. A test that breaks on every refactor without catching a behaviour change is a maintenance tax.
- Choose the cheapest layer that gives confidence: a pure unit test for logic, an integration test for a boundary, end-to-end only for a small number of critical journeys.
- For a bug, write the failing test first. For legacy code, add characterization tests around the current behaviour before changing it.
- Cover the edges that matter: empty, invalid, unauthorized, duplicate, timeout, partial failure and retry. One test per behaviour, not one per line.
- Make failures diagnostic: assert the important value and include the input in the failure. Avoid sleeps, shared mutable state and dependence on execution order.
- Treat a flaky test as a defect. Quarantine, reproduce and fix the source; do not retry until green.
- Report coverage gaps honestly. A high percentage does not prove the risky paths were tested.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
