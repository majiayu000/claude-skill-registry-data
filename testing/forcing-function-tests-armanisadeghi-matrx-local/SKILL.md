---
name: forcing-function-tests
type: Skill
title: "forcing-function-tests — a test may pass only when the real system works"
description: "The bar every automated test or guard must clear: green only when the real system works. Use when writing, fixing, or reviewing a test, mock, stub, fixture, snapshot, or self-test; adding a regression test for a bug; or about to call work done because tests pass."
tags: [testing, guards, verification, doctrine]
timestamp: 2026-09-14T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/forcing-function-tests/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Forcing-Function Tests

A test's only job is to FAIL when the system is broken. The expected result must exist only at the
end of a chain of real work — a **forcing function** — with no shortcut to it through the harness.
A green reachable without the system doing its job is fiction: worse than no test, because it ships
false confidence. Applies to pytest, jest, `node --test`, `check:*` scripts, and `--self-test` guards.

**A real test around a big change — a playbook a fresh agent walks in the live product, written first and proven to fail on a planted break — is the `safety-net` skill; this one is the bar for the automated kind.** **Tests are guards, not verification.** Green never flips anything to done. Done = someone who did
not build it, on the live surface, with real data (`campaign-pattern`). A test keeps one named break
caught forever. **Fixture names look real, and test people come only from the persona factory** ([test-data-looks-real](/policies/test-data-looks-real.md): `aidream/aidream/testing/persona.py`, `matrx-frontend/scripts/lib/persona.mjs`; never hand-make an account).

## 1. Before the body: name the break

Write the production change that makes this test fail — in the name or a one-line comment.
- Cannot name one → no test; find an observable outcome.
- Only an intentional decision fails it (a constant, message wording, private structure) → change
  detector. Test the behavior that depends on the decision: not `MAX_RETRIES == 5`, but "the 6th
  attempt never happens".
- Only a crash or a missing selector fails it → it guards nothing.

**Method.** (1) Name the SUT precisely — "the function `foo`", "the orchestrator", never "the
feature". (2) List what it OWNS: ordering, routing, decisions, joins, persistence, transformations —
never stubbed. (3) List external dependencies: network, registered functions, third-party SDKs,
time, randomness — stubbed with known returns. (4) Design input and environment so the expected
output is reachable only if every owned responsibility executes; any misstep (wrong order, dropped
branch, swapped data, silent corruption) diverges observably. (5) Assert on that forcing output,
never on an intermediate value the harness set up. (6) Gut check (§3).

## 2. The expected value comes from outside the code

A literal, a worked example, the spec, or a payload captured from the live system. Never:
- computed by the code under test or its helpers (`expect(build(x)).toBe(build(x))`,
  `expected = items.reduce(...)`);
- the fixture or input echoed back (`User(name="Alice").name == "Alice"` proves assignment, not
  `User`; input `url` asserted on output `url`).

## 3. Gut check, then mutation pass

**Gut check — RUN it, every test, before you call the test written.** Replace the SUT with
`return expected` and execute the suite. Still green → rewrite the test. Reasoning that it would fail
is not the gut check, and a mutation pass does not stand in for it: the two are both required, and the
pass most tests survive is this one. **One forcing input never survives it** — a constant returns that
input's expected value. So when every case shares one expected value, a second input with a DIFFERENT
expected value belongs in the SAME change (`it.each` / `parametrize`, a second captured page), never as
a "before done" follow-up. (Observed 2026-09-10: 5 of 6 skill-guided reps shipped a single forcing input
under "keep it small"; the two that named the second input deferred it, and the runner's executed
`return expected` mutant passed their merged tests.)
**Mutation pass:** for each realistic mutation, at least one test must go red — wrong constant or
argument · wrong branch · missing side effect or state change · empty/default return · missing
refusal for empty, zero, null, unauthorized, malformed · stages swapped or data between them
corrupted · work silently skipped or dropped. A mutation nothing catches is an unguarded behavior:
add the forcing input; do not bolt assertions onto a weak test.
**Shared checkout → every mutation runs through `plant.py` beside this skill, never a hand edit**,
one test file per command (usage in its docstring; proof: `plant_selftest.sh`). Exit 3 (restore failed) or
5 (mutation committed) → stop and revert it. Hand plants were left on disk and captured by peer commits,
one of them an auth bypass (2026-09-10).

