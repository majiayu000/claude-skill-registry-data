---
name: implement-from-plan
description: >-
  Load this skill when building from a written plan: phase by phase, failing test first, only what
  the phase names, with each phase's check run and its evidence recorded. Trigger on "implement the
  plan", "build phase 2", "start building product/plans/mvp.md".
argument-hint: "[plan-file] [phase]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Implement From a Plan

Build a plan one phase at a time, and prove each phase with its own check before starting the
next. The plan format is in `${CLAUDE_SKILL_DIR}/references/plan-format.md`. Done means every
targeted phase is `done` with evidence in the plan, or the run stopped at a named phase with the
reason recorded.

## Procedure

1. **Find the plan.** Take the path from the arguments. Otherwise look in the plans folder for a
   plan with `status: ready` or `building`, and when there are several, take the most recently
   created and say which. With no plan at all, write a minimal one from the request in the plan
   format: Goal, Scope, and phases with checks, every assumption under Open. Say that you did,
   because the user may have expected a plan to exist.
2. **Read the whole plan before any code.** Design is binding. An Open item marked as blocking
   stops the run before it starts.
3. **Build each targeted phase in order.** The target is the named phase, or by default every
   `todo` phase. Skip `done` phases. At an `unplanned` phase, stop: it needs planning first.
   For each phase:
   1. Say which phase you are starting and what it builds, in one line. When the phase adds a
      type, module, or function other code calls, sketch its shape before the test. When
      `ceh-coding-conduct` is installed, `ceh-coding-conduct:sketch-design` sets out how.
   2. Write the failing test for the behavior the phase adds, and run it to see it fail. When
      `ceh-testing` is installed, `ceh-testing:write-test-first` sets out how.
   3. Implement what **Builds** names, and nothing else.
   4. Run the phase's **Check**. When it fails, fix and rerun. When the same failure comes back
      after two fixes, stop: record the failure and what you tried in the phase's Status, leave
      it `todo`, and report. A third blind fix rarely works, and the next session needs the
      record.
   5. Set the phase's Status to `done` with its evidence: the commit, or the check command and
      one line of its passing output. Append a Built Phase line to the plan's `## Record`. When
      this is the plan's first `done` phase, set `status: building`.
4. **Close the plan.** When every phase is `done`, set `status: built`.
5. **Copy the lasting decisions.** The built plan stays in the plans folder as the record of this
   change: later planning runs read only its frontmatter. When `ceh-check-build-against-plan` is
   installed, run `ceh-check-build-against-plan:check-build-against-plan` first, because it adds
   its Checked line to the plan. Then, in one commit: copy each Design decision a later reader
   still needs to the Key Decisions log in `product/ARCHITECTURE.md` (the format is in
   `ceh-codebase-explanation:document-architecture` when installed, otherwise a dated heading with
   Context, Decision, and Consequences), and add a changelog entry when the repo keeps a
   changelog. Say which decisions were copied.

## Rules

- Build only what the phase names. A gap you find in the plan goes under Open with the
  assumption you took, never into code as unplanned scope.
- When the code has to depart from Design, edit the Design line, give the reason in the phase's
  Status, and append a Design changed line to the plan's `## Record` quoting the old line, so the
  plan stays true to the code and the original decision survives.
- A phase is `done` only on a passing Check run after its last edit. A check you could not run
  leaves the phase `todo`, with the reason in its Status.

## Output

After the run, report per phase: done or stopped, the Check command and its result, assumptions
taken, and anything not verified with the command the user should run. List the decisions copied
to `product/ARCHITECTURE.md`.

## Stop conditions

- An Open item blocks building, or the next phase is `unplanned` → stop and name it. With
  `ceh-build-planning` installed, `ceh-build-planning:write-build-plan` plans it.
- A Check needs a secret, a service, or a device the session cannot reach → stop at that phase,
  record what it needs, leave it `todo`, and report.
- The same check failure survives two fixes → stop as in step 3.4.
