---
name: git-conventional-commit
description: Generates and executes git commits following the Conventional Commits specification. It analyzes git diffs, stages changes, and creates formatted commit messages. Use this skill when the user wants to commit code, generate a commit message, or mentions "git commit", "conventional commits", or "commit my changes".
allowed-tools:
  - shell
---

# Git Conventional Commit Generator

This skill automates the process of staging changes and committing them using the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Core Process

1.  **Analyze Changes**: Check for staged and unstaged changes using `git status` and `git diff`.
2.  **Stage Files**: If no changes are staged, ask the user if they would like to stage all changes (`git add .`) or specific files.
3.  **Generate Message**: Analyze the diff to determine the appropriate type, scope, and description.
4.  **User Review**: Present the proposed commit message to the user for approval.
5.  **Execute**: Once approved, run the commit command. **Never** push the changes to a remote repository.

## Conventional Commit Format

The generated message must follow this structure:
`<type>[optional scope]: <description>`

### Allowed Types
-   `feat`: A new feature
-   `fix`: A bug fix
-   `docs`: Documentation only changes
-   `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
-   `refactor`: A code change that neither fixes a bug nor adds a feature
-   `perf`: A code change that improves performance
-   `test`: Adding missing tests or correcting existing tests
-   `chore`: Changes to the build process or auxiliary tools and libraries

## Instructions

### 1. Identify the Diff
If the user hasn't provided a diff, use the `shell` tool to retrieve it:
-   To see staged changes: `git diff --cached`
-   To see unstaged changes: `git diff`
-   To see a summary of modified files: `git status --short`

### 2. Draft the Message
-   **Type**: Choose the most relevant type based on the diff.
-   **Scope**: Use a noun describing a section of the codebase (e.g., `(api)`, `(ui)`, `(auth)`).
-   **Description**: Use the imperative, present tense: "change" not "changed" nor "changes". Do not capitalize the first letter and do not end with a period.

### 3. Confirmation
Present the message clearly to the user:
> **Proposed Commit Message:**
> `feat(auth): add JWT validation logic`
> 
> Would you like me to execute this commit?

### 4. Execution
Upon confirmation, run:
`git commit -m "<message>"`

## Examples

### Example 1: New Feature
**User**: "Commit these changes for me."
**Claude**: (After checking diff) "I've analyzed your changes to `user_controller.go`. I suggest the following commit: `feat(users): add password reset endpoint`. Should I proceed?"

### Example 2: Bug Fix
**User**: "I fixed the alignment in the header, can you commit it?"
**Claude**: "I see the changes in `header.css`. Proposed message: `fix(ui): correct logo alignment in mobile header`. Shall I commit this for you?"

## Constraints
-   **Do Not Push**: Never run `git push`. Only perform local commits.
-   **Confirmation Required**: Always ask for confirmation before running the `git commit` command.
-   **No Empty Commits**: If there are no changes to commit, inform the user.