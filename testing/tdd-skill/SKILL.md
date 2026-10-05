---
name: tdd-skill
description: >
  Test-first (red-green-refactor) workflow for any codebase. Invoke whenever
  adding or changing behavior, fixing a bug (the fix starts with a failing
  regression test), or when asked to "add tests", "write a test for this",
  "cover this", or "do this with TDD". Codebase-agnostic: it tells you to first
  discover how THIS project runs tests, then apply the loop, and to verify
  against a live stack when a unit test can't reach the behavior. Do NOT use it
  merely to run/observe an existing change in the app — that's the /verify
  command; this skill is the discipline for driving code WITH tests.
---

# TDD Skill

Core rule: **always test your work.** A change isn't done until a test exercises
it (or, where a unit test can't, you've run it against a live stack and watched
it behave). Never report something as working that you haven't observed working.
Code that merely compiles/loads is not proof.

> **Who writes the code:** when implementation is delegated to another agent, that
> applies to tests too: the orchestrator writes the failing-test brief and reviews the
> diff, and does not author product code or specs itself unless the delegate is
> unavailable (then it does, at the identical bar, flagged inline). Two rails that bite
> here specifically: some delegate sandboxes **cannot bind sockets or reach the
> network**, so such a delegate's green is not green for anything
> server/e2e/coverage-gated — re-run it yourself, and verify any environment limit it
> claims rather than accepting it; and **review its tests as adversarially as its
> implementation** — a test whose name asserts the opposite of its body still passes.
> (Who writes the code in this install: `LOCAL.md` beside this skill, when your copy
> keeps one — section *Who writes the code*.)

## Step 0 — discover how this project tests (do this first, every repo)

Don't assume a command — a wrong runner wastes the whole loop on tooling noise
(e.g. running jest bare from inside a package can pick up the wrong root config and die on
plain TS). Consult the **project-config** skill's reference file first; if the
facts aren't recorded there, discover them once and record them (its
record-on-miss rule). What you need before writing any test:

- The runner: `package.json` scripts (jest/vitest/mocha), `Gemfile` +
  `.rspec` (RSpec), `pytest.ini`/`pyproject.toml` (pytest), `go test`,
  `cargo test`, `Makefile`/`justfile` targets, CI config (`.github/workflows`).
- Where tests live and the naming pattern (`spec/`, `test/`, `__tests__`,
  `*_test.go`, `*.test.ts`).
- The fixture/factory and mocking conventions already in use — read 1–2
  neighboring tests and copy them, so your test reads like the rest.
- How to run **one** test fast (single file / single case by name or line).

Gate: do not write a test until you can run a single existing test and see it
pass — that proves your invocation works before your own red/green means anything.

## The loop

1. **Red** — write the smallest failing test that names the behavior you want.
   Run it; confirm it fails for the *right reason* (the assertion, not a
   typo/import/load error — a wrong-reason red proves nothing).
2. **Green** — write the minimum code to make it pass. Run that one test.
3. **Refactor** — clean up with the test green. Re-run.
4. **Widen** — run the surrounding test file (and related ones) to catch
   regressions before moving on.

Work one behavior at a time. Don't write five tests then five implementations —
you lose the signal of which change made which test pass.

**For a bug fix, prove the test is load-bearing.** If you wrote the test after
(or alongside) the fix, you never watched it fail on the real bug — so it isn't
proven to guard anything. After green: temporarily restore the buggy version
(`git show HEAD:<file> > <file>` or revert the line), run only the new test,
confirm it fails with the bug's *exact symptom*, then restore the fix.

**When the fix hinges on a subtlety, red-probe the naive alternative too.** A
passing test proves the fix is sufficient, not that it's necessary for the right
reason. Swap in the obvious-but-wrong version and confirm the test also fails —
that pins the subtle requirement (e.g. a typed-nil check that `== nil` misses).

## Prove the test is load-bearing — mutate, don't admire

Reverting the fix (above) is the bug-fix case. The general form is mutation: break
the subject deliberately and require a red. Every rail here is a way that check has
silently failed.

- **Mutate each claim separately.** A route's decorators are independent claims.
  `@UseGuards` was pinned by a test while `@RequireScope('write')` on the same route
  was decoration — deleting it left the entire suite green, and a read-scoped token
  could have changed the account's email. "Unauthenticated → 401" does not bind
  "wrong scope → 403".
