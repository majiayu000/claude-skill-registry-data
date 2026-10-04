---
name: mcx
description: Required routing guide and CLI reference for mcx. MUST be invoked when an mcx hook says to evaluate routing, before a second related MCP call, or after a bloated MCP result. Uses an existing chain when available, routes ephemeral optimizations to /mcx:new, explicit persistence to /mcx:save, or takes a narrow isolated-call exception. Covers forward, ad-hoc run, registered chains, filters, and diagnostics.
---

# mcx cheatsheet

mcx is an MCP **client** CLI. It exists to keep large MCP tool output from flooding
the context window, via two registries:

| Registry | What | How it runs |
|---|---|---|
| **Filters** | declarative JSON reshaping of a tool's result (drop/keep/rename/truncate) | **automatic** — a PostToolUse hook runs `mcx filter` on every MCP result |
| **Chains** | a script that orchestrates several MCP calls and returns a digest | **on purpose** — run a script path ad hoc or a saved chain by name |

Rule of thumb: **filters** cut cruft from a single call (they just happen).
**chains** collapse a fan-out (many calls, or a cross-service join) into one call
whose only context cost is the digest.

## Routing gate

When an mcx hook invokes this skill, do not read the cheatsheet and then resume
the same direct-MCP pattern. **Stop before the next direct MCP call and make the
routing decision:**

1. Run `mcx list` and use a matching registered chain when one exists.
2. If no chain exists and two or more related calls remain, invoke `/mcx:new`.
   It executes ad-hoc script source from a heredoc so this task's intermediate
   payloads stay out of context without creating a file or registry entry.
3. Continue directly only for an isolated call where a chain would not reduce
   calls or keep intermediate payloads out of context.

For a bloated unfiltered result, invoke `/mcx:new` before calling that tool
again; it will select the filter workflow. Continue unfiltered only when the
result is already mostly signal or the task requires its exact shape.

This is a routing requirement, not an optional optimization. A one-time task
with a multi-call fan-out is not an exception; convenience alone is not an
exception.

## Forward one MCP call (keychain OAuth injected automatically)

```sh
mcx forward --server jira --tool getJiraIssue \
  --args '{"cloudId":"00000000-0000-0000-0000-000000000000","issueIdOrKey":"PROJ-123"}'
mcx forward --list        # every server from config ∪ keychain; [keychain-auth] = OAuth-backed
```

An HTTP server with no auth header in config gets a bearer token from the macOS
keychain, refreshed (RFC 8414) if expired. Static-header servers work untouched.

## Chains: heredoc by default; save only on request

Run script source directly for the current task. The first operand becomes the
script's parsed `args`; stdin carries the source into mcx, not into the child script:

```sh
mcx run '{"jiraServer":"jira","cloudId":"00000000-0000-0000-0000-000000000000","issue_keys":["PROJ-123","PROJ-124"]}' ruby <<'RUBY'
rows = args["issue_keys"].map do |key|
  issue = forward(
    args["jiraServer"],
    "getJiraIssue",
    { "cloudId" => args["cloudId"], "issueIdOrKey" => key }
  )
  { key: key, status: issue.dig("fields", "status", "name") }
end
emit(rows)
RUBY
```

`mcx run <args-json> <path>` is also ad hoc. If the user explicitly asks to persist the
proven workflow, invoke `/mcx:save`; it owns registration and verification by
name:


```sh
mcx register ./chains/sprint_to_sheet.rb          # name=sprint-to-sheet, lang=ruby, desc=first comment
mcx run '{"sprint":42}' sprint-to-sheet
mcx list
mcx remove sprint-to-sheet
```

Overrides when you want them: `--name`, `--lang`, `--desc`, `--schema`.

Chains are stored **inline** (source as a block scalar in a `chains.yaml` entry, self-contained) and resolve
across layers merged by name, most specific winning: plugin default (`${CLAUDE_PLUGIN_ROOT}`, ships
example chains that appear in `mcx list` with no registration) → project `.mcx/` → user
`~/.config/mcx/`. `register`/`remove` write the user layer; a user/project entry overrides a plugin
chain of the same name.

`register`/`remove` also sync a personal skill per chain into `~/.claude/skills/<chain-name>/`, so every
resolved chain (any layer) becomes invocable as `/<chain-name>` with no extra step. The sync is a full
reconciliation each time — it also prunes any previously-synced skill whose chain no longer resolves,
even if a different command removed it — and it never touches a skill it didn't create itself.

