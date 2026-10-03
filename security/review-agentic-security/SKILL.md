---
name: review-agentic-security
description: Audit security boundaries in AI agents, multi-agent systems, MCP integrations, autonomous workflows, and copilots with side-effecting tools. Use when reviewing tool permissions, agent identities, delegation, memory, inter-agent messages, approval gates, code execution, supply-chain trust, failure propagation, kill controls, or effective least privilege.
---

# Review Agentic Security

Trace how goals become actions under effective identities and privileges. Evaluate deterministic controls around the model instead of assuming the agent will follow instructions.

Read [methodology](references/methodology.md) before building the capability graph or assigning agentic risk mappings.

## Safety boundaries

- Review code, manifests, policies, and effective permissions read-only by default.
- Require explicit authorization before invoking a live tool or changing agent state.
- Replace send, delete, pay, publish, deploy, execute, grant, and external-write operations with stubs or isolated fixtures.
- Use synthetic accounts, data, credentials, memories, and inter-agent messages.
- Stop if inherited credentials, cross-tenant data, hidden production effects, or an uncontrolled autonomous loop appears.
- Do not publish credentials, sensitive prompts, tool secrets, or weaponized agent instructions.

## Workflow

1. **Frame the workflow.** Record the agent's intended goal, users, autonomy level, consequential actions, approval policy, environment, owners, and risk tolerance.
2. **Inventory the graph.** List agents, models, prompts, planners, routers, tools, MCP or other protocol servers, memory stores, message buses, external services, identities, credentials, sandboxes, monitors, and kill paths.
3. **Map effective capability.** Trace `instruction source -> agent -> identity -> tool schema -> validation -> resource -> side effect`. Record declared and effective permissions, credential inheritance, tenant scope, egress, and delegation depth.
4. **Review tool contracts.** Check tool descriptions, argument schemas, server-side authorization, input and output validation, allowlists, idempotency, rate and cost limits, timeout, rollback, and audit logs.
5. **Review control points.** Evaluate goal integrity, trusted and untrusted context separation, meaningful human confirmation, least privilege, secret isolation, code-execution sandboxing, memory provenance and expiry, inter-agent authentication, and state transition guards.
6. **Test bounded scenarios.** Use stubs to exercise malicious tool output, ambiguous goals, forged messages, poisoned memory, privilege confusion, unsafe delegation, repeated actions, partial failure, stop commands, and recovery.
7. **Trace propagation.** Determine whether one compromised agent, tool, message, or memory entry can cause lateral action, privilege expansion, persistent influence, cascading failure, or uncontrolled cost.
8. **Prioritize fixes.** Move authorization and validation outside model judgment, reduce capability, add reversible stages, improve observability, and create regression tests for every confirmed path.

## Evidence rules

- Capture source locations for prompts, tool schemas, policies, IAM, memory handling, and approval code.
- Verify effective permissions through configuration, provider policy, or authorized no-op tests; do not trust declared scopes alone.
- Preserve full tool-call and delegation traces with secrets redacted.
- Record identity, tenant, state, model, prompt, tool, and server versions for every dynamic test.
- Separate observed behavior from inferred reachability.
- Require a full capability or propagation path and evidence references for every finding.

## Output contract

Return:

1. Scope, target fingerprint, autonomy assumptions, and limitations.
2. Agent, identity, credential, tool, memory, and dependency inventory.
3. Capability graph and trust-boundary diagram.
4. Effective-permission matrix with consequential actions and required approval.
5. Scenario matrix with expected controls, observed traces, cleanup, and evidence.
6. Findings with attack or failure chain, blast radius, severity, confidence, and framework mapping.
7. Prioritized least-privilege, containment, recovery, and observability plan with regression tests.
8. Unknown, untested, out-of-scope, and residual-risk sections.

Write each finding as: `ID | affected agent or tool | initiating condition | effective identity | capability chain | violated control | side effect or blast radius | evidence | severity | confidence | remediation | regression | framework mapping`.

## Quality gate

Do not finalize until:

- Every consequential tool maps to an effective identity, authorization check, confirmation rule, and rollback or recovery path.
- Declared permissions are compared with effective permissions.
- Human approval is tested for clarity, context, binding to exact arguments, freshness, and bypass resistance.
- Memory, inter-agent communication, tool output, and external content are classified by trust and provenance.
- Stop, timeout, retry, partial-failure, and duplicate-action behavior are assessed.
- Every dynamic test uses a stub, sandbox, or explicitly authorized reversible target.
- Every finding includes a full chain and a deterministic regression test where feasible.
