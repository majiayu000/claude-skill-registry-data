---
name: decision-log
category: strategy
description: >
  Captures a decision with context, alternatives considered, and rationale, then links
  it to the relevant project doc in the vault. Creates a searchable decision record.
  Use when the user says "decision log", "log this decision", "record this choice",
  "document why we chose", "decision record", "ADR", or has just made an important decision.
---

# Decision Log

Capture decisions so future-you knows why.

## Workflow

1. **Capture the decision** — Get from the user:
   - **What was decided** — the actual choice made
   - **Context** — what prompted this decision? What problem does it solve?
   - **Alternatives considered** — what other options were evaluated?
   - If the user doesn't provide alternatives, ask: "What other options did you consider?"

2. **Document rationale** — For the chosen option:
   - Why was this chosen over alternatives?
   - What trade-offs were accepted?
   - What constraints influenced the decision?

3. **Assess each alternative** — For each option considered:
   - Pros and cons
   - Why it was rejected
   - Under what conditions it might be reconsidered

4. **Identify consequences** — What follows from this decision:
   - Immediate next actions
   - Long-term implications
   - Reversibility: Is this a one-way door or two-way door?
   - Review trigger: When should this decision be revisited?

5. **Link to project** — Connect the decision to:
   - Relevant project docs in the vault (`[[Project Name]]`)
   - Related prior decisions
   - People involved in the decision

## Output Format

```markdown
---
type: decision
status: decided
date: [YYYY-MM-DD]
project: [[Project Name]]
decision-makers: [list]
reversibility: [one-way-door | two-way-door]
review-by: [YYYY-MM-DD or trigger condition]
tags: [decision, project-name, topic]
---

# Decision: [Short Title]

## Context

[What prompted this decision? What problem are we solving?]

## Decision

**We chose**: [the decision]

## Alternatives Considered

### Option A: [Name] (chosen)
- **Pros**: ...
- **Cons**: ...

### Option B: [Name] (rejected)
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

### Option C: [Name] (rejected)
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

## Rationale

[Why this option? What trade-offs were accepted?]

## Consequences

- **Immediate**: [next actions]
- **Long-term**: [implications]
- **Revisit when**: [trigger condition]

## Related
- [[Related Decision 1]]
- [[Project Doc]]
```

## Vault Integration

- Save to: `~/broomva-vault/decisions/decision-[short-title]-[YYYY-MM-DD].md`
- Backlink to the relevant project doc
- If a `decisions/` index exists, append the new entry

## Behavior

- Don't skip the alternatives — even "we considered nothing else" is worth recording
- Capture the emotional/political context if the user shares it (e.g., "leadership pushed for this")
- For one-way-door decisions, emphasize the review trigger
- Keep it factual — this is a record, not advocacy