- **Confirm the mutation applied, and that it landed on the live path.** A mutation
  hitting dead code, a mock branch, or an early return "fails to fail" and reads as a
  weak test. Anchor the edit so it cannot no-op silently (a Python replace with
  `assert old in s`, never a bare `sed`/`perl` that quietly matches nothing), then
  print the diff and confirm the changed line is on the path the test exercises.
  `grep -c` cannot tell you whether an edit applied — it counts *lines*, so a token
  appearing twice gives an identical count before and after; `cmp -s` against your
  own backup is the honest check. Passing that proves only that bytes moved — then
  confirm the mutation expresses the behavior you meant.
- **Require a green baseline in the same harness, run first.** One round scored a
  hoped-for "N/N caught" entirely on exit **127**: the test command sat in an
  unquoted shell variable and zsh does not word-split, so nothing ever ran. A run
  that never executed fails exactly like a mutation that got caught.
- **Restore from a backup copy, never `git checkout -- <file>`.** On an uncommitted
  tree `checkout --` restores from HEAD — it deletes the whole slice's work in that
  file rather than the mutation you injected. This destroyed in-flight
  implementations twice, and because the specs survived it presented as a test
  failure rather than a self-inflicted wipe. `cp <file> /tmp/bk` → mutate → run →
  `cp /tmp/bk <file>`, then `cmp -s`. Tell-tale that you just wiped yourself: after
  "restoring", `git status` no longer lists the file as modified. Reserve
  `checkout --` for code already committed.
- **Red-check per FILE, never per suite.** A delegated e2e spec "proved" that a raw
  token could reach an admin route while faking the auth service wholesale — it
  passed identically against the old code, invisible inside a suite-level red where
  two other files failed. Read `Test Files 2 failed | 1 passed`, not the total. Any
  file that stays green while its feature is reverted is unrelated or tautological.
- **Say which grade of red you got.** A revert that also changes a constructor's
  arity fails all 17 specs in the file — that proves coupling, not that your guard is
  pinned. The narrow reds are the clean signal. And a spec for an intentionally
  unchanged component legitimately cannot go red; don't chase one.

## Believe the exit code, not the summary

Every rail here is a run that reported success while proving nothing.

- **A suite can print `515 passed` and exit 1** — a timed-out spec, or an unhandled
  rejection the runner reports outside any test. A mutation is caught iff the **exit
  code** is non-zero; branch on `$?`, never on a `Tests \d+ passed` line. Capture
  output and exit code from the *same* run.
- **`cmd | tail` reports the PIPE's status, not the tool's**, and truncates away the
  summary block that proves the run completed. Redirect and read the code directly:
  `<test command> > /tmp/out.log 2>&1; echo "EXIT=$?"`. Same trap wrapping in
  `timeout` — a killed run looks identical to a passing one from the tail alone.
- **A file that dies at import passes vacuously.** `Tests 31 passed (31)` printed
  beside `ProfileView.spec.ts (0 test)`, exit 1. Grep for `0 test`; read `Test
  Files`, not `Tests`.
- **A skipped or env-gated test exits 0 having run nothing.** `it.skipIf(...)` is an
  unverified test, and unverified tests rot — one asserted a `201` contract for
  months after the endpoint went async. Audit skips whenever you touch a spec file,
  and confirm a tier ran what you think (`--reporter=verbose`).
- **A coverage threshold you never collect coverage for is a silent no-op.** Jest
  and Vitest enforce thresholds only when coverage is actually collected, so a
  `test:unit` script without `--coverage` makes the policy *look* enforced while it
  never fires. Never trust a gate you have not watched fail — delete a spec, confirm
  a non-zero exit on the threshold, restore.
- **Check system load before believing a failure.** Load 7.3 produced 15 phantom
  `expected 200, got 404` failures (the app had not booted) on a command that was
  595/595 at load 4.8. Three greens and one red-under-load means green.

## When an agent writes the tests

When one agent briefs and reviews while another writes the specs and the code, that
separation is what makes a genuine red possible — and it adds failure modes a solo
loop doesn't have. (This install's split: `LOCAL.md` beside this skill, when your copy
keeps one — section *Who writes the code*.)

