---
name: ui-review
description: Use when critiquing an interface design. Covers hierarchy, affordance, consistency, states, and delivering feedback that changes the design rather than describing taste.
metadata:
  category: design
  version: 1.0.0
  tags: [critique, ux, usability, hierarchy, feedback]
---

# UI Review

## Purpose

Critique an interface in a way that improves it. A critique of "it feels cluttered" is a symptom report; a critique that identifies three elements competing for the same visual weight is a fix.

## When to Use

- Reviewing a mockup, a screenshot, or a live interface.
- A design that "feels wrong" and nobody can say why.
- Before a design goes to engineering.
- Auditing an interface for consistency.

## Capabilities

- Hierarchy analysis: what is read first, and is it the right thing?
- Affordance: does the interface communicate what can be done?
- Consistency against a system.
- State coverage: empty, loading, error, overflow.
- Feedback that is specific enough to act on.

## Inputs

- The design, and what the user is trying to accomplish with it.
- The stage: exploration (be generous) or final polish (be exacting).
- The design system, if there is one.

## Outputs

Findings ranked by impact:

- **Blocking** — The user cannot complete the task, or will be misled.
- **Should fix** — The design works but costs the user effort.
- **Consider** — Polish.

Each with a specific observation and a specific fix.

## Workflow

1. **Identify the primary action** — What is this screen for? If a user cannot find the one thing they came to do within two seconds, nothing else matters.
2. **Trace the hierarchy** — Squint at it. What is still visible? That is the actual hierarchy, and it is frequently not the intended one.
3. **Check the affordances** — Does what is clickable look clickable? Is anything that is not clickable styled as though it is?
4. **Enumerate the states** — Empty, loading, error, one item, a thousand items, a very long name. Most designs cover the state where everything is perfect and none of the others.
5. **Check consistency** — Against the design system, and against the rest of the product. Two button styles for the same action is a defect.
6. **Report specifically** — With a location, an observation, and a fix.

## Best Practices

- The squint test is the fastest hierarchy diagnostic available. Blur the design until only the strongest elements are visible. If the primary action is not among them, the hierarchy is wrong regardless of how it looks in focus.
- "Cluttered" is never the finding. The finding is what specifically is competing: three elements at equal weight, or insufficient space between groups, or no clear primary action.
- Every design has an empty state, an error state, and an overflow state. Reviewing only the populated happy-path mockup means reviewing a third of the design.
- A disabled button with no explanation is a dead end. If the user cannot proceed, the interface must say why.
- Do not report taste as though it were a usability finding. "I would have used a different blue" is not a critique.
- Be generous in exploration and exacting in polish. Detailed feedback on a direction that is about to be discarded wastes everyone's time.

## Examples

**A critique that changes the design:**

```markdown
## Review: order detail screen

### Blocking

**No primary action.** "Refund", "Cancel", "Resend receipt", and "Edit" are four
buttons of identical weight, in a row. The screen's purpose — per the brief — is
to let support agents issue refunds. That action is competing with three others
of equal prominence and is third from the left.

Squint test: at 20px blur, the four buttons read as a single grey bar. Nothing
stands out.

Fix: "Refund" becomes the only filled button. The other three become text buttons,
or move into an overflow menu. One primary action per screen.

### Should fix

**The order total is not the most prominent number on the screen.** The order ID
(`ord_01HXKZ8...`) is set at 18px bold; the total ($1,204.80) is at 14px regular.
The ID is a reference the agent copies; the total is the number they are about to
act on.

Fix: swap the weights. The total at 24px semibold; the ID at 13px monospace, muted.

**No empty state for the refund history.** The mockup shows three refunds. What
does an order with no refunds show? Currently, an empty bordered box with a
header. It should say "No refunds issued" so the agent knows it is empty rather
than broken.

### Consider

The status pill and the payment-method pill use different corner radii (4px and
999px). Both come from the design system; one of them is wrong.

### What works

The line-item table is well-composed: the quantity and price columns are aligned
right, the totals row is separated, and the long product names truncate with a
tooltip rather than wrapping. This should be the pattern elsewhere.
```

## Notes

- The squint test finds hierarchy problems in seconds that a careful reading misses in ten minutes. It works because it approximates what the eye actually does in the first half-second.
- Reviewing only the populated state is the most common review failure. Ask for the empty, error, and overflow mockups explicitly — if they do not exist, that is the finding.
- Say what works. A review that is only findings is demoralizing and, more practically, does not tell the designer which patterns to reuse.
