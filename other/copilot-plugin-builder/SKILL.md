---
name: copilot-plugin-builder
description: "Author, scaffold, test, and distribute GitHub Copilot plugins — portable Agent Plugins 1.0 packages (skills + MCP servers) plus Copilot-specific components (agents, commands, rules, hooks) that run across Copilot CLI, VS Code/Agents Window, the GitHub Copilot desktop app, and the Copilot SDK. Use when the user wants to: (1) create or scaffold a new Copilot plugin, (2) add skills, agents, hooks, commands, or MCP servers to a plugin, (3) write or validate a plugin.json manifest, (4) distribute or install a plugin via a marketplace or Git repository, (5) test a local plugin in any Copilot runtime, (6) migrate a legacy Copilot-format plugin to Agent Plugins 1.0, (7) bump or sync plugin versions, or (8) build programmable plugins with @github/copilot-sdk. Covers the Agent Plugins 1.0 format (agent-plugins.org) and the legacy Copilot format. Do NOT use for Copilot CLI extensions (tools/commands/canvas via @github/copilot-sdk/extension) — use copilot-extension-builder instead."
metadata:
  version: 0.2.0
---

# Copilot Plugin Builder

Author GitHub Copilot plugins — packages of skills, agents, hooks, and MCP servers that install into Copilot CLI, VS Code (Agents Window), the GitHub Copilot desktop app, and the Copilot SDK.

Agent Plugins 1.0 went generally available on 2026-08-12 across VS Code, Copilot CLI, the Copilot SDK, and the Copilot app, on all Copilot plans. Build one package; compatible clients load the portable parts.

## Plugin Architecture

Plugins are **file-based** (markdown + JSON). No compilation required. Two Copilot formats:

| Format | Marker | Use |
|--------|--------|-----|
| **Agent Plugins 1.0** | `$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` | Recommended — portable across Copilot runtimes and other Agent Plugins clients |
| **Legacy Copilot** | No `$schema` | Still supported (no migration required); use only when custom component paths are needed |

Always use **Agent Plugins 1.0** unless the user has a specific reason for the legacy format.

### Portability model

| Component | Location (Agent Plugins 1.0) | Portable |
|-----------|------------------------------|----------|
| Skills | `skills/<name>/SKILL.md` | Yes — Agent Skills spec |
| MCP servers | `mcp.json` | Yes — MCP spec |
| Agents | `com.github.copilot/agents/*.agent.md` | No — Copilot namespace |
| Commands | `com.github.copilot/commands/` | No |
| Rules | `com.github.copilot/rules/` | No |
| Hooks | `com.github.copilot/hooks/hooks.json` | No |
| LSP servers | `com.github.copilot/lsp.json` | No |
| Automation templates | `automations/*.automation.md` (VS Code) | No |
| Canvases / other extensions | loaded by CLI and Copilot app | No |

Clients ignore namespaces they don't implement (for example `com.example.client/`), so Copilot-specific components never block portability.

## Directory Layout (Agent Plugins 1.0)

```text
my-plugin/
├── plugin.json                    # Required manifest (with Agent Plugins $schema)
├── skills/                        # Portable skills (immediate subdirectories only)
│   └── skill-name/
│       └── SKILL.md
├── mcp.json                       # Portable MCP server configs (fixed location)
├── automations/                   # VS Code automation templates (*.automation.md)
├── scripts/                       # Hook/MCP support files (referenced via ${PLUGIN_ROOT})
└── com.github.copilot/            # Copilot-specific components
    ├── agents/
    │   └── my-agent.agent.md
    ├── commands/
    ├── rules/
    ├── hooks/
    │   └── hooks.json
    └── lsp.json
```

Minimal plugin: just `plugin.json` + one component (for example a skill, agent, hook, command, MCP server, or LSP config).

## Workflow

### Phase 1: Gather Requirements

Ask the user these questions (one at a time, skip if already specified):

1. **What should the plugin do?** — Get a clear purpose statement
2. **Which components?** — Skills, agents, hooks, commands, MCP servers, or a combination
3. **Which runtimes?** — Copilot CLI, VS Code/Agents Window, Copilot app, SDK (drives the test matrix)
4. **Plugin name?** — 1–64 chars, lowercase ASCII letters, digits, hyphens, periods

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

