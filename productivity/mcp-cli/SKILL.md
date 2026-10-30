---
name: mcp-cli
description: "Use when needing to interact with MCP servers on-demand via CLI without permanently loading integrations, discover available tools/resources on an MCP server, or call MCP tools from the command line. Triggers on: 'mcp cli', 'mcp tool call', 'call mcp server', 'discover mcp tools', 'mcp on-demand', 'mcp command line', 'mcp binary', 'list mcp tools', 'invoke mcp', 'mcp without integration'."
source: obra/superpowers-lab (MIT) — superpowers-lab/skills/mcp-cli
tier: TIER 3 — PRODUCTIVITY
---

# MCP CLI — On-Demand MCP Server Interaction
# Source: obra/superpowers-lab (MIT) — github.com/obra/superpowers-lab

Dùng `mcp` CLI binary để gọi MCP servers **on-demand** mà không cần load vĩnh viễn vào config.
Context sạch, không bloat, không cần restart Claude Code.

Khác `terminal--mcp-client` (SDK-based programmatic): cái này là CLI tool cho human/agent dùng trực tiếp.

---

## Khi nào dùng

- Muốn thử một MCP server mới mà không commit vào config
- Debug tool call từ MCP server
- Automation script cần gọi MCP tool
- Xem schema của tool trước khi integrate

---

## Setup

```bash
# Cài mcp CLI binary
npm install -g @modelcontextprotocol/cli 2>/dev/null \
  || pip install mcp-cli 2>/dev/null

# Verify
mcp --version

# Đảm bảo có trong PATH
export PATH="$HOME/.local/bin:$PATH"
```

---

## Workflow chuẩn: Discover → Schema → Call → Cleanup

```bash
# 1. Discover tools trên server
mcp tools npx -y @modelcontextprotocol/server-filesystem /tmp

# 2. Xem schema chi tiết
mcp tools --format json npx -y @modelcontextprotocol/server-filesystem /tmp \
  | python3 -m json.tool | head -60

# 3. Call tool
mcp call read_file \
  --params '{"path": "/tmp/test.txt"}' \
  npx -y @modelcontextprotocol/server-filesystem /tmp

# 4. Alias cho session (tránh type lại)
mcp alias fs "npx -y @modelcontextprotocol/server-filesystem /tmp"
mcp tools fs
mcp call read_file --params '{"path":"/tmp/test.txt"}' fs

# 5. Remove alias sau khi xong
mcp alias rm fs
```

---

## Các loại operations

```bash
# List tools
mcp tools <server-cmd>

# List resources
mcp resources <server-cmd>

# List prompt templates
mcp prompts <server-cmd>

# Read resource
mcp read "file:///tmp/test.txt" <server-cmd>

# Get prompt template
mcp prompt my-prompt-name --args '{"key":"value"}' <server-cmd>
```

---

## Authentication

```bash
# HTTP Basic Auth
mcp tools --auth user:password http://mcp.server:3000

# Bearer Token
mcp tools --header "Authorization: Bearer $TOKEN" http://mcp.server:3000

# Từ env var
MCP_AUTH_TOKEN=sk-xxx mcp call tool_name --params '{}' http://mcp.server:3000
```

---

## Common Servers

```bash
# Filesystem (local files)
mcp tools npx -y @modelcontextprotocol/server-filesystem /workspace

# Memory / Knowledge Graph
mcp tools npx -y @modelcontextprotocol/server-memory

# GitHub (cần GITHUB_TOKEN)
GITHUB_TOKEN=ghp_xxx mcp tools npx -y @modelcontextprotocol/server-github

# Brave Search (cần BRAVE_API_KEY)
BRAVE_API_KEY=xxx mcp tools npx -y @modelcontextprotocol/server-brave-search

# Puppeteer (browser automation)
mcp tools npx -y @modelcontextprotocol/server-puppeteer

# Sequential Thinking
mcp tools npx -y @modelcontextprotocol/server-sequential-thinking
```

---

## Transport types (auto-detected)

```bash
# stdio (default — local npx/cmd)
mcp tools npx -y @my/server

# HTTP
mcp tools http://localhost:3000

# SSE
mcp tools --transport sse http://localhost:3000/sse
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng mcp-cli cho servers cần permanent config (dùng .mcp.json thay thế)
❌ FAIL nếu pass secrets trong --params JSON (dùng env var)
✅ PASS khi: mcp tools trả về list hợp lệ + call trả về expected result
```

## See also
- `terminal--mcp-client` — SDK-based programmatic MCP integration
- `agent-reach` — reach external platforms (Twitter, GitHub, Reddit) qua HTTP

