---
name: clients
description: Use when model Context Protocol client hub — connect AI agents to any
  MCP server for tool discovery, invocation, and ecosystem management. Use when working
  with MCP clients, discovering MCP servers, or building MCP-based toolchains.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp-clients
tags:
- mcp
- model-context-protocol
- client
- discover
- tool-integration
- server-registry
persona:
  name: MCP Hub Operator
  title: Model Context Protocol Integrator
  expertise:
  - MCP Client Architecture
  - Server Discovery & Registration
  - Tool Invocation
  - Cross-platform Integration
  philosophy: Every agent is only as capable as the tools it can reach.
  credentials:
  - MCP ecosystem maintainer
  - Tool integration specialist
  - Cross-platform automation architect
  principles:
  - Discover before you build
  - Standardize the protocol, not the tool
  - Fail fast with clear error codes
  - One server, one responsibility
version: 1.0.0
category: mcp
---


# MCP Clients Hub — Model Context Protocol Client Ecosystem


## Overview

MCP Clients Hub is the central client layer for the Model Context Protocol ecosystem. It provides tool discovery, invocation, and ecosystem management for connecting AI agents to any MCP server. This skill covers client architecture, server discovery, tool chaining, and cross-platform integration patterns.

## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

MCP clients are the gateway layer that connects AI agents to the entire tool ecosystem. Mastering MCP client usage and discovery directly enables revenue generation across every other skill:

| Capability | ROI Impact | Timeline |
|---|---|---|
| Rapid server discovery & integration | Eliminates 4-8h of manual integration per tool | Day 1 |
| Multi-server orchestration | 3-5x more tools per agent = 10x capability surface | Week 1 |
| Custom client for proprietary APIs | Build once, sell as MCP server ($500-5K/server) | Week 2 |
| Tool composition (chaining servers) | Automate 12h workflows in 30 minutes | Week 2 |
| MCP server marketplace listing | Passive income stream ($200-2K/mo per popular server) | Month 1 |

**Total addressable leverage:** An agent ecosystem with 50+ connected MCP servers delivers 20x the value of one with 5 servers. Every discovered and integrated server compounds.

## Combined Capabilities

| Capability | mcp-client | mcp-discover | Combined Power |
|---|---|---|---|
| Connect to any MCP server | Core | Auto-discovery | Zero-config server onboarding |
| Tool invocation with type safety | Core | — | Type-safe calls to any discovered tool |
| Server endpoint registry | — | Core | Always up-to-date server inventory |
| Schema introspection | Manual | Automated | Auto-resolve schemas before invocation |
| Stdio transport | Core | — | Run local tool daemons |
| HTTP/SSE transport | Core | — | Remote server connections |
| Resource access (URIs) | Core | — | Fetch data from server resources |
| Broadcast discovery | — | Core | Find all available servers in ecosystem |
| Health checking | — | Core | Validate server liveness before routing |
| Authentication | — | Core | Discover auth requirements pre-call |

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Agent / Application              │
│        (Claude, Cursor, Custom Client)        │
└──────────────────┬──────────────────────────┘
                   │ MCP Protocol (JSON-RPC)
                   ▼
┌─────────────────────────────────────────────┐
│           MCP Clients Hub                    │
│                                              │
│  ┌──────────────┐  ┌──────────────────┐     │
│  │  mcp-client   │  │  mcp-discover     │     │
│  │  - Connect    │  │  - Find servers   │     │
│  │  - Invoke     │  │  - List tools     │     │
│  │  - Stream     │  │  - Check health   │     │
│  │  - Error      │  │  - Get schemas    │     │
│  └──────┬───────┘  └────────┬─────────┘     │
│         │                    │                │
└─────────┼────────────────────┼────────────────┘
          │                    │
          ▼                    ▼
┌─────────────────────────────────────────────┐
│         Available MCP Servers                │
│                                              │
│  github-mcp  notion-mcp  slack-mcp           │
│  stripe-mcp  supabase-mcp  resend-mcp        │
│  linear-mcp  codebase-memory-mcp  ...        │
└─────────────────────────────────────────────┘
```

## First Action in 60 Minutes

### Phase 1: Discover Everything (10 min)
```bash
# 1. List registered MCP servers and their tools
mcp-discover --list-servers
mcp-discover --server all --list-tools

# 2. Check health of all servers
mcp-discover --health-check --timeout 5s

# 3. Get schema for a specific server's tools
mcp-discover --server github-mcp --schema
```

### Phase 2: Connect and Invoke (15 min)
```python
from mcp_client import MCPClient

# Connect to a discovered server
client = MCPClient("github-mcp", transport="stdio")

# List available tools
tools = client.list_tools()
print(f"Available: {[t.name for t in tools]}")

# Invoke a tool with typed parameters
result = client.call_tool(
    "create_issue",
    {
        "owner": "my-org",
        "repo": "my-repo",
        "title": "Auto-discovered from MCP client",
        "body": "Created via MCP client hub"
    }
)
print(f"Status: {result.status}, ID: {result.data.id}")
```

### Phase 3: Build a Multi-Server Workflow (20 min)
```python
from mcp_client import MCPClient, ServerRegistry

