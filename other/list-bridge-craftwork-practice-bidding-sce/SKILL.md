---
name: list
description: >
  Queue an item WITHOUT acting on it. Appends the provided text as a new pending
  item on the working todo list, then stops. Use /list <text> to stack up tasks
  or notes one at a time; act on them later with /go. Does not plan or start the work.
---

# /list — queue an item (don't act)

Append the skill's argument text as ONE new `pending` item on the working todo
list, using the TodoWrite tool: send the full list = every existing item
**unchanged** plus the new pending item (its `content` is the provided text,
verbatim; `activeForm` a present-tense form of it).

Then reply with a single line: what was just queued and the current pending count.

**Do NOT act, plan, research, or start the work** — `/list` only stacks the item.
If the argument is empty, just show the current queue. Acting happens on `/go`.
