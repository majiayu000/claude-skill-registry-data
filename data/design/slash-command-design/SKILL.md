---
name: slash-command-design
description: Interpretive guidance for designing Claude Code slash commands. Helps you apply official documentation effectively and create high-quality commands. Use when creating or reviewing slash commands.
---

# Slash Command Design

This skill provides interpretive guidance and best practices for creating Claude Code slash commands. It helps you understand how to create excellent commands.

## Fundamentals

**Prerequisites:** This skill builds on box-factory-architecture. If not already loaded, core concepts like isolation model and component selection may be unclear.

Four core principles for slash command design:

### Commands Are User-Triggered Prompt Expansions

Commands execute when users type `/command-name`. They expand to prompts that Claude processes. Typically invoked directly by user, but Claude Main Agent can also invoke them autonomously via the SlashCommand tool.

### Use Delegation When It Provides Clear Benefits

Commands should delegate to sub-agents to achieve: context isolation, parallelization, or leveraging the abilities of specialized agents.

Delegate when:

- The goal of the command can be satisfied clearly and cleanly by a sub-agent (preserves context)
- There is a clear specialty agent designed for the task (eg, 'researcher', 'test-runner')
- The task can be parallelized into independent subtasks (efficiency)

Do not delegate when:

- There is no clear, appropriate agent
- The task needs user interaction or broad context from the main conversation
  
### Arguments Are Simple String Substitutions

Use `$1`, `$2` for positional arguments or `$ARGUMENTS` for all arguments as a single string.

### Tool Restrictions Are Optional

Commands can use any tools needed for their task. Use `allowed-tools` frontmatter only when you specifically want to constrain scope (security-sensitive operations, read-only review commands, etc.).

## Workflow Selection

