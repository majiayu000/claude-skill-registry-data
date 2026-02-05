---
name: prototype-planning
description: Define what to build at what fidelity to learn what you need without over-investing. Use before starting any prototype.
---

# Prototype Planning

## Overview
Define what to build, at what fidelity, to learn what you need to know without over-investing.

## When to Use
- Before starting any prototype
- When transitioning from Ideate to Prototype phase
- When deciding between low-fi and high-fi approaches
- When prototype scope is unclear

## How to Apply

### 1. Define Learning Goals
What questions must this prototype answer?

Examples:
- "Will users understand the core concept?"
- "Can users complete the task with this flow?"
- "Is the information architecture clear?"
- "Will this perform fast enough?"
- "Do users want this feature?"

### 2. Choose Appropriate Fidelity

Match fidelity to learning goals:

**Low Fidelity** (paper sketches, wireframes, clickable mockups)
- Test concepts and flows
- Validate information architecture
- Early user reactions
- Fast iteration

**Medium Fidelity** (interactive prototypes, basic functionality)
- Test specific interactions
- Validate workflows end-to-end
- More realistic user testing
- Some technical validation

**High Fidelity** (working code, realistic data, edge cases)
- Performance testing
- Technical feasibility
- Real-world usage patterns
- Pre-launch validation

**Rule**: Use the lowest fidelity that answers your questions.

### 3. Define Scope

**In scope**:
- What features/flows are included?
- What data/content is needed?
- What interactions must work?

**Out of scope**:
- What can be faked or simulated?
- What can wait for later iterations?
- What's not relevant to learning goals?

### 4. Plan Iteration

**Success criteria**: What would make this prototype worth pursuing?
**Failure criteria**: What would invalidate this idea?
**Iteration plan**: How will you test with users?
**Timeline**: How long to build and test?

### 5. Document the Plan

Create in `ideas/[idea-name]-001.md`:

```markdown
# Offline Capture - Prototype 001

**Fidelity**: Low (paper + clickable mockup)
**Timeline**: 3 days build, 1 week testing

## Learning Goals
1. Do users understand offline sync concept?
2. Is 3-field quick capture sufficient?
3. Will users trust data won't be lost?

## Scope
**In scope**:
- Quick capture form (3 fields)
- Offline indicator
- Sync status display

**Out of scope**:
- Full form (can fake)
- Conflict resolution (assume happy path)
- Settings/configuration

## Success Criteria
- 4/5 users complete capture without confusion
- Users express confidence data will sync
- No requests for missing critical fields

## Testing Plan
- 5 field techs
- Simulate offline scenario
- Task: Log 3 service calls
- Observe and interview
```

## Fidelity Decision Tree

```
Are you testing concept/value?
  Yes → Low fidelity
  No ↓

Are you testing usability/flow?
  Yes → Low to Medium fidelity
  No ↓

Are you testing technical feasibility?
  Yes → Medium to High fidelity
  No ↓

Are you testing performance/scale?
  Yes → High fidelity
```

## Tips
- Start lower fidelity than you think
- Focus on learning, not impressing
- Fake what you can (wizard of oz testing)
- One prototype, one primary learning goal
- Plan 2-3 iterations per idea
- Throwaway prototypes are okay
- Document what you learn, not just what you build
