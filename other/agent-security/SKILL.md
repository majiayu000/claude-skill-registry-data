---
name: agent-security
description: "Audit AI agents and MCP servers for prompt injection, over-permissioning, and data-exfiltration paths. Use when building or reviewing agent configs, tools, MCP servers, or system prompts."
---

# agent-security

Treat prompts, tool output, retrieved content, webhooks, and client-provided identity fields as untrusted until a boundary validates them.
## Inspection

Inventory tools, permissions, data stores, egress paths, and who can invoke what; trace where untrusted text can reach the model or tool calls.

## Decision rules

Least privilege per tool; confirmation on destructive actions; output filtering for secrets/PII; budgets + logging on every loop.


## Activate when

- Designing or reviewing agent tool definitions, MCP servers, system prompts, or orchestration code.
- Answering "is this agent setup safe?" before deployment.

## Do NOT activate for

- Application code without LLM/agent surface (see secure-baseline).
- Model capability evaluation (see ai/agent-architecture).

## Procedure

1. Inventory: tools, permissions, data stores, network egress, and who can invoke what.
2. Injection surface: where untrusted text can reach the model or be quoted into tool calls; check for tool-call injection and indirect prompt injection via retrieved docs.
3. Agency check: least privilege per tool, confirmation for destructive/irreversible actions, output filtering for PII/credentials, action budgets, and logging of agent actions.
4. MCP review: least-privilege servers, no confused-deputy flows, no data exposure across trust boundaries.
5. Test: run prompt-injection probes (direct + indirect via retrieved content) and assess LLM-app risk against OWASP LLM Top 10.
6. Report: permission findings, injection paths with reproduction steps, guardrail gaps, residual risk + owner.
7. Verify: re-run probes after fixes (previously failing probe now blocked + logged), confirm destructive actions require confirmation end to end, never declare "agent is safe" — report residual risk with an owner.

## Failure modes

Over-permissioned MCP servers; tool output trusted as instructions; no confirmation on irreversible actions; secrets in memory stores.

## Escalation

App-code findings → security/secure-baseline; MCP mechanics → ai/mcp-engineering.
