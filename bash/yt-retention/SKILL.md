---
name: yt-retention
description: >-
  Read a YouTube Studio audience-retention export, find the moments viewers
  leave, and name the one change to make. Use for "why do people stop
  watching", "my retention is bad", a retention chart or CSV, or "fix my
  pacing".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/retention.py *)
---

# yt-retention

The retention graph is the most honest feedback a video gets, and most creators never download it.

```bash
python3 ${CLAUDE_SKILL_DIR}/retention.py retention.csv --duration 600
python3 ${CLAUDE_SKILL_DIR}/retention.py retention.csv --duration 600 --transcript transcript.srt
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.
The transcript reader is `../yt-edit/deadair.py`, so install the two together.

**Getting the file:** Studio → the video → Analytics → Engagement → the audience-retention chart →
the download icon → "Audience retention".

**What it reads:** two columns - a position and the share still watching. The position can be
seconds, `m:ss`, a percent of the video, or a 0-1 ratio as the Analytics API gives it. The header
decides when it names the unit; otherwise anything up to 100 is read as percent. **If the position
is a percent, always pass `--duration`** (the length in seconds) - without it the drops have no
timestamps and the transcript cannot tell you what was being said. Ask for the length; do not guess.

## Three different problems

- **The opening loss**: what goes in the first 30 seconds. Under 25% is healthy. When it is the
  problem, the fix is always the first fifteen seconds of script, not the edit.
- **Cliffs**: single steep drops, a specific moment - a topic change with no signal, a sponsor
  segment, a long setup. With the transcript, the tool prints what was said there, which is what
  makes the report useful instead of merely interesting.
- **The slide**: the steady loss across the middle. That is pacing, and the fix is cutting, not
  rewriting.

## What to hand back

The biggest problem and one change for it - not five. More only if asked. If the opening is healthy
and the slide is flat, say the video is fine and the issue is packaging, and point to `/yt-package`.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
