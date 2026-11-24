---
name: implement-from-plan
description: >-
  Load this skill when building from a written plan: phase by phase, failing check first, only what
  the phase names, with each phase's check run and its evidence recorded. Trigger on "implement the
  plan", "build phase 2", "start building the mvp plan".
argument-hint: "[plan-file] [phase]"
compatibility: >-
  Needs uv, which runs scripts/artifact.py with Python 3.10+, pydantic 2 and PyYAML to check a
  plan/v2 plan, an ARCHITECTURE YAML or a PRD YAML and render its Markdown. Without uv each is
  saved unchecked and unrendered.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Implement From a Plan

Build a plan one phase at a time, and prove each phase with its own check before starting the
next. The plan format is in `${CLAUDE_SKILL_DIR}/references/plan-schema.md`. Done means every
targeted phase is `done` with evidence in the plan, or the run stopped at a named phase with the
reason recorded.

## Procedure

1. **Find the plan.** Take the path from the arguments, matching a slug given in place of a path
   as the format's Location section says. Otherwise look in the plan folder for a
   plan with `status: ready` or `building`, and when there are several, take the most recently
   created and say which. With no plan at all, write a minimal one from the request as `plan/v2`,
   a filled copy of `${CLAUDE_SKILL_DIR}/assets/plan.template.yaml`: Goal, Scope, and phases with
   checks, every assumption under Open. Say that you did, because the user may have expected a
   plan to exist. A plan found only at the old root `product/plans/`, in a repo whose `CLAUDE.md`
   names no plan folder, is reported with its move (each file under root `product/` to the same
   sub-path under `.agents_workspace/product/`) and the run stops, never reading it or writing
   beside it, because two folders split the artifacts again.

   **A `plan/v2` plan is checked first.** When `<slug>.yaml` sits beside the plan's `.md`, the
   YAML is the plan: read and edit it, never the `.md`. Before acting on it, run
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <slug>.yaml`. When it exits 1
   with errors, stop and report them, because a stage that acts on a broken plan builds the wrong
   thing. When its only error is a stale `.md`, run the same command with `render` and go on.
   When it exits 3 or uv is missing, say in the reply that the plan went unchecked, and go on.
   After the last write to the YAML, run `render`. In the YAML, a phase's Status is its `status`
   and `evidence`, the reason or failure the steps below put in a Status goes in its `note`, and a
   Record line is a `record` entry, with `phase` set on a Built Phase entry.

2. **Read the whole plan before any edit.** Design is binding. An Open item marked as blocking
   stops the run before it starts.
3. **Build each targeted phase in order.** The target is the named phase, or by default every
   `todo` phase. Skip `done` phases. At an `unplanned` phase, stop: it needs planning first.
   For each phase:
   1. Say which phase you are starting and what it builds, in one line. When the phase adds a
      type, module, or function other code calls, take its shape from the plan's Design. When the
      Design does not settle it (an older plan, or the minimal plan step 1 writes), settle it there
      first: the signature, the file it lives in, a forbidden value each type can hold, what each
      write does when it runs twice, who writes each shared value, and the smallest interface each
      module needs. Append a Design changed line to the Record.
   2. When the phase builds code, write the failing test for the behavior it adds and run it to
      see it fail. When `ceh-testing` is installed, `ceh-testing:write-test-first` sets out how.
      When the phase builds documents, write its acceptance checks (the commands or read-through
      items its Check names) into the phase's `note`, run them, and add one line of their failing
      output to the note.
   3. Implement what **Builds** names, and nothing else.
   4. Run the phase's **Check**. When it fails, fix and rerun. When the same failure comes back
      after two fixes, stop: record the failure and what you tried in the phase's Status, leave
      it `todo`, and report. A third blind fix rarely works, and the next session needs the
      record.
   5. Set the phase's Status to `done` with its evidence: the commit, or the check command and
      one line of its passing output. Append a Built Phase line to the plan's `## Record`. When
      this is the plan's first `done` phase, set `status: building`.
4. **Close the plan.** When every phase is `done`, set `status: built`. Then, when
   `.agents_workspace/product/PRD.yaml` exists, run `artifact.py check` on it (format in
   `${CLAUDE_SKILL_DIR}/references/prd-schema.md`). When a feature's `plans` holds this plan's
   path, read the `status` of every plan that feature lists: when all are `built`, set the
   feature's `status` to `built` and the PRD's `updated`, and run `artifact.py render` on it.
   Otherwise leave the feature as it is. A PRD whose check lists errors is reported and left
   alone, because the build is already proven and does not stop here. When the only error is a
   stale `.md`, go on, since the render fixes it. When the check exits 2 or 3 or uv is missing,
   make the edit and say in the reply that the PRD went unchecked and unrendered.
5. **Copy the lasting decisions.** The built plan stays in the plan folder as the record of this
   change: later planning runs read only its frontmatter. When `ceh-check-build-against-plan` is
   installed, run `ceh-check-build-against-plan:check-build-against-plan` first, because it adds
   its Checked line to the plan. Then append each Design decision a later reader still needs to
   `key_decisions` in `.agents_workspace/product/ARCHITECTURE.yaml`, in the shape of
   `assets/architecture.template.yaml`, per the `architecture/v3` section of
   `references/architecture-schema.md` (a missing file starts as a copy of the template, and an
   `ARCHITECTURE.md` with no YAML is moved first, as that section says). Check the YAML with
   `artifact.py check` before the edit and `render` it after, as for the plan, and never edit the
   generated `ARCHITECTURE.md`. Skip a decision the log already holds, under the same title or
   with the same decision, or that a `technical_design` entry already states, and say which
   were skipped. When the plan's Design, or one of its Design changed entries, states a
   different choice on a `technical_design` entry's topic, edit that entry to what was built:
   the decision you copy is its history, and each earlier `Accepted` entry of `key_decisions`
   on that topic becomes `Superseded by <date> <title>`. Say which entries you edited. Then look at each diagram marked `planned: true`: when
   every node or entity it shows now exists in the code, remove the key, delete the built entry
   of the same `name` that it replaces when there is one, and say so. Otherwise leave it and
   name what is still missing. Add a changelog entry when the repo keeps a changelog. Say which
   decisions were copied.

## Rules

- Build only what the phase names. A gap you find in the plan goes under Open with the
  assumption you took, never into the build as unplanned scope.
- When the build has to depart from Design, edit the Design line, give the reason in the phase's
  Status, and append a Design changed line to the plan's `## Record` quoting the old line, so the
  plan stays true to the build and the original decision survives.
- A phase is `done` only on a passing Check run after its last edit. A check you could not run
  leaves the phase `todo`, with the reason in its Status. The one exception is a check the user
  reports having run: it sets the phase `done` with
  `evidence: reported by the user, not run by the agent`, and its Built Phase line carries the
  same words.

## Output

After the run, report per phase: done or stopped, the Check command and its result, assumptions
taken, and anything not verified with the command the user should run. List the phases set `done`
on the user's report apart from the ones whose Check you ran. List the decisions copied
to `.agents_workspace/product/ARCHITECTURE.yaml`. Name the PRD feature the plan delivers and its
status after the run, when there is one.

## Stop conditions

- An Open item blocks building, or the next phase is `unplanned` → stop and name it.
  `ceh-build-plan:write-build-plan` plans it.
- A Check needs a secret, a service, or a device the session cannot reach → stop at that phase,
  record what it needs, leave it `todo`, and report.
- The same check failure survives two fixes → stop as in step 3.4.