# Auto-discover available servers
registry = ServerRegistry()
servers = registry.discover()
print(f"Found {len(servers)} servers")

# Connect to relevant servers
github = MCPClient("github-mcp")
notion = MCPClient("notion-mcp")
slack = MCPClient("slack-mcp")

# Cross-server workflow: GitHub issue → Notion page → Slack alert
def issue_to_notion_to_slack(owner, repo, title, body):
    # Step 1: Create GitHub issue
    issue = github.call_tool("create_issue", {
        "owner": owner, "repo": repo,
        "title": title, "body": body
    })
    issue_url = issue.data["html_url"]

    # Step 2: Log to Notion database
    notion.call_tool("create_database_page", {
        "database_id": "issues-tracker",
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "URL": {"url": issue_url},
            "Status": {"select": {"name": "Open"}}
        }
    })

    # Step 3: Notify Slack
    slack.call_tool("send_message", {
        "channel": "#engineering",
        "text": f"New issue created: {issue_url}"
    })

    return issue_url
```

### Phase 4: Discovery-Driven Automation (15 min)
```python
# Automatically find and connect to new servers as they appear
from mcp_discover import DiscoveryAgent

agent = DiscoveryAgent(
    scan_interval=300,      # check every 5 minutes
    auto_register=True,     # register new servers automatically
    health_required=True    # only register healthy servers
)

agent.start()

# Handle new servers dynamically
@agent.on_server_registered
def handle_new_server(server_info):
    print(f"New server: {server_info.name} ({server_info.transport})")
    # Auto-connect and explore tools
    client = MCPClient(server_info.name)
    tools = client.list_tools()
    print(f"  Tools: {[t.name for t in tools]}")
    # Store in registry for later use
    registry.store(server_info)
```

## Concrete Action Flow

### Discover → Connect → Invoke → Chain → Monitor

### Step 1: Server Discovery
```bash
# Quick broadcast discovery (local network)
mcp-discover scan --network 192.168.1.0/24 --port-range 5000-5100

# Registry-based discovery (pre-registered servers)
mcp-discover list --verbose

# URL-based discovery (remote servers)
mcp-discover probe https://mcp.example.com/tools.json
```

### Step 2: Connection & Authentication
```python
# Standard stdio connection (local process)
client = MCPClient("local-server", transport={
    "type": "stdio",
    "command": "node",
    "args": ["server.js"],
    "env": {"API_KEY": os.environ["MY_API_KEY"]}
})

# HTTP/SSE connection (remote)
client = MCPClient("remote-server", transport={
    "type": "http",
    "url": "https://mcp.example.com",
    "headers": {"Authorization": f"Bearer {token}"}
})

