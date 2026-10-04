---
name: phxstack-simplify
description: Propose removals only, never new architecture. Use when a spec, diff, file, subsystem, or whole repository feels bloated, over-engineered, or sloppy.
---

# phxstack-simplify

One question: can this be less?

Look for dead code, unused exports, one-caller abstractions, pass-through
layers, unused configuration, needless dependencies, speculative extensions,
duplicate structures, and comments that restate code.

Every proposal must be:

```text
REMOVE
<thing>

LOSE
<what capability disappears, or "nothing">
```

Propose removals only. Show the list before changing anything and apply only
what the developer approves, in small verified batches.
