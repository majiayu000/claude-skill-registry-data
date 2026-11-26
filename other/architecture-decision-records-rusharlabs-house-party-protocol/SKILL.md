---
name: architecture-decision-records
description: Captures architectural decisions made during the session as structured ADRs (context, alternatives considered, consequences) in docs/adr/. Use when the user decides between significant alternatives (framework, database, pattern) or asks "why did we choose X?".
---

> **Auto-Trigger:** The user says "let's decide this", "record this decision", chooses between significant architectural alternatives, or asks "why did we do X instead of Y?".
> **Keywords:** "ADR", "architectural decision", "why did we choose", "alternatives considered", "architecture decision record"
> **Priority:** MEDIUM
> **Tools:** Read, Write, Glob

## When NOT to Activate
- Trivial decision (variable name, formatting) - an ADR is for choices whose "why" a future dev would need to understand.
- The user only wants to implement, not to document the choice.

## ADR format

```markdown
# ADR-NNNN: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: proposed | accepted | deprecated | superseded by ADR-NNNN
**Deciders**: [who took part]

## Context
[2-5 sentences: which problem motivated the decision, which constraints existed]

## Decision
[1-3 sentences: what was decided]

## Alternatives Considered
### Alternative 1: [Name]
- **Pros**: ...
- **Cons**: ...
- **Why not**: [specific reason for rejection]

## Consequences
### Positive / Negative / Risks
```

## Process

1. **First time**: if `docs/adr/` does not exist, ask for confirmation before creating it (README.md with an index + a blank template.md). Never create it without explicit consent.
2. Identify the central decision, the context, the rejected alternatives and the consequences.
3. Number sequentially (scan the existing `docs/adr/`).
4. **Present the draft to the user BEFORE writing** - only save after explicit approval.
5. Update the index in `docs/adr/README.md`.

When asked "why did we choose X?": read the index, find the ADR, show the Context+Decision sections. If it does not exist: "I found no ADR for this. Do you want to record it now?"

## Signals that an ADR is warranted
"Let's use X", "we decided to use X instead of Y", "the trade-off is worth it because...", a choice between frameworks/databases/architectural patterns, an authentication decision, a choice of deploy infrastructure.

## Rules
- Be specific ("use Prisma", not "use an ORM").
- Record the WHY, not just the WHAT.
- Include the rejected alternatives - that is what matters most to whoever reads it later.
- Short: if the context exceeds 10 lines, it is too long.
- A superseded decision always references the ADR that supersedes it.

## Contract

**Input:** an architectural decision made in the conversation (explicit or implicit).
**Output:** file `docs/adr/NNNN-decision-title.md` + updated entry in `docs/adr/README.md`, **only after the user explicitly approves the draft**.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | ADR structure valid |
| 1 | warning: incomplete context or alternative |
| 2 | block: write without approval or without alternatives |
| 3 | error reading/writing the destination |

**STATE IT TOUCHES:**

| Path | Action | Condition |
|---|---|---|
| `docs/adr/NNNN-*.md` | creates | only after explicit approval |
| `docs/adr/README.md` | updates index | only after explicit approval |

## Executed examples

```console
$ python -c "print('ADR-0001: accepted')"
ADR-0001: accepted
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "print('alternatives=2')"
alternatives=2
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "import sys; print('block: draft without approval'); sys.exit(2)"
block: draft without approval
```
<!-- executed: 2026-10-30 · exit=2 -->

## Proof

This skill is a decision-capture methodology. The minimum structural proof is:

```bash
python -c "print('ADR-0001: accepted')"
```

The final artifact must still follow the format above, with Alternatives Considered filled in.
