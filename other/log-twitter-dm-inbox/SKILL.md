---
name: log-twitter-dm-inbox
description: "Reading the DM inbox: who is waiting on you. A log play (docs/useCases/twitter/dmInbox.md): Read every DM conversation on the account and sort it into a pipeline: who is waiting on you and what they asked, who you're waiting on, and what to do next for each. It sends nothing and marks nothing read. Replies only go out after the owner says what to send."
when_to_use: "Use when the owner asks for this, in words like: \"who is waiting on me\", \"check my x dms\", \"go through my twitter inbox and tell me who needs a reply\", \"who am I waiting on in my dms\"."
metadata:
  summary: "Reading the DM inbox: who is waiting on you"
---

# Reading the DM inbox: who is waiting on you

This is the log play `twitter/dmInbox`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/dmInbox" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Read every DM conversation on the account and sort it into a pipeline: who is waiting on you and what they asked, who you're waiting on, and what to do next for each. It sends nothing and marks nothing read. Replies only go out after the owner says what to send.

How the owner asks for it: "who is waiting on me", "check my x dms", "go through my twitter inbox and tell me who needs a reply", "who am I waiting on in my dms".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/dmInbox.md"**. The agent then reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Who is waiting on you: conversations where the last message isn't yours, message requests included | `twitterDms` { account, waiting: true, limit: 50 } | a list, newest first, with each conversation id |
| 2 | The latest conversations, whoever spoke last | `twitterDms` { account, limit: 10 } | the newest 10 |
| 3 | Read the ones that matter in full | `twitterDms` { account, conversation: "<id>" } | what they asked, and when |
| 4 | Who they are: bio and followers, and whether they're already in your CRM | [treg](https://treg.to/?ref=matthewdonse-aebsh)'s X profile read, Twenty | one line per person |
| 5 | Sort it into a table: **reply now** (a real opportunity waiting on you), **waiting on them** (worth one nudge), **no action** (pitches, spam). Each with a suggested move | wherever the owner reads | the owner picks what to answer |
| 6 | Send what the owner approves, dry run first. One person: dry run, then live. Two or more go into the account's one queue, never a loop of sends (rule 105): `twitterQueueAdd` { queue, targets, action: "dm", by } adds them, even while it runs, at least minGap apart; if no run is going, `twitterQueueRunLive` { queue, keepOpen: true, confirmLive: true } starts it. Right before each send the queue reads that person again and holds the item when anything changed (rule 109) | `twitterDm`, then `twitterDmLive` { userId, text, approvedBy, confirmLive: true }, or `twitterQueueAdd` and `twitterQueueRunLive` | X's answer is `sent` |

Who wrote last is already in context at the start of a session: the SessionStart hook reads it from the account's local inbox store, with nothing fetched. `twitterDms` keeps that store up to date the way X's own app does: the first read takes the whole inbox once (about 20 s), and every read after asks X only for what is newer (about 5 s), decrypting only what is new and adding it to the conversation search. `full: true` reads everything again.

## What to know

