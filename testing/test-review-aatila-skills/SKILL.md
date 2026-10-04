---
name: test-review
description: Use when the user asks to review or audit existing tests, questions whether tests are any good, suspects a flaky or vacuous/smoke test, asks what test cases are missing, or wants a test-quality and coverage-gap check before a refactor or on brownfield / AI- / teammate-authored tests. Read-only — exposes false greens (bad tests that pass for the wrong reasons) and coverage gaps as findings, hands gaps to tdd. NOT tdd (writes tests test-first), NOT qa-plan (manual acceptance from intent), NOT aa-second-opinion (general diff review).
disable-model-invocation: true
---

# Test Review

Judge an existing test suite against one standard: a good test pins observable behaviour through the public interface. The enemy is the **false green** — a suite that passes for the wrong reasons, hiding rot behind a wall of green: tests that assert nothing, tests welded to the implementation, tests that never ran the branch that matters. You **expose** the false green as findings; you never write the fix. Each coverage gap is a job for `tdd`, driven out one at a time. Code you just TDD'd is the weak target; this earns its keep on tests you _didn't_ write — brownfield, AI-authored, teammate, or rotted suites, and before a refactor you need to trust the green behind you.

## Pipeline position

Read-only, dual-home:

- **VERIFY** — audit teammate- or AI-authored tests before merge, beside `qa-plan` / `aa-second-opinion`.
- **MAINTAIN** — sweep a brownfield or rotted suite; a churn hotspot's tests are suspect.

Feeds `tdd`: each coverage gap becomes a red-green cycle. Supplies the trust check upstream of any refactor — are these tests good enough to change the code behind them?

## Scope

Resolve a target; never silently default to the diff (a suite you just TDD'd is near-empty by construction):

- A named **module / directory / suite** — the sweep, primary mode.
- A **diff** — when the tests under review are teammate- or AI-authored ("I didn't write these").

If none is given, ask which. Audit that target's blast radius, not the whole repo.

## Gates

- **G1 — Behaviour, not coverage %.** Every finding names a behaviour a caller cares about. "Line 42 is uncovered" is not a finding; "the empty-cart path has no test and ships a crash" is.
- **G2 — Grounded in evidence.** A quality finding cites the test and the smell. A coverage gap gives `input → expected`, grounded in a real branch, guard, or spec — never a generic "test your error handling".
- **G3 — Expose, never write.** Findings only. Each gap hands to `tdd` for one-at-a-time red-green. Emit zero tests — batching missing tests after the fact is the horizontal-slicing anti-pattern `tdd` exists to prevent.

## The method

Two passes hunt the false green from both sides: Pass 1 finds green that asserts nothing; Pass 2 finds the behaviour the green never ran. See [references/detection-heuristics.md](references/detection-heuristics.md) for the full smell catalogue, static flaky signals, and coverage heuristics.

### Pass 1 — Quality (existing tests)

Read each test cold and ask the diagnostic. If you can't answer "yes, definitely", it's a finding.

- **Does it assert observable behaviour?** — not a mock's own return, not `toHaveBeenCalledWith` as the only assertion (tautological); not `toBeDefined` / snapshot-only (vacuous / "smoke").
- **Would it survive an internal rename?** — or does it mock internal collaborators, test privates, assert call order (implementation-coupled)?
- **Does it pass for the same reason every run?** — or does it read uncontrolled time / random, real network / fs, timer-based waits, or shared mutable state (flaky-prone)?
- **Is it live?** — `.skip` / `.only` / `xit` / ownerless `todo` / commented-out.

### Pass 2 — Coverage (missing behaviour)

Read the branches, guards, and error paths in the code under test. Each one with no test that exercises it is a gap — phrase it as `input → expected` for `tdd`: a real happy path a user hits · a guarded branch · an unasserted throw / reject / `Result`-error · boundary values (empty / null / max / off-by-one) · the regression surface a diff exposes.

Ground every gap in an actual branch (G2). A gap you can't tie to observed behaviour is coverage-% chasing — cut it (G1).

## Execution (opt-in)

The findings are the deliverable. Running is a separate, confirmed step — never automatic:

- **Confirm flaky:** re-run a suspected test N times.
- **Confirm gaps:** run the coverage tool and reconcile against Pass 2.

## Output

A findings list — not a report artifact. Group by severity; lead with `fix`. Per finding:

- **Location** — `file:line` or test name
- **Finding** — the smell or the gap, one sentence
- **Why** — the diagnostic it fails (G1 / G2) or the untested branch
- **Hand-off** — the concrete fix, or the `input → expected` for `tdd`
- **Severity** — `fix` (broken or misleading test) · `gap` (missing case that matters) · `consider` (judgement call)

A clean suite is a valid result. Don't manufacture findings to look thorough.

## Worked examples

**Good.** A `checkout` suite's only test asserts `paymentService.process` was called → `fix`, implementation-coupled + tautological (asserts the call, not the outcome). Reading the code, the empty-cart and declined-card branches have no test → two `gap` findings, each `input → expected`, handed to `tdd`.

**Rejected by a gate.** "Add tests to cover these 12 uncovered lines." Refused by **G1** — no behaviour named. Reframed only for the lines that map to a real behaviour (the expiry branch); a logging line and a defensive `?.` stay uncovered on purpose.

**Wrong skill.** "Write the tests for me" → `tdd`. "Walk me through QA-ing this" → `qa-plan`. "Review the whole PR, not just tests" → `aa-second-opinion`.

## Boundaries

| Want to…                          | Use                                | Relationship                                               |
| --------------------------------- | ---------------------------------- | ---------------------------------------------------------- |
| Write tests test-first            | `tdd`                              | It writes; this judges and feeds it gaps.                  |
| A manual acceptance walkthrough   | `qa-plan`                          | Intent-first, human-run; this is code-contract, static.    |
| Review non-test code too          | `aa-second-opinion`                | General diff review; this is the test lens.                |
| Cut over-engineered code          | `aa-simplify`                      | Removal-biased; shares the read-cold, findings-only shape. |

## Before you hand over

- [ ] Target resolved and blast-radius-scoped, not the whole repo?
- [ ] Every finding names a **behaviour** (G1), grounded in a test or branch (G2)?
- [ ] Coverage gaps written as `input → expected` for `tdd` — **no tests written** (G3)?
- [ ] Severity-grouped, `fix` first; a clean suite reported honestly?
- [ ] Execution offered as opt-in, not run automatically?
