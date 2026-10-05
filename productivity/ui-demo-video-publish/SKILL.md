---
name: ui-demo-video-publish
description: Publish UI demo evidence to Linear after frontend or visible product changes. Use when an agent has already implemented or validated a visible UI flow and needs to record the flow, attach the resulting video to a Linear issue, and leave a concise proof comment. Prefer Playwright MCP for recording and the existing `ui-demo-video-linear` skill for artifact discovery and attachment preparation.
---

# UI Demo Video Publish

## Overview

Run the complete workflow for visible UI work:
- record a short demo
- find the finalized video file
- attach it to Linear
- post a concise comment explaining what the demo proves

This skill is the wrapper. It should call the lower-level skill at:
- `../ui-demo-video-linear/SKILL.md`

## Use this skill when

Use it when all are true:
- the issue has visible UI impact
- a short visual proof would help review or handoff
- the target Linear issue is known

Do not use it for:
- backend-only changes
- library or infra work
- tasks with no meaningful UI path to demonstrate

## End-to-end workflow

1. Decide if the issue deserves a demo.
2. Launch the app under test.
3. Record the shortest path that proves the change.
4. Finalize and locate the video artifact.
5. Attach the video to Linear.
6. Post a short comment summarizing the evidence.

## Recording

Prefer Playwright MCP for browser automation.

Recording rules:
- keep the demo short
- prove one or two target behaviors only
- avoid noisy or unrelated exploration
- close the recording context cleanly so the artifact is finalized

If recording capability is not exposed directly by Playwright MCP in the current environment, fall back to a local Playwright script or skip with a clear reason.

## Artifact handling

Use the lower-level skill resources:
- `find_latest_video.py`
- `prepare_linear_attachment.py`

Canonical flow:
1. locate the artifact
2. validate that it is non-empty and plausibly a video
3. prepare attachment payload
4. upload to Linear

## Linear publication

Preferred publication flow:
1. create the attachment on the issue
2. add a comment with a short summary

Comment content should answer:
- what was validated
- which flow was shown
- any known limitation or omission

Use:
- `scripts/build_demo_comment.py`

## Output contract

A successful run should leave:
- a Linear attachment containing the video
- a short Linear comment summarizing the demo
- a local record of:
  - issue id
  - video path
  - attachment status
  - comment body

## Failure handling

If recording fails:
- say whether launch, navigation, or video finalization failed
- do not pretend a demo was published

If upload fails:
- preserve the local path to the video
- report whether attachment or comment creation failed

If the video is too large or noisy:
- rerun a shorter scenario instead of publishing a weak artifact

## Resources

### scripts/
- `build_demo_comment.py`: Generate the standard Linear comment body for a published demo.

### references/
- `linear-publication-flow.md`: Canonical publication sequence and operator expectations.
