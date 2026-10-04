---
name: sr-spec
description: >
  Phase 2 of the SRS workflow. Reads projects/{slug}/brainstorm.md and writes
  a comprehensive spec.md. No word limit.
---

# sr-spec

Goal: turn the brainstorm output into a structured, comprehensive spec.
No word limit — every section must be fully written.

---

## Step 0 — Identify Project

Ask user for the project slug (or detect from context):

Ask the user: "Which project to write spec for? (slug name or path to brainstorm.md)"

Read `projects/{slug}/brainstorm.md`. If it doesn't exist, tell the user to run
`$sr-brainstorm` first.

---

## Step 1 — Write spec.md

Write `projects/{slug}/spec.md`. No word limit. Every sub-section fully written.

### §1 — Project Overview
- System name (confirmed in brainstorm)
- Problem statement (what problem does this solve?)
- Solution summary (what does the system do, for whom, how)
- Primary success metrics (how will we know it's working?)

### §2 — Actors
One full entry per confirmed actor:
- Name and role
- Technical proficiency (non-technical | basic | intermediate | expert)
- Domain knowledge level
- Frequency and channel of use (web | mobile | API | all)
- Accessibility needs (if any)
- Data access scope (read | write | admin)

### §3 — Features (IN Scope)
For each confirmed feature:
- Feature name + cluster
- Description in user's own words (verbatim from brainstorm)
- AI-expanded detail (what sub-capabilities does this imply?)
- Actors who use it
- Priority tier: Essential | Conditional | Optional

### §4 — OUT of Scope
Table: Feature | Reason excluded | Planned for version
Every item from brainstorm OUT scope list.

### §5 — Technical Constraints
- Tech stack: languages, frameworks, runtime
- Hosting / deployment model
- Existing systems to integrate (name, protocol, direction)
- Security standards (auth model, encryption requirements)
- Compliance: applicable regulations + specific obligations

### §6 — Business Rules
Numbered list. Each rule: precise, testable statement.
Example: "BR-01: A user cannot place an order if their account balance is below the order total."
Cover every rule surfaced in brainstorm Round 5.

### §7 — NFR Baselines
Table format:

| ID | Characteristic | Target | Status |
|----|---------------|--------|--------|
| NFR-01 | Response Time | < 500ms at p95 | Confirmed |
| NFR-02 | Availability | 99.9% uptime | Confirmed |
| NFR-03 | Data Retention | 7 years | [TBD: legal to confirm \| owner: PM \| resolve-by: Sprint 1] |

### §8 — Assumptions
Numbered list. Each assumption: what is assumed + what happens if the assumption is wrong.

### §9 — Open Items
Every [TBD] from the brainstorm open-items section, with:
- What is unknown
- Who needs to answer it
- Impact if unresolved

---

## Step 2 — Confirm Before Finishing

After writing, do a self-check:
- Every confirmed actor appears in at least one feature entry?
- Every confirmed feature has a priority tier?
- Every [TBD] from brainstorm.md appears in §9?
- Every business rule is numbered and testable?

Fix any gaps before outputting the handoff message.

---

## Step 3 — Handoff

Output:
```
Spec written: projects/{slug}/spec.md

Actors:         {count}
Features (IN):  {count}
OUT scope:      {count}
Business rules: {count}
NFR baselines:  {count confirmed} confirmed, {count TBD} [TBD]
Open items:     {count}

Next: $sr-plan → breaks this spec into per-section SRS plan files
```
