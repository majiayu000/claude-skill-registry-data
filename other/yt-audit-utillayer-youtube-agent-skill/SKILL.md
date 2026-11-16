---
name: yt-audit
description: >-
  Review a whole YouTube channel - packaging, consistency, openings, rhythm -
  and end with the single fix that matters most. Use for "audit my channel",
  "why isn't my channel growing", "review my videos", or a pasted channel link.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../yt-package/title.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/../yt-script/hookscore.py *)
---

# yt-audit

A list of twenty problems is a way to avoid the one that matters. This review ends with **one** fix.

## Before you start

1. Read `~/.claude/youtube/voice.md` if it exists. If not, ask for three of the creator's videos
   and write it.
2. Never make up a number. Use the channel's figures or none.

## What to look at, in order

1. **The last ten titles, as a list** - the way the channel page shows them. Do they promise
   different things? Lint them with `${CLAUDE_SKILL_DIR}/../yt-package/title.py`. When every title has
   the same shape, the problem is the format, not the titles.
2. **The thumbnails, at feed size.** Shrink them. What still reads? If three are unreadable small,
   that is the fix and nothing else matters yet.
3. **The first fifteen seconds of the last three videos.** Transcribe them and score them with
   `${CLAUDE_SKILL_DIR}/../yt-script/hookscore.py`. This is where most channels lose people.
4. **Upload rhythm.** Consistency, not frequency. Six videos in a week and then a silent month does
   more harm than one every fortnight forever.
5. **Retention**, if they can export it: `/yt-retention`.

## What to hand back

- The single biggest fix, named, with what to do about it this week.
- Three things that already work, so they are not broken by accident. Specific: "your energy is
  good" is not an observation.
- What not to do yet, and why.

No praise you do not mean at the start, no twenty-item list at the end.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
