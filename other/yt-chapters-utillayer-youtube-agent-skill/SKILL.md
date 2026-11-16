---
name: yt-chapters
description: >-
  Draft YouTube chapters from a transcript and check them against YouTube's
  rules so they actually appear. Use for "add chapters", "timestamps",
  "split this video into sections".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/chapters.py *)
---

# yt-chapters

```bash
python3 ${CLAUDE_SKILL_DIR}/chapters.py transcript.srt --target 8
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.
It reads transcripts with `../yt-edit/deadair.py`, so install the two together.

To fetch a video's own captions:

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o transcript "<video url>"
```

## Before you start

Read `~/.claude/youtube/voice.md` if it exists: chapter titles are the creator's words, not yours.
Without it, title plainly and mention that the voice file would sharpen them.

## YouTube's rules

A list that breaks any of these silently is not shown as chapters at all:

- the first timestamp is **00:00**
- at least **three** chapters
- each at least **ten seconds** long
- in **ascending** order

The tool checks all four and says so when a list fails. Some channels must also enable advanced
features in Studio before chapters appear; if a valid list does not show, check that first.

## Retitle every line

`chapters.py` is good at boundaries - it scores the pauses taken and how much the vocabulary changes
across them. Its titles are just the topic words. Rewrite each as the promise of that section, in
three to five words, in the creator's voice.

A section you cannot name in five words is two sections, or filler. That is worth telling the
creator too.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
