---
name: feature-build
description: >-
  Builds a feature's PLAN.md task by task: a builder subagent implements, a reviewer
  subagent gates, and each task commits only on pass. Use once feature-plan has an ordered
  task list and it's time to write code.
user-invocable: true
argument-hint: [path to the feature's plan folder, optional]
---

# feature-build

> 🎯 **Design for change.** Each task's diff should be small, local, and behind a stable
> seam. The reviewer fails work that couples modules or bloats blast radius; the builder
> should pre-empt that.

Execute the task checklist in a feature's plan folder, one task at a time. You are the
orchestrator. You do **not** write or review feature code yourself. You dispatch to the
`builder` and `reviewer` subagents and gate on their verdicts.

**On the gate granularity:** review runs before every commit, not once at the end, so a bad
task is caught before it compounds into the next. This is the default, not optional. It
doesn't replace the whole-feature review (see "Finish"); the two catch different things.

## Scope

- IN: build each unchecked task, get it through review, commit it.
- OUT: planning, writing the task list, authoring specs — this **consumes** a plan, it
  doesn't author one.

## Preflight

1. Resolve the plan folder: the path given in the argument; else, if the current
   branch/worktree name matches a plan folder under the project's convention (see
   `CLAUDE.md`'s "Finding the current feature's plan folder" rule; the normal case when
   resuming), use that match; else **stop and ask**. Don't guess. Its name is the feature slug
   used below for the branch/worktree.
2. Read `PLAN.md`. It must be a checklist (`- [ ]` / `- [x]`). If it has no checkboxes, stop
   and send the user to `feature-plan`.
3. **Resuming or first run?** If any task in `PLAN.md` is already `- [x]`, or `BUILD-LOG.md`
   has entries, an earlier run already cut the branch/worktree: skip to step 5. Otherwise
   continue to step 4.
