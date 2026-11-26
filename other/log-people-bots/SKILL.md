---
name: log-people-bots
description: "Bots. A log play (docs/useCases/people/bots.md): log drops bots from the Relate network view and keeps them as people you can still read: a bot is whoever log's own reading of a chat calls automated, a stored profile the platform flagged, a hand label, a name that says bot, or the platform account itself. The flag is written by `markAutomatedIdentity`, which the catch-up path only writes for messages read after it existed, so a backlog can hold bots with no flag at all: @MEE6, @Welcomer, @Discohook Utils and @Hermes-Log are ordinary-looking people there until the platform itself says otherwise. `peopleBots` asks the platforms for their own answer and records it, so nothing is inferred from a name."
when_to_use: "Use when the owner asks for this, in words like: \"there are bots in my network\", \"why is MEE6 a person\"."
metadata:
  summary: "Bots"
---

# Bots

This is the log play `people/bots`. Before anything else, call the log MCP tool `getGuide({ useCase: "people/bots" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

log drops bots from the Relate network view and keeps them as people you can still read: a bot is whoever log's own reading of a chat calls automated, a stored profile the platform flagged, a hand label, a name that says bot, or the platform account itself. The flag is written by `markAutomatedIdentity`, which the catch-up path only writes for messages read after it existed, so a backlog can hold bots with no flag at all: @MEE6, @Welcomer, @Discohook Utils and @Hermes-Log are ordinary-looking people there until the platform itself says otherwise. `peopleBots` asks the platforms for their own answer and records it, so nothing is inferred from a name.

How the owner asks for it: "there are bots in my network", "why is MEE6 a person".

## Run it from a fresh context

Say: **"go on docs/useCases/people/bots.md"**. The agent reads this page and runs the steps. Nothing is sent: only log.db is written, and the platforms are only read.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Ask each platform that keeps an automated flag for its own answer and record it: Discord's member list per server plus the people log already knows and the account's own user, Slack's `is_bot` / `bot_id` | `peopleBots` {} | one line per platform with how many members were read, how many the platform says are automated, and how many were newly marked |
| 2 | Read the network again: the bots are no longer people in any state, and the count per platform is the identities log knows minus them | `relateMachine` { view: "network" } | a bot's handle is missing from the network and its own person view still answers |

## What to know

- It is idempotent: a second run marks nothing new and says how many were already marked.
- Names are never used. X, Instagram and LinkedIn keep no automated flag in what log stores, so they are skipped and the output says so.
- A platform whose session is missing is a coded refusal (`noPlatformSession`) for that account, never a guess.
- `botKnowledge` still reads log.db only: the network view makes no platform call when it is asked who is a bot.
- The graph owner runs the same backfill on its own, spaced (6 h apart, retried 30 min after a failure) while it streams events; `LOG_BOTS_BACKFILL=off` stops it.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [The Relate graph](https://github.com/matthewdonsemail-lab/log/blob/main/docs/relateGraph.md)
