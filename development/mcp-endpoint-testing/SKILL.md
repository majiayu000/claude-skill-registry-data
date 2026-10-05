---
name: mcp-endpoint-testing
description: "Test MCP server endpoints across all transports — stdio (Python client), HTTP/StreamableHTTP (curl), SSE (curl with event-stream extractor). Transport detection, common failure patterns, and verification checklists."
version: 1.0.0
category: devops
metadata:
  hermes:
    tags: [mcp, endpoint-testing, curl, sse, streamable-http, stdio, transport-detection]
    triggers:
      - test MCP server
      - check MCP endpoint
      - verify MCP tools
      - MCP transport detection
      - curl MCP test
      - test SSE MCP
    related_skills:
      - native-mcp
      - mcp-server-onboarding
      - mcp-fleet-audit
      - building-mcp-servers
      - mcp-server-wiring
---

# MCP Endpoint Testing

Test MCP server endpoints across all transport types. Use when onboarding a new server, diagnosing a connection failure, or verifying health during a fleet audit.

## Transport Detection

Before testing, identify which transport the server uses:

| Signal | Transport |
|--------|-----------|
| Config has `command:` + `args:` | **Stdio** — test with Python client |
| Config has `url:` | **HTTP** — test with curl |
| `curl -v` returns `content-type: text/event-stream` | **SSE** — use SSE extractor pattern |
| `curl -v` returns `content-type: application/json` | **StreamableHTTP** — plain JSON response |
| `POST /mcp` returns 404 but server process exists | **SSE** (SSE does NOT respond to bare POST on /mcp) |

### Quick transport probe (single curl command)

```bash
curl -v -s \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  http://localhost:PORT/mcp 2>&1 | grep -E "(content-type:|event:|HTTP/)"
```

- `HTTP/1.1 200 OK` + `content-type: application/json` → **StreamableHTTP**
- `HTTP/1.1 200 OK` + `content-type: text/event-stream` + `event: message` → **SSE**
- `HTTP/1.1 404` → likely **SSE** on a different path or port
- Connection refused / timeout → server process is **DOWN**

## Testing Stdio MCP Servers (Python)

For stdio-based servers (command + args in config.yaml):

```python
import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession

async def test_server():
    params = StdioServerParameters(
        command="python",
        args=["-m", "app.main"],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            # List tools
            result = await session.list_tools()
            print(f"Tools ({len(result.tools)}):")
            for t in result.tools:
                print(f"  {t.name}: {t.description[:80]}")
            # Call a tool
            health = await session.call_tool("health_check", {})
            print("Health:", health.content[:300])

asyncio.run(test_server())
```

### Pre-warming for uvx/npx servers

First-run `uvx`/`npx` servers download 70MB+ of dependencies and may exceed `connect_timeout`. Pre-warm before testing:

```bash
uvx server-name --help 2>/dev/null || npx -y server-name --help 2>/dev/null
```

## Testing HTTP/StreamableHTTP MCP Servers (curl)

For servers that return `content-type: application/json`:

```bash
# Initialize
curl -s http://localhost:PORT/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'

# List tools
curl -s http://localhost:PORT/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":2,"params":{}}}'

# Call a tool
curl -s http://localhost:PORT/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":3,"params":{"name":"tool_name","arguments":{}}}'
```

**Key signals:** initialize returns `protocolVersion` + `serverInfo`. tools/list returns tool array without error. tools/call returns content.

## Testing SSE MCP Servers (curl with event-stream extractor)

