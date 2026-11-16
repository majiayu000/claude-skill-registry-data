---
name: yt-shorts
description: >-
  Find the moments in a long video that work as Shorts on their own, and write
  each one a new opening. Use for "cut this into shorts", "clip this",
  "repurpose this video", "what should I clip".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/shorts.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/../yt-script/hookscore.py *)
---

# yt-shorts

A good Short from a long video is not its best moment. It is a moment that **makes sense with
nothing around it**, and those are rarer.

```bash
python3 ${CLAUDE_SKILL_DIR}/shorts.py transcript.srt              # top 5, 20-55s each
python3 ${CLAUDE_SKILL_DIR}/shorts.py transcript.srt --top 8 --max 90 --json
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.
It uses `../yt-edit/deadair.py` and `../yt-script/hookscore.py`, so install all three together.

To fetch a video's own captions:

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o transcript "<video url>"
```

Auto-captions have no punctuation, so sentence ends are guesses; the tool says when that is the
case. A `whisper` transcript gives cleaner cuts.

## Before you start

Read `~/.claude/youtube/voice.md` if it exists. The new opening line is spoken or captioned in the
creator's voice, and the "will not claim" list still applies.

## Picking

Run `shorts.py` and work from its shortlist. Each Short needs all three:

1. **It starts on a fresh thought.** If the first sentence needs the minute before it, it is not a Short.
2. **Something turns** - a claim, then what complicates or proves it.
3. **It ends on a line**, not a trailing thought.

The tool checks the first and the third and scores the opening line. Only you can check the turn:
read each candidate, drop those without one, and show the best five with their timecodes and first
lines so the creator can reject one at a glance.

**Length:** Shorts can run to three minutes. 20-55 seconds is a choice: short spans finish and
loop better. Use `--max` for longer only when the turn needs the room. **Past 60 seconds, any
Content ID claim blocks the Short everywhere**, so a long span over someone else's music is not
an option.

## Writing each one

- **A new first line.** The long video's line leans on context this viewer never saw. Write the
  replacement and score it with `${CLAUDE_SKILL_DIR}/../yt-script/hookscore.py`.
- **On-screen text for the first two seconds**, in different words from the spoken line.
- **A loop**: what the last line sets up so the first line answers it.
- **A vertical note**: what the 9:16 crop loses from a 16:9 frame, and whether it matters.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