## 4. Doubles replace what the SUT CALLS, never what it IS

Ask of every double: *does it replace a dependency, or the logic I am verifying?* Only the first.
- Legitimate: third-party API, LLM, network, registered function, clock, randomness, filesystem, slow startup.
- Illegitimate: anything the SUT owns. If the stub's return IS the answer, you are testing the stub
  (`mock.run.return_value = 42; assert mock.run([1,2,3]) == 42` — the pipeline did nothing).
- Before mocking, list the real method's side effects; keep the ones the test depends on real and
  mock the slow/external level beneath them.
- Never assert on the double's own presence (a `*-mock` test id, "the mock rendered").
- Call args, counts, and order ARE assertable when they are the contract (dedupe, exactly-once send,
  not-reinvoked-on-resume). Make the double specific enough that the wrong branch cannot satisfy it —
  one fixture per branch (success, error, malformed).
- Mock setup outgrowing the test logic → use real components (real `Scheduler` + `MemoryCheckpointer`;
  real store + real reducers with only the API module mocked).

## 4a. Proving RED never weakens the shared working tree (added 2026-09-12, Data Doctrine chair)

A RED proof that edits the real guard on disk is one interruption away from shipping the weakening: on
a shared checkout a peer sweeper commits whatever is on disk the moment a lane dies (it happened —
a frame guard reached `main` deleted; DD-158). So: prove RED by injecting the weakening **in memory**
(patch/mock inside the test), in a **scratch copy**, or in a **`git worktree`** you delete after. If the
real file must be touched, weaken and restore in the SAME tool call, then verify the restore.

## 5. Fixtures: captured, complete, typed

The done law bans manufactured data as PROOF. Controlled inputs inside a guard are fine — shaped
from reality:
- **Captured, not invented.** Record a live payload or a sanitized real row (RecordReplay
  `mode="record"`) and commit it beside the test.
- **Complete.** Every field the real thing carries, not just the ones this test reads. A partial
  double passes while integration breaks.
- **Typed against generated contracts.** TS fixtures `satisfies` the generated DB/API type — never
  `as` / `as unknown as` a partial object (matrx-frontend `type-safety` skill). Python fixtures go through the real
  Pydantic model.
- **Environment conspiracy** (nondeterministic systems — agents, schedulers, solvers): choose stubbed
  dependency values whose composition leaves exactly one correct output. The SUT must consume,
  combine, and route every one of them to land it; no partial-credit path exists. This tests that
  the orchestration fed the nondeterministic component the right inputs and used its output
  correctly, without testing that component itself.

## 5a. Every value comes from a REAL USE CASE (the owner's law, 2026-09-21)

Before entering any test data, name the real use case in one sentence: who the user is, what
business they run, what job this exact feature does for them. A recycling company's pickup
schedule. A dental practice's new-patient intake. A property manager's maintenance requests. Then
make the values true to that business — field names a practitioner would use, statuses that follow
a real lifecycle, money that adds up, dates that make sense together, and relationships true to the
domain (an invoice belongs to a job that belongs to a client).

**Banned outright:** `Acme`, `foo`/`bar`/`baz`, lorem ipsum, `test table`, `ZZZ …`, `Job 001`,
sequential `Item 1…N`, `.example` mailboxes, and one stand-in person repeated everywhere. A
screenshot of "Job 001 / Ada / 42" tells the owner nothing; a picture of a recycling route with
today's pickups tells him whether the product works. Placeholder data does not fail a test — it
destroys the only way anybody can tell whether the thing is finished.