SSE servers return `content-type: text/event-stream` and wrap JSON-RPC in:
```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

Piping raw SSE output to `json.loads()` fails because the `event:` / `data:` lines are not valid JSON. **Always extract the JSON payload with `grep "^data: " | sed 's/^data: //'`:**

### Initialize + detect transport

```bash
curl -v -s \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  http://localhost:8888/mcp 2>&1 | grep -E "(content-type:|event:)"
```

Expected SSE output: `content-type: text/event-stream` + `event: message`

### List tools from an SSE MCP server

```bash
response=$(curl -s \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":2,"params":{}}' \
  http://localhost:8888/mcp)
echo "$response" | grep "^data: " | sed 's/^data: //' | python -c "
import json, sys
data = json.load(sys.stdin)
tools = data.get('result', {}).get('tools', [])
print(f'Tools count: {len(tools)}')
for t in tools:
    print(f'  - {t[\"name\"]}: {t.get(\"description\", \"\")[:80]}')
"
```

### Call a tool on an SSE MCP server

```bash
response=$(curl -s \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":3,"params":{"name":"tool_name","arguments":{}}}' \
  http://localhost:8888/mcp)
echo "$response" | grep "^data: " | sed 's/^data: //' | python -c "
import json, sys
data = json.load(sys.stdin)
content = data.get('result', {}).get('content', [])
for c in content:
    print(c.get('text', str(c))[:500])
"
```

**Key signals:** `grep "^data: " | sed 's/^data: //'` extracts valid JSON. tools/list returns expected tools. tools/call returns meaningful content.

### SSE session flow (for manual testing)

SSE servers use a two-step connection pattern:
1. `GET /mcp` (SSE stream) → receive session_id from initial event
2. `POST /messages?session_id=<id>` for each JSON-RPC request

Some SSE servers (like Open Coscientist) accept POST directly on `/mcp` and return SSE responses inline — these are hybrid implementations. Detect by testing POST directly first.

## Testing WebSocket / BiDi Endpoints (Firefox remote agent, browser bridges)

Some servers expose a raw WebSocket protocol instead of HTTP JSON-RPC — notably Firefox's WebDriver BiDi remote agent (started with `--remote-debugging-port`) and MCP bridge servers that connect to it. Standard HTTP MCP probes do NOT apply; the liveness probe is a WebSocket upgrade handshake.

### Identification signals (Firefox 129+, CDP removed)

| Probe | Response | Meaning |
|---|---|---|
| `GET /` | 200 HTML "httpd.js is up and serving requests!" | BiDi remote agent ALIVE (built on Mozilla's httpd.js — this is NOT a ghost/foreign server) |
| `GET /json/version` | 404 | CDP endpoints removed in Firefox 129 — any CDP-based detection/readiness loop is dead |
| `GET /session` (no WS upgrade) | 400 | endpoint present; needs a real WebSocket handshake |
| `ws://host:PORT/session` upgrade | 101 | definitive BiDi-alive signal |

### BiDi liveness probe (Python)

```python
import asyncio, websockets
async def bidi_alive(port=9239):
    try:
        async with websockets.connect(f'ws://127.0.0.1:{port}/session', open_timeout=8):
            return True
    except Exception:
        return False
```

**⚠️ `open_timeout`, not `timeout`** — websockets 14.0 renamed the open-handshake kwarg `timeout` → `open_timeout`; 15.0 removed the old name. Passing `timeout=` sweeps it into `**kwargs` → `loop.create_connection(factory, **kwargs)` → `TypeError: BaseEventLoop.create_connection() got an unexpected keyword argument 'timeout'`. When that call sits in `try/except Exception: return False`, detection fails **silently forever** ("Cannot detect Firefox on BiDi:PORT or CDP:PORT" while Firefox listens on the exact configured port). Always probe directly before trusting a negative detection result.

### Post-connect failure modes

- **`'NoneType' object is not iterable` in list/flatten** — Firefox's `browsingContext.getTree` returns `"children": null` (key present, null value) for leaf contexts; `ctx.get("children", [])` returns `None` (default only applies to a MISSING key) → crash. Use `(ctx.get("children") or [])`.
- **`session.new` → "Maximum number of active sessions"** — one active BiDi session per browser process; hard-killing the client (`taskkill /F`) leaves the slot held. Reconnecting the client is NOT enough — relaunch a fresh browser (its launcher's `kill_orphans` clears the port first).
- **Kill-and-respawn hot-load** — Hermes' MCP client auto-reconnects a killed stdio server (exponential backoff): patch the server source on disk, `taskkill /F /PID <server>`, and the respawned instance loads the fix — no Hermes restart. Also purges duplicate instances (venv python + hermes-runtime python can both host copies of the same server).

Full case study (ultimate-firefox-mcp bridge, Aug 2026): [references/websocket-bidi-endpoint-probing.md](references/websocket-bidi-endpoint-probing.md)

## Diagnosing Tool Calls That Hang or Kill the Server

Symptom signature: `initialize` + `list_tools` succeed, a specific tool call then hangs forever or the server process dies mid-call (`McpError: Connection closed`), but the SAME code completes in seconds when run standalone. This is the classic **FastMCP worker-thread context** failure: `mcp.server.fastmcp` runs sync tool functions via `anyio.to_thread`, and heavy lazy-import libraries (OpenBB, pandas, numba) are not thread-safe on first use (extension auto-build / type generation deadlocks or hard-crashes the process).

### Isolation ladder (cheap → expensive)

1. **In-process direct call** — import the server module and call the tool function in the MAIN thread, no MCP round-trip:
   ```python
   import importlib.util
   spec = importlib.util.spec_from_file_location("srv", r"E:/path/to/server.py")
   m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
   print(m.market_summary()[:400])   # works fast → bug is MCP/thread context, not the data layer
   ```
   - Returns JSON quickly → the data layer is fine; the hang lives in the FastMCP worker thread.
   - Hangs/errors → the tool body itself is at fault; debug the data call chain directly.
2. **Distinguish tool-vs-tool**: if a DIFFERENT tool using the same stack also hangs, it's the shared context/library, not that tool's logic.
3. **Clean-env Windows note**: when testing with `env -i`, Windows Python needs `USERPROFILE` (plus `HOMEDRIVE`/`HOMEPATH`/`APPDATA`/`LOCALAPPDATA`/`SYSTEMROOT`) — `HOME` alone is not enough. Omitting them yields a misleading `"Could not determine home directory."` error or a hang in libraries that resolve config dirs.
4. **Workarounds, in order**: pre-warm the lazy library at module import (main thread) before `mcp.run()`; wrap the tool body in a dedicated `threading.Thread` with a join timeout; pin `fastmcp`/`mcp` to a known-good combo; escalate a confirmed library thread-safety defect with a repro.

Full worked example (OpenBB trading-signals: provider default-routing hang + column-oriented `to_dict()` extraction bug + worker-thread hang): see [references/fastmcp-thread-context-hang.md](references/fastmcp-thread-context-hang.md).

## Verification Checklist

- [ ] Transport correctly identified (stdio vs StreamableHTTP vs SSE)
- [ ] initialize returns `protocolVersion` + `serverInfo` without error
- [ ] tools/list returns expected tools (count and names match docs)
- [ ] At least one tool call returns meaningful content (not an error)
- [ ] Server process survives multiple sequential tool calls
- [ ] Server process exits cleanly on disconnect
- [ ] For SSE: JSON payload successfully extracted with grep+sed extractor
- [ ] For stdio: Python test script runs without import errors

## Pitfalls

- **SSE raw pipe to json.loads() fails** — always use `grep "^data: " | sed 's/^data: //'` to extract JSON from SSE framing before piping to Python.
- **uvx/npx first-run timeout** — pre-warm with `--help` before testing or increase `connect_timeout` to 120s.
- **Same `Accept` header for both transports** — both StreamableHTTP and SSE require `Accept: application/json, text/event-stream`. The response content-type tells them apart.
- **POST on /mcp returns 404 for SSE servers** — some SSE servers require POST on a separate `/messages?session_id=<id>` endpoint. Check raw response headers first before assuming the server is dead.
- **Connection refused vs 404** — connection refused means no process is listening on the port. A 404 means the process IS running but the path is wrong. Very different fixes.
- **Stdio servers inherit filtered env** — only PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR + XDG_* are passed. If your test works in terminal but Hermes fails, missing env vars are the most likely cause. Pass them explicitly under `env:`.
- **Windows `which` lies about `.exe` files** — Use `command -v <binary>` (bash built-in) not `which <binary>`.
- **`env -i` clean tests on Windows miss `USERPROFILE`** — Windows Python resolves the home dir from `USERPROFILE`, not `HOME`. A clean-env test (`env -i PATH=... HOME=...`) fails with `"Could not determine home directory."` or hangs in libs that resolve config dirs. Pass `USERPROFILE`/`HOMEDRIVE`/`HOMEPATH`/`APPDATA`/`LOCALAPPDATA`/`SYSTEMROOT` explicitly.

## Related Skills

- `native-mcp` — MCP client config reference, transport types, Hermes integration
- `mcp-fleet-audit` — Fleet-wide health checks, dormant server discovery
- `mcp-server-onboarding` — Full workflow for finding, fixing, and wiring servers
- `building-mcp-servers` — Building MCP servers from scratch
- `mcp-server-wiring` — Wiring existing Python modules as MCP tools

## References

- [Open Coscientist SSE Discovery](references/open-coscientist-sse-discovery.md) — Real-world case study: identifying SSE transport on a running MCP server, troubleshooting the raw pipe to json.loads() failure, and the grep+sed extractor pattern.
- [FastMCP Thread-Context Hang](references/fastmcp-thread-context-hang.md) — Real-world case study: OpenBB trading-signals server whose tools hang/die over MCP stdio but work in-process; isolation technique, two OpenBB SDK quirks (provider default routing, column-oriented `to_dict()`), and the Windows clean-env pitfall.
- [WebSocket/BiDi Endpoint Probing](references/websocket-bidi-endpoint-probing.md) — Real-world case study: ultimate-firefox-mcp bridge's week-long "Cannot detect Firefox" — websockets 15 `timeout`→`open_timeout` API break swallowed by `except Exception`, `children: null` flatten crash, BiDi session-slot exhaustion, and the kill-and-respawn hot-load pattern.
