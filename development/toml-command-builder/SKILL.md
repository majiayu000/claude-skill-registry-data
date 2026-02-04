---
name: toml-command-builder
description: Guide for building Gemini CLI TOML custom commands. Covers syntax, templates, argument handling, shell injection, and file injection. Use when creating Gemini TOML commands, adding {{args}} argument handling, injecting shell output with !{}, or troubleshooting command issues.
allowed-tools: Read, Glob, Grep, Skill
---

# TOML Command Builder

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about TOML commands:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific command topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

This skill provides comprehensive guidance for creating Gemini CLI custom commands using TOML format. Custom commands are slash commands that extend Gemini's capabilities with project-specific or user-specific functionality.

## When to Use This Skill

**Keywords:** toml command, custom command, slash command gemini, gemini command, create command, {{args}}, @{}, !{}

**Use this skill when:**

- Creating a new Gemini CLI custom command
- Understanding TOML command syntax
- Adding argument handling to commands
- Injecting shell output or file content
- Troubleshooting command issues

## Command Locations

### User Commands (Global)

```text
~/.gemini/commands/
├── commit.toml           # /commit
├── review.toml           # /review
└── git/
    └── log.toml          # /git:log (namespaced)
```

### Project Commands (Local)

```text
.gemini/commands/
├── build.toml            # /build
├── test.toml             # /test
└── deploy/
    └── staging.toml      # /deploy:staging
```

## Basic Syntax

### Minimal Command

```toml
# ~/.gemini/commands/hello.toml
description = "A simple greeting command"
prompt = "Say hello to the user"
```

### With Multi-line Prompt

```toml
description = "Generate a commit message"
prompt = """
Analyze the staged changes and generate a commit message.

Follow conventional commit format:
- feat: new features
- fix: bug fixes
- docs: documentation
- refactor: code refactoring
"""
```

## Argument Handling

### Basic Arguments (`{{args}}`)

Arguments passed after the command are injected at `{{args}}`:

```toml
# /greet Kyle -> "Say hello to Kyle"
description = "Greet a person"
prompt = "Say hello to {{args}}"
```

### Default Behavior

If no `{{args}}` placeholder, arguments are appended:

```toml
description = "Analyze code"
prompt = "Analyze this code for issues"
# /analyze src/main.ts -> "Analyze this code for issues src/main.ts"
```

### Multiple Arguments

Arguments are space-separated, accessible together:

```toml
description = "Compare two files"
prompt = "Compare these files: {{args}}"
# /compare file1.ts file2.ts -> "Compare these files: file1.ts file2.ts"
```

## Shell Injection (`!{...}`)

Execute shell commands and inject output:

### Basic Shell

```toml
description = "Analyze git diff"
prompt = """
Review the following git diff:

~~~diff
!{git diff --staged}
~~~

Suggest improvements.
"""
```

### Shell with Safety

Commands are confirmed before execution. Use `--yolo` to skip.

### Complex Shell

```toml
description = "Analyze project structure"
prompt = """
Project structure:
!{find . -type f -name "*.ts" | head -50}

Package dependencies:
!{cat package.json | jq '.dependencies'}

Analyze and suggest improvements.
"""
```

### Shell with Arguments

Combine shell injection with arguments:

```toml
description = "Grep for pattern"
prompt = """
Search results for "{{args}}":

!{grep -r "{{args}}" src/ --include="*.ts" | head -20}

Analyze these occurrences.
"""
```

**Note:** Arguments in shell blocks are automatically escaped for safety.

## File Injection (`@{...}`)

Inject file or directory contents:

### Single File

```toml
description = "Review config"
prompt = """
Review this configuration:

@{tsconfig.json}

Suggest improvements.
"""
```

### Multiple Files

```toml
description = "Review setup"
prompt = """
Package config:
@{package.json}

TypeScript config:
@{tsconfig.json}

Analyze for consistency.
"""
```

### Directory Contents

```toml
description = "Review utilities"
prompt = """
Utility functions:
@{src/utils/}

Analyze for patterns and improvements.
"""
```

**Note:** Directory injection respects `.gitignore` and `.geminiignore`.

### With Arguments

```toml
description = "Review file"
prompt = """
Review this file:
@{{{args}}}

Provide feedback.
"""
# /review src/main.ts -> Injects content of src/main.ts
```

## Processing Order

Injection is processed in order:

1. **`@{...}`** - File content injection
2. **`!{...}`** - Shell command execution
3. **`{{args}}`** - Argument substitution

## Namespacing

Organize commands with directories:

```text
~/.gemini/commands/
├── git/
│   ├── commit.toml     # /git:commit
│   ├── review.toml     # /git:review
│   └── log.toml        # /git:log
├── test/
│   ├── unit.toml       # /test:unit
│   └── e2e.toml        # /test:e2e
└── deploy/
    ├── staging.toml    # /deploy:staging
    └── prod.toml       # /deploy:prod
```

## Template Library

### Git Commit Message

