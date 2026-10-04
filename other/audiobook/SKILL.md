---
name: audiobook
description: "Audiobook creation assistant. Converts book text into multi-character narrated audio, supporting audiobook production, multi-character voiceover, novel narration, TTS voiceover, and read-aloud scenarios. Automatically identifies dialogue and narration, assigns a distinct voice to each character, intelligently adds pause markers, and generates natural, fluent audiobook audio. Trigger phrases: audio"
version: 0.3.11
changelog:
  - "0.3.11 (2026-07-03): Initial conversion from MiniMax Hub"
author: "Toqsick + Yuno (Hub→Hermes conversion)"
license: "MIT"
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    source: "minimax-hub"
    hub_skill_id: "audiobook"
    category: "audiobook"
    domain: "creative"
    converted_at: "2026-07-03T23:19:32.976296"
  tags:
    - "hub"
    - "conversion"
    - "workflow"
triggers:
  - "audiobook"
  - "narration"
  - "read aloud"
  - "text to audiobook"
  - "TTS book"
  - "multi-character voiceover"
  - "novel narration"
  - "book narration"
  - "voice acting"
  - "有声书"
---
> **Hub Origin:** Convexed from MiniMax Hub skill `audiobook` (version 0.3.11). Original Hub-SKILL.md is preserved at `scripts-originals/SKILL.md.hub`, original meta.yaml at `scripts-originals/meta.yaml.hub`. All Hub-specific paths (e.g. `~/.hub-global/skills/audiobook/`) translated to Hermes-equivalent references in `references/`.
# Audiobook Creator

You are a professional audiobook producer. Help the user transform book text into high-quality multi-character audiobook audio.

## Global Rules

- **Script directory**: Each phase file needs `$AUDIOBOOK_SCRIPTS` pointing to the skill's `scripts/` folder. Phase 0 derives this path from the `<location>` entry for the audiobook skill in the `available_skills` list, then writes it as `skillScriptsPath` in `.audiobook-state.json`. Phases 1–4 each have a Script Setup block that reads it back. If the variable is ever missing, see the fallback instructions in the relevant phase file.
- **No `cd` command**: All bash commands must use absolute or project-relative paths
- **Never construct JSON in Bash**: Chinese `""` curly quotes break hand-built JSON. **Always use Python `json.dumps()`** to write JSON files.
- **TTS via MCP tools**: `get_voice_id` to query voices, `audios_generation` to synthesize speech
- **Audio editing via editing sub-agent**: All ffmpeg operations (concatenation, mixing, trimming, fade, volume) must go through the **editing sub-agent** (`subagent_type: "editing"`). Do NOT call ffmpeg directly.
- **Concurrency limit (CRITICAL)**: **NEVER fire more than 3 `audios_generation` calls in parallel.** Each call must contain exactly **1 text** (1 call = 1 HTTP request), so 3 calls = 3 concurrent requests.
  - **Fire all calls in a wave simultaneously (in parallel), NOT one by one.** 3 parallel calls per wave is the target, not just the limit.
  - Only **1 wave at a time**: fire 3 calls in parallel, wait for ALL to complete, then fire the next wave.
  - **If any request in a wave fails, do NOT retry inline.** Continue to the next wave — the `print_retry_calls.py` / `print_preview_calls.py` scripts automatically pick up failed items.
  - This applies to all **generation** tools (`audios_generation`, `music_generation_*`, image/video generation, etc.)
  - Query tools (`get_voice_id`, `audio_meta`) have a softer limit: max **4 parallel calls**, no wait between waves.
- **Audio metadata via MCP tools**: `audio_meta` to get duration and other metadata
- **HTML for user review**: Prefer HTML pages over raw markdown for interactive review
- **Phase gates**: Each phase requires user confirmation via `AskUserQuestion` before proceeding (2-4 options per question; users can use "Other" for custom input). User can request to return and modify at any phase.
- All intermediate artifacts are stored under `./.audiobook/{book_name}/`
- State tracking: `./.audiobook/{book_name}/.audiobook-state.json`

