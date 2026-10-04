---
name: repo-bootstrap
description: 'Composite skill — configure a fresh or under-configured repo for the release-branch workflow in one pass. Creates the `release` branch on origin, seeds `CHANGELOG.md` (Keep-a-Changelog format), drops in `.claude/dep-sweep-config.json` + `.claude/branch-hygiene-config.json` + a `release-cadence.md` standard stub, opens a `chore/repo-bootstrap` PR to main. Use instead of manually setting these up before the first `/pr-to-release` — without this, none of the release-branch composites can fire. Idempotent: skips any artifact that already exists. Replaces ad-hoc "set up the new repo" scripts.'
user-invocable: true
auto-invoke: '"bootstrap this repo", "set up release branch", "new repo setup", "configure release workflow", first session in a repo with no `release` branch and no `.claude/` directory'
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/repo-bootstrap
---

# Repo Bootstrap

The release-branch composites (`/pr-to-release`, `/release-cut`, `/hotfix`,
`/dep-sweep`, `/first-pr`, `/branch-hygiene`) all assume the repo is already
configured for the model — a `release` branch on origin, a `[Unreleased]`
changelog section, sensible defaults at `.claude/*-config.json`. Without that,
the first composite invocation fails or makes uninformed defaults stick.

This composite does the setup once, idempotently.

## When this fires

- User says "bootstrap this repo", "set up release branch", "new repo setup",
  "configure release workflow", "make this repo work with /pr-to-release"
- Auto-suggest on the first session in a repo where:
  - `git ls-remote --heads origin release` returns empty AND
  - `.claude/` directory is missing OR has no config files
- Queued by `/first-pr` Phase 0 if the repo is not yet bootstrapped
- After `git init` + first push to origin

If the repo is not a git repo: exit with
`repo-bootstrap skipped: not a git repository`.

If the repo has no `origin` remote: surface as a blocker and refuse — the
release branch must exist on a remote to be useful.

## Workflow

### Phase 1 — Detect state (always)

Probe without writing:
```bash
git remote get-url origin                              # must succeed
git symbolic-ref refs/remotes/origin/HEAD --short      # default branch (e.g. origin/main)
git ls-remote --heads origin release                   # release branch presence
test -f CHANGELOG.md && echo has-changelog
test -d .claude && echo has-claude-dir
test -f .claude/dep-sweep-config.json && echo has-dep-sweep
test -f .claude/branch-hygiene-config.json && echo has-branch-hygiene
test -f .claude/standards/release-cadence.md && echo has-release-cadence
```

Record into a detection summary. Every later phase reads this and skips if
its artifact already exists — idempotency is the contract.

### Phase 2 — Create `release` branch on origin (skip if exists)

```bash
git fetch origin
git push origin "origin/$(default_branch):refs/heads/release"
```

Where `default_branch` is `main` or whatever Phase 1 detected. Refuse if the
default branch has zero commits (empty repo) — surface as
`(blocked: default branch has no commits yet — push initial commit first)`.

Do NOT check out the release branch locally. The model is push-only from the
local default branch via `/pr-to-release`.

### Phase 3 — Seed `CHANGELOG.md` (skip if exists)

Create at repo root:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Fixed
### Removed
### Security
```

If CHANGELOG.md exists but has no `[Unreleased]` section, do NOT rewrite it —
flag as `(skipped: CHANGELOG.md exists but lacks [Unreleased] — manual review
needed)`. `/pr-to-release` requires the section; this is the user's call.

### Phase 4 — Seed `.claude/dep-sweep-config.json` (skip if exists)

Create `.claude/` if missing. Then:

```json
{
  "base_branch": "release",
  "sensitive": [],
  "always_hold": ["react", "next", "vue", "svelte", "@types/node"],
  "auto_merge_minor": false,
  "auto_merge_dev_deps": true
}
```

`sensitive` defaults to empty — the user fills it per-repo (e.g.,
`["stripe", "@aws-sdk/*"]`). The pattern is conservative: dev-deps auto-merge,
minors hold for review, framework packages always hold.

### Phase 5 — Seed `.claude/branch-hygiene-config.json` (skip if exists)

```json
{
  "worktree_root": "$HOME/.worktrees",
  "stale_pr_threshold_days": 7,
  "protect_branches": ["main", "master", "release", "develop", "staging"],
  "skip_phases": []
}
```

The `worktree_root` reflects the user's storage policy. If the user is on a
machine without External HD mounted, the path is still recorded — `/branch-hygiene`
will skip the orphan-sweep phase at runtime.

### Phase 6 — Stub `.claude/standards/release-cadence.md` (skip if exists)

```markdown
# Release Cadence — <repo>

