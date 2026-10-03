---
name: ai-harness
description: AI layer embeds the Pi SDK. Load when touching AI module, harness integration, providers, MCP decision, or chat UI.
triggers:
  - ai
  - llm
  - harness
  - pi
  - "pi-agent-core"
  - "pi-ai"
  - mcp
  - skill
  - extension
  - claude
  - openai
  - ollama
---

# AI Harness — embeds Pi SDK

We do **not** build our own agent runtime. We embed [earendil-works/pi](https://github.com/earendil-works/pi) as the AI layer.

## Why Pi

Pi is the minimalist coding harness by Mario Zechner. Its philosophy is identical to what we wrote in [`culture`](../culture/SKILL.md): 4 tools, no spaceships, skills via npm/git. Adopting it instead of reinventing reduces our code, reuses an existing ecosystem of Pi Packages, and keeps the cultural fit.

## Packages we depend on

| Package | Purpose |
|---|---|
| [`@earendil-works/pi-agent-core`](https://www.npmjs.com/package/@earendil-works/pi-agent-core) | General-purpose agent runtime: transport, state management, attachments |
| [`@earendil-works/pi-ai`](https://www.npmjs.com/package/@earendil-works/pi-ai) | Unified LLM API with model discovery and provider config |
| [`@earendil-works/pi-coding-agent`](https://www.npmjs.com/package/@earendil-works/pi-coding-agent) | Coding agent with Read/Bash/Edit/Write + session management. SDK mode: `createAgentSession(...)` |
| [`@earendil-works/pi-tui`](https://www.npmjs.com/package/@earendil-works/pi-tui) | TUI library with differential rendering (optional, for future TUI mode) |

Pi runs in four modes: interactive, print/JSON, RPC, and **SDK for embedding**. We use the SDK mode.

## Core tools (provided by Pi)

`pi-coding-agent` ships these built-in. We do **not** reimplement:

- **`Read(path)`** — file with line numbers, gitignore-aware
- **`Write(path, content)`** — refuses to overwrite
- **`Edit(path, old, new)`** — exact-string replace
- **`Bash(command, cwd?)`** — streaming command execution

Everything else (web search, image gen, planning, etc.) is a **Pi Package** (a Skill or Extension), not a built-in.

## Multi-provider (delegated to `pi-ai`)

Provider config lives in `pi-ai`. Supported (current list — check upstream): Anthropic, OpenAI, OpenAI-compat (Ollama, MLX server), Groq, Cerebras, XAI, and more.

Our job is to expose Settings UI that writes Pi's provider config (or pass it programmatically when we instantiate the session).

## MCP decision (DEFERRED — see epic #15)

**Pi explicitly rejects native MCP.** From the upstream README:

> *"No MCP. Build CLI tools with READMEs (see Skills), or build an extension that adds MCP support."* — [Mario Zechner: What if you don't need MCP?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)

This is a deliberate philosophical choice. Pi's stance: most "tools" are better expressed as CLI binaries with `--help` text the agent can read, rather than as MCP servers.

For nyxterm we have three options. **Do not pick one in this skill — that's a decision for epic #15**:

1. **Skills-as-CLIs** (the Pi way): replace MCP servers with CLI wrappers. Example: instead of `engram` as MCP server, ship an `engram` CLI binary; instead of `context7` MCP, write a thin CLI fetcher. The agent uses `Bash` to invoke them. Pro: aligned with Pi. Con: re-implements MCP work the user already did in their dotfiles.
2. **MCP support as an opt-in Pi extension**: build (or wait for) a Pi extension that adds an `Mcp` tool. Pro: MCP servers (`engram`, `context7`, etc.) keep working. Con: we own that extension.
3. **MCP support as a nyxterm-native module** (separate from Pi): nyxterm manages MCP server lifecycle and exposes their tools to the Pi agent via a custom adapter. Pro: full control, MCP servers persist across restarts as nyxterm-managed processes. Con: more code on our side; arguably violates Pi minimalism.

Pick the option in epic #15. Until then, this skill stays agnostic.

## Skills and extensions (Pi terminology)

Pi has its own extension system. We **reuse** it; we don't build a parallel one.

- **Skills**: prompt templates + scoped knowledge. Distributed as npm/git packages.
- **Extensions**: TypeScript code that adds tools or hooks. Distributed the same way.

For nyxterm-specific behavior (e.g., theme-aware output, pane-aware Bash routing, Engram memory injection), we publish our own Pi Packages under `@nyxterm/pi-*`.

This means epic #21 ("Plugin / extension API") **shrinks**: we don't design our own API; we contribute upstream-shaped packages to Pi's ecosystem and document how nyxterm-flavored extensions are loaded.

## Context injection

Before sending each request, we inject:

```xml
<env>
  <workspace-root>...</workspace-root>
  <active-pane-cwd>...</active-pane-cwd>
  <git-branch>...</git-branch>
  <git-dirty>...</git-dirty>
  <privacy-mode>...</privacy-mode>
</env>
<project-memory>
  <!-- top relevant Engram observations, cap 8 KB -->
</project-memory>
```

Implementation: we hook into Pi's session via the SDK (likely via a pre-request hook or a custom extension that runs before the LLM call). Specifics TBD when the harness is wired in epic #12.

## Streaming

`pi-coding-agent` streams tool calls and text deltas natively. The chat UI binds to those streams. No buffering.

## What we explicitly DON'T do

- **No custom agent runtime.** We use `pi-agent-core` + `pi-coding-agent`.
- **No reinvention of multi-provider.** `pi-ai` already does it.
- **No sub-agents in core.** Pi rejects them; so do we. If a user wants sub-agents, they spawn another `nyxterm` window (or tmux pane) running another Pi session.
- **No auto-mode without confirmation for destructive Bash.** Every `rm`, `git reset`, `git push --force` requires a confirm UI on top of Pi's tool-call event.
- **No built-in RAG.** A Pi Package can index a project, but core does not pre-process.

## UI

- **Chat panel** — side pane, toggleable, Tokyo Night themed, Markdown + code blocks, tool-call cards, streaming.
- **AI command palette** (`Ctrl+;`) — NL → bash via a Pi Skill that constrains output to a single shell command. User reviews + Enter to run.
- **Output explainer** (Phase 2 stretch) — right-click block of stderr → "Explain this" sends to Pi with a "explain output" prompt template.

## Safety

- Wrap `Bash` tool calls with a nyxterm confirm UI for destructive patterns (configurable allowlist in Settings).
- `Write` outside workspace → explicit user confirm.
- API keys go to OS keychain (Secret Service / Keychain / WinCred). Never logged. Stream traces redact known key patterns.

## Implementation pointers (when starting epic #12)

- `createAgentSession({...})` from `pi-coding-agent` is the entry point. See `packages/coding-agent/docs/usage.md` upstream.
- `pi-ai` exposes provider config via constructor args or env vars — we want programmatic config from Settings, so pass them in code, not env.
- Pi Packages live in `~/.config/pi/` (upstream default). We may want a nyxterm-scoped location too — confirm during integration.
- We run Pi in-process (Node) via Tauri's sidecar pattern, OR we embed it via WASM/N-API. Decide in epic #12 spec phase.
