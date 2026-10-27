---
description: Generate a client proposal from a project brief
argument-hint: "[project or client name]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Bash(date:*)
---

Turn a rough brief into a structured client proposal with scope, timeline, deliverables, and pricing.

## Steps

### Step 1: Gather the brief

If the user provided project details, use those. Otherwise, ask for:
- Client / project name
- What do they need? (the problem)
- What's the desired outcome?
- Any constraints (budget range, timeline, technical requirements)?

### Step 2: Scope definition

Break the project into phases and deliverables:

For each phase:
- **Phase name** and duration
- **Deliverables** — specific, tangible outputs
- **Dependencies** — what's needed to start this phase
- **Assumptions** — what you're assuming to be true

Flag anything that could cause scope creep. Be explicit about what's included and what isn't.

### Step 3: Timeline

Create a realistic timeline:
- Map phases to calendar weeks
- Identify milestones (decision points, reviews, handoffs)
- Build in buffer for feedback rounds
- Note any hard deadlines or dependencies on the client

### Step 4: Pricing

Structure the pricing:
- **Option A (Recommended):** Full scope as described
- **Option B:** Reduced scope (MVP / Phase 1 only)
- **Optional add-ons:** Additional services that complement the core work

For each option, list: total price, payment schedule, what's included, what's not.

### Step 5: Terms

Standard terms to include:
- Payment schedule and terms
- Revision policy (how many rounds of revisions)
- Ownership / IP transfer
- Timeline for acceptance / sign-off
- Cancellation terms

### Step 6: Write the proposal

Save to `proposals/[client-name]-proposal.md`:

```markdown
# Proposal — [Project Name]

**Prepared for:** [Client]
**Prepared by:** [Your name/company]
**Date:** [date]

---

## Executive Summary

[2-3 sentences: the problem, your solution, expected outcome]

## Understanding

[Restate the client's problem in your words — proves you listened]

## Approach

### Phase 1: [Name] — [duration]
**Deliverables:**
- [specific output]
- [specific output]

### Phase 2: [Name] — [duration]
**Deliverables:**
- [specific output]
- [specific output]

[Continue for each phase]

## Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| [Phase 1] | [weeks] | [key deliverable] |

## Investment

### Option A: Full Scope (Recommended)
[price, payment schedule, what's included]

### Option B: Phase 1 Only
[price, payment schedule, what's included]

### Optional Add-ons
- [add-on]: [price]

## Terms

- [Payment terms]
- [Revision policy]
- [Ownership]

## Next Steps

1. Review this proposal
2. [Specific action to proceed]
3. Kick-off call to align on details

---
Valid for 30 days from date above.
```

Output a summary and tell the user where the file is saved.
