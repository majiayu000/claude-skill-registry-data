---
name: instagram-reel-script-generator
description: >-
  Instagram Reel script generator: turns one idea into a script someone
  finishes - 3 hooks from 26 tested formulas scored by a hook scorer, the
  spoken script, the on-screen text, and a timed beat sheet checked for a slow
  hook and dead beats. Use when the user wants a Reel script, a short-form
  video script, hooks, a voiceover, "write a reel about X", "what do I say in
  this video", "give me hooks", or is about to record without a first line.
  Pulls the user's best past hooks and outlier transcripts from the IShort MCP
  (search_my_scripts, list_my_scripts) when connected.
---

# Instagram Reel script generator

One raw idea in, a scored, timed, shootable Reel script out.

```bash
python3 scripts/hookscore.py hooks.txt              # rank hook options (one per line)
python3 scripts/hookscore.py --hook "one line"      # score one
python3 scripts/beats.py script.txt --target 30     # timed beat sheet
```

## Before writing

1. **Voice.** Read `~/.instagram-claude-skills/brand-voice.md`. If missing, get
   three of the user's own reels (IShort: `list_my_scripts` filtered to their
   handle, or paste) and write the file from `templates/brand-voice.md`. They
   have to say this out loud; the wrong voice is unusable.
2. **Evidence.** If `~/.instagram-claude-skills/swipe.md` exists (written by
   `instagram-reels-research`), its formulas beat the defaults. With IShort,
   `search_my_scripts("<topic>")` shows how outliers on this topic opened.
3. **One true specific thing.** If the idea is thin, ask one batched question:
   what happened, to whom, what did it cost or return. Don't pad.

## The shape

```
0:00-0:02  HOOK     the claim. Spoken line and on-screen line written SEPARATELY.
                    Motion or a change in the first frame.
0:02-0:07  STAKE    why the viewer should care. One line.
0:07-...   BODY     one idea per beat; change the frame every beat.
LAST 3s    PAYOFF   deliver what the hook promised, then the single ask.
LAST LINE  LOOP     echo a word from the hook so the replay lands.
```

Default 20-40 seconds. Long is earned, not assumed.

## Hooks

Read `references/hooks.json` (26 formulas: template, example, on-screen
version, when to use, how it gets ruined). Write **3 hooks from 3 different
formulas**, run `hookscore.py`, and lead with the top one.

Be honest about the scorer: it reliably catches bad hooks (greetings,
preambles, nothing concrete, too long, "stop scrolling", emoji) and it does
**not** pick winners between two decent hooks. Dealbreakers cap a hook at 45.
If the top hook is under 50, none of them is the hook; write more.

## On-screen text

A separate script: max 6 words per card, read before it is heard. The first
card carries the topic keyword (it is indexed by Instagram and Google). Burn in
captions for the body; most people start muted.

## Check the timing

Run `beats.py --target <seconds>`. Fix every flag: hook past 3s, any beat over
4s on one frame, three beats with nothing concrete, no loop. Re-run until clean.

## Output

```
REEL READY
hook: #<id> <formula>, scored <n> <verdict>   (alternatives: <n>, <n>)
length: <s>s across <n> beats
[spoken script, fenced]
[on-screen cards with timings]
[shot list: what is on screen per beat]
next: instagram-seo-caption-generator --script <this script>
```

Run `instagram-humanizer` on the spoken script before showing it.

## Rules

- No invented numbers, clients or results: `{{your number}}` + a flag.
- One idea per Reel. Two ideas, two Reels.
- Never open on a greeting, "in this video", or "stop scrolling".
- You write, they shoot and post.

Credit: hook formulas, `hookscore.py` and `beats.py` adapted from
instagram-agent-skill by Jake Schincariol (MIT). See `NOTICE`.
