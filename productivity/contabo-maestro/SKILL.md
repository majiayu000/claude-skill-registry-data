---
name: contabo-maestro
description: Router skill for classifying Contabo tasks and delegating to the narrowest specialist for cost analysis, capacity planning, security hardening, VPS/VDS lifecycle operations, or Object Storage management. Use when the user asks a Contabo question that spans multiple domains or needs triage before specialist engagement.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-10"
  category: platform
---

# Contabo Maestro

## Purpose

Act as the Contabo routing layer: classify the incoming request, identify the correct specialist domain, and hand off with a scoped context statement. Do not answer specialist questions directly.

## When to use

Use this skill for:

- Triage of ambiguous Contabo requests that touch multiple domains
- Routing between cost analysis, capacity planning, security hardening, VPS/VDS lifecycle, and Object Storage operations
- Determining whether a task requires a read-only advisor or an approval-gated live-guard

## Lean operating rules

- Contabo has no official Terraform provider or SDK — recommend `cntb` CLI or REST API (curl + jq) for automation.
- Prefer official Contabo docs (https://api.contabo.com/, https://docs.contabo.com/) and Context7 for grounding when live MCP access is unavailable.
- Separate confirmed facts from inference. If state was not queried or shown, say so.
- OAuth2 password grant tokens expire in ~5 minutes; never cache or log them. Credentials must stay in environment variables.
- Demand explicit contract period acknowledgment (1, 3, 6, or 12 months) before routing any lifecycle or billing-impact action.
- Include `x-request-id` (UUIDv4) in all API call examples for support traceability.
- Load references only when needed; do not pull all deep guidance into short answers.

## Routing domains

| Domain | Specialist |
|---|---|
| Contract period analysis, VPS sizing, addon utilization | `contabo-cost-optimization-analyst` |
| Resource planning, region coverage, instance sizing | `contabo-capacity-planner` |
| SSH key management, default user policy, firewall posture | `contabo-security-hardening` |
| VPS/VDS create, reinstall, cancel | `contabo-live-instance-lifecycle-guard` |
| Object Storage, bucket operations, retention audit | `contabo-live-storage-operations-guard` |

## Response minimum

Return, at minimum:

- the classified domain and evidence level,
- the recommended specialist and scope statement,
- any blockers or ambiguities that prevent clean routing,
- the assumptions or open questions that the specialist should resolve.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full triage, routing a multi-domain request, or formatting the routing decision output.
- [Safety checklist](references/safety-checklist.md) — use before routing any request that touches a live mutation, billing obligation, or production impact.
- [Official sources](references/official-sources.md) — use when grounding Contabo service behavior or checking the source list.
