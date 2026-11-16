---
name: yt-edit
description: >-
  Turn the transcript of a raw recording into a cut list - silences, filler and
  false starts, each with timecodes. Use for "edit this", "cut the dead air",
  "tighten this up", "I rambled", or any request to shorten footage from its
  transcript.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/deadair.py *)
---

# yt-edit

A cut list from a timestamped transcript. It tells you what to cut; your editor does the cutting.

```bash
python3 ${CLAUDE_SKILL_DIR}/deadair.py transcript.srt               # srt, vtt or whisper json
python3 ${CLAUDE_SKILL_DIR}/deadair.py transcript.srt --floor 0.35 --json
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.

No transcript yet? `whisper`, `faster-whisper`, or YouTube's own captions on an unlisted upload all
work. YouTube's auto-caption `.vtt` goes in as it comes: word timings, rolling repeats and
`[Music]`-style tags are cleaned on load. To fetch it from a link:

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o transcript "<video url>"
```

That writes `transcript.en.vtt`. Swap `en` for the video's language. Auto-captions carry no
punctuation; a `whisper` transcript does, and gives cleaner sentence edges. Never guess timings.

## What it finds

- **DEAD**: gaps longer than the floor, trimmed from the middle so both sides keep a breath.
  Cutting tight against speech is what makes a tightened take sound breathless.
- **FILLER**: cues that are nothing but filler - English ("um", "so yeah", "basically"), Spanish
  ("bueno", "o sea"), Hindi ("matlab", "accha", "मतलब") and Nepali ("ani", "khai", "अनि"). Other
  languages get DEAD and REPEAT only; say so.
- **REPEAT**: a sentence started again. The abandoned attempt is the one cut, usually the shorter,
  and it is found even with an "um" between the two tries.

## What it does not do

It never touches the media file and has no view on your B-roll. The percentage it reports is of
speech: if the video has a long silent demo, the runtime it predicts is wrong. Check the list
against the footage before trusting the final length.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
