---
name: Claude Code Plugin Builder
description: Creates Claude Code plugins with proper manifest structure, directory layout, and components (commands, agents, skills, hooks, MCP servers). Use when user requests creating plugins, adding slash commands, integrating MCP servers, setting up hooks, migrating Gemini extensions, or mentions "plugin.json", ".claude-plugin", or "marketplace.json". Handles plugin testing, debugging, and marketplace distribution.
---

# Claude Code Plugin Builder

Expert skill for developing professional Claude Code plugins.

## Critical Directory Rules

Components MUST be at plugin root, NOT inside `.claude-plugin/`:

```
✅ CORRECT:
plugin/
├── .claude-plugin/plugin.json  # Only manifest here
├── commands/                    # At root
├── agents/                      # At root
├── skills/                      # At root
└── hooks/                       # At root

❌ WRONG:
plugin/.claude-plugin/
├── plugin.json
├── commands/      # Won't load
└── agents/        # Won't load
```

## Plugin Creation Workflow

### 1. Initialize Structure

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/{commands,agents,skills,hooks}
```

### 2. Create Manifest

**Minimal** (`my-plugin/.claude-plugin/plugin.json`):
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does"
}
```

**Complete**:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Your Name",
    "email": "email@example.com",
    "url": "https://github.com/user"
  },
  "repository": "https://github.com/org/repo",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "hooks": "./hooks/hooks.json",
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@org/package"],
      "env": {
        "API_KEY": "${API_KEY:-}"
      }
    }
  }
}
```

### 3. Add Components

**Commands** (user-invoked):
```markdown
<!-- commands/deploy.md -->
---
description: Deploy to production
validation:
  requiresFiles: ["package.json"]
---

# Deploy Command

1. Verify deployment readiness
2. Execute: npm run deploy
3. Monitor deployment status
4. Report results
```

**Agents** (autonomous specialists):
```markdown
<!-- agents/security-expert.md -->
---
description: Security vulnerability analysis expert
capabilities: ["vulnerability-scan", "audit", "remediation"]
---

# Security Expert

Specializes in OWASP vulnerabilities, CVE analysis, dependency scanning.

Invoke for: security audits, vulnerability assessments, compliance reviews.
```

**Skills** (model-invoked expertise):
```markdown
<!-- skills/incident-response/SKILL.md -->
---
name: Incident Response
description: Production incident handling including rollback, root cause analysis, postmortem. Use when production outages, security breaches, critical bugs, or user mentions "incident", "production down", "rollback".
---

# Incident Response

## Protocol
1. Assess severity (P0-P4)
2. Contain: rollback/disable/rate-limit
3. Investigate: logs, metrics, recent changes
4. Resolve: fix, test, deploy, verify
5. Document: postmortem, lessons learned

See [incident-procedures.md](./incident-procedures.md) for detailed runbooks.
```

**Hooks** (event automation):
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/format.sh",
        "timeout": 30
      }]
    }]
  }
}
```

**MCP Servers** (external integration):
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/db"],
      "env": {
        "PGPASSWORD": "${POSTGRES_PASSWORD}"
      }
    }
  }
}
```

## Component Selection Guide

| Need | Component | Example |
|------|-----------|---------|
| User triggers action | Command | `/deploy production` |
| Autonomous specialist | Agent | Security analysis |
| Auto-invoked expertise | Skill | Incident response |
| Event automation | Hook | Format after write |
| External system | MCP Server | Database queries |

## Testing Workflow

### Local Development

**Checklist:**
- [ ] Create dev marketplace
- [ ] Add plugin to marketplace
- [ ] Install for testing
- [ ] Test each component
- [ ] Iterate and reload

**Setup:**
```bash
# 1. Create marketplace
cat > .claude-plugin/marketplace.json <<EOF
{
  "name": "dev",
  "owner": {"name": "Dev"},
  "plugins": [{
    "name": "my-plugin",
    "source": {"source": "path", "path": "."}
  }]
}
EOF

# 2. Install
claude
/plugin marketplace add /path/to/dev-marketplace
/plugin install my-plugin@dev

# 3. Test
/my-plugin:command-name

