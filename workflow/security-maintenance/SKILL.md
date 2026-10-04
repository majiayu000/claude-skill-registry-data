---
name: security-maintenance
description: Triage and fix Dependabot alerts and CodeQL findings in the ai repository. Use when the user asks to address security vulnerabilities, fix Dependabot alerts, resolve CodeQL issues, or do security maintenance.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "2.0.0"
  languages: python
  audience: developers
  workflow: automation
  since: "2026-04-14"
---

## What I do

I drive the security maintenance workflow for the `ai` repository to keep both dashboards at zero:

- **Dependabot** — https://github.com/Unique-AG/ai/security/dependabot
- **CodeQL** — https://github.com/Unique-AG/ai/security/code-scanning

## When to use me

- "fix dependabot", "security maintenance", "fix vulnerabilities", "dependabot alerts", "CodeQL findings"
- Periodic security maintenance sessions
- After Dependabot auto-opens PRs (we do **not** merge those directly)

---

## Release model — read first

Versions and changelogs are **fully owned by release-please** (config: `release-please-config.json`, manifest: `.release-please-manifest.json`). CI enforces this via `.github/scripts/check-no-manual-release.sh`, which **fails any PR that modifies**:

- any `CHANGELOG.md`
- `.release-please-manifest.json`
- the `version = "..."` line in any `pyproject.toml`

Because of that:

- **Never** edit `CHANGELOG.md` or bump `version` by hand. Do **not** use the `release-process` skill to justify manual edits in security PRs — that skill documents automation, not hand bumps.
- Drive the next release entries through **conventional commit subjects** (see `git-conventional-commits`). For Dependabot/CodeQL fixes use `fix(<scope>): ...` so release-please groups them under "Bug Fixes". Use `chore(deps): ...` only for risk-free dep bumps you don't want to surface in user-facing notes (it's hidden in the changelog).
- One commit per PR is fine; release-please derives bumps per workspace package from the commit subject + changed paths.

## Dependabot workflow

**Never merge Dependabot auto-PRs.** Use `constraint-dependencies` in the root `pyproject.toml` instead.

1. **List alerts** — see [gh commands reference](references/gh-commands.md). Always paginate (`gh api --paginate`); the Dependabot endpoint is cursor-paged and a single `per_page=100` call silently caps at 100.
2. **Find fix version** from the alert JSON.
3. **Add/bump `constraint-dependencies`** in root `pyproject.toml` with `"<package>>=<fixed-version>"`.
4. **Handle `exclude-newer` conflicts** — if the fix version is within the 2-week rolling window, add an `exclude-newer-package` timestamp (day after latest PyPI upload). See [exclude-newer reference](references/exclude-newer.md).
5. **Prune stale `exclude-newer-package` entries** — remove any timestamp older than 2 weeks (redundant, global window already covers it). Keep `= false` entries.
6. **Relock** — `uv lock --refresh`. If resolution fails, bump the timestamp and retry.
7. **Branch and commit** — branch `fix/dependabot-<pkg>-<ver>` (single CVE) or `fix/security-<date>` (batch). Subject: `fix(deps): bump <pkg> to >=<ver> (GHSA-xxxx)` or `fix(security): batch dependabot fixes <date>`. Do **not** touch `CHANGELOG.md` or any `version = ...` field — release-please will pick the commit up on the next standing Release PR.
8. **Open PR, then close Dependabot auto-PRs** after merge (they won't auto-close because we ship via constraints, not by merging their lockfile bump).

## CodeQL workflow

1. **List findings** — see [gh commands reference](references/gh-commands.md). Paginate the same way.
2. **Read the rule and flagged code** in context.
3. **Fix the code** — see [common CodeQL patterns](references/codeql-patterns.md).
4. **Branch and PR** — same shape as Dependabot. Use `fix(<package-or-area>): <what was hardened> (CodeQL <rule-id>)`. Again: no manual changelog/version edits.

## Batch session

1. List all Dependabot alerts and CodeQL findings (paginated).
2. Prune stale `exclude-newer-package` entries.
3. Fix Dependabot alerts (mechanical: constraints + relock).
4. Fix CodeQL findings (code changes).
5. Single branch for related fixes, separate branches for unrelated areas.
6. Commit with `fix(...)` subjects so release-please attributes bumps to the right workspace package(s) on the next Release PR.
7. Create PR(s), let CI run `check-no-manual-release.sh`, then close any resolved Dependabot auto-PRs after merge.

## Tips

- **Never merge Dependabot auto-PRs** — `constraint-dependencies` persists across relocks; auto-PRs only edit `uv.lock`.
- **Never touch `CHANGELOG.md`, `.release-please-manifest.json`, or `version = ...`** — `check-no-manual-release.sh` will block the PR.
- **Use `fix(...)` not `chore(deps): ...`** when you want the fix to appear in user-facing release notes; `chore` is hidden by the changelog config.
- **Round timestamps up** — day *after* latest artifact upload (`uv` uses strict `<` on individual wheel upload times).
- **Batch when possible** — one PR reduces noise; release-please still attributes per workspace package.
- **Prune stale timestamps** — entries older than the 2-week window are redundant.
- **Check both dashboards** — Dependabot and CodeQL are independent.
