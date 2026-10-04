---
name: sap-maestro
description: Route SAP AI workflow requests to the correct domain skill using taxonomy classification, a routing table, and dispatch mode selection. Use when an incoming request spans multiple SAP domains (BTP, S/4HANA, SuccessFactors, Ariba, etc.) and the correct downstream skill or agent must be identified before any action is taken. Does not touch live systems.
allowed-tools: Read Grep Glob WebSearch WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-19"
  category: platform
  lifecycle: experimental
---

# SAP Maestro

## Purpose

Classify, route, and dispatch SAP AI workflow requests to the correct domain skill or agent without conflating guidance across unrelated SAP domains. Maestro is a pure routing layer — it reads domain taxonomy, applies a routing table, selects a dispatch mode, and passes control to the appropriate downstream skill. It does not execute business logic, mutate live systems, or make architectural recommendations on behalf of domain skills.

## When to use

Use this skill when the request:

- spans or may span multiple SAP product domains (BTP, S/4HANA, SuccessFactors, Integration Suite, Ariba, Datasphere, GRC, Transport Management, etc.),
- is ambiguous about which SAP skill or agent should handle it,
- needs an explicit routing decision logged before dispatch (compliance or traceability requirement),
- involves maestro-gated dispatch — i.e., downstream skills or agents require an upstream classification before they will accept a request.

## When not to use

- When the domain is already known and a specific skill (e.g., `sap-clean-core-debt-review`, `sap-live-readonly-landscape-discovery`, `sap-guarded-transport-import`) should be invoked directly.
- When the request is purely informational and no routing or dispatch is needed.
- When the downstream skill is already loaded and active in the current session.

## Does not touch live systems

This skill is a pure routing and classification layer. It does not connect to any SAP system, issue API calls, read from BTP cockpit, query ABAP systems, or invoke transport management services. All live-system interaction is delegated to downstream skills that carry their own live-environment access rules.

## Lean operating rules

- Classify first. Every request must receive a domain classification before any dispatch action is proposed.
- Use the routing table verbatim. Do not improvise skill-to-domain mappings from memory; use the documented routing table in `references/workflow-and-output.md`.
- One domain per dispatch. If the request genuinely crosses domains, split it into domain-scoped sub-requests and route each separately.
- Surface routing rationale. Always state which taxonomy bucket was matched, which routing table entry fired, and which dispatch mode was selected.
- Live-guard gate. If the routed skill carries a live-environment tier (`read-only-runtime` or `mutating-runtime`), call out the live-guard requirement explicitly before proposing dispatch. Do not bypass the gate.
- Do not hallucinate skill IDs. Only route to skills and agents that are declared in the catalog. If no matching skill exists, return `unrouted` and explain why.
- Prefer official SAP documentation for taxonomy clarification; use `references/official-sources.md` for grounding.

## Evidence rules

Label all claims with one of:

- `documentation-based` — grounded in SAP official docs or BTP taxonomy
- `catalog-evidence` — grounded in a declared skill/agent entry in this repo
- `user-provided evidence` — stated by the user in this session
- `inference` — derived reasoning not directly confirmed by docs or catalog

## Live-environment rules

**This skill does not touch live systems.** There is no credential, API call, shell command, or system connection of any kind in this skill's execution path. If a routing decision leads to a downstream skill that does touch live systems, those rules apply to the downstream skill — not here.

## References

Load only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — routing table, domain taxonomy, dispatch modes, output format.
- [Safety checklist](references/safety-checklist.md) — routing safety, live-guard gate, non-negotiables before dispatch.
- [Official sources](references/official-sources.md) — SAP BTP taxonomy, product catalog, and domain classification grounding.

## Response minimum

Return, at minimum:

- **Problem classification**: which SAP domain(s) are in scope and why.
- **Evidence used**: documentation-based / catalog-evidence / user-provided / inference.
- **Routing table match**: which entry in the routing table was fired.
- **Dispatch mode**: direct / gated / split / unrouted.
- **Risk level**: none (pure classification) / low (advisory dispatch) / elevated (dispatch to live-tier skill).
- **Recommended action**: load the named skill or agent, or explain why routing is unrouted.
- **Refusal / escalation triggers**: if the request matches a live-tier skill and no live-guard approval is present, escalate before dispatch.
- **Business impact**: what breaks if routing is wrong (wrong domain skill gives wrong guidance).
- **Next verification step**: confirm with the user that the classification is correct before dispatching to a mutating-runtime skill.