4. **Cut the feature's branch/worktree.** The one point in the pipeline that touches git
   before feature code exists (see `git-workflow`'s "Branch/worktree per feature" section).
   In order:
   1. Confirm the working tree is clean *except* for the plan folder and any new or refreshed
      mockup starters in `docs/mockups/starters/` (`feature-explore`/`feature-design`/`feature-plan` never
      commit them). Any *other* uncommitted change is unrelated work; stop and report.
   2. Confirm you're on the project's trunk branch (see `CLAUDE.md`'s Feature workflow
      section). If not, stop and ask. Don't guess which branch to fork from.
   3. **Ask the user to confirm before running any of this.** It commits to trunk, which the
      "always ask before touching main" rule covers however small the change.
   4. Commit the plan folder as-is, on trunk, with any changed project starters: `git add
      <plan-folder> docs/mockups/starters && git commit -m "docs: add plan folder for
      <feature-slug>"`.
   5. Create the branch/worktree named after `<feature-slug>`, off that commit. Prefer Claude
      Code's native worktree mechanism (`isolation: "worktree"` on the `Agent` tool, or the
      project's `WorktreeCreate` hook) so the project decides the real branch name and
      location; else fall back to `git checkout -b <feature-slug>` off trunk. Never invent a
      separate worktree/branch mechanism.
5. Before touching code, confirm `pwd` and the current branch match `<feature-slug>` (or
   whatever the project's hook named it), and that the plan-folder commit is in the new
   branch's history (`git log --oneline -5`). A `WorktreeCreate` hook that branches from
   `origin/<trunk>` instead of local trunk silently leaves out a commit that was never pushed.
   If it's missing, remove the worktree, ask the user before pushing trunk, then create it
   again.
6. **Check the demo/test site is worktree-safe, if one exists.** Check its `.csproj`
   references `Umbraco.Community.WorktreeDevPort`. Without it, the site runs on a fixed port
   (two worktrees smoke-testing at once collide, and it looks like a broken build) or on a
   random `:0` port nothing can find. If missing, **stop and flag it** and suggest re-running
   `project-init`; its "Demo site ports" step adds the package and fixes anything that finds the
   site by a hardcoded port. No demo/test site: this step is a no-op.

## The loop

For each task still unchecked (`- [ ]`) in `PLAN.md`, in order, top to bottom:

1. **Build.** If the task changes an existing screen, first screenshot it at 1440×900 as
   `screenshots/<screen>-before.png`. Once the builder starts, the old screen is gone, and the
   PR needs before and after.

   Then dispatch a `builder` subagent (Agent tool, `subagent_type: builder`, model
   sonnet). Give it: the exact task text, the relevant sections of `ARCHITECTURE.md` and
   `SPEC.md`, the path to any mockup for a screen the task touches, the files/extension points
   it owns, and an instruction to invoke the project's
   stack skills (`umbraco-extensibility`, `umbraco-package-conventions`, `ef-core-data`,
   `umbraco-backoffice-conventions`, etc. as relevant) and run the existing specs before reporting back. If the project has e2e tests and none covers the
   task's path, tell the builder to add one (the smoke step runs it). The builder does not
   commit.

2. **Review.** Dispatch a `reviewer` subagent (Agent tool, `subagent_type: reviewer`, model
   opus, must be ≥ builder). It invokes `umbraco-security` (when the diff
   touches security) and the relevant stack skills, reads the builder's diff, and returns `PASS` or
   `FAIL` with specific findings.

3. **Recurse.** If `FAIL`: send the findings to a fresh `builder` for the same task, then
   review again. Nothing reaches git history before `PASS`. If a finding is a repeatable
   mistake a future `builder` would likely make on another task, write it to
   `.claude/memory/` (type: `gotcha`) once fixed.
   - **Re-review the round, not the task.** Before each fix round, snapshot the tree
     (`git add -A && git write-tree`, which stages but doesn't commit). After it, give the
     `reviewer` the previous round's findings and the round's diff
     (`git add -A && git diff --cached <tree>`), so it runs its "Re-review rounds" mode.
     Reviewing the whole task again each round mostly finds older code, not the fix, and
     the loop stops converging.
   - **Three rounds, then rethink.** After the third `FAIL` on one task, don't send a fourth
     patch. Dispatch one fresh `builder` with every round's findings, told to reconsider the
     approach rather than patch the last finding, and review its result in full. If that
     fails too, stop and report the task and its findings. If the findings show the design
     is wrong, not the code, hand off to `feature-design`.

4. **Smoke the real entry point.** Before commit, exercise the deployed artifact. Use the
   first of these the project has:
   - **An end-to-end (e2e) test suite.** Run the e2e test covering the task's path. If none
     covers it, the builder adds one as part of the task. A suite passing without touching
     the new code proves nothing.
   - **A demo site.** Start it and run through the change yourself: drive the backoffice UI
     (Playwright or equivalent), or send one real request through the Management API
     controller for a change with no screen.
   - **Neither**, because you're building the host itself (like Umbraco CMS), not a package
     installed into one: a thorough integration test that boots the real hosting/DI pipeline
     (not a unit test through an internal seam) is the equivalent gate.

   Fakes for external services are fine in all three; the request must travel through the
   real entry point, not an internal function that bypasses it. If the smoke fails, recurse
   to step 3 with a finding. A green unit test suite is not enough to ship.

   **If the task adds or changes a migration** and the project supports SQL Server, the smoke
   includes running it on a real SQL Server, as `ef-core-data` describes. Note in the task's
   `BUILD-LOG.md` entry which providers it actually ran on.

   **If the task renders a screen that has a mockup,** screenshot the built screen at 1440×900
   and compare it with `mockups/<screen>.png`. A difference in layout, components used, or
   what's shown (a missing or extra column, a box split or merged, a different chart type) is
   a smoke failure unless the builder's report flagged it as a deliberate departure. Small
   spacing and colour differences are not. Once the screen is complete, save its screenshot as
   `screenshots/<screen>.png` in the plan folder (this loop's folder; `mockups/` belongs to
   `feature-design`). Link it from the task's `BUILD-LOG.md` entry with the click path to reach it
   ("Settings › Webhooks › any webhook › Deliveries tab"), so `pr-describe` can tell
   reviewers where to find it.

5. **Commit.** On `PASS` + smoke green, have the builder commit *only this task's changes*
   with a message naming the task, following the project's commit conventions (see
   `git-workflow`). One commit per task. If the task's code makes a pending spec pass for
   the first time, that spec file goes in the same commit, never in a later cleanup commit.

6. **Check the box.** Edit `PLAN.md`: `- [ ]` → `- [x]` for the completed task, and add a
   one-line entry to `BUILD-LOG.md` (commit SHA, what was verified). Commit that change, plus
   any `screenshots/` this task saved, with the task commit or immediately after.
   `pr-describe` links screenshots by commit, so an uncommitted one is a broken image in the
   PR. If the builder's report named "any decision the plan left implicit that you had to
   make" (step 6 of its workflow), such as an assumption, spec deviation, or workaround,
   append a dated one-line entry to `DECISION-LOG.md` too. Otherwise it is lost when the task
   ends; `decision-review` depends on it being on disk.

7. Next task.

## Finish

When every box is checked: run the full test suite once more. If `BRIEF.md` has a `Repro`
section, run it through the real entry point, as step 4 does, and see it pass; a failure goes
to a fresh `builder` like a review finding. Then run the whole-feature review below, then
report a summary (tasks completed, commits, anything still red).

**Whole-feature review.** The per-task `reviewer` sees one task's diff, so it misses what
builds up across tasks: duplicated logic, a class that took on a second job, a component that
started calling a repository directly, drift from `ARCHITECTURE.md`. Dispatch one `reviewer`
subagent in whole-feature mode with the full branch diff (`git diff <base>...HEAD`),
`ARCHITECTURE.md` and `SPEC.md`.

- On `FAIL`, send the findings to a fresh `builder`, then review again. Repeat until `PASS`,
  with the same round diffs and three-round limit as the loop's "Recurse" step; here the
  round diff is the round's own `refactor:` commit. Commit each round as its own `refactor:`
  commit and add a `BUILD-LOG.md` line for it.
- If a finding means the design itself is wrong, not just the code, stop and hand off to
  `feature-design`.

A human still reviews the PR; this pass means they aren't the first to see cross-task
problems. Update the `BUILD-LOG.md` line in `README.md`: check its box and replace
`<pending>` with one plain-English line (task count, commit count). Never touch another
phase's line. If this feature is (or completes) a standalone package ready to publish, invoke
`umbraco-marketplace` before tagging a release; it's not part of this loop.

**Open the PR: invoke `pr-describe` directly (via the Skill tool). Don't write the body
yourself.** Claude Code's built-in `gh pr create --body "$(cat <<'EOF' ... EOF)"` recipe does
**not** apply here. Per `git-workflow`, the PR body is always `pr-describe`'s job, no
exceptions: never `--body` at all. `pr-describe` handles branch/push via `git-workflow` and
runs `decision-review`, so the assumptions, deviations, and workarounds in `DECISION-LOG.md`
reach a human in the PR. (`decision-review` is also user-invocable on its own, read-only, for
an earlier look.)

If this feature built inside a worktree, don't remove it here. That's post-merge cleanup (the
project's `WorktreeRemove` hook, or `git worktree remove`). Archiving the plan folder is
post-merge too: `feature-close`, once the PR is merged.

## Rules

- Sequential, dependency-ordered. This is a pipeline, not a parallel team.
- Builder owns code; reviewer owns the gate; this loop owns sequencing, `PLAN.md` checkbox
  state, `BUILD-LOG.md`, `screenshots/`, and its own line in `README.md`. Never collapse these roles.
- The orchestrator may investigate directly: read docs, call an endpoint, read logs. The
  moment a fix touches code, dispatch a builder, even for one line you already know. This is
  easiest to break mid-debugging against a live system, where each small tweak feels too
  small to hand off.
- If a gate still fails after the rethink round, stop and report the task + findings rather
  than committing degraded code.
