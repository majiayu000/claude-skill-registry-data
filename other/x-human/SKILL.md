---
name: x-human
description: >-
  Strip the machine fingerprint out of any draft - em dashes, AI slop words,
  invisible watermark characters, thread boilerplate - and score it against a
  five-check detection panel before it goes out. Use whenever text needs to
  sound human, when the user says humanize, "does this sound like AI", "remove
  the em dashes", "de-slop this", "this sounds like ChatGPT", or before any
  post, thread, reply or DM from this pack is shown to the user.
---

# x-human

Two tools live in this folder and they both actually run. Use them. Do not
eyeball this.

```bash
python3 humanize.py draft.txt --report        # clean it, show what changed
python3 detect.py draft.txt                    # score it, five checks
python3 detect.py before.txt after.txt         # prove the delta
```

Both read `slop.json`: 176 stock words and phrases with plain-English
replacements, 18 invisible character classes, 11 typographic substitutions and
18 structural tells. The last block of each list is X-specific: thread
boilerplate ("if you found this thread helpful"), repost bait ("RT if you
agree", "like and repost") and the "A thread 🧵" hook. It is meant to be
edited. If the user has a word they always use that the lexicon strips, take
it out of the file.

## Why this matters more on X than it looks

A post is 280 characters. One em dash in a two-line post is a far larger share
of the text than the same dash in an essay, and people on X have spent three
years learning to spot the shape. The tell is not a detector flagging the
post. The tell is a reply that says "chatgpt ahh post", and it sits under your
post for everyone to read.

## What gets fixed automatically

**1. Invisible characters.** Zero-width spaces and joiners, word joiners, soft
hyphens, byte-order marks, Unicode tag characters, invisible separators,
non-breaking and narrow spaces. A keyboard does not produce these. They survive
copy-paste and they are invisible in every editor. `humanize.py` deletes every
one, including any remaining Unicode format character it does not have a name
for.

**Except inside emoji.** X is full of them, and two invisible characters are
load-bearing there: the joiner that makes 👨‍💻 one glyph instead of 👨💻, and
the tag characters that spell the England, Scotland and Wales flags. Those are
kept. A joiner or a tag anywhere else is still deleted, and `detect.py` does
not count the kept ones against you.

**2. Typography.** Em dash to comma, en dash to hyphen, curly quotes to
straight, ellipsis to three dots, bullet character to hyphen. The em dash pass
is the one that matters.

**3. The slop lexicon.** delve, leverage, robust, seamless, game-changer,
"let that sink in", "read that again", plus the X block. Each swapped for a
plain word or deleted, with capitalisation preserved and URLs left untouched.

## What does NOT get fixed automatically

Structural tells get **flagged, not rewritten**, because changing the shape of
a sentence needs judgement:

- "It's not just X, it's Y" and "not only X but also Y"
- Rule-of-three triads
- One-word rhetorical question lines: "The result?"
- "A thread 🧵" as the hook, and the stock thread closer
- The preamble: "in this thread I'm going to show you"
- Two lines in a row that open on an emoji
- Three or more shouted words in a row
- Three or more hashtags
- Reflex bait: "RT if you agree", "follow for more", "Thoughts?"

That list is your job. Rewrite each flagged line by hand, keeping the meaning,
then re-run `detect.py`.

## The five checks

`detect.py` scores five signals 0-100, higher is more human:

| check | what it measures | machine looks like |
| --- | --- | --- |
| BURSTINESS | sentence-length variation | every sentence the same length |
| SPECIFICITY | numbers, names, concrete markers per 100 words | abstract nouns, no figures |
| SLOP DENSITY | lexicon hits per 100 words | stock vocabulary |
| FINGERPRINT | invisible chars, em dashes, ellipses per 1k chars | typographically perfect |
| VOICE | contractions, person, structural tells | no contractions, staged reveals |

The verdict weights the mean at 60% and the **weakest single check** at 40%,
because one signal is enough. PASS needs 70+ overall with no check below 55.

**Short posts are scored on what a short post can show.** Burstiness needs four
sentences and specificity needs about 25 words, so under that they print n/a
and sit out rather than count as a neutral 50. Voice drops to its
structural-tell half. The output says "scored on 3 of 5 checks" when that
happens, so nobody mistakes it for the full panel.

**Curly quotes count a quarter.** iOS types them by default and most posts
are written on a phone, so on their own they say very little. They are still
straightened.

## Say this honestly

These are five local heuristics modelled on the signals public detectors key
on. They run entirely on the user's machine and nothing is uploaded. They are
**not** GPTZero, Originality, Copyleaks, Winston or Turnitin, they do not call
those APIs, and they cannot promise those verdicts. Do not make a bigger claim
on the user's behalf, and do not tell a user their text is undetectable.

## Order of operations

1. `humanize.py draft.txt -o clean.txt --report`
2. Read the structural flags. Rewrite those lines yourself.
3. `detect.py draft.txt clean.txt` to show the before and after.
4. If the verdict is not PASS, fix the weakest check named in the output and
   go again. Two rounds is normal. Five means the draft was written by
   formula, and the fix is a different draft.
5. Show the user the cleaned text and the score. Never the score alone.
