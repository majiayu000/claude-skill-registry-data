---
name: commit-message-creator
description: Generate standards-compliant commit messages following Conventional Commits with emojis. Use this when creating commits, reviewing commit messages, or ensuring consistent commit history.
license: MIT
---

# Commit Message Creator

This skill guides agents in creating clear, standards-compliant commit messages that follow the Conventional Commits specification with meaningful emojis.

## When to Use This Skill

Use this skill when:
- Creating a commit message for code changes
- Reviewing or improving existing commit messages
- Asked to "commit", "write a commit message", or "create a commit"
- Ensuring consistent commit history
- Generating release notes from commits
- Following semantic versioning practices

## Prerequisites

- Understanding of the code changes being committed
- Knowledge of related issue numbers or tickets
- Familiarity with the project's scope naming conventions
- Git repository with staged changes

## Instructions

### 1. Identify the Commit Type

**Choose the appropriate type with emoji:**

| Type | Emoji | Use When |
|------|-------|----------|
| **feat** | ✨ | Adding a new feature for users |
| **fix** | 🐛 | Fixing a bug for users |
| **docs** | 📚 | Documentation only changes |
| **style** | 💎 | Code style/formatting (no functional change) |
| **refactor** | ♻️ | Code change that neither fixes a bug nor adds a feature |
| **perf** | 🚀 | Performance improvements |
| **test** | ✅ | Adding or updating tests |
| **build** | 🔧 | Build system or dependency changes |
| **ci** | 👷 | CI/CD configuration changes |
| **chore** | 🔨 | Other changes (tooling, etc.) |
| **revert** | ⏪ | Reverting a previous commit |

### 2. Determine the Scope (Optional but Recommended)

**Add contextual scope in parentheses:**

**For this project (nomos-provider-terraform-remote-state):**
- `provider` - gRPC provider service implementation
- `backend` - Backend implementations (local, Azure, etc.)
- `state` - State parsing and handling logic
- `config` - Configuration management
- `deps` - Dependency updates
- `spec` - Specification/documentation in specs/ folder
- `api` - gRPC API contract changes

**General common scopes:**
- `auth` - Authentication
- `api` - API endpoints
- `ui` - User interface
- `db` - Database
- `core` - Core functionality

### 3. Write the Description

**Follow these rules:**

1. **Use imperative, present tense**
   - ✅ "add feature" NOT "added feature" or "adds feature"
   - Think: "This commit will..."

2. **Don't capitalize first letter**
   - ✅ "add two-factor authentication"
   - ❌ "Add two-factor authentication"

3. **No period at the end**
   - ✅ "fix race condition in user updates"
   - ❌ "fix race condition in user updates."

4. **Maximum 72 characters**
   - Keep it concise and scannable

5. **Be specific and descriptive**
   - ✅ "prevent race condition in user updates"
   - ❌ "fix bug"

### 4. Add Body (When Needed)

**Include a body when:**
- The change requires explanation beyond the subject
- You need to explain the "why" not the "what"
- Multiple related changes need listing
- Context is important for future maintainers

**Body formatting:**
- Separate from subject with a blank line
- Wrap at 72 characters
- Use bullet points for multiple items
- Explain what and why, not how

### 5. Add Footer (When Appropriate)

**Include footer for:**

**Issue references:**
```
Fixes #123
Closes #456, #789
Refs #999
```

**Breaking changes:**
```
BREAKING CHANGE: The /auth/login endpoint now requires email
instead of username. Update all API clients accordingly.
```

**Co-authors:**
```
Co-authored-by: Name <email@example.com>
```

### 6. Construct the Complete Message

**Format:**
```
<emoji> <type>[optional scope]: <description>

[optional body]

[optional footer]
```

## Examples

### Simple Feature
```
✨ feat(backend): add Azure Blob Storage backend support

Implements Azure backend for remote state storage using
Azure Storage SDK. Supports authentication via environment
variables following Azure standard patterns.

Closes #42
```

### Bug Fix
```
🐛 fix(state): prevent panic on malformed state files

Add validation for state format version before parsing.
Return proper error instead of panicking when state file
is corrupted or has unsupported version.

Fixes #156
```

### Documentation
```
📚 docs: update quickstart with Azure backend example

Add step-by-step guide for configuring Azure backend
including required environment variables and permissions.
```