# 4. Reload after changes
/plugin uninstall my-plugin@dev
/plugin install my-plugin@dev
```

### Debug Mode

```bash
claude --debug  # Shows plugin loading, errors, registration
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Plugin not loading | Validate JSON: `jq . .claude-plugin/plugin.json` |
| Commands missing | Ensure `commands/` at root, not in `.claude-plugin/` |
| Hooks not firing | `chmod +x hooks/script.sh`, use `${CLAUDE_PLUGIN_ROOT}` |
| MCP server fails | Use `${VAR:-}` for optional env vars, test command independently |
| Skill not activating | Add specific triggers: file types, error patterns, keywords |

## Marketplace Creation

```json
{
  "name": "company-plugins",
  "owner": {
    "name": "Company",
    "email": "dev@company.com"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "What it does",
      "source": {
        "source": "github",
        "repo": "org/repo"
      }
    }
  ]
}
```

**Distribution:**
- GitHub: `/plugin marketplace add owner/repo`
- Git URL: `/plugin marketplace add https://git.server.com/plugins.git`
- Local: `/plugin marketplace add ./marketplace`

## Gemini CLI Migration

**Checklist:**
- [ ] Create `.claude-plugin/` directory
- [ ] Convert `gemini-extension.json` → `plugin.json`
- [ ] Migrate `GEMINI.md` to SessionStart hook
- [ ] Update README with Claude Code install
- [ ] Test with `claude --debug`

**Quick migrate:**
```bash
#!/usr/bin/env bash
set -euo pipefail

mkdir -p .claude-plugin hooks

# Extract from gemini-extension.json
NAME=$(jq -r '.name' gemini-extension.json)
VERSION=$(jq -r '.version' gemini-extension.json)
DESC=$(jq -r '.description' gemini-extension.json)

# Create plugin.json
cat > .claude-plugin/plugin.json <<EOF
{
  "name": "$NAME",
  "version": "$VERSION",
  "description": "$DESC",
  "hooks": "./hooks/hooks.json"
}
EOF

# Create SessionStart hook
cat > hooks/hooks.json <<'EOF'
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/context.sh",
        "timeout": 10
      }]
    }]
  }
}
EOF

cat > hooks/context.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
CONTEXT="${CLAUDE_PLUGIN_ROOT}/hooks/CONTEXT.md"
if [ -f "$CONTEXT" ]; then
  jq -n --arg ctx "$(cat "$CONTEXT")" '{
    "hookSpecificOutput": {
      "hookEventName": "SessionStart",
      "additionalContext": $ctx
    }
  }'
fi
EOF

chmod +x hooks/context.sh
[ -f GEMINI.md ] && cp GEMINI.md hooks/CONTEXT.md
```

## Best Practices

**Manifest:**
- Use semantic versioning
- Include keywords for discovery
- Document env vars in README

**Commands:**
- Clear descriptions for `/help`
- Single responsibility per command
- Add validation rules

**Agents:**
- Define clear expertise boundaries
- Specify invocation criteria
- Document tool usage

**Skills:**
- Descriptions with concrete triggers (file types, error patterns, keywords)
- Keep SKILL.md under 500 lines
- Use reference files for details: `[details](./reference.md)`
- Focus on workflows, not explanations

**Hooks:**
- Scripts executable: `chmod +x`
- Use `${CLAUDE_PLUGIN_ROOT}` for paths
- Include timeouts
- Return proper JSON

**MCP Servers:**
- Prefer npx for npm packages: `npx -y @org/package`
- Use `${VAR:-}` for optional env vars
- Use fully qualified tool names: `ServerName:tool_name`
- Test command independently

## Progressive Disclosure

For complex plugins:
- Keep SKILL.md concise with workflows
- Link to reference files one level deep
- Organize by task, not by concept
- Example structure:
  ```
  skills/plugin-expert/
  ├── SKILL.md              # Core workflows
  ├── components.md         # Component details
  ├── testing.md            # Testing procedures
  ├── troubleshooting.md    # Common issues
  └── examples/             # Example plugins
  ```

## Quick Reference

**Commands:**
```bash
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace
/plugin uninstall plugin-name@marketplace
/plugin list
claude --debug
```

**Paths:**
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory
- `${VAR:-}` - Optional env var
- `${VAR}` - Required env var

**Events:**
- SessionStart, SessionEnd
- PreToolUse, PostToolUse
- UserPromptSubmit
- Notification, Stop, SubagentStop
- PreCompact

## Resources

For detailed information:
- Component examples: [examples.md](./examples.md)
- Ready-to-use templates: [templates.md](./templates.md)
- Complete guides: [README.md](./README.md)

Official docs:
- [Plugins](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)
- [Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MCP](https://modelcontextprotocol.io/)