---
name: craft-command
description: How to craft a Slash Command trigger.
---

# Skill: Craft Command

> "Thin commands. Fat skills."

## The Philosophy

Commands are **triggers**, not logic containers. If you're writing prose or instructions in a command body, **stop**. That belongs in a skill.

## The Spec

**Read first**: https://code.claude.com/docs/en/slash-commands

## The Pattern

```markdown
---
description: One-line purpose.
argument-hint: <what user provides>
---

/skills/skill-name "$ARGUMENTS"
```

## Frontmatter Reference

| Field           | Purpose                               |
|-----------------|---------------------------------------|
| `description`   | Brief purpose (shown in autocomplete) |
| `argument-hint` | Expected arguments                    |
| `allowed-tools` | Restrict tool access                  |
| `model`         | Override model for this command       |

## Arguments

- `$ARGUMENTS` — all arguments as single string
- `$1`, `$2`, etc. — positional access

## See Also

- `examples.md` — patterns and anti-patterns
