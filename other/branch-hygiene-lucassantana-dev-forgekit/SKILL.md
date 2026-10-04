---
name: branch-hygiene
description: 'Composite skill — one-pass cleanup of stale local branches, dead worktrees, merged branches, and abandoned remote PR branches. Chains `git fetch --prune` → `clean_gone` (kill [gone] branches) → worktree prune + offer-to-remove dead worktrees → list-and-delete branches merged to main and release → delete remote PR branches whose PRs merged >7 days ago. Use instead of running `clean_gone` alone — that only catches half the rot. Daily-friction composite; fires on "clean up branches", "branch hygiene", "stale worktrees", and on session start when local branch count > 30.'
user-invocable: true
auto-invoke: '"branch hygiene", "clean up branches", "prune branches", "stale worktrees", "dead worktrees", "git is a mess", local-branch-count > 30 at session start'
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/branch-hygiene
---

# Branch Hygiene

Local git state rots faster than people notice. `clean_gone` catches branches
whose remote was deleted, but misses:

- Worktrees pointing at branches that no longer exist
- Local branches merged into `main` or `release` weeks ago
- Remote PR branches that the contributor forgot to delete
- Orphan worktree directories on External HD with no git registration

This composite handles all four in one pass with confirmation prompts at every
destructive step.

## When this fires

- User says "branch hygiene", "clean up branches", "prune branches", "dead
  worktrees", "git is a mess in this repo"
- Auto-suggest at session start when `git branch | wc -l > 30` in the active repo
- After `/release-cut` Phase 9 (which already deletes some stale branches but
  doesn't touch worktrees)
- Weekly cadence per active repo (let `/next-priority` surface it)

If the repo is not a git repo or `git` is unavailable: exit with
`branch-hygiene skipped: not a git repository`.

## Workflow

### Phase 1 — Fetch + prune (always)

```bash
git fetch --all --prune --prune-tags
```

This refreshes the remote-tracking state so subsequent phases see accurate
`[gone]` markers. No prompts; safe.

### Phase 2 — Kill [gone] local branches (skill: `commit-commands:clean_gone`)

Invoke the existing `clean_gone` skill. It already prompts before deleting and
removes associated worktrees registered with git. If it bails out (e.g.,
dirty worktree on a `[gone]` branch), record the offender in the reconciliation
block and continue — do not abort the chain.

### Phase 3 — Worktree prune + orphan sweep (composite logic)

```bash
git worktree prune --verbose
git worktree list --porcelain
```

Compare `git worktree list` output against the directory listing under
`$WORKTREE_ROOT` (default: `$HOME/.worktrees/` —
the user's storage policy). For any directory that exists on disk but is NOT
registered as a worktree:
- Confirm with user before removing (single prompt summarizing all orphans)
- `rm -rf` only after explicit confirmation
- Record paths removed in the reconciliation block

If the worktree volume is not mounted, skip the orphan sweep with
`(skipped: External HD not mounted)`.

### Phase 4 — Branches merged to main (composite logic)

```bash
git fetch origin main
git branch --merged origin/main \
  | grep -vE '^\*|^\s*(main|master|release|develop)\s*$'
```

For each candidate:
- Show: branch name, last commit date, last commit subject
- Single bulk prompt: "Delete N merged branches? (y/N/select)"
  - `y` → `git branch -d <each>` (safe delete; refuses if not fully merged)
  - `N` → skip phase, record count in reconciliation
  - `select` → enumerate and let user pick by index

Never use `-D` here. If `-d` refuses, surface that branch in the
reconciliation block as `unsafe-merge: <branch>` and continue.

### Phase 5 — Branches merged to release (skip if no release branch)

Probe: `git ls-remote --heads origin release 2>/dev/null | grep -q .`
- If no release branch: `(skipped: no release branch on origin)`, continue
- If exists: repeat Phase 4 logic with `git fetch origin release` +
  `git branch --merged origin/release`

This catches the case where a PR landed on `release` via `/pr-to-release` and
the contributor never deleted the source branch locally.

### Phase 6 — Stale remote PR branches (skill: `gh-cli`)

If `gh` is available:
```bash
gh pr list --state merged --limit 100 \
  --json number,headRefName,mergedAt,headRepositoryOwner
```

Filter to:
- `mergedAt` more than 7 days ago
- `headRefName` not in {main, master, release, develop, HEAD}
- Branch still exists on origin (`git ls-remote --heads origin <ref>` non-empty)
- PR head repo owner matches the current repo's owner (skip fork branches)

Show the filtered list, prompt once for bulk deletion. On confirm:
```bash
git push origin --delete <ref>   # per branch, swallow individual failures
```

If `gh` is missing: `(skipped: gh CLI unavailable)`.

### Phase 7 — Final state snapshot (always)

```bash
echo "Branches remaining: $(git branch | wc -l)"
echo "Worktrees remaining: $(git worktree list | wc -l)"
git branch -vv | head -20
```

These numbers go into the reconciliation block so the user sees the delta.

## Reconciliation block (mandatory output)

```
BRANCH HYGIENE — <repo>
  Fetched:         <n> branches updated, <m> tags pruned
  Gone-killed:     <n> branches (skill: clean_gone)<, unsafe-merge: <list> if any>
  Worktree prune:  <n> registered worktrees removed
  Orphan sweep:    <n> directories removed | (skipped: <reason>)
  Merged to main:  <n> deleted, <m> kept (unsafe-merge: <list>)
  Merged to release: <n> deleted | (skipped: no release branch)
  Stale PR refs:   <n> deleted | (skipped: gh unavailable)
  Delta:           <before> → <after> local branches, <before> → <after> worktrees
  Snapshot:        (none — interactive cleanup, no handoff written)
  Open watch:      (none) | <e.g. "1 unsafe-merge branch: feature/X — manually verify before -D">
```

If any phase failed mid-step, mark it `(failed: <reason>)` and continue to the
next phase. Phases are independent — failure of one does not abort the rest.

## Stop conditions

- Not a git repo → exit immediately with the skip message
- Repo has uncommitted changes on the currently-checked-out branch → run
  anyway; the destructive phases never touch the current branch
- User answers `N` to any phase's bulk prompt → record phase as
  `(skipped: user declined)` and continue
- More than 50 deletion candidates in any single phase → require explicit
  confirmation phrase (`yes, delete all <n>`) not just `y` — guards against
  catastrophic miscounts

## Configuration

Optional `.claude/branch-hygiene-config.json` in the repo root:

```json
{
  "worktree_root": "$HOME/.worktrees",
  "stale_pr_threshold_days": 7,
  "protect_branches": ["main", "master", "release", "develop", "staging"],
  "skip_phases": []
}
```

Defaults apply when the file is missing. `skip_phases` accepts phase numbers
(e.g., `[6]` to skip the remote PR sweep on a repo where the user prefers to
review those manually).

## Negative rules

- Do NOT use `git branch -D` to force-delete branches. The whole point is to
  delete what's *safely* merged; force-delete defeats the safety check.
- Do NOT skip the bulk prompt. Even when only one branch matches, the prompt
  is the contract — silent deletion is forbidden.
- Do NOT delete branches that are protected by the repo's `protect_branches`
  config OR by GitHub branch protection (probe via `gh api`); surface them
  as `protected: <branch>` instead.
- Do NOT touch worktrees outside `worktree_root`. If the user has worktrees
  elsewhere, the orphan sweep does not see them — flag this in the
  reconciliation block if `git worktree list` shows paths outside the root.
- Do NOT auto-queue another composite. This is a maintenance pass, terminal.
