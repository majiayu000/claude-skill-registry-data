---
name: ace-step-xl
description: Adapt score or song cues into ACE-Step 1.5 XL inputs using task type, caption, lyrics or instrumental structure, BPM, key, time signature, and temporal performance directions.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ACE-Step 1.5 XL Prompting

ACE-Step XL uses the same control pattern as ACE-Step 1.5 with a larger 4B DiT decoder.

## Core fields

- `task_type`: usually `text2music`, or another supported transform task when the source cue requires it
- `caption`: overall genre, instruments, mood, atmosphere, timbre, vocal identity, production, and progression
- `lyrics`: lyric text plus section and temporal performance information. For instrumental score, use `[Instrumental]` and structure markers as needed
- `bpm`: 30 to 300 when a fixed tempo matters
- `keyscale`: musical key when useful
- `timesignature`: meter when useful

## Workflow

1. Read music cue and score motif rules.
2. Put global musical identity in `caption`.
3. Put time-varying structure, section changes, performance shifts, and lyrics in `lyrics`.
4. Do not overload caption with a second-by-second timeline that belongs in structure.
5. Choose XL variant only as execution metadata: `xl-turbo` for fast high-quality iteration, `xl-sft` for tunable higher-quality sampling, `xl-base` when the task requires base-model transform features.
6. Save under `04_generation/prompts/ace-step-xl/<cue-id>.json`.

## Done

Global musical identity and temporal structure are separated cleanly, and the prompt reflects the cue's dramatic job and hit points.
