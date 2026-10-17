---
name: verify-configuration
description: Verify a Crossplane configuration package before committing - build it, run its composition tests and read the render, and optionally orchestrate its E2E tests or run the project on a development control plane ("verify the configuration", "validate the project", "is this ready to commit", "run the tests", "run the project", "deploy it", "spin it up", "try it on a control plane", "up project run", "dev control plane"). Use it instead of running raw `up project run` - on a Space context that run pushes to a private repository the control plane cannot pull, hangs on `Waiting for package to be ready` and dies with `context deadline exceeded`; this skill checks for that first and hands the choice of target back rather than falling back to `--local`. Not for writing tests (author-tests) or running a single E2E test (e2e-test-configuration).
license: Apache-2.0
references:
  - references/report-templates.md
  - references/dev-control-plane.md
---

# Crossplane Configuration Verification

Verify that a configuration package is ready for commit: build it, run the composition tests,
report what ran, and on request orchestrate E2E tests or run the project on a dev control
plane.

## Before you start

Load `control-plane-project-charter` first, or read its `SKILL.md` beside this skill's
directory; this skill does not load it. Every "ask" below follows its §1 (unattended: never
ask; act on the brief and state the assumption, or stop and report), and its §4 binds every
summary.

- This skill changes no code and fixes nothing: fixes go to the authoring skills, new tests to
  `author-tests`. It runs E2E only through `e2e-test-configuration`.
- **Asked to run, deploy or try the project:** Phase 5; verification alone stops at Phase 3.
- **Reviewing someone else's change:** read
  `control-plane-project-charter/references/charter/review.md` first: what to re-run and what
  to check beyond the gate.

### Local-only projects and projects with their own gate

