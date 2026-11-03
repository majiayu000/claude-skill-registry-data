---
name: copilot-extension-builder
description: "Build custom Copilot extensions — tools, slash commands, and canvas UI surfaces — as Node.js/JavaScript modules using @github/copilot-sdk/extension. Extensions run in GitHub Copilot CLI (experimental) and the GitHub Copilot app; canvas extensions are documented for the Copilot app and VS Code, where they render as 'Canvases' (Agents window and Chat view, Copilot harness). Use when the user asks to: (1) create a new Copilot extension, (2) add a tool for Copilot to call, (3) add a /slash command, (4) build an interactive canvas (Copilot app, VS Code Agents window/Chat view, or experimental CLI), (5) enable experimental extensions in Copilot CLI, (6) scaffold extension boilerplate, or (7) troubleshoot/debug extension errors. Do NOT use for general Copilot customization (skills, agents, hooks, MCP servers, plugins) — those are separate concern areas. Do NOT use for classic VS Code IDE extensions (webviews) — Copilot canvas extensions are a different, SDK-hosted primitive."
metadata:
  version: 0.2.1
---

# Copilot Extension Builder

Build custom Copilot extensions. An extension is a JavaScript module that runs as a separate Node.js process alongside an interactive session and connects through the extension SDK bundled with the host, adding tools (agent-invoked), slash commands (user-invoked), and canvas UIs (shared interactive surfaces).

Extensions are supported in **GitHub Copilot CLI** (experimental) and the **GitHub Copilot app**. Canvas extensions are documented for the Copilot app (right side panel) and for VS Code, where they surface as **Canvases** in the Agents window and Chat view; canvas rendering in Copilot CLI is SDK-level but not covered by the official docs — treat it as experimental. All extensions are distinct from IDE extensions (such as the Copilot extension installed in an editor) and from the retired GitHub App-based Copilot Extensions integration.

## Quick Reference

| Extension Type | Visible To | Use Case |
|---|---|---|
| **Tool** | Copilot agent | Add functions the agent calls autonomously |
| **Command** | User | Add `/slash` commands the user invokes |
| **Canvas** | Agent + User | Interactive shared UI (side panel in CLI/app, editor tab in VS Code) |
| **Mixed** | Both | Combine tools, commands, and/or canvases |

## Choose the Right Customization

The distinction is the capability needed, not where it is installed:

| Need | Start with |
|---|---|
| A repeatable workflow expressed as instructions and resources | An agent skill |
| Access to tools exposed by an external service | An MCP server |
| A command at a defined agent lifecycle event | A hook |
| Session-aware tools or slash commands implemented in JavaScript | An extension (this skill) |
| A distributable bundle of related capabilities | A plugin |

> **Security:** Extensions execute on the user's machine with their privileges. Only load extension code that is trusted, like any other script.

## Canvas Correlation: Copilot CLI ↔ VS Code Agents Window

A canvas built with this skill is the same primitive the VS Code **Agents window** (and Chat view) surfaces as a "Canvas" — the Copilot harness in VS Code runs on the GitHub Copilot SDK, the same foundation as Copilot CLI and the Copilot app. One canvas extension works across all three hosts; only the host's renderer differs.

What stays identical everywhere:
- Authoring contract: `createCanvas()` plus `joinSession({ canvases, requestCanvasRenderer: true })` (see Phase 2 and `assets/templates/canvas-extension.mjs`).
- Agent-facing tools: `list_canvas_capabilities`, `open_canvas`, `invoke_canvas_action`, addressed by `canvasId` + `instanceId`.
- Scope locations: personal `~/.copilot/extensions/NAME/`, repository `.github/extensions/NAME/`, or bundled in a plugin.

What differs per host:

| Host | Canvas renders as | Requirements |
|---|---|---|
| Copilot CLI | Side panel via canvas renderer (SDK-level, not documented in official CLI docs) | `--experimental` / `/experimental on`; treat CLI canvas as experimental |
| GitHub Copilot app | Right side panel | Installed canvas extension or chat plugin |
| VS Code Agents window / Chat view | Editor tab tied to the owning chat (Agents window: **Add Tab (+)** > **Canvas**) | Setting `chat.canvases.enabled` on; desktop only, local Copilot Agent Host sessions |

VS Code notes:
- Users can open a canvas themselves via **Add Tab (+)** > **Canvas** (Agents window) or **New Chat (+)** > **Canvas** (editor window) without asking the agent; dismissed live canvases can be reopened from the same menu.
- The built-in `/create-canvas` skill can scaffold a canvas extension directly in a workspace; sample canvas extensions live at https://awesome-copilot.github.com/extensions/.
- No VS Code-specific code is required — ship the same `extension.mjs`; VS Code hosts render it natively.

## Workflow

### Phase 1: Gather Requirements

Ask the user these questions (one at a time):

1. **What should the extension do?** — Get a clear description
2. **What type?** — Tool, command, canvas, or mixed?
3. **Where should it live?** — `~/.copilot/extensions/NAME/` (user, all sessions) or `.github/extensions/NAME/` (project, shared with repo)

If the user is unsure about type, suggest the simplest option that meets their need.

