---
name: demeter-skills
description: Central skill registry for demeter project. Use to discover available skills, understand skill conventions, and find the right skill for a task.
---

# Demeter Skills

This directory contains skills that Claude auto-activates based on task context.

## Available Skills

| Skill | File | Purpose |
|-------|------|---------|
| Architecture | [architecture.md](architecture.md) | Project structure and design patterns |

## Skill Conventions

### File Format

Each skill file uses YAML frontmatter:

```yaml
---
name: skill-name
description: What this skill does. When to use it.
allowed-tools: Tool1, Tool2  # Optional
---

# Skill Content
```

### Naming

- Use lowercase with hyphens: `my-skill-name`
- Max 64 characters
- Be specific: `rust-error-handling` not `errors`

### Description Guidelines

The `description` field drives auto-activation. Include:

1. **What** the skill does
2. **When** Claude should use it
3. **Trigger keywords** users would mention

```yaml
# Good
description: Debug Rust compile errors and borrow checker issues. Use when encountering lifetime errors, ownership problems, or type mismatches.

# Bad
description: Helps with Rust
```

## Adding New Skills

1. Create `skill-name.md` in this directory
2. Add YAML frontmatter with `name` and `description`
3. Write skill content in markdown
4. Update the table in this file

## Skill Discovery

Claude automatically discovers skills based on:

- Task relevance
- Description keywords
- Request context

No explicit invocation needed—write good descriptions and Claude will find them.
