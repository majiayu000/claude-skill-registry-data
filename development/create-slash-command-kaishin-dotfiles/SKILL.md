---
name: create-slash-command
description: Create custom slash commands for Claude Code. Use when the user wants to create, add, or build a new slash command, custom command, or save a prompt as a command.
allowed-tools: Write, Read, Glob, Bash
---

# Create Slash Command Skill

This Skill helps you create custom slash commands for Claude Code. Slash commands are user-invoked shortcuts stored as Markdown files that can include arguments, bash execution, and file references.

## Instructions

When creating a slash command, follow these steps:

1. **Determine the command scope:**

   - Project commands: `.claude/commands/` (shared via git)
   - Personal commands: `~/.claude/commands/` (local only)

2. **Ask the user for command details:**

   - Command name (use lowercase, hyphens, descriptive)
   - What the command should do
   - Whether it needs arguments
   - Whether it needs to execute bash commands
   - Whether it needs to reference files

3. **Create the command file:**

   - Filename should be `{command-name}.md`
   - Use frontmatter for advanced features (optional)
   - Write clear, concise prompt instructions

4. **Add appropriate frontmatter fields (if needed):**

   - `allowed-tools`: Restrict which tools Claude can use
   - `argument-hint`: Help text shown to users (e.g., `[message]`, `[PR number]`)
   - `description`: Brief description of the command
   - `model`: Specific model to use (e.g., `claude-3-5-haiku-20241022`)
   - `disable-model-invocation: true`: Prevent Claude from auto-invoking this command

5. **Test the command:**
   - Inform user they can use it immediately by typing `/{command-name}`
   - Show example usage with arguments if applicable

## Frontmatter Template

```markdown
---
allowed-tools: Tool1, Tool2, Bash(command:*)
argument-hint: [your hint here]
description: Brief description
model: claude-3-5-haiku-20241022
disable-model-invocation: false
---
```

## Common Patterns

### Simple Prompt Command

No frontmatter needed, just plain text:

```markdown
Review this code for best practices and suggest improvements.
```

### Command with Arguments

Use `$ARGUMENTS` for all args or `$1`, `$2` for individual args:

```markdown
---
argument-hint: [issue number]
description: Fix a specific GitHub issue
---

Fix issue #$ARGUMENTS following our coding standards and create a commit.
```

### Command with Bash Execution

Use `!` prefix for bash commands:

```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current status: !`git status`
- Current diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Task

Create a commit based on the above changes.
```

### Command with File References

Use `@` prefix for files:

```markdown
---
argument-hint: [file path]
description: Document a specific file
---

Add comprehensive documentation to @$ARGUMENTS including:

- Purpose and functionality
- Parameters and return values
- Usage examples
- Edge cases
```

### Command with Restricted Tools

Limit Claude to specific tools for safety:

```markdown
---
allowed-tools: Read, Grep, Glob
description: Read-only code analysis
---

Analyze the codebase for security vulnerabilities without making any changes.
```

## Examples

### Example 1: Simple Review Command

**File:** `.claude/commands/review.md`

```markdown
Review this code for:

- Code quality and readability
- Potential bugs
- Performance issues
- Security vulnerabilities
```

**Usage:** `/review`

### Example 2: PR Review with Arguments

**File:** `.claude/commands/pr-review.md`

```markdown
---
argument-hint: [PR number]
description: Review a GitHub pull request
---

Review PR #$ARGUMENTS and provide:

1. Summary of changes
2. Potential issues
3. Suggestions for improvement
4. Approval recommendation
```

**Usage:** `/pr-review 123`

### Example 3: Complex Commit Command

**File:** `.claude/commands/commit.md`

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*)
argument-hint: [commit message]
description: Create a git commit with context
---

## Current State

- Branch: !`git branch --show-current`
- Status: !`git status`
- Staged changes: !`git diff --cached`

## Task

Create a commit with message: $ARGUMENTS

Follow conventional commits format and include detailed description.
```

**Usage:** `/commit feat: add user authentication`

### Example 4: Test Generator

**File:** `.claude/commands/test.md`

```markdown
---
argument-hint: [file path]
description: Generate tests for a file
---

Generate comprehensive unit tests for @$ARGUMENTS including:

- Happy path scenarios
- Edge cases
- Error handling
- Mocking external dependencies

Use the same testing framework already used in the project.
```

**Usage:** `/test src/utils/helpers.ts`

## Command Organization

### Using Subdirectories

Organize commands by category:

```
.claude/commands/
├── git/
│   ├── commit.md        → /commit (shows as "project:git")
│   └── pr-review.md     → /pr-review (shows as "project:git")
├── testing/
│   ├── unit-test.md     → /unit-test (shows as "project:testing")
│   └── e2e-test.md      → /e2e-test (shows as "project:testing")
└── docs/
    └── document.md      → /document (shows as "project:docs")
```

## Best Practices

1. **Use descriptive names:** `/review-pr` is better than `/rpr`
2. **Keep commands focused:** One command = one clear purpose
3. **Add argument hints:** Help users understand what to pass
4. **Use frontmatter sparingly:** Only add it when you need the features
5. **Test with different inputs:** Verify arguments work as expected
6. **Document complex commands:** Add comments explaining what the command does
7. **Use allowed-tools for safety:** Restrict tools for read-only or limited-scope commands
8. **Choose the right location:**
   - Project commands (`.claude/commands/`): Team workflows, project-specific
   - Personal commands (`~/.claude/commands/`): Your personal preferences

## Troubleshooting

### Command Not Found

- Verify file exists in `.claude/commands/` or `~/.claude/commands/`
- Check filename matches command name (e.g., `review.md` for `/review`)
- May need to restart Claude Code to pick up new commands

### Arguments Not Working

- Use `$ARGUMENTS` for all args or `$1`, `$2`, etc. for individual args
- Add `argument-hint` to frontmatter for better UX
- Test with and without arguments

### Bash Commands Not Executing

- Use `!` prefix: `!`git status``
- Add permission in `allowed-tools`: `Bash(git status:*)`
- Commands run in project directory

### File References Not Working

- Use `@` prefix: `@src/file.ts`
- Can use with arguments: `@$1` or `@$ARGUMENTS`
- File must exist or Claude will ask for clarification

## After Creating

After creating a command, remind the user:

1. The command is immediately available as `/{command-name}`
2. Show example usage with sample arguments
3. If it's a project command, they can commit it to git to share with team
4. They can edit the command file anytime to update it
