---
description: Package all brand elements into a complete brand guidelines document
---

# Brand Guidelines

Compile all brand work for "$ARGUMENTS" into a comprehensive brand guidelines document — the single source of truth for anyone using the brand.

## Prerequisites

Read all prior phase artifacts. If `04-visual.md` does not exist, tell the user:

> Phase 4 (Visual) has not been completed for "$ARGUMENTS". Run `/branding:visual $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/branding/$ARGUMENTS/skip-log.md`.

## Process

1. **Read all prior artifacts:**
   - Read `.metapowers/branding/$ARGUMENTS/01-discover.md` for context
   - Read `.metapowers/branding/$ARGUMENTS/02-strategy.md` for brand platform
   - Read `.metapowers/branding/$ARGUMENTS/03-verbal.md` for voice, tone, messaging
   - Read `.metapowers/branding/$ARGUMENTS/04-visual.md` for visual identity
   - Read `plugins/branding/shared/brand-guidelines-template.md` for output structure

2. **Compile the brand guidelines** following the template, combining:
   - Brand overview (purpose, vision, mission, values from Strategy)
   - Logo usage rules and variations (from Visual)
   - Color palette with specifications (from Visual)
   - Typography system (from Visual)
   - Imagery and photography guidelines (from Visual)
   - Voice and tone guidelines (from Verbal)
   - Application examples — how the brand appears across key touchpoints

3. **Add compliance rules:**
   - What must always be done (mandatory elements)
   - What must never be done (prohibited uses)
   - Common mistakes to avoid
   - When to seek brand team approval

4. **Reference assets:**
   - Link to all files in `.metapowers/branding/$ARGUMENTS/assets/`
   - List available logo variants, fonts, and imagery

5. **Write the artifact** to `.metapowers/branding/$ARGUMENTS/05-guidelines.md`

## Output

The brand guidelines written to `.metapowers/branding/$ARGUMENTS/05-guidelines.md`. Present a summary to the user highlighting:
- Sections covered
- Number of compliance rules
- Asset inventory
- How other domains can use these guidelines (e.g., `/branding:audit`)
