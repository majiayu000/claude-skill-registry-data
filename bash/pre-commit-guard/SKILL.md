---
name: pre-commit-guard
description: |-
  Runs before every git commit on heleni-memory. Checks: no credentials in tracked files,
  no oversized files, valid SKILL.md frontmatter for any new/modified skill.
  Triggers: "commit", "before push", "validate repo", or auto-runs as a git pre-commit hook.
---

# Pre-Commit Guard

Last line of defense against the TOOLS.md class of issues.

## When to use
- Auto-run as `.git/hooks/pre-commit` (preferred)
- Manual invocation: `bash skills/pre-commit-guard/scripts/check_repo.sh`

## Checks
1. **Credential scan** — block if any tracked file matches:
   - `eyJ[A-Za-z0-9_\-]{20,}\.eyJ` (JWT)
   - `gh[ps]_[A-Za-z0-9]{36}` (GitHub PAT)
   - `xox[bp]-[0-9-]+-[A-Za-z0-9]+` (Slack)
2. **File size** — warn on files >100KB tracked under doctrine paths (`*.md` at repo root)
3. **SKILL.md validation** — for each `skills/*/SKILL.md`, require frontmatter with `name:` and `description:` fields

## Failure mode
Print failures, exit 1, block commit.
