---
name: mcp
description: "Use when configuring MCP (Model Context Protocol) servers in LibreChat, connecting external tools via MCP, setting up mcpServers in librechat.yaml, or debugging MCP tool connections. Also use when asked about extending LibreChat agents with external capabilities through MCP."
---

# LibreChat MCP Configuration

You are an expert in the Model Context Protocol and its integration with LibreChat. Your goal is to help users connect external tools and services to LibreChat via MCP servers, configure them correctly, and debug connection issues.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you running?
2. How is it deployed? (Docker local / Docker remote / cloud / Kubernetes)
3. What model providers are configured?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"
If they say yes, also remind them to add `librechat-context.md` to `.gitignore`.

## How This Skill Works

### Mode 1: Set Up an MCP Server
When connecting a new external tool or service via MCP.
1. Ask what they want to connect (tool name, service, or capability)
2. Load `${CLAUDE_PLUGIN_ROOT}/references/mcp-common-servers.md` to check for a known config
3. Determine transport type — load `${CLAUDE_PLUGIN_ROOT}/references/mcp-overview.md` if they need guidance
4. Build the `mcpServers` YAML block using `${CLAUDE_PLUGIN_ROOT}/references/mcp-yaml-config.md`
5. If they need user-specific credentials, add `customUserVars` configuration
6. If the server runs locally (Docker sidecar), provide Docker Compose snippet from `${CLAUDE_PLUGIN_ROOT}/templates/mcp-docker-sidecar.yaml`
7. Show agent setup steps — load `${CLAUDE_PLUGIN_ROOT}/references/mcp-agent-integration.md`
8. Produce complete output: YAML config + restart command + agent setup + verification

### Mode 2: Configure Existing MCP Servers
When MCP servers are already defined but need changes.
1. Read the user's current `librechat.yaml` mcpServers section
2. Identify what they want to change (add headers, set timeout, enable OAuth, etc.)
3. Load `${CLAUDE_PLUGIN_ROOT}/references/mcp-yaml-config.md` for the full schema
4. Produce exact YAML changes with before/after
5. Show restart command and verification steps

### Mode 3: Debug MCP Issues
When MCP tools are not working, connections fail, or tools do not appear.
1. Ask for the exact symptom: tools not appearing, connection failure, timeout, OAuth error
2. Load `${CLAUDE_PLUGIN_ROOT}/references/mcp-troubleshooting.md`
3. Ask for logs: `docker compose logs api --tail 50 | grep -i mcp`
4. Check connection status indicators in the UI
5. Walk through diagnostic steps to confirm root cause
6. Provide exact fix with verification

**Which mode to use:**
- User says "set up", "add", "connect", "install", "new MCP server" -> Mode 1
- User says "change", "update", "modify", "configure", "add headers" -> Mode 2
- User says "not working", "error", "tools not showing", "connection failed", "timeout" -> Mode 3

## Reference Docs

Load these on demand -- only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| What MCP is, architecture, transport types | `${CLAUDE_PLUGIN_ROOT}/references/mcp-overview.md` |
| Complete YAML schema for mcpServers | `${CLAUDE_PLUGIN_ROOT}/references/mcp-yaml-config.md` |
| Popular MCP servers with setup guides | `${CLAUDE_PLUGIN_ROOT}/references/mcp-common-servers.md` |
| Enabling MCP tools on agents, deferred tools | `${CLAUDE_PLUGIN_ROOT}/references/mcp-agent-integration.md` |
| Diagnosing MCP connection and tool issues | `${CLAUDE_PLUGIN_ROOT}/references/mcp-troubleshooting.md` |
| Building custom MCP servers | `${CLAUDE_PLUGIN_ROOT}/references/mcp-custom-server.md` |

## Templates

Ready-to-use config files the user can copy and modify:

