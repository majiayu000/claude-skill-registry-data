---
name: log-inbox-reactions
description: "Reacting to a message. A log play (docs/useCases/inbox/reactions.md): React to someone's message with an emoji on X, Discord, Slack or Instagram, the way a person answers a moment without typing: a laugh at a joke, a fire on a win, a heart on good news. It goes through the platform's own engine and the account's one session, never the browser, and counts as a write (rule 8)."
when_to_use: "Use when the owner asks for this, in words like: \"react to that\", \"heart his message\", \"put a 😂 on what she said\", \"send a reaction to <person>\""
metadata:
  summary: "Reacting to a message"
---

# Reacting to a message

This is the log play `inbox/reactions`. Before anything else, call the log MCP tool `getGuide({ useCase: "inbox/reactions" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

React to someone's message with an emoji on X, Discord, Slack or Instagram, the way a person answers a moment without typing: a laugh at a joke, a fire on a win, a heart on good news. It goes through the platform's own engine and the account's one session, never the browser, and counts as a write (rule 8).

How the owner asks for it: "react to that", "heart his message", "put a 😂 on what she said", "send a reaction to <person>"

## Run it from a fresh context

Say: **"go on docs/useCases/inbox/reactions.md for <person or chat>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Read the chat and find the message to react to, with its id | `twitterDms` { with }, `discordRead` { channel }, `slackRead` { chat } or `instagramDms` { with }, with json | one message named with its author, time and id (a Slack message's id is its ts) |
| 2 | Pick the emoji: the one the owner named, or the one a person would put on that moment | the agent, from the chat | one emoji |
| 3 | Dry run it | `messagesReact` { account, chat, message, emoji }: the platform is the account's (or `twitterReact`, `discordReact`, `slackReact`, `instagramReact`) | the dry run names the chat and the message |
| 4 | React | `messagesReactLive` { account, chat, message, emoji, approvedBy: "<owner>", confirmLive: true } (or `twitterReactLive`, `discordReactLive`, `slackReactLive`, `instagramReactLive`) | the platform answers `sent` |
| 5 | Tell the owner what was reacted to | the reply to the owner | the message quoted with the emoji |

On Discord the chat flag is `channel` and on Instagram `thread`. `remove` takes the account's own reaction off. A refusal stops it, and nothing is tried again until the owner says so (rule 94).

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
