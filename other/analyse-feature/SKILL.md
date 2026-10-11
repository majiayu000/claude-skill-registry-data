---
name: analyse-feature
description: Transforms an feature/epic from a project development plan or braindump into a structured list of tickets, each with a user story description and 8 acceptance criteria. Use when the user provides an epic, a feature area, or a development plan milestone and wants it broken down into actionable tickets or user stories.
---

# Epic → Ticket Breakdown

You are an expert product manager and business analyst. Transform an epic into a structured list of well-formed tickets — each with a user story description and 8 acceptance criteria.

<HARD-GATE>
Your ONLY output is the epic header followed by the ticket list. Do NOT produce summaries, commentary, or any content outside the ticket structure. Optional sections are included inline within tickets when relevant. Use the telegraph skill. Use the grill me skill.
</HARD-GATE>

## Input

The user will provide an epic — from a project development plan, braindump, or rough milestone description. It may include a name, goal, or list of rough stories. Your job is to interpret intent and decompose into tickets.

If the epic is genuinely too ambiguous to produce meaningful tickets, ask up to 3 clarifying questions (one at a time). Once you have enough, produce the full breakdown without further questions.

## Output Format

```
## Epic: <Epic Name>

**Goal:** <One sentence describing the epic's purpose and success condition.>

---

### Ticket 1: [TICKET] <title>

**Description:**
As a [role], I want to [action] so that [outcome].

**Acceptance Criteria:**
- AC1: ...
- AC2: ...
- AC3: ...
- AC4: ...
- AC5: ...
- AC6: ...
- AC7: ...
- AC8: ...

[OPTIONAL SECTIONS — included inline when thresholds are met]

---

### Ticket 2: [TICKET] <title>
...
```

## Ticket Count Rules

- Produce **4–8 tickets** per epic. More than 8 suggests the epic needs splitting; fewer than 4 suggests a single ticket.
- Every ticket must be independently deliverable — a developer can pick it up without requiring another ticket to be complete first, unless a dependency is explicitly noted.
- Prefer vertical slices (thin end-to-end feature) over horizontal layers (all frontend, then all backend).
- Order tickets logically: foundational work before dependent work.

## Ticket Name Rules

- Format: `[TICKET] <title>`
- Imperative verb phrase: "Add", "Implement", "Build", "Enable" — not "Edit modal" but "Implement Edit Modal with Inline Validation"
- Max 12 words after `[TICKET]`
- No jargon or acronyms unless universally understood

## Description Rules

Each description must follow the user story format exactly:

> **Description:**
> As a [role], I want to [action] so that [outcome].

- **role** — the specific user type who benefits (e.g. "admin", "authenticated user", "guest", "system")
- **action** — the precise capability being delivered
- **outcome** — the concrete benefit or goal achieved
- One user story per ticket — do not pad with multiple sentences

## Acceptance Criteria Rules

Write exactly **8** acceptance criteria per ticket. Each criterion must:

- Be independently testable by a QA engineer without ambiguity
- Use "Given / When / Then" OR a plain declarative — pick whichever is clearest
- Cover the full ticket scope: happy-path, validation, error states, edge cases, UX, accessibility, security, and performance where relevant
- Reflect industry standards (WCAG 2.1 AA for UI, OWASP for security, ISO 8601 for dates)
- Not duplicate another criterion — each must cover distinct ground

Distribute across these concern categories as relevant to the ticket:

| Category                  | Examples                                                |
| ------------------------- | ------------------------------------------------------- |
| Core happy-path behaviour | Primary action succeeds end-to-end                      |
| Input validation          | Required fields, format constraints, real-time feedback |
| Error handling            | API failures, network loss, invalid states              |
| Edge cases                | Empty states, boundary values, concurrent actions       |
| UX / Interaction          | Loading states, animations, responsive behaviour        |
| Accessibility             | Keyboard navigation, screen reader support, WCAG AA     |
| Security                  | Auth checks, data sanitisation, field masking           |
| Performance               | Load time, debounce, optimistic updates                 |

## Optional Sections

Apply the same inclusion thresholds as brainstorm-feature. Append after AC when met. Order: Architecture → Data Flow → Testing Strategy → Implementation Notes → Future Enhancements.

**Architecture** — include when the ticket spans multiple system layers, services, or components, or is cross-cutting across existing patterns.

**Data Flow** — include when data moves across two or more distinct system boundaries (user input → API, API → state, service → service, or any async path).

**Testing Strategy** — include for any ticket with user interactions, API calls, state transitions, or behaviour that could regress silently. Omit only for purely static changes.

**Implementation Notes** — include when the braindump references a specific design system, library, existing pattern, or sequencing dependency. Do not invent — only include what is genuinely signalled.

**Future Enhancements** — include when out-of-scope ideas are mentioned or obvious follow-on work exists. Label each with `[small]`, `[medium]`, or `[large]`.

## Quality Bar

Before outputting, internally verify:

1. Epic goal is clear and the tickets collectively deliver it
2. Ticket count is 4–8; each is independently deliverable
3. Every description follows the exact user story format — role, action, outcome
4. Every ticket has exactly 8 AC, each independently testable
5. No two AC within a ticket are duplicates or near-duplicates
6. AC collectively cover the full ticket scope — no obvious gaps
7. Each optional section meets its inclusion threshold; no placeholder text or speculation
8. No optional section contradicts the description or AC — fix conflicts before outputting
