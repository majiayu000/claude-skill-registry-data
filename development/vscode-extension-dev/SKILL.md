---
name: vscode-extension-dev
description: Conventions for working on this LocalPilot VS Code extension codebase — build/test commands, architecture map, and where to add providers, tools, or UI features.
---

# Working on LocalPilot

## Commands
- Type-check + lint + bundle: `npm run compile`
- Offline logic tests (mock Ollama/OpenAI servers, agent loop): `npm run smoke`
- Launch the extension host: VS Code `Run Extension` (F5)

## Architecture map
| Area | Path | Notes |
|---|---|---|
| Model backends | `src/providers/` | `ollama.ts` (native API), `openaiCompat.ts` (LM Studio, llama.cpp, vLLM…), `registry.ts` resolves `provider/model` ids |
| Agent loop | `src/agent/agentLoop.ts` | model ⇄ tools loop, parallel tool execution, text-protocol fallback |
| Subagents & skills | `src/agent/subagents.ts`, `src/agent/skills.ts` | `run_subagent`, `run_parallel_subagents`, `load_skill` |
| Context window | `src/context/contextManager.ts` | prune → summarise → truncate |
| Tools | `src/tools/*.ts` | each exports `Tool[]`; register in `src/extension.ts` |
| UI | `src/ui/`, `media/chat.{js,css}` | webview controller, chat participant, LM provider, inline completions |
| MCP | `src/mcp/mcpManager.ts` | stdio JSON-RPC client |

## Adding a tool
1. Create `src/tools/<name>.ts` exporting a `Tool` with a JSON-schema `definition`.
2. Mark `parallelSafe: true` if read-only; set `approvalKind` for anything mutating.
3. Add it to the `registerAll` call in `src/extension.ts`.
4. Add a `toolSummary` case in `media/chat.js` for a nice label.

## Adding a provider type
Implement `LLMProvider` from `src/types.ts`, then branch on `cfg.type` in `createProvider()` in `src/providers/registry.ts` and extend the `enum` in `package.json` → `localpilot.providers`.
