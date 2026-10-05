---
name: zvec-grep
description: "Index and semantically search the local workspace with zvec-grep (zg). Use when mcp__zvec_grep__zvec_grep_search is missing, a search says there is no index, zvec_index status says not ready, or the user asks to index this repo. Exact words/regex/filenames stay on native grep/glob."
---

# zvec-grep

Load this when local workspace search needs **meaning**, not an exact string — or when `mcp__zvec_grep__zvec_grep_search` is missing / returns "no index". Typical triggers: "where is X handled?", "what did we decide about Y?", "index this repo", "zg not found".

Do **not** load this for exact identifiers, quotes, filenames, regexes, or exhaustive hit lists — those are native `grep` / `glob`. Do **not** use zg for open-web or literature search (`consensus_search` / `parallel_search` / Firecrawl).

## Install the CLI

The plugin already installs `zg` into `~/.dsh/zvec-grep` on the first ResearchCraft start. **Do not** `npm i -g @zvec/zvec-grep` and **do not** ask the user to restart `dsh` unless `mcp__zvec_grep__zvec_grep_search` is still missing after that first start.

Only if the tool is absent (install failed or `ZVEC_GREP_SKIP_INSTALL=1`):

```bash
npm install --prefix "${DSH_HOME:-$HOME/.dsh}/zvec-grep" --no-fund --no-audit @zvec/zvec-grep
```

then tell the user to restart `dsh`. Override with `ZVEC_GREP_CLI` if they already have a `zg` binary. Do not keep a long-lived `npx @zvec/zvec-grep` as the MCP server.

## Index

Session-start indexing is **off by default** (Settings → Index at session start). The user can turn it on there, or ask in chat at any time. While an index runs, the UI shows a progress bar with estimated time and Cancel; there is no timeout.

**Never** shell out to `zg index`. Use the native tool:

```
zvec_index  action=status   # ready, auto_index, live progress
zvec_index  action=start    # blocks until done or cancelled; user can cancel in the UI
zvec_index  action=cancel
```

**Never** `zg index --drop` or `--rebuild` unless the user asked. **Never** index `$HOME` or `/`.

If semantic search would improve the answer and `status` says `ready` is false:

1. If the user already asked to index, or already said yes this turn → `action=start`.
2. Else if `auto_index` is true → `action=start` (joins a session-start job, or starts one).
3. Else → `ask_user_question` with two choices: **Yes, index now** (recommended) / **No, keep using exact grep/glob only**. Only `action=start` if they pick yes.

Do not start indexing silently when auto-index is off. After start succeeds, call `mcp__zvec_grep__zvec_grep_search`, not `zg query`.

## Search

Every MCP call needs an **absolute** `root` equal to the session working directory. Relative `root` fails. Do not point `root` outside the workspace unless the user named another tree.

```json
{
  "root": "/absolute/path/to/workspace",
  "query": "decision history behind the launch date",
  "limit": 5
}
```

Optional: `fts` (lexical constraints), `vector` (semantic-only), `fuse`, `globs`, `limit` (max 50). When the user asks whether conceptually related local material exists and you have no exact anchor, make **at most one** focused probe and stop if the hits are irrelevant.

Exact follow-up (a symbol, a quoted string, a path) goes back to native `grep`.

## Remote embedding (ask first)

Default is local. A remote Qwen model sends query text / workspace fragments off-machine and needs `ZVEC_GREP_API_KEY` (or `DASHSCOPE_API_KEY`) **and** an explicit workspace grant. DSH does not show zg's MCP permission form.

If a search errors about remote embedding authorization, call `ask_user_question` with exactly three choices:

1. Allow Remote Embedding for this workspace (`zg auth grant`)
2. Stay local (FTS / local model only) — retry without vector routes
3. Cancel

Do not collect a token, API key, or password in that question. Only after (1) run:

```bash
zg auth grant "$(pwd)" --capability embedding --scope workspace
```

then retry the original MCP search once. In a headless situation where you cannot ask, stop without granting.

## CLI cheat sheet

`zg help` / `zg help query` / `zg help index` are authoritative over anything below.

```
zvec_index action=status|start|cancel             # agents: native tool, not the CLI
zg status --check-ready
zg query "where theme preferences are restored"   # human/CLI; agents prefer the MCP tool
zg query --rg -F "loadTheme" src                  # exhaustive rg; agents prefer native grep
zg server status --check-ready
```

The plugin starts `zg server on` when the ResearchCraft preset mounts and talks to the loopback daemon over HTTP (`http://127.0.0.1:7999/mcp`), not `zg server --stdio`. Stopping `dsh` runs `zg server off`. Do not leave a long-lived daemon running for this plugin, and do not `zg server off` while DSH is still up unless the user asked.
