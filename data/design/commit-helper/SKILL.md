---
name: commit-helper
description: Guide users through creating meaningful, well-structured git commits following best practices. Use this skill when users want to commit changes, ask for help with commit messages, or need guidance on what to commit. Ensures commits are atomic, descriptive, and follow conventional commit standards.
---

# Commit Helper

This skill helps you create high-quality git commits by systematically analyzing changes, crafting meaningful commit messages, and following industry best practices.

## When to Use This Skill

Activate this skill when:
- User asks to "commit changes" or "create a commit"
- User requests "help with commit message"
- User says "what should I commit?" or "how should I organize these changes?"
- Multiple files have been changed and commits need to be organized
- User wants to follow best practices for git commits

## Core Principles

### Atomic Commits
- One logical change per commit
- Each commit should be independently deployable
- If you can describe a commit with "and", it should be split

### Meaningful Messages
- Explain WHY, not just WHAT
- Use present tense ("Add feature" not "Added feature")
- Be specific and concise
- First line: 50 chars or less summary
- Optional body: detailed explanation with 72 char lines

### Conventional Commits
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification when appropriate:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Formatting, missing semi colons, etc.
- `refactor:` Code restructuring without behavior change
- `perf:` Performance improvements
- `test:` Adding or updating tests
- `chore:` Maintenance tasks, dependencies, etc.
- `ci:` CI/CD changes

## Commit Analysis Process

Follow these steps systematically:

### 1. Review Current State

```bash
# Check what's staged vs unstaged
git status

# See staged changes
git diff --staged

# See unstaged changes
git diff

# Review recent commits for context
git log --oneline -5
```

### 2. Analyze Changes

Group changes by:
- **Type**: Feature, fix, refactor, docs, etc.
- **Scope**: Which component/module affected
- **Impact**: Breaking changes, minor changes, patches
- **Independence**: Can changes be separated?

### 3. Determine Commit Strategy

**Single Atomic Commit** - Use when:
- All changes relate to one logical task
- Changes are interdependent
- It's a small, focused change

**Multiple Commits** - Use when:
- Changes span multiple concerns
- Some changes are independent
- Mixing features with fixes
- Large refactoring with multiple steps

### 4. Stage Strategically

```bash
# Stage specific files
git add file1.js file2.js

# Stage parts of a file interactively
git add -p filename.js

# Stage all changes of a certain type
git add *.test.js
```

### 5. Craft Commit Message

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**
```
feat(auth): add JWT token refresh mechanism

Implemented automatic token refresh to improve user experience
by preventing unexpected logouts. Tokens now refresh 5 minutes
before expiration.

- Added RefreshTokenService
- Updated AuthInterceptor to handle 401 responses
- Added token expiration checking in auth guard

Closes #123
```

### 6. Pre-Commit Checklist

Before committing, verify:
- [ ] Code compiles/runs without errors
- [ ] Tests pass (if applicable)
- [ ] No debugging code (console.log, debugger, etc.)
- [ ] No sensitive data (API keys, passwords, tokens)
- [ ] No unintended files (node_modules, .env, etc.)
- [ ] Commit message is clear and descriptive
- [ ] Changes are atomic and focused

## Commit Message Templates

### Feature Addition
```
feat(<scope>): add <feature-name>

Brief description of what the feature does and why it's needed.

- Implementation detail 1
- Implementation detail 2
- Implementation detail 3
```

### Bug Fix
```
fix(<scope>): resolve <issue-description>

Explanation of what was broken and how it's fixed.

Root cause: <brief explanation>
Solution: <brief explanation>

Fixes #<issue-number>
```

### Refactoring
```
refactor(<scope>): <what-was-restructured>

Explanation of why the refactoring improves the codebase.
Note: No functional changes.

- Extracted common logic into utility
- Improved naming for clarity
- Simplified conditional logic
```

### Documentation
```
docs: update <what-documentation>

Description of documentation changes and why they were needed.
```

### Breaking Changes
```
feat(<scope>): <feature-name>

BREAKING CHANGE: <description of breaking change>

Migration guide:
1. Step one
2. Step two
3. Step three
```

## Best Practices

### DO:
- Commit early and often
- Write commit messages for your future self
- Reference issue numbers when applicable
- Test before committing
- Use branches for features
- Keep commits focused and atomic
- Write in imperative mood ("Add" not "Added" or "Adds")

### DON'T:
- Commit commented-out code
- Commit merge conflicts
- Use vague messages like "fix stuff" or "WIP"
- Commit generated files (unless necessary)
- Mix whitespace changes with logic changes
- Commit directly to main/master (use branches)
- Forget to add new files

## Special Cases

### Work In Progress (WIP)
```bash
# For genuine WIP that you need to save
git commit -m "WIP: implementing user authentication"

# Later, amend or squash before merging
git commit --amend
# or
git rebase -i HEAD~n
```

### Fixing the Last Commit
```bash
# If you forgot to add a file
git add forgotten-file.js
git commit --amend --no-edit

# If you need to change the message
git commit --amend
```

### Co-Authors
```
feat(api): add GraphQL endpoint

Implemented GraphQL API with user queries and mutations.

Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

## Output Format

When helping users commit, present:

```markdown
## Commit Analysis

**Changes Detected:**
- [List of changed files with brief description]

**Suggested Strategy:**
[Single commit / Multiple commits with reasoning]

**Proposed Commit(s):**

### Commit 1: [Type]
```
[Full commit message]
```

**Files to stage:**
- file1.js
- file2.js

### Commit 2: [Type] (if applicable)
...

**Commands to execute:**
```bash
git add file1.js file2.js
git commit -m "..."
```
```

## Anti-Patterns to Avoid

- **Avoid "god commits"**: 50 files changed with "various updates"
- **Avoid mixing concerns**: Don't commit refactoring + new features together
- **Avoid unclear subjects**: "fix bug" vs "fix login validation error"
- **Avoid committing broken code**: Each commit should leave the codebase functional
- **Avoid generic messages**: Be specific about what and why
- **Avoid skipping the body**: Complex changes need explanation

## Examples

### Example 1: Single Feature
```
User: "I added a dark mode toggle to the settings page"