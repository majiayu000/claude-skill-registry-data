---
name: decision-recorder
description: "Records architectural decisions with context, alternatives considered, and rationale when significant technical choices are made. Triggers when choosing between libraries, frameworks, patterns, approaches, or making trade-off decisions."
---

# Decision Recorder

## Goal

Create clear, permanent records of WHY technical choices were made, so that future agents (or the orchestrator returning months later) can understand the reasoning without guessing.

## Instructions

### Step 1: Identify the Decision

A decision record is warranted when:
- Choosing between 2+ libraries or tools
- Selecting an architectural pattern
- Making a trade-off (speed vs. safety, simple vs. flexible, etc.)
- Changing an approach that was previously established
- The orchestrator asks "why did you do it this way?"

### Step 2: Determine the Next ADR Number

Check `.agent/knowledge/decisions/` for existing ADR files. The new file should be numbered sequentially: `ADR-001`, `ADR-002`, etc.

### Step 3: Write the ADR

Create a new file at `.agent/knowledge/decisions/ADR-NNN-short-title.md` using the template in `resources/adr-template.md`.

Key principles:
- **Context section**: Write as if explaining to someone who has never seen this project. No assumed knowledge.
- **Alternatives table**: Be honest about pros AND cons of each option, including the chosen one.
- **Consequences section**: State both positive outcomes AND trade-offs/risks.

### Step 4: Inform the Orchestrator

Summarize the decision in plain English:
- "I chose [X] over [Y] because [reason in one sentence]."
- "The main trade-off is [what we give up]. I recorded this as ADR-NNN."

### Step 5: Cross-Reference

If this decision relates to or supersedes a previous ADR:
- Add a reference in the "Related Decisions" section of the new ADR
- Update the old ADR's status to "superseded by ADR-NNN" if applicable

## Constraints

- Never delete an ADR — if a decision changes, create a new ADR and mark the old one as superseded
- ADR numbers are never reused
- Write Context and Consequences sections in plain English — the orchestrator must understand them
- Include at least 2 alternatives (even if one is "do nothing" or "keep current approach")
