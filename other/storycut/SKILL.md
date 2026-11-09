---
name: storycut
description: Turn an interview, podcast, lecture, founder story, or other spoken video/audio file into a verified transcript, meaningful highlights, and an ordered, timestamped story cut list. Use whenever the user asks for the best moments, clips, an interview highlight reel, a rough cut, an edit decision list, or transcript-to-video storytelling, even if they do not mention StoryCut by name.
---

# StoryCut — evidence-based interview editing

You are the story editor; `scripts/storycut.py` does deterministic transcription preparation, timestamp math, source checks, and exports. Never invent a quotation or timestamp. Never claim a rendered video exists unless you actually render one.

## Environment and input

- Run scripts with Python 3.10+ from this skill directory, for example `python3 scripts/storycut.py doctor`.
- Supported transcript inputs: `.srt`, `.vtt`, or `.txt` with explicit timestamp ranges. Supported media: audio/video readable by FFmpeg.
- Media transcription is **local** and requires FFmpeg plus `faster-whisper` (`pip install faster-whisper`). Its model downloads on first run; no paid transcription API is required. Ask permission before installing or downloading if the environment requires it.
- Input media can contain sensitive speech. Keep it local; do not upload, publicize, or commit it without consent. Analyze only media the user owns or is permitted to process.
- In Claude Code, the user needs to provide a **local accessible file path**. An attachment in a chat interface is not automatically accessible to this skill.

## Workflow

1. Ask only for missing essentials: file path, intended audience/format, target duration, and desired story angle. If omitted, use: general viewers, an engaging 90-second highlight, and fidelity to speaker intent; state those assumptions.
2. Run `python3 scripts/storycut.py prepare INPUT --out OUTPUT_DIRECTORY`. For long media, provide `--model small` or another available faster-whisper model. For a timestamped transcript, no model is needed.
3. Open the generated `transcript.json`. Every item has a stable `id`, `start`, `end`, and `text`. Use those IDs, not guessed seconds. For very long files, inspect the transcript in chunks, first making a compact story map with IDs, then reread source segments for final choices.
4. Identify moments with a hook, stakes, change, concrete example, insight, or satisfying payoff. Do not treat emotional intensity alone as quality. Design a coherent **hook → setup → turning point → payoff** sequence, or explain a justified alternative. Preserve context and speaker meaning.
5. Write `cutlist_draft.json` according to `references/cutlist-format.md`. Every clip must refer to one or more **consecutive** segment IDs. The script derives start/end timestamps from those IDs. Use `quote` only if it is an exact, contiguous excerpt in the source clip; otherwise omit it. Scores are qualitative judgments, never objective virality predictions.
6. Run `python3 scripts/storycut.py validate OUTPUT_DIRECTORY/transcript.json OUTPUT_DIRECTORY/cutlist_draft.json --out OUTPUT_DIRECTORY`. If validation fails, fix the cited IDs or quotes and rerun. Read warnings about overlong clips or target duration.
7. Deliver `cutlist.md`, `cutlist.csv`, and `cutlist.json` with a short explanation of editorial logic and any uncertainty. The user can hand these files to an editor. Do not present them as frame-accurate edits: speech segments are approximate and may need manual handles.

## Guardrails

- Never fabricate speech, transitions, or speakers. Explicitly flag missing narrative bridges and context.
- Keep segment IDs consecutive *within* each clip. Non-adjacent clips form separate cuts.
- If no transcription engine is installed, do not pretend video was analyzed. Explain the missing dependency or use a real timed transcript the user supplies.
- If the user's input is plain text without timestamps, request the original media or a timed transcript. Do not infer timing from word counts.
- The MVP generates an editorial **cut list**, not a finished MP4. Do not promise automated video rendering.
- For journalistic, legal, or sensitive material, emphasize human fact-checking and context review before publication.