- **The project has its own gate** — a script or make target that builds and runs the
  tests. Run it instead of the phases it covers, and report its command, exit code and output
  (charter §2: the project's own decisions win; §4).
- **Upbound Cloud is ruled out** — by the project or the user. Use `--local` throughout and
  skip the Space checks and the push-target decision. A local run that fits in your shell's
  timeout runs in the foreground, with no monitoring loop.

## Phase 1: Build

Run the phases in order, one at a time: a failed build or composition test ends the
verification. Run `up project build`. If it fails, report the error and stop.

## Phase 2: Composition tests, and the render

Run `up test run "tests/test-*"`. If any fail, report the failures and stop. If it prints
`No test files found`, no test ran, though it exits 0: report that, never a pass (charter §8).
Each run pays a full project build (timings:
`control-plane-project-charter/references/charter/tdd.md`).

Keep the `test-*` glob: `tests/*` also runs the e2e test programs, even without `--e2e`, and
fails at `✗ Parsing tests` whenever an e2e input is unset. `no valid CompositionTests found`
means the matched dirs produced no `CompositionTest` (e.g. only `e2etest-*` dirs): a wrong glob,
not a failing test (charter §7).

**Read the render, not just the exit code.** `up test run` checks only the resources a test
asserts: an extra managed resource added to a function left a 2-test suite at 2/2 PASS. When the
change added or modified a composed resource, re-run with `--function-logs` and list what the
function emitted as `control-plane-project-charter/references/charter/evidence.md` shows (use
the directory the run prints). Check that every resource the change should produce is in the
render and asserted: one rendered but not asserted is a gap to report, not a pass.

## Phase 3: Report, then offer E2E

**If failed:** report the failures and stop. Do not offer E2E tests.

**If passed:** report what ran, as a summary rather than full logs
([report-templates.md](references/report-templates.md)).

Two things a composition run does not prove, so don't report them as verified (charter §8):
- **Readiness branches** run only in a test that sets `spec.observedResources`, and even then
  prove the branch logic, not that a provider reports that status.
- **`providerConfigRef` correctness**: a reference to a ProviderConfig that does not exist
  renders and asserts cleanly and fails only on a real control plane
  (`control-plane-project-charter/references/charter/v2-resources.md`).

Then E2E, unless the project rules it out:

- **Interactive:** ask whether to run the E2E tests now, later, or not at all because they
  already passed, and on which target (local kind or a Space group) unless the project, its
  gate or the user already named one; `e2e-test-configuration`'s `local.md` and `space.md`
  references give the durations per target. For "later", say E2E is still outstanding before
  commit.
- **Unattended:** run them only if your brief asks for E2E and names the target; otherwise
  say they were not run, and why.

## Phase 4: E2E orchestration (if confirmed)

1. **Discover:** `ls -1d tests/e2etest-* | sed 's|tests/||' | sort`
2. **Run one test at a time.** For each, hand this brief to a sub-agent and wait for its
   result. Do not load `e2e-test-configuration` into your own context while you can start a
   sub-agent; only if your harness has none, follow the brief yourself (charter §1):
   ```text
   Run E2E test: <name> on <local kind | Space <space>/<group>>[, with --public].
   Load the `e2e-test-configuration` skill. Return PASSED with summary or FAILED with analysis.
   ```
   Add `with --public` only when the user chose it.
3. **Keep going past a failed test:** each test gets its own control plane, so one failure
   says nothing about the next. A sub-agent that cannot start, or a skill that errors, counts
   as that test's failure. Stop the remaining tests only when the failure is shared — a
   precondition, the target or the package install (`Waiting for package to be ready`) would
   fail every test the same way — and list what did not run.
4. **Write the report** `e2e-test-report-YYYY-MM-DD.md` and output a short summary: pass/fail
   count with each test's duration from its run's log
   ([report-templates.md](references/report-templates.md)).

## Phase 5: Run it on a dev control plane (when asked to run/deploy)

**Read [dev-control-plane.md](references/dev-control-plane.md) before any
`up project run`** and work through its steps: where the context sends the run, the Space
pre-flight, the choice you hand back when a Space cannot pull, applying credentials, a
ProviderConfig and an example XR, confirming the run reconciled, reading the effect back from
the provider, and a run that hangs on `Waiting for package to be ready`.

**Wait for the run inside your turn.** `up project run` takes several minutes. Run it in the
background only if your harness tells you when it exits, and then wait for that; otherwise run
it in the foreground (charter §1: never detach a run yourself). Never end your turn with the
run in flight: in many agents a session's jobs die with it, leaving the KIND cluster
`up-<project>` and its registry container running, and no result.

**Tear down with `up project stop`** from the project root, but only after deleting the XRs you
applied and waiting until `kubectl get managed -A` is empty: `up project stop` deletes the
control plane with whatever is still on it, and the cloud resources behind it stay. The steps,
what to do when deletion hangs, and what a hand-deleted cluster leaves behind:
`control-plane-project-charter/references/charter/targets.md` (Teardown and leftovers).

### Never

- Run `up project run` without working through the reference's steps.
- On a Space the control plane cannot pull from, pick the target yourself: no silent
  `--local`, and **never `--public` on your own initiative — it permanently publishes the
  user's package.** Put the three options to the user, or report them to your caller and stop.
- Create a control-plane group, Space or control plane to make a run work (charter §9).
- Pipe the run into `tail`/`head`: it buffers until exit, so a healthy run looks hung.
- Retry a hang blindly, or report "the run timed out": the cause is usually permanent, and the
  real error is in the Configuration's conditions.
- Report "verified" from `Ready=True` or from your own manifest. Without a provider read, say
  "reconciled; not independently verified at the provider".

## Success criteria

Checks for you, not a report format (report what ran, charter §4):
- Build succeeds (exit 0, package in `_output/`).
- All composition tests pass ("Failed tests: 0"), the run did not print `No test files found`,
  and every resource the change produces is in the render and asserted.
- E2E offered (interactive) or handled as the brief says (unattended), unless the project
  rules it out.
