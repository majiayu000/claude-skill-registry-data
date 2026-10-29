---
name: requirements-validator
description: "Use when you need to review, validate, and improve requirements documents, acceptance criteria, or implementation briefs."
argument-hint: [requirements.md]
allowed-tools: Read, Glob, Grep
---

## Purpose

Review a requirements document or implementation brief and identify gaps, ambiguity, inconsistencies, or missing acceptance criteria before work begins.

## Inputs

- A requirements document, PRD, ticket, spec, or pasted text.
- Optional context such as business goals, constraints, or technical assumptions.

If `$ARGUMENTS` is provided and resolves to an existing file path, read that file as the
requirements document. If `$ARGUMENTS` is plain text rather than a path, treat it as the
pasted requirements content directly. If `$ARGUMENTS` is empty, ask via `AskUserQuestion`
how to provide it: **Paste the requirements text** / **Provide a file path**. Then request
the actual content per their choice as free text -- the requirements themselves have no
finite menu.

## Steps

1. Read the requirements and identify the intended outcome, scope, and stakeholders.
2. Check for clarity and completeness:
   - Missing functional or non-functional requirements
   - Ambiguous wording or undefined terms
   - Conflicting requirements or contradictions
   - Missing edge cases, dependencies, or constraints
   - Unstated assumptions — anything the document treats as given or obvious without saying so explicitly
3. Evaluate whether each requirement is:
   - Specific and measurable
   - Testable and observable
   - Feasible within the stated constraints
   - Traceable to a user need or business goal
4. Suggest improvements to make the requirements stronger and easier to implement.
5. Draft or refine acceptance criteria so each requirement can be verified.
6. Highlight risks, open questions, and items that require stakeholder confirmation.
7. Present a concise validation summary with priorities and recommended fixes.

## Output

Present the review in chat using this structure:

```
## Validation Report: [document name or topic]

### Summary
[1-2 sentence overall assessment of readiness]

### Issues Found
| # | Requirement/Section | Issue Type | Description | Severity |
|---|---|---|---|---|
| 1 | [section] | Ambiguous/Missing/Conflicting/Untestable/Assumption | [detail] | High/Medium/Low |

### Unstated Assumptions
- [assumption the document relies on without stating] — [why it matters / what could go wrong if it's wrong]

### Suggested Acceptance Criteria
- [requirement]: [refined, testable acceptance criterion]

### Open Questions for Stakeholders
- [question]

### Recommendation
[Ready to proceed / Needs revision before proceeding] — [1-2 sentence justification]
```

## Guardrails

- Do not invent requirements that are not supported by the source material.
- Do not rewrite the entire document unless it is necessary for clarity.
- Preserve the original intent while improving structure and testability.
- Flag uncertainty instead of guessing.
- Prefer concrete, verifiable language over vague statements.

## Notes

- Clickable-question convention: the Inputs section's intake-method choice uses `AskUserQuestion`. The requirements content itself stays free text -- genuine data, not a finite menu. No other user-facing questions exist; this skill is report-only.
