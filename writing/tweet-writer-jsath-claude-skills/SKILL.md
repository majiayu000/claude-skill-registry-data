---
name: tweet-writer
description: "Writes X (Twitter) posts and threads in the user's own voice, learned from 5 to 10 of their best posts, using format rules measured on real post data: numbered tutorials and copy-paste config tips beat stories, numbered lists beat arrow lists, link cards die. Use when someone asks for a tweet, a thread, tweet ideas, or to turn a demo, lesson or result into an X post. Drafts only; never posts."
---

# Tweet Writer

Writes posts that sound like you and use the formats that actually get read and saved on X.

By Johann (@johannships). The format rules come from pulling and ranking 100 of my own posts by views, likes and bookmarks, then re-checking against newer posts. They held across months.

## Step 0: learn the voice (first run, then reuse)

Ask the user to paste **5 to 10 of their own top posts** (highest views or bookmarks; X Analytics or the post itself shows them). Then write a short `voice.md` next to this file with:
- capitalisation habit (all lowercase? sentence case?)
- typical line length and whitespace pattern
- words and shorthand they use (e.g. "&", "gonna", "tbh") and words they never use
- emoji and hashtag habit (count them, do not guess)
- how they open and how they close

Show `voice.md` to the user once and fix anything they correct. On later runs, read it instead of asking again. If they will not share posts, use the default voice at the bottom and say so.

## Inputs

- Topic, result, demo or lesson (required). Real numbers if they have them.
- Format: single (default), thread, or ideas.
- Optional: their own draft, hook or CTA. **Anything they supply is locked**: keep their hook word for word, keep their bullet structure and CTA. Shorten inside those parts before cutting any of them.

## Formats ranked by measured performance

| Rank | Format | What it looked like in the data |
|---|---|---|
| 1 | Numbered step-by-step tutorial with an insider hook ("the full X setup nobody explains:") | Every top post in the sample was one of these two formats |
| 1 | Copy-paste config tip + before/after ("X tip most people miss:" then the exact snippet) | Bookmarks ran about 2x likes. Re-posting variations kept working; the format did not fatigue |
| 2 | Numbered process ("i automated my X:" then 1 to 10) | Solid |
| 3 | Contrarian "stop doing X" + the fix | Solid |
| 4 | Bullet list of use cases | Decent |
| 5 | Arrow (->) list | About 4x worse than the same content as a numbered list |
| 6 | Pure story with no structure | Weak |
| 7 | Link cards, product announcements, landing-page screenshots | Dead last every time |

Rules that follow from it:
- **Bookmarks are the metric.** Write things people save: exact steps, a config, a checklist.
- **Always numbered lists, never arrows.**
- **A story works only with structure**: a real scenario, then a numbered list of what happened, then a one-line reframe.
- **Never lead with the product.** Show the thing working, not the landing page.
- Fear or money hooks work when the list delivers ("your X setup can be hacked in 5 minutes. 10 things to lock it down:").

## Voice defaults (overridden by voice.md)

- Whitespace is mandatory: one thought per block, blank line between blocks, blank line between numbered items.
- Real numbers over vague ones ("208 hours in calls", not "lots of calls"). Only numbers the user gave you.
- Get to the point. No "here's what i learned about X" setup.
- Observations over advice ("i noticed X" beats "you should do X").
- Never: em dashes, "delve", "leverage", "utilize", "it's worth noting", "thread 🧵", rocket or lightbulb emojis, more than one hashtag.

Correct:
```
unpopular opinion: the best software companies will be run by 1 person

with agents doing everything else

we're already here
```
Wrong (same words, no air):
```
unpopular opinion: the best software companies will be run by 1 person with agents doing everything else. we're already here.
```

## Shapes

Tutorial:
```
the full [thing] setup nobody explains:

1. [step]

2. [step]

3. [step]

[one-line payoff]
```

Demo caption ("i built..."):
```
i built [thing] that [does job]

you tell it "[plain-English instruction]"

then it:
- [mechanism 1]
- [mechanism 2]
- [mechanism 3]

[one real use line]

[simple reply CTA]
```
No grand lesson, no slogan stack at the end.

Thread: tweet 1 is the hook (never "a thread on..."), one point per tweet, last tweet is the payoff or a soft CTA. Each tweet under 270 characters.

## Output rules

- Return only the post text, ready to paste. No labels or rationale unless asked.
- "give me the tweet" or "just the tweet" = exactly one post.
- Ideas mode = 5 to 10 options, each a different format or angle, not rewrites of one thesis.
- Count characters mechanically (whitespace, bullets and emoji included). Single post: under 280 unless the user has X Premium and asks for long-form. Never claim a long post fits 280.
- Long-form asked for ("a bit more detail", "like I'm talking"): keep experience, what changed, takeaway in spoken sentences with spacing. Do not compress the story into slogans to hit 280.

## When something is missing

- No numbers: write it without them. Never invent views, revenue, users or time saved.
- No voice samples: use the defaults, label the draft "default voice".
- User says it sounds like AI: simplify. Fewer staged one-liners, fewer contrasts, plainer words. Do not add fake casualness ("lol").

## Feedback log

When the user rejects or edits a draft, or shares how a post performed, append a line to `feedback.md` (date, post format, result or correction, rule going forward). Read it before writing.
