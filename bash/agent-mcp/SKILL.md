---
name: agent-mcp
description: Manage and health-check the machine's MCP servers (mcp_agents.py CLI) - inventory the declared servers from user and repo configs, audit declared vs running via localhost probes, deep-probe one server (daemon reachability, corpus freshness via BUILT_AT-style globs, referenced paths in its config file), run the doctor CI gate, or start/stop/restart through declared lifecycle commands. Use when an MCP-dependent feature fails silently, before claiming a daemon is up, or on any session bootstrap that depends on local search/indexer daemons.
---

# agent-mcp - MCP fleet health, locally

MCP servers fail silently: a localhost daemon dies and every fallback keeps
working "on the surface", an indexer's config references directories that were
renamed weeks ago, a corpus goes stale. This CLI makes all three visible and
gives the lifecycle commands a single declared entry point.

Everything is driven by a **local, git-ignored fleet descriptor**
(`mcp-fleet.local.yml` next to `.agent/`, template:
`template/mcp-fleet.template.yml` in agents-kit). Machine paths never enter a
repository.

## Invocation

```bash
uv run --no-project .agents/skills/agent-mcp/scripts/mcp_agents.py [--repo PATH] <command>
```

- Standard library only, Python 3.11+: no install, no venv, works on fresh
  clones and CI.
- In the agents-kit repository the canonical copy is `scripts/mcp_agents.py`;
  the copy shipped here is byte-identical (test-enforced mirror).

## Commands

| Command | Effect |
|---|---|
| `inventory [--fleet ROOT]` | Parse MCP declarations: user-level configs (`mcpServers` or `mcp.servers` key) plus repo-level `.mcp.json` files under the fleet roots. Token-like values (token, key, secret, password) are masked. |
| `audit` | Declared vs running: run each descriptor entry probe (localhost HTTP URL, process name, or command) and report `up / down / unknown`. Exit 1 if any entry is down. |
| `probe <name>` | Deep check of one entry: probe + freshness globs (e.g. `**/BUILT_AT.txt`, age budget) + every absolute path referenced by its declared config file must exist. |
| `doctor` | Audit + freshness + referenced paths for every entry. Exit 0 only when everything is healthy - usable as a CI/local gate. |
| `start <name>` / `stop <name>` / `restart <name>` | Run the lifecycle command declared in the descriptor (e.g. a `start-*.cmd`). `restart` falls back to the declared stop then start. These are the ONLY effectful commands. |

Descriptor discovery: `--config PATH` > `MCP_FLEET_CONFIG` env var >
`<repo>/mcp-fleet.local.yml` > upward walk from the repo root.

## Safety rules

- `inventory`, `audit`, `probe` and `doctor` never write anything.
- Lifecycle commands run with the descriptor as the single source: nothing is
  improvised on the command line. Machine-level rules (no shutdown, no
  restart of the machine itself) stay governed by the kit's common block.
- No secret value is ever printed: masking is applied to every output,
  including `--json`.
- External effect (starting or stopping a daemon) is a machine state change:
  report it, never hide it.

## Workflow

1. Before trusting any MCP-backed feature: `doctor` (or `audit` for the
   network view only). Fix what is red before working around it.
2. A down daemon: `probe <name>` for the why (process? stale corpus? missing
   referenced directory?), then `start <name>` if the descriptor declares how,
   then `probe <name>` again to confirm.
3. After renaming or deleting a repository: `doctor` flags the indexers whose
   config still references the old path - fix the config, then restart the
   daemon through the declared lifecycle commands.
4. A red `doctor` is a finding, not a nuisance: report it with the captured
   output as evidence (paths redacted outside the machine).
