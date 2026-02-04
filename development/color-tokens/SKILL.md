---
name: color-tokens
description: Generate accessible color tokens from a single accent color. Use when user wants to create or update color palettes, check accessibility contrast, or generate warm/cool adaptive gray scales.
allowed-tools: Read, Write, Edit, Bash
---

# Generate Color Tokens

Generate accessible color tokens from a single accent color following Dieter Rams' "Less, but better" philosophy.

## Usage

1. Ask user for the accent color (hex format, e.g., `#ed8008`)
2. Run: `node .claude/skills/color-tokens/generate.js "#hexcolor"`
3. Review output with user
4. Update `src/styles/tokens.css` with new values

## What It Generates

- 10 adaptive grays that harmonize with the accent (warm/cool/neutral)
- Accessible text color for the accent (light or dark based on APCA contrast)
- CSS custom properties ready to paste
- Accessibility contrast checks

## Example

```bash
node .claude/skills/color-tokens/generate.js "#ed8008"
```
