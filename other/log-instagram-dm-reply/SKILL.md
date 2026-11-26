---
name: log-instagram-dm-reply
description: "Reading and answering an Instagram DM. A log play (docs/useCases/instagram/dmReply.md): Read what someone wrote to the account on Instagram and answer it in the owner's voice, with text or a meme, on the account's own session through vendor/instagrapi. No browser, ever."
when_to_use: "Use when the owner asks for this, in words like: \"read my instagram dms\", \"what did <someone> say on instagram\", \"reply to <someone> on instagram\", \"send <someone> a meme on instagram\""
metadata:
  summary: "Reading and answering an Instagram DM"
---

# Reading and answering an Instagram DM

This is the log play `instagram/dmReply`. Before anything else, call the log MCP tool `getGuide({ useCase: "instagram/dmReply" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Read what someone wrote to the account on Instagram and answer it in the owner's voice, with text or a meme, on the account's own session through vendor/instagrapi. No browser, ever.

How the owner asks for it: "read my instagram dms", "what did <someone> say on instagram", "reply to <someone> on instagram", "send <someone> a meme on instagram"

## Run it from a fresh context

Say: **"go on docs/useCases/instagram/dmReply.md for <someone>"**. The agent reads this page and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 1 | Session check | `instagramSessionCheck` { account } | `loggedIn` as the account's handle |
| 2 | The inbox, or the thread with them | `instagramDms` { account }, then `instagramDms` { account, with: "<handle>" } | their latest message and what came before it |
| 3 | Pull how the owner writes to them, then draft only from facts the owner gave | `voice` { to: "<handle>", with: "<who>", context } (no text) | a draft that answers what they said |
| 4 | For a meme, find one that fits the moment, ranked by the owner's taste, and save its picture | `memelordSearch` { query: ["<the moment>"], method: "fulltext", type: "meme" } | a template that fits, saved as a JPEG |
| 5 | Gate the draft or the meme | `voice` { to, with, context, text: "<draft or media url>" } | it passes |
| 6 | Send it: text one message per line, a meme as `photo` | `instagramSendLive` { account, with: "<handle>", text and/or photo: "<file>", approvedBy: "<owner>", confirmLive: true } | Instagram answers each message with its id |
| 7 | Tell the owner what they said and what went out | the reply to the owner | both quoted with their times |

New messages arrive by themselves: the inbox hook keeps `log instagram watch --inbox` open for every signed-in Instagram account on Instagram's realtime connection and puts each new DM in front of the agent (`>>> NEW INSTAGRAM MESSAGE`).

## What the runs taught

- **Never the browser.** On 2026-11-04 a meme went out through the account's [AdsPower](https://www.adspower.com/share/pD25Iu) browser and the owner said that is not the way: read, send and watch are the engine's.
- **A meme goes as the picture.** [Memelord](https://www.memelord.com/sign-up?ref=kfwut9wc) answers with a media URL; save it as a JPEG and send it as `photo`, never the link.
- **Pick from the top of the taste ranking, with judgement.** A template built on a stereotype is skipped even when it ranks first.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

> Some links in this play carry ListeningKit's referral or affiliate credit (a `ref=` or `aff=` code). They cost the owner nothing extra; use the plain address without the code if you prefer.
