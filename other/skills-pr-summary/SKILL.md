---
name: skills-pr-summary
description: Use when refreshing the current pull request description in the Scenario skills repository.
license: MIT
metadata:
  internal: true
---

Update the current PR description with a fresh summary.

1. Run `git fetch origin main --quiet && git diff --stat $(git merge-base HEAD origin/main)..HEAD` for change stats
2. Run `git log --oneline $(git merge-base HEAD origin/main)..HEAD` for all commits
3. Run `pnpm run validate` for validation status (house style, skill supporting files, spelling, skills-ref spec validation)
4. Generate an updated PR body with:
   - Summary section (3-5 bullet points of key changes)
   - Validation section (checked items for what passed)
   - Stats (files changed, skills touched)
5. Remember this is a public repository: the PR body must contain only publicly shareable language (see AGENTS.md, "Public content only")
6. Write the exact PR body to a temporary file, then update the PR with `gh pr edit --body-file <file>`
7. Tell me the PR URL
