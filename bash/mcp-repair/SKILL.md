---
name: mcp-repair
description: >-
  Repair broken MCP: a tool call fails, a server reports "Connection closed",
  tools that used to exist are gone, a project moved or its venv was rebuilt,
  junk breaks the stdio stream, or a server answers from the CLI but not from
  the session. Method: split client / server / environment first, then walk a
  5-step ladder (real name → status → logs → CLI reproduction → stdio probe) and
  fix by category. Use for any "MCP is broken", "the browser tool is not called",
  "everything broke after the move".
---

# MCP-Repair — fix MCP the way we fixed it

A method for taking apart any MCP breakage, built from real incidents: "Connection
closed", `✗ tools.<server>.<tool>`, relocated directories, broken venvs.

**The main principle:** first **split** — is the client, the server or the
environment broken — then fix. Most of the time goes into fixing the wrong one.

## When to use

- A tool call fails inside the session while the server looks configured.
- `MCP server failed: Connection closed`, or the server drops mid-call.
- The model says "tool not found" while the tool should exist.
- After moving or renaming a project directory, or rebuilding a venv/system.
- "research fell over for no reason", "the browser tool does not answer".

## The ladder: steps 0–5

### Step 0 — Resolve the real tool name (never from memory)

In this runtime there is one shape: `search_mcp_tools` finds a tool, then
`call_mcp_tool(server, tool, arguments)` runs it. The server name must match
`~/.agents/mcp.json` exactly; a tool name copied from another client
(`tools.x.y`, `mcp__x__y`, `mcp_x_y`) is the symptom "read from the wrong client",
not a server fault.

### Step 1 — Status: is the server alive at all?

Start with the cheapest read-only tool of that server through the live surface. A
clean answer is health. Two config files matter, and they are not interchangeable:

| File | Shape | Who reads it |
|---|---|---|
| `~/.freebuff/mcp.json` | app consent store: hash-keyed entries, `enabled`, `allowedTools`, approved manifest | the session's own tool surface |
| `~/.agents/mcp.json` | classic `mcpServers` object with `command`/`args`/`env` | `_scripts/mcp-call.py` |

- Tool answers → the server is fine; the problem is the caller (step 2).
- Tool missing from the surface → the server is not enabled for this thread, or its
  entry is broken. Check the consent record before touching the config.
- "Connection closed" → step 3 for the server, then step 5 for the client path.

Do not hand-edit `~/.freebuff/mcp.json`: the app owns that schema. A change goes
through the consent flow.

### Step 2 — The call, not the server

Re-read the tool's schema (`search_mcp_tools` with the server named) and compare it
with the arguments actually sent. Most "internal failure" reports are a missing
required field, a path with the wrong separator, or a query the backend rejects.
Never resend identical invalid arguments: either build one valid request or stop
and report the missing information.

### Step 3 — Reproduce outside the session

The bridge mounts any configured stdio server in the current thread without a
runtime restart:

```bash
python _scripts/mcp-call.py <server> tools
python _scripts/mcp-call.py <server> <tool> '{"query": "test"}'
python _scripts/mcp-call.py <server> <tool> --json          # raw result
```

- **Bridge works** → server and request are fine; the problem is the session's tool
  surface or transport (steps 4–5).
- **Bridge fails** → the server: read the traceback, and look at the raw exception
  before theorising.

### Step 4 — stdio probe: is the protocol clean?

A server that prints anything into stdout before JSON-RPC breaks the stream. Probe
it the same way the bridge does — one `initialize`, then one `tools/list`:

```bash
python - <<'PY'
import asyncio, json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="uv", args=["run", "--project", "<abs>/<server>", "-m", "<server>", "mcp"])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            print(json.dumps((await s.initialize()).model_dump())[:300])
            print(len((await s.list_tools()).tools), "tools")

asyncio.run(main())
PY
```

- A clean handshake and a tool count → go to step 5 by category.
- Junk or a hang → the startup wrapper writes into stdout: look for a top-level
  `print()` in the module (outside `def main`), a progress bar, or a shell banner in
  the configured `command`.

### Step 5 — Fix by category

**Server fix (raw exceptions).** If a tool catches only its own errors while
something raw (sqlite, network, a broken page) escapes into the protocol, wrap it and
return a readable error so the connection survives:

```python
except ResearchError as exc:
    raise ValueError(str(exc)) from exc
except Exception as exc:  # noqa: BLE001 — a readable error instead of tearing down stdio
    raise ValueError(f"<tool> failed internally: {type(exc).__name__}: {exc}") from exc
```

Storage degrades gracefully: a sqlite error means cache-less mode plus a warning, not
a crash — the next call must still be able to run.

**Environment fix (after a move or a rebuild).**

1. Editable installs break first: `site-packages/*.pth` and
   `*.dist-info/direct_url.json` hold **absolute** paths (telltale: `ImportError`
   while `python -c "import sys"` works) → rewrite them or reinstall.
2. Console scripts in `bin/` (Windows: `Scripts/`) carry an absolute shebang → reinstall.
3. `pyvenv.cfg` and `bin/python` usually survive a move — check the `.pth` files first.
4. Config entries with absolute paths: prefer `uv run --project <abs>` over a baked
   interpreter path.

**Client fix.** A server that is fine through the bridge but absent in the session is
a consent/thread problem: verify the server is enabled and allowed in
`~/.freebuff/mcp.json`, and let the app's consent flow do the change. A restart of
the thread is the last resort, not the first move.

## Diagnosis vs recovery

| Symptom | First action |
|---|---|
| Tool call "failed internally" | read the schema and the arguments; fix the server's broad except only if it is genuinely hiding a raw error |
| `Connection closed` | bridge reproduction (step 3), then the stdio probe |
| The tool returned, but the result is empty | server log / `err.log`; bridge call with the same arguments |
| Everything fine in the bridge, broken in the session | tool surface/consent; large responses and timeouts |
| After moving the project | `.pth`/`direct_url.json`, config paths, then re-enable |

## Checks after the fix

1. `python _scripts/mcp-call.py <server> tools` lists the expected tools.
2. One real read-only call through the session returns a result, not a bare error.
3. The failing request is repeated once — the error, if any, is now readable.

## References

- `skills/mcp/parts/mcp-usage/` — which server serves which task, and the config rules.
- `_scripts/mcp-call.py` — the bridge; `--json` for raw output, `--timeout` for slow servers.
- `skills/mcp/parts/mcp-repair/` incidents: searchmcp research resiliency (cache degradation +
  broad except), BrowserMCP stdio, relocated venvs.
