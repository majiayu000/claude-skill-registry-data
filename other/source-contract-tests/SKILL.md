---
name: source-contract-tests
description: Run or extend the host-side static source-contract tests without mistaking them for dynamic firmware tests.
---

# Source Contract Tests

## Use when

Safety-relevant code integration, rollover helpers, EEPROM ordering, fallback behavior, or their host-side checks change.

## Procedure

1. Read `tools/source_contract_test.py` and identify the specific production-code contract under test.
2. Run `python tools/source_contract_test.py` from the repository root.
3. If adding a test, make it specific to a stable source contract; avoid brittle whole-file snapshots and unrelated formatting checks.
4. Run both AVR builds after production C++ changes.
5. Report what the test proves and what it does not prove.

## Constraints

- Current tests inspect source structure/order; they do not emulate the MCU, EEPROM electrical behavior, ISR timing, or motor controller.
- Never describe a source-contract test as a hardware or runtime test.
- Do not add a fake test that merely repeats a hardcoded expected string without binding it to the production path.

## Done when

All relevant tests pass, or failures identify a precise source contract that is absent or violated. Residual behavior questions are documented separately.