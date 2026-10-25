---
name: git-commit-messages
description: Guide for writing descriptive yet succinct git commit messages following best practices. Use this when creating commit messages, reviewing commits, or establishing commit message conventions.
license: MIT
---

# Git Commit Messages

This skill helps you write clear, descriptive, and succinct git commit messages that follow industry best practices and make project history more maintainable.

## When to Use This Skill

Use this skill when:

- Writing commit messages for code changes
- Reviewing pull requests and commit quality
- Establishing commit message conventions for teams
- Understanding how to structure commit history
- Training team members on commit message best practices

## Prerequisites

- Basic understanding of git commands
- Familiarity with your project's commit history
- Knowledge of the changes being committed

## Commit Message Guidelines

### Basic Structure

A good commit message follows this format:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

Use these conventional commit types:

- **feat**: New feature or functionality
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style/formatting changes (no logic changes)
- **refactor**: Code refactoring (no feature changes or bug fixes)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, build changes, dependency updates
- **perf**: Performance improvements
- **ci**: CI/CD pipeline changes
- **build**: Build system or dependency changes

### Subject Line Rules

1. **Limit to 50 characters** - Keep it concise but descriptive
2. **Do not end with a period** - No punctuation at the end
3. **Use imperative mood** - "Add feature" not "Added feature" or "Adding feature"
4. **Be specific** - Clearly describe what changed

### Body Guidelines

1. **Separate from subject with blank line** - Always add a blank line
2. **Wrap at 72 characters** - Maintain readability
3. **Explain what and why** - Describe the change and reasoning
4. **Use bullet points** - For multiple related changes
5. **Reference issues** - Link to tickets or issues when applicable

### Footer Guidelines

1. **Breaking changes** - Use "BREAKING CHANGE:" followed by description
2. **Issue references** - Closes #123, Fixes #456, etc.
3. **Co-authors** - `Co-authored-by: Name <email>`

## Instructions

### Step 1: Analyze Your Changes

Before writing the commit message, understand what changed:

1. **Review the diff** - Use `git diff --cached` to see staged changes
2. **Categorize the change** - Determine the appropriate type (feat, fix, etc.)
3. **Identify the scope** - Which component, module, or feature was affected
4. **Note breaking changes** - Any changes that break existing APIs

### Step 2: Write the Subject Line

Craft a clear, concise subject line:

```bash
# Good examples
feat(auth): add password reset functionality
fix(api): resolve null pointer in user validation
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic

# Bad examples (too vague, too long, wrong tense)
"fixed bug"                                    # Too vague
"fixed the bug that was causing the login to fail when users entered invalid credentials"  # Too long
"Fixes login bug"                             # Wrong tense
```

### Step 3: Add Body (When Needed)

Include a body for complex changes:

```bash
# Complex feature addition
feat(user-profile): add avatar upload functionality

- Implement file upload validation for images only
- Add image resizing and optimization
- Store avatars in cloud storage with CDN
- Update user profile API to include avatar URLs

Closes #123
```

### Step 4: Include Footer (When Applicable)

Add footer information for special cases:

```bash
# Breaking change
refactor(api): change authentication endpoint

BREAKING CHANGE: The /auth/login endpoint now requires
JSON payload instead of form data. Update client code
accordingly.

# Issue reference
fix(database): resolve connection timeout issues

Fixes intermittent database connection failures in
production environment. Added connection pooling and
retry logic.

Closes #456
```

### Step 5: Commit the Changes

Use git to create the commit:

```bash
# Stage changes if not already staged
git add .

# Commit with your message
git commit -m "feat(user-auth): implement OAuth2 login flow

- Add OAuth2 provider configuration
- Implement authorization code flow
- Store user tokens securely
- Add logout functionality

Closes #789"
```

## Examples

### Feature Addition

```text
feat(dashboard): add real-time metrics display

Implement live updating charts for system performance metrics.
- Add WebSocket connection for real-time data
- Create reusable chart components
- Optimize data polling to reduce server load
- Add error handling for connection failures

Resolves #234
```

### Bug Fix

```text
fix(payment): resolve double-charge issue

Prevent duplicate payment processing when users refresh
the confirmation page. Added idempotency key validation
and improved error messaging.

Fixes #567
```

### Documentation Update

```text
docs(api): update webhook payload examples

Add comprehensive examples for all webhook event types
and clarify field descriptions. Include error response
examples and rate limiting information.
```

### Refactoring

```text
refactor(auth): extract user validation logic

Move user input validation to dedicated service class.
- Create UserValidationService with comprehensive rules
- Add unit tests for all validation scenarios
- Update existing controllers to use new service
- Improve error messages for validation failures
```

### Breaking Change

```text
feat(api): migrate to GraphQL API

Replace REST endpoints with GraphQL schema for improved
flexibility and reduced over-fetching.

BREAKING CHANGE: All REST API endpoints are deprecated.
Clients must migrate to GraphQL queries by v2.0.0.

Migration guide: docs.mysite.com/graphql-migration
```

## Best Practices

### Do's

- ✅ Keep subject lines under 50 characters
- ✅ Use conventional commit format when possible
- ✅ Explain the "why" behind changes, not just the "what"
- ✅ Reference related issues or pull requests
- ✅ Use bullet points for multi-part changes
- ✅ Review commit messages before pushing

### Don'ts

- ❌ Write vague messages like "fix bug" or "update code"
- ❌ Include irrelevant details about your day or mood
- ❌ Use swear words or unprofessional language
- ❌ Commit large, unrelated changes together
- ❌ Forget to mention breaking changes

### Team Consistency

1. **Establish conventions** - Document your team's commit message standards
2. **Use templates** - Create commit message templates for common scenarios
3. **Review process** - Include commit message quality in code reviews
4. **Tools integration** - Use commit hooks or CI to enforce standards
5. **Education** - Train team members on best practices

## Tools and Automation

### Commit Message Linting

Use tools to enforce commit message standards:

```bash
# Install commitlint
npm install -g @commitlint/cli @commitlint/config-conventional

# Create .commitlintrc.js
module.exports = {
  extends: ['@commitlint/config-conventional']
};
```

### Git Hooks

Add pre-commit hooks to validate messages:

```bash
#!/bin/sh
# .git/hooks/commit-msg
commitlint < $1
```

### Interactive Commit

Use git's interactive mode for complex commits:

```bash
# Stage changes interactively
git add -p

# Use commit with verbose flag
git commit -v
```

## Common Patterns

### For Different Project Types

**Web Applications:**

```text
feat(ui): add dark mode toggle
fix(auth): prevent session timeout on mobile
perf(images): implement lazy loading for gallery
```

**APIs:**

```text
feat(api): add rate limiting middleware
fix(validation): correct email regex pattern
docs(api): update OpenAPI specification
```

**Infrastructure:**

```text
chore(deps): update Node.js to v18 LTS
ci(pipeline): add automated testing for PRs
build(docker): optimize image size by 40%
```

### For Different Change Sizes

**Small Changes:**

```text
fix(typo): correct variable name in user model
style(lint): fix eslint warnings in component
```

**Large Changes:**

```text
feat(onboarding): implement complete user registration flow

- Add multi-step form with validation
- Integrate email verification service
- Create welcome email templates
- Add user preference settings
- Implement progress tracking

Part of epic #1234
```

## File Structure

```text
git-commit-messages/
├── SKILL.md              # Main skill file with guidelines
├── README.md             # Overview and usage guide
├── examples.md           # Good and bad commit message examples
├── commit-generator.py   # Python script for commit message generation
└── vscode-integration.md # VS Code integration guide
```
