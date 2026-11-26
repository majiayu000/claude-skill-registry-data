---
name: log-inbox-quiet-push
description: "Quieting the live push. A log play (docs/useCases/inbox/quietPush.md): The live push brings every new message into the owner's session the moment it lands. When the owner wants a break from it, the push goes quiet for as many minutes as he says: the watchers keep hearing and storing everything, nothing is pushed into any session until then, and what came in arrives as one batch when it ends."
when_to_use: "Use when the owner asks for this, in words like: \"go silent for 30 minutes\", \"turn the notifications back on\""
metadata:
  summary: "Quieting the live push"
---

# Quieting the live push

This is the log play `inbox/quietPush`. Before anything else, call the log MCP tool `getGuide({ useCase: "inbox/quietPush" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

The live push brings every new message into the owner's session the moment it lands. When the owner wants a break from it, the push goes quiet for as many minutes as he says: the watchers keep hearing and storing everything, nothing is pushed into any session until then, and what came in arrives as one batch when it ends.

How the owner asks for it: "go silent for 30 minutes", "turn the notifications back on"

## Run it from a fresh context

Say: **"go on docs/useCases/inbox/quietPush.md for <minutes>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Quiet the push for the minutes the owner named, or 0 to end it now | `inboxQuiet` { minutes, by: "<owner>" } | the time it ends |
| 2 | Tell the owner when it ends | the reply to the owner | the owner knows the push is quiet until then, and that nothing is lost |

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
