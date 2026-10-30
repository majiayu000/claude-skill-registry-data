---
name: pr-description
description: Generate a PR description from the project template and apply it directly to the current branch's GitHub PR
disable-model-invocation: true
argument-hint: "[additional context]"
---

# Generate PR Description

## PR Template

!`cat "$(git rev-parse --show-toplevel)/.github/pull_request_template.md" 2>/dev/null || echo "NO_TEMPLATE — no .github/pull_request_template.md found; use a sensible default structure (Description / Changes Made / Testing / Additional Notes)."`

## Branch Context

- **Current branch:** !`git branch --show-current`
- **Existing PR for this branch:** !`gh pr view --json number,title,url 2>/dev/null || echo "NONE"`
- **Commits on this branch:**

!`git log --oneline master...HEAD`

- **Diff stats:**

!`git diff --stat master...HEAD`

## Instructions

This skill checks and updates the GitHub PR **only** — it must NOT write any local file (e.g. `pr-description.md`).

1. Analyze the commits and diff stats above to understand what changed
2. Read key changed files to understand the changes in detail (focus on non-generated files, skip lockfiles)
3. Fill in ALL sections of the PR template above:
   - **Description**: 1-3 sentences summarizing purpose and goals
   - **Changes Made**: Bullet list grouped by package/area (e.g., "**tereo:** Added bucket lifecycle endpoint", "**@tereo-io/sdk:** …")
   - **Version Plan**: Check if a file exists in `.nx/version-plans/` on this branch — check the box only if one exists
   - **Testing**: Note which tests were added/modified, which packages are affected
   - **Additional Notes**: Migration notes, new env vars, newly declared permissions/roles/buckets/event types, breaking changes (including for app services on `@tereo-io/sdk`), deployment considerations
4. Update the PR on GitHub with the completed description:
   - If **Existing PR for this branch** above is `NONE`, stop and tell the user there is no PR to update (offer to run `gh pr create` if they want one). Do NOT create a local file.
   - Otherwise, write the body to a temp file in the scratchpad directory (never in the repo) and run `gh pr edit <number> --body-file <scratchpad>/pr-body.md`, then report the PR URL.

## Guidelines

- Be specific about what changed — not vague
- Group changes by package when multiple packages are affected
- Mention any new dependencies, environment variables, or permissions added
- Note if database migrations are needed
- If commits reference issue numbers, include them
- The PR reflects only **pushed** commits. If `git status` shows uncommitted changes or the branch is ahead of its remote, warn the user that those changes won't be in the PR until pushed.
- Only check a template checkbox (e.g. Version Plan, "tests pass") if you have actually verified it. Leave unverifiable boxes unchecked and say why, rather than checking them optimistically.

$ARGUMENTS
