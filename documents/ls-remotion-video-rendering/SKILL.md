---
name: ls-remotion-video-rendering
description: Guide Remotion projects and video-rendering best practices. Use for Remotion
  compositions, rendering, media assets, performance, and deploy workflows.
metadata:
  version: '1.0'
---

# Remotion Video Apps

Use this skill when working on Remotion video apps tasks.

## Workflow

- Inspect Remotion, React, bundler, and Node versions before changing rendering code.
- Keep compositions deterministic: validate props, preload assets, and avoid time-dependent side effects.
- Test representative frames and renders before broad refactors or cloud rendering changes.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.

## Provenance

- Source classification: `official-docs-reference`
- This is a LocalSetup-native skill written from project workflow requirements and public/official documentation routing.

## Transcripts and captions

For local recording preparation, private transcription, human wording/timing
review, and sidecar captions, use
[recording transcripts and captions](../ls-recording-transcript-captions/SKILL.md).
Use this rendering owner for an optional separate burned-in video copy; a rendered
caption track does not establish that its transcript has been reviewed.
