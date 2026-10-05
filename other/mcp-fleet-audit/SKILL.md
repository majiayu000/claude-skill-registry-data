---
name: mcp-fleet-audit
version: 1.0.0
category: devops
description: Periodic health audits of all MCP servers across stdio, Docker, and HTTP transports — fleet-wide status, dormant server discovery, standalone verification, and onboarding evaluation.
metadata:
  hermes:
    tags: [mcp-servers, fleet-audit, health-check, server-discovery]
    triggers:
      - audit MCP servers
      - check all MCP servers
      - MCP fleet health
      - find un-onboarded MCP
      - check MCP connectivity
    related_skills: [mcp-server-discovery, native-mcp, gateway-troubleshooting]
---

# MCP Fleet Audit

Periodic health checks across all MCP server transports: stdio (Hermes config), Docker (compose containers), HTTP/SSE (remote endpoints), and dormant (built but unwired) projects.

## Audit Sequence

### 1. Live Server Checks

**Profile vs root config cross-reference:** MCP servers may be split across multiple Hermes configs. Check ALL locations before concluding a server is absent:
```bash
# Root config (system-wide servers)
grep -A20 "^mcp_servers:" ~/.hermes/config.yaml 2>/dev/null | head -30
# All profile configs
for f in ~/.hermes/profiles/*/config.yaml; do echo "=== $f ==="; grep -A20 "^mcp_servers:" "$f" 2>/dev/null | head -25; done
```
Root config servers (a2asearch-mcp, postgres) are NOT inherited by profile sessions — each profile maintains its own `mcp_servers:` block. A profile missing servers the root has is a config gap. Conversely, a server that's healthy in root config but absent from a profile's list isn't a failure — it's a deliberate scoping choice. Flag the mismatch either way in the audit report.

**brain.md / gbrain (HTTP):**
```bash
curl -s http://localhost:3000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"audit","version":"1.0"}}}'
```
Follow with `tools/list` to verify tool count, `current_datetime` to confirm server time.

**Docker containers:**
```bash
docker ps --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
```
Check for:
- All containers Up (no Exited/Crashed)
- Expected MCP containers present (open-coscientist on 8888, plane-mcp on 8211, etc.)
- Unexpected containers absent (no orphaned services)

**Stdio server directories** (from config.yaml `mcp_servers` entries):
```bash
# For each stdio MCP server, verify the command resolves and entry point exists
command -v <server-command>
ls -la <project-dir>/app/main.py
ls -la <project-dir>/mcp_server.py
```

**Key DB freshness checks** — check `ls -la` timestamps for each project's database:
```bash
# Personal intelligence
ls -la git-mcp/services/personal-intelligence-mcp/pim.db
# Git stars
ls -la git-mcp/services/github-star-intelligence-mcp/gitmcp.db
# Trading signals
ls -la finance-team/insider-trading/data/signals.db
```

### 2. Dormant / Un-Onboarded Server Discovery

Scan known service directories for complete but unwired MCP server projects — servers that exist on disk but are NOT registered in any Hermes config.yaml.

**Root directories to scan:**
```bash
ls -d ${MY_REPOS}/git-mcp/services/*/
ls -d ${MY_REPOS}/auto-resume/*/
ls -d ${MY_REPOS}/finance-team/*/
```

**Filter for MCP candidates** in each directory:
```bash
# Check for pyproject.toml with MCP dependency
grep -l "mcp" */pyproject.toml 2>/dev/null
# Check for MCP server entry point
ls -la */app/main.py 2>/dev/null
ls -la */mcp_server.py */server.py 2>/dev/null
```

**Detect duplicate/alternative MCP server installations:** MCP server projects can exist as multiple copies (original + fork + hermes-integration copy). After finding a candidate, check for duplicates:
```bash
# Find all copies of a suspected MCP server by its entry-point script name
find ${MY_REPOS} -maxdepth 4 -name "hermes_mcp_server.py" -type f 2>/dev/null
# Find all copies by mcp_server.py
find ${MY_REPOS} -maxdepth 4 -name "mcp_server.py" -type f 2>/dev/null
# Compare line counts to determine if one is a thin wrapper vs the real server
wc -l $(find ${MY_REPOS} -maxdepth 4 -name "hermes_mcp_server.py" -type f 2>/dev/null)
```
When duplicates are found, diff the entry points and check README identity. One may be a stale backup — flag it in the pulse entry with `🔄 Duplicate found`.

### 3. Standalone Verification Test

For each candidate, test it independently before any config.yaml wiring:

```python
import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession

async def test_server(project_label, command, args, timeout=10):
    params = StdioServerParameters(command=command, args=args)
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                result = await asyncio.wait_for(session.list_tools(), timeout=timeout)
                print(f"[{project_label}] {len(result.tools)} tools:")
                for t in result.tools:
                    print(f"  {t.name}: {t.description[:80]}")
    except Exception as e:
        print(f"[{project_label}] ERROR: {e}")

asyncio.run(test_server("firefox-remote", "python", ["-m", "app.main"]))
```

**Key signals a server is functional and worth onboarding:**
- `list_tools()` returns tools without error
- 5+ meaningful tools (not just health check)
- Dependencies install cleanly
- No external service requirements beyond what's available

