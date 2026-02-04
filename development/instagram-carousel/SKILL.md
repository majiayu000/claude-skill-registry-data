---
name: instagram-carousel
description: DEPRECATED - Use the instagram-carousel agent instead. Triggers on "create a carousel", "turn this into slides".
allowed-tools: Read
---

# Instagram Carousel (Deprecated)

This skill has been converted to an **agent** for proper skill orchestration.

## Why the Change

Skills can't properly orchestrate other skills (like hook-stack-evaluator). Agents can.
The carousel creation pipeline needs to invoke hook-stack-evaluator with Automation Mode,
which requires agent-level orchestration.

## How to Invoke

Say any of these:
- "Create an Instagram carousel from this article"
- "Turn this into slides"
- "Make a carousel for [topic]"

The agent lives at `.claude/agents/instagram-carousel.md`

## Resources Still Here

The resource files in this folder are still used by the agent:
- `resources/visual-metaphors.md`
- `resources/secondary-characters.md`
- `resources/carousel-formats.md`
- `resources/prompt-templates.md`

Do NOT delete this skill folder - only the SKILL.md was deprecated.
