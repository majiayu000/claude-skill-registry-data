---
name: unit-testing-standard
description:
  MUST load this BEFORE writing or editing any *.test.ts or *.test.tsx file in
  this repo.
---

- Tests MUST follow setup (arrange deps/mocks) -> act (perform) -> verify
  (assert) structure.
- Mocks MUST use `ts-mockito`, object-oriented style, not ad-hoc
  `vi.fn()`/module patching.
- Indeterministic code (time, randomness, network, etc.) MUST NOT be handled by
  guessing — ASK the user how to handle it before writing the test.
- Tests MUST be black-box: assert on observable behavior/contract, not
  implementation details, so they catch real bugs instead of just mirroring the
  code as written.
