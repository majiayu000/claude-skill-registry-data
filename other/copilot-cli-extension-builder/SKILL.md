---
name: copilot-cli-extension-builder
description: "Build custom GitHub Copilot CLI extensions — tools, slash commands, and canvas UI surfaces. Use when the user asks to: (1) create a new Copilot CLI extension, (2) add a tool for Copilot to call, (3) add a /slash command, (4) build an interactive canvas side-panel, (5) enable the experimental extensions feature, (6) scaffold extension boilerplate, or (7) troubleshoot/debug extension errors. Do NOT use for general Copilot customization (skills, agents, hooks, MCP servers, plugins) — those are separate concern areas. Covers Node.js/JavaScript extensions using @github/copilot-sdk/extension on the Copilot CLI."
metadata:
  version: 0.1.0
---

# Copilot CLI Extension Builder

Build custom GitHub Copilot CLI extensions. Extensions are Node.js modules that connect to the CLI over JSON-RPC via stdio, adding tools (agent-invoked), slash commands (user-invoked), and canvas side-panels (interactive UI).

## Quick Reference

| Extension Type | Visible To | Use Case |
|---|---|---|
| **Tool** | Copilot agent | Add functions the agent calls autonomously |
| **Command** | User | Add `/slash` commands the user invokes |
| **Canvas** | Agent + User | Interactive side-panel UI with rich HTML |
| **Mixed** | Both | Combine tools, commands, and/or canvases |

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
  extension.mjs      ← Entry point (required, .mjs only)
```

**The `@github/copilot-sdk/extension` import is auto-resolved** — no `package.json` or `npm install` needed.

#### Tool Extension

Use when Copilot needs to call a function autonomously. See `assets/templates/tool-extension.mjs` for the full template.

Key properties for `Tool` objects:
- `name` — Unique name across all extensions
- `description` — What it does; affects when agent calls it
- `parameters` — JSON Schema for arguments
- `handler` — Async function `(args, invocation) => result`
- `skipPermission` — `true` skips approval prompt
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

Set `requestCanvasRenderer: true` on `joinSession()`.

For rich patterns (session bridging, bidirectional agent communication, live event subscriptions, hooks), see `references/extension-patterns.md`.

### Phase 3: Enable Experimental Mode

Extensions are experimental. The user must run **one** of:

| Option | Command |
|---|---|
| Startup flag | `copilot --experimental` |
| Session slash | `/experimental on` (inside interactive session) |

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

| Scope | Location | Sharing |
|---|---|---|
| **User-level** | `~/.copilot/extensions/NAME/extension.mjs` | Your sessions only |
| **Project-level** | `.github/extensions/NAME/extension.mjs` | All repo contributors |
| **Plugin** | Bundle in `plugin.json` manifest | Marketplace-distributable |

To share with a team: move from `~/.copilot/extensions/NAME/` to `.github/extensions/NAME/` in the repo.

For full plugin packaging, see the plugins documentation (separate concern).

## API Reference

For complete API types (Tool, CommandDefinition, CanvasAction, CopilotSession, events, hooks), see `references/api-reference.md`.

For real-world extension patterns from `github/awesome-copilot`, see `references/extension-patterns.md`.

For template source files, see `assets/templates/`.
