---
name: git-commit
description: Create logically grouped, atomic git commits with well-formatted commit messages following best practices. Use this skill when you need to commit changes to a git repository with proper message formatting and atomic grouping.
allowed-tools:
  - Bash
  - Read
  - Edit
---

# Git Commit Skill

This skill helps you create well-structured, atomic git commits with properly formatted commit messages.

## When to Use This Skill

Use this skill when:
- You need to commit changes to a git repository
- You want to create atomic, logically grouped commits
- You need to follow commit message best practices
- You have multiple changes that should be split into separate commits
- You need to use git partial adds (git add -p) for fine-grained control

## Task Overview

Based on the current git status and changes, create a set of logically grouped, atomic commits.
Be specific with each grouping, and keep scope minimal. Leverage partial adds to
make sure that multiple changes within a single file aren't batched into
commits with unrelated changes.

## Process

1. **Analyze Current State**
   - Check git status to see staged and unstaged changes
   - Review git diff to understand what has changed
   - Check recent commits (`git log --oneline -20`) to understand:
     - Whether the project uses conventional commits (e.g., `feat:`, `fix:`, `docs:`)
     - The project's commit message style and conventions
     - Typical subject line length and formatting patterns

2. **Group Changes Logically**
   - Identify related changes that should be committed together
   - Separate unrelated changes into different commits
   - Use `git add -p` for partial adds when a file contains multiple logical changes

3. **Create Commits**
   - Stage the appropriate changes for each commit
   - Write commit messages following the best practices below
   - Verify each commit is atomic and complete

## Commit Message Format Detection

**IMPORTANT**: Before writing any commits, analyze the recent git history to determine the project's commit style:

- **Check for Conventional Commits**: Look for patterns like `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `style:`, `perf:`, `ci:`, `build:`
- **Match the existing style**: If 80% or more of recent commits follow conventional commits, use that format
- **Be consistent**: Match the capitalization, punctuation, and structure of existing commits

### Conventional Commits Format

If the project uses conventional commits, follow this structure:

```
<type>[(optional scope)]: <description>

[optional body]

[optional footer(s)]
```

**Common types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Changes to build system or dependencies
- `ci`: Changes to CI configuration
- `chore`: Other changes that don't modify src or test files

**Examples:**
- `feat: add user authentication`
- `fix: resolve null pointer in login handler`
- `docs: update API documentation`
- `refactor(auth): simplify token validation logic`

## Git Commit Message Best Practices

Follow these seven rules for excellent commit messages (adjust for conventional commits if used):

1. **Separate subject from body with a blank line** - Critical for readability
2. **Limit subject line to 50 characters** - Forces concise summaries
3. **Capitalize the subject line** - Consistent formatting
4. **Do not end subject line with a period** - It's a title, not a sentence
5. **Use imperative mood in subject** - "Add feature" not "Added feature"
   - Test: Subject should complete "If applied, this commit will _____"
6. **Wrap body at 72 characters** - Ensures readability in terminals
7. **Use body to explain what and why vs. how** - Code shows how, commit explains why

### Message Structure

```
<subject: concise summary, imperative, capitalized, no period>

<body: explain the motivation for the change and contrast with previous behavior>

<footer: references to issues, breaking changes, etc.>
```

### Key Principles

- **Atomic commits**: Each commit should represent one logical change
- **Context is king**: Explain WHY the change was made, not just what
- **Future-proof**: Write for someone (including future you) reading this months later
- **Consistency**: Maintain uniform style across the project

### Examples

**Good Examples (Traditional Style):**
- `Refactor subsystem X for readability`
- `Remove deprecated methods from UserService`
- `Fix null pointer exception in login handler`
- `Add user authentication middleware`

**Good Examples (Conventional Commits):**
- `feat: add user authentication middleware`
- `fix: resolve null pointer exception in login handler`
- `refactor: improve subsystem X readability`
- `chore: remove deprecated methods from UserService`

**Bad Examples:**
- `fixed stuff`
- `Changes`
- `wip`
- `Update file.js`
- `feat added new feature` (incorrect format - missing colon)

## Implementation Steps

1. Run `git status` to see current state
2. Run `git diff HEAD` to see all changes
3. Run `git log --oneline -20` to analyze recent commit style
   - **Determine if conventional commits are used** (look for `type:` prefix patterns)
   - Note the typical capitalization and formatting style
   - Identify any project-specific conventions
4. Identify logical groupings of changes
5. For each logical group:
   - Stage the relevant changes (use `git add -p` if needed)
   - Create a commit with a well-formatted message **matching the project's style**
   - Verify the commit with `git show`
6. After all commits, run `git status` to verify nothing important was missed

## Notes

- **ALWAYS check recent git history first** to determine if conventional commits are used
- **Match the project's existing style** - consistency is more important than personal preference
- DO NOT push to remote unless explicitly asked
- Always verify authorship and commit details before amending
- Use `git add -p` for interactive staging when files contain multiple unrelated changes
- Keep commits focused and atomic - one logical change per commit
- If in doubt about whether to use conventional commits, look at the last 20-30 commits for patterns
