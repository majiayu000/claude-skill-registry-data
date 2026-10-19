---
name: podcast-clip-scout
description: "Use when the user has a timestamped podcast or video transcript and wants the best short clips picked from it (for example 'find the best clips in this episode', 'which moments would work as shorts', 'pick reel candidates from this transcript')."
---

# Podcast Clip Scout

## Overview

Picks ranked short-form clip candidates from a timestamped transcript and writes a cut list. It chooses and describes moments; it does not cut audio or video, burn in captions or write show notes. You score each moment with a five-part rubric; a helper script reads the transcript, checks your picks and exports the list. The scores are your judgment and nothing here has validated them against human picks, so say that in your final message.

## The helper

`scripts/clips.py` in this skill's folder, Python 3 standard library only (use `python3`, or `python` / `py -3`, whichever works). Transcripts can be SRT, VTT or JSON (a list of `{start, end, text}` segments, or Whisper's `{"segments": [...]}`).

- `clips.py cues TRANSCRIPT [--from N] [--to M]`: prints every cue as a number, a timestamp and its text.
- `clips.py check TRANSCRIPT --picks picks.json [--min 20] [--max 60] [--max-caption 150]`: validates your picks. Exit 0 clean, 1 problems (read every `ERROR` line), 2 unreadable input.
- `clips.py export TRANSCRIPT --picks picks.json --out DIR`: runs the same check and, only if it is clean, writes `clips.csv` and `clips.json`.

## The rubric

Score each candidate on five dimensions, each a whole number from 0 to 3. `total` is their sum. Rank by total, highest first; break ties by `hook`, then `standalone`.

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| `hook` | Opens on filler or a greeting | Weak opening, but a real point arrives within about 10 seconds | Opens on the topic with some pull | The first sentence grabs: a claim, question, surprise or conflict |
| `standalone` | Needs earlier context to follow | Needs one fact a caption could supply | Clear except one minor reference | A stranger understands it cold |
| `emotion` | Flat | Mild interest or amusement | Clear emotion or a real surprise | Laughter, anger, vulnerability or strong surprise |
| `payoff` | Trails off or cuts mid-thought | Ends on a point, not a conclusion | Ends on a clear conclusion without a final punch | A punchline, conclusion or takeaway lands at the end |
| `quotable` | Nothing worth repeating | A decent sentence | A strong line, but wordy | A line someone would screenshot or caption |

## Process

1. **Read.** Run `clips.py cues` on the transcript and read all of it. If it is too long to read at once, read it in ranges with `--from` and `--to`, overlapping each range by enough cues to hold a whole clip, collect candidates from each range, and rank across all of them.
2. **Pick.** Choose the requested number of clips (default 5). If the episode does not hold that many good moments, return fewer and say so; never pad. A clip is a run of whole cues. Start on a cue that begins a sentence and end on one that finishes a thought. Keep it inside the length range (default 20 to 60 seconds; the user may give another).
3. **Write `picks.json`** next to the transcript, citing cue numbers only. Never type a timestamp; the helper derives times from the cues.
4. **Check.** Run `clips.py check`. Fix every `ERROR` and re-run until it is clean. A `WARN` (a clip that starts or ends mid-sentence, or has a gap inside it) is yours to judge: fix it or keep it, and mention a kept one.
5. **Export.** Run `clips.py export` with `--out` set to a folder the user names (or a new one beside the transcript).
6. **Report.** Show the ranked table (rank, start, end, total, caption) and the output folder. State plainly that the scores are your judgment and have not been validated against human picks.

## picks.json

```json
{"clips": [{
  "start_cue": 41, "end_cue": 58,
  "scores": {"hook": 3, "standalone": 2, "emotion": 2, "payoff": 3, "quotable": 1},
  "total": 11,
  "reasons": {"hook": "one line each", "standalone": "...", "emotion": "...", "payoff": "...", "quotable": "..."},
  "caption": "The line to post with the clip"
}]}
```

## What to tell the user

- This reads text only. Tone of voice, laughter that is not in the transcript, and anything visual are invisible to it.
- The check proves the list is consistent (real cues, lengths in range, no overlaps, arithmetic and order right). It does not prove a hook is a good hook.
- The skill makes no claim about what performs well on any platform. The 150-character caption cap is this tool's own default, not a platform rule.
- Transcript quality caps the result: wrong timestamps or missing speaker labels give wrong clips. If speakers matter and the transcript has none, ask instead of guessing.
- Cutting the clips is a separate step (for example `podcast-use` or `ffmpeg`), using the start and end times in `clips.csv`.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Typing timestamps into picks.json | Cite cue numbers only; times come from the cues |
| Scoring every clip 2s and 3s | Use the full 0 to 3 range; a clip that needs context scores `standalone` 0 or 1 |
| Padding to hit the count | Return fewer clips and say why |
| Skipping `check` before `export` | `export` re-checks and writes nothing on errors; run `check` first so you can fix them |
| Ranking by gut after scoring | The list must be in rank order: total, then `hook`, then `standalone` |
