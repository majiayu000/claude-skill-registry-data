---
name: fix-in-the-shared-layer
description: Use when a bug surfaces while building on one's own shared code - a library, base class, SDK, or component.
---

## The rule

A bug you hit while using your own shared code is almost never a one-off. It's a gap in the shared layer, and every other caller has it too, they just haven't tripped it yet. Fix it where it lives so the fix is inherited everywhere, instead of working around it in the one place you happened to notice.

This is a different move than fix-the-root-cause. That rule picks the causal layer of a bad state; this one is about ownership: when the gap is in code you share, fix it there so every caller inherits the fix.

## Fires when

While building one feature you hit a bug in a util, base class, component, or SDK that other features also use, and you're tempted to add a local workaround.

## How to apply

When a bug surfaces through shared code, ask "would another caller hit this too?" The answer is usually yes. Fix the shared layer and let every consumer inherit it. Then check the fix against the other callers, not just the one that surfaced it.

A workaround at your call site leaves the trap armed for the next person.

## Worked example

Building the invoices screen, you see due dates render a day early for users east of UTC. The cause is your shared date-format helper: it silently converts to UTC before formatting. The tempting patch is to shift the date back on the invoices screen. But the reports screen and the CSV export call the same helper, so they're quietly wrong too — nobody has noticed yet. Fixing the helper to format in the user's timezone repairs all three at once. The step that matters afterwards: re-read the other two callers, because one of them may have built its own compensation on top of the old behavior. The local shift would have "fixed" one screen and left the rest of the product lying.

## Red flags

| Thought | Reality |
|---|---|
| "I'll just guard it here" | The same trap is still armed everywhere else. |
| "It only happens in my screen" | It happens wherever the shared code is called. |
| "I don't want to touch the shared util" | That's exactly where the bug is. |
