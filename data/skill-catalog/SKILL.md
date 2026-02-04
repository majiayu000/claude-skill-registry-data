---
name: skill-catalog
description: Categorize and display available skills. Use when listing or selecting skills.
allowed-tools: ["Read"]
---

# Claude Code Global Skill System

Claude Code maintains a **global skill registry**. All installed skills are automatically available.

```
System Prompt (자동 포함):
<available_skills>
  <skill><name>skill-name</name><description>...</description></skill>
  ...
</available_skills>
```

**No discovery needed** - Claude already knows all skills.

---

# Skill Sources

| Source | Location | Registration |
|--------|----------|--------------|
| Plugin Skills | `~/.claude/plugins/*/skills/` | marketplace.json `skills` array |
| User Skills | `~/.claude/skills/` | Automatic |
| Project Skills | `.claude/skills/` | Automatic |

All sources merge into a single global registry accessible via `Skill` tool.

---

# Categories

| Icon | Category | Keywords |
|------|----------|----------|
| 📊 | Data & Analysis | data, sql, database, query |
| 🎨 | Design & Frontend | ui, frontend, component, design |
| 📝 | Documentation | doc, writing, content |
| 🔧 | Development Tools | build, deploy, test, ci |
| 🔒 | Security | security, auth, validation |
| 🤖 | AI & Orchestration | ai, workflow, orchestration, agent |
| 📦 | Code Generation | generate, scaffold, template |
| 🔍 | Code Analysis | analyze, review, refactor |

---

# Usage

## Listing Skills
Claude can reference `<available_skills>` from system prompt directly.

## Calling Skills
```
Skill("skill-name")           # Load skill into context
Skill("plugin:skill-name")    # Fully qualified name
```

## In Agent YAML
```yaml
skills: skill1, skill2        # Auto-loaded at agent start
```

---

# Skill Selection Guide

For orchestrator agents, help users select skills:

```markdown
## Available Skills by Category

### 🔍 Code Analysis
- **serena-refactor:analyze** - SOLID violation detection
- **pr-review-toolkit:code-reviewer** - PR code review

### 🤖 AI & Orchestration
- **skillmaker:orchestration-patterns** - Agent architecture
- **skillmaker:mcp-gateway-patterns** - MCP isolation

Which skills does your agent need?
```

---

## Best Practices

1. **Use global registry** - Don't manually glob for skills
2. **Categorize by domain** - Help users find relevant skills
3. **Prefer plugin:skill format** - Avoid naming conflicts

## References

- [Skill Categories](references/skill-categories.md) - Detailed category definitions
