---
name: yt-package
description: >-
  Write and test a video's title and thumbnail together, linted for truncation,
  repetition and vague words before it goes live. Use for "title ideas", "what
  should I call this", "thumbnail text", "my click-through is low", packaging,
  or renaming a video that already exists.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/title.py *)
---

# yt-package

A viewer sees the title and the thumbnail in the same glance, so write them as one thing. The
commonest waste is a thumbnail that repeats the title: two surfaces, one message.

```bash
python3 ${CLAUDE_SKILL_DIR}/title.py --title "..." --thumb "THREE WORDS"
python3 ${CLAUDE_SKILL_DIR}/title.py titles.txt --thumb "THREE WORDS"    # one per line, ranked
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.

## Before you start

1. Read `~/.claude/youtube/voice.md` if it exists. If not, ask for three of the creator's videos
   and write it. The title should sound like the person in the video.
2. Never make up a number. "Doubled" needs the before and after.

## What the linter checks, and why

- **Length.** About 60 characters survives desktop search and about 40 a phone feed. YouTube does
  not publish either number - truncation is by pixel width - so treat them as the safe side, not a
  law. A desktop cut loses the end; a phone cut can lose the subject. The hard limit is 100, and
  `<` `>` are not allowed.
- **Repetition.** The thumbnail says what the title does not.
- **Thumbnail words.** Three at most. A fourth turns to mush at feed size.
- **Something concrete.** A number, a name or a date beats any adjective.
- **Capitals.** Two all-caps words is the limit before it reads as shouting.

## The method

1. Write ten titles. Lint them all. Show the best three with their scores and the one issue each has.
2. For the winner, write the thumbnail: the single image, the expression, at most three words, and
   how the background keeps contrast at feed size.
3. If the top two are close, say so and suggest Studio's A/B test (up to three titles or
   thumbnails, judged by watch time share; desktop Studio only, not for Shorts) instead of
   pretending the linter can tell them apart. The score is a lint, not a forecast.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
