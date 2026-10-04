---
name: commit-message-generator
description: Generates clear, conventional commit messages from git diffs. Use when writing commit messages, reviewing staged changes, or when the user asks to generate a commit message.
---

# Commit Message Generator

This skill helps Claude generate high-quality commit messages following conventional commit format and best practices.

## Instructions

When asked to generate a commit message:

1. **Check staged changes**:

   ```bash
   git diff --staged
   ```

2. **Analyze the changes** to understand:

   - What files were modified
   - What functionality changed
   - Why the change was made

3. **Generate a commit message** with this structure:

   ```
   <type>(<scope>): <subject>

   <body>

   <footer>
   ```

4. **Follow these rules**:
   - **Subject line**: 50 characters or less, present tense, no period
   - **Type**: feat, fix, docs, style, refactor, test, chore
   - **Scope**: Component or area affected (optional)
   - **Body**: Explain what and why, not how (wrap at 72 characters)
   - **Footer**: Reference issues (e.g., "Fixes #123")

## Examples

### Simple Feature

```
feat(auth): add password reset functionality

Implement password reset flow with email verification.
Users can now request a password reset link via email.

Fixes #456
```

### Bug Fix

```
fix(parser): handle null values in JSON responses

Previously, null values would cause parser to throw.
Now gracefully handles null by using default values.
```

### Multiple Changes

```
refactor(api): restructure endpoint handlers

- Split large handlers into smaller functions
- Add input validation helpers
- Improve error messages

This makes the codebase more maintainable and testable.
```

## Best Practices

- Use **imperative mood**: "add feature" not "added feature"
- **Be specific**: "fix login bug" → "fix authentication timeout on slow networks"
- **Explain why**: Include motivation for the change
- **Reference issues**: Link to tickets or issues when relevant
- **Keep it focused**: One commit = one logical change
