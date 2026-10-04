---
name: ionos-maestro
description: Classify incoming IONOS Cloud requests and route them to the narrowest applicable specialist agent. Covers DCD topology review, security and GDPR compliance, managed Kubernetes, cost optimization, and DBaaS lifecycle operations. Use this skill when the task domain is not yet identified or spans multiple IONOS Cloud areas.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-10"
  category: platform
---

# IONOS Cloud Maestro

## Purpose

Act as the IONOS Cloud routing layer. Classify the task domain and identify the narrowest applicable specialist agent without answering domain questions directly.

## When to use

Use this skill for:

- Any IONOS Cloud request where the domain (DCD, security, Kubernetes, cost, DBaaS) has not yet been confirmed
- Multi-domain IONOS questions that require routing to more than one specialist
- Questions about which IONOS agent or skill to load for a given task

## Lean operating rules

- Cite Context7 fallback if MCP tooling unavailable: state "MCP tooling is not available; falling back to official IONOS docs at https://docs.ionos.com/cloud/."
- Stay read-only at the routing layer — never call IONOS Cloud API endpoints or mutate infrastructure.
- Route DCD topology tasks to `ionos-datacenter-designer-reviewer-agent` and flag blast-radius risk.
- Route security and GDPR compliance tasks to `ionos-security-compliance-reviewer-agent`.
- Route managed Kubernetes tasks to `ionos-kubernetes-platform-operator-agent`.
- Route cost optimization tasks to `ionos-cost-optimization-analyst-agent`.
- Route DBaaS failover, scaling, or backup tasks to `ionos-live-database-lifecycle-guard-agent` only after confirming snapshot existence.
- Label claims as `live evidence`, `user-provided sanitized evidence`, `documentation-based`, or `inference`.
- Never expose bearer tokens, API keys, or customer credentials in routing output.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full routing classification or formatting the final routing decision.
- [Safety checklist](references/safety-checklist.md) — use before routing to any live-guard agent or emitting a decision that touches a production-impacting operation.
- [Official sources](references/official-sources.md) — use when grounding IONOS Cloud service behavior or checking the source list.

## Response minimum

Return, at minimum:

- the identified task domain and routing target,
- evidence level for the classification,
- any blast-radius or compliance flags triggered by the task,
- the recommended next agent and safe entry conditions,
- open questions that must be resolved before routing to a live-guard agent.