### The chain environment (already set up — no boilerplate)

Inside a chain script you get, free:

- `forward(server, tool, args = {})` — calls an MCP tool via `mcx forward`, parses
  the result, raises on tool errors. Fan these out; the raw payloads live and die
  in the sandbox.
- `emit(obj)` — writes the digest (a String is passed through; anything else is
  JSON-encoded). Whatever you emit is the only thing that re-enters context.
- `args` — the parsed `--args` JSON, ready to use (no stdin handling needed).

All three (`forward`/`emit`/`args`) are baked into ruby, python, and javascript
chains. Ruby example (the whole file):

```ruby
# Fan out getJiraIssue over many keys, return a compact status table.
jira_server = args["jiraServer"] || "jira"
rows = args["keys"].map do |key|
  issue = forward(
    jira_server,
    "getJiraIssue",
    {
      "cloudId" => args["cloudId"],
      "issueIdOrKey" => key
    }
  )
  { key: issue["key"], status: issue.dig("fields", "status", "name") }
end
emit(
  {
    count: rows.length,
    issues: rows
  }
)
```

Runtimes: ruby / python / javascript / shell (auto-selected by file extension).
The sandbox environment is stripped to a safe allow-list — no API keys reach the
script; pass everything through stdin.

## Filters: auto-filtering tool output

Configured in `filters.yml`, keyed by full MCP tool name. Applied automatically
by the PostToolUse hook; you rarely run `mcx filter` by hand.

```yaml
mcp__jira__getJiraIssue:
  drop:
    - expand
    - self
    - fields.reporter.avatarUrls
  truncate:
    fields.description: 400
```

- `drop` (denylist) / `keep` (allowlist) / `rename` / `truncate` over **dotted
  paths** (no wildcards — every touched field is explicit).
- A tool with no entry passes through untouched (fail-open). `MCX_FILTER=off`
  disables filtering entirely.
- Precedence (merged by tool key, most specific wins): plugin default →
  project `.mcx/filters.yml` → user `~/.config/mcx/filters.yml`.
- Shipped defaults are **drop-only**, with every dropped path validated against
  a checked-in capture so signal fields are preserved.

## Diagnose and sync: doctor, observe, scan, sync-connectors

**doctor** — self-check that the binary and config load correctly:

```sh
mcx doctor
```

Reports plugin root, whether shipped filters reshape payloads, chain count. Non-zero exit means something is wrong.

**observe** — live routing gate during a session. From the second MCP call onward it requires a chain decision before another direct call; a bloated unfiltered result requires a filter decision before that tool is called again. Per-session state lives in `${CLAUDE_PLUGIN_DATA}`. Set `MCX_OBSERVE=off` to disable.

**scan** — retrospective analysis of a transcript. Reads JSONL logs and reports chain candidates (tools called repeatedly — suggest `mcx register`) and filter candidates (large, unfiltered results — suggest config):

```sh
mcx scan --config "${CLAUDE_PLUGIN_ROOT}/filters.yml"
mcx scan --transcript /path/to/session.jsonl
```

Omit `--transcript` to scan the newest transcript for this project.

**sync-connectors** — mirror claude.ai account-level MCP connectors into local `~/.claude.json` config:

```sh
mcx sync-connectors --list        # show available connectors
mcx sync-connectors --only Name1,Name2   # sync specific ones
```

Credentials still require authentication — run `/mcp` after syncing a new server.

## Env vars

- `MCX_FORWARD_TIMEOUT` — per forward call (default 120s).
- `MCX_EXECUTE_TIMEOUT` — per chain run (default 120s).
- `MCX_FILTER=off` — disable filter filtering.
- `MCX_NUDGE=off` — disable the prompt-mentions-mcx skill reminder.
- `MCX_OBSERVE=off` — disable the live chain/filter routing gates.
- `MCX_HOOK_ECHO=on` — also surface nudge/observe hook messages to the human (`systemMessage`), not just the agent.
- `XDG_CONFIG_HOME` — relocate the `~/.config/mcx` store (chains + user config).

To optimize a new workflow or bloated result, invoke `/mcx:new`; it selects an
ad-hoc chain or filter from the task evidence. Invoke `/mcx:save` only for an
explicit persistence request. Registration is never implicit.
