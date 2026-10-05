---
name: ui-demo-video-linear
description: Record a short browser demo for frontend or UI work and attach it to a Linear issue. Use when an agent changes visible application behavior, needs to prove the UI works, or should leave video evidence on a Linear issue. Prefer Playwright MCP for browser automation and Linear MCP for attachment/comment publishing.
---

# UI Demo Video Linear

## Overview

Record a short UI demo, locate the video artifact, upload it to Linear, and leave a concise issue comment with what was validated.

Use this skill only for work with visible UI changes. Skip it for backend-only, library-only, or non-visual tasks.

## Workflow

1. Decide whether a demo video is warranted.
2. Launch the app and validate the target user flow with Playwright MCP.
3. Save or locate the final video artifact.
4. Upload the video to Linear.
5. Leave a short comment summarizing what the demo proves.

## Decision rules

Record a demo when at least one is true:
- the issue touches frontend, web, desktop, or visible product behavior
- the issue changes navigation, forms, layout, interactions, or animations
- the issue would benefit from visual proof in review or handoff

Skip the demo when all are true:
- no visible UI changed
- the work is backend, CLI, library, schema, or infra only
- there is no meaningful user journey to show

If unsure, read `references/workflow-rules.md`.

## Browser automation

Prefer Playwright MCP if available.

Recommended pattern:
- start the app under test
- wait for readiness
- open a browser context with video recording enabled
- run only the shortest path that proves the change
- close the browser context cleanly so the video file is finalized

Keep the demo short:
- target 15 to 60 seconds
- avoid long idle time
- avoid private or irrelevant screens

## Artifact discovery

If Playwright MCP returns an explicit video path, use it.

If not, use:
- `scripts/find_latest_video.py --dir <root>`

The script returns JSON with:
- `video_path`
- `size_bytes`
- `mtime_epoch`
- `mime_type`

Reject empty or suspicious artifacts before upload.

## Linear upload

Prefer Linear MCP for publication.

Primary path:
1. prepare attachment payload with:
   - `scripts/prepare_linear_attachment.py --file <video> --issue <ISSUE>`
2. call the Linear attachment tool with the emitted JSON fields
3. add a short issue comment with:
   - what was validated
   - the main flow shown in the video
   - any known limitations

Use issue attachments as the default publication surface. Only use comments alone if attachment upload is unavailable.

## Comment template

Keep comments short and factual.

Suggested shape:
- `Demo video attached.`
- `Validated: <one sentence>`
- `Path shown: <one sentence>`
- `Known limitation: <optional>`

## Failure handling

If recording fails:
- state whether app launch, navigation, or video finalization failed
- do not claim the demo exists
- leave a short diagnostic note if useful

If upload fails:
- preserve the local video path
- report whether failure happened during encoding or Linear publication

If the artifact is too large:
- prefer a shorter rerun over uploading a large noisy video

## Resources

### scripts/
- `find_latest_video.py`: Locate the newest demo video in a directory tree and emit JSON metadata.
- `prepare_linear_attachment.py`: Base64-encode a video file and emit JSON ready for Linear attachment upload.

### references/
- `workflow-rules.md`: When to record, when to skip, and what a good demo proves.
