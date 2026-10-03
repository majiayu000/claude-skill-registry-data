---
name: ls-remotion-best-practices
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
