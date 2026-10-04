---
name: release-cut
description: 'Composite skill — promote the long-lived `release` branch to `main`, cut a single version that batches every PR accumulated since the last tag, then clean up. Chains pr-merge-readiness (on release→main PR) → version-bump (semver from commits) → changelog-update (promote [Unreleased] → versioned) → ship (tag + GitHub release) → stale-branch cleanup → optional ship-it for deploy. Use this INSTEAD of releasing every small fix individually. Many small commits become one well-scoped release.'
user-invocable: true
auto-invoke: 'manual only, BUT nudged by next-priority / session-bootstrap when release..main has ≥5 commits'
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/release-cut
---

# Release Cut

Take everything that has piled up on the long-lived `release` branch and cut a
single, well-scoped version. Replaces the "every tiny fix is its own release"
anti-pattern: PRs land on `release` via `/pr-to-release`, then `/release-cut`
batches them.

This composite never auto-fires. It only fires when the user explicitly invokes
it. Other workflows may **nudge** the user that it is time:
- `next-priority` and `session-bootstrap` should surface a one-liner when
  `git rev-list --count main..release` returns ≥ 5
- `/pr-to-release`'s reconciliation block prints the same nudge

## Preconditions (hard-fail if any miss)

1. `release` branch exists on origin
2. `main` is fully merged into `release` (no divergence the other way)
3. CHANGELOG.md contains an `[Unreleased]` section with at least one entry
4. Working tree is clean
5. No open release-train PR already (`gh pr list --base main --head release`)

## Workflow

### Phase 1 — Inventory (always)
```bash
git fetch origin --quiet
COMMITS=$(git rev-list --count main..release)
PRS=$(git log main..release --merges --pretty=%s | wc -l | tr -d ' ')
LAST_TAG=$(git tag --sort=-version:refname | head -1)
```

Show: count of commits, count of merged PRs, last tag, list of PR titles, current
`[Unreleased]` entries.

If `COMMITS == 0`: STOP with "Nothing to release. `release` is at the same point as `main`."

### Phase 2 — Semver decision
Invoke `version-bump` in **dry-run** mode to propose patch / minor / major from
conventional commit history. Surface the proposal to the user; ask for override
only if any commit is marked `BREAKING CHANGE` and the proposal is not major,
or if the user explicitly requested a different bump.

### Phase 3 — Promote changelog
Invoke `changelog-update` in **promote mode**: move `[Unreleased]` content under
a new `[X.Y.Z] - YYYY-MM-DD` header, re-add an empty `[Unreleased]` skeleton on
top. The promotion happens on a **dedicated branch** (`chore/release-vX.Y.Z`)
forked from `release`, not directly on `release`.

### Phase 4 — Open the release-train PR
- Base: `main`
- Head: `chore/release-vX.Y.Z` (which already contains every commit from `release`
  plus the changelog promotion + version bumps)
- Title: `chore(release): vX.Y.Z`
- Body: full `[X.Y.Z]` section copied verbatim from the new CHANGELOG, plus a list
  of every PR being shipped (`git log main..HEAD --merges --pretty='- #%h %s'`).

### Phase 5 — Gate the train PR
Invoke `pr-merge-readiness` against the release-train PR. Treat it like any
other PR: CI must be green, automated reviewers must be satisfied, no human
CHANGES_REQUESTED. On WAIT or FIX, hand back to user — never auto-fix a
release-train PR; the diff is too large to rebase blindly.

### Phase 6 — Merge to main
- Method: **merge commit** (NOT squash). The whole point of the release branch is
  to preserve the individual PR shas in main's history.
- After merge: confirm `main` now contains every release commit, and the version
  in `package.json` on `main` equals X.Y.Z.

### Phase 7 — Tag + GitHub release
Invoke `ship` in tag-only mode against `main`:
- Create annotated tag `vX.Y.Z` on the merge commit
- Push the tag
- Create GitHub release using `[X.Y.Z]` section as the release notes
- Mark as `--latest`

### Phase 8 — Sync release back to main
```bash
git switch release
git merge --ff-only origin/main || git merge --no-ff origin/main -m "chore: sync release with main after vX.Y.Z"
git push origin release
```

`release` and `main` must end at the same commit. Any later PR that targets
`release` starts from a clean post-release base.

### Phase 9 — Cleanup stale branches (always)
Find branches whose tip is now reachable from `main`:
```bash
git fetch origin --prune
# Local branches gone on remote
git branch -vv | awk '/: gone]/{print $1}' | xargs -r git branch -D
# Local branches fully merged to main (excluding main/release/protected)
for b in $(git for-each-ref --format='%(refname:short)' refs/heads); do
  case "$b" in main|master|release|develop) continue;; esac
  git merge-base --is-ancestor "$b" origin/main && git branch -D "$b"
done
# Remote feature branches merged via squash (titles match closed PRs)
gh pr list --state merged --base release --search "merged:>=$(date -u -v-30d +%Y-%m-%d)" \
  --json headRefName --jq '.[].headRefName' \
  | while read -r b; do git push origin --delete "$b" 2>/dev/null || true; done
```

Show count of branches pruned locally and remotely. Never delete `main`,
`master`, `release`, `develop`, or any branch matching `release/*`, `hotfix/*`.

### Phase 10 — Deploy (optional, only if user confirms)
Ask: "Deploy vX.Y.Z now? (y/N)". On yes, invoke `/ship-it` starting at Phase 3
(deploy phase) — the version + changelog + tag work is already done.

## Stop / escalation conditions

- Release-train PR has any failing check → hand to user, do not auto-fix
- Main↔release divergence cannot fast-forward and merge produces conflicts →
  surface to user with the conflict files listed
- `[Unreleased]` is empty (no work to ship)
- Tag `vX.Y.Z` already exists (someone half-cut the release earlier)

## Reconciliation

```
RELEASE CUT — <repo> v<old> → v<new>
  Commits batched:   N (across M PRs)
  Bump:              <patch|minor|major> (proposed by conventional commits)
  Train PR:          #<n> — base=main, head=chore/release-vX.Y.Z
  Merge:             merge-commit at <SHA>
  Tag:               vX.Y.Z pushed, GitHub release published
  Sync:              release fast-forwarded to main
  Cleanup:           K local branches pruned, J remote branches deleted
  Deploy:            <deployed via /ship-it | skipped | scheduled>
```

## Outputs / Evidence

- New version + tag + GitHub release URL
- Merge SHA on `main`
- List of PRs shipped in this version (for release notes / Slack)
- Branch cleanup count
- Nudge to deploy if not already deployed

## Cadence guidance

When the nudge fires (≥5 commits on `release` beyond `main`), surface this in
session bootstrap output:
> "`release` is N commits ahead of `main` across M PRs. Worth running
> `/release-cut` to batch these into one version?"

Do NOT auto-cut. The user controls cadence; the nudge just makes the cost of
NOT cutting visible.

## What this composite is NOT

- Not a hotfix → use `/hotfix` (bypasses release branch)
- Not a per-PR ship → use `/pr-to-release` to land work on `release` first
- Not a deploy-only step → use `/ship-it` after the release is cut, if needed

## Pairs with

- `/pr-to-release` — feeds work into `release`; this composite cuts the batch
- `/hotfix` — the only acceptable bypass of this cadence
- `/ship-it` — optional Phase 10 deploy
