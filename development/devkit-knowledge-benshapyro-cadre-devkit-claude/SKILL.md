---
name: devkit-knowledge
description: Knowledge base for the Cadre DevKit. Use when answering questions about the devkit structure, commands, skills, hooks, agents, or workflows.
---

# Cadre DevKit Knowledge Base

This skill helps you find information in the devkit. **Read the actual files** - they are the source of truth.

## Where to Find Things

| Topic | Location |
|-------|----------|
| Global config | `~/.claude/CLAUDE.md` |
| Commands | `~/.claude/commands/*.md` |
| Skills | `~/.claude/skills/*/SKILL.md` |
| Hooks | `~/.claude/hooks/` + `settings.json` |
| References | `~/.claude/references/*.md` |
| Agents | Defined in system, use `Task` tool |

## Quick Answers

### How do I add a command?

Create `~/.claude/commands/my-command.md`:
```markdown
---
description: What this command does
argument-hint: [optional args]
---

# My Command

Instructions for Claude...
```

### How do I add a skill?

Create `~/.claude/skills/my-skill/SKILL.md`:
```yaml
---
name: my-skill-name
description: What it does and when to use it.
---

# My Skill

Instructions and examples...
```

### Skills vs Agents?

- **Skills** = Knowledge (methodology, templates, best practices)
- **Agents** = Workers (spawned via Task tool to do tasks independently)

Skills inform *how* to do something. Agents actually *do* things.

### Debug hooks not running?

1. Enable debug mode: `CLAUDE_HOOK_DEBUG=1`
2. Check `settings.json` has hook registered
3. Verify file is executable (`chmod +x`)

### Skill not activating?

1. Check YAML frontmatter is valid (name + description)
2. Ensure description has trigger keywords
3. Try explicit reference: "Use the X skill"

### Command workflow?

**New Project:**
```
/greenfield → SPEC.md + DESIGN.md + PLAN.md → /plan [feature] → implement → /review → /validate → /ship
```

**Existing Project:**
```
/plan [feature] → implement → /slop (optional) → /review → /validate → /ship
```

**Research:**
```
/research [topic] → findings → /progress (save as docs)
```

## Project vs Global

| Location | Scope |
|----------|-------|
| `~/.claude/` | All projects (personal) |
| `./.claude/` | This project only (team) |

Project-level config takes precedence over global.

## For Everything Else

Read the actual files. This skill points you where to look - don't rely on this skill having the latest info.

---

## Version
- v2.0.0 (2025-12-05): Refactored to reference actual files instead of duplicating content
- v1.0.0 (2025-11-15): Initial version
