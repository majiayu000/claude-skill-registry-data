---
name: write-prd
description: >
  Write a Product Requirements Document (PRD). Use when the user says "write a PRD",
  "document this feature", "product requirements for X", "write requirements",
  "I need a PRD", "pitch this feature", or wants to formalize a feature or product
  idea into a structured doc - even if they don't explicitly say "PRD".
---

## Overview

Based on **Shape Up** by Ryan Singer (Basecamp). A PRD defines the problem, the appetite, and the solution boundaries - not a detailed spec. The key insight from Shape Up: fix the time, flex the scope. Define how much the team is willing to spend before deciding what to build.

## Workflow

### Step 1: Set the Appetite
Before writing requirements, define the appetite - how much time is this worth?
- **Small batch:** 1-2 weeks
- **Big batch:** 4-6 weeks

If the solution requires more time than the appetite allows, cut the scope - don't extend the time.

### Step 2: Write the Problem Statement
One paragraph. Answer: what is broken or missing today, who is affected, and what is the cost of not solving it. Avoid mentioning solutions here.

### Step 3: Write the Pitch (Shape Up format)
Structure:
```
# PRD: [Feature Name]
**Appetite:** [Small batch / Big batch]
**Status:** Draft
**Author:** [your name]

## Problem
[What's broken, who's affected, cost of inaction]

## Solution
[Fat marker sketch - broad strokes, not pixel-perfect]

## Rabbit Holes
[Specific technical or design traps to avoid]

## No-Gos
[Explicitly what this does NOT include]
```

### Step 4: Write the Solution at the right altitude
Shape Up's "fat marker sketch" principle: describe the solution broadly enough that engineers have room to make decisions. Over-specifying kills ownership and slows delivery.

Write requirements at the level of: "Users can do X" - not "There is a button in the top-right corner."

### Step 5: Define Rabbit Holes
List specific traps the team could fall into. Examples:
- "Don't rebuild the notification system - use existing infrastructure"
- "Don't support bulk operations in v1"

### Step 6: Define No-Gos
Explicit list of what this does NOT cover. This is the most important section for scope control.

### Step 7: Add Open Questions
Format:
```
Q: [question]
Owner: [name]
Due: [date]
```

## Anti-Patterns

**1. Specifying solutions in the problem statement**
Bad: "We need to add a modal because users don't see the CTA."
Good: "30% of users drop off at checkout. The CTA is not visible enough."

**2. No appetite defined**
Bad: PRD with requirements but no time boundary.
Good: "This is a small batch - 2 weeks max. If the solution needs more, cut scope."

**3. Missing No-Gos**
Bad: PRD with only what's included.
Good: Explicit No-Gos that prevent scope creep during build.

**4. Over-specified requirements**
Bad: "The button is blue, 48px, positioned top-right with 16px margin."
Good: "Users can trigger X from the main action area." (Let design decide the details.)

## Quality Checklist

- [ ] Appetite is defined (small or big batch)
- [ ] Problem statement explains "why", not "what"
- [ ] Solution is at the right altitude - no pixel-level specs
- [ ] Rabbit holes are listed
- [ ] No-Gos are explicit
- [ ] Open questions have owners and due dates
