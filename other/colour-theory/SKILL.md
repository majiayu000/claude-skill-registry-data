---
name: colour-theory
description: "Harmonious palettes built from one anchor hue."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, colour]
    category: web
    related_skills: [web-design, colour-contrast, semantic-colour]
    web_designer_stages: [direction, colour]
---

# Colour Theory and Palette Harmony Skill

Using the colour wheel to build a harmonious palette: one brand anchor hue, a named harmony rule, and roles assigned so the palette feels intentional rather than random. This skill defines the palette for a site. It does not check contrast ratios — that is the colour-contrast skill — and it does not assign fixed semantic meanings to colours — that is the semantic-colour skill.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- When defining a site's palette.
- When choosing an accent or CTA colour.
- When fixing a palette that feels jarring or flat.
- When the direction stage needs a colour direction, or the colour stage needs a palette recorded.
- When a palette has grown past 5 colours and needs cutting back to an intentional set.

It is NOT for contrast checking, semantic status colours, or judging the finished palette — the visual judger checks the result and the a11y judger checks contrast.

## Prerequisites

- The run is active and the coordinator loaded this skill for the direction or colour stage.
- The direction stage has a chosen direction, or is choosing one now, so the palette matches it.
- The brief is frozen, so the palette serves the site's audience and mood rather than taste alone.
- The brand anchor hue is known, so the palette starts from one hue rather than from random colours.

## How to Run

1. Start from one brand anchor hue.
2. Apply a named harmony rule: monochromatic, analogous, complementary, triadic or tetradic.
3. Choose hue, saturation and lightness for mood and emphasis, not at random.
4. Assign roles: background 60–70%, primary, secondary, neutrals, semantic.
5. Keep saturated colour for actions only; large areas stay calm.
6. Use complementary colours as accent versus background, never both at full saturation in large areas.
7. Check the palette as a whole, not colour by colour: 3–5 colours that feel intentional together.
8. Record the palette and its roles in the colour stage record, and the chosen direction in the direction stage record.
9. Revisit the palette only when it feels jarring or flat — a named rule applied to the anchor hue is the fix, not a new random colour.
10. Give the accent and CTA their colour from the roles, not from a fresh pick outside the palette.
11. Confirm the neutrals carry the quiet areas: backgrounds and surfaces must not need a saturated colour to hold together.
12. Check the palette on a real page: the roles must read clearly in context, not only in a swatch list.

## Quick Reference

- Harmony rules: monochromatic, analogous, complementary, triadic, tetradic.
- Palette size: 3–5 colours.
- Background role: 60–70% of the palette's area.
- Saturated colour: actions only, never large areas at full saturation.
- Complementary colours: accent versus background, never both at full saturation in large areas.
- Roles: background, primary, secondary, neutrals, semantic.
- Start from one brand anchor hue; choose hue, saturation and lightness for mood and emphasis.
- Judge the palette as a whole, not colour by colour.
- The accent and CTA colours come from the roles, not from a fresh pick outside the palette.
- The neutrals carry the quiet areas; saturated colour carries the actions.
- The roles read clearly on a real page, not only in a swatch list.

## Procedure

### 1. What it is

Using the colour wheel to build harmonious palettes — monochromatic, analogous, complementary, triadic, tetradic — with hue, saturation and lightness chosen for mood and emphasis, not at random.

### 2. How Hermes applies it

Hermes starts from one brand anchor hue, applies a named harmony rule, assigns roles (background 60-70%, primary, secondary, neutrals, semantic), and keeps saturated colour for actions only.

### 3. What it returns to the stage

- Direction stage: `directions` — the colour directions explored; `chosen` — the direction picked, carrying the anchor hue and harmony rule.
- Colour stage: `roles` — the palette roles (background, primary, secondary, neutrals, semantic); `contrast_table` — the contrast figures for the palette's pairs, which the colour-contrast skill fills in.

The palette is the value both stages record. The direction record carries the anchor hue and the named rule; the colour record carries the roles and the contrast figures for the pairs. If a record key is missing, the stage does not complete.

### 4. Good looks like

A palette of 3-5 colours that feels intentional; complementary colours used as accent vs background, never both at full saturation in large areas.

## Pitfalls

- A palette built without an anchor hue, so the colours have no relationship to each other.
- Saturated colour used across large areas, which makes the page feel jarring.
- Complementary colours both at full saturation in large areas, which vibrate against each other.
- Roles never assigned, so the same colour is used for background on one page and action on another.
- More than 5 colours in the palette, so nothing feels intentional.
- A palette chosen for a single page and never carried across the site.
- Hue, saturation and lightness chosen at random instead of for mood and emphasis.
- A palette that feels flat because no accent or CTA colour was ever chosen.
- Background given less than 60% of the area, so the palette has no calm ground to sit on.
- A jarring palette fixed by adding another colour instead of returning to the anchor hue and the named rule.
- An accent colour chosen outside the roles, so the palette gains a sixth colour by stealth.
- The palette judged from swatches alone and never checked on a real page.

## Verification

- The palette has 3–5 colours built from one anchor hue under a named harmony rule.
- Roles are assigned: background 60–70%, primary, secondary, neutrals, semantic.
- Saturated colour appears only on actions.
- The palette and its roles are recorded in the colour stage record.
- The chosen direction carries the anchor hue and the harmony rule.
- The palette feels intentional as a whole, not colour by colour.
- The accent and CTA colours come from the roles, not from outside the palette.
- The roles read clearly on a real page, not only in a swatch list.

The skill does the work and the visual judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: direction, colour. Returns: `directions`, `chosen` (direction stage); `roles`, `contrast_table` (colour stage). Judger boundary: the visual judger checks palette harmony and role use; the a11y judger checks the contrast of the pairs.
