---
name: command-authoring
description: Guide for authoring, creating, writing, building, reviewing, or improving slash commands that delegate to agents or skills. Use when designing /commands for user shortcuts, fixing existing commands, or learning command best practices. Helps design simple command files, choose delegation targets, handle arguments, and decide when to use commands vs skills. Also triggers when asking how to create commands, whether to use a command vs skill, or understanding command patterns. Expert in command patterns, best practices, and keeping commands focused.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
model: sonnet
---

## Reference Files

Detailed command authoring guidance:

- [command-design-patterns.md](command-design-patterns.md) - Four design patterns with complete examples and when to use each
- [command-creation-process.md](command-creation-process.md) - Step-by-step command creation workflow (7 steps)
- [command-examples.md](command-examples.md) - Real command examples with analysis and best practices

---

## About Commands

Commands are user-invoked shortcuts that provide explicit control over when capabilities are used. They're typed as `/command-name` and typically delegate to agents or skills.

**Key characteristics**:

- **User-invoked** - Typed explicitly as `/command-name` (not auto-triggered)
- **Simple** - Delegate to agents/skills rather than containing complex logic
- **Focused** - Single, clear purpose
- **Explicit** - User controls timing of invocation
- **Discoverable** - Shown in `/help` output

**When to use commands**:

- User wants explicit shortcut for frequent task
- Simple delegation pattern
- User should control timing
- Creating convenience wrapper for agent/skill

## Core Philosophy

### Commands Should Be Simple

**Golden rule**: Commands delegate, they don't implement.

**Good command** (simple delegation):

```markdown
---
description: Audit shell scripts for best practices, security, and portability
---

# audit-bash

Audit shell scripts for best practices, security, and portability using the bash-audit skill.
```

**Bad command** (complex logic):

```markdown
# bad-example

# DON'T DO THIS - complex logic in command

Read all shell scripts, run ShellCheck, analyze results, generate report...
[50 lines of implementation details]
```

**Why keep it simple**:

- Easier to maintain
- Clear delegation target
- Less prone to errors
- Follows single responsibility principle

### Commands Are Explicit

Unlike skills (which auto-trigger), commands require user action.

**Use commands when**:

- User wants control over timing
- Action shouldn't happen automatically
- Frequently-used prompt that deserves shortcut
- Explicit workflow trigger

**Use skills when**:

- Should auto-trigger based on context
- User doesn't need to remember to invoke it
- Complex domain knowledge that enhances conversation

### Delegation Pattern

Commands use descriptive delegation - see `../../references/delegation-patterns.md` for complete validation criteria and patterns.

## Command Structure

### Required Elements

Every command must have:

1. **description field** (in frontmatter) - Required for `/help` and model invocation
2. **Command name heading** (# command-name)
3. **Clear purpose** - What the command does

### Optional Elements

Depending on complexity:

- **Usage section** - How to invoke, with/without arguments
- **What It Does** - Detailed explanation
- **Examples** - Sample invocations
- **Delegation** - Which agent/skill it uses
- **Use Cases** - When to use the command
- **Output** - What to expect

### Two Patterns

**Pattern 1: Simple Delegator** (6-10 lines)

- Just frontmatter + brief description
- Minimal documentation
- Clear delegation statement

**Pattern 2: Documented Delegator** (30-80 lines)

- Full usage instructions
- Examples and use cases
- Detailed delegation explanation
- What It Does section

**Choose based on**:

- Complexity of underlying agent/skill
- Whether arguments need explanation
- How often users will reference it

See [command-design-patterns.md](command-design-patterns.md) for detailed design patterns and examples.

See [command-creation-process.md](command-creation-process.md) for step-by-step creation workflow.

## Commands vs Skills Decision Guide

**📄 See [when-to-use-what.md](../../references/when-to-use-what.md) for complete decision guide including agents and output-styles (shared)**

**Quick guide**:

**Use a Command when**:

- User wants explicit control over timing
- Action should be deliberate, not automatic
- Frequently-used prompt deserves shortcut
- User-initiated workflow
- Simple wrapper around agent/skill

**Use a Skill when**:

- AI should auto-discover capability
- Complex domain knowledge
- Should trigger on user queries automatically
- Needs progressive disclosure with references/
- Automatic workflow assistance

## Common Mistakes to Avoid

1. **Complex logic in command** - Commands should delegate, not implement
2. **Missing description** - Frontmatter description is required
3. **No delegation info** - Unclear what agent/skill it uses
4. **Vague purpose** - Command should have single, clear focus
5. **Too many arguments** - Keep it simple, 0-2 args typically
6. **Not testing with /help** - Verify command appears correctly
7. **Poor naming** - Use descriptive, action-oriented names

See [command-examples.md](command-examples.md) for complete examples with analysis.

## Tips for Success

1. **Keep commands under 50 lines** unless truly necessary
2. **Delegate, don't implement** - let agents/skills do the work
3. **Test with `/help`** to verify display
4. **Use descriptive names** - action verbs work well
5. **Document delegation target** - make it clear what runs
6. **Make purpose immediately clear** - no guessing
7. **Optional arguments are better** - provide defaults
8. **Start simple** - can always add documentation later

## Related Skills

This skill is part of the authoring skill family:

- **agent-authoring** - Guide for creating agents
- **skill-authoring** - Guide for creating skills
- **command-authoring** - Guide for creating commands (this skill)
- **output-style-authoring** - Guide for creating output styles

For validation, use the corresponding audit skills:

- **command-audit** - Validate command configurations
- **audit-coordinator** - Comprehensive multi-faceted audits

## Quick Start Checklist

Creating a new command:

- [ ] Identify what agent/skill to delegate to
- [ ] Choose descriptive name (kebab-case)
- [ ] Write clear description (50-150 chars)
- [ ] Decide: simple (6-10 lines) or documented (30-80 lines)?
- [ ] Create file at `~/.claude/commands/command-name.md`
- [ ] Add required frontmatter with description
- [ ] Document delegation target
- [ ] Test with `/help` and invocation
- [ ] Verify arguments work correctly (if any)

## Reference to Standards

For detailed standards and validation:

- **Naming conventions** - Use kebab-case for command names
- **Frontmatter requirements** - description field is required
- **File organization** - `~/.claude/commands/command-name.md`

See `audit-coordinator` skill for comprehensive standards.
