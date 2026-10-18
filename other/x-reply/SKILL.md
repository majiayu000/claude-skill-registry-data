---
name: x-reply
description: >-
  Handle the replies under the user's own X posts - sort every one, then draft
  answers in the order that matters. Use when the user pastes the replies on
  their post, says "reply to these", "handle my replies", "someone said X under
  my post", "how do I answer this", or is dealing with a critic, a troll or a
  lead in their mentions.
---

# x-reply

The reply section under your own post is where a post keeps going or stops.
X's published ranker weighs a predicted reply at ten times a predicted like,
and adds a boost on top when the two people follow each other (run
`python3 ../x-plan/weights.py` for today's values). A thread with the author
in it keeps getting served. A post the author abandoned does not.

But the value is not equal across replies, so this skill sorts before it
writes.

## Input

The user pastes the replies, ideally with handles. Screenshots are fine. Do
not scrape the thread with a browser tool.

## Triage first

Sort every reply into one bucket and say the counts out loud:

| bucket | what it is | what it gets |
| --- | --- | --- |
| **LEAD** | someone describing the problem you solve | a real answer, then one sentence of open door |
| **SUBSTANCE** | adds data, disagrees, extends | the best reply on the thread |
| **PEER** | an account worth being seen next to | a reply that gives them something back |
| **QUESTION** | asks how, what, which | the answer, in the reply, not "DM me" |
| **SUPPORT** | "great post", an emoji, a tag | a like. A short reply to the first few at most |
| **NOISE** | spam, bots, bait, bad faith | nothing |

Write in that order and stop when the value stops.

## How to reply

- **Inside the first hour.** That is when replying does the most for the post.
- **Answer the actual question in the reply.** Sending people to your DMs for
  an answer they could have had in public is how a thread dies.
- **Match their length.** A one-line reply does not get six lines back.
- **To a critic:** concede the true part first, in their words, then hold the
  line on the part you believe. Once. Never twice on the same thread.
- **To a lead:** answer fully in public. The open door is one sentence, an
  offer of help, not a pitch. Public value is what makes the next person DM.
- **To bait, a bot, or a pile-on:** nothing. A reply gives it reach.
  If it is abusive, hide the reply, mute, or block, in that order of force.
- **Never quote-post a reply to dunk on it.** That is a second post with
  their name in it, and mutes are weighted heavily against you.

## Output

One block, grouped by bucket, each reply copy-ready and already through
`/x-human`:

```
REPLIES  ·  23 replies  ·  2 LEAD, 3 SUBSTANCE, 2 PEER, 4 QUESTION, 9 SUPPORT, 3 NOISE

LEAD
@sarahbuilds  "we have the same problem with onboarding"
> The fix for us was deleting the welcome call and sending a 4-minute Loom
> instead. Completion went up, not down. Happy to send the script.

QUESTION
@devon_k  "which model did you use for this?"
> Claude, with the skill file doing most of the work. The model mattered
> less than the file.

SUPPORT  (like these; reply to the first three)
...

NOISE  (3)
Skipped: two bots and a reply-guy account farming. Replying gives them reach.
```

Then the gate: **nothing is posted until the user says yes**, and then the
user posts each reply by hand. X's automation rules only allow automated
replies to people who opted in, and this is not that.
