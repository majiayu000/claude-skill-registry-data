---
name: generate-bdr
description: Create, update, and review source-backed Business Decision Records (BDRs) for material product, investment, scope, ownership, policy, sourcing, operating-model, or risk-acceptance choices. Use when a business choice must authorize or constrain use cases and architecture, or when a BDR reference such as BDR-001 is supplied.
---

# Generate Business Decision Record

## Workflow

1. Read `AGENTS.md`, `architecture/toolkit-profile.yaml` when present, the idea and related use cases, existing BDRs, stakeholder evidence, and relevant business documentation.
2. Decide whether a BDR is required. Use it for a material business choice; do not create one merely to repeat requirements or technical design. Record a concise skip reason when no such choice exists.
3. Resolve the next unused `BDR-NNN` or the referenced record. Never reuse or renumber an identifier.
4. Copy [assets/bdr-template.md](assets/bdr-template.md), replace every placeholder, and remove irrelevant optional sections.
5. Separate current state, target state, transition, confirmed facts, proposals, assumptions, and open questions.
6. Compare viable options against the same decision drivers. Apply [references/bdr-quality.md](references/bdr-quality.md); do not invent weak alternatives.
7. Keep status `Proposed` until authoritative decision evidence exists. Never infer an approver or acceptance.
8. Save under `architecture/business-decisions/BDR-NNN-<slug>.md` unless the project profile or repository establishes another path.
9. Link the source idea/evidence and downstream use cases, ADDs, ADRs, C4 views, and tasks reciprocally when those artifacts exist.

## Rules

- Keep one primary, independently changeable business decision per BDR.
- Define measurable outcomes and review conditions, including when the decision should be revisited.
- Apply applicable privacy, AI, security, accessibility, safety, and sector governance without guessing applicability or classification.
- Record human decisions and automation boundaries for material outcomes.
- Do not invent cost, benefit, owner, deadline, approval, classification, or policy values.
- Exclude personal records, credentials, secrets, and sensitive operational details.

## Output

Return path, status, selected option or `Not yet decided`, affected use cases, constraints handed to architecture, assumptions, governance result, approval gaps, and recommended next step.