**Never real personal data.** Names, emails, phones and addresses are synthesized to look real and
belong to nobody; no row is copied from a real customer, a real inbox, or the production tables.
Realistic is the standard; real people are forbidden. Test identities stay `admin@admin.com` and
`test@test.com`.

**Name everything after the use case.** The organization, the tables, the form, the pipeline, the
document, the notification — "the Harbor Dental new-patient intake", never "ZZZ FORMS-2 safe to
delete". Cleanup finds a test organization by a tag in its settings, never by a junk name.

**Do not invent your own.** The datasets live once, in `@ai-matrx/records/use-cases`
(`aidream/apps/shared/records/src/use-cases/`, with a README on adding one). Draw from it; add a
use case there when none fits, and the library's validator will refuse a dataset whose field types
the store cannot resolve, whose relations point at rows that do not exist, or that carries junk.

**Enforced:** `aidream/scripts/check_no_placeholder_data.mjs` and matrx-frontend's
`pnpm check:no-placeholder-data`, both reading their banned patterns from that one library so they
cannot disagree. They scan the data that reaches a SCREEN — demo harnesses, seeds, screenshot
scripts and recorded fixtures — not every unit test's opaque handles: `user-1` in a cache
assertion is a handle, and `example.com` in a URL-parser test is the reserved domain doing its job.
A line genuinely needing a banned word carries `matrx-real-data:allow <reason>`, and the reason is
required.

## 6. Bug fixes and guards: red first, for the right reason

- Fixing a defect: write the test or guard FIRST and watch it fail on the unfixed code. It must sit
  at a seam that reproduces the real bug pattern (the real caller chain, the real boundary); a seam
  too shallow to exhibit the bug is false confidence — record the missing seam instead (`diagnose` §5).
- The red must be an assertion failure that names the defect. An import error, typo, missing
  fixture, or timeout is not a red — fix it and re-run until it fails correctly.
- Fix, watch green. For guards, commit the sabotage as `--self-test`: plant the violation → exit
  non-zero with file:line and the fix → restore → clean ([strictness-law](/policies/strictness-law.md) §7–8).
- A test green on its first-ever run has proven nothing yet — sabotage it once.
- **A multi-rule guard must prove each rule SEPARATELY, and the sabotage is per-rule.** Break one
  rule at a time and watch the self-test go red *for that rule*. Whole-suite red proves nothing
  about which rule earned it.
- **A fixture caught by a rule OTHER than the one it names is a fake proof.** Observed 2026-09-11:
  a byte-size guard grew four rules; the fixture for the fourth put the unit label three lines from
  the arithmetic, inside an older rule's six-line window, so the older rule matched it and the new
  rule was never exercised. Deleting the new rule entirely left the self-test PASSING. The rule was
  real; only its proof was fake. Write each fixture so it can be caught by nothing but its own rule
  — then delete that rule and confirm the self-test goes red.
- New features: test-first order is not mandated; the §3 mutation pass is the proof. Never delete
  working code to replay a red-green ceremony.

## 7. Source-reading tests: census, never change detector

Reading source is legitimate when it derives a CLASS from the code and fails on any new member
(every field the client sends is writable; every `postgres_changes` table is published). Asserting
that one specific line or symbol exists — or stays removed — is a change detector: replace it with
behavior or delete it. Census tests carry a self-test.

## 8. Where tests go

- Your code's boundary contract — the query emitted, payload produced, row persisted, event emitted —
  not framework mechanics (Pydantic raising, a router calling a handler, React rendering a prop).
- Persistence: assert the LIVE row or DB machinery, not the repo's belief ([verify-live-state](/policies/reality-is-the-referee.md) §1).
- Vertical slices: one behavior → its test → its code → next. Never a batch of tests for imagined
  behavior up front.
