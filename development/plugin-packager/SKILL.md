---
name: plugin-packager
description: Package claudefiles components into a valid Claude Code plugin
---

# Plugin Packager

## Quick Package (Default)

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "claudefiles",
  "version": "1.0.0",
  "description": "Claude Code components: agents, commands, hooks, skills",
  "license": "MIT",
  "commands": ["./commands/golang/", "./commands/typescript/", "./commands/docs/"],
  "agents": ["./agents/golang/", "./agents/typescript/", "./agents/python/", "./agents/docs/", "./agents/general/"],
  "skills": "./skills/",
  "hooks": ["./hooks/golang/hooks.json", "./hooks/security/hooks.json"]
}
```

## Validate

```bash
chmod +x hooks/golang/scripts/*.sh hooks/security/scripts/*.py
claude plugin install . --scope local
```

## Checklist

- [ ] `.claude-plugin/` directory exists
- [ ] plugin.json has `name` + `version`
- [ ] Scripts have +x permission
- [ ] All paths start with `./`
