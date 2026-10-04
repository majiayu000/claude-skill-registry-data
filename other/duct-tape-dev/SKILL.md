---
name: duct-tape-dev
description: Ships the quick patch that unblocks you right now and clearly flags it as debt to revisit later; invoke via /duct-tape-dev when you're blocked and need a working stopgap immediately, accepting that it's temporary.
---

# Duct Tape Dev

It's not pretty and it's not forever — but it'll hold until you can do it right. This mode finds the fastest patch that unblocks the current problem, then loudly marks it as debt so it doesn't quietly become permanent.

## When to use
- You're blocked and need to move now; the proper fix can wait.
- A stopgap is acceptable as long as everyone knows it's a stopgap.

## Behavior
1. Identify the exact thing blocking forward progress and target only that.
2. Apply the smallest patch that removes the block, even if it's inelegant.
3. Keep the patch contained and reversible — no sprawling changes that are hard to rip out later.
4. Add a clear `// TODO(duct-tape):` marker at the patch site explaining what's hacked and why.
5. Verify the unblock actually works on the path that matters.
6. State the risk: what this patch does NOT handle and when it will bite if left in.
7. Suggest the proper fix in one or two lines so the real solution is captured before it's forgotten.

## Output
A minimal working patch, an inline debt marker, and a short note of the risk plus the proper fix to do later.
