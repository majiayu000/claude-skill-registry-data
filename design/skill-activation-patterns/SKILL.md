---
name: skill-activation-patterns
description: Design patterns for automatic skill activation at plugin or project level. Use when implementing keyword-based skill suggestions.
allowed-tools: ["Read", "Write", "Grep", "Glob"]
---

# Skill Activation Patterns

Automatic skill suggestions based on user prompt keywords.

## Two Scopes

| Scope | Location | Purpose | Who Sets It |
|-------|----------|---------|-------------|
| **Plugin-level** | `$CLAUDE_PLUGIN_ROOT/.claude/skills/skill-rules.json` | Plugin recommends its own skills | Plugin author |
| **Project-level** | `$CLAUDE_PROJECT_DIR/.claude/skills/skill-rules.json` | User configures for their project | End user |

### Plugin-level (Recommended for plugins with multiple skills)

Plugins with related skills **SHOULD** include skill-activation to help users discover relevant skills:

```
my-plugin/
├── hooks/hooks.json              ← UserPromptSubmit hook
├── scripts/skill-activation.py   ← Hook script
├── .claude/skills/skill-rules.json  ← Plugin's own rules
└── skills/
    ├── skill-a/
    └── skill-b/
```

**Example**: skillmaker uses plugin-level activation to suggest `skill-design` when user mentions "create skill".

### Project-level (User-configured)

Users can add skill-activation to their own projects independently:

```
my-project/
├── .claude/
│   └── skills/
│       └── skill-rules.json   ← User's rules
└── settings.json              ← UserPromptSubmit hook
```

## Quick Start

1. Create `.claude/skills/skill-rules.json`
2. Add UserPromptSubmit hook
3. Hook reads rules, matches triggers, suggests skills

## Core Concept

```
User Prompt → [Hook] → skill-rules.json → Match triggers → Suggest skills
```

## skill-rules.json (Minimal)

```json
{
  "version": "1.0",
  "skills": {
    "backend-patterns": {
      "type": "domain",
      "enforcement": "suggest",
      "promptTriggers": {
        "keywords": ["backend", "API"]
      }
    }
  }
}
```

## Skill Types

| Type | Purpose |
|------|---------|
| **domain** | Expertise/knowledge |
| **guardrail** | Enforce standards |

## Enforcement Levels

| Level | Behavior |
|-------|----------|
| **suggest** | Recommend |
| **warn** | Allow + warning |
| **block** | Must use skill |

## Best Practices

1. **Start with suggest** - Don't block until proven
2. **Specific keywords** - Avoid generic over-triggering
3. **Test regex** - Verify no false positives
4. **Use skipConditions** - Allow escape hatch

## References

- [Full Schema](references/full-schema.md) - Complete skill-rules.json spec
- [Hook Implementation](references/hook-implementation.md) - TypeScript/Bash code
- [Real Examples](references/skill-rules-examples.md) - Production configs