Rules:

- Allowed top-level fields: `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `extensions`. Unknown fields are reported and ignored.
- `extensions` holds client-specific manifest data keyed by reverse-domain namespace (for example `"extensions": { "com.github.copilot": { ... } }`).
- In Agent Plugins 1.0, component locations are fixed — you cannot override them in `plugin.json`. Legacy format plugins may use component path fields instead.

Then author each component — see Phase 3 below.

### Phase 3: Author Components

#### Skills

Skills inject context/instructions into the agent via `SKILL.md`:

```markdown
---
name: my-skill
description: When and why to use this skill
---

# Instructions

Be concise. Use imperative form. Include only what the model doesn't already know.
```

Skills must be immediate subdirectories of `skills/`, and the directory name must match the frontmatter `name` (plain kebab-case, no namespace prefix — invalid names are silently skipped). Follow skill-creator patterns for scripts/, references/, assets/.

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

Hooks are client-specific and fire at lifecycle points. In Agent Plugins 1.0, create `com.github.copilot/hooks/hooks.json` (legacy format: `hooks.json` at the plugin root):

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      { "type": "command", "command": "./scripts/init.sh", "timeoutSec": 10 }
    ],
    "preToolUse": [
      { "type": "command", "command": "./scripts/validate.sh", "timeoutSec": 5 }
    ]
  }
}
```

Supported events: `agentStop`, `errorOccurred`, `notification`, `permissionRequest`, `postToolUse`, `postToolUseFailure`, `preCompact`, `preToolUse`, `sessionEnd`, `sessionStart`, `subagentStart`, `subagentStop`, `userPromptSubmitted`, `userPromptTransformed`. Use `timeoutSec` (default 30; `timeout` is an alias). For payloads, matchers, payload formats (camelCase vs PascalCase/VS Code-compatible), and SDK hook registration, see `references/hook-lifecycle.md`.

#### Automation templates (VS Code)

Reusable prompt + schedule templates in `automations/*.automation.md` with YAML frontmatter (`version`, `id`, `name`, `schedule`). Templates only seed the New Automation dialog — they cannot auto-start. Extra folders via `extensions.com.github.copilot.automations.paths`.

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

Transports: `stdio`, `streamable-http`, `sse` (deprecated). Variables: `${PLUGIN_ROOT}` (package root), `${PLUGIN_DATA}` (writable state that persists across updates). For `stdio`, Copilot CLI also provides these as environment variables.

### Phase 4: Install and Test

Test in every runtime the plugin targets. Hooks and MCP servers execute local code — review them before installing anything from a community marketplace.

**Copilot CLI:**

```bash
copilot plugin install ./my-plugin   # local install
copilot plugin list                  # verify loaded
```

Then in an interactive session: `/plugin list`, `/skills list`, `/agent`.

Components are cached — re-run `copilot plugin install ./my-plugin` after edits. Uninstall by the `name` field from `plugin.json`, not the directory path.

**VS Code / Agents Window:**

- Ensure `chat.plugins.enabled` is `true`.
- Install via Extensions view (`@agentPlugins`), Command Palette **Chat: Install Plugin From Source**, or the Agent Customizations editor's Plugins page.
- For local development, register the path with `chat.pluginLocations` (Experimental): `{ "/path/to/my-plugin": true }`.
- VS Code automatically discovers plugins installed by Copilot CLI from `~/.copilot/installed-plugins/` (marketplace subfolders plus a `_direct` bucket for Git-URL installs).
- Verify components appear: skills in **Configure Skills**, MCP servers in the tools list, agents in the picker, hooks fire on their events.

**Copilot app:** install from the `awesome-copilot` marketplace (registered by default).

**Copilot SDK:** load a plugin programmatically — see `references/sdk-examples.md`.

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

**Via marketplace:** users register and browse with:
```bash
copilot plugin marketplace add OWNER/REPO      # or a local path / .git URL
copilot plugin marketplace browse my-marketplace
copilot plugin install my-plugin@my-marketplace
```