How this repo ships.

## Model

Long-lived `release` branch on origin. New work lands on `release` via
`/pr-to-release`. Versions are NOT cut per-PR — they are batched by
`/release-cut` when enough has accumulated.

## Cadence triggers

- Manual: user invokes `/release-cut`
- Nudge: when `git rev-list --count main..release` ≥ 5 commits
- Hotfix exception: `/hotfix` bypasses the release branch and cuts a patch
  immediately, then cherry-picks back to release

## What goes in each version

- Patch: bug fixes, dependency patches, no behavior change
- Minor: new features, backward-compatible changes
- Major: breaking changes — requires migration notes in the CHANGELOG entry

## Bot PRs

`/dep-sweep` handles Dependabot/Renovate/pre-commit-ci. See
`.claude/dep-sweep-config.json` for the rules.

## Hotfix policy

Only acceptable bypass of `release` is `/hotfix`. Criteria documented in
~/.claude/skills/hotfix/SKILL.md. Routine "small fix" work belongs on the
release branch.
```

Replace `<repo>` with the directory name from `basename $(git rev-parse --show-toplevel)`.

### Phase 7 — Open `chore/repo-bootstrap` PR (always, if any artifact was created)

If at least one phase 2–6 produced a change:

```bash
git switch -c chore/repo-bootstrap
git add CHANGELOG.md .claude/
git commit -m "chore: bootstrap release-branch workflow

Adds CHANGELOG.md, dep-sweep + branch-hygiene config, release-cadence standard.
Release branch was pushed to origin separately (does not require this PR to merge)."
git push -u origin chore/repo-bootstrap
gh pr create --base "$(default_branch)" --title "chore: bootstrap release-branch workflow" \
  --body "$(bootstrap_pr_body)"
```

PR body must list every artifact created (or skipped + reason). This is the
audit trail for the bootstrap.

If `gh` is unavailable: push the branch and emit the `gh pr create` command in
the reconciliation block for the user to run manually.

### Phase 8 — Verify (always)

After Phase 7 (or after a fully-idempotent no-op run), re-probe:
- `git ls-remote --heads origin release` must return a SHA
- `CHANGELOG.md` must contain a literal `## [Unreleased]` line
- Each config file must parse as valid JSON

Record verification results in the reconciliation block. A failed verification
on a fresh bootstrap is a hard error — surface and stop.

## Reconciliation block (mandatory output)

```
REPO-BOOTSTRAP — <repo>
  Detection:        default-branch=<name>, release=<exists|missing>, changelog=<exists|missing>, .claude/=<state>
  Release branch:   created | (skipped: already exists) | (blocked: <reason>)
  CHANGELOG.md:     created | (skipped: exists with [Unreleased]) | (skipped: exists, lacks [Unreleased] — manual review)
  dep-sweep config: created | (skipped: exists)
  hygiene config:   created | (skipped: exists)
  release-cadence:  created | (skipped: exists)
  PR:               <url> | (skipped: no changes) | (manual: run `gh pr create ...`)
  Verify:           release-on-origin ✓, [Unreleased] ✓, configs-parse ✓
  Snapshot:         (none — bootstrap is terminal)
  Open watch:       (none) | <follow-up if Phase 3 flagged manual changelog review>
```

## Stop conditions

- Not a git repo → exit immediately
- No `origin` remote → refuse with explicit message
- Default branch has zero commits → block Phase 2; surface remediation
- Verification (Phase 8) fails after a write phase succeeded → hard error,
  rollback the local branch (`git switch -` + `git branch -D chore/repo-bootstrap`)
  if the PR push didn't happen yet; if the PR push did happen, leave it
  open and flag for manual fix

## Idempotency contract

Running `/repo-bootstrap` twice on the same repo must:
- Not duplicate any file
- Not error on existing artifacts
- Produce a reconciliation block showing every phase as `(skipped: exists)`
- Exit clean with no PR opened (Phase 7 sees zero changes)

This property is what makes the composite safe to auto-suggest at session
start — false positives cost nothing.

## Negative rules

- Do NOT overwrite an existing CHANGELOG, config, or standard. Skip and flag
  instead. The user's existing content is canonical.
- Do NOT auto-merge the bootstrap PR. It's a setup-time change that benefits
  from human review even when mechanical.
- Do NOT check out `release` locally. The model is push-only.
- Do NOT touch `.gitignore`, package.json, or any source code. Bootstrap is
  workflow configuration only — it never modifies the project itself.
- Do NOT auto-queue another composite. Bootstrap is a one-shot setup;
  cascading from it would surprise the user.
