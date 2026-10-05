---
name: subagent-conflict-detection
description: 'Use before dispatching a subagent with `isolation:"worktree"`, or while another subagent is in flight, to avoid three dispatch hazards — file-scope overlap with an in-flight subagent, a stale dispatch base, and collisions with another live agent/session editing the same checkout or git-submodule path. Invoke when about to call the Agent tool with `isolation:"worktree"`; when another subagent is running; right after a merge or branch switch; or when another Claude session is editing a shared repo/submodule path. Does NOT cover PR / merge mechanics (github-contribution-workflow) or post-commit diff sanity (pr-diff-verification).'
allowed-tools: Bash(git worktree *) Bash(git status *) Bash(git log *) Bash(git rev-parse *) Bash(git merge-base *)
---

# Subagent Conflict Detection

## Native mechanism

Claude Code's own isolation primitives are the [Subagents](https://code.claude.com/docs/en/subagents) feature ("each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions") and `isolation:"worktree"`'s [base-branch selection](https://code.claude.com/docs/en/worktrees#choose-the-base-branch). Neither one checks whether a NEW dispatch's file scope overlaps an in-flight one, or whether the worktree base is stale — that pre-flight discipline is what this skill adds on top.

- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

## When to invoke

Before dispatching a new subagent via the Agent tool — especially with `isolation: "worktree"` — if ANY other subagent is currently running or has an active worktree.

Trigger phrases / situations:
- "派 subagent" / "dispatch a subagent" / "再派一個" while a prior subagent is in flight
- About to call `Agent` tool when `git worktree list` shows non-main worktrees
- Multiple `[in_progress]` tasks in TaskList that involve subagent work

Skip when: dispatching the first subagent in a session, or all prior subagents have completed AND their worktrees are cleaned/merged.

## The pattern (3-step pre-dispatch check)

### Step 1 — inventory in-flight subagents

```bash
git worktree list --porcelain | grep '^worktree ' | cut -d' ' -f2- | tail -n +2
```

Plain `git worktree list` is fine for a human to eyeball, but don't parse it: filtering
on `[main]` breaks when the default branch isn't named `main`, and splitting on
whitespace breaks on a path containing a space — `cut -d' ' -f2-` keeps everything after
the first space instead of splitting on every space, so it doesn't have that problem.
`--porcelain` sidesteps the `[main]`-name issue — `tail -n +2` drops the first
(main-checkout) `worktree` line. For each remaining worktree path,
capture:
- Branch checked out
- Dirty files: `(cd <path> && git status --short)`
- Most recent commit subject: `(cd <path> && git log -1 --format=%s)`

Expect one permission prompt per worktree for these two checks, whichever form you write
them in. Per the [permissions docs](https://code.claude.com/docs/en/permissions), a Bash
rule "must match each subcommand independently"; `git -C <path> status` is a different
invocation form that `Bash(git status *)` doesn't match; and `cd` combined with `git`
"prompts when the `cd` changes into a different directory, since running `git` in a new
directory can execute that directory's hooks". So this skill's `allowed-tools` covers the
Step-1 listing (`Bash(git worktree *)`) but not the per-worktree checks — the prompt is
expected; approve it.

### Step 2 — enumerate the NEW dispatch's likely file scope

Read the planned subagent's task prompt. Extract:
- Explicit file paths it'll edit (usually under the prompt's `## Task scope` and `## Inputs` sections — see `leader-developer-handoff-contract`)
- Likely-touched files via the task domain (e.g. "Settings redesign" → `Sources/.../Settings/`)
- Test files it'll add or modify

### Step 3 — compute intersection

For each in-flight subagent's dirty-file set vs the new dispatch's likely scope:
- **Direct overlap** (same file path): BLOCK dispatch, surface to user. Options: serialize (wait for in-flight to merge) OR carve scopes (rewrite new dispatch's prompt to exclude overlapping files).
- **Module overlap** (same target directory but different files): WARN but allow with `isolation: "worktree"`. Note in dispatch prompt: "in-flight subagent X is editing target Y; do not touch files Z."
- **No overlap**: dispatch safely.

### Non-file exclusive resources also conflict

The intersection check above only reasons about file paths, but a **booted Simulator** is
just as exclusive a resource as a file: pre-assign a UDID per subagent in the dispatch prompt
rather than letting each agent boot/pick one implicitly. Some `simctl` settings are **device-global**,
not per-app — `xcrun simctl ui <udid> appearance|content_size` changes the whole device's state,
so agent A switching to dark mode or Dynamic Type contaminates agent B's screenshots if they
share a simulator (see `apple-dev-skills:interactive-simulator-ux-audit` for the driving pattern this protects).

## Pre-dispatch base correctness (verify the worktree base before you dispatch)

`isolation: "worktree"` does **not** always branch from your current local HEAD — the base
depends on `worktree.baseRef` (`"fresh"` vs `"head"`), and a resumed agent can drift off its
starting branch. **Before dispatching, confirm the base:**

```bash
git rev-parse --abbrev-ref HEAD          # on the branch you think you are?
git log --oneline -3                     # does it include the commit/PR this work depends on?
git merge-base --is-ancestor <dep-sha> HEAD && echo "base OK" || echo "STALE BASE"
```

For the `baseRef` decision table, the sync-before-dispatch recovery recipe, the real incident
that motivated this check, and the two resumed-agent traps (stale `pwd`/branch, ghost index
entries), see `references/worktree-base-and-recovery.md`.

## Coexisting with another live agent / session on the same repo

When ANOTHER Claude session (or human) is actively editing the same working checkout — or a **git submodule** vendored into your repo (e.g. a shared `.claude/skills/<plugin>` submodule) — do NOT edit that shared checkout in place. Two writers on one working tree clobber each other's uncommitted edits, fight over branch HEAD, and produce confusing diffs.

Instead, collaborate through isolation + PR:

1. Add your own worktree of THAT repo, branched from its `origin/main` (not the shared checkout's possibly-dirty local state):
   `git -C <shared-repo-or-submodule-path> fetch origin && git -C <…> worktree add /tmp/<name> -b <branch> origin/main`
2. Make your edits in the isolated worktree.
3. Commit, push the branch, open a PR on that repo. Let the normal review/merge flow integrate it.
4. For a submodule: after the upstream PR merges (and is tagged, if the consumer pins tags), bump the submodule pointer in the consuming repo via a SEPARATE PR — never hand-edit the submodule's checked-out files from the parent repo.

This is the cross-session mirror of the within-session conflict check: same goal (no two writers on one tree), different scope (independent sessions / submodules rather than your own in-flight subagents). When unsure whether another agent is on a path, treat it as occupied and use the worktree+PR path — it's cheap insurance.

## Output format

When overlap detected, present to user:

```
⚠️ Conflict detected between new dispatch and in-flight subagent:

In-flight: <subagent-id> editing:
  - <file 1>
  - <file 2>

New dispatch would touch:
  - <file 1>  ← OVERLAP
  - <file 3>

Options:
1. Serialize — wait for in-flight to merge, then dispatch
2. Carve — rewrite new dispatch prompt to exclude overlapping files
3. Proceed anyway — risk: subagent commits compete on push
```

## Anti-patterns this prevents

- **Parallel-dispatch race**: Two subagents on isolated worktrees edit the same file. `--force-with-lease` does NOT silently overwrite — it rejects the push when the remote ref has moved since the client last fetched. The real footgun is a different one: worktree B rebases onto a stale base (e.g. the main SHA from before worktree A pushed), producing a divergent history; resolving it then requires a force-push that can drop worktree A's commits. Prevent this by serializing or carving scopes before dispatch.
- **Lost-work on worktree wipe**: Subagent A's worktree wipes without commit; subagent B's dispatch reuses the path or branch name; A's work is unrecoverable.
- **Code Reviewer confusion**: CR sees a PR whose diff includes changes from a parallel subagent that's not yet merged; verdict is on wrong baseline.

## Pre-flight discipline this skill adds

If your Leader runs a pre-dispatch pre-flight (process cleanup, rebase onto main, tool trust), insert this conflict-detection step before it. For why `mise trust` is required before `mise install`/`mise exec` take effect in a fresh worktree or CI checkout, see `apple-dev-skills:mise-tool-management`.

## False-positive handling

If `git worktree list` shows stale entries (worktree dir gone but git registration alive), they are NOT a conflict source — they just need `git worktree prune`. Don't block dispatch on stale registrations; check `ls <worktree-path>` to confirm the directory actually exists before computing dirty-file intersection.

## Example application

```
Leader is about to dispatch: "Developer for error funnel refactor — files: Sources/App/Composition/Live.swift, Sources/App/Root/RootViewModel.swift, Tests/RootViewModelTests.swift"

`git worktree list` shows in-flight subagent `agent-abc123` editing:
  M Sources/App/Components/BannerController.swift

Intersection: Module overlap (same `Sources/App/`, different files) → WARN.

Verdict: dispatch with `isolation: "worktree"`. Note in prompt: "in-flight subagent on BannerController.swift — do not touch that file; module Sources/App/ is shared."
```

## Related skills

- `github-contribution-workflow` — routes worktree/submodule collision questions here; that skill owns PR/branch mechanics, this one owns pre-dispatch and cross-session conflict checks.