# Verify connection
assert client.ping(), "Server unreachable"
```

### Step 3: Tool Invocation with Error Handling
```python
def safe_invoke(client, tool_name, params, max_retries=2):
    """Resilient tool invocation with retry and error classification."""
    errors = []
    for attempt in range(max_retries + 1):
        try:
            result = client.call_tool(tool_name, params)

            if result.is_error:
                error_code = result.error.get("code", -1)
                if error_code in (-32700, -32600, -32601):  # protocol errors
                    raise RuntimeError(f"Protocol error: {result.error['message']}")

            return result

        except ConnectionError as e:
            errors.append(f"Connection failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # exponential backoff
            continue

        except TimeoutError as e:
            errors.append(f"Timeout (attempt {attempt + 1}): {e}")
            if attempt < max_retries:
                time.sleep(1)
            continue

    raise RuntimeError(f"Tool invocation failed after {max_retries} retries: {'; '.join(errors)}")

# Usage
result = safe_invoke(client, "search", {"query": "MCP protocol", "limit": 10})
```

### Step 4: Tool Composition (Chaining)
```python
class MCPPipeline:
    """Compose multiple MCP tools into a reusable pipeline."""

    def __init__(self, registry: ServerRegistry):
        self.registry = registry
        self.steps: list[dict] = []

    def add_step(self, server: str, tool: str,
                 params: dict, transform: callable = None):
        """Add a pipeline step. Transform maps previous output to this step's params."""
        self.steps.append({
            "server": server, "tool": tool,
            "params": params, "transform": transform
        })
        return self

    async def run(self, initial_context: dict = None):
        context = initial_context or {}
        results = []

        for i, step in enumerate(self.steps):
            client = MCPClient(step["server"])

            # Resolve params: static dict + transform from previous result
            params = dict(step["params"])
            if step["transform"] and results:
                dynamic = step["transform"](results[-1])
                params.update(dynamic)

            result = await client.call_tool_async(step["tool"], params)
            results.append(result)
            context[f"step_{i}"] = result

            print(f"[Pipeline] {step['server']}/{step['tool']} → {result.status}")

        return context, results

# Example: Research → Document → Notify
pipeline = MCPPipeline(registry)
pipeline.add_step("github-mcp", "search_repos", {"q": "mcp-server", "sort": "stars"})
pipeline.add_step("notion-mcp", "create_database_page", {
    "database_id": "research-db",
    "properties": {}
}, transform=lambda prev: {
    "properties": {
        "Name": {"title": [{"text": {"content": f"MCP Server Research - {len(prev.data)} results"}}]},
        "Count": {"number": len(prev.data)}
    }
})
pipeline.add_step("slack-mcp", "send_message", {
    "channel": "#research"
}, transform=lambda prev: {
    "text": f"Research documented - see Notion"
})

await pipeline.run({"started_at": datetime.now().isoformat()})
```

### Step 5: Monitoring & Health
```python
def monitor_servers(servers: list[str], interval_s: int = 60):
    """Continuously monitor MCP server health."""
    from datetime import datetime, timedelta

    status = {s: {"healthy": False, "last_seen": None, "errors": []} for s in servers}

    while True:
        for name in servers:
            try:
                client = MCPClient(name)
                pong = client.ping()
                status[name]["healthy"] = pong
                status[name]["last_seen"] = datetime.now()

                if pong:
                    tools = client.list_tools()
                    status[name]["tools"] = len(tools)

            except Exception as e:
                status[name]["healthy"] = False
                status[name]["errors"].append(str(e))

        yield status
        time.sleep(interval_s)

# Run health monitor
for snapshot in monitor_servers(["github-mcp", "notion-mcp", "stripe-mcp"], interval_s=30):
    unhealthy = [s for s, v in snapshot.items() if not v["healthy"]]
    if unhealthy:
        print(f"WARNING: Unhealthy servers: {unhealthy}")
    else:
        counts = {s: f"{v.get('tools', 0)} tools" for s, v in snapshot.items()}
        print(f"All healthy: {counts}")
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just use curl to call APIs directly" | MCP handles auth, retries, streaming, type safety, and cross-platform compatibility. Manual curl is tech debt. |
| "One mega-server is simpler" | Single-responsibility servers are independently deployable, testable, and replaceable. Monoliths rot. |
| "MCP is just a wrapper around REST" | MCP is a standardized protocol with tool schemas, resource URIs, streaming, and error codes — not an ad-hoc REST convention. |
| "Discovery is a one-time setup" | Servers come and go, ports change, versions update. Continuous discovery keeps the ecosystem alive. |
| "I know all the servers I need" | Discovery often surfaces servers you didn't know existed — that is the point. |
| "Auto-discovery is over-engineering" | Manual registration breaks the moment the ecosystem grows past 5 servers. Automate it. |

## Output Format

When using MCP clients hub, produce structured results:

```json
{
  "server": "github-mcp",
  "tool": "search_repos",
  "params": {"q": "mcp-server", "limit": 5},
  "result": {
    "status": "success",
    "data": [
      {"name": "modelcontextprotocol/servers", "stars": 12000},
      {"name": "anthropics/anthropic-cookbook", "stars": 8500}
    ],
    "duration_ms": 423
  },
  "chain": null
}
```

For pipeline results:

```json
{
  "pipeline": "Research → Notion → Slack",
  "steps": [
    {"server": "github-mcp", "tool": "search_repos", "status": "success", "duration_ms": 400},
    {"server": "notion-mcp", "tool": "create_database_page", "status": "success", "duration_ms": 250},
    {"server": "slack-mcp", "tool": "send_message", "status": "success", "duration_ms": 180}
  ],
  "total_duration_ms": 830,
  "context": {"iteration": 1, "started_at": "2026-07-16T10:00:00Z"}
}
```

## Process

1. **Discover** — `mcp-discover scan --network 192.168.1.0/24` → find all servers
2. **Connect** — `mcp-client.connect()` for each server, validate tool schemas
3. **Chain** — Build pipelines: server A output → server B input → server C output
4. **Orchestrate** — Use `swarm` skill for parallel independent tasks across servers
5. **Monitor** — Health checks, auto-reconnect, swap failed servers
6. **Scale** — Add servers, compose workflows, measure revenue per server

## Verification

- [ ] `mcp-discover` lists all expected servers with their tool schemas
- [ ] `mcp-client.connect()` succeeds for each discovered server
- [ ] Each server's `list_tools()` returns valid tool definitions with JSON Schema
- [ ] `call_tool()` with valid parameters returns expected structured output
- [ ] `call_tool()` with invalid parameters returns standard MCP error codes (not crashes)
- [ ] Pipeline chains complete end-to-end with correct parameter transformation
- [ ] Failed servers are detected by health monitor within configured interval
- [ ] Auto-discovery registers newly available servers without manual config
- [ ] Authentication flows (Bearer token, env-based, OAuth) resolve correctly
- [ ] Streaming responses deliver partial results incrementally
- [ ] At least 3 servers are connected and producing revenue-generating workflows
- [ ] Rollback plan exists for each server connection (disable, reconnect, swap)


## When to Use
Use this skill when working with clients.
