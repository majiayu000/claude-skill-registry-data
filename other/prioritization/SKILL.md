---
name: prioritization
description: >
  Prioritize a feature backlog or list of ideas. Use when the user says "help me prioritize",
  "prioritize this backlog", "RICE score these", "MoSCoW", "opportunity solution tree",
  "what should we build first", "rank these features", or has a list of items and needs
  to decide order - even if they don't explicitly say "prioritization".
---

## Overview

Based on **Continuous Discovery Habits** by Teresa Torres + RICE scoring. Torres's key insight: teams prioritize solutions when they should be prioritizing opportunities (unmet user needs). Map opportunities first, then generate solutions. Use RICE to score which opportunity is worth pursuing.

## Workflow

### Step 1: Separate opportunities from solutions
Before scoring anything, sort the backlog into:
- **Opportunities** - unmet user needs, pain points, desires ("users can't track their progress")
- **Solutions** - specific things to build ("add a dashboard")

Prioritize at the opportunity level. For each opportunity, generate 2-3 possible solutions. This prevents locking into one solution prematurely.

### Step 2: Build the Opportunity Solution Tree (optional, for complex backlogs)
```
Outcome (what business result do we want?)
  └── Opportunity 1 (unmet user need)
        └── Solution A
        └── Solution B
  └── Opportunity 2
        └── Solution C
```

### Step 3: RICE Score each opportunity
| Opportunity | Reach | Impact | Confidence | Effort | RICE |
|-------------|-------|--------|------------|--------|------|

- **Reach** - Users affected per period (number)
- **Impact** - Effect per user: 0.25 / 0.5 / 1 / 2 / 3
- **Confidence** - How sure are you: 100% / 80% / 50%
- **Effort** - Person-weeks (number)
- **Formula:** `(Reach x Impact x Confidence) / Effort`

### Step 4: Apply MoSCoW for stakeholder alignment
Use RICE scores to inform MoSCoW bucketing:
- **Must Have** - Highest RICE, directly tied to outcome
- **Should Have** - High value, not critical this cycle
- **Could Have** - Nice to have, cut if pressed
- **Won't Have** - Explicitly out this cycle

### Step 5: Identify assumption gaps
Torres's approach: before committing to a solution, list the riskiest assumptions. Flag items where confidence is low and assumptions are untested.

### Step 6: Recommend clearly
State: "Focus on X, Y, Z this cycle. Reason: [one sentence per item]."

## Anti-Patterns

**1. Prioritizing solutions before opportunities**
Bad: "Should we build a dashboard or a report export?"
Good: "The opportunity is: users can't track progress. Which solution best addresses that?"

**2. Scoring without assumptions**
Bad: RICE scores presented as facts.
Good: "Confidence = 50% because we haven't validated this with users yet."

**3. Everything is Must Have**
Bad: Stakeholders protect everything by labeling it critical.
Good: Force constraint: "You have 3 Must Have slots. Pick 3." Scarcity reveals real priorities.

**4. No connection to outcome**
Bad: Prioritizing features that don't tie to a measurable business outcome.
Good: Every top-priority item maps to an explicit outcome at the top of the tree.

## Quality Checklist

- [ ] Opportunities separated from solutions before scoring
- [ ] RICE scores have stated assumptions
- [ ] Confidence reflects actual evidence level
- [ ] MoSCoW: no more than 40% of items in Must Have
- [ ] Top priorities connect to a stated business outcome
- [ ] Clear recommendation with reasoning at the end
