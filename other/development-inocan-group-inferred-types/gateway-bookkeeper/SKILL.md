---
name: gateway-bookkeeper
description: "Enforce MCP-first tool usage through a centralized gateway/bookkeeper: discover MCP capabilities, route intents to the best MCP tool, block non-MCP execution when an MCP equivalent exists, and log all tool calls/results with auditable fallbacks. Use when building or operating a multi-agent system where agents must not access tools/networks directly and all actions must be policy-enforced and recorded."
---

# Gateway Bookkeeper

## Overview

Operate a central gateway that is the only MCP client: agents submit intents; the gateway resolves to MCP tools via a capability registry, executes with full logging, blocks bypass attempts, and permits tightly-controlled fallbacks only when MCP is unavailable or insufficient.

## MCP-First Enforcement

### MCP-First Principle

- If an action can be performed via an **MCP server/tool**, perform it via MCP.
- Direct execution (local libraries, ad-hoc HTTP calls, custom scripts) is blocked by default unless explicitly allowed as a fallback with justification and logged approval.

### MCP Discovery and Registry

Implement an MCP registry inside the gateway:

- `register_mcp_server(server_id, capabilities, tools, auth_context, healthcheck)`
- `refresh_capabilities(server_id)` (periodic or on-demand)

Maintain a capability index:

- `capability → [server_id, tool_name, constraints, cost/latency hints]`

### Tool Routing: MCP Resolution Step (mandatory)

Every tool request MUST go through the MCP resolution pipeline:

1. Intent classify (e.g., “read repo file”, “create PR”, “query dataset”, “write doc”, “deploy”, “search web”).
2. Resolve the best MCP tool:
   - exact match > high-confidence match > fallback candidates
3. Enforce:
   - If an MCP tool exists: route only via MCP
   - If multiple MCP tools qualify: choose by policy (preferred servers, least privilege, auditability, cost)
4. Execute via MCP with full logging:
   - log `MCP_TOOL_CALL` and `MCP_TOOL_RESULT`
   - store metadata: server, tool name, args, output refs, errors, retries

### Policy: No Direct Tools Unless Proven Necessary

Reject attempts to:

- call tools directly (bypassing the gateway)
- call non-MCP tools when an MCP equivalent exists

Return a structured denial:

- `POLICY_BLOCKED` including:
  - recommended MCP tool(s)
  - required parameters or missing context
  - steps to comply

### Fallback Rules (when MCP isn’t available)

Fallback is allowed only if all are true:

- No MCP tool exists for the capability OR MCP tools are unhealthy/unreachable
- The fallback tool is in an approved allowlist
- A justification is provided and logged
- For higher-risk actions: require approval from a designated approver role

Ledger entries must clearly mark:

- `execution_path: MCP | FALLBACK`
- `fallback_reason: no_mcp | mcp_unhealthy | mcp_insufficient | emergency_override`
- any approval references

### MCP Compliance Checks (auditor mode)

Generate an “MCP Compliance Report” including:

- % of tool calls executed via MCP
- list of fallback tool calls + justification + approvals
- detected bypass attempts (blocked/allowed)
- gaps in MCP coverage (capabilities frequently requested without MCP tools)

### Hard Enforcement: Gateway as the Only MCP Client

Agents must never talk to MCP servers directly.

- Only the gateway holds MCP connection credentials/session state.
- Agents submit requests to the gateway; the gateway invokes MCP tools and returns results.
- This guarantees centralized logging, policy enforcement, and consistent tool selection.

### Optional: Capability-Driven Guidance for Agents

When returning tool options, provide “how to ask” guidance:

- “Use MCP tool X with parameters A/B/C”
- “Required input format”
- “Evidence/artifact refs to attach”

## Enforceability Constraint (recommended)

If the runtime permits, remove outbound network/tool access from agents entirely; allow access only through the gateway. Without this, an agent can still attempt side-channel bypasses.