### Refactoring
```
♻️ refactor(provider): extract port discovery to separate function

Move port printing logic into dedicated function for
better testability and separation of concerns.
```

### Performance
```
🚀 perf(state): optimize output parsing with lazy evaluation

Defer parsing of nested module outputs until accessed.
Reduces memory usage by 60% for large state files.
```

### Tests
```
✅ test(backend): add integration tests for local backend

Cover file reading, missing file handling, and workspace
selection. Tests use temporary directories for isolation.
```

### Build/Dependencies
```
🔧 build(deps): upgrade go to 1.25

Update go.mod and CI workflows to use Go 1.25.
Required for new generics features in state parser.
```

### CI Changes
```
👷 ci: add race detection to test workflow

Run all tests with -race flag to catch concurrency issues.
Increases test time but catches critical bugs.
```

### Breaking Change
```
✨ feat(api): change GetOutput to return typed values

BREAKING CHANGE: GetOutput now returns Value message with
type information instead of raw strings. Clients must
handle new Value structure.

Migration: Replace response.value with response.value.string_value
for string outputs. See migration guide in docs/.

Closes #234
```

### Multiple Issues
```
🐛 fix(provider): resolve gRPC error handling issues

- Return proper gRPC status codes for all error cases
- Add NotFound for missing outputs
- Use InvalidArgument for configuration errors

Fixes #123, #124, #125
```

### Revert
```
⏪ revert: "feat(backend): add S3 backend support"

This reverts commit abc123def456.

S3 backend implementation caused memory leaks in
long-running processes. Needs redesign before merge.

Refs #999
```

## Best Practices

### Do's ✅
- Use emoji prefix for visual context
- Keep subject line under 72 characters
- Use imperative mood ("add" not "added")
- Reference related issues/PRs
- Group related changes in single commit when logical
- Write for future maintainers
- Capitalize proper nouns (OAuth, HTTP, API, gRPC)
- Be specific about what changed and why

### Don'ts ❌
- Don't use vague messages ("fix bug", "update code")
- Don't commit multiple unrelated changes together
- Don't use past tense ("fixed", "added")
- Don't capitalize first letter of description
- Don't add period at end of subject
- Don't forget to reference issues
- Don't commit directly to main branch
- Don't include debugging code or commented code

## Semantic Versioning Impact

**Your commit type affects version bumps:**

- **feat** → Minor version (0.1.0 → 0.2.0)
- **fix** → Patch version (0.1.0 → 0.1.1)
- **BREAKING CHANGE** → Major version (0.1.0 → 1.0.0)

## Git Workflow

```bash
# Stage your changes
git add <files>

# Commit with proper message
git commit -m "✨ feat(provider): add Azure backend support"

# For messages with body and footer, use editor
git commit
# Then write full message following format
```

## Validation

**Check your commit message:**
- [ ] Emoji and type are correct
- [ ] Scope is appropriate (if used)
- [ ] Description uses imperative mood
- [ ] Description is lowercase
- [ ] No period at end of subject
- [ ] Subject is under 72 characters
- [ ] Body explains "why" not "how" (if present)
- [ ] Issue references included (if applicable)
- [ ] Breaking changes documented (if applicable)

## Enforcement

**Use commitlint for automated validation:**

```bash
# Install
npm install --save-dev @commitlint/{config-conventional,cli}

# Configure .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [2, "always", [
      "feat", "fix", "docs", "style", "refactor",
      "perf", "test", "build", "ci", "chore", "revert"
    ]]
  }
}

# Add to husky pre-commit hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
```

## Troubleshooting

**Issue**: Commit message too long
**Solution**: Move details to body, keep subject focused and under 72 chars

**Issue**: Unsure which type to use
**Solution**: Use "feat" for user-facing changes, "refactor" for internal improvements

**Issue**: Multiple unrelated changes
**Solution**: Split into separate commits - one logical change per commit

**Issue**: Forgot issue number
**Solution**: Use `git commit --amend` to update message

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Commit Message Standards](https://github.com/autonomous-bits/development-standards/blob/main/commit-messages.md)
- [Semantic Versioning](https://semver.org/)
- [Gitmoji Guide](https://gitmoji.dev/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
