---
name: generate-add
description: Create, update, and review a source-backed Architecture Design Document (ADD) from reviewed use cases, applicable Business Decision Records, repository evidence, constraints, quality attributes, C4 views, and ADRs. Use when a change needs an overall technical design, an ADD reference must be revised, or implementation readiness must be assessed without writing code.
---

# Generate ADD

## Workflow

1. Read `AGENTS.md`, the project profile, reviewed use cases, applicable BDRs, existing architecture, relevant code, deployment sources, diagrams, and decisions.
2. Resolve the next `ADD-NNN` or the referenced ADD. Never reuse or renumber identifiers.
3. Copy [assets/add-template.md](assets/add-template.md) and apply [references/add-quality.md](references/add-quality.md).
4. Define scope, drivers, constraints, system context, responsibilities, data flows, interfaces, deployment, operations, risks, and migration/rollback.
5. Link C4 views rather than embedding several abstraction levels in one diagram. Request `$generate-c4` only for views that answer a concrete stakeholder question.
6. Identify independently changeable choices as ADR candidates. Link proposed ADRs; treat only accepted ADRs as constraints.
7. Run the privacy, security, clinical/legal safety, and human-oversight assessment. Stop on an unresolved compliance conflict.
8. Save under `architecture/design/ADD-NNN-<slug>.md` unless an established layout exists.

## Rules

- Do not invent owners, technologies, protocols, service levels, classifications, approvals, or data flows.
- Distinguish current, transition, target, and conceptual states.
- Include failure modes and operational ownership, not only the happy path.
- Keep real personal/health data, credentials, secrets, and sensitive endpoints out of the document.
- Keep status `Draft` or `In Review` until authoritative approval is cited.

## Completion

Report the document path, linked use cases, required C4 views, ADR candidates, compliance blockers, open questions, and implementation-readiness result.
