---
name: x-post
description: >-
  Write an X (Twitter) post from a raw idea using 21 proven hook formulas, in
  the user's own voice, counted the way X counts characters and humanized so it
  does not read as AI. Use whenever the user wants a tweet, an X post, a hook,
  "post about X", "turn this into a tweet", a long post for Premium, or asks for
  hook options. Produces three scored hooks, one full draft, and a copy-ready
  block that is never published without an explicit yes.
---

# x-post

Turns one raw idea into a post that sounds like the person who posted it.

Three files in this folder do real work:

```bash
python3 hookscore.py --hook "one line"     # five-property hook panel + formula name
python3 hookscore.py hooks.txt             # rank several options
python3 count.py post.txt                  # X's weighted count + six lints
python3 count.py post.txt --premium        # long post: shows where "Show more" cuts
```

`hooks.json` holds the 21 formulas: template, filled example, what each is
for, the way each usually gets ruined, and the regex that names it.

## Before you write

1. Read `~/.claude/x/voice.md` if it exists. That is the user's voice
   profile. If it does not exist, ask for **five of their own recent posts**,
   infer the voice, and write the file from `templates/voice.md`. Do not
   invent a voice. A post in the wrong voice is worse than no post.
2. Read `hooks.json`. All 21.
3. Read `~/.claude/x/swipe.md` if `/x-viral` has run. If a formula is
   over-indexing in the user's niche right now, prefer it when it fits.
4. If the idea is thin ("post about AI"), do not pad it. Ask one batched
   question: what happened, to whom, and what did it cost or return. A post
   needs one specific true thing.

## The shape of a post on X

On X the first line is not the start of the post. It is most of the post.

```
Line 1   the hook. Complete on its own. Under ~110 characters so it reads
         in one glance on a phone.
Line 2   the payoff of line 1, or the proof of it. Not setup for line 3.
Rest     only if it earns its place. Short lines. A blank line between ideas.
End      the last true sentence, or one specific question. Never both.
```

- **Standard account: 280 weighted characters.** `count.py` counts it the
  way X does: every link is 23, every emoji is 2, "…" is 2.
- **Premium long posts** go to 25,000, but the timeline shows about the first
  280 and hides the rest behind "Show more". Everything that matters goes
  above that fold. `count.py --premium` draws the fold for you.
- **Most of the posts that travel are one to three lines.** Use the length
  when the idea needs it, not because it is there.

## What X's ranker rewards

X publishes its current ranking weights. Run `python3 ../x-plan/weights.py`
for today's numbers. The shape has been stable even as the values move:
replies, quotes and shares (by DM or copied link) are weighted far above
likes, and "not interested", mute, block and report are weighted heavily
negative. X's own comment in that file warns these apply to predicted
probabilities, not to counts, so do not tell the user "a reply is worth ten
likes". Tell them what it means for the draft:

- Write the post someone replies to, quotes, or sends to one friend.
- Do not write the post that gets muted: bait, rage, or off-topic for the
  people who follow you.

## The loop

**1. Three hooks, from three different formulas.** Run the idea through
`hooks.json`, pick the three that genuinely fit, write one line each, then
score them together:

```bash
printf '%s\n' "hook one" "hook two" "hook three" | python3 hookscore.py -
```

Show the ranking. Say which you would ship and why, in one sentence. If the
top one is under 50, none of these is the hook. Write three more.

**2. Draft the full post** on the strongest hook.

**3. Count it.** `python3 count.py draft.txt`. Fix every FAIL. Read every
WARN out to the user with what you did about it.

**4. Humanize it.** Run the draft through `/x-human`. Every post from this
skill ships humanized.

**5. Print the block.** Copy-ready, in a fenced block, exactly as it should
be pasted. Then:

```
POST READY
hook:      #9 Time Anchor  (score 81 STRONG)
length:    187 / 280
humanizer: 3 artefacts stripped, human score 91 PASS
post at:   Tuesday 9:00am their time (from your plan)

Reply "yes" to log it, or tell me what to change.
```

**6. Never publish.** This skill writes text. The user posts it. On "yes",
append the post to `~/.claude/x/log.md` with the date, the hook formula and
the first line, so `/x-audit` has a history to work from.

## Rules that make the difference

- **One idea per post.** Two ideas is two posts. Say so.
- **Numbers over adjectives.** "$4,200" beats "a lot". If the user has not
  given you a number, ask. Never write around the hole.
- **No label as a hook.** "Hot take:", "Thread:", "Quick one" are packaging.
- **No reflex bait.** "Thoughts?", "Agree?", "RT if you agree" are dead. A
  closing question has to be one only this post could ask.
- **Hashtags: one, or none.** Elon Musk, Dec 2024: the system doesn't need
  them anymore. A hashtag is a link out of your own post.
- **Links.** X says it stopped down-ranking link posts over a year ago. An
  independent analysis in January 2026 still measured fewer views on them.
  Default: link in a reply under the post, and tell the user that is a
  choice, not a rule. `/x-audit` will show which is true for their account.
- **Mentions** past character 280 of a long post do not notify the person.
- **Never fabricate.** No invented metrics, clients, revenue or outcomes under
  the user's name, even as a placeholder. If a number is needed and unknown,
  leave `{{your number}}` in the draft and flag it.

## Example

```
/x-post I rebuilt my proposal process with Claude, 5 hours down to 20 minutes
```

```
HOOK RANKING
->  84.0 STRONG  I wasted two years hand-formatting proposals I should hav...
        #17 The Regret  ·  weakest: SPECIFICITY (75)
    81.4 STRONG  Writing a proposal used to take me 5 hours. It now takes ...
        #9 Time Anchor  ·  weakest: STAKES (70)
    66.2 OK      A $12,000 proposal writer vs a weekend with Claude. The w...
        #18 The Comparison  ·  weakest: ADDRESS (35)

Shipping #9 over #17. The scores are three points apart, which is noise, and #9's
numbers are the user's own. The scorer is a lint, not a judge.
```
