---
name: ba-report
description: Use when approved BA/project truth needs to be communicated as a professional, plain-language FRD report that mixed business and technical readers can understand without changing the underlying requirements.
argument-hint: "[format, audience, or report focus]"
---

# BA Report

Create a **professional ELI5 FRD report** from approved project truth. The report is a communication artifact, not a new source of truth.

**Core rule: explain clearly; do not invent.**

## Entry

Preferred input is an approved Phase 4 Final FRD plus the current valid Project Brain. If the Final FRD is not approved, explain the gap and recommend `/ba-spec` first. If the user explicitly wants a draft report anyway, label it clearly as **DRAFT / NOT FINAL** and use only current valid evidence.

Read only what is needed from:

- `.ba/PROJECT.md`,
- the latest valid Phase 4 snapshot/final FRD,
- referenced `REQUIREMENTS.md`, `DECISIONS.md`, and `RESEARCH.md`,
- approved Phase 1–3 snapshots only when needed to recover rationale/context.

Do **not** create, change, confirm, supersede, or reinterpret requirements/decisions from this skill. If the report exposes missing or contradictory project truth, route the issue back to `/ba-requirements`, `/ba-design`, or `/ba-spec` instead of repairing it here.

## Pending change boundary

By default, report only **approved truth**. A **pending change** may be mentioned as a clearly separated pending item when the user explicitly wants that context, but its candidate meaning must not be merged into approved report statements. Pending truth is context, not approval.

## Fixed report pattern

Before drafting, read [references/report-pattern.md](references/report-pattern.md). Follow its section order exactly. Do not reorder or omit sections. When a section is not applicable, keep the heading and state that it is not applicable in the current approved scope.

The fixed opening is:

1. **Background**
2. **Goal**
3. **What We Will Do**
4. **Scope & Boundaries**
5. **Current → Future**
6. **Project / System Logic**
7. **Functional Requirements**

Then continue with the remaining fixed specification sections from the pattern reference.


## Fixed HTML shell

For HTML output, start from [assets/report-template.html](assets/report-template.html). Copy and fill its semantic slots and fixed section containers. **Do not redesign** the visual system, typography, section order, component grammar, or print behavior unless the user explicitly asks for a different presentation. Add content/rows/items inside the established components instead.

The template is the canonical visual definition for HTML reports. Keep output self-contained and offline-readable.

## Writing model: Explain → Show → Specify

For every material concept, use three layers when useful:

1. **Explain** — plain language first; answer what this means and why it matters.
2. **Show** — example, before/after, flow, scenario, or table that makes the logic visible.
3. **Specify** — exact rule, requirement IDs, decision IDs, acceptance criteria, constraints, and technical references.

Do not make the report childish or vague. ELI5 means reducing decoding effort while preserving the real distinctions and logic.

## Functional requirements presentation

Group requirements by **business capability / user goal**, not by API, service, database table, or implementation component.

Each functional area uses the same internal pattern:

- Purpose
- When It Happens
- How It Works
- Business Rules
- Example
- Exceptions
- Expected Result
- Requirement / Decision / Acceptance references

Keep `REQ-*`, `DEC-*`, and other canonical IDs visible for traceability without forcing non-technical readers to understand them first.

## Output

Default output is a **self-contained HTML** report that is professional, print-friendly, and readable without external assets. Read [references/html-presentation.md](references/html-presentation.md) before generating HTML.

Default path:

```text
docs/BA-FRD-Report.html
```

If the user explicitly requests Markdown, create:

```text
docs/BA-FRD-Report.md
```

If the target project has an established documentation location or naming convention, follow it instead. Never overwrite an existing report silently; preserve it or create a revisioned/new file unless the user explicitly requests replacement.

## Report status and provenance

The report must display:

- project name,
- report pattern: `BA-ELI5-FRD v1.0`,
- report status: FINAL or DRAFT,
- source baseline / Final FRD reference,
- generation date only when the environment provides a trustworthy current date,
- important unresolved items if any.

The report may summarize and visualize approved truth, but canonical records remain in `.ba/`.

## Quality gate

Before presenting the report, verify:

- Background → Goal → What We Will Do → Scope flow is coherent,
- Current → Future accurately reflects approved changes,
- system logic does not add unapproved behavior,
- functional areas cover material confirmed requirements,
- business rules and exceptions are not hidden,
- technical jargon is explained where first needed,
- every material technical claim can be traced to approved truth,
- open items/assumptions remain visible,
- the fixed section order is unchanged,
- HTML is self-contained and print-friendly when HTML is generated.

Then present the report path and a short note about its source baseline/status. Do not mutate Project Brain merely because a report was generated.
