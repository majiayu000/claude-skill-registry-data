---
description: Show what this workspace has actually done to context cost in this repo — weekly context-per-turn, before and after. Use when the user asks whether chamnan is worth keeping.
---

# Show the effect, honestly

```
chamnan-report
```

## Reading it out

The metric is **context per call** — tokens carried into each API request. That is what a workspace
can change. Cost per call is not: it moves when the user switches model, which has nothing to do
with this plugin, and quoting it would take credit for something the plugin did not do.

`new-read/call` is the sharper number. It counts material entering the context for the first time —
files being opened. That is exactly what an index is supposed to make unnecessary.

## What not to say

Do not present this as proof. The user's model, tasks, and Claude Code itself all changed over the
same weeks. It is an observation on one repository, which is the honest and useful thing about it:
it is *their* number, not a figure from someone's README.

If there is not enough history on both sides yet, say that plainly and stop. Do not reach for a
comparison the data cannot support.
