---
name: asset-pipeline
description: Generate, iterate, deliver, and lifecycle-manage creative assets (image, video, audio clips, music) with Telegram-first reply delivery, working/final storage separation, metadata + prompt history tracking in .meta.md files, retention cleanup (3-day working, 7-day final pre-offload), and future S3 offload readiness. Use when creating or revising assets requested in chat threads.
---

# Asset Pipeline

Use this skill to run the full asset workflow:

1. Clarify request (only if needed)
2. Generate candidates (multi-engine by default)
3. Save working outputs
4. Iterate with feedback
5. Promote winner to final
6. Reply with the asset in the same thread/request context
7. Enforce retention + offload reminders

## Scope

Handle:
- Images
- Videos
- Audio clips (SFX/prank-style clips)
- Music

Do NOT handle:
- Conversational TTS used to "talk" to the user. Keep that in a separate skill/path and treat as ephemeral.

## Directory Layout

Use this structure under workspace root:

```text
assets/
  working/
    image/
    video/
    audio/
    music/
  final/
    image/
    video/
    audio/
    music/
  manifests/
```

Notes:
- Keep `assets/manifests/` reserved for optional indexes/summaries later.
- The authoritative metadata for each final asset lives in its adjacent `.meta.md` file.

## Naming Rules

### Final assets

Use:
- `YYYY-MM-DD-DESCRIPTION.ext`
- `YYYY-MM-DD-DESCRIPTION.meta.md`

Where:
- `YYYY-MM-DD` is UTC date of finalization
- `DESCRIPTION` is meaningful, searchable, and normalized to lowercase kebab-case

Example:
- `2026-03-04-curly-robot-avatar.webp`
- `2026-03-04-curly-robot-avatar.meta.md`

Collision rule:
- If needed, append version suffix: `-v2`, `-v3`, ...

### Working assets

Use deterministic but temporary names:
- `YYYY-MM-DD-DESCRIPTION--wrk-<jobid>-<engine>-r<round>-c<candidate>.ext`

Example:
- `2026-03-04-curly-robot-avatar--wrk-j8f2-midjourney-r2-c1.webp`

## Delivery Rules (Telegram-first)

- When user requests an asset in a thread, deliver results as a literal reply to that request message in the same thread/context.
- Default to storage-efficient formats unless user explicitly asks otherwise.
- Caption/content should follow the user prompt; avoid adding unrelated caption text.

## Retention Rules

- Working assets: delete after 3 days.
- Final assets: keep locally for 7 days, then offload to long-term storage (when configured).
- Until off-host storage is configured, keep finals locally and remind user weekly that offload is pending.

## Generation Strategy Defaults

- Start with multi-engine + multi-asset per engine.
- If cost/latency becomes a concern, reduce breadth after user agreement.
- For music requests, ask clarifying questions before generation (style, duration, mood, use case, platform constraints).

## Final Metadata File Format (`.meta.md`)

For each final asset, create or update an adjacent `.meta.md` file with:

1. YAML frontmatter: manifest-level metadata
2. Iteration history body:
   - newest iteration at top
   - include prompt + model-specific meta sent for that run
   - include user feedback entries between prompt iterations
   - oldest iteration at bottom

Read `references/meta-template.md` for exact structure.

## Workflow

1. Parse asset request and detect type: image/video/audio/music.
2. If request is ambiguous, ask only minimal clarifying questions.
3. Create working job id and save all candidates under `assets/working/<type>/`.
4. Track each generation round (engine, parameters, outputs, cost if available).
5. On user selection, promote chosen output to `assets/final/<type>/` with final naming rules.
6. Create/update `.meta.md` next to final file.
7. Deliver asset by replying to the original request message.
8. Run retention cleanup for expired working files.
9. Check finals older than 7 days:
   - if offload unavailable, keep local and include in weekly reminder queue;
   - if offload configured, transfer and verify.

## Optional Helper Scripts

- `scripts/cleanup_working_assets.sh` removes working files older than TTL.
- `scripts/list_final_offload_due.sh` lists finals older than 7 days.

Run from workspace root.

## Safety and Quality

- Keep private data out of prompts sent to third-party generators unless explicitly required.
- Preserve enough generation metadata to reproduce outputs.
- Prefer deterministic transforms (e.g., ffmpeg/ImageMagick) for format conversion.
- Never mix conversational TTS artifacts into this pipeline.
