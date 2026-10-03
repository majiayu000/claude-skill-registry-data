---
description: Push the branch and open a pull request with template body, labels, and assignee
argument-hint: "[issue-number]"
allowed-tools: "Read, Bash(git *), Bash(gh *)"
---

# Create Pull Request

## Context

!`git branch --show-current`
!`git log main..HEAD --oneline`
!`git diff main..HEAD --stat`

## Instructions

1. **Never open a PR from `main`.** If the current branch is `main`, create a branch first and move the commits onto it.

2. **Push**:
   ```bash
   git push -u origin HEAD
   ```

3. **Title** — conventional commit style, under 70 chars: `<type>(<scope>): <description>`. Derive the type from the branch prefix (`feat/` → feat, `fix/` → fix, `ref/` → ref). If `$ARGUMENTS` holds an issue number, read its title for context:
   ```bash
   gh issue view <number> --json title -q '.title'
   ```

4. **Read `.github/PULL_REQUEST_TEMPLATE.md`** and reuse its **exact headers** — do not hardcode them here.

5. **Create**:
   ```bash
   gh pr create --title "<title>" --assignee Chemaclass --label "<label>" --body "$(cat <<'EOF'
   <exact headers from the template, filled in>

   Closes #<issue-number>
   EOF
   )"
   ```

   **Label** — pick the single most relevant:

   | Label | When |
   |---|---|
   | `bug` | branch starts with `fix/` |
   | `enhancement` | branch starts with `feat/` |
   | `documentation` | docs only |
   | `refactoring` | restructuring, no behavior change |
   | `dependencies` | dependency bumps |

   **Body**: what changed and why, not how. Under 15 lines. Use `Closes #<n>` so merging closes the issue.

6. **Report the PR URL.**

## Note on emoji

The PR template headers carry emoji and should keep them. GitHub squash-merges copy the **title** verbatim into history — keep emoji out of the title.
