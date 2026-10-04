---
name: working-with-serena
description: |
  MANDATORY before reading or editing any code file. Use when working with Serena — the MCP
  toolkit (github.com/oraios/serena) that wraps Language Servers to give symbol-level code
  retrieval and editing — or any time you are about to Read/Edit/Write a code OR config/data
  file, Grep/Glob for a symbol, plan a refactor, configure the Serena MCP server, or wire
  Serena Hooks. Covers the `serena`/`serena-hooks` CLIs, MCP server setup (contexts/modes,
  `--context claude-code`), the full tool set, a Serena↔native tool mapping with rationale,
  agent flows (search/understand/edit/refactor/debug), a cookbook, and the tool-compliance
  problem (newer Claude models drift off Serena's tools toward native ones — Serena Hooks +
  a custom config-file hook counteract it). Do NOT Read+Edit a code file — use
  `find_symbol` + `replace_symbol_body`. Supersedes the older `using-serena` skill.
metadata:
  last_updated: "2026-06-16"
---

# Working with Serena

Serena is an MCP server that wraps **Language Servers (LSP)** to give an agent **symbol-level**
operations on code: find a function by name, read just that symbol's body, replace it at exact AST
boundaries, rename it across the whole codebase, find every reference. It replaces the blunt
`Read` → `Grep` → `Edit` loop with precise, token-cheap, structurally-safe calls.

Tool names in this environment: `mcp__plugin_serena_serena__<tool>` (e.g.
`mcp__plugin_serena_serena__find_symbol`). Load them with `ToolSearch("serena find_symbol replace_symbol")`.

## STOP — pre-edit mandatory checklist

**Before touching any code file, complete this sequence:**

1. Project active? If not → `activate_project(project="<name or path>")`. First time in a repo →
   `onboarding()`.
2. Understand a file → `get_symbols_overview`, **not** `Read`.
3. Find a function/class → `find_symbol` (with `include_body=true` when you need the code),
   **not** `Grep` + `Read`.
4. Edit a function → `replace_symbol_body`, **not** `Read` + `Edit`.
5. Add code near a symbol → `insert_before_symbol` / `insert_after_symbol`, **not** `Read` + `Edit`.

```
❌  Read file → understand code → Edit file
✅  get_symbols_overview → find_symbol(include_body=true) → replace_symbol_body
```

If you catch yourself about to `Read` a `.py`/`.ts`/`.js`/`.go`/`.rs`/`.java` file — stop and use
`find_symbol` or `get_symbols_overview`. **This applies to config/data/doc files too** (`.json`,
`.yaml`, `.toml`, `.md`, `.sql`, …): prefer `search_for_pattern` for targeted lookup, and
`get_symbols_overview`/`find_symbol` for the many formats Language Servers support (JSON, YAML,
Bash, Markdown, TOML, and more). Repeatedly `Read`-ing whole config files is the same anti-pattern.

## Why Serena beats the blunt tools

- **Token efficiency** — `find_symbol` returns one symbol, not a 2,000-line file. `get_symbols_overview`
  gives you a file's structure for a fraction of a full read.
- **Structural accuracy** — `replace_symbol_body` targets exact symbol boundaries via the LSP. No
  line-number guessing, no "the file changed since you read it" races.
- **Safe refactoring** — `rename_symbol` does a real cross-codebase LSP rename; `find_referencing_symbols`
  finds every caller before you change a signature; `safe_delete_symbol` checks for remaining usages.
- **Fewer round-trips** — one symbolic call replaces a `Read` → `Grep` → `Edit` chain.

Full version, with token math: [`references/guides/why-serena.md`](references/guides/why-serena.md).

## Tool mapping (summary)

| Task | ❌ Native | ✅ Serena |
|---|---|---|
| Find a function/class | `Grep` + `Read` | `find_symbol` |
| Understand file structure | `Read` whole file | `get_symbols_overview` |
| Find all references / callers | `Grep` name | `find_referencing_symbols` |
| Edit a function body | `Read` + `Edit` | `replace_symbol_body` |
| Add code near a symbol | `Read` + `Edit` | `insert_before_symbol` / `insert_after_symbol` |
| Rename across codebase | `Grep` + multi-file `Edit` | `rename_symbol` |
| Delete a symbol safely | `Read` + `Edit` | `safe_delete_symbol` |
| Regex / text search | `Grep` | `search_for_pattern` |
| Diagnostics (errors/warnings) | run build, parse output | `get_diagnostics_for_file` |
| Persist cross-session notes | scratch files | `write_memory` / `read_memory` |

Full mapping + legitimate fallbacks: [`references/guides/tool-mapping.md`](references/guides/tool-mapping.md).

## The compliance problem (why hooks exist)

Newer Claude models — especially the Opus line — are trained so heavily on their built-in tools that
they **drift off** Serena's, particularly in long sessions and under Claude Code's dynamic tool
loading. Serena's own docs note CC's built-in tool descriptions consume ~16k tokens and bias the
model so strongly that it can be "almost impossible to convince Opus to use Serena" without
intervention. The fix is **enforcement via hooks**, plus the `--context claude-code` flag and the
`serena prompts print-cc-system-prompt-override` system prompt. Joe runs upstream **Serena Hooks**
(`serena-hooks remind/auto-approve/activate/cleanup`) **and** a custom hook that extends the nudge to
config/data/doc file types Serena Hooks omits. See [`references/guides/hooks.md`](references/guides/hooks.md).

## Quick reference

| Need to… | Read |
|---|---|
| Be sold on Serena vs native tools (token math, drift) | [`references/guides/why-serena.md`](references/guides/why-serena.md) |
| Map every Serena tool ↔ native tool, with fallbacks | [`references/guides/tool-mapping.md`](references/guides/tool-mapping.md) |
| Pick a flow: search / understand / edit / refactor / debug | [`references/guides/agent-flows.md`](references/guides/agent-flows.md) |
| Copy-paste recipes (rename, add method, find callers, onboard) | [`references/guides/cookbook.md`](references/guides/cookbook.md) |
| Set up the MCP server (contexts, modes, `--context claude-code`) | [`references/guides/mcp-setup.md`](references/guides/mcp-setup.md) |
| Enforce tool use with Serena Hooks + the custom config-file hook | [`references/guides/hooks.md`](references/guides/hooks.md) |
| `serena` / `serena-hooks` CLI reference (version-exact) | [`references/cli/`](references/cli/) |
| Official Serena docs (tools list, configuration, workflow) | [`references/docs/`](references/docs/) |

The full, authoritative tool list (with optional/BETA flags) is fetched at
[`references/docs/01-about__035_tools.md`](references/docs/01-about__035_tools.md).
