---
name: tutopanda-documentary-producer
description: Coordinate Tutopanda CLI and MCP to generate, edit, inspect, and preview documentary videos (video-audio-music blueprint with FinalVideo export). Use when users ask for Tutopanda to build, edit, or review movies inside Claude Code.
---

# Tutopanda Documentary Producer

Use this skill whenever a user wants Tutopanda to create or modify documentary-style videos, export an MP4, or preview results from within Claude Code.

## Preconditions
- `tutopanda` binary is available on PATH. If not, stop and ask the user to install the published CLI manually.
- Tutopanda has been initialized (`tutopanda init --rootFolder=<absolute-path>`). Confirm the config path or `TUTOPANDA_CLI_CONFIG` before running any command.
- Default blueprint is `video-audio-music.yaml` because it emits `FinalVideo` (MP4) in addition to the timeline. Switch blueprints only if the user requests a different workflow.

## Generation workflow
1. Collect required inputs from the user: `InquiryPrompt`, `Duration`, `NumOfSegments`, `SegmentDuration`, `VideoStyle`, `AspectRatio`, `Resolution`, `VoiceId`, plus optional `Audience`, `Language`, `Emotion`, `MusicalStyle`. Do not fabricate values.
2. Write an inputs YAML with those values at an absolute path the user approves.
3. Run Tutopanda via MCP (preferred) or CLI:
   - CLI example:
     ```bash
     tutopanda query "<InquiryPrompt>" \
       --inputs=/absolute/path/to/inputs.yaml \
       --usingBlueprint=video-audio-music.yaml \
       --concurrency=<workers-if-needed> \
       --nonInteractive
     ```
4. Capture the `movieId`, plan path, and friendly view path from the output.
5. If the user wants a preview, call `tutopanda viewer:view --movieId=<movieId>`.

## Editing workflow
- Require the existing `movieId` and an explicit inputs file path. Run:
  ```bash
  tutopanda edit \
    --movieId=<movie-id> \
    --inputs=/absolute/path/to/inputs.yaml \
    --usingBlueprint=video-audio-music.yaml \
    --concurrency=<workers-if-needed> \
    --nonInteractive
  ```
- Use `--dryRun` or `--upToLayer` only when the user asks for them. After the run, refresh the viewer.

## Inspection and review
- For prompts/timelines, run `tutopanda inspect --movieId=<movie-id> --prompts --all` and summarize key findings.
- Keep outputs and artefact paths tied to the configured root; do not relocate them.

## Failure handling
- If the CLI or config is missing, stop and ask the user to install or initialize Tutopanda rather than guessing paths or creating defaults.
- Avoid silently falling back to placeholder inputs—always confirm required fields before running.
