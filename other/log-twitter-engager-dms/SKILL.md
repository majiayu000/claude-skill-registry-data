---
name: log-twitter-engager-dms
description: "DMing the people who liked or reposted your post. A log play (docs/useCases/twitter/engagerDms.md): A post that does well leaves hundreds of people who liked or reposted it and were never followed up. This page turns them into a short list the owner knows is worth it, writes each one a DM that opens on why they're on the list, and sends them through the queue as dms."
when_to_use: "Use when the owner asks for this, in words like: \"dm everyone who liked my post\", \"message the people who retweeted my tweet\", \"dm the likers and reposters of <post url> pitching <what>\"."
metadata:
  summary: "DMing the people who liked or reposted your post"
---

# DMing the people who liked or reposted your post

This is the log play `twitter/engagerDms`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/engagerDms" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

A post that does well leaves hundreds of people who liked or reposted it and were never followed up. This page turns them into a short list the owner knows is worth it, writes each one a DM that opens on why they're on the list, and sends them through the queue as dms.

This is outbound DMs. Reading the inbox and answering people who are waiting is [dmInbox.md](../log-twitter-dm-inbox/SKILL.md).

How the owner asks for it: "dm everyone who liked my post", "message the people who retweeted my tweet", "dm the likers and reposters of <post url> pitching <what>".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/engagerDms.md for <post url>, pitching <what>"**. The agent then reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md) and runs the steps.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | Session check | `twitterSessionCheck` | `loggedIn` |
| 1 | Who liked and reposted the post. X only shows likers of your own post to your own session | `twitterNotifications` { account, type: "likes", post } and again with type "reposts" (the account's own session, free; [notifications.md](../log-twitter-notifications/SKILL.md)); [treg](https://treg.to/?ref=matthewdonse-aebsh)'s likers read for anything older than the notifications reach | the list, with each person's user id |
| 2 | Score them: their bio matches who you want, they reposted (a bonus) or engaged with more than one post, and a sensible follower count. Few followers and no bio is a bot | treg's X profile read | a ranked list |
| 3 | The owner checks the top of the list: drop the team, people they don't want to contact, and friends (friends get a personal note, not a template) | a table | the owner's corrections applied |
| 4 | Check for an existing thread with each person, and DMs already waiting | `twitterDms` { account, limit: 200 } | no one gets a cold template where a chat already exists |
| 5 | Write each DM the first-DM way below: their own tweet forwarded first, then one informal line | house style | passes `twitterQueueCheck` |
| 6 | Queue as dms: targets are `{handle, user_id, text}`, `action: "dm"`. Approve, plan, run live | README queue steps, `twitterQueueBuild` { action: "dm" }, `twitterQueueRunLive` | `finished` |

## How a first DM opens

The first message is the opener and nothing else: always relevant to them, never an ask. No pitch, no "you using `<tool>` yet", no call, no link to the owner's own stuff. Going in for the kill on a first message is what a template does. The ask comes later, once they've answered and there's a conversation. `voice` fails a first message with an ask in it (`opener only`).

Never open cold with a line built from their bio. Build the context of the conversation from what they posted:

1. **Find one of their own recent tweets that's relevant** (an original post, not a reply or a repost), with treg's posts read for that handle.
2. **Forward it into the DM:** the tweet's link goes first, so X shows it as a card in the chat.
3. **Then one informal line:** "saw this", then what's true about how you're connected ("also saw we follow each other but never chatted", or "saw you followed me but we ain't chatted yet" when you don't follow them back; check with `twitterFollows`), then something brief and true about their tweet. Stop there: no ask.
4. **No usable original tweet:** use what else they've been posting or reposting lately (treg's posts read gives replies and reposts too), or that they reposted the owner. With nothing relevant to them at all, don't message them yet: a generic opener could go to anyone, and the gate fails it.

Never: "saw you're `<bio thing>`", their name, made-up camaraderie, or "thanks for following".

> `https://x.com/<them>/status/<id>` saw this and noticed we follow each other but haven't spoken
> 4249 live ads for one product is insane

> hey we follow each other and havent had a chat yet
> been seeing you share all the world model stuff genie 4 looked mad

## What to know

- A DM only lands if the person accepts DMs from accounts they don't follow. X answers otherwise, and the queue logs it and moves on.
- Some chats live in X's encrypted Chat. `twitterDms` reads them once the account's X Chat PIN is saved, and step 4 must include them: a person you already talk to in X Chat never gets a cold template. A send still goes out as an old-style DM, which shows in their X Chat too.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [All X use cases, and the parts they share](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md)
- [What log does on X](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/x.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

> Some links in this play carry ListeningKit's referral or affiliate credit (a `ref=` or `aff=` code). They cost the owner nothing extra; use the plain address without the code if you prefer.
