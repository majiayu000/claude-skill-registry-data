---
name: log-twitter-topic-replies
description: "Replying to everyone posting about one topic. A log play (docs/useCases/twitter/topicReplies.md): Pick a topic you have something real to say about, find everyone on X posting about it, and reply to each person with one line about their own post, backed by one of your own facts. Each reply can point at your article or video on the topic. The owner approves the list, then the queue sends it over days, inside the account's 240 writes a day ([write budgets](../../specs/writeBudgets.md))."
when_to_use: "Use when the owner asks for this, in words like: \"reply to everyone tweeting about <topic>\", \"find everyone posting about <topic> on x and reply with my article\", \"reply to the people talking about <topic> with my video\"."
metadata:
  summary: "Replying to everyone posting about one topic"
---

# Replying to everyone posting about one topic

This is the log play `twitter/topicReplies`. Before anything else, call the log MCP tool `getGuide({ useCase: "twitter/topicReplies" })`: it returns this page and makes it the session's play, so every log tool's answer says which step you are on and a send with no play loaded is refused (rules 157, 158). Then follow the steps in order.

Draft every message from that person's own thread and the owner's real replies (`voice` with no text, `search`), never from memory, and never send two that read alike (`sameAsSent`).

Pick a topic you have something real to say about, find everyone on X posting about it, and reply to each person with one line about their own post, backed by one of your own facts. Each reply can point at your article or video on the topic. The owner approves the list, then the queue sends it over days, inside the account's 240 writes a day ([write budgets](https://github.com/matthewdonsemail-lab/log/blob/main/docs/specs/writeBudgets.md)).

How the owner asks for it: "reply to everyone tweeting about <topic>", "find everyone posting about <topic> on x and reply with my article", "reply to the people talking about <topic> with my video".

## Run it from a fresh context

Say: **"go on docs/useCases/twitter/topicReplies.md for <topic>, linking <article or video url>"**. The agent then:

1. Reads this page and [README.md](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md).
2. Gets the owner's facts on the topic from their own posts, article or video. Every number in a reply has to come from there.
3. Runs the steps below and shows the full list with the copy for the owner's yes.

## The steps


| # | Step | Tool | Done when |
| --- | --- | --- | --- |
| 0 | Session check | `twitterSessionCheck` | `loggedIn` |
| 1 | Find the posts: the topic's words, latest first, original posts and replies with a real take | [treg](https://treg.to/?ref=matthewdonse-aebsh)'s X post search | a pool of posts, newest first |
| 2 | One post per person, only from people with 1500 followers or fewer (bigger accounts aren't worth it yet; people in the owner's network first). Drop anyone the account already replied to, and accounts that only repost news | the network's `followers` (in the Relate graph),  treg's posts read on the account, for its past replies | a unique list, everyone at 1500 followers or under |
| 3 | For each post, a one-line summary of what they said, and a reply that answers it with one of your facts. Mark which link it carries (article or video) | house style | every line passes `twitterQueueCheck` |
| 4 | Write the list somewhere the owner can read it on a phone: number, handle, link type, post url, "they said", the reply | a shared page | the owner says yes |
| 5 | Queue it: each target carries its own `text`, build, check, approve, plan, run live. Plan only what fits today's limit (`limit`), and plan the rest on later days | README queue steps: `twitterQueueBuild`, `twitterQueuePlan` { limit }, `twitterQueueRunLive` | the queue's `pending` reaches 0 |

## What one item looks like

> they said: thinks it's a get rich quick scheme
>
> theres a course crowd on it for sure but the buyers are real and here's what one actually pays `<your fact>`

## What the runs taught

- **Check past replies before approving.** One run replied to someone the account had already answered several times; that's where the one-reply-per-person rule came from.
- **Big lists take days.** At 240 writes a day, a list of a hundred and more is planned day by day with `limit`.

## Next

- [#37](https://github.com/matthewdonsemail-lab/log/issues/37) spreads a long list over several days. Until then, the queue plans up to its limit and is planned again each day.

## Related

- Up: [All use cases](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/README.md)
- [All X use cases, and the parts they share](https://github.com/matthewdonsemail-lab/log/blob/main/docs/useCases/twitter/README.md)
- [What log does on X](https://github.com/matthewdonsemail-lab/log/blob/main/docs/platformGuides/x.md)
- [Connect your agent](https://github.com/matthewdonsemail-lab/log/blob/main/docs/mcp.md) · [Trust](https://github.com/matthewdonsemail-lab/log/blob/main/docs/trust.md)

> Some links in this play carry ListeningKit's referral or affiliate credit (a `ref=` or `aff=` code). They cost the owner nothing extra; use the plain address without the code if you prefer.
