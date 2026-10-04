---
description: Define visual identity — colors, typography, logo usage, and imagery style
---

# Visual Identity

Define the visual identity system for "$ARGUMENTS". Create specifications for logo usage, color palette, typography, and imagery that express the brand visually.

## Prerequisites

Read `.metapowers/branding/$ARGUMENTS/02-strategy.md` and `.metapowers/branding/$ARGUMENTS/03-verbal.md`. If `03-verbal.md` does not exist, tell the user:

> Phase 3 (Verbal) has not been completed for "$ARGUMENTS". Run `/branding:verbal $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/branding/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context files:**
   - Read `.metapowers/branding/$ARGUMENTS/02-strategy.md` for personality and positioning
   - Read `.metapowers/branding/$ARGUMENTS/03-verbal.md` for voice and tone

2. **If the user has existing assets:**
   - Review logo files in `.metapowers/branding/$ARGUMENTS/assets/logo/`
   - Review fonts in `.metapowers/branding/$ARGUMENTS/assets/fonts/`
   - Review imagery in `.metapowers/branding/$ARGUMENTS/assets/imagery/`
   - Document and formalize what exists

3. **If creating from scratch, define:**

   **Logo usage rules:**
   - Minimum size, clear space requirements
   - Approved variations (primary, icon, monochrome, reversed)
   - Prohibited uses
   - Ask the user to provide/create logo files and place in `.metapowers/branding/$ARGUMENTS/assets/logo/`

   **Color palette:**
   - Primary colors (2-3) with hex, RGB values
   - Secondary colors (2-4) with hex, RGB values
   - Neutral colors for backgrounds and text
   - Accessibility: contrast ratios for text on each background

   **Typography:**
   - Primary typeface: name, weights, usage (headings vs. body)
   - Secondary typeface (if needed)
   - Type scale: sizes, weights, line heights for each level
   - Ask the user to provide font files and place in `.metapowers/branding/$ARGUMENTS/assets/fonts/`

   **Imagery style:**
   - Photography style (mood, composition, subjects)
   - Illustration style (if applicable)
   - Icon style
   - Do's and don'ts

4. **Write the artifact** to `.metapowers/branding/$ARGUMENTS/04-visual.md`

## Output

The visual identity written to `.metapowers/branding/$ARGUMENTS/04-visual.md`. Present a summary to the user highlighting:
- Primary color palette
- Typography choices
- Logo variations defined
- Imagery direction
