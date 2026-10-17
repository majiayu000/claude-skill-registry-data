---
name: tech-debt
description: >
  Document and prioritize technical debt. Use when the user says "tech debt",
  "legacy code", "this code is a mess", "refactoring plan", "we need to clean this up",
  "paying down debt", "this is hard to change", "how do we fix this codebase",
  or has code that's difficult to understand or modify
  - even if they don't explicitly say "technical debt".
---

## Overview

Based on **"Working Effectively with Legacy Code"** by Michael Feathers. Feathers' definition: legacy code is code without tests. His central technique: find the "seams" - places where you can insert test coverage without changing the code under test. Once a seam has test coverage, you can safely refactor. The discipline: never refactor without a safety net. Never add features to untested code without first covering it.

## Workflow

### Step 1: Define the debt
Before prioritizing, describe the debt specifically:

```
Debt item: [name]
Location: [file:line or module]
What it is: [one sentence description]
Why it's a problem: [what it makes harder]
Symptom: [what developers experience because of it]
```

Vague debt ("the codebase is messy") can't be prioritized. Specific debt can.

### Step 2: Classify the debt type
| Type | Description | Urgency |
|------|-------------|---------|
| **Reckless/Deliberate** | Shortcuts taken knowingly ("we'll fix it later") | High |
| **Reckless/Inadvertent** | Mistakes made without knowing better | High |
| **Prudent/Deliberate** | Conscious tradeoff: ship now, fix later | Medium |
| **Prudent/Inadvertent** | Learned better approach after the fact | Low |

### Step 3: Find the seams (Feathers)
A seam is a place where you can change behavior without editing existing code - typically a function call boundary or an interface.

For each debt item:
- Where is the seam that would let you add tests without changing production code?
- What would you need to mock or stub to isolate this code?
- What's the minimum test coverage needed before safe refactoring?

### Step 4: Estimate the cost of the debt
| Dimension | Questions |
|-----------|-----------|
| **Cost of carry** | How much does this slow development each sprint? |
| **Cost of fix** | How many days to resolve? |
| **Blast radius** | How many systems/teams are affected? |
| **Risk if ignored** | What breaks if this is never fixed? |

### Step 5: Prioritize the backlog
Prioritize debt that:
- Has high cost of carry (slows the team every sprint)
- Sits in high-change areas (touched frequently)
- Blocks a planned feature

Deprioritize debt in stable areas that are rarely touched.

### Step 6: Write the debt ticket
```
Title: [specific debt item]
Location: [file/module]
Type: [reckless/prudent x deliberate/inadvertent]
Impact: [what this costs the team per sprint]
Fix plan:
  1. Add seam tests: [specific tests to write first]
  2. Refactor: [what to change once tests exist]
  3. Verify: [how to confirm the refactor is safe]
Effort estimate: [days]
Priority: [P1/P2/P3]
```

## Anti-Patterns

**1. Refactoring without tests**
Bad: "Let me clean this up" without adding test coverage first.
Good: Find the seam. Write tests. Then refactor. Tests prove you didn't break behavior.

**2. Big bang rewrites**
Bad: "We'll rewrite the whole module from scratch."
Good: Feathers: big rewrites fail. Incrementally improve with seam-by-seam coverage. Ship working code at every step.

**3. Paying debt in high-risk sprints**
Bad: Refactoring core payment code the week before a major release.
Good: Pay debt in low-risk windows. Prioritize timing as much as priority.

**4. Debt without business context**
Bad: "This code is bad, we need to fix it." (to a PM or stakeholder)
Good: "This debt costs us 2 days per sprint. Fixing it is a 5-day investment that pays back in 3 sprints."

## Quality Checklist

- [ ] Debt is described specifically (file, module, or function - not "the codebase")
- [ ] Debt type classified
- [ ] Seam identified for each item (where to add tests safely)
- [ ] Cost of carry estimated in developer-days per sprint
- [ ] Cost to fix estimated
- [ ] Highest priority items are in high-change areas
- [ ] Debt ticket includes fix plan with seam tests as first step