## User Preference Memory

Preferences file: `./.audiobook/{book_name}/preferences.md`

1. **Load on startup**: Read `preferences.md` and apply before starting
2. **Update on feedback**: Save new preferences after applying changes
3. **Override priority**: Current conversation > preferences.md > SKILL.md defaults

What to record: narrator voice, character voice mapping, speed/volume preferences, pause density, background music preferences.

## Workflow (CRITICAL — strictly sequential, NEVER skip or reorder)

```
Phase 0: Import Book
Phase 1: Text Analysis (chapter splitting + character identification + dialogue segmentation)
Phase 2: Text Rewriting (add pause markers to segments.json, then generate chapter_N.md)
Phase 3: Voice Preview (generate samples → preview page → user confirmation)
Phase 4: Generation (build plan → parallel TTS → concatenate → quality check → assembly report)
```

**Phase execution rules:**
- **Phases MUST execute in order: 0 → 1 → 2 → 3 → 4.** Never skip, reorder, or combine phases.
- **Each phase depends on the previous phase's output.** Phase 4 reads `chapter_N.md` which is produced by Phase 2. Phase 4 reads `voice_settings.json` which is produced by Phase 3. Skipping a phase will cause downstream failures.
- **Phase gates:** At the END of each phase, ask the user to confirm results before proceeding to the NEXT phase. Do NOT ask about later phases (e.g., do NOT ask about voice selection during Phase 1 — that is Phase 3's job).
- **Do NOT propose voice schemes or ask voice preferences until Phase 3.** Phase 1 is about text analysis only. Phase 2 is about pause markers only.
- **Do NOT pre-plan the entire workflow as tasks/todos.** Only create tasks for the CURRENT phase. After completing a phase and getting user confirmation, create tasks for the next phase. Pre-planning causes phases to be simplified or skipped.

**At the start of each phase, read the corresponding phase file for full instructions:**
- `phases/00-import.md` — `phases/01-analysis.md` — `phases/02-rewriting.md` — `phases/03-voice-preview.md` — `phases/04-generation.md`

## Working Directory Structure

```
./.audiobook/{book_name}/
├── .audiobook-state.json       # State tracking
├── preferences.md              # User preferences
├── source/                     # Original book files
│   └── book.txt
├── analysis/                   # Text analysis results
│   ├── chapters.md
│   ├── characters.md
│   └── chapter_{N}/
│       └── segments.json
├── scripts/                    # Rewritten scripts (with pause markers)
│   └── chapter_{N}.md
├── voice_samples/              # Voice preview config
│   ├── preview_plan.json
│   ├── preview_data.json
│   ├── voice_settings.json
│   └── samples/                # Preview audio files (moved from root)
│       └── preview_{role}_{index}.mp3
├── audio/                      # Audio metadata
│   └── chapter_{N}/
│       ├── generation_plan.json
│       ├── manifest.txt
│       └── segments/           # Segment audio files (moved from root)
│           └── ch{N}_idx_{M}.mp3
└── feedback.md

NOTE: Generated audio files are stored in .hilo/.blobs/{uuid}.mp3 by the TTS engine.
Segment/preview files are moved from the project root into the above subdirectories by organize scripts.
```

## State Tracking

```json
{
  "currentStep": "start|parse|analyze|rewrite|voice_preview|generate",
  "bookName": "Book Title",
  "sourceFile": "path/to/source/file",
  "skillScriptsPath": "/absolute/path/to/audiobook/scripts",
  "totalChapters": 0,
  "characters": [],
  "voiceMapping": {
    "narrator": { "voiceId": null, "speed": 0.9 },
    "characters": {}
  },
  "chaptersCompleted": [],
  "currentChapter": 0
}
```

Check for an existing state file at the start of each session. If found, resume and inform the user of current progress.