- **The threads are already local.** `~/.logCli/conversations/twitter/<account>` holds every saved thread and `~/.logCli/log.db` every event since (messages, the account's own, notifications): read who is waiting and what they said from there first, and read X only for one person right before a send (rule 109).
- **Gate one draft at a time.** Running several `voice` gates at once crashed them on 2026-11-07 (EPERM renaming `search/voice/vectors/manifest.json`); nothing was sent, and run one after another they pass.
- **Past the daily cap only when the owner says.** At its request cap the governor refuses every read; `twitterDms` { force: true } reads past it for that call, and the governor still counts it (rule 86). On 2026-11-02 xAccount read its inbox at 501-506 of 500 this way, with the owner's go-ahead.
- **A nudge can be a meme.** Where someone owes a reply or promised something, `twitterDmLive` { media: ["<meme url>"] } sends the meme as an image on the first message, with the nudge after it (docs/extensions/memelord.md). A chat where the owner's last messages are still unanswered gets nothing stacked on top.

- `twitterDms` reads the inbox, the message requests and X's encrypted Chat. X Chat opens with the account's X Chat PIN, saved once in a masked terminal prompt (`log twitter chat pin --account <account>`); without it X Chat threads show who and when, not what.
- A person can have both an old DM thread and an X Chat thread. Read them together with `twitterDms` { account, with: "<handle>" } before answering, so nothing they said in X Chat is missed.
- Every X Chat message opens with the saved PIN: a reaction shows as `(reacted 🔥)`, an edit as `(edited) …`, a photo as `(image: name.jpg)`, a shared post or link as its URL, and a read marker is hidden, so "they read it and haven't answered" never looks like a message waiting on you. A message still showing "could not open" is reopened the next time its chat is read, and each sync reopens a few on its own. Group chats are read with `twitterDms` { account, conversation: "g…" }.
- **Photos and files open.** Reading a person or a conversation (`twitterDms` { with } or { conversation }) downloads each X Chat image, gif, video or file the way X's own chat app does (ton.x.com `xchat_media/<conversation>/<mediaHashKey>`, decrypted with the conversation key it was sent under) into `~/.logCli/twitter/<account>/media/<conversation>/`, and the message shows `(image saved: <path>)`. Open that path to see what they sent before answering: at most 8 a read, and a stored message whose file was never fetched is asked of X again, 3 a read.
- **Behind after a network blip catches up by itself.** When an account is behind (`accountBehind`), only X's own refusal (a 429, 226, 344 or soft block) holds it until the owner says `inboxResume`. A DNS failure, a timeout or log's own crash leaves the gap open, and the owner's next check (every 30 s) catches up through the account's one session. A gap once held for one of those reopens by itself (rule 94, REQ-HOOKS-23). Once, one account had been held since a DNS failure and another since a crash. Both caught up, and `twitterDms` { with } reads came back from log.db in about 150 ms. If `twitterDms` is slow, `timing` { call } now shows the keep-for-search step (`keep.shape`, `keep.save`, `keep.rows`, `db.writeLock`).
- **Opened with no reply is a follow-up.** When their last event is a reaction to the owner's message (`(reacted ❤️)`), or their read receipt is past his last message, they opened it and didn't type back. It isn't a reply waiting on him: `twitterDms` { waiting: true, limit: 200 } lists it apart ("they opened it, no reply yet: follow up"), and the follow-up is the network-maxing kind (networkMaxing.md, "Everyone who opened it"). X Chat read receipts come through as events of an unknown type, sent by the reader right after the other side's message; they're never shown as messages.
- Before answering, check who actually wrote last: a thread where the owner's message is the newest real one isn't waiting on him, even if the list put it there.
- X has its own daily limit on tweets and messages (code 344; the governor allows 240 writes a day, likes, reposts and follows included, and X can still stop it before that), and going past the governor doesn't get past it. Spend the day's writes on people who answered first. After a 344 nothing more goes out until the owner says so.
- To find something said in any conversation, search instead of reading every thread: `search` { query, with, after } after `searchIndex`.
- A DM send counts as a write against the account's 240 a day.
- **Missed openings** ("look on my twitter for missed opportunities"). The waiting list only shows who wrote last right now. It misses a thread where someone explained their model, said they're hiring, said "lets do it" or offered an intro, and the talk then stopped. Go through the saved conversations instead (`~/.logCli/conversations/twitter/<account>/*.json`, merged by `with`, since the old DM and X Chat files of one person are two files). Keep the threads from the last two weeks where they wrote last, or where their last few messages carry a deal signal (hiring, retainer, price, collab, intro, a question). Then read each one in full with `twitterDms` { with } before saying anything. The saved copy can be behind: it once showed a contact unanswered when the owner had already replied. Group banter, spam and cold pitches at the owner aren't openings. What to send to the openings is [collabMaxxing.md](../log-twitter-collab-maxxing/SKILL.md).
- The waiting list can show people the owner already answered in the old DM inbox (seen with three people at once). Check the thread before treating one as waiting.
- Everyone is told to the owner by @username, never as a number (rule 154). The list names each person before it is shown; if one still comes back as an id, that is a bug to fix in the same turn, not something to pass on. Once six of seventeen came back as ids until `name_people` named them.
- Tell the owner what each conversation is about in one line, newest first, grouped: people waiting on him, people who reacted (a follow-up), automated notices. Nothing is sent until he says which.

## Next

- [#34](https://github.com/matthewdonsemail-lab/log/issues/34) writes every conversation into Twenty, so each person's thread sits on their record.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [All X use cases, and the parts they share](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md)
- [What log does on X](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/x.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

> Some links in this play carry ListeningKit's referral or affiliate credit (a `ref=` or `aff=` code). They cost the owner nothing extra; use the plain address without the code if you prefer.
