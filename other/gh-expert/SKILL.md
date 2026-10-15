---
name: gh-expert
description: Guides coding agents through the standard workflow for working on GitHub issues and moving them to completed pull requests using the 'gh' CLI.
---

# GitHub Expert Workflow

This skill provides a structured process for contributing to projects via GitHub Issues and Pull Requests. It ensures clear communication, visibility, and high-quality contributions by following a strict sequential workflow.

## Quick Reference
For detailed command usage and flag options, refer to:
- [workflow.md](references/workflow.md) - Project-specific workflow rules.
- [gh_help.md](references/gh_help.md) - GitHub CLI command reference.

---

## 1. Discovery and Claiming
All work must begin with an existing GitHub Issue.

1. **Find an issue:** Use `gh issue list` to find tasks.
2. **Review details:** Use `gh issue view <number>` to understand requirements.
3. **Claim it:** Use `gh issue edit <number> --add-label "claimed"` before starting work.

## 2. Branching and PR Initialization
Never work directly on `main`. Create a draft PR early to signal active work.

1. **Create branch:** `git checkout -b <branch-name>` (use descriptive names like `feature/` or `fix/`).
2. **Initial commit:** `git commit --allow-empty -m "Initial commit for issue #<number>"`
3. **Push branch:** `git push -u origin <branch-name>`
4. **Create Draft PR:** 
   ```bash
   gh pr create --title "Work on #<number>: <description>" --body "Closes #<number>" --draft
   ```

## 3. Planning with TODO.md
Create a `TODO.md` file in the root directory to track granular tasks. This file is the primary source of truth for the branch's progress.

1. **Define tasks:** List specific, actionable steps with Markdown checkboxes (`- [ ]`).
2. **Commit plan:** `git add TODO.md && git commit -m "Add implementation plan (TODO.md)" && git push`

## 4. Implementation (In Progress)
Transition the issue and start coding.

1. **Mark in-progress:** `gh issue edit <number> --add-label "in-progress"`
2. **Iterate:** 
   - Work on tasks.
   - Update `TODO.md` (check off completed items).
   - Commit frequently with clear messages.
   - Push to remote regularly.

## 5. Completion and Review
Finalize the work and request a review.

1. **Validate:** Run all project tests and ensure they pass.
2. **Document:** Update the Pull Request description with a detailed summary of changes, implementation details, and test results.
   ```bash
   gh pr edit --body "## Summary
   Brief description of changes.

   ## Changes
   - Detail 1
   - Detail 2

   ## Testing
   - [x] Unit tests passed
   - [x] Integration tests passed"
   ```
3. **Clean up:** Remove `TODO.md` before merging.
   ```bash
   rm TODO.md
   git add TODO.md
   git commit -m "Remove TODO.md before PR review"
   git push
   ```
4. **Mark Ready:** `gh pr ready`
5. **Request Review:** `gh pr edit --add-reviewer <username>` (if applicable).

---

## Best Practices
- **Atomic Commits:** Keep commits focused and descriptive.
- **Stay Updated:** Regularly pull from the base branch to avoid conflicts.
- **Close Issues:** Ensure the PR body contains "Closes #<number>" to automate issue closure.
