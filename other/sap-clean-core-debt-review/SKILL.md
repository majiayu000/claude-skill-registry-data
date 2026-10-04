---
name: sap-clean-core-debt-review
description: Review SAP custom code, modifications, and extensibility debt against the SAP Clean Core standard. Use when assessing custom ABAP, implicit enhancements, customer modifications, or legacy Z/Y code for remediation toward released APIs, ABAP Cloud, RAP objects, key-user extensibility, or developer extensibility on BTP. Does not touch live systems.
allowed-tools: Read Grep Glob WebSearch WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-19"
  category: architecture
  lifecycle: experimental
---

# SAP Clean Core Debt Review

## Purpose

Assess the clean core compliance posture of SAP custom code, customer modifications, and extensibility debt. Surface which customizations violate clean core principles, classify them by remediation path (released API, ABAP Cloud object, RAP business object, key-user extensibility, developer extensibility on BTP CAP/RAP, or retire), and recommend a prioritized remediation plan. Does not touch or read live systems.

## When to use

Use this skill when the user asks to:

- audit Z/Y custom ABAP programs, function modules, or classes for clean core compliance,
- assess customer modifications (`CMOD`/`ENH`/user exits/implicit enhancements/substitutions) against the clean core standard,
- identify which custom objects use deprecated or non-released SAP APIs,
- plan remediation of custom code toward released APIs, ABAP Cloud whitelisted objects, or SAP RAP/CAP extensibility patterns,
- understand the difference between key-user extensibility (in-app) and developer extensibility (side-by-side on BTP),
- evaluate the clean core compliance impact of an S/4HANA upgrade or migration to S/4HANA Cloud.

## When not to use

- When the user needs live system inspection of custom code — use `sap-live-readonly-landscape-discovery` first to enumerate objects, then return here for advisory review.
- When the request is about transport mechanics — use `sap-guarded-transport-import`.
- When the request is about BTP infrastructure provisioning rather than ABAP extensibility patterns.

## Does not touch live systems

This skill operates on code artifacts, architecture documents, upgrade reports (e.g., SAP Readiness Check, ABAP Test Cockpit results, custom code migration app output), or user-provided descriptions. It does not connect to any SAP system, run SE38/SE84 searches, read from BTP cockpit, or invoke ABAP Test Cockpit programmatically. All live enumeration is out of scope.

## Lean operating rules

- Classify first. Every custom object must be classified by clean core violation type before a remediation path is proposed.
- Use official SAP clean core taxonomy. The four extensibility pillars are: (1) in-app key-user, (2) in-app developer (BAdI/released API), (3) side-by-side developer (BTP CAP/RAP), (4) partner/ISV extensions.
- Do not recommend deprecated paths. Implicit enhancements, `CALL CUSTOMER FUNCTION`, and customer includes in standard SAP objects are deprecated extensibility patterns. Do not propose them as remediation targets.
- Separate upgrade risk from clean core debt. Objects that block upgrade (compatibility-level `NOT_RELEASED`) must be distinguished from objects that are technically functional but architecturally non-compliant.
- Released API = C1 contract. Only ABAP objects with release contract `C1` (use system-internally permitted) or `C2` (use in customer namespace permitted) are clean-core-compliant extensibility entry points.
- RAP is the preferred ABAP Cloud extensibility layer. For new transactional extensions on S/4HANA Cloud, ABAP RESTful Application Programming Model (RAP) is the strategic direction.
- CAP is supplementary for side-by-side. SAP Cloud Application Programming Model (CAP) applies for side-by-side extensions on BTP — not for in-system ABAP extensions.
- Evidence from official SAP sources takes precedence over memory or training data.
- Load only the reference needed for the component in scope.

## Evidence rules

Label all claims with one of:

- `documentation-based` — grounded in SAP Clean Core docs, ABAP Cloud docs, or S/4HANA extensibility guides
- `user-provided evidence` — code snippets, upgrade reports, or custom code lists provided by the user
- `context7-supplementary` — grounded in CAP/RAP framework docs fetched from Context7 (supplementary to official SAP docs)
- `inference` — derived reasoning not directly confirmed by official docs or user evidence

## Live-environment rules

**This skill does not touch live systems.** There is no credential, API call, RFC connection, or ABAP system access in this skill's execution path. Users must supply code artifacts, upgrade report output, ABAP Test Cockpit results, or written descriptions of custom objects for this skill to review.

## References

Load only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — classification taxonomy, remediation paths, output format.
- [Safety checklist](references/safety-checklist.md) — non-negotiables, common mistakes, when to push back.
- [Official sources](references/official-sources.md) — SAP Clean Core docs, ABAP Cloud, RAP, S/4HANA extensibility.
- [Context7 framework docs](references/context7-framework-docs.md) — CAP extensibility patterns (supplementary; use for BTP side-by-side guidance).

## Response minimum

Return, at minimum:

- **Problem classification**: clean core violation type(s) and affected object(s).
- **Evidence used**: documentation-based / user-provided / context7-supplementary / inference.
- **Risk level**: upgrade-blocking / clean-core-non-compliant / compliant.
- **Recommended action**: remediation path per object class (released API, ABAP Cloud RAP, key-user, side-by-side CAP, retire).
- **Refusal / escalation triggers**: if live object inspection is needed, escalate to `sap-live-readonly-landscape-discovery` first.
- **Business impact**: upgrade risk, cloud readiness, maintenance overhead.
- **Next verification step**: validate remediation candidates against current SAP API Business Hub release contracts.
