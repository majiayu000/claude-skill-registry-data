---
name: x-comment
description: >-
  Write replies on other people's X posts and threads that read as a person
  with something to add, not a reply guy. Use when the user pastes a post and
  wants a reply, says "reply to this", "comment on this thread", "engage with
  this", "what do I say here", "quote tweet this", or wants a batch of replies
  for their daily engagement round.
---

# x-comment

On X, replying to other people is how small accounts grow. A good reply under
a post with 300,000 views is seen by more people than most of your own posts,
and the people reading it already care about the topic. A bad one is seen by
the same people, which is the problem.

## Input

The user pastes the post (and the author's handle and what they do, if they
have it). Screenshots are fine. If they give a URL you cannot open, ask them
to paste the text. Do not guess what a post said, and do not use a browser to
scrape anyone's timeline.

## Reply or quote

Decide first, and say which:

- **Reply** when you are adding to their conversation. Your reply lives in
  their thread, in front of their audience.
- **Quote** when you have a take for your own audience that needs their post
  as the context. A quote is your post. It needs to stand on its own.
- **Never quote to dunk on a smaller account.** It reads exactly the way it
  is, and a mute is weighted heavily against you in X's own ranker.

## The nine reply types

Pick by what the post actually is. Never default to type 1.

| # | type | when | shape |
| --- | --- | --- | --- |
| 1 | **Add a datum** | a claim you can support with a number | "Same here: 40% of our..." |
| 2 | **Add the missing case** | right, but incomplete | "Holds until {condition}. Then..." |
| 3 | **Respectful disagree** | you think it is wrong | the agreement first, then the fork |
| 4 | **Extend one line** | one sentence in the post is the good one | build on that sentence |
| 5 | **Ask the real question** | the post skipped the hard part | one question, specific |
| 6 | **The receipt** | you have done the thing | what happened, in two sentences |
| 7 | **The correction** | a factual error | be right, be brief, be kind, be sure |
| 8 | **The reframe** | right facts, wrong frame | "Another way to read this:" |
| 9 | **The one-liner** | the post needs nothing, you want presence | under 12 words, funny or true |

## Rules

- **One to three sentences.** Most good replies are under 200 characters.
- **Never open with** "Great post", "This 👆", "So true", "Facts", "💯",
  "Bookmarked", "Couldn't agree more", or the author's name and an
  exclamation mark. All invisible.
- **Never restate the post.**
- **Say the specific thing.** If the reply could sit under any post on the
  topic, it is noise.
- **Early beats clever.** A reply in the first 15 minutes of a big account's
  post is seen. A better one two hours later is not. That is why this skill
  batches.
- **Replies between people who follow each other get a boost** in X's
  published ranker (run `python3 ../x-plan/weights.py`). Peers matter.
- **Premium replies are ranked higher.** X says so and calls the effect
  "slight". Mention it only if the user asks; it is a purchase decision, not
  advice.

## Output

**Two options of different types**, labelled, plus one line on which to post.
Both through `/x-human` first: a reply with an em dash is more obviously
machine-written than a post, because replies are short and read closely.

```
REPLY OPTIONS  (on @author's post about pricing)

[6 · Receipt]
We raised prices 40% in March and lost 2 of 31 clients. The two we lost
were the two we argued with most.

[5 · Real question]
What happened to churn on the annual plans? That is where it bit us.

Post the receipt. It is your own number and it concedes a cost, which is
what people reply to.
```

## Batch mode

For an engagement round, ask for 5 to 15 posts pasted in one message and
return one reply each, in one block. Keep a running note in
`~/.claude/x/log.md` of who the user replied to this week. Replying to the
same three people every day is visible, and it looks like what it is.

## Never

Do not post the reply. Do not drive a browser to publish it. X's automation
rules prohibit automated replies and mentions, including replies triggered by
keyword searches, and AI reply bots need X's written approval. This skill
writes the reply. The user posts it by hand.
