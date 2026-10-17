---
name: feature-spec
description: >
  Write a concise feature spec for engineering handoff. Use when the user says "write a spec",
  "feature spec", "one-pager for eng", "spec this out", "write up this feature",
  "I need to hand this off to engineering", "shape this up", or wants a concise
  technical brief - even if they don't say "feature spec".
---

## Overview

Based on **Shape Up** by Ryan Singer (Basecamp). A feature spec is not a PRD. A PRD justifies building something. A spec tells engineers exactly what to build - but at the right altitude. Shape Up's principle: give engineers a shaped problem with clear boundaries, not a detailed recipe. Ambiguity in the spec becomes a bug in production. Over-specification kills ownership.

## Workflow

### Step 1: Write the header
```
# Feature Spec: [Feature Name]
**PM:** [your name]
**Eng Lead:** [engineer name]
**Appetite:** [1-2 weeks / 4-6 weeks]
**Status:** Draft | In Review | Approved
**Related PRD / Ticket:** [link]
```

### Step 2: Write the Problem (2-3 sentences)
What is broken or missing? Who is affected? Shape Up framing: "Jobs to be done" - what job is the user hiring this feature to do?

### Step 3: Write the Solution at the right altitude
Shape Up's "fat marker sketch" - describe the solution broadly. Engineers need room to make technical decisions. Write at the level of user-visible behavior, not implementation.

Structure:
- **Key interactions** - what users can do (not how)
- **Boundaries** - explicit scope limits
- **Rabbit holes** - specific traps to avoid

### Step 4: Write Functional Requirements
Number each. Cover in order:
1. Happy path
2. Error states
3. Empty states
4. Edge cases

### Step 5: Write Non-Functional Requirements
Only include what's genuinely constrained:
- Performance targets
- Accessibility level (WCAG AA minimum)
- Browser/device support
- Security or compliance requirements

Don't pad. If there's no real constraint, don't list one.

### Step 6: Define No-Gos (Shape Up)
Explicit list of what this spec does NOT include. This is Shape Up's most important contribution to spec writing - stating what you're NOT building is as important as what you are.

### Step 7: List Open Questions
```
Q: [question]
Owner: [name]
Due: [date]
```
No spec should be approved with unresolved questions. Assign owners.

### Step 8: Link assets
Figma files, API specs, data models. A spec without visuals is incomplete for UI work.

## Anti-Patterns

**1. Over-specifying implementation**
Bad: "The button is blue, 48px, positioned top-right with 16px margin."
Good: "Users can trigger X from the main action area. Exact placement per Figma [link]."
Shape Up: over-speccing removes creative ownership from engineers and designers.

**2. Missing error states**
Bad: "User submits the form and sees confirmation."
Good: Cover success, validation error, server error, empty state, and loading state.

**3. No rabbit holes section**
Bad: Spec that describes what to build but not what to avoid.
Good: "Don't rebuild the notification system for this - use existing email infrastructure."

**4. Spec approved with open questions**
Bad: "TBD" items in an approved spec.
Good: All open questions resolved or explicitly deferred with a named owner and date.

## Quality Checklist

- [ ] Appetite defined (small or big batch)
- [ ] Problem framed as "job to be done"
- [ ] Solution at the right altitude - behavior not implementation
- [ ] Requirements cover happy path, errors, empty states, edge cases
- [ ] No-Gos explicitly listed
- [ ] Rabbit holes called out
- [ ] Open questions have owners and due dates
- [ ] Figma / mockup links included for UI work
- [ ] Spec fits on one page (split if it doesn't)
