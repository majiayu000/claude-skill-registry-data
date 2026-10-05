---
name: mk:worktree
description: Manages git worktrees for parallel agent isolation. Creates isolated worktrees for parallel agents on parallel/{name}-{timestamp} branches, merges results with conflict detection, prunes stale metadata, and reports health status. NOT for user-initiated feature branches — use git worktree directly for that.
argument-hint: '[create|merge|cleanup|list|status|prune] [agent-name]'
source: local
keywords:
  - worktree
  - git-worktree
  - parallel-isolation
  - parallel-agents
  - branch-setup
  - task-decomposition
  - orchestration
  - worktree-cleanup
  - worktree-status
  - worktree-health
when_to_use: 'Auto-invoked when orchestrator decomposes COMPLEX tasks into parallel subtasks per parallel-execution-rules.md. Manages the full worktree lifecycle: create before agents start, merge + integration-test after agents complete, cleanup after merge. NOT for user-initiated feature branches (use git worktree directly). NOT invoked directly by users.'
user-invocable: false
owner: git
criticality: medium
status: active
runtime: claude-code
---

# Git Worktree Manager

Manages git worktrees for parallel agent isolation. Each parallel agent works in its own
worktree to prevent file conflicts. Backed by `scripts/worktree.cjs`.

See `references/commands.md` for full option reference and JSON field docs.

## Actions

### create

Pre-flight: get repo info, then create a parallel worktree.

```bash
# Step 1: verify repo state
node .claude/skills/worktree/scripts/worktree.cjs info --json

# Step 2: create parallel agent worktree
node .claude/skills/worktree/scripts/worktree.cjs create "{agent-name}" --orchestrated --json
```

Before creating the first parallel worktree in a repo, verify `.worktrees/` is in `.gitignore`.
If not, append it:

```bash
echo '.worktrees/' >> .gitignore
```

The script places the worktree at `.worktrees/{agent-name}` on branch
`parallel/{agent-name}-{timestamp}` per `parallel-execution-rules.md` Rule 3.

### merge

Merge a completed parallel branch back to the feature branch using no-fast-forward:

```bash
git merge --no-ff {branch} -m "merge: parallel/{agent-name} into {feature-branch}"
```

On conflict: list conflicting files, STOP, report to orchestrator. Do NOT auto-resolve —
human or lead agent decides.

On success: run the full test suite (parallel-execution-rules.md Rule 5). After integration
test passes, delegate to `project-manager` (background):

```
"Generate delivery status for plan at {plan-dir}. Write report to
{plan-dir}/status-reports/{YYMMDD}-status.md (create subdir if absent).
Load template from tasks/templates/pm-status-template.md.
Run in the background — do not block the caller."
```

Skip PM delegation if `MEOWKIT_PM_AUTO=off` is set in environment.

### cleanup

Before removing a worktree, ensure the parallel agent has released its task ownership
in `mk:task-queue`. Then:

```bash
node .claude/skills/worktree/scripts/worktree.cjs remove "{agent-name}" --json
```

Never cleanup a worktree with uncommitted changes — commit or stash first.

### list

```bash
node .claude/skills/worktree/scripts/worktree.cjs list --json
```

### status

Health audit of all active worktrees (ahead/behind divergence, dirty state):

```bash
node .claude/skills/worktree/scripts/worktree.cjs status --json
```

### prune

Clean stale worktree metadata. Always dry-run first:

```bash
# Safe first-pass
node .claude/skills/worktree/scripts/worktree.cjs prune --dry-run --json
# Execute if no surprises
node .claude/skills/worktree/scripts/worktree.cjs prune --json
```

### review-pr

Create an isolated, **detached**, SHA-bound worktree from a PR head for a
high-assurance review (never mutates the user's checkout). The base remote is a
required argument — `pull/N/head` exists only on the PR's base repo, so a fork PR is
fetched from the base remote, never a fork remote. Writes a manifest to the persistent
session dir `tasks/reviews/<session>/manifest.json` (survives worktree removal) and a
`.mewkit-review.json` back-reference (ownership nonce) inside the worktree.

```bash
# Preview only (no fetch, no worktree) — validates inputs, prints the manifest
node .claude/skills/worktree/scripts/worktree.cjs review-pr --pr 123 --remote origin --session <id> --dry-run --json
# Create for real
node .claude/skills/worktree/scripts/worktree.cjs review-pr --pr 123 --remote origin --session <id> --json
```

### review-pr-cleanup

Remove a review worktree. Accepts **only a manifest path** — nothing else. Removal
proceeds only when the manifest's nonce matches the in-worktree back-reference AND the
target is a detached `.worktrees/review-pr-*` worktree (never the main checkout, never a
feature worktree). Force is allowed (review worktrees are legitimately dirty after
build/test); ownership, not cleanliness, is the guard.

```bash
node .claude/skills/worktree/scripts/worktree.cjs review-pr-cleanup --manifest tasks/reviews/<id>/manifest.json --json
# Stale-session sweep — dry-run by default; --apply to execute
node .claude/skills/worktree/scripts/worktree.cjs review-pr-cleanup --sweep --dry-run --json
```

## Gotchas

- `review-pr` worktrees are DETACHED (no branch) and owned by their manifest nonce;
  `review-pr-cleanup` refuses any worktree whose in-worktree back-reference nonce does not
  match the manifest — this is what makes cross-session deletion impossible
- Worktree creation fails if the branch name already exists — script handles this with
  BRANCH_CHECKED_OUT error; timestamps in orchestrated branches prevent collisions
- `git worktree remove` fails silently if the directory was already deleted manually —
  script checks existence first via `getWorktreeRecords()`
- Worktrees share the same `.git` — force-pushing from a worktree affects the main
  checkout (Safety Rule: NEVER force-push)
- `.worktrees/` directory must be gitignored — add to `.gitignore` before first parallel run
- Merge conflicts on `SKILL.md`/`CLAUDE.md` are common in parallel runs — always stop
  and report to orchestrator, never auto-resolve
- `mk:task-queue` ownership must be released before worktree cleanup, or the next agent
  cannot claim that task
- Max 3 active worktrees at any time (parallel-execution-rules.md Rule 2) — `status`
  command shows current count
- On macOS, paths with `:` in skill names need quoting in shell commands

## Safety Rules

- NEVER create worktrees on `main` or `master` — only on feature branches
- ALWAYS cleanup worktrees after merge (don't leave stale worktrees)
- NEVER force-delete a worktree with uncommitted changes — commit or stash first
- NEVER force-push from a worktree — it affects the shared `.git`
- ALWAYS check `.worktrees/` is in `.gitignore` before creating the first worktree
- ALWAYS release `mk:task-queue` task ownership before calling cleanup

## Integration

- Called by orchestrator (`mk:cook`, `mk:workflow-orchestrator`) when decomposing COMPLEX tasks
- Coordinates with `mk:task-queue` for task claiming and ownership enforcement during parallel runs
- Delegates to `project-manager` after merge integration test passes
  (post-phase-delegation Rule 1, background mode)
- Respects `MEOWKIT_PM_AUTO=off` — skip PM delegation when set
- Not invoked directly by users
