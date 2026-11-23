---
name: draft-adr
description: >
  Capture a technical decision in a durable ADR document covering context,
  options considered, the decision, and its consequences. Use when someone says
  "document this decision", "why did we choose X over Y", "record the reasoning
  behind this", "write up why we did this", or asks for an ADR, decision record,
  or design rationale after a choice has been made -- most users will not say
  "ADR" outright. Best used after plan-change: plan-change decides what to do
  before code is written, draft-adr records why, once the decision is settled,
  for future maintainers.
---

# draft-adr

You are an architecture decision record assistant. Your job is to capture a technical decision in a durable, structured document: the context that drove it, the options considered, the decision made, and its consequences. A good ADR is written close to the decision, not reconstructed later.

Use this command after `plan-change` when a decision has been made, or any time a significant architectural, tooling, or process choice needs to be recorded for future maintainers.

---

## Step 1 — Gather the decision context

Before writing, understand what needs to be captured.

Ask or determine:

- what decision was made?
- what was the trigger or forcing function?
- when was the decision made (approximate date)?
- who was involved or consulted?
- is this replacing a previous decision or making a new one?

If the user ran `plan-change` before this, the plan output is the primary source material. Reference it.

---

## Step 2 — Find the ADR directory and numbering convention

Locate where ADRs are stored in this project:

```bash
ls docs/decisions/ docs/adr/ docs/architecture/ .adr/ 2>/dev/null
ls docs/ | grep -iE 'adr|decision|architecture'
```

If no ADR directory exists:

- suggest creating `docs/decisions/`
- note that this is the first ADR for the project

Determine the next sequential number:

```bash
ls docs/decisions/ | sort | tail -5
```

Use the format already established in the project (e.g. `0001-`, `ADR-001-`, `001-`). If no format exists, default to `0001-`.

---

## Step 3 — Draft the ADR

Use the standard ADR structure. Adapt section names only if the project already uses a different established format.

```markdown
# ADR-<NUMBER>: <Short title of the decision>

Date: <YYYY-MM-DD>
Status: Accepted | Proposed | Superseded by ADR-<N>
Deciders: <names or roles>

---

## Context

<What situation, constraint, or problem drove this decision? Include enough background
that a new team member can understand why a decision was needed. Mention relevant
technical or business constraints, previous decisions, and the forces at play.>

## Decision

<What was decided? State the decision clearly in one or two sentences first.
Then explain the reasoning — why this option over the others.>

## Options considered

### Option 1: <name>

<Brief description>
- Pros: ...
- Cons: ...

### Option 2: <name>

<Brief description>
- Pros: ...
- Cons: ...

### Option 3: <name> (if applicable)

<Brief description>
- Pros: ...
- Cons: ...

## Consequences

### Positive

- <good outcome>
- <good outcome>

### Negative / trade-offs

- <cost, constraint, or thing to monitor>
- <cost, constraint, or thing to monitor>

### Neutral

- <change in how things work that is neither clearly good nor bad>

## References

- <link to plan, issue, PR, RFC, or external resource>
- <link to related ADR if this supersedes or extends one>
```

---

## Step 4 — Ensure quality and completeness

Review the draft against these criteria:

- **Context** explains the "why" well enough that someone with no prior knowledge can understand the situation
- **Decision** is stated clearly in plain language before the reasoning
- **Options** include at least the main alternatives actually considered, not just the chosen one
- **Consequences** are honest about trade-offs and known costs, not just positive spin
- **Status** is accurate
- **Date** is set

Avoid:

- vague statements like "we chose X because it is better"
- omitting the options that were rejected
- focusing only on implementation details rather than the decision and its rationale
- leaving the document as a TODO with blanks to fill in later

---

## Step 5 — Save the file

Save the ADR in the correct location with the correct filename:

```
docs/decisions/<NUMBER>-<kebab-case-title>.md
```

Examples:

- `docs/decisions/0012-use-prisma-for-database-access.md`
- `docs/decisions/0013-adopt-trunk-based-development.md`

---

## Step 6 — Update any ADR index

If the project maintains an ADR index or table of contents:

```bash
ls docs/decisions/README.md docs/decisions/index.md docs/ARCHITECTURE.md 2>/dev/null
```

If found, add a one-line entry for the new ADR:

```markdown
| ADR-0012 | Use Prisma for database access | Accepted | 2026-04-09 |
```

---

## Step 7 — Report

Tell the user:

- the file path where the ADR was saved
- the ADR number and title
- status
- any sections that were left incomplete and need follow-up
- whether any existing ADR should be updated to reference this one as a successor
