---
name: ddev-cleanup
description: >
  End-of-day cleanup for Grok Build + ddev projects. Repo status check, drift gate,
  ddev stop, cache/TODO update, commit and push on a feature branch, then reposition
  off master/develop for tomorrow. Use on shutdown, end of day, clean stop, daily cleanup.
argument-hint: "Optional summary for commit message, e.g. 'filament panel work done'"
user-invocable: true
disable-model-invocation: false
---

# ddev-cleanup

## Role

Perform a complete, clean shutdown of the current Grok Build + ddev project session. Enforce no project drift, verify GitHub/repo health, deliver via feature branches (never leave the workspace on `master` or `develop`), and ensure seamless resumption the next day.

## Activation

Use when the user says "end of day", "shutdown for today", "clean stop", "daily cleanup", "stop work", "push and shutdown".

## Branch policy (orchestrator template)

| Branch | EOD rule |
|--------|----------|
| `feature/*` | Commit/push here; may stay if work continues tomorrow |
| `develop` | **Never commit EOD changes directly** — create `feature/<slug>-YYYY-MM-DD` from `develop` first |
| `master` | **Never commit or remain here** — reposition to new `feature/*` from `develop` after cleanup |

Promotion flow: `feature/*` → PR → `develop` → PR → `master` (`branch-promotion-prs.yml`).

## Procedure (run in order)

### 1. Repository status check (mandatory — `/github-expert` lite)

Activate `/github-expert` or run these checks from project root:

```bash
git fetch origin --prune
git branch --show-current
git status -sb
git rev-list --left-right --count origin/develop...develop 2>/dev/null || true
git rev-list --left-right --count origin/master...master 2>/dev/null || true
gh pr list --limit 10
gh pr list --state merged --limit 5
```

**Report an EOD repo status table:**

| Check | Expected | Action if fail |
|-------|----------|----------------|
| Working tree | Clean before branch switch | Commit or stash on correct branch first |
| Current branch | Not `master` for new commits | Reposition (step 6) |
| `develop` vs `origin/develop` | In sync | `git pull origin develop` before new feature branch |
| Open PRs | None stale/blocking | Note in summary; user resolves tomorrow |
| Merged feature branches | Delete local stale | `git branch -d <name>` when merged |

Cache findings in session summary; update `docs/github/repo-health.md` when drift or recurring issues appear.

### 2. Enforce no project drift

- Activate `/project-drift-guardian` and `/branch-context-agent`.
- Align with active TODO and branch scope.
- Resolve drift before commit/push.

### 3. Branch gate before commit

If current branch is `master` or `develop`:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<slug>-$(date +%Y-%m-%d)
```

- `<slug>`: short kebab from TODO objective or user hint (e.g. `loop-hardening`, `work`).
- Move any uncommitted work onto this branch before staging.

If already on `feature/*` with aligned scope, stay.

### 4. Stop ddev environment

- Run `ddev stop` (or `ddev poweroff` if no other projects active) when `.ddev/` exists.
- Confirm with `ddev list` or `ddev describe`.
- **Template repos without `.ddev/`:** skip and note N/A.

### 5. Update Grok Build artifacts

- Refresh project cache if applicable.
- Run `python3 scripts/sync_grok_to_github_claude.py` when `.grok/` skills or prompts changed.
- Update active TODO (today closed, tomorrow opened via `/todo-specialist-agent` when chained).
- Run `bash scripts/chain-audit.sh` when `chains/registry.yaml` changed.

### 6. Git cleanup and push

```bash
git status
git add <relevant files>
git commit -m "End of day cleanup: <summary>. No project drift confirmed."
git push -u origin "$(git branch --show-current)"
```

- Open PR to `develop` when branch protection blocks direct push.
- Never push EOD commits to `master` or `develop`.

### 7. Reposition for tomorrow (mandatory if on `master` or `develop`)

After push (or when working tree is clean on a promotion branch):

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<slug>-$(date -d tomorrow +%Y-%m-%d 2>/dev/null || date -v+1d +%Y-%m-%d)
```

- Use **tomorrow's date** in the branch name when creating the next-day branch.
- Leave the workspace on this feature branch — **not** on `master`.
- Empty branch: no push required until first commit tomorrow.

### 8. Final verification

- Confirm last push succeeded (if any).
- Confirm current branch is `feature/*`.
- Suggest tomorrow: `ddev start` (if applicable), `/chain session-start` (offers resume to latest remote branch worked on), active `TODO/YYYY-MM-DD_TODO.md`.

## Idempotency

- Check before destructive actions (`git branch -D`, force push).
- If already on a suitable `feature/*` with clean tree, skip step 7.
- Safe to re-run; repo status step always runs.

## Chained use

Part of `eod-shutdown` chain (`todo-specialist` → `readme-specialist` → `ddev-cleanup`). Repo status + branch reposition are owned by this skill's steps 1, 3, and 7.

Run commands via bash tool. Always work in project root. Log each step.