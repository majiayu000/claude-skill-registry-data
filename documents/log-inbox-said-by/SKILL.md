---
name: log-inbox-said-by
description: "Someone's messages on every platform, found by name, newest first. A log play (docs/useCases/inbox/saidBy.md): Someone's messages on every platform, found by name, newest first. Made from a hand-rolled one-off with log tool scaffold (getGuide({ useCase: \"log/toolFromOneOff\" })), so it is a log tool from now on and the one-off is never written again."
when_to_use: "Use when the owner asks for this, in words like: \"what did he say\", \"find his messages\", \"everything they said\""
metadata:
  summary: "Someone's messages on every platform, found by name, newest first"
---

# Someone's messages on every platform, found by name, newest first

This is the log play `inbox/saidBy`. Before anything else, call the log MCP tool `getGuide({ useCase: "inbox/saidBy" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Someone's messages on every platform, found by name, newest first. Made from a hand-rolled one-off with log tool scaffold (getGuide({ useCase: "log/toolFromOneOff" })), so it is a log tool from now on and the one-off is never written again.

How the owner asks for it: "what did he say", "find his messages", "everything they said"

## The steps

| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Someone's messages on every platform, found by name, newest first | `saidBy` { name, limit } | it answers what the one-off answered |

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
