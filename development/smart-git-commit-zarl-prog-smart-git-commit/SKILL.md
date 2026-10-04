---
name: smart-git-commit
description: >
  Use this skill for ANY git operation — commits, pushes, PRs, releases,
  or version tagging. Triggers on: "commit", "push", "save my changes",
  "create a PR", "open a pull request", "ship this", "make a release",
  "tag this version", "checkpoint my work", or any request to record or
  publish code changes. Produces gold-standard commits using a unique
  5-part format (CONTEXT/CHANGE/WHY/IMPACT) that is more useful and
  human-readable than any other agent's default git behavior. Includes
  secret scanning, test gating, atomic splitting, issue linking, PR
  creation, and release tagging. Use aggressively whenever git is involved.
---

# Smart Git Commit Skill

Produces gold-standard Git commits: tested, atomic, secure, documented, and
traceable. Follow every phase below in order. Never skip phases unless the
user explicitly says so.

<!-- line-limit: 500 -->

---

## Phase 0 — Read Project Rules

Check for CLAUDE.md, .gitmessage, .git/COMMIT_TEMPLATE at repo root.
If found, those rules override this skill's defaults.

```bash
cat CLAUDE.md 2>/dev/null && echo "→ Found CLAUDE.md"
cat .gitmessage 2>/dev/null && echo "→ Found .gitmessage"
```

Show what rules were loaded before proceeding.

---

## Phase 1 — Diff Analysis

Run full diff analysis before touching `git add`:

```bash
git status
git diff --stat          # which files, how many lines
git diff                 # full diff for small changesets
git log --oneline -5     # recent commit context
```

Categorize every changed file:

| Path pattern | Category |
|-------------|----------|
| `src/` `lib/` `app/` | feature/fix/refactor |
| `tests/` `*.test.*` | test |
| `docs/` `*.md` | docs |
| `package.json` deps | chore |
| `.github/` `Makefile` | tooling |

If files span more than one category → flag for atomic split in Phase 4.
Read `references/atomic-patterns.md` if split is needed.

---

## Phase 2 — Security Scan (Never Skip)

Run the automated security scanner:

```bash
bash scripts/scan-secrets.sh
```

- **Exit 0** → show "✓ Clean" and continue
- **Exit 1** → **HARD STOP**. Show findings. Do not proceed until clean.

If secrets found:
1. `git reset HEAD <file>` to unstage
2. Replace with env var or placeholder
3. Add to `.gitignore` if needed
4. Rotate exposed credentials if already pushed

Read `references/security-rules.md` for the full pattern list.

---

## Phase 3 — Test Gate (Never Skip)

Auto-detect and run the project's test suite:

```bash
bash scripts/detect-test-runner.sh
```

- **status = "pass"** → show test count and continue
- **status = "fail"** → **HARD STOP**. Fix failures first, then commit fix + feature together.
- **status = "not_found"** → warn user, ask if they want to proceed anyway

Supported runners: npm test, pytest, cargo test, go test, make test,
rspec, mix test, gradle, ctest.

---

## Phase 4 — Atomic Split Decision

If Phase 1 found multiple concerns:

```bash
bash scripts/split-commits.sh
```

Show the proposed split plan. Execute each commit group in sequence
(Phases 5-7 repeat per group).

If single concern: proceed directly to Phase 5.

Read `references/atomic-patterns.md` for splitting strategies.

---

## Phase 5 — Commit Message Construction

Use the **5-part format** for every commit. No exceptions.

```
<type>(<scope>): <imperative summary — max 72 chars>

CONTEXT: <what state existed BEFORE this change — past tense>
CHANGE:  <exactly what was done — present tense, specific>
WHY:     <business or technical reason — not obvious from the code>
IMPACT:  <what this enables/unblocks, or "No breaking changes">

<footers>
```

### Summary line rules

- **Imperative mood**: "add" not "added", "fix" not "fixing"
- **No period** at end
- **Under 72 characters**
- **Types**: `feat` `fix` `perf` `security` `refactor` `test` `docs` `chore` `hotfix` `revert` `release`

### Field rules

| Field | Rule | Good | Bad |
|-------|------|------|-----|
| CONTEXT | Past tense, describes the gap | "Auth tokens had no expiry" | "There was a bug" |
| CHANGE | Present tense, specific | "Adds 15-min sliding expiry with refresh rotation" | "Fixed the token thing" |
| WHY | Not obvious from code | "Required for SOC2 compliance" | "To improve security" |
| IMPACT | Downstream effect | "Enables audit logging of token refresh events" | "Things are better now" |

### Example

```
fix(payments): prevent double-charge on Stripe webhook retry

CONTEXT: Stripe delivered webhooks twice under high load due to 30s
         application timeout, causing duplicate charges.
CHANGE:  Adds idempotency_key (order_id + unix_ts hash) to all Stripe
         charge requests.
WHY:     Stripe's API natively deduplicates on idempotency keys — simpler
         than Redis-based deduplication.
IMPACT:  Eliminates billing support tickets for duplicate charges.

Closes #301
```

Read `references/message-examples.md` for 15 full examples.

---

## Phase 6 — Issue and Ticket Linking

Auto-detect from branch name:

```bash
git branch --show-current | grep -oE '[0-9]+'
```

Check for open issues:

```bash
gh issue list --state open 2>/dev/null | head -20
```

Use the correct footer keyword:

| Footer | Intent |
|--------|--------|
| `Closes #N` | Fully resolves (auto-closes on merge) |
| `Fixes #N` | Bug fix (same as Closes) |
| `Refs #N` | Related but does not close |
| `Part of #N` | One commit in a larger effort |

If no issue found, ask user before proceeding.

---

## Phase 7 — Execute Commits

Stage selectively — never `git add .` blindly:

```bash
git add <specific files or directories>
git diff --cached --stat   # verify before committing
git commit -m "<subject>" \
  -m "CONTEXT: ...
CHANGE:  ...
WHY:     ...
IMPACT:  ..." \
  -m "<footers>"
git show --stat HEAD       # confirm after
```

---

## Phase 8 — Push Strategy

Never push directly to `main` or `develop`. Always push to feature branch:

```bash
git push origin HEAD
git push --set-upstream origin <branch>   # if new branch
```

Show commits being pushed:

```bash
git log --oneline origin/main..HEAD
```

---

## Phase 9 — PR Creation

If on a feature branch after push:

```bash
bash scripts/create-pr.sh
```

- Always creates as **draft** — user promotes when ready
- Show PR URL after creation

---

## Phase 10 — Release Tagging

Triggers on: "release", "ship", "version bump", "tag this"

```bash
bash scripts/generate-changelog.sh
```

Then:
1. Read current version from `package.json`, `pyproject.toml`, `Cargo.toml`
2. Bump version in the appropriate file
3. Commit: `chore(release): bump version to vX.Y.Z` (with 5-part format)
4. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. Push: `git push && git push --tags`

Read `references/release-workflow.md` for full semver guide.

---

## Quick Reference

| Scenario | Start at Phase |
|----------|---------------|
| Single clean commit | Phase 1 |
| Secret found | Phase 2 → fix first |
| Tests failing | Phase 3 → fix first |
| Mixed concerns in diff | Phase 4 |
| Already staged, need msg | Phase 5 |
| Need to push + open PR | Phase 8 |
| Release / version bump | Phase 10 |
| Hotfix on main | Phase 0 → check rules |