| If you need to...                                                           | Go to...                                                         |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Understand command vs agent vs skill (when to use each component type)      | [Decision Framework](#decision-framework)                        |
| See basic command structure (quick reference for creating commands)         | [Quick Start](#quick-start)                                      |
| Learn frontmatter fields (official specification)                           | [Frontmatter Fields](#frontmatter-fields-official-specification) |
| Use arguments in commands (positional vs all-arguments patterns)            | [Argument Patterns](#argument-patterns)                          |
| Execute bash or reference files (! prefix, @ prefix, tool restrictions)     | [Advanced Features](#advanced-features)                          |
| Decide delegation vs direct implementation (when to use agents vs commands) | [Best Practices](#best-practices-opinionated-guidance)           |
| Avoid common mistakes (anti-patterns catalog with symptoms and fixes)       | [common-pitfalls.md](common-pitfalls.md)                         |
| Validate before completing (final checklist before creating command)        | [Quality Checklist](#quality-checklist)                          |

## Quick Start

Create a command file based on the path-resolution rules from box-factory-architecture component-paths.

```markdown
---
description: Brief description of what this command does
argument-hint: expected-args
---

Command prompt content here.
Use $1, $2 for individual arguments or $ARGUMENTS for all.
```

**With delegation:**

```markdown
---
description: Run full test suite and analyze failures
---

Use the test-runner agent to execute all tests and provide detailed failure analysis.
```

## Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when creating commands to ensure current syntax:

- **<https://code.claude.com/docs/en/slash-commands>** - Core specification and examples
- **<https://code.claude.com/docs/en/settings#tools-available-to-claude>** - Verify tool names

## Decision Framework

### Command vs Agent vs Skill

**Quality test:** If you want this to happen automatically based on context, it's an agent, not a command.

**Use Command when:**

- User wants explicit control over when it runs
- Simple, deterministic operation
- Wrapping a bash script or tool sequence
- "I want to type `/something` to make X happen"

**Use Agent when:**

- Need isolated context window (large outputs shouldn't pollute main conversation)
- Want parallelization (multiple agents working simultaneously)
- Reusable workflow (same logic invoked by multiple commands)
- Want autonomous delegation based on context detection

**Use Skill when:**

- Multiple contexts need the same knowledge
- Substantial procedural expertise
- Progressive disclosure would save tokens

**Deep dive:** Load the box-factory-architecture skill for full component selection guidance. **Traverse when:** ambiguous component choice, edge cases not covered by summary. **Skip when:** summary above clearly answers the question.

## Frontmatter Fields (Official Specification)

All fields are optional:

| Field                      | Purpose                                             | Default                    |
| -------------------------- | --------------------------------------------------- | -------------------------- |
| `description`              | Brief command description for `/help`               | First line of prompt       |
| `argument-hint`            | Expected arguments (e.g., `[pr-number] [priority]`) | None                       |
| `allowed-tools`            | Restrict to specific tools (e.g., `Bash(git:*)`)    | Inherits from conversation |
| `disable-model-invocation` | Prevents SlashCommand tool from auto-invoking       | false                      |

### Best Practices for Frontmatter (Opinionated Guidance)

**Always include `description`** even though it's optional - improves discoverability and Claude's ability to use the SlashCommand tool for autonomous command invocation. Use strong language guiding Claude when it is appropriate to use this tool.

**Use `argument-hint`** when arguments are expected - helps users understand command syntax in `/help` output.

**Use `allowed-tools` when:**

- Security-sensitive operations (restrict to specific git commands, read-only access)
- Single-purpose commands with clear scope (status checks, simple queries)
- Preventing accidental file modifications (read-only tools only)

**Don't use `allowed-tools` when:**

- Command delegates to agent (let agent define its own tool restrictions)
- Need full tool access for complex operations
- Multiple tool combinations required

**Use `disable-model-invocation`** only in edge cases where SlashCommand tool auto-invocation causes issues. Most commands don't need this field.

## Argument Patterns

### Official Specification

**All arguments as single string:**

```markdown
$ARGUMENTS
```

Example: `/fix-issue 123 high-priority` → `$ARGUMENTS = "123 high-priority"`

**Individual positional arguments:**

```markdown
$1, $2, $3, etc.
```

Example: `/review-pr 456 high alice` → `$1="456"`, `$2="high"`, `$3="alice"`

### When to Use Which Pattern (Best Practices)

**Use `$1, $2` when:**

- Need arguments in different parts of the prompt
- Want to provide defaults or conditional logic
- Arguments have distinct semantic meanings

**Use `$ARGUMENTS` when:**

- Passing all arguments directly to agent
- Single compound argument (like a description or message)
- Don't need to reference specific positions

### Argument Handling

Commands use simple string substitution (`$1`, `$ARGUMENTS`). Claude handles the actual interpretation and validation as part of processing the expanded prompt.

```markdown
---
description: Deploy to specified environment
argument-hint: environment
---

Deploy to $1 environment. Validate the environment name, check deployment prerequisites, and proceed with appropriate rollback strategy.
```

Complex multi-step workflows with error recovery may benefit from agent delegation for context isolation, but straightforward argument handling works fine in commands.

## Advanced Features

### Bash Execution with `!` Prefix (Official Specification)

Execute bash commands before the prompt runs:

```markdown
---
allowed-tools: Bash(git:*)
---

!git status

Review the git status above and suggest next steps.
```

**When to use:** Quick status checks before analysis (`!git status`, `!npm test`), gathering context for Claude's response, read-only commands that inform the prompt.

**Avoid for:** Multi-step conditional bash workflows, write operations without confirmation.

### File References with `@` Prefix (Official Specification)

Include file contents in the prompt:

```markdown
Review @src/utils/helpers.js for potential improvements.
```

Multiple files: `Compare @src/old.js with @src/new.js`

**When to use:** Simple file review tasks, direct comparison of specific files, quick analysis of known paths.

**Avoid for:** Large files (token limits), dynamic file discovery where paths aren't known upfront.

### Subdirectory Namespacing (Official Specification)

Organize commands in subdirectories:

```text
commands/frontend/component.md → /component (project:frontend)
commands/backend/endpoint.md → /endpoint (project:backend)
```

Command name comes from filename, subdirectory appears in `/help` as namespace label.

**When to use:** Large projects with distinct subsystems, commands specific to tech stack areas, avoiding command name collisions.

**Avoid for:** Small projects (flat structure is clearer), over-categorization (3-5 commands don't need subdirectories).

### Tool Restriction Patterns (Official Specification)

Restrict commands to specific tools via `allowed-tools`:

```markdown
---
description: Show git status
allowed-tools: Bash(git status:*)
---

Run `git status` and display the output.
```

**Common patterns:**

- `Bash(git:*)` - Git operations only
- `Bash(git status:*)` - Specific git command
- `Read, Grep, Glob` - Read-only file operations
- Omit field entirely to inherit conversation tools

**When to use:** Security-sensitive operations, single-purpose commands with clear scope, preventing accidental file modifications.

## Best Practices (Opinionated Guidance)

### When to Delegate vs Handle Directly

Commands can do substantial work. Delegation to sub-agents isn't about complexity—it's about specific benefits:

**Delegate when you need:**

- **Context isolation** — Large outputs (test results, logs, file contents) shouldn't clutter the main conversation
- **Parallelization** — Multiple independent tasks that can run simultaneously
- **Reusable workflows** — Same logic invoked by multiple commands or contexts

**Handle directly when:**

- Task is straightforward even if it involves multiple steps
- Output is reasonably sized and useful in main conversation
- No need for the workflow to be reusable elsewhere

**Deep dive:** Load the box-factory-architecture skill for multi-component patterns. **Traverse when:** designing workflows that span multiple components. **Skip when:** single command design.

### Generation Pattern

For creating files/code, be specific about structure and requirements:

```markdown
---
description: Create a new React component with TypeScript
argument-hint: component-name
---

Create a new React component named `$1` in the components directory.

Include:
- TypeScript interface for props
- Basic component structure with proper typing
- Export statement
- Test file in __tests__ directory

Follow project conventions for imports and file structure.
```

### Real-World Examples

**Direct command (no delegation needed):**

```markdown
---
description: Show current git branch and status
allowed-tools: Bash(git:*)
---

!git branch --show-current
!git status --short

Current branch and working tree status displayed above.
```

**Direct command with file operations:**

```markdown
---
description: Review package.json dependencies
---

Read package.json and analyze the dependencies. Flag any outdated packages, security concerns, or unused dependencies.
```

**With delegation (context isolation for large output):**

```markdown
---
description: Run full test suite and analyze failures
---

Use the test-runner agent to execute all tests and provide failure analysis.
```

The test-runner agent is appropriate here because test output can be large and detailed analysis benefits from isolated context.

**With delegation (reusable workflow):**

```markdown
---
description: Commit all changes with smart message generation
argument-hint: [commit-message]
---

Use the git-committer agent. Pass arguments: $ARGUMENTS
```

The git-committer agent encapsulates commit workflow logic reused across multiple entry points.

## Component Paths

**Deep dive:** Load the box-factory-architecture skill for component path resolution. **Traverse when:** need to determine exact file paths, working in plugin context. **Skip when:** caller specified path or using default project location (`.claude/commands/`).

## Quality Checklist

Before finalizing a command:

**Structure (from official docs):**

- [ ] Valid YAML frontmatter (if used)
- [ ] Proper markdown formatting
- [ ] Filename is kebab-case (becomes command name)

**Best Practices (opinionated):**

- [ ] Includes `description` field for discoverability
- [ ] Uses `argument-hint` if arguments expected
- [ ] Action-oriented (not knowledge storage)
- [ ] Clear, single-purpose design
- [ ] Tool restrictions only if specifically needed for security/scope

**Delegation Decision:**

- [ ] If delegating: justified by context isolation, parallelization, or reusability need
- [ ] If not delegating: task fits naturally in main conversation context
