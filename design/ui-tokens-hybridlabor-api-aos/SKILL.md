---
name: ui-tokens
description: "Use when listing, adding, or updating StyleSeed design tokens, keeping JSON sources, CSS variables, and dark-mode values perfectly in sync."
category: design-ui-ux
risk: safe
source: community
source_repo: bitjaru/styleseed
source_type: community
date_added: "2026-04-08"
author: bitjaru
tags: [ui, tokens, design-system, theming, styleseed]
tools: [claude, cursor, codex, gemini]
---

# UI Tokens

## Overview

Part of [StyleSeed](https://github.com/bitjaru/styleseed), this skill manages design tokens without letting the source-of-truth files drift apart. It is meant for teams using the Toss seed's JSON token files and CSS implementation together.

## When to Use
- Use when you need to inspect the current token set
- Use when you want to add a new color, shadow, radius, spacing, or typography token
- Use when you need to update a token and propagate the change safely
- Use when the project has both JSON token files and CSS variables that must stay aligned

## How It Works

### Supported Actions

- `list`: show the current tokens in a human-readable form
- `add`: introduce a new token and wire it through the implementation
- `update`: change an existing token value and audit the downstream usage

### Typical Source-of-Truth Split

For the Toss seed:
- JSON under `tokens/`
- CSS variables and theme wiring under `css/theme.css`
- typography support in the font and base CSS files

### Rules

- keep JSON and CSS in sync
- prefer semantic names over descriptive names
- provide dark-mode support where relevant
- update the token implementation, not just the source manifest
- check for direct component usage that might now be stale

## Output

Return:
1. The requested token inventory or change summary
2. Every file touched
3. Any affected components or utilities that should be reviewed
4. Follow-up actions if the new token requires broader adoption

## Best Practices

- Add semantic intent, not one-off brand shades
- Avoid token sprawl by extending existing scales first
- Keep naming consistent with the rest of the system
- Review contrast and accessibility when introducing new colors

## Additional Resources

- [StyleSeed repository](https://github.com/bitjaru/styleseed)
- [Source skill](https://github.com/bitjaru/styleseed/blob/main/seeds/toss/.claude/skills/ui-tokens/SKILL.md)

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.


## Core Process
1. Identify the need for a new token and ensure an existing semantic token doesn't already fit.
2. Update the master JSON token source.
3. Generate or manually update the corresponding CSS variables.
4. Explicitly define and verify the corresponding dark-mode token values.

## Common Rationalizations
| Rationalization | Reality |
|---|---|
| I'll just add the CSS variable directly without updating the JSON. | Desyncs the token source of truth, breaking multi-platform tooling. |
| I don't need to define a dark mode equivalent for this specific color. | Incomplete token definitions cause random bright spots in dark mode. |
| I'll create a new token for this one-off color. | Bloats the design system; semantic tokens should be reused whenever possible. |

## Red Flags
- CSS variables and JSON token sources are out of sync.
- Missing dark mode definitions for new color tokens.
- Creating highly specific, non-reusable tokens instead of semantic ones.

## Verification
- [ ] Token is defined in both the JSON source and CSS variables.
- [ ] Dark mode values are explicitly set and verified.
- [ ] Token naming follows the established semantic conventions.
