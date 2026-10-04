---
name: generate-adr
description: Create, update, review, reject, deprecate, or supersede source-backed Architecture Decision Records (ADRs), compare viable options, and connect decisions to use cases, ADDs, C4 views, risks, compliance evidence, and implementation. Use for any significant architecture choice or ADR reference; use the separate conformance-review skill when comparing code with accepted decisions.
---

# Generate ADR

## Workflow

1. Read `AGENTS.md`, existing decisions, linked use cases/ADDs/C4 views, supplied evidence, and relevant code.
2. Determine whether to create, update, review, reject, deprecate, or supersede an ADR.
3. For a new record, select the next unused `ADR-NNN` under `architecture/decisions/` and copy [assets/adr-template.md](assets/adr-template.md).
4. Apply [references/adr-quality.md](references/adr-quality.md). Compare viable options using the same decision drivers; do not invent weak alternatives.
5. Record the decision, positive and negative consequences, risks, compliance effects, follow-ups, and reciprocal artifact links.
6. Use `Proposed` until an authoritative decision source supports another state.
7. Treat accepted ADR content as immutable history. Create a new ADR to change the decision and update reciprocal supersession links.
8. Save as `architecture/decisions/ADR-NNN-<slug>.md` unless an established layout exists.

## Rules

- Keep one primary, independently changeable decision per ADR.
- Phrase the title as the decision outcome.
- Never claim approval without evidence.
- Use `To classify` rather than inferring personal/health-data or AI-risk classification.
- Exclude personal/health records, credentials, secrets, connection strings, and sensitive endpoints.
- Update affected target-state C4/ADD artifacts after acceptance; proposed decisions may be shown only as proposals.
- When asked to review code, use `$review-architecture-conformance` and report deviations without rewriting accepted history.

## Output

Return path, lifecycle action/status, selected option, unresolved questions, evidence/approval gaps, affected artifacts, and required follow-ups.
