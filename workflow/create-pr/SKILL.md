---
name: create-pr
description: "Create a pull request from the current branch with structured summary"
user-invocable: true
workflow:
  version: 1
  steps:
    - id: verify-branch
      role: system
      intent: "Verify not on main/develop, check for uncommitted changes, get commits ahead of main."
      produces: [branch-name, branch-state, commit-list]
    - id: gather-context
      role: system
      intent: "Collect diff stats, run tests and lint for PR description context."
      requires: [branch-state]
      produces: [diff-summary, test-result, lint-result]
    - id: generate-description
      role: system
      intent: "Build structured PR description from commits, diff stats, and test results."
      requires: [commit-list, diff-summary, test-result, lint-result]
      produces: [pr-description, pr-title]
      gate: true
    - id: create-pr
      role: system
      intent: "Push branch to origin and create PR via gh CLI."
      requires: [pr-description, pr-title, branch-name]
      produces: [pr-url]
    - id: post-creation
      role: system
      intent: "Display PR URL and suggest next steps."
      requires: [pr-url]
      produces: [summary]
      gate: true
---

# Create PR

Creates a pull request from the current feature branch with a structured summary, test results, and change description. Closes the pipeline loop: init -> build-feature -> create-pr.

## When to use

- After completing a feature with `/build-feature`
- When you have changes on a feature branch ready for review
- To create a well-structured PR without manual formatting

## Usage

`/create-pr`

## Process

### Step 1 -- Verify branch state

1. Confirm you are NOT on `main` or `develop` -- refuse to create PR from default branches
2. Run `git status` to check for uncommitted changes -- if any, warn the user and ask whether to commit first
3. Run `git log main..HEAD --oneline` to get the list of commits that will be in the PR
4. If there are no commits ahead of main, report that there is nothing to PR

### Step 2 -- Gather context

Collect the information needed for the PR description:

1. **Commits**: `git log main..HEAD --oneline` -- list of all commits on this branch
2. **Diff summary**: `git diff main..HEAD --stat` -- files changed with line counts
3. **Test results**: Run project tests (e.g., `npm test`) and capture pass/fail
4. **Lint results**: Run project lint (e.g., `npm run lint`) and capture pass/fail
5. **Branch name**: Extract feature name from the branch (e.g., `feature/dark-mode` -> `dark-mode`)

If tests or lint fail, warn the user but allow them to proceed (some PRs are draft/WIP).

### Step 3 -- Generate PR description

Build a structured PR description:

```markdown
## Summary
[2-4 bullet points describing what this PR does, derived from commit messages]

## Changes
[File-level summary from git diff --stat]

## Test plan
- [x] Tests: [pass/fail] ([count] tests)
- [x] Lint: [pass/fail]
- [ ] [Any manual verification steps if applicable]
```

### Step 4 -- Create the PR

1. Push the branch to origin: `git push -u origin [branch-name]`
2. Create the PR using `gh pr create`:
   - Title: derived from branch name or first commit message (max 70 chars)
   - Body: the generated description from Step 3
   - Base: `main` (or the project's default branch)
3. Report the PR URL to the user

### Step 5 -- Post-creation

1. Display the PR URL
2. Suggest next steps:
   - "Request review from a teammate"
   - "Run `/code-review` for an AI code review"
   - "Merge when ready with `gh pr merge [number]`"

## Example Session

```text
User: /create-pr

Checking branch state...
Branch: feature/dark-mode (4 commits ahead of main)
Tests: 82 passed, 0 failed
Lint: 0 errors

Creating PR...
PR #42: "feat: add dark mode toggle to settings"
https://github.com/org/repo/pull/42

Next steps:
- Request review from a teammate
- Run /code-review for AI code review
- Merge when ready
```

## Notes

- The PR title should be concise (under 70 characters) and follow conventional commits format when the project uses it
- If the branch has `wip:` commits from build-feature checkpoints, consider squashing them before creating the PR
- This skill does NOT merge the PR -- that is a manual step or a separate command
