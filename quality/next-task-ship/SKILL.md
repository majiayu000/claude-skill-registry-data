---
name: "Next Task: Ship"
description: "Autonomously run the full delivery loop for the next roadmap task: suggest, worktree, implement, roadmap-sync, PR, self-review. Pass 'loop [N]' to repeat for up to N ready tasks"
when_to_use: "When you want to hand over a whole task cycle unattended: the user's veto over the task pick is the run's only gate, then it builds in an isolated worktree with tests green, keeps roadmaps.json and its projections coherent, opens the PR and self-reviews, fixes and re-reviews before handing back control. Add 'loop' to repeat this for successive ready tasks (default cap 3) until the ready-set is empty, a BLOCKED.md is written or the cap is hit."
model: fable
effort: high
metadata:
  glyph: ᚠ
  family: next-task
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash(git:*)", "Bash(gh:*)", "Bash(python3:*)", "Bash(node:*)", "Bash(jq:*)", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Bash(deno:*)"]
argument-hint: "[assignee] [focus area] [loop [N]] (all optional; assignee/focus area forwarded to next-task-suggest)"
---

# Ship: Next, the full delivery loop, unattended

Orchestrates four existing skills (`next-task-suggest`, `roadmap-maintain`, `pr-create`, `pr-review`) plus the mechanical git/test/lint work between them into one autonomous cycle: pick a task, build it in isolation, keep the roadmap coherent, open a PR, self-review it, fix what's actionable.

This skill does not reimplement any of those four skills' methodology; it invokes them and carries their outputs forward. Where this file's instructions and a called skill's own instructions conflict on *how* to do that skill's job, the called skill wins; this file only owns sequencing, the git/test/lint mechanics between them and the hard rules below.

## Hard rules (never break these)

1. **Roadmap files are never hand-edited.** `.claude/roadmaps.json` is the only source of truth. Never directly edit the PHASE file's task list, the Mermaid block, `ROADMAP_OVERVIEW.md` or the HTML artefact; those are `roadmap-maintain`'s job, driven off `roadmaps.json`. If something about the roadmap looks wrong, fix `roadmaps.json` (or flag it) and let `roadmap-maintain` propagate it.
2. **Never run `git stash` blind.** Before any stash, run `git status` and `git stash list` first, and only stash what those show is genuinely in the way. Prefer not stashing at all when a worktree already isolates the work.
3. **Unmet dependencies → stop and write `BLOCKED.md`, never guess.** If the suggested task turns out to have an unmet dependency, an ambiguous requirement no reasonable default resolves, or a blocker `roadmap-maintain`/`next-task-suggest` didn't already surface, stop the loop at that point and write a `BLOCKED.md` report (template in Step 8) instead of improvising a workaround. One case is *not* unmet: a dependency marked `done` whose PR is still open is a **stacking parent**; Step 2 branches from it and Step 6 opens a stacked PR (see `~/.claude/library/references/stacked-prs.md`). A dependency that is not `done` at all remains a hard stop.
4. **The gate loop is capped at 6 rounds.** Step 3's implement/test/typecheck/lint cycle gets at most 6 fix-and-rerun rounds. If the gate still isn't green after the sixth, stop and write `BLOCKED.md` with the failing output: a gate that won't converge means the task is misunderstood or the ground is broken, and grinding on it unattended burns usage without progress. The same cap applies to Step 7's post-review fix gate.
5. **A `loop` run is capped too, by cycle count and by any one cycle's own stop.** See Step 9. The same reasoning as hard rule 4 applies one level up: an unbounded outer loop outruns your ability to review its output.

## Step 0: Parse arguments

Strip a trailing `loop` (optionally followed by an integer `N`) from `$ARGUMENTS` before forwarding the rest. The remainder forwards verbatim to `next-task-suggest` (assignee and/or focus area, same parsing rules as that skill's Step 0). No arguments is the common case: just "give me the next thing".

`loop` with no `N` defaults to **3** cycles. `loop N` sets an explicit cap. Without `loop`, this run is a single cycle exactly as before; go straight to Step 1 and skip Step 9 entirely.

## Step 1: Suggest the next task

Invoke the `next-task-suggest` skill with `$ARGUMENTS`. Take its chosen task (roadmap ID, description, dependencies) as this run's target. If `next-task-suggest` reports no ready candidate (empty candidate set, or an assignee filter matched nothing), stop here; write `BLOCKED.md` (Step 8) rather than picking arbitrarily.

**The run's only gate:** present the chosen task (ID, description, dependencies, the signals that drove the pick) and **await the user's approval before touching anything**. A veto ends the run cleanly; offer `next-task-group` so they can choose manually. Everything after this gate runs unattended to completion.

Cross-check the chosen task's `dependsOn` against `roadmaps.json` directly: every dependency must show `status: done`. `next-task-suggest`'s `ready` set should already guarantee this, but this is the hard-rule-3 checkpoint: if anything is unmet, stop and write `BLOCKED.md` now, before touching git.

Then check whether any `done` dependency is **still unmerged**: read its `pr` field (recorded by Step 6 of the run that shipped it; see `roadmap-conventions.md`) and `gh pr view {pr} --json state,headRefName`, falling back to `gh pr list --state open` matched on the task-derived branch name when no `pr` field exists. An open PR makes that dependency the task's **stacking parent**: Step 2 branches from its head branch instead of `main`. More than one stacking parent is fine only when they lie on a single existing chain (each is an ancestor of the next; branch from the topmost); parents on separate chains cannot form a linear stack, so stop and write `BLOCKED.md`. Likewise stop if the parent already sits at stack depth 3: this run never stacks deeper (see the reference's depth rule).

