---
name: ux-audit
description: >
  Audit a user flow for friction and drop-off points. Use when the user says "UX audit",
  "audit this flow", "where are users dropping off", "why isn't this converting",
  "review the onboarding", "usability audit", "what's causing friction",
  "user journey review", or wants to identify why users struggle with a flow
  - even if they don't explicitly say "UX audit".
---

## Overview

Based on **"Don't Make Me Think"** by Steve Krug. Krug's core principle: every question a user has to ask themselves is a source of friction. Good UX eliminates questions. Users don't read - they scan. They don't make optimal choices - they satisfice (pick the first option that seems good enough). Design for scanning, not reading. Design for satisficing, not deliberation.

Krug's usability testing insight: you don't need 20 users. 5 users reveal ~85% of usability problems (Nielsen's law). The fastest audit tool is watching one real user try to use the product.

## Workflow

### Step 1: Define the flow and success criteria
State the flow you're auditing and what success looks like:
- Flow: [start state] to [end state] (e.g., landing page to first value moment)
- Success: [specific action that means the user succeeded]
- Current conversion/completion rate: [if known]

### Step 2: Map every step in the flow
List every screen and decision point a user encounters. Include:
- What the user sees
- What the user must do (read, decide, input, wait)
- What the user must remember from a previous step

Steps requiring memory or prior knowledge are friction points.

### Step 3: Apply Krug's "trunk test"
For each screen: can a user who arrives with no context answer these questions in 5 seconds?
- What site/product is this?
- What page am I on?
- What are the main sections?
- What can I do here?
- Where am I in the flow?
- How do I get started?

If any answer requires more than a quick scan, there's a clarity problem.

### Step 4: Identify cognitive load hotspots
Flag every step where the user must:
- Read more than 50 words to proceed
- Make a decision between more than 3 options
- Remember something from a previous step
- Understand jargon or insider terminology
- Enter data that could be pre-filled or inferred

### Step 5: Check for happy path bias
Most flows are designed for the happy path. Audit the non-happy paths:
- What happens on validation error?
- What happens if the user stops and returns later?
- What happens if the user goes backward?
- What happens on network failure?

### Step 6: Prioritize findings

| Priority | Criteria |
|----------|----------|
| P1 | Blocks completion of the flow for significant user segments |
| P2 | Adds significant friction but users can complete with effort |
| P3 | Minor confusion, edge cases, polish |

### Step 7: Write the audit report

```
UX Audit: [flow name]
Date: [date]
Flow: [start] to [end]
Current completion rate: [x]% (if known)

P1 Issues:
  [screen/step]: [problem] -> [impact] -> [recommended fix]

P2 Issues:
  [screen/step]: [problem] -> [impact] -> [recommended fix]

P3 Issues:
  [screen/step]: [problem] -> [recommended fix]

Quick wins (high impact, low effort):
  [list]
```

## Anti-Patterns

**1. Auditing without watching real users**
Bad: Designer audits their own flow based on their own understanding.
Good: Watch 3-5 real users attempt the flow. Say nothing. Note where they hesitate, misclick, or ask questions.

**2. Auditing only the happy path**
Bad: Audit covers only the ideal case (valid inputs, no errors, no confusion).
Good: Explicitly test error states, re-entry, and edge cases.

**3. P1 everything**
Bad: Every finding marked critical.
Good: Prioritize ruthlessly. One genuine P1 is worth more than 10 vague concerns.

**4. Audit without a benchmark**
Bad: Findings with no baseline.
Good: Know the current completion rate before the audit. After fixes, measure again.

## Quality Checklist

- [ ] Flow and success criteria defined before audit begins
- [ ] Every step in the flow mapped including decision points
- [ ] Trunk test applied to each screen
- [ ] Cognitive load hotspots flagged (reading, deciding, remembering)
- [ ] Non-happy paths audited (errors, re-entry, back navigation)
- [ ] Findings prioritized P1/P2/P3
- [ ] Each finding has a recommended fix direction
- [ ] Quick wins (high impact, low effort) identified separately
