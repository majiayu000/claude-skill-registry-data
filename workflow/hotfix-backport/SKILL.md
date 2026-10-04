---
name: hotfix-backport
description: Backport fixes from main onto release/YYYY.WW in the ai repo with cherry-pick and rebase merge so release-please changelogs stay correct. Use when hotfixing a release branch, cherry-picking to release/*, or preparing a release backport PR.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: release
---

# Hotfix backport to `release/*`

## Workflow

1. Identify commits on `main` to backport (merge commits or PR numbers).
2. Branch from the target release branch:
   ```bash
   git fetch origin main release/YYYY.WW
   git checkout -b hotfix/UN-XXXXX origin/release/YYYY.WW
   ```
3. Cherry-pick in order (oldest first):
   ```bash
   git cherry-pick <sha1> <sha2> ...
   ```
4. Open a PR targeting `release/YYYY.WW` with a list of backported commits/PRs in the description.
5. Merge with **Rebase and merge** only (squash is blocked by branch rules).

## CI guardrails

- `.github/scripts/check-release-lineage.sh` — each PR commit must be on `main` or patch-equivalent (`git cherry -` prefix). Cherry-picks get new SHAs; identical hashes are not required. No commit-metadata bypass (author/subject are forgeable).
- `release-please--*` PRs skip lineage in `ci.yaml` (automation-owned version/changelog bumps).
- Do not squash-merge: one squashed commit breaks release-please changelog generation.

## After the fix PR merges

release-please opens `chore: hotfix release/YYYY.WW to YYYY.WW.N`. Approve and **rebase-merge** that PR too. PyPI publish follows the GitHub Release event.

## Related

- `release-process` — versioning and changelog ownership
- `git-conventional-commits` — commit subjects on cherry-picked commits must stay conventional
- `model-deployment` LESSONS-LEARNED — monorepo pins after AI packages ship
