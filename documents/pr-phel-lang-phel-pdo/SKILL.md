---
description: Push branch and open a PR (assigned to @me, labeled, Closes #N)
argument-hint: "[issue-number]"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(git *), Bash(gh *)"
---

# PR

## Context

!`git branch --show-current`
!`git log main..HEAD --oneline`

## Instructions

1. If `## [Unreleased]` in `CHANGELOG.md` wasn't updated, update it and commit: `docs: update changelog`.
2. `git push -u origin HEAD`.
3. Title: `<type>(<scope>): <short>` (conventional, under 70 chars). Derive type from branch prefix (`feat/` → `feat`, `fix/` → `fix`, `docs/` → `docs`, `ref/` → `ref`). If `$ARGUMENTS` is an issue number, pull the title via `gh issue view <num> --json title -q '.title'`.
4. Pick one label: `bug` (`fix/`), `enhancement` (`feat/`), `documentation` (`docs/`), `refactoring`, `pure testing`, `dependencies`.
5. Open:
   ```bash
   gh pr create --title "<title>" --assignee @me --label "<label>" --body "$(cat <<'EOF'
   ## Summary
   - <what + why, one or two bullets>

   ## Test plan
   - [ ] `composer test` green locally
   - [ ] CI green

   Closes #<issue-number>
   EOF
   )"
   ```
   Drop the `Closes` line if there's no linked issue. Body under 15 lines.
6. Report URL.