- Test-only helpers (reset, destroy, inject) live in test utilities, never on production modules.
- One behavior per test — a name that needs "and" gets split. The name states the forcing function:
  `test_<must_be_true>_when_<condition>` / `it("refuses X when Y")`; never `test_it_works` /
  `test_happy_path`.

## Reject on sight — the four failure modes and their cousins

- **Tautology:** asserting what the fixture set up; `assert True`, `is not None`, `toBeDefined()`,
  `toBeTruthy()` as the primary behavior assertion
- **Over-fitted input:** one cherry-picked input a hardcoded return satisfies (`apply_discount(100,
  "SAVE10") == 90` passes against `return 90`) — use several inputs, `parametrize`, or property-based tests
- **Mock owns the logic:** mocking the SUT or a layer inside it (§4)
- **Coincidental ordering:** dependence on dict/set iteration, thread scheduling, harness step order,
  or test order the SUT does not guarantee; shared mutable state across tests
- Waiting with `sleep`/fixed delays for async work — wait on the actual condition with a timeout whose
  error names what never happened; a fixed delay is legitimate only when the behavior under test IS
  timing (debounce, tick interval), with a comment saying why
- Broad `except` / `catch` asserting "didn't crash"
- Snapshots nobody hand-checked
- Real LLM / paid API calls in CI (use committed recordings)
- `skip`, `xfail`, `.only`, `it.todo` left on a behavior-critical test — an escape hatch
- "Tests are green" offered as done

## Rationalizations

| Excuse (verbatim, observed 2026-09-10) | Reality |
|---|---|
| "A second saved page, via `parametrize`, would stop a hard-coded answer from passing" — listed as a follow-up | A known hole deferred is a shipped hole; a constant passes the merged test today. |
| "The test still checks two things in one, because the brief said not to restructure it" | "Keep it small" never waives §3 or one behavior per test. A split is one more `it`. |
| "…which works because the node imports `scrape` at call time" | That is the SUT's own pipeline. Stub the fetch beneath it (§4). |
| "My lines add nothing — the existing test already catches this bug" | Run `return expected` against it first: that test used the SUT's own helper as its oracle and passed a hard-coded mutant. |

## Red flags — in the brief or in your own reasoning

- "Keep it small — just add an assertion to the existing test."
- "A second input can come later."
- "The existing test already guards this" — said before a `return expected` run.
- "The stub works because it is looked up at call time."
- CI is red on something else / the release train leaves in 20 minutes.

## Done criteria — every one true, or the test is rewritten, not patched

1. It fails when the execution path is wrong.
2. It fails when a piece of work is silently skipped or dropped.
3. It fails when data between stages is swapped or corrupted.
4. It fails against a `return expected` replacement of the SUT — executed, not reasoned.
5. Its expected output is a forcing function on everything the SUT owns, from a source independent of the SUT.
6. It sits at a seam that reproduces the real bug pattern.

## Review sequence (anyone's test, including yours)

1. What exactly is the SUT? 2. What does it own — is any of it stubbed? 3. Name the one-line bug this
catches. 4. Does `return expected` pass it — run, not reasoned? 5. Is the expected output forced by correct execution
and independent of the SUT, or arranged by the fixture? 6. Are fixtures captured, complete, and typed?
Any unanswerable → not mergeable.

## Stack notes

- **Python:** `pytest`, not `unittest`; fixtures set up, never assert; `@pytest.mark.parametrize` one
  forcing function over many inputs; `pytest.raises(..., match=...)` asserting type AND the
  message/attribute proving the right path fired; mark `@pytest.mark.integration` (and e2e) so they
  can be selected or excluded. Workflow actions → aidream `matrx-action-testing`.
- **TypeScript:** jest (`pnpm test <path>`), `node --test` for scripts. RTL queries by role/text, never
  by mock test id. Redux: real store + reducers.
- **Guards:** exit code is the verdict; unreachable data = UNMEASURED = fail (strictness-law §7).
