---
name: mcp-server-discovery
version: 1.0.0
category: devops
description: Systematic discovery of MCP servers on a live system — probing open ports for HTTP MCP endpoints, scanning known project directories for dormant-but-ready servers, and identifying un-onboarded Docker containers. Companion skill to mcp-server-onboarding (wiring) and mcp-fleet-audit (health verification).
metadata:
  hermes:
    tags: [mcp, discovery, port-probing, server-discovery]
    triggers:
      - find MCP servers
      - discover MCP endpoints
      - probe for MCP
      - what MCP servers are running
      - find unconfigured MCP
      - scan for MCP servers
    related_skills: [native-mcp, mcp-fleet-audit]
---

# MCP Server Discovery

Systematic discovery of MCP servers on a live system — both **live** (HTTP
endpoints already running on open ports) and **dormant** (complete projects
sitting on disk but never wired into Hermes config).

## Discovery Sequence

### Phase 1 — Live Port Probing (HTTP MCP Endpoints)

Not all MCP servers are registered in Hermes config. Docker containers,
standalone processes, and background services may expose MCP HTTP endpoints
on open ports without any agent knowing about them.

```bash
# Step 1: Enumerate all listening ports
netstat -ano | grep LISTENING
```

**Prioritized ports** (most likely MCP hosts first):
| Port Range | Typical Service |
|------------|----------------|
| 8888 | Open Coscientist / AI Scientist |
| 3000-3003 | Node.js (brain.md, Cal.diy, Buzz relay) |
| 8000-8080 | Python HTTP servers |
| 8211, 8222 | Plane MCP, Firefox Remote |
| 9222-9226 | Browser debug / CDP ports |
| 8088, 8081 | ClawFleet, docker-control-plane |

```bash
# Step 2: Probe each candidate port with MCP initialize
PORT=8888
curl -s http://localhost:$PORT/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,\
       "params":{"protocolVersion":"2024-11-05",\
       "capabilities":{},\
       "clientInfo":{"name":"discovery","version":"1.0"}}}'
```

**Identify the server** from the response — success looks like:
```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05",
 "serverInfo":{"name":"open-coscientist-lit-review","version":"2.14.7"},...}}
```

**Empty response / connection refused** = not an MCP endpoint.

```bash
# Step 3: List tools on confirmed server
curl -s http://localhost:$PORT/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":2,"params":{}}'

# Step 4: Identify the owning process or Docker container
tasklist /FI "PID eq $PID" /FO TABLE
docker ps --format "{{.Names}}\t{{.Image}}\t{{.Ports}}" | grep ":$PORT"
```

**Port → PID → container mapping on Docker-heavy Windows:**
- `netstat` shows `com.docker.backend.exe` for ALL Docker-exposed ports.
- A parallel `wslrelay.exe` on the same port means WSL passthrough.
- Always cross-reference with `docker ps` — do NOT conclude a server from
  PID alone.
- Run `docker ps | grep ":$PORT"` to resolve the container.

**Pitfall: `/health` false positives.** A port whose `/health` returns `"ok"`
is NOT necessarily an MCP server. The wslrelay/Docker forwarding layer can
return `"ok"` from a non-MCP container (e.g., Buzz Nostr Relay). Always
confirm with MCP `initialize` — if it returns empty or errors, the port does
NOT host an MCP server.

### Phase 2 — Docker Container Scan

Docker containers named `*-mcp` or exposing unusual ports are prime candidates.

```bash
# List all containers with names/ports
docker ps --format "{{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"

# Look for containers with MCP indicators in the name
docker ps --format "{{.Names}}" | grep -i "mcp\|agent\|server"

# Check recently added containers (sorted by age)
docker ps --format "{{.Names}}\t{{.CreatedAt}}" | sort -k2
```

Cross-reference exposed ports against `netstat` to check if they're host-reachable.
Some containers expose only on Docker-internal networks and need port forwarding
to be usable from Hermes.

### Phase 3 — Project Directory Scan

For dormant-but-ready MCP server projects that exist on disk but were never
wired into Hermes config:

```bash
# Known MCP project roots
ls -d ${MY_REPOS}/git-mcp/services/*/
ls -d ${MY_REPOS}/finance-team/*/
ls -d ${MY_REPOS}/auto-resume/*/

# Filter for MCP candidates
grep -l "mcp" */pyproject.toml 2>/dev/null
ls -la */app/main.py */mcp_server.py */server.py 2>/dev/null
```

Check for duplicate/alternative copies — MCP projects may exist in multiple
locations (original + hermes-integration-copy):

```bash
find ${MY_REPOS} -maxdepth 4 \
  -name "mcp_server.py" -o -name "hermes_mcp_server.py" \
  -type f 2>/dev/null | xargs wc -l 2>/dev/null
```

When duplicates are found, diff entry points and check which has an active
`.venv`. The one with a populated virtualenv is the real deployment target.

### Phase 4 — Standalone Verification

For each candidate discovered in Phase 2 or 3, test it independently before
any config wiring:

```python
import asyncio, sys
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

async def probe(project, command, args, timeout=15):
    params = StdioServerParameters(command=command, args=args)
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                tools = await asyncio.wait_for(
                    session.list_tools(), timeout=timeout)
                print(f"[{project}] {len(tools.tools)} tools:")
                for t in tools.tools:
                    print(f"  {t.name}")
    except Exception as e:
        print(f"[{project}] FAIL: {e}")

asyncio.run(probe(*sys.argv[1:]))
```

**Key signals the server is worth onboarding:**
- `list_tools()` returns tools without error
- 5+ meaningful tools (not just health check)
- Dependencies install cleanly
- No external service requirements beyond what's available

## Standard Tool Naming Checklist

Once discovered, add a cross-reference in the pulse report using this format:
```
🆕 **SERVER** (port PORT) — vVERSION, N tools: tool1, tool2, tool3
```

## Related Skills

- `mcp-server-onboarding` — Wire discovered servers into Hermes config.yaml
- `mcp-fleet-audit` — Periodic health checks after servers are onboarded
- `native-mcp` — Client config reference, transport types, troubleshooting
