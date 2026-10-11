---
name: release-prep
description: Pre-release checklist for dev-team-agents — semver bump, tagging, rollback.
---

## Version Bump Strategy

| Change type | Bump | Examples |
|-------------|------|---------|
| Breaking change | **major** | Agent behavior removed, skill renamed, install path changed |
| New agent, skill, or command | **minor** | New agent file, new `/devteam:*` command, new workflow |
| Bug fix, typo, clarification, doc sync | **patch** | Broken script fixed, wording corrected, link updated |

Rule: when in doubt, prefer **patch** over minor. Prefer **minor** over major.

## Pre-Release Checklist

Run through every item before creating the tag.

### 1. Tests and Linting

```bash
bash helpers/agent-lint.sh
bash helpers/orphan-skill-scan.sh
```

Both must exit 0 with no ACTION REQUIRED lines.

### 2. CHANGELOG

- `CHANGELOG.md` has an entry for this version under `## [vX.Y.Z] - YYYY-MM-DD`
- Entry lists all changes grouped by type: Added / Changed / Fixed / Removed
- No unreleased items left in the `## [Unreleased]` section

### 3. Docs Sync

- `README.md` and `README.pt-BR.md` are in sync
- `docs/agents.md` matches the agents currently in `agents/`
- `CLAUDE.md` command table reflects all commands in `commands/`

### 4. No Debug Artifacts

```bash
grep -r "console\.log\|TODO:\|FIXME:\|HACK:\|XXX:" agents/ skills/ commands/ --include="*.md" -l
```

Output must be empty (or all matches are intentional and documented).

## Git Tag and Push

```bash
# Confirm the version
git log --oneline -5

# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Push tag
git push origin vX.Y.Z
```

Do not force-push tags. If a tag was created in error, see Rollback below.

## Post-Release Steps

1. **GitHub Release**: go to Releases → Draft a new release → select the tag → paste the CHANGELOG entry as the body.
2. **Notify stakeholders**: post in the team channel with a summary of what changed and a link to the release notes.
3. **Update `docs/reports/_index.md`** if the release changes the fingerprint baseline.

## Rollback Strategy

### Delete a bad tag (before others have pulled it)

```bash
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z
```

### Hotfix after a bad release

```bash
git checkout -b hotfix/vX.Y.Z+1 vX.Y.Z
# apply fix
git tag -a vX.Y.Z+1 -m "Hotfix release vX.Y.Z+1"
git push origin hotfix/vX.Y.Z+1 vX.Y.Z+1
```

Open a PR from `hotfix/vX.Y.Z+1` into `main`. Do not skip review.