- **Two dispatches, never one.** An agent that writes the implementation and its
  tests in one dispatch never observes a failure. *Dispatch A:* "write ONLY
  `Foo.spec.ts`; do **NOT** create `Foo.vue`; do NOT modify any other file. The spec
  is **EXPECTED to fail** — do not 'fix' it by creating the component," with the
  unit's API pinned in the brief so the spec is written against a locked contract.
  You then run it and confirm the red is the right one. *Dispatch B*, to a **fresh**
  agent: "the spec already exists and FAILS. **That spec is the specification. Do NOT
  edit it.** If you believe a test is wrong, STOP and report." The no-edit clause is
  load-bearing — without it an agent that can't satisfy a test quietly relaxes it and
  you get green-by-amendment. Resume the Phase A agent only to correct its own specs;
  reusing it for Phase B defeats the point.
- **Verify the frozen specs by blob hash.** `git hash-object` (tracked) or mtime
  ordering (untracked) is decisive and takes one command. Hunk arithmetic on
  `git diff --stat` produced a false "the implementer edited a spec" alarm that
  nearly triggered a re-dispatch.
- **Freeze assertions, exempt plumbing — and state the exemption.** A brief that
  freezes a spec while also requiring DI-stub edits leaves the implementer unable to
  boot it; one that renames a DDL object a test pins by name breaks a spec without
  ever looking like a spec change. Mechanical trigger: when a change renames or drops
  any string-identified artifact (constraint, index, column, enum), `grep -rn "<old
  name>"` across specs and explicitly exempt every test that pins it. A frozen-spec
  break whose diff shows only an identifier change is a rename *confirmation*, not a
  regression.
- **Diff the spec against the implementation brief before freezing.** A Phase A spec
  advancing timers 1x while the Phase B brief specified 2x backoff was independently
  satisfiable — the doubling silently never shipped and everything stayed green.
  Check every constant and timing the brief names, and look for the same collaborator
  method mocked two different ways.
- **Don't trust "tests pass."** A delegate runs the specs it touched and misses
  import-level breakage it caused elsewhere — one "verified" report had **6 suites
  failing to run**. Run the module or app suite and diff against a known baseline.
- **The reviewer drives the artifact end-to-end at its real input boundary, with
  adversarial inputs, before trusting green.** Implementer-written tests encode the
  implementer's assumptions: 40/40 genuine green tests shipped an inbox that accepted
  `{{{not json at all` as a valid todo — its fallback test asserted "plain text
  becomes a todo," which was true and was exactly the bug. A 30-line script found it
  in the first output line. Budget this as a review step, not a test-writing step.
- **A delegate refusing your brief may be the delegate being right.** One declined
  to assert that a write-scoped token gets 403 on a read-scoped endpoint; the guard
  legitimately lets write pass read. Treat push-back as a claim to verify, not noise
  to override — had it complied, the suite would have encoded a false premise as a
  passing test.

## Where the bugs actually are: seams, not units

A retro on ~15 live-only defects from one shipped experience: **almost none were
logic errors inside a unit, and almost none were reachable by more unit tests of the
kind already written.** Every one lived at a seam between our code and something we
do not control — and unit tests mock exactly those seams *with our own assumptions*,
so both sides of our code agree with each other while disagreeing with reality.

