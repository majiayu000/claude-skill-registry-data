---
name: upgrade-dependencies
description: upgrade frontend dependencies, backend dependencies, or mise tools through parallel worker tasks
argument-hint: "npm|gem|mise [major]"
disable-model-invocation: true
---

you are the orchestrator. worker tasks own the dependency changes and PRs

- task: the worker that owns 1 group. codex: a new thread visible in its desktop app. claude code: a desktop session, or a sub-agent as the fallback, per step 3

the prompt names the ecosystem, `npm`, `gem`, or `mise`. its branch file, [`npm.md`](npm.md), [`gem.md`](gem.md), or [`mise.md`](mise.md), holds everything ecosystem-specific for you and the workers; read it and [`worker.md`](worker.md) before step 1

modes:

- default: non-major moves only. a dependency whose only newer stable releases are new majors is major-only: reported, never dispatched
- `major` in the prompt: major-only dependencies only, each in a task of its own; non-major moves are out of scope

1. inventory direct dependencies
   - inspect the manifests and lockfile per the branch file without changing files
   - the desired version is the newest stable release the mode and the version ceilings below allow, whether or not the current constraint allows it
   - if a package manager or repository release-age policy blocks the desired version, target the newest earlier stable release in scope that has aged past the cap
   - follow the branch file's manifest policy and read the comment above a line before moving it; a comment that pins for a bug means the worker must confirm the bug fixed before moving

   complete when every direct dependency is current, a candidate, out of the mode's scope, or non-registry-managed

2. group candidates
   - non-major candidates: the branch file's groups; keep coupled families in 1 group; resolve ambiguity into `everything-else`
   - major candidates: 1 group per dependency. a coupled family (a package and its runtime, plugins, adapters, `*-rails` wrapper, siblings released in lockstep) is 1 dependency; 2 candidates that constrain each other's target share 1 group

   complete when every candidate appears in exactly 1 group

3. dispatch each non-empty group
   - create 1 task per group in its own worktree; this skill is the authorisation to spawn them
   - codex: `create_thread` with a worktree environment, `gpt-6.1-sol` with high reasoning. `clientThreadId` means setup is queued and completes dispatch; retain it and resolve the task when setup finishes, with no retry or fallback for that group
   - claude code: read and follow [/claude-parallel-writers](../claude-parallel-writers/SKILL.md) with 1 writer per group. its fallback order replaces the retry and blocking rule below: a group blocks only after every fallback fails
   - retain the task for follow-up requests
   - after a creation error, reconcile the task list, `git worktree list`, branches, and PRs. retry once only after a definitive failure that left no task, PR, commits, or worktree or branch besides the one you created for the dispatch, which the retry reuses; any other failure, a failed retry, or an unknown outcome blocks the group
   - prompt it with the group, the mode, the exact list as current -> desired version, `worker.md`, the branch file, instructions to read and follow [/loop](../loop/SKILL.md), `bash bin/ensure-environment`, base branch `develop`, "never merge", "own only your branch and PR", and "return the full result plus token-efficient verification commands"
   - never include a major-only dependency outside `major` mode
   - run tasks in parallel

   complete when every non-empty group has a task and every empty group is skipped

4. wait without micromanaging
   - wait until every task finishes or needs attention; read each task's full final answer, not the truncated wait output
   - a task that surfaces a product choice is blocked: relay the choice with its context to the user and resume the task with the answer
   - enforce the scope ceiling in `worker.md`: a task growing beyond it is redirected to report the rest as follow-up work
   - if the user merges a PR mid-run, `develop` now contains it; nothing else changes

   complete when every task has finished its loop or reported its whole group as blocked

5. verify and report
   - cross-check each PR is green, mergeable, targets `develop` directly (no stacks), and stays inside its group and the scope ceiling
   - combine the open PR heads in group order in `playground/worktrees/combined` created from `origin/develop`; run `bash bin/ensure-environment` there first, then the branch file's checks
   - a lockfile conflict between 2 ready PRs is expected and cheap: after the earlier PR merges, the later one is rebased onto `develop` by its owning task inside its running loop (or by you when the task is finished) with the branch file's lockfile recipe, then diff-only review. no stacks, no rewriting another task's branch, no chasing `develop` advances that do not conflict. 1 loop per task
   - list ready PRs, accepted upgrades, and merge order; per PR every non-lockfile change with its reason and every compat setting added; per major PR also the version path, transitive dependencies that moved, call sites changed, and every behaviour change the new major introduces
   - list blocked upgrades with cause, evidence, workaround, required work, and retry condition, including the dependency that pins a target when that is the cause
   - outside `major` mode, list major-only dependencies as current -> latest major for `$upgrade-dependencies <ecosystem> major`
   - list non-registry-managed packages and transitive-dependency security advisories the workers saw once, as baseline, since no group owns them
   - combine the workers' `cream of the crop` findings as dependency -> item -> where it applies in this codebase; keep the concrete items, do not flatten them into 1 sentence

   complete when every dependency is accounted for and every PR is ready to merge in order

## version ceilings

a ceiling caps the desired version in every mode; a dependency at the newest release under its ceiling is current

npm:

- `node`, `@types/node` 24.x
- `lucide-react-v0` 0.x

gem:

- `ruby` 3.x
- bundler at the lockfile's current `BUNDLED WITH`
