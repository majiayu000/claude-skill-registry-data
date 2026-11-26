---
name: log-twitter-followers
description: "Checking who really follows you. A log play (docs/useCases/twitter/followers.md): Before a slide, a page or a message says someone follows you (or that you follow them), check it live on X. Engaging with you isn't following you. This page reads it on the account's own session and sends nothing."
when_to_use: "Use when the owner asks for this, in words like: \"does <someone> follow me\", \"check who really follows me on x\", \"is <someone> following me on twitter\", \"check these people follow me before the slide says so\"."
metadata:
  summary: "Checking who really follows you"
---

# Checking who really follows you

This is the log play `twitter/followers`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/followers" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Before a slide, a page or a message says someone follows you (or that you follow them), check it live on X. Engaging with you isn't following you. This page reads it on the account's own session and sends nothing.

How the owner asks for it: "does <someone> follow me", "check who really follows me on x", "is <someone> following me on twitter", "check these people follow me before the slide says so".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/followers.md for <handles>"**, or "for everyone named on <page>". The agent then reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | Session check | `twitterSessionCheck` | `loggedIn` |
| 1 | For each handle: do they follow the account, does the account follow them | `twitterFollows` { account, handles: ["a", "b", "c"] } | one answer per handle, from X |
| 2 | Take anyone who doesn't follow off the "followers" line, or reword the line | the page or copy | every name on it is true today |

Handles come from research or from the owner, never guessed (rule 53). The read is 1.5 s per handle, so a long list takes a minute.

## What the runs taught

- **People who engage aren't always followers.** A slide naming the account's "circle" listed people who had only engaged; two of them didn't follow. Every named follower now gets this check first.
- **The full follower list comes from the account's own session,** not from who engaged.

## Reading the list

`log twitter followers --account <a>` (MCP `twitterFollowers`) reads the account's full follower list on its own session, on the direct-API engine.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [All X use cases, and the parts they share](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md)
- [What log does on X](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/x.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
