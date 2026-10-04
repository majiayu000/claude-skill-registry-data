---
name: tdd-workflow
description: Drives RED → GREEN → IMPROVE in this repo's actual runners — pytest via `rtk proxy`, vitest in frontend/, Playwright for flows — and requires the RED state to be observed, not assumed. Use when writing a new feature, fixing a bug, or refactoring anything under the Python API, frontend/, or the theme's JS. Do NOT use for retrofitting tests onto code that already shipped green (that is a coverage-gap task), and do NOT use it to decide whether an existing suite's result is trustworthy — that is verification-loop.
origin: ECC
---

# Test-Driven Development

TDD's value is not the test file. It is the **observed RED**: the one moment you have
evidence the test can fail. Skip it and you have written an assertion nobody has ever
seen return "no" — decoration with a green checkmark.

This repo has paid for that. A fraud scorer shipped with a fully green suite; adversarial
review then found **16 real defects** (bug-150). The tests proved each rule fires. Nobody
had ever watched them fail for the right reason.

## When to use

Use it when:

- adding a feature or endpoint under `agents/`, `api/`, `services/`, `skyyrose/`
- fixing a bug — the regression test is written first and must reproduce the bug
- refactoring: the suite is the safety net, so it must be green *before* you touch code
- changing a gate, guard, or validator — those need an explicit fail-closed test

Do **not** use it:

- to backfill tests onto already-shipped code. That is a coverage-gap task with a
  different shape (read the code, find the untested branch); there is no RED to observe.
- to judge whether someone else's green suite means anything — that is
  [`verification-loop`](../verification-loop/SKILL.md) plus
  [`adversarial-verification`](../adversarial-verification/SKILL.md).
- for pure config/docs edits with no behaviour.

## Inputs

| Required | How to get it | If absent |
|---|---|---|
| A green baseline before you start | `rtk proxy pytest tests/ -q` → 6546 passed, 0 failed | **Stop.** On a red baseline you cannot tell your break from the existing one. Fix or quarantine first, and name who owns the pre-existing failure. |
| The right runner for the surface | Python → `rtk proxy pytest` · `frontend/` → `npm test` (vitest) · flows → `npx playwright test` | **Stop.** A bare `pytest` in this repo can print "no tests collected" and read as success. |
| A stated behaviour, not a stated function | "invalid SKU raises `ValueError`", not "test `resolve_image`" | **Stop and restate.** A test named after a function tests whatever the function does, including the bug. |
| A writable per-test temp dir (`tmp_path`) | pytest fixture | **Never write to tracked files.** bug-153: a test injected tokens into the real shared `design-tokens.css` and failed only under the full suite. |
| For `frontend/`: the suite must be importable under vitest | `vitest.config.ts` uses an explicit `include` (`lib/wp/**`, `tests/**`) | **Stop.** A suite outside `include` is silently never run — and a skipped security test is indistinguishable from a passing one. |

## Procedure

1. **Record the baseline.** Run the suite for the surface you are about to touch and note
   the exact counts. You will diff against these, not against "green".
2. **Write the test first**, naming the behaviour and the failure it forbids. One
   behaviour per test; arrange-act-assert.
3. **Run it and read the failure text.** RED must be the *right* red — an assertion
   about your behaviour, not `ImportError`, not a fixture typo. A test that errors before
   reaching its assertion has not demonstrated anything.
4. **Write the minimum implementation** to turn it green. No speculative branches, no
   abstraction for a single call site.
5. **Re-run the single test, then the surface's full suite.** A test that passes alone
   and fails in the suite is shared-state pollution (bug-231, ×5), not flake.
6. **Prove the test can still fail** — extract the pre-change file with
   `git archive HEAD <path> | tar -x -C <scratch>` and run your new test against that
   pristine tree. It **must** fail there. Never `git stash`: the stash stack is shared
   across worktrees.
7. **Check coverage for the module you touched**, not repo-wide — the repo number moves
   too slowly to show your delta.
8. **Refactor with the suite green**, re-running after each step.
9. **Never weaken a test to make it pass.** Loosening an assertion, adding `xfail`, or
   widening a tolerance to reach green converts a real failure into a silent one.

**A SKIP is not a PASS.** This worktree is sparse, so asset-dependent tests skip by
design (bug-257). Report them as "not executed here; closed by CI / the full checkout" —
never inside a passing count.

## Verification

**1 — The new test is green in isolation and in the suite.**

```bash
rtk proxy pytest tests/mcp/test_http_mount.py -q && rtk proxy pytest tests/ -q
```

**PASS:** the single file passes, and the full run reports `N passed` with `0 failed`
and `N >= 6546` (the baseline). A drop in total count means you deleted or de-collected
tests. `[test]`

