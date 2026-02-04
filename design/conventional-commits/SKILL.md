---
name: conventional-commits
description: Generate properly formatted Conventional Commits messages with Claude Code footer. Use when creating git commits, writing commit messages, or the user mentions "commit", "git commit", or wants to save changes.
allowed-tools: Bash, Read, Grep
---

# Conventional Commits for emoji_gen

This Skill helps create commit messages that follow the Conventional Commits specification and include the required Claude Code footer.

## Commit Message Format

```
<type>[optional scope][optional !]: <description>

[optional body]

[required footer]
```

## Types

- **feat**: New feature for the user or library
- **fix**: Bug fix for the user
- **docs**: Documentation changes only
- **build**: Changes to build system or dependencies (Cargo.toml, Dockerfile, CI)
- **test**: Adding or updating tests
- **refactor**: Code changes that neither fix bugs nor add features
- **perf**: Performance improvements
- **chore**: Maintenance tasks, tooling changes

## Scope Examples

- `feat(cli):` - CLI-related feature
- `fix(parser):` - Parser bug fix
- `build(docker):` - Docker build changes
- `docs(readme):` - README updates

## Breaking Changes

Indicate with `!` after type/scope:
```
feat!: drop support for count=0
```

Or use `BREAKING CHANGE:` footer:
```
feat: change default emoji pool

BREAKING CHANGE: removed deprecated emojis from pool
```

## Required Footer

**ALWAYS include this footer:**

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Instructions for Creating Commits

1. **Run git diff to understand changes:**
   ```bash
   git diff --staged
   # or
   git diff
   ```

2. **Analyze the changes** to determine:
   - Appropriate type (feat, fix, docs, build, etc.)
   - Optional scope (cli, docker, ci, etc.)
   - Whether it's a breaking change
   - Clear, concise description (imperative mood)

3. **Draft commit message** following the template in `commit-template.txt`

4. **Use heredoc format for multi-line commits:**
   ```bash
   git commit -m "$(cat <<'EOF'
   feat: add emoji category support

   Adds categorization system for emojis (animals, food, symbols).
   Users can now filter by category using --category flag.

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

## Best Practices

- Use imperative mood: "add" not "added", "fix" not "fixed"
- Keep summary under 50 characters when possible
- Explain **what** and **why**, not **how**
- Reference issue numbers in body if applicable
- Always include the Claude Code footer
- Use body for context if the change needs explanation

## Common Patterns

### Simple feature
```
feat: add emoji pool customization via config file

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Bug fix with details
```
fix: correct emoji count validation

Previously accepted negative counts, now returns error for count < 0.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Build/CI change
```
build(docker): optimize dependency caching layer

Remove emoji_gen-specific artifacts to prevent cache conflicts between
dummy and real builds.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Documentation
```
docs: add Docker development workflow to README

Includes docker-dev.sh helper script usage and examples.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Breaking change
```
feat(cli)!: replace --count with --num flag

BREAKING CHANGE: --count flag removed, use --num instead

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Error Prevention

**DO NOT:**
- Forget the Claude Code footer
- Use past tense ("added", "fixed")
- Write vague descriptions ("update stuff", "fix bug")
- Skip the body when breaking changes need explanation
- Commit without running git diff first

**DO:**
- Always check staged changes first
- Use clear, specific descriptions
- Include body for context when needed
- Use appropriate type and scope
- Include the required footer