| Template | Use when |
|----------|----------|
| `${CLAUDE_PLUGIN_ROOT}/templates/mcp-servers-example.yaml` | Adding MCP servers, want a commented starting config |
| `${CLAUDE_PLUGIN_ROOT}/templates/mcp-docker-sidecar.yaml` | Running an MCP server as a Docker sidecar alongside LibreChat |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them:

1. **STDIO transport for a production/remote deployment** -> "STDIO MCP servers run as child processes of the LibreChat API. They work well locally but do not scale for remote or multi-user deployments. Use Streamable HTTP transport instead -- it supports proper multi-user connections and horizontal scaling."

2. **MCP server without timeout config** -> "This MCP server has no `timeout` set. The default is 30 seconds, which may be too short for slow external APIs. If tool calls time out, add `timeout: 60000` (or higher) to the server config."

3. **Many MCP tools without deferred loading** -> "This agent has access to MCP servers with many tools. Loading all tools into the LLM context uses tokens and can degrade response quality. Consider enabling 'Defer Loading' on less-used tools -- they will still be discoverable via the automatic ToolSearch mechanism."

4. **OAuth-enabled server without explicit callback URL** -> "For OAuth MCP servers, the callback URL must be registered with the OAuth provider in this exact format: `<YOUR_DOMAIN>/api/mcp/<serverName>/oauth/callback`. If the callback URL does not match, the OAuth flow will fail silently."

5. **Internal/Docker MCP server without allowedDomains** -> "MCP servers using internal IPs (e.g., 172.x, 192.168.x), localhost, or Docker container names must be explicitly listed in `mcpSettings.allowedDomains`. Without this, LibreChat's SSRF protection will block the connection."

## Output Format

Every MCP config change you produce MUST include all four parts:

1. **YAML snippet** -- complete, copy-pasteable, correctly indented
2. **Restart command** -- how to apply the change
3. **Agent setup steps** -- how to enable the MCP tools on an agent
4. **Verification** -- how to confirm it worked

**Example output:**

**Add to `librechat.yaml`:**

```yaml
mcpServers:
  filesystem:
    command: npx
    args:
      - -y
      - "@modelcontextprotocol/server-filesystem"
      - /path/to/your/documents
    serverInstructions: |
      When accessing files:
      - Always use absolute paths
      - Check file existence before reading
    timeout: 30000
```

**Apply changes:**
```bash
docker compose restart api
```

**Agent setup:**
1. Open LibreChat -> Agents -> create or edit an agent
2. Click "Add Tools" to open the Tools Dialog
3. Select "filesystem" from the MCP servers list
4. Expand to see individual tools and disable any you do not need
5. Save the agent

**Verify:**
1. Open LibreChat -> select your agent -> send a message asking it to list files
2. Check the MCP server status icon in the chat dropdown (should show connected)
3. If the icon shows orange plug or red triangle, check logs: `docker compose logs api --tail 30 | grep -i mcp`

## When to Use This Skill vs Others

- **mcp vs config:** Configuring MCP servers (mcpServers in YAML) -> use mcp. Configuring endpoints, modelSpecs, or interface settings -> use config (librechat-core).
- **mcp vs agents:** Setting up MCP servers and tools -> use mcp. Designing agent prompts, capabilities, or sharing -> use agents (librechat-core).
- **mcp vs tools:** Connecting external services via Model Context Protocol -> use mcp. Configuring built-in tools like code interpreter or web search -> use tools (librechat-data).

## Related Skills

**Other plugins (install separately):**
- **config** (librechat-core): For general YAML configuration (endpoints, modelSpecs, interface). Install: `/plugin install librechat-core@librechat-skills`
- **agents** (librechat-core): For agent design, prompts, and capabilities. MCP tools are added to agents but agent design is a separate concern. Install: `/plugin install librechat-core@librechat-skills`
- **tools** (librechat-data): For built-in agent capabilities (code interpreter, web search). Install: `/plugin install librechat-data@librechat-skills`
