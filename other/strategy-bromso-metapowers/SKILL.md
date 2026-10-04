---
description: Define brand positioning, values, personality, and competitive differentiation
---

# Strategy

Define the brand strategy for "$ARGUMENTS". Synthesize discovery findings into a clear positioning, values, personality, and differentiation framework.

## Prerequisites

Read `.metapowers/branding/$ARGUMENTS/01-discover.md`. If this file does not exist, tell the user:

> Phase 1 (Discover) has not been completed for "$ARGUMENTS". Run `/branding:discover $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/branding/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context files:**
   - Read `.metapowers/branding/$ARGUMENTS/01-discover.md` for research findings
   - Read `plugins/branding/shared/brand-platform-template.md` for output structure
   - Read `plugins/branding/shared/brand-prism-guide.md` for the six brand facets

2. **Define brand purpose, vision, and mission:**
   - Purpose: why does this brand exist?
   - Vision: where is the brand going?
   - Mission: what does it do, for whom, and how?

3. **Define brand values:**
   - 3-5 core values that guide all brand decisions
   - For each value: description and how it manifests in behavior

4. **Craft positioning statement:**
   - For [target audience] who [need], [brand] is the [category] that [benefit] because [reason]

5. **Define brand personality:**
   - 3-5 personality traits (e.g., bold, approachable, expert, playful)
   - For each trait: how it influences communication

6. **Map competitive differentiation:**
   - What sets this brand apart from each key competitor?
   - The unique value proposition

7. **Write the artifact** to `.metapowers/branding/$ARGUMENTS/02-strategy.md` following the brand platform template.

## Output

The brand strategy written to `.metapowers/branding/$ARGUMENTS/02-strategy.md`. Present a summary to the user highlighting:
- The positioning statement
- Core values
- Key personality traits
- Primary differentiator