**2 — RED was real: the test fails against the pristine tree.** This is the
prove-it-can-fail rule and the attribution rule in one move.

```bash
mkdir -p /tmp/tdd-pristine && git archive HEAD mcp_tools/ | tar -x -C /tmp/tdd-pristine
rtk proxy pytest tests/mcp/test_http_mount.py -q --rootdir=/tmp/tdd-pristine
```

**PASS-OF-THE-PROOF:** this run **fails**. If your new test passes against code that
predates your change, it is not testing your change. `[test]`

**3 — Coverage on the module you touched.**

```bash
rtk proxy pytest tests/mcp/ -q --cov=mcp_tools --cov-report=term-missing
```

**PASS:** the touched module reports ≥ 85% and the `Missing` column contains no line
from your new code. `[repro]`

**4 — Frontend suites are actually collected.** vitest's explicit `include` makes silent
non-collection the default failure here.

```bash
cd frontend && npm test 2>&1 | tail -5
```

**PASS:** the summary names your spec file. If your file is absent from the output, it
was never run — fix `vitest.config.ts` `include` or move the suite. `[repro]`

**5 — Flows: the Playwright spec is registered.**

```bash
cd frontend && ./node_modules/.bin/playwright test --list | tail -1
```

**PASS:** the total count went **up** by your test count. `testDir` is `./tests/e2e`;
a spec written into the legacy `frontend/e2e/` is never executed and shows here as an
unchanged total. `[repro]`

**A run that errored, timed out, or hit a session limit is not a pass.** Its empty
failure list is an artifact — re-run it by hand (bug-230).

## Worked example

Regression test for bug-211 (MCP bearer token compared with `!=`; fail-open when
`MCP_SERVICE_TOKEN` is unset). Real commands in this worktree, 2026-07-29.

Baseline for the surface:

```bash
$ rtk proxy pytest tests/mcp/test_http_mount.py -q
......                                                                   [100%]
```

`[repro]` — 6 passed. That is the number the next run is diffed against.

The behaviour under test, stated before the code: *"an Authorization header that shares a
prefix with the real token is rejected, and the comparison is constant-time"* — which is
why the implementation reads:

```bash
$ grep -n "compare_digest" mcp_tools/http_mount.py
88:        if not hmac.compare_digest(provided, f"Bearer {token}")
```

`[repo]`. The RED proof is the interesting half: run the same test file against the
pre-fix tree via `git archive`, and it must fail on the `!=` comparison. Running it only
against the fixed tree — where it passes — would have demonstrated nothing about the
test.

The contrast case, same session, same runner:

```bash
$ rtk proxy pytest tests/test_asset_manifest.py -q
SKIPPED [1] tests/test_asset_manifest.py:42: sparse worktree deliberately excludes
  assets/products; this gate runs in full checkouts and CI
SKIPPED [1] tests/test_asset_manifest.py:51: ... (×4 total)
```

`[repro]` — 4 skipped, **0 passed**. Reported as "asset-manifest integrity did not run in
this worktree". Rolling those four into a "tests pass" line is the exact bug-257 defect.

## Failure modes

| Symptom | What is really happening | Bug |
|---|---|---|
| Suite fully green, adversarial review finds many real defects | Tests proved each rule fires; none exercised calibration, boundaries, or the never-raises guard. Green ≠ correct. | bug-150 |
| Test passes alone, fails in the full suite | Shared state — module globals, a real tracked file written in place, ordering under `asyncio_mode=auto`. Use `tmp_path` / `monkeypatch`. | bug-231 (×5), bug-153 |
| Test skipped everywhere, counted as passing | A SKIP is not a PASS. Name who closes it (CI / full checkout). | bug-257 |
| `pytest` says "no tests collected", read as success | Bare pytest misreports in this repo. Always `rtk proxy pytest`. | — |
| New frontend spec never appears in output | Outside `vitest.config.ts`'s explicit `include`, or written into the legacy `frontend/e2e/` that Playwright's `testDir` excludes. | — |
| Test made to pass by loosening its assertion | The failure was real and is now silent. Fix the cause, never the assertion. | — |
| RED never observed; test written after the code | No evidence the assertion can fail. Re-derive via `git archive` against the pristine tree. | — |
| `git stash` used to get a clean tree for the RED check | The stash stack is shared across worktrees; you can pop another session's work. | — |
| Multiprocess/fork test SIGSEGVs on macOS | Darwin fork safety — `no_proxy='*'` must be pre-set and the resource tracker pre-spawned. | bug-263 (×7) |
| Coverage measured repo-wide, shows "no change" | Your delta is invisible in a 6546-test total. Measure `--cov=<touched module>`. | — |
