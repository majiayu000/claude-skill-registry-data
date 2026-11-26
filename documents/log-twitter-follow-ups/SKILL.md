---
name: log-twitter-follow-ups
description: "Following up in your own voice. A log play (docs/useCases/twitter/followUps.md): Answer or follow up the people the owner picked, each in the owner's own voice, the way they write to that person. It's for warming a relationship as much as for a deal: say it was good to meet, ask for advice, take someone up on an offer, keep a door open. Nothing goes out until the owner has seen every draft and said yes."
when_to_use: "Use when the owner asks for this, in words like: \"follow up with these, not for anything in particular, just warming up the relationship\", \"say it was cool to meet him\", \"ask him for some advice on what he's doing\", \"take him up on the doc he offered\"."
metadata:
  summary: "Following up in your own voice"
---

# Following up in your own voice

This is the log play `twitter/followUps`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/followUps" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Answer or follow up the people the owner picked, each in the owner's own voice, the way they write to that person. It's for warming a relationship as much as for a deal: say it was good to meet, ask for advice, take someone up on an offer, keep a door open. Nothing goes out until the owner has seen every draft and said yes.

How the owner asks for it: "follow up with these, not for anything in particular, just warming up the relationship", "say it was cool to meet him", "ask him for some advice on what he's doing", "take him up on the doc he offered".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/followUps.md"**, and who, with what the owner wants from each. The agent reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md), loads `getGuide({ topic: "xSending" })`, and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Read each person in full, old DM thread and X Chat merged | `twitterDms` { account, with: "<handle>" } | everything they've said, oldest first |
| 2 | Take what the owner wants from each, in the owner's words only (met in person, ask advice, take up an offer) | the owner | one intent per person |
| 3 | How the owner really writes to this person: their messages to them first, then the owner's whole history | `voice` { to: "<handle>", with: "<handle>", context: "<what they said>" } | the owner's own lines to draft from |
| 4 | Draft each one from those lines, in the owner's words and length. Every draft reads differently: no shared opener, no stock line. Each line of a draft is one message | the agent | one draft per person |
| 5 | Gate each draft against the same person, and rewrite until it passes | `voice` { to, with, context, text: "<draft>" } | the gate passes |
| 6 | Show the owner every draft as it will go out, one message per line | the owner | the owner says yes, or what to change |
| 7 | One person: dry run, then live. Two or more: put them in the account's one queue, never a loop of sends (rule 105): `twitterQueueAdd` { queue, targets, action: "dm", by } adds them, even while it runs, fitted between what is already planned; if no run is going, `twitterQueueRunLive` { queue, keepOpen: true, confirmLive: true } starts it. A draft on several lines goes out one message per line | `twitterDm`, then `twitterDmLive` { userId, text, approvedBy, confirmLive: true }, or `twitterQueueAdd` and `twitterQueueRunLive` | X's answer is `sent` for every part |

## What to know

- Never ask something the person already told the owner. Read far enough back first (step 1, and `search` { query, with } for older talk).
- Use only facts the owner said. Nothing invented about a meeting, a deal or a number.
- `--asOne` (`asOne: true`) sends a draft as one message, only when the owner asks for that.
- A drop or a 429 stops the rest: what went out stays out, nothing is resent, and the next send waits for the owner (rule 94).
- An account has one queue and one run for everything it sends: follow-ups, reply-guy replies and answers go into the same one (rule 105). Never start a second queue or run beside it, and never send from a hand-run command or a loop (rules 105, 163). Each target carries its own `text`, and its dm items split one message per line the same way.
- Every call goes through the account's one X session (rule 105); the answer's `xSession` names it.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [All X use cases, and the parts they share](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md)
- [What log does on X](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/x.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)
