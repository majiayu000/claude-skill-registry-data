---
name: commit
description: Optionally checks, then commits code to the current or a new feature branch.
---

When asked to commit code, follow these steps:

## Arguments

- `check` (default): Lint, build, and test the code at step 3, after the prose pass. Stop if any checks fail.
- `force`: Skip the check step and commit directly.

## Steps

1. Run these bash commands in parallel to understand the current state:

   - `git status` to see all untracked files
   - `git diff HEAD` to see both staged and unstaged changes
   - `git log --oneline -10` to see recent commit messages for style consistency

2. Run the prose pass over the diff: Skill tool with skill="prose-pass". Apply its cuts before staging anything. **Do not skip this**, however small the diff.

3. Unless invoked with `force`, lint, build, and test the code (`lint-build-test`). This runs after the prose pass because that pass may rename an identifier or drop a comment lint requires. Stop if any checks fail.

4. If you are on the `main` branch, create a new feature branch using `git branch` and switch to it.

5. Analyze all changes and draft a commit message:

   - Summarize the nature of the changes (new feature, enhancement, bug fix, refactoring, test, docs, etc.)
   - Use the conventional commit format: `type(scope): description`
   - Keep the first line under 72 characters
   - Do not commit files that likely contain secrets (.env, credentials.json, etc.)

6. Stage and commit the changes:

   - Add relevant files using `git add`
   - Use a plain string for the commit message (do not use HEREDOCs).

7. Report the results including:
   - The commit hash
   - The commit message
