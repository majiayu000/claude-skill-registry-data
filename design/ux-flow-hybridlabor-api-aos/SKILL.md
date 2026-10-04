---
name: ux-flow
description: "Use when designing user flows, progressive disclosure, and hub-and-spoke navigation using established StyleSeed UX structure patterns."
category: design-ui-ux
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ux, flows, navigation, product-design, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UX Flow

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill designs flows before screens. It uses proven UX patterns to define entry points, exits, screen inventory, and navigation structure so the implementation has a coherent user journey instead of a pile of disconnected pages.

## When to Use
- Use when planning onboarding, checkout, account management, dashboards, or drill-down flows
- Use when a new feature spans multiple screens or modal states
- Use when users need a clear path through a task instead of a single isolated page
- Use when the UI needs navigation logic before components are built

## How It Works

### Information Architecture Principles

- progressive disclosure: reveal complexity only when needed
- Miller's Law: chunk content into manageable groups
- Hick's Law: minimize decision overload on each screen

### Common Navigation Models

- hub and spoke for dashboards and detail views
- linear flow for onboarding, forms, and checkout
- tab navigation for 3 to 5 top-level areas

### Flow Rules

- every flow has a clear entry point
- every flow has a clear exit or success condition
- key features should usually be reachable within three taps from home
- non-root screens need back navigation
- loading, empty, and error states need explicit recovery paths

## Output

Provide:
1. An ASCII flow diagram
2. A screen inventory with each screen's purpose
3. Edge cases for loading, empty, and error states
4. Recommended page scaffolds and reusable patterns to implement next

## Best Practices

- Optimize for clarity before density
- Let one screen answer one primary question
- Keep escape hatches visible for risky or destructive steps
- Define state transitions before drawing detailed layouts

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ux-flow/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.


## Core Process
1. Map the navigation hierarchy utilizing hub-and-spoke or pyramid models.
2. Apply progressive disclosure to hide secondary complex features until needed.
3. Ensure clear exit paths and predictable back navigation independent of the browser.
4. Validate that primary actions are highly discoverable.

## Common Rationalizations
| Rationalization | Reality |
|---|---|
| I'll put all the settings on one long page. | Overwhelms the user; progressive disclosure should group related settings. |
| Users can just use the browser back button. | In-app navigation must provide clear, predictable paths independent of browser controls. |
| I'll hide this important feature in a deep submenu to keep the UI clean. | Violates the information pyramid; core features must be easily discoverable. |

## Red Flags
- Dead-end screens without clear navigation back to a hub.
- Overwhelming users with too many choices on a single screen.
- Inconsistent navigation patterns across similar flows.

## Verification
- [ ] User flow avoids dead ends and provides clear exit paths.
- [ ] Complex tasks use progressive disclosure to minimize cognitive load.
- [ ] Navigation hierarchy follows a clear hub-and-spoke or pyramid model.
