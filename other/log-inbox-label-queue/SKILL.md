---
name: log-inbox-label-queue
description: "Teaching log who your people are. A log play (docs/useCases/inbox/labelQueue.md): log reads who each person is and where they are on every new message, with a small model on this machine. It is only as good as the labels it learns from, so it asks the owner about the chats it is least sure of, about ten minutes of his time, then trains on his answers. SubQ can label the rest once, as a paid pass he approves after seeing the cost."
when_to_use: "Use when the owner asks for this, in words like: \"what should i label\", \"teach the labeller\", \"train the labeller\", \"which chats are you unsure about\""
metadata:
  summary: "Teaching log who your people are"
---

# Teaching log who your people are

This is the log play `inbox/labelQueue`. Before anything else, call the log MCP tool `getGuide({ useCase: "inbox/labelQueue" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

log reads who each person is and where they are on every new message, with a small model on this machine. It is only as good as the labels it learns from, so it asks the owner about the chats it is least sure of, about ten minutes of his time, then trains on his answers. SubQ can label the rest once, as a paid pass he approves after seeing the cost.

How the owner asks for it: "what should i label", "teach the labeller", "train the labeller", "which chats are you unsure about"

## Run it from a fresh context

Say: **"go on docs/useCases/inbox/labelQueue.md"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | List the chats log is least sure of, spread across platforms | `inboxLabelQueue` { limit? } | up to 35 chats, each with log's guess |
| 2 | Show the owner each chat's name and guess and take his answer: who, and where only for a lead or client | `inboxLabel` { platform, account, chat, who, where?, by: "<owner>" } | each answer is stored |
| 3 | Optional: show what one SubQ pass over the unlabelled chats would cost; run it with apply only after the owner says yes to that cost | `inboxLabelTeach` { apply? } | the cost is shown, or SubQ's labels are stored |
| 4 | Train the labeller on the owner's labels and SubQ's confident ones | `inboxLabelTrain` {} | a head is stored with its counts |
| 5 | Tell the owner what changed: the who and where counts and anything that moved | `inboxLabels` {} | he sees the new counts |

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
