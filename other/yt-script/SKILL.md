---
name: yt-script
description: >-
  Turn a video idea into a script meant to be spoken: five hooks scored against
  21 formulas, the best opening kept, then the narration paragraph by paragraph
  with what is on screen, checked before anyone records. Use for "write my
  script", "write my next video", "I need a hook", "how should I open this",
  "what do I say", or any time someone is about to record without a first line.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/hookscore.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scriptcheck.py *)
---

# yt-script

The script is the video. Everything after it - voice, edit, thumbnail - can only lose what the
words did not earn. Two tools here keep the writing honest:

```bash
python3 ${CLAUDE_SKILL_DIR}/hookscore.py hooks.txt       # score and rank opening lines
python3 ${CLAUDE_SKILL_DIR}/scriptcheck.py script.json   # is it ready to be spoken?
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.

## Before you start

1. Read `~/.claude/youtube/voice.md` if it exists: who the viewer is, how the creator talks, the
   words they never use, the claims they will not make. If it is missing, ask for three of their
   videos, work out the voice, and write the file. Words in someone else's voice cannot be read
   aloud convincingly.
2. If the video retells a book, a record or history, run `/yt-research` first and write from its
   brief. Nothing goes in the script that is not in the brief.
3. Never make up a number, a result or a quote. If a line needs a figure you do not have, ask for
   it or cut the figure.

## The opening

The first fifteen seconds decide the video. They must keep the title's promise, open a question the
viewer cannot answer yet, and show the answer is coming.

Write **five** openings against [the 21 formulas](hooks.json), score them with `hookscore.py`, and
show the best two with their scores. Pick the more accurate one if they are close: a hook the video
does not deliver is worse than a weaker one it does. No channel intro, no "before we start", no
subscribe request - those are where the early drop comes from.

## The body

- **One idea per paragraph**, 30-75 words: one breath for a person, one take for a voice model.
- **Written for the ear.** Short sentences. Numbers as words. No dashes, brackets, semicolons or
  double quotes - they trip narrators and break captions.
- **Write pictures.** Every paragraph gives the screen something to show: a place, an action, a
  face. Mark it: `[ON SCREEN: ...]`. A paragraph that is only an idea becomes a slideshow.
- **Turn at the middle.** Around 45% in, a question or a reversal that resets attention. Retention
  graphs sag there; give them a reason not to.
- **Pay off the opening**, explicitly, and say you are doing it.
- **Close with one line.** One ask at most.

## The check

Put the narration in `script.json` - `{"title", "names", "text", "sources"}`, paragraphs separated by
blank lines, every proper name in `names` - and run `scriptcheck.py`. Fix every error before
recording; read every warning. For a sourced video, the independent fact check in `/yt-research`
comes next.

## What to hand back

- the two best openings with their scores, and which formula each uses
- the script, paragraph by paragraph, with `[ON SCREEN: ...]`
- the `scriptcheck.py` result
- the runtime at about 150 words a minute

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