In VS Code, marketplaces are configured with `chat.plugins.marketplaces` (shorthand `owner/repo`, `.git` URL, SCP-style remote, or `file:` URI; pin with `#<ref>` or a full 40-character commit SHA). Organizations govern plugins with `enabledPlugins`, `extraKnownMarketplaces`, and `strictKnownMarketplaces` in `managed-settings.json` across VS Code, CLI, the Copilot app, and Copilot cloud agent.

For marketplace schema, versioning, and distribution details, see `references/marketplace-guide.md`.

### Version Bump

When bumping a plugin's version, **always update both files atomically**:

1. `plugin.json` → `version` (source of truth)
2. `marketplace.json` → `plugins[name=X].version` (must mirror plugin.json)

These MUST match. Drift causes users to miss updates or install unexpected versions. See `references/marketplace-guide.md` → "Bump Procedure" for the full checklist including verification and commit steps.

## SDK Usage

The `@github/copilot-sdk` provides programmatic control via JSON-RPC. Supports 6 languages: TypeScript, Python, Go, .NET, Rust, Java. Agent Plugins 1.0 support is generally available in the SDK.

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

For SDK examples in all languages, custom tools, streaming, plugin loading, and MCP configuration, see `references/sdk-examples.md`.

## Component Reference

| Component | Format | Location (Agent Plugins 1.0) | Portable | Purpose |
|-----------|--------|------------------------------|----------|---------|
| Skill | `SKILL.md` | `skills/<name>/SKILL.md` | Yes | Inject context/instructions |
| MCP Server | `mcp.json` | `mcp.json` | Yes | External tool providers |
| Agent | `.agent.md` | `com.github.copilot/agents/*.agent.md` | No | Scoped sub-agents |
| Command | `.md` | `com.github.copilot/commands/` | No | `/` slash commands |
| Rule | — | `com.github.copilot/rules/` | No | Standing instructions |
| Hook | `hooks.json` | `com.github.copilot/hooks/hooks.json` | No | Lifecycle callbacks |
| LSP Server | `lsp.json` | `com.github.copilot/lsp.json` | No | Language server integration |
| Canvas / extension | — | `com.github.copilot/` namespace | No | Loaded by Copilot CLI and the Copilot app |
| Automation | `.automation.md` | `automations/` (VS Code) | No | Prompt + schedule templates |

## Key Concepts

- **Agent Plugins 1.0** is the open, vendor-neutral standard from `agent-plugins.org` (spec: `github/agentplugins/agent-plugins-spec`); GA 2026-08-12 across VS Code, Copilot CLI, Copilot SDK, and the Copilot app
- Portable core = `skills/` + `mcp.json`; everything Copilot-specific lives under the `com.github.copilot/` namespace
- Legacy Copilot-format plugins remain supported — no migration required; migrate only for portability or to adopt fixed component locations
- Legacy **Copilot Extensions** (GitHub App–based tools/commands/canvas platform) were sunset November 10, 2025 — do not build new ones on it
- Plugins are **file-based** — no compilation or build step required
- Hooks and MCP servers run code on the user's machine — review before installing from community marketplaces
- The SDK manages CLI process lifecycle automatically

## Authoritative Sources

- [Agent Plugins specification](https://agent-plugins.org/) — portable format, schemas, governance
- [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins) — discovery, install, marketplaces, settings, troubleshooting
- [Agent plugin authoring reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference) — manifest fields, formats, hooks, automations, cross-tool compatibility
- [Agent Plugins 1.0 changelog (2026-08-12)](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/) — GA scope, migration, enterprise settings
- [Finding and installing plugins (Copilot CLI)](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) — CLI install/marketplace commands
- [Creating a plugin (Copilot CLI)](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating) — format selection, structure, test loop
- [GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference) — hook events, payloads, command-hook format

## References

- `references/plugin-manifest.md` — Full manifest schema, fields, and validation
- `references/sdk-examples.md` — SDK usage in all 6 languages with custom tools, streaming, plugin loading, MCP
- `references/hook-lifecycle.md` — All hook events with input/output signatures
- `references/marketplace-guide.md` — Creating and distributing through marketplaces
