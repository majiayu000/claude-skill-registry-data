---
name: queue
description: Defer a request to run after the current turn instead of interrupting it.
disable-model-invocation: true
argument-hint: [request to run after the current turn]
---

The request below was deferred with /queue, so it runs after the previous turn
finished — by which point the user has likely stepped away and isn't watching
live. So:

- Treat it as a normal, fresh request. Don't mention that it was queued or
  deferred — just do it.
- Don't stop to ask clarifying questions. Make a reasonable choice, note the
  assumption you made, and carry on to completion.
- End with a one-line summary: what you did, and anything that needs the
  user's attention when they're back.

$ARGUMENTS
