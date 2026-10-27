---
name: copilot-cli-plugin-builder
description: "Author, scaffold, test, and distribute GitHub Copilot CLI plugins. Use when the user wants to: (1) create a new Copilot CLI plugin, (2) add skills, agents, hooks, or MCP servers to a plugin, (3) write a plugin.json manifest, (4) use the Copilot SDK to build programmable plugins, (5) publish a plugin to a marketplace, (6) scaffold plugin boilerplate, (7) migrate from legacy Copilot Extensions, or (8) bump or update a plugin's version. Covers the Agent Plugins 1.0 format (agent-plugins.org) and the @github/copilot-sdk in all 6 languages. Do NOT use for Copilot CLI extensions (tools/commands/canvas via @github/copilot-sdk/extension) — use copilot-cli-extension-builder instead."
metadata:
  version: 0.1.1
---

# Copilot CLI Plugin Builder

Author GitHub Copilot CLI plugins — packages of skills, agents, hooks, and MCP servers distributed via marketplaces.

## Plugin Architecture

Plugins are **file-based** (markdown + JSON). No compilation required. Two formats exist:

| Format | Schema | Use |
|--------|--------|-----|
| **Agent Plugins 1.0** | `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` | Recommended — portable across Copilot CLI, Cursor, VS Code |
| **Legacy** | No `$schema` | Still supported but not recommended for new plugins |

Always use **Agent Plugins 1.0** unless the user has a specific reason for legacy format.

## Directory Layout (Agent Plugins 1.0)

```
my-plugin/
├── plugin.json                    # Required manifest
├── skills/                        # Portable skills
│   └── skill-name/
│       └── SKILL.md               # Skill definition
├── mcp.json                       # MCP server configs
└── com.github.copilot/            # Copilot-specific components
    ├── agents/
    │   └── my-agent.agent.md
    ├── commands/
    ├── rules/
    ├── hooks/
    │   └── hooks.json
    └── lsp.json
```

Minimal plugin: just `plugin.json` + one component (skill, agent, hook, or MCP server).

## Workflow

### Phase 1: Gather Requirements

Ask the user these questions (one at a time, skip if already specified):

1. **What should the plugin do?** — Get a clear purpose statement
2. **Which components?** — Skills, agents, hooks, MCP servers, or a combination?
3. **Plugin name?** — 1–64 chars, lowercase ASCII, digits, hyphens, periods

If unsure about components, suggest the simplest approach: a single skill.

### Phase 2: Scaffold the Plugin

Create the directory structure with `plugin.json`:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": { "name": "Your Name" },
  "license": "MIT",
  "keywords": ["relevant", "tags"]
}
```

Then create each component. See the Component Guides below.

### Phase 3: Author Components

#### Skills

Skills inject context/instructions into the agent via `SKILL.md`:

```markdown
---
name: my-skill
description: When and why to use this skill
---

# Instructions

Be concise. Use imperative form. Include only what Claude doesn't already know.
```

Skills follow the same conventions as workspace skills (scripts/, references/, assets/ subdirectories). For skill authoring best practices, follow the skill-creator patterns.

#### Custom Agents

Agents are scoped sub-agents with isolated tools and prompts. Define as `.agent.md` files in `com.github.copilot/agents/`:

```markdown
---
name: my-agent
displayName: My Agent
description: What this agent does (used by runtime for intent matching)
tools:
  - grep
  - glob
  - view
---

You are a specialized agent. Your role is to...
```

Or programmatically via the SDK — see `references/sdk-examples.md`.

#### Hooks

Hooks fire at lifecycle points. Create `com.github.copilot/hooks/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      { "type": "command", "command": "./scripts/init.sh", "timeout": 10 }
    ],
    "preToolUse": [
      { "type": "command", "command": "./scripts/validate.sh", "timeout": 5 }
    ]
  }
}
```

Available hooks: `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse`, `postToolUse`, `postToolUseFailure`, `errorOccurred`, `subagentStart`, `subagentStop`. For full details, see `references/hook-lifecycle.md`.

#### MCP Servers

External tool providers. Create `mcp.json` at plugin root:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["${PLUGIN_ROOT}/server/index.js"],
      "env": { "DATA_DIR": "${PLUGIN_DATA}" }
    }
  }
}
```

Transports: `stdio`, `streamable-http`, `sse` (deprecated). Variables: `${PLUGIN_ROOT}`, `${PLUGIN_DATA}`.

### Phase 4: Install and Test

```bash
# Install locally
copilot plugin install ./my-plugin

# Verify
copilot plugin list

# Test in interactive session
copilot
# Then: /skills list, /agent, /plugin list
```

Plugins are cached — re-run `copilot plugin install ./my-plugin` after edits.

### Phase 5: Distribute

**Local development:**
```bash
copilot plugin install ./my-plugin
```

**From GitHub repo:**
```bash
copilot plugin install OWNER/REPO
copilot plugin install OWNER/REPO:PATH/TO/PLUGIN
```

**Via marketplace:** See `references/marketplace-guide.md` for creating and distributing through marketplaces.

### Version Bump

When bumping a plugin's version, **always update both files atomically**:

1. `plugin.json` → `version` (source of truth)
2. `marketplace.json` → `plugins[name=X].version` (must mirror plugin.json)

These MUST match. Drift causes users to miss updates or install unexpected versions. See `references/marketplace-guide.md` → "Bump Procedure" for the full checklist including verification and commit steps.

## SDK Usage

The `@github/copilot-sdk` provides programmatic control via JSON-RPC. Supports 6 languages: TypeScript, Python, Go, .NET, Rust, Java.

Quick start (TypeScript):
```typescript
import { CopilotClient, approveAll } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();
const session = await client.createSession({
    model: "auto",
    onPermissionRequest: approveAll,
});
const response = await session.sendAndWait({ prompt: "Hello" });
console.log(response?.data.content);
await client.stop();
```

For SDK examples in all languages, custom tools, streaming, and MCP configuration, see `references/sdk-examples.md`.

## Component Reference

| Component | Format | Location (Agent Plugins 1.0) | Purpose |
|-----------|--------|------------------------------|---------|
| Skill | `SKILL.md` | `skills/<name>/SKILL.md` | Inject context/instructions |
| Agent | `.agent.md` | `com.github.copilot/agents/*.agent.md` | Scoped sub-agents |
| Hook | `hooks.json` | `com.github.copilot/hooks/hooks.json` | Lifecycle callbacks |
| MCP Server | `mcp.json` | `mcp.json` | External tool providers |

## Key Concepts

- **Agent Plugins 1.0** is the portable, cross-client standard from `agent-plugins.org`
- **Legacy Copilot Extensions** (GitHub App–based) were sunset November 10, 2025 — do not reference them
- The old `gh copilot` extension was deprecated October 25, 2025 — replaced by standalone `copilot` CLI
- Plugins are **file-based** — no compilation or build step required
- The SDK manages CLI process lifecycle automatically

## References

- `references/plugin-manifest.md` — Full manifest schema, fields, and validation
- `references/sdk-examples.md` — SDK usage in all 6 languages with custom tools, streaming, MCP
- `references/hook-lifecycle.md` — All 9 hook types with input/output signatures
- `references/marketplace-guide.md` — Creating and distributing through marketplaces
