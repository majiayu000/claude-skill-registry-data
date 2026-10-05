---
name: gate-test-execution
description: Gate 5 — unit + e2e direct (+ docker for connectors) all run green. Use after Gate 4, before producing the final build artifact.
---

# Gate 5: Test execution

Gate 4 verified the tests *exist* and are shaped right. Gate 5 verifies they *run* against the current code and pass.

## What to run

```bash
cd package/<vendor>/[<suite>/]<service>

# 1. Unit tests
zbb test --slot local

# 2. e2e direct — in-process, hits the live API
zbb testDirect --slot local

# 3. e2e docker (connectors only) — through the container's wire protocol
zbb testDocker --slot local

# 4. (Skip testHub — blocked upstream)
```

Every command must exit 0.

## Pass criteria

- `zbb test` exits 0 — no unit failures, no `pendingMocks()` leaks, no unhandled rejections
- `zbb testDirect` exits 0 — happy paths green against the real API; tests skip cleanly when their env constants are missing
- For connectors: `zbb testDocker` exits 0 — same suite runs against the containerized impl
- No new tests are silently skipped because of missing fixtures (compare skip counts between local and what the test author expected)
- No tests rely on local file system or shell env beyond what `zbb env`/`zbb secret` provides

## What to look for in the output

- **`<N> passing`**, **`<M> pending`** (skipped), **`0 failing`** — the shape you want
- A high `pending` count is fine, but each pending test should be there because a required env constant is empty, not because someone `it.skip(...)`'d it without a reason
- "before" hook failures show up as a single line at the top of the report — read upstream of the test list to find them
- nock leak warnings (only relevant in `zbb test`): `unmatched request` means a producer call wasn't mocked; `unfinished mocks` means a mock was set up but never consumed

## Iterating on a single test

```bash
# Run only one file
zbb test       --slot local -- --grep "<Tag>Api"
zbb testDirect --slot local -- --grep "<operation>"

# Debug output
LOG_LEVEL=debug zbb testDirect --slot local
```

## Pre-Gate 6 stamp

After Gate 5 passes locally, the next thing is to lock the proof in with `zbb gate --slot local` (Gate 6). Don't run `zbb gate` before Gate 5 passes — it'll just fail at the test step and you waste the rest of the lifecycle.

## On failure

- **Unit failures** — re-run with `LOG_LEVEL=debug`; look at the nock interaction. The most common bug is a producer URL that doesn't match the mocked URL exactly (trailing slash, missing query string).
- **e2e direct failures** — your impl is reading the live API and getting back a shape mappers don't expect. Capture the raw response (see `@.claude/skills/mapper-runtime/SKILL.md`) and fix the mapper or the API spec.
- **e2e docker passes nothing** — the container can't reach the API. Usually a credential or env that's set in your shell but not on the slot (`zbb env list --slot local` to verify).
- **All e2e tests are pending** — `constants.ts` defaults are empty and you haven't set the env vars on the slot.

## Related

- @.claude/skills/gate-unit-tests/SKILL.md — Gate 4a (unit creation)
- @.claude/skills/gate-integration-tests/SKILL.md — Gate 4b (e2e creation)
- @.claude/skills/gate-build/SKILL.md — Gate 6 (final + stamp)
- @.claude/skills/integration-testing/SKILL.md — e2e patterns
- @.claude/skills/unit-testing/SKILL.md — unit patterns
- @.claude/skills/environment-files/SKILL.md — zbb env / secret
