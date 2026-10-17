---
name: design-critique
description: >
  Critique a design for usability, hierarchy, and accessibility. Use when the user says
  "critique this design", "review this screen", "what's wrong with this UI",
  "design feedback", "UX review", "how can I improve this", "review my mockup",
  "is this good UX", or shares a design and wants structured feedback
  - even if they don't explicitly say "design critique".
---

## Overview

Based on **"The Design of Everyday Things"** by Don Norman. Norman's framework: good design makes the right action obvious and the wrong action difficult. Bad design forces users to think when they should act. A critique is not about aesthetics - it's about whether the design communicates correctly: what can I do here, how do I do it, and did it work?

Norman's three key concepts:
- **Affordances** - what actions does the design suggest are possible?
- **Signifiers** - what cues communicate where and how to act?
- **Feedback** - does the system communicate the result of every action?

## Workflow

### Step 1: Define the user goal
Before critiquing, state: what is the user trying to accomplish on this screen?
Critiques without a user goal produce aesthetic feedback, not usability feedback.

### Step 2: Check affordances and signifiers
Walk through every interactive element:
- Is it obvious this is clickable/tappable/draggable?
- Does the visual design suggest the correct interaction?
- Are buttons distinguishable from static content?
- Does the hierarchy direct attention to the primary action?

Norman: "If it requires a label, the design has failed."

### Step 3: Check feedback
For every action a user can take:
- Is there immediate visual feedback that the action registered?
- Are loading states communicated?
- Are success and error states clearly differentiated?
- Does error feedback tell the user what to do next, not just what went wrong?

### Step 4: Apply Nielsen's 10 Heuristics
Scan the design against each heuristic:
1. **Visibility of system status** - does the user always know what's happening?
2. **Match with real world** - does language and metaphor match user expectations?
3. **User control and freedom** - can users undo, escape, or cancel?
4. **Consistency and standards** - does it follow platform conventions?
5. **Error prevention** - does the design prevent mistakes before they happen?
6. **Recognition over recall** - are options visible, not memorized?
7. **Flexibility and efficiency** - does it serve both novice and expert users?
8. **Aesthetic and minimalist design** - is every element earning its place?
9. **Help users recognize, diagnose, recover from errors** - are errors human-readable?
10. **Help and documentation** - is help available when needed?

### Step 5: Check accessibility
- Color contrast ratio >= 4.5:1 for normal text, 3:1 for large text (WCAG AA)
- Interactive targets >= 44x44px (mobile), >= 24x24px (desktop)
- No information conveyed by color alone
- Focus states visible for keyboard navigation

### Step 6: Write the critique
Structure as:
- **Works well** - what the design gets right (always include this)
- **Critical issues** - prevents task completion, must fix
- **Usability issues** - adds friction, should fix
- **Polish** - optional improvements

For each issue: describe the problem, explain the impact, suggest a solution.

## Anti-Patterns

**1. Aesthetic critique instead of usability critique**
Bad: "The blue is too dark. I'd try a lighter shade."
Good: "The CTA button doesn't have enough contrast against the background. Users with low vision may not see it as actionable. Test with contrast ratio >= 4.5:1."

**2. Critique without knowing the user goal**
Bad: Generic feedback about layout without understanding what the user is trying to do.
Good: "Given that the primary goal is checkout completion, the payment form should be the dominant element. Currently the promotional banner competes with it."

**3. No positive feedback**
Bad: Only problems listed.
Good: Name what's working. It tells the designer what to preserve and builds trust in the critique.

**4. Solutions without problems**
Bad: "Make the button bigger."
Good: "The CTA is competing with 3 other buttons of equal weight. Users don't know where to look first. Establish a clear visual hierarchy."

## Quality Checklist

- [ ] User goal stated before critique begins
- [ ] Affordances and signifiers reviewed for every interactive element
- [ ] Feedback reviewed for every user action
- [ ] Nielsen's 10 heuristics scanned (at least the relevant ones)
- [ ] Accessibility: contrast, touch targets, color-as-information
- [ ] Critique has positive feedback section
- [ ] Issues classified: critical / usability / polish
- [ ] Every issue paired with a suggested direction (not just a problem)
