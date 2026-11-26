---
name: agent-governance-lord
description: Lord skill for governing AI coding agents at runtime — gateway interception, agent/flow/model allowlisting, and MCP-server-as-securable. The control layer between an agent's decision and its real-world action.
triggers:
  - agent governance lord
  - agent governance
  - agent gateway
  - runtime interception
  - agent allowlist
  - mcp securable
  - حوكمة الوكلاء
  - بوابة الوكلاء
personas:
  - ARCH
  - SEC
  - SRE
  - API
  - DEVOPS
tech_stack: []
lord: true

---

# Agent Governance Lord

[OBJ] Runtime governance for AI coding agents: intercept, allowlist, and audit every agent action.

## Problem

AI agents can write, push, and deploy without human review at each step. Access control answers "can the agent do this?" — governance answers "should the agent do this?" Permission is necessary; it is not sufficient. An agent can be fully permitted and still wrong.

## Rules

1. [REQ] **Gateway on the path.** Every LLM request and MCP tool call MUST pass through `runtime/agent_gateway.py` (pre-LLM + post-execution guardrails). No bypass.
2. [REQ] **Three verdicts.** Guardrails emit ALLOW / REDACT / BLOCK. Most severe wins (BLOCK > REDACT > ALLOW). Never silently drop a BLOCK.
3. [REQ] **Pre-LLM guardrails.** Inspect outbound prompt + tool payloads BEFORE the model sees them. Catch: secret leakage, prompt injection in tool responses fed back, forbidden tool calls.
4. [REQ] **Post-execution guardrails.** Inspect inbound response + generated code BEFORE the developer sees it. Catch: destructive commands, insecure patterns, hallucinated APIs.
5. [REQ] **Agent allowlist.** Only agents registered in `runtime/agent_catalog.py` with `status == ALLOWED` may run. Unknown agent = BLOCK + alert.
6. [REQ] **Flow allowlist.** Each agent has an `allowed_flows` list. A flow not in the list = BLOCK. No blanket flow access.
7. [REQ] **Model allowlist.** Each agent has an `allowed_models` list. A model not in the list = BLOCK. Prevents unauthorized model escalation.
8. [REQ] **MCP-as-securable.** MCP servers registered in `runtime/mcp_securable.py` as governed assets. Access via GRANT policies (USE/ADMIN/REGISTER). No ungoverned MCP server.
9. [REQ] **Composite identity.** Every agent action attributed to BOTH agent + human principal (`runtime/composite_identity.py`). No anonymous agent actions.
10. [REQ] **Audit every verdict.** Every ALLOW/REDACT/BLOCK logged with agent_id, user_id, tool, reason. Tamper-evident via existing audit chain.
11. [REQ] **Rate limiting.** Per-agent rate limits enforced at the gateway. Burst > threshold = BLOCK + cooldown.
12. [REQ] **Cost attribution.** Per-agent cost tracked via `runtime/cost_attribution.py`. Anomaly (spike/budget breach) = alert + optional throttle.
13. [REQ] **Plan validation.** Before edits, validate the agent's plan via `runtime/plan_diff_validator.py`. Forbidden paths = BLOCK. File count > max = WARN.
14. [REQ] **Diff validation.** After edits, validate the git diff. Undeclared imports = WARN. Test gap = WARN. Unrelated refactor = WARN.
15. [REQ] **Supply-chain guard.** New imports not in lockfile = WARN. External package not declared = BLOCK in strict mode.
16. [REQ] **Human-in-the-loop.** Irreversible/destructive actions (rm, drop, force-push, deploy to prod) require explicit human approval. Gateway holds the action pending approval.
17. [REQ] **Rollback path.** Every agent action that modifies state must have a documented rollback. No rollback = BLOCK.
18. [PROHIBIT] Bypassing the gateway for "trusted" agents. All agents pass through.
19. [PROHIBIT] Allowing an agent to call an ungoverned MCP server.
20. [PROHIBIT] Executing a destructive action without composite identity attribution + human approval.
21. [REQ] **SARC enforcement sites.** Implement 4 enforcement sites: Pre-Action Gate (block injection/PII/policy violations before LLM call), Action-Time Monitor (rate/cost/budget enforcement, circuit breakers), Post-Action Auditor (log, evaluate, score for reliability@k), Escalation Router (human approval, kill-switch, incident creation).
22. [REQ] **Agent SRE Governance v1.0.** Implement SLOs, error budgets, circuit breakers, chaos engineering, trace replay, Ed25519 artifact signing, SBOMs, and OpenTelemetry for all agent deployments. Reference: Microsoft Agent Governance Toolkit.
23. [REQ] **Microsoft Agent Hooks.** Support framework-neutral governance contracts — "deny means deny" enforceable across LangChain, CrewAI, OpenAI Agents SDK, etc.
24. [REQ] **MCP 2026-07-28 stateless governance.** Update gateway for stateless MCP protocol. No session state assumptions. Per-request protocolVersion validation. Header-based routing (Mcp-Method, Mcp-Name).
25. [REQ] **Per-PR spend limits.** Implement per-PR spend caps (soft block) and org-level ACU visibility. Devin enterprise pattern.
26. [REQ] **Enterprise MCP server allowlist.** Maintain allowlist of approved MCP servers. Block ungoverned servers. Enterprise plugin governance (required/optional/forbidden plugins).
27. [REQ] **5-layer control plane.** Gateway Layer (auth, rate limiting, cost tracking) → Policy Layer (4-level hierarchy, fail-closed) → Observability Layer (tamper-evident audit) → Governance Layer (approvals, kill-switch, RBAC) → Integration Layer (A2A, MCP, REST, webhooks).
28. [PROHIBIT] Deploying agents without SARC 4-site enforcement and Agent SRE Governance compliance.

## Enforcement Stack

```
Agent request → AgentGateway.check_request (pre-LLM)
             → AgentCatalog.is_agent_allowed
             → AgentCatalog.is_flow_allowed_for_agent
             → AgentCatalog.is_model_allowed_for_agent
             → McpSecurableRegistry.check_permission (if MCP)
             → LLM call
             → AgentGateway.check_response (post-execution)
             → PlanDiffValidator.validate_diff (if code generated)
             → SupplyChainGuard.check_diff (if imports added)
             → CostAttribution.record
             → AuditLogger.log (composite identity)
```

## References

- Fiddler AI: "controls only hold where they sit on the agent's request and response path."
- GitLab Duo: composite identity, agent/flow catalog, tool approval guardrails.
- Databricks Unity Catalog: MCP servers as securables with GRANT policies.
- repo-contract: negative-constraint enforcement (most effective for safe agent workflows).