- **Fixture honesty.** A fixture must be traceable to the real wire shape — the
  serializer, the producer's struct, the migration — not to what the consuming code
  happens to want. Invented fields gave a table whose every checkbox selected every
  row, a DTO typing an int as a string (every booking 503'd), and an explicit `null`
  that defeated a `NOT NULL DEFAULT 0`. When a spec is green and the user reports
  breakage, suspect fixture honesty **first**. Provenance counts as much as content:
  a smoke test using a locally-created file could not fail the way production failed,
  because the real input arrived as an unmaterialized cloud-sync placeholder. If a
  human, another machine, or a sync daemon sits in the real path but not the test
  path, you have a rehearsal — say so rather than claiming end-to-end.
- **Assembly invariants — the cheapest, highest-yield tests available.** Nobody
  tests the app *as assembled*: a layout missing its modal host silently killed every
  modal on two surfaces, a module registered at `path: ''` was unreachable through the
  deployed door while every controller test passed, a shared field hardcoding
  `type="text"` stripped `type="email"`. Pin route manifests (no empty mount, no
  duplicates, critical paths present), "every layout provides the modal host",
  "generics preserve semantic attributes". Hermetic, fast, no infra — and they reach a
  bug class no amount of component testing does.
- **Lifecycle and order under the real router.** Unit tests mount once, in a fixed
  order, with a fake router. Adopting a session re-registered routes and thereby
  *remounted* the page; a guard reading state `onMounted` had cleared bounced a
  successful booking back to the start. Gate locally the way CI runs — parallel, never
  `--no-file-parallelism` as the merge gate: a barrel import cycle only threw when the
  module graph was entered service-first.
- **Read-path semantics — the write worked and the read lied.** A PUT persisted
  while the list read a five-minute matview, which the user experienced as "not
  saving". Test the read path against seeded data, and treat "it didn't save" as a
  read-your-writes question before a write bug.
- **Then one committed happy-path e2e per money flow.** Every flow that broke
  repeatedly had *zero* committed e2e — the probes were written throwaway and deleted,
  so the same bug class recurred freely.
- **The tell:** if a bug only reproduces when the app is assembled, authenticated,
  deployed, or talking to a real producer, no additional isolated unit test will find
  it. Ask what invariant of the **assembly** it violates and pin that — and do not
  respond to this class of bug by writing more unit tests of the same shape. They are
  already green and will stay green.

## Use the project's own conventions

Match the neighbouring tests — fixtures, factories, and mocking style. Two
preferences that are *not* the default instinct:

- **Construct the unit directly with hand-rolled mocks rather than booting the
  framework's full DI/test-module.** Faster, and a failure points at the unit
  instead of at the container.
- **Mock only the true boundary** (network, clock, external services). Over-mock
  the thing under test and the test only proves your mocks agree with themselves.

## Test the wiring, not just the logic

Two classes of bug that logic-only unit tests are structurally blind to:

- **Cross-cutting wiring (guards/middleware/decorators/routing).** A behavior
  test that constructs the unit directly bypasses everything the framework
  applies *around* it — it stays green even if the guard is missing entirely.
  When you change auth/permissions/middleware, add a test that pins the wiring
  contract itself (the guard is attached, in the right order; the permission
  set is exactly X), and red→green it on a destructive path. An annotation with
  no enforcement wired up is an open door.
- **The real lifecycle.** A test that seeds data the app actually loads *after*
  init (async fetch, lazy state) passes on code that breaks in the app. Write
  it the way the app runs: start empty → deliver data → assert it updated.

**For behavior-preserving refactors, flip the loop: characterization first.**
Pin current behavior with tests that stay GREEN through the change; reserve
red→green for intentional changes. For paths a unit test can't reach, run old
vs new against a real datastore and diff outputs for parity — and say so.

## When a unit test can't reach it: verify against a live stack

Some behavior (HTTP endpoints, workers draining a queue, commit-time callbacks,
cross-service calls) is only truly proven by running it.

- **Any DB-touching change needs a real-DB run — mocked green is necessary, not
  sufficient.** Query-builder/repository doubles never execute SQL, so
  column-name mappings, NOT-NULL/defaults, joined-column ordering, and coercion
  bugs sail through mocks and crash on the first real query. After unit tests
  pass, exercise the new query path against the real dev DB — an authenticated
  request that asserts the *result* changed (a filter narrows the rows), or a
  small script that runs the real service in a transaction and rolls back. A
  guard-level 401/200 probe never reaches the query, so it can't cover this.
- Boot the smallest stack that exercises the path (a dev server, one worker,
  the needed datastore). Probe concretely: a status code, a processed job, a
  log line, a written row. A 401 from an auth-guarded endpoint already proves
  it booted and routed — but see the DB caveat above for what it can't prove.
- Know your tooling's surprises before trusting a probe (process managers that
  re-export `PORT`/env from a dotfile ignore your CLI override — check what the
  process actually bound; a harness cwd may reset between commands).
- Be careful with shared/dev queues and databases: real side effects (emails,
  webhooks, analytics). Tear the stack down when done.