```toml
# ~/.gemini/commands/git/commit.toml
description = "Generate conventional commit message from staged changes"
prompt = """
Analyze the staged changes and generate a commit message.

## Staged Changes
~~~diff
!{git diff --staged}
~~~

## Requirements

- Use conventional commit format (feat/fix/docs/refactor/test/chore)
- Keep subject line under 72 characters
- Add body if changes are significant
- Reference issue numbers if applicable

Generate only the commit message, nothing else.
"""
```

### Code Review

```toml
# ~/.gemini/commands/review.toml
description = "Review code changes with specific focus"
prompt = """
Review the following code changes:

~~~diff
!{git diff}
~~~

Focus on: {{args}}

Provide:

1. Issues found (if any)
2. Suggestions for improvement
3. Positive observations
"""
```

### Test Generator

```toml
# ~/.gemini/commands/test/generate.toml
description = "Generate tests for a file"
prompt = """
Generate comprehensive tests for this file:

@{{{args}}}

Requirements:
- Use the existing test framework (jest/vitest/pytest)
- Cover edge cases
- Include positive and negative tests
- Follow existing test patterns in the project
"""
```

### Documentation Generator

```toml
# ~/.gemini/commands/docs/generate.toml
description = "Generate documentation for code"
prompt = """
Generate documentation for:

@{{{args}}}

Include:
- Purpose and overview
- Function/method documentation
- Usage examples
- Parameter descriptions
"""
```

### Dependency Analyzer

```toml
# ~/.gemini/commands/deps/analyze.toml
description = "Analyze project dependencies"
prompt = """
Analyze these dependencies:

## package.json
@{package.json}

## Lock file (partial)
!{head -100 package-lock.json 2>/dev/null || head -100 yarn.lock 2>/dev/null || echo "No lock file"}

Identify:
1. Outdated packages
2. Security concerns
3. Unused dependencies
4. Duplicate functionality
"""
```

### Migration Helper

```toml
# ~/.gemini/commands/migrate.toml
description = "Help with code migration"
prompt = """
Help migrate this code: {{args}}

Current code:
@{{{args}}}

Migration requirements:
- Preserve functionality
- Follow modern patterns
- Add TypeScript types if missing
- Update deprecated APIs
"""
```

## Validation Patterns

### Check Syntax

```bash
# Validate TOML syntax
python -c "import tomllib; tomllib.load(open('command.toml', 'rb'))"
```

### Required Fields

- `description` (string): Shown in command list
- `prompt` (string): The prompt template

### Common Errors

| Error | Cause | Fix |
| --- | --- | --- |
| Parse error | Invalid TOML syntax | Check quotes, brackets |
| Command not found | Wrong location | Verify path |
| Args not injected | Missing `{{args}}` | Add placeholder |
| Shell fails | Command error | Test command manually |

## Best Practices

### 1. Clear Descriptions

```toml
# Good
description = "Generate commit message from staged changes using conventional format"

# Bad
description = "commit stuff"
```

### 2. Structured Prompts

```toml
prompt = """
## Task
{what to do}

## Context
{relevant information}

## Requirements
- {requirement 1}
- {requirement 2}

## Output Format
{expected format}
"""
```

### 3. Safe Shell Commands

```toml
# Good - read-only, limited output
!{git diff --staged | head -500}

# Risky - potentially destructive
!{rm -rf {{args}}}  # DANGEROUS!
```

### 4. Helpful Error Messages

```toml
prompt = """
{{args}}

If no file specified, respond: "Please specify a file path after the command"
"""
```

### 5. Consistent Naming

```text
commands/
├── git/          # Git operations
│   ├── commit.toml
│   └── review.toml
├── test/         # Testing
│   ├── unit.toml
│   └── e2e.toml
└── docs/         # Documentation
    └── generate.toml
```

## Related Skills

- `gemini-cli-docs` - Official command documentation
- `policy-engine-builder` - Tool execution policies

## Related Commands

- `/build-toml-command` - Interactive command builder wizard

## Keyword Registry

| Topic | Keywords |
| --- | --- |
| Basic syntax | `toml command`, `custom command`, `gemini command` |
| Arguments | `{{args}}`, `command arguments`, `argument injection` |
| Shell | `!{...}`, `shell injection`, `git diff command` |
| Files | `@{...}`, `file injection`, `directory contents` |
| Namespacing | `command namespace`, `git:commit`, `organize commands` |

## Test Scenarios

### Scenario 1: Create Basic Command

**Query**: "How do I create a custom TOML command in Gemini CLI?"
**Expected Behavior**:

- Skill activates on "toml command" or "custom command"
- Provides basic TOML syntax with description and prompt
**Success Criteria**: User receives working .toml file template

### Scenario 2: Shell Injection

**Query**: "How do I include git diff in a Gemini command?"
**Expected Behavior**:

- Skill activates on "shell injection" or "git diff"
- Provides `!{git diff}` syntax
**Success Criteria**: User receives shell injection pattern with safety notes

### Scenario 3: File Injection

**Query**: "How do I inject file contents into a Gemini command?"
**Expected Behavior**:

- Skill activates on "file injection" or "@{"
- Provides `@{filename}` syntax
**Success Criteria**: User receives file injection pattern with directory support

## Version History

- v1.1.0 (2025-12-01): Added MANDATORY section, Test Scenarios, Version History
- v1.0.0 (2025-11-25): Initial release
