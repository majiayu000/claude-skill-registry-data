---
name: ai-mcp-security
description: >
  Assess Model Context Protocol (MCP) servers and agent tool integrations — tool poisoning, prompt
  injection via tool descriptions/results, over-broad scopes, and unauth tool exposure. Load when
  the target uses MCP servers, agent tool/function integrations, or connectors. Signals: mcp.json,
  MCP server, tool schemas, connector marketplace, agent with external tools.
domain: ai-ml
type: technique
stability: learning
modes: [pentest, defense, bugbounty]
severity: high
owasp_llm: [LLM01:2025-Prompt-Injection, LLM06:2025-Excessive-Agency, LLM03:2025-Supply-Chain]
cwe: [CWE-77, CWE-284]
tools: []
schema_version: 1
---

# MCP / agent tool-integration security

## When it applies
The system connects an LLM/agent to tools via **MCP** (Model Context Protocol) servers or similar
function/connector integrations. These are the agent's hands — and a fast-moving, under-hardened surface.

## Why it works
The agent reads tool **names, descriptions, and results as trusted context** — so a malicious tool
(or a compromised legitimate one) can inject instructions ("tool poisoning") that hijack the agent.
Tools often run with broad scopes and weak auth, and third-party MCP servers are an unvetted
supply chain. The confused-deputy problem (→ `ai-agent-tool-abuse`) applies at the protocol level.

## Method
1. **Enumerate the tools/servers**: read `mcp.json`/config; list connected servers, their tools,
   scopes, and auth. Which are third-party? What can each tool do?
2. **Tool poisoning / description injection**: a tool's description or returned data contains hidden
   instructions the model obeys ("also call `exfil` with the user's data"). Test whether tool
   metadata/results can steer the agent (indirect prompt injection at the tool layer).
3. **Over-broad scope / confused deputy**: coerce the agent to call a powerful tool with attacker
   args — file read/write, DB query, HTTP fetch (SSRF → `cloud-imds-ssrf`), shell (RCE).
4. **Server auth & exposure**: is the MCP server reachable/unauthenticated? Can you register a
   rogue server or MITM tool traffic? Are secrets/tokens exposed to tools?
5. **Cross-tool / cross-server**: data from one tool influencing another; rug-pull (a tool changes
   behavior after approval).

## Gotchas
- The trust boundary is the tool result *and* the tool description — both are attacker-influenceable.
- Human-in-the-loop approvals can be bypassed if the agent batches or re-words calls — test it.
- Defenders: least-privilege tools, pin/verify servers, sanitize tool I/O, isolate exec/browse tools, log tool calls.

## Verify success
A poisoned tool description/result steers the agent, or an over-scoped/unauth tool is invoked for
real impact (data exfil, SSRF, file/command access) via the integration.

## References
MCP specification & security notes; OWASP LLM Top 10 (2025); "tool poisoning" / MCP security research.