**Which `roadmaps.json` this step reads:** a standalone run reads the main checkout's. Within a `loop` run, cycle N reads the copy at the tip of the *previous cycle's branch* (that's where the loop's `done` marks and `pr` fields live; the main checkout won't see them until the PRs merge). The simplest mechanics: run Step 1 from the previous cycle's worktree, or `git show <prev-branch>:.claude/roadmaps.json` from anywhere.

## Step 2: Worktree and branch

1. `git status` on the main checkout; confirm it's clean enough to branch from (uncommitted work here is the user's, not this task's; if present, stop and write `BLOCKED.md` (Step 8) rather than assuming it's abandoned; an unattended run never asks mid-flight).
2. Derive a branch name from the task: `<prefix>/<short-description>` per the branch-naming convention (`feat/`, `fix/`, `enhance/`, `refactor/`, `test/`, `docs/`, `config/`; pick the prefix from the task's nature). Check it doesn't already exist (`git branch --list`, `git worktree list`) before creating; reuse rather than duplicate if it does.
3. Create the worktree: `git worktree add <path> -b <branch-name> [<start-point>]` (path convention: sibling directory, e.g. `../<repo>-worktrees/<branch-name>`, or the project's existing worktree convention if `git worktree list` shows one already). The start-point defaults to the main checkout's HEAD; **when Step 1 found a stacking parent, pass the parent's branch as the start-point** so this branch carries the parent's code. Note which case applies; Step 6 needs it.
4. Install dependencies inside the new worktree before doing anything else there: `git worktree add` never carries over `node_modules` (it's gitignored), so skipping this produces confusing false-positive failures (missing-module errors, generated-config-dependent path aliases like SvelteKit's `$lib` failing to resolve) that look like real bugs but are just a bare worktree. Use the project's package manager (`bun install` / `npm install` / etc, per the ecosystem preference order) and, if the project has a codegen step its own tooling depends on (e.g. `svelte-kit sync`), run that too before trusting any test/typecheck output from this worktree.
5. All subsequent steps operate inside this worktree, not the main checkout.

## Step 3: Implement with tests

1. Implement the task as described in `roadmaps.json` / the PHASE file entry. Follow the project's existing conventions (read nearby code before writing) rather than this file's general style defaults where the two differ.
2. Write tests alongside the implementation; this is in-scope by default per testing convention, not an optional extra.
3. Discover the project's test, typecheck and lint commands from `package.json` scripts (or the equivalent for the project's ecosystem) rather than guessing flags.
4. Run all three (full test suite, typecheck, lint) and iterate until every one is green. Do not silence or skip a failing check; fix the underlying issue. If a failure traces back to something outside this task's scope (pre-existing breakage unrelated to the change), stop and report it rather than expanding scope to fix it unasked: this is a "flag assumptions" moment, not a "guess and proceed" one.
5. Re-run all three together once more after the last fix, to catch cross-check regressions (a lint fix that breaks a test, etc).

## Step 4: Roadmap sync

Invoke the `roadmap-maintain` skill (plain status-sync run, not `reconcile`; this task's completion is already known and explicit, not something to infer from a codebase scan) to mark the shipped task `done` in `roadmaps.json` and propagate to the PHASE file, the Mermaid diagram, `ROADMAP_OVERVIEW.md` and the HTML artefact. This is the only sanctioned way any of those projected files change; never hand-edit them in this step or any other.

Confirm its Step 7 validation report comes back clean before continuing.

## Step 5: Commit

Commit the implementation and the `roadmaps.json` change (plus its synced projections) using Conventional Commits (`type(scope): description`), split into granular thematic commits rather than one giant commit; typically one or more commits for the implementation/tests, one for the roadmap sync. Flag any breaking-change signal (removed/renamed exports, changed signatures, schema/API/env changes) with a `BREAKING CHANGE:` footer or `!` per the breaking-change convention; do not silently omit it.

Every commit passes through the global `commit-msg` hook (British spelling, no em dashes, no Oxford commas). If `git commit` exits non-zero and stderr contains `commit-msg:` lines, read each `L<n> <rule>: <excerpt>` line, rewrite the message to clear every hit (keeping the meaning) and retry the commit once. If the retry fails too, stop and write `BLOCKED.md` (Step 8) with the hook's stderr verbatim: nobody is watching this run, and a message that fails twice needs a human. Never pass `--no-verify` and never change git config to get past the hook.

## Step 6: Open the PR

Invoke the `pr-create` skill from this branch with the `auto` token: the user's veto already happened at task selection, so the PR is created without a second pause. When Step 2 branched from a stacking parent, also pass `base <parent-branch>` so the PR opens as a stacked layer, and `pr-create` links it into the parent's stack: `gh stack link <stack#> <new-pr-number>` appends it to the top of an existing stack, and `gh stack link <parent-pr-number> <new-pr-number>` starts one when the parent is not in a stack yet. Capture the PR URL/number.

Then record the PR number on the task in `roadmaps.json` as its `pr` field (a direct edit of the source file is fine; hard rule 1 forbids hand-editing the *projections*, not the source), commit it (`chore(roadmap): record PR for <task-id>`) and push. This field is what lets a later run detect this task as a stacking parent while its PR is open.

## Step 7: Self-review and fix

1. Invoke `pr-review` against the PR just opened. It posts a real GitHub review (inline comments + verdict); let it run its full methodology (via `pr-review-dry_run` underneath) rather than re-deriving findings here. The PR's author is this run's own login, so GitHub only accepts a comment review: pr-review posts the verdict as the first line of the review body instead of as an approve/request-changes event.
2. Read back the posted findings. Anything marked actionable and correctness/quality-bearing (not stylistic bikeshedding, not a finding the review itself flags as low-confidence) gets fixed in a **follow-up commit** on the same branch; never amend the commits already reviewed.
3. Re-run the full test/typecheck/lint gate (Step 3.4) after the fix commit, same bar: all green.
4. Push the follow-up commit, then re-invoke `pr-review` once so the newest review's verdict line reflects the fixed state rather than leaving a pre-fix "Request Changes" as the PR's last word from this run. Findings from this second review are reported in the final summary, never fixed in this run: one fix cycle per run is the cap.

## Step 8: BLOCKED.md (only if a hard rule triggers a stop)

Written to the repo root (main checkout, not the worktree, so it survives worktree cleanup) when Step 1's dependency check, Step 2's dirty-tree check or any other genuinely unresolved ambiguity stops the loop. Never write this file speculatively: only on an actual stop.

```markdown
# BLOCKED on <task ID>: <short description>

**Stopped at:** Step <N>, <step name>
**Reason:** <what's unmet: a specific dependsOn ID not done, an ambiguous requirement, a pre-existing test failure unrelated to this task, etc.>

## What was checked
<the specific evidence: dependsOn IDs and their actual status from roadmaps.json, the git status output, the failing check output, etc.>

## What would unblock this
<the concrete next action: "mark TASK-4 done first", "resolve the ambiguity in roadmaps.json's notes field for this task", "a human decision on X">
```

Report the file's location and a one-line summary; do not attempt to guess past the blocker.

## Step 9: Loop (only when `loop` was passed in Step 0)

After Step 7 completes a cycle (PR opened, self-reviewed, fixed once), check whether to run another cycle. Stop when **any** of these holds, and report which one fired:

1. The cycle count reaches the cap (`N`, default 3).
2. `next-task-suggest` returns an empty ready-set on the next cycle's Step 1.
3. Any cycle wrote a `BLOCKED.md` (Step 1's, Step 2's or Step 3/7's gate-cap stop).
4. A cycle's gate failed to converge within its 6-round cap (this is the same event as condition 3's gate-cap case, named separately because it's the one worth calling out in the final report as a "the ground was broken" stop rather than a clean exhaustion of ready work).

If none fire, start the next cycle from Step 1: **the approval gate re-fires every cycle.** A `loop` run never skips the veto; it only removes the need to re-invoke the skill by hand between cycles. Each cycle picks its task, worktree and branch independently, exactly as a standalone run would, with two loop-specific twists from Step 1: the roadmap is read from the previous cycle's branch tip, and a task depending on an earlier cycle's still-open PR stacks on that cycle's branch. The stack the loop builds merges bottom-up later via `pr-land`, one layer at a time or all at once.

Report at the end of the whole `loop` run: how many cycles completed, which stop condition ended it and the PR for each cycle that shipped.

## Red flags

**Never:** hand-edit the PHASE file, Mermaid block, `ROADMAP_OVERVIEW.md` or HTML artefact directly: `roadmap-maintain` only. **Never:** `git stash` without checking `git status` and `git stash list` first. **Never:** invent a resolution to an unmet dependency or genuine ambiguity: write `BLOCKED.md` instead. **Never:** push with a red test/typecheck/lint gate. **Never:** amend a commit `pr-review` already reviewed; fix findings in a new commit. **Never:** skip `pr-create`'s own approval pause for the PR description. **Never:** branch a dependent task from `main` while its parent's PR is unmerged; stack on the parent branch or stop. **Never:** `git commit --no-verify` or `-c slop.commitMsg=off`; a rejected message gets rewritten once, then the run stops.

<raw-arguments value="$ARGUMENTS" />
