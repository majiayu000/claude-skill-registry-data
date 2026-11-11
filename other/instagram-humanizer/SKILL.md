---
name: instagram-humanizer
description: >-
  Humanize AI-written Instagram captions, Reel scripts, comments and DMs: strips
  em dashes, AI slop words ("delve", "game-changer", "in today's video"),
  invisible watermark characters and stock Instagram phrases, then scores the
  text on a five-check AI-detection panel and reports the before/after. Use
  when the user says "humanize", "does this sound like AI", "remove em dashes",
  "de-slop this", "make it sound human", "this sounds like ChatGPT", and before
  any caption, script, comment or DM from this pack is shown to the user.
---

# Instagram humanizer

Two tools, both run locally. Use them; do not eyeball it.

```bash
python3 scripts/humanize.py draft.txt --report -o clean.txt   # clean it (writes -o, else stdout)
python3 scripts/detect.py draft.txt                # score it, five checks
python3 scripts/detect.py before.txt after.txt     # prove the delta
```

Both read `references/slop.json`: 154 stock words and phrases with plain
replacements, 18 invisible character classes, typographic substitutions and
16 structural tells, the last block Instagram-specific ("stop scrolling",
"follow for more", "tag someone who needs this", "the algorithm loves").
Edit it: if the user always says a word the lexicon strips, remove it.

## Fixed automatically

1. **Invisible characters**: zero-width spaces/joiners, word joiners, soft
   hyphens, BOMs, Unicode tags, non-breaking spaces.
2. **Typography**: em dash to comma, curly quotes to straight, ellipsis to
   three dots; orphaned punctuation cleaned (including the `.!` a deleted
   closer leaves).
3. **The lexicon**: delve, leverage, seamless, game-changer, in today's video...

## Flagged for a human rewrite (shape needs judgement)

"It's not just X, it's Y"; rule-of-three lists; the video preamble; emoji
bullet lists; three shouted words; hashtag walls; reflex follow-bait; every
sentence the same length. Rewrite these yourself, then re-run.

## The panel

BURSTINESS (sentence-length variety), SPECIFICITY (numbers, names, concrete
nouns per 100 words), SLOP DENSITY, FINGERPRINT (dashes, invisible chars,
curly quotes), VOICE (contractions, pronouns, structural tells). PASS = overall
70+ AND every check 55+. For short texts (under ~200 characters: bios, hooks,
one-line comments) the panel is noisy: score all variants together in one
file, or use only the FINGERPRINT and SLOP checks as the gate.
The weakest check is the one to fix first; usually SPECIFICITY, and the fix is
a real number or name from the user, never an invented one.

## Honest limits

Local heuristics modelled on the signals public detectors use. Not GPTZero,
Originality or Turnitin, no API calls, no promise of "undetectable". It makes
text read like a person wrote it, which is the actual goal on Instagram:
captions get read, and scripts get said out loud.

## When the tools disagree

Readability and SEO beat the panel. If raising BURSTINESS makes `beats.py`
flag long beats, or a rewrite drops the keyword, keep the script timing and
the keyword and accept a REVIEW on the panel; say so in one line.

## Order of operations in this pack

writer skill -> humanize.py -> rewrite flagged shapes -> detect.py (70+) ->
seo_caption.py lint (humanizing must not delete the keyword: re-check) -> show.

Credit: adapted from instagram-agent-skill by Jake Schincariol (MIT), with a
punctuation fix. See `NOTICE`.
