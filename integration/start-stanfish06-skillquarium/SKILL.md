---
name: start
description: Use when starting Zoom work.
---

# Start

Use this as the default entry skill for the plugin.

## What This Skill Does

- Classifies the request by job-to-be-done, not by product name alone
- Routes into the right implementation skill
- Pulls in product-specific Zoom references only after the route is clear
- Prevents common early mistakes, especially Meeting SDK vs Video SDK and REST API vs SDK confusion

## Routing Table

| If the user wants to... | Route to |
|---|---|
| Choose the right Zoom surface for a new project | [plan-zoom-product](../plan-zoom-product/SKILL.md) |
| Set up OAuth, tokens, scopes, or app credentials | [setup-zoom-oauth](../setup-zoom-oauth/SKILL.md) |
| Embed or customize a Zoom meeting flow | [build-zoom-meeting-app](../build-zoom-meeting-app/SKILL.md) |
| Build a bot, recorder, or real-time meeting processor | [build-zoom-bot](../build-zoom-bot/SKILL.md) |
| Debug a broken integration | [debug-zoom](../debug-zoom/SKILL.md) |

## Supporting Zoom References

Use these only after selecting the workflow:

- [general](../zoom-general/SKILL.md)
- [rest-api](../build-zoom-rest-api-app/SKILL.md)
- [meeting-sdk](../build-zoom-meeting-sdk-app/SKILL.md)
- [video-sdk](../build-zoom-video-sdk-app/SKILL.md)
- [webhooks](../setup-zoom-webhooks/SKILL.md)
- [websockets](../setup-zoom-websockets/SKILL.md)
- [oauth](../zoom-oauth/SKILL.md)

## Operating Rules

1. Prefer one clear recommendation over a product catalog dump.
2. Ask a short clarifier only when the route is genuinely ambiguous.
3. Keep the first response architectural and actionable, then go deep.
4. Pull in deeper references only when they directly help the current decision or implementation.