## What to cover (scope) and how hard to push

Cover the critical path, then **try to break it** — adversarial cases are
non-negotiable for anything complex, and the user's standing directive is solid
edge-case tests over happy path. The probes that have actually caught bugs here:

- partial/missing inputs; empty/zero/falsy values that must be rejected as "not
  provided" (`''` and `0` are the classic misses); non-numeric/malformed params;
- "all required" vs "some" permission sets;
- ordering-independence, circular refs (no infinite loop), transitive refs;
- a dependency that throws — must fail **safe/denied**, not crash;
- short-circuit precedence: first matching branch wins, and later collaborators
  are **not** consulted (assert that).

Skip trivial passthroughs and pure config; a test there is noise.

## Common failure modes (stop if you catch yourself doing these)

- **Writing the implementation first, then a test that passes immediately** —
  that test was never red; you don't know it can fail. Go back and red it
  against the old/broken code.
- **Accepting a red for the wrong reason** (import error, typo, missing fixture)
  as "the failing test." Fix the harness issue until the failure is the assertion.
- **Trusting green mocked tests for query/schema code** — run it on a real DB.
- **Testing the handler and calling the auth change covered** — pin the
  decorator/guard wiring too.
- **Pre-populating state the app loads asynchronously** — mount empty, then
  deliver the data.
- **Fighting a framework gotcha inside the harness** (e.g. Rails `after_commit`
  never fires under transactional fixtures; unflushed timers/promises pass
  before the effect). Test the unit directly and cover the wired path with an
  integration/live check instead.
- **Hardcoding "today" into an assertion.** A spec pinning a date input to the
  literal `'2026-07-18'` passed on the day it was written, then failed *every branch
  in the repo* from midnight onward. Freeze the clock instead
  (`vi.setSystemTime(new Date('…T12:00:00Z'))` — midday UTC so no local offset shifts
  the date; `shouldAdvanceTime: true` so awaited promises don't deadlock). And never
  fix it by recomputing the expectation the way the implementation does — an
  assertion that mirrors the impl can never fail.
- **Shipping a spec you never executed.** Two Playwright specs used
  `await expect(page.goto(url)).toBeOK()`; `toBeOK()` takes an APIResponse while
  `goto` resolves a navigation Response, so both errored before reaching a single
  real assertion. They looked thorough in review. Corollary: when a test aborts
  early, every assertion after the abort point is unverified even though it is
  written down — after fixing the abort, re-read them as if new.
- **Declaring done from "it compiles" or "the suite is green"** without a test
  that exercises the new behavior specifically.

## Before you call this done

- The new/changed behavior has a test that failed before and passes after —
  and for a bug fix, you watched it fail on the actual buggy code.
- The failure you observed was the assertion, not a harness error.
- The surrounding test file (and related ones) is green.
- Wiring is pinned where the change was cross-cutting (guards/middleware/routes).
- DB-touching changes ran against a real database, not only mocks.
- For behavior a unit test can't cover, you ran it live and observed the
  expected result — and you state plainly what was verified and what was not.
- Don't re-run a clean suite as reassurance — a repeat run on unchanged code
  proves nothing. Re-run after subsequent edits, not to feel better.

## Related skills

- [debugging-and-error-recovery](../debugging-and-error-recovery/SKILL.md): a bug fix starts with the failing regression test written here.
- [database-optimization](../database-optimization/SKILL.md): a DB-touching change needs a real-database run; that skill says how to live-verify a query.
- [orchestration](../orchestration/SKILL.md): review a delegate's tests as adversarially as its implementation.
- [monitoring](../monitoring/SKILL.md): when a unit test cannot see the behavior, verify it on the live stack.

## Capturing learnings (session-handoff protocol)

This skill accumulates project-specific testing knowledge in `LEARNINGS.md` beside this
skill, when your copy keeps one.
When the user hands off a session, asks to "update skills", or when you finish testing
work: scan the session for durable testing knowledge (how THIS stack runs/locates tests,
mocking patterns that worked, framework gotchas, useful adversarial cases), distill into
concise rules, and append to LEARNINGS.md — dedupe/merge, tag stack-specific items, and
read it at the start of testing work in a matching stack.