Extract from the current session context if the user doesn't specify (e.g., they're building something the session is working on).

### Phase 2: Choose Extension Type and Create File

**File structure (both locations):**
```
NAME/
  extension.mjs      ← Entry point (required; .mjs recommended — .js/.cjs also accepted, no TypeScript)
```

**The `@github/copilot-sdk/extension` import is auto-resolved** — no `package.json` or `npm install` needed.

**Lifecycle:** the extension process is long-lived within a session, but module-level state is in-memory — it resets on extension reload, `/clear`, or CLI restart. Persist to disk if state must survive.

#### Tool Extension

Use when Copilot needs to call a function autonomously. See `assets/templates/tool-extension.mjs` for the full template.

Key properties for `Tool` objects:
- `name` — Unique name across all extensions
- `description` — What it does; affects when agent calls it
- `parameters` — JSON Schema for arguments
- `handler` — Async function `(args, invocation) => result`
- `skipPermission` — `false` (default) prompts per call; `true` skips per-call prompts after a one-time per-extension grant (`--allow-tool='extension-permission-access(user:NAME)'`) — use only for read-only, low-risk tools
- `defer` — `"never"` keeps tool always visible; `"auto"` allows lazy-loading

#### Command Extension

Use when the user needs `/slash` commands. See `assets/templates/command-extension.mjs`.

Key properties for `CommandDefinition`:
- `name` — Command name without leading `/`
- `description` — Picker description
- `handler` — Async `(ctx) => void`; `ctx.args` is the argument string

Use `session.log(message, { level: "info" | "warning" | "error" })` for output.

#### Canvas Extension

Use when the extension needs a visual side-panel UI. See `assets/templates/canvas-extension.mjs`.

The agent gets three synthetic tools: `list_canvas_capabilities`, `open_canvas`, `invoke_canvas_action`.

Key structure for `createCanvas()`:
- `id`, `displayName`, `description` — Metadata
- `inputSchema` — JSON Schema for open input
- `actions[]` — `{ name, description, inputSchema, handler }`; names must NOT start with `canvas.`
- `open` — Async `(ctx) => ({ url, title?, status? })`; must be idempotent
- `onClose` — Optional cleanup callback

Set `requestCanvasRenderer: true` on `joinSession()` — it asks the host to attach a canvas renderer and register the three agent-facing canvas tools. Always include it: some older samples omit it, and without it the canvas may not appear.

For rich patterns (session bridging, bidirectional agent communication, live event subscriptions, hooks), see `references/extension-patterns.md`.

#### Mixed Extension

Combine tools, commands, and/or canvases in a single `joinSession()` call. See `assets/templates/mixed-extension.mjs`.

### Phase 3: Enable Experimental Mode

Copilot CLI extensions are experimental. The user must run **one** of:

| Option | Command |
|---|---|
| Startup flag | `copilot --experimental` |
| Session slash | `/experimental on` (inside interactive session) |

Users also control whether extensions run at all and whether the agent can manage them (extension modes in the Copilot CLI reference). Copilot app and VS Code hosts do not use the CLI's experimental flag.

### Phase 4: Test and Debug

**Load/reload the extension:**
| Method | Action |
|---|---|
| Ask Copilot | `Reload my extensions` (requires Load & Augment mode) |
| `/clear` | Starts fresh session, reloads extensions from disk |
| Restart CLI | Quit and restart |

**Verify it's running:**
```copilot
/extensions manage
```

**Check logs:**
- Logs: `~/.copilot/logs/extensions/NAME.log`
- `/extensions manage` shows status and log path

**Common issues:**

| Issue | Resolution |
|---|---|
| `stdout is reserved for JSON-RPC` | Replace `console.log()` with `session.log()` |
| Tool name collision | Ensure tool `name` is unique across all extensions |
| Extension not loading | Check `extension.mjs` syntax; run `/extensions manage` to inspect |
| Canvas not appearing | Ensure `requestCanvasRenderer: true` in `joinSession()` |
| `open` not re-entrant | Make `open` handler idempotent (same instanceId may re-open after reconnect) |
| Canvas action name rejected | Action names must NOT start with `canvas.` |

### Phase 5: Distribute

Choose scope by who needs the capability:

| Scope | Location | Sharing |
|---|---|---|
| **Personal** | `~/.copilot/extensions/NAME/extension.mjs` | Your sessions only |
| **Repository** | `.github/extensions/NAME/extension.mjs` | All repo contributors |
| **Plugin** | Bundle in `plugin.json` manifest | Marketplace-distributable |

To share with a team: move from `~/.copilot/extensions/NAME/` to `.github/extensions/NAME/` in the repo. A canvas extension created in the Copilot app may also include a `package.json` (metadata and dependencies) and an optional `artifacts/` directory for persisted canvas state alongside `extension.mjs`.

For full plugin packaging, see the plugins documentation (separate concern).

## API Reference

For complete API types (Tool, CommandDefinition, CanvasAction, CopilotSession, events, hooks), see `references/api-reference.md`.

For real-world extension patterns from `github/awesome-copilot`, see `references/extension-patterns.md`.

For template source files, see `assets/templates/`.