**Standalone test failure causes:**
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `ImportError` / ModuleNotFound | Relative import fails when run from wrong CWD | Run from project root or use `python -m app.main` |
| `TypeError: cannot specify both default and default_factory` | Pydantic too new | `pip install "pydantic>=2.10,<2.14" "pydantic-settings>=2.0,<2.7"` |
| `Received request before initialization was complete` | fastmcp/mcp SDK version mismatch | Pin: `pip install "fastmcp>=0.4,<1.0" "mcp>=1.0,<1.2"` |
| `TypeError: FastMCP.run() got an unexpected keyword argument 'host'` (or `port`) | Server written for fastmcp <=0.4 API (`mcp.run(transport="sse", host=..., port=...)`) but running against fastmcp 3.x which removed those kwargs | Remove `host` and `port` from `run()`. For SSE hosting, use `uvicorn` with `mcp.sse_app()`. For Hermes, switch to `transport="stdio"` |
| Connection timeout / 000 exit | Server requires external service (DB, browser) | Check project README for prerequisites |

### 4. Onboarding Evaluation Criteria

After finding a dormant server, evaluate with this checklist:

- [ ] Does it serve a distinct capability not already covered by live servers?
- [ ] Does it require external services (running DB, browser, API keys)? If so, are those available?
- [ ] Is the code maintained? (check `git log --oneline -10`)
- [ ] How many tools does it expose? (from standalone test)
- [ ] What auth/credentials does it need? (check `config.py`, `.env.example`, `pyproject.toml` deps)
- [ ] Is it worth adding to Hermes config or better left as a standalone CLI?

Document the evaluation in the pulse entry with `🆕 Dormant server found` prefix.

### 5. Version Audit

Check npm/PyPI packages used across MCP servers for bump opportunities:
```bash
# Check npm packages (from package.json or npx versions)
npx @remotion/mcp --version 2>/dev/null || echo "check package.json"

# Check Python packages
pip show mcp fastmcp 2>/dev/null | grep Version
```

## Pitfalls

- **Not all projects with `mcp` in pyproject.toml are MCP servers** — some just have `mcp` as a dependency. Check for `app/main.py` or `mcp_server.py` with `mcp.server.Server` or `fastmcp.FastMCP` usage.
- **firefox-remote-mcp requires a running Firefox** instance on port 9222. The server starts but `list_tools()` errors if Firefox isn't running. Test with Firefox launched.
- **firefox-phantom-mcp uses WebDriver BiDi** and `app.main` does NOT export a `mcp` object (different server creation pattern). Test via `app.tools` imports instead.
- **Windows drive letter** — Always use `E:/...` not `/e/...` in Python scripts run via Windows Python (MSYS path resolution fails across drives).
- **DB staleness ≠ pipeline death** — Some MCP servers (git-stars, personal-intel) have data that doesn't change rapidly. Check `ls -la` timestamps across multiple pulses before concluding ingestion is stalled. A 0-byte stale `app/pim.db` sibling can falsely report staleness if the wrong file is checked.
- **brain.md startup syntax** — `brainmd.exe` v0.4.9 uses **flags**, not subcommands. `brainmd serve --port 3000` fails with `unexpected positional argument: serve`. Correct: `brainmd -p 3000 -v <vault>`. Verify with `--help` before each restart — the flag interface may change across versions.
- **brain.md silent crash pattern** — The binary exits silently with no error message, no stderr, and no core dump. 7+ documented crashes across pulse history. After restart, always verify with `initialize` → `tools/list` → `current_datetime`. Recovery procedure is documented in `references/brainmd-crash-recovery.md`.
- **brain.md restart requires background=true** — Do NOT use `nohup` or shell backgrounding (`&`). Hermes blocks shell-level background wrappers. Use `terminal(background=true, command="...")`. This is a long-lived server, so omit `notify_on_complete`.
- **fastmcp 3.x `FastMCP.run()` API change** — Code written for fastmcp <=0.4 used `host` and `port` kwargs in `mcp.run()`; fastmcp 3.x removed them. Causes `TypeError` at startup. See `references/fastmcp-run-api-migration.md` for the full migration guide.
- **Duplicate MCP server projects** — A server may exist as multiple near-identical copies (e.g., `/AI-Scientist/` and `/ai-scientist-hermes/` with 607 vs 605 lines, near-zero functional difference). Always `diff` the entry points before onboarding. If one copy has an active `.venv` and the other doesn't, that's the real deployment target. Flag the stale copy for cleanup in the pulse entry — don't silently wire the wrong path.
- **MCP config gaps between root and profile** — Root config (`~/.hermes/config.yaml`) may list servers not present in any profile, and vice versa. This is not necessarily a bug (profiles scope deliberately), but a server healthy in one config that another profile lacks warrants a mention in every audit so the reader knows the gap exists consciously.

## Related Skills

- `mcp-server-onboarding` — Full workflow for wiring discovered servers into Hermes config.yaml
- `native-mcp` — MCP client configuration reference, transport types, server testing
- `infrastructure-self-healing-pulse` — Broader infrastructure probing and auto-recovery
- `building-mcp-servers` — Building MCP servers from scratch
