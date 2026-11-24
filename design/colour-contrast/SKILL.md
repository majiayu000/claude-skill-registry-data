---
name: colour-contrast
description: "Text and surface pairs that meet AA contrast."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, colour, accessibility]
    category: web
    related_skills: [web-design, colour-theory, accessibility-wcag]
    web_designer_stages: [colour, theme]
---

# Colour Contrast and Accessibility Skill

WCAG contrast for every text, background, icon, border and focus-indicator pair, in light and dark themes, with colour never the only way to convey meaning. This skill computes and enforces the contrast of the pairs the palette produces. It does not build the palette itself — that is the colour-theory skill — and it does not assign semantic meanings to colours — that is the semantic-colour skill.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- For every text/background, icon, border and focus-indicator combination, in light and dark themes.
- When the colour stage needs a contrast table recorded, or the theme stage needs both themes checked.
- When a palette pair looks light-on-light and may fail.
- When a new theme surface is added and its pairs need checking.
- When a status is conveyed by colour alone and needs an icon or label alongside it.

It is NOT for choosing the palette, assigning status colours, or judging the finished page — the a11y judger runs the contrast check before judging a design done.

## Prerequisites

- The run is active and the coordinator loaded this skill for the colour or theme stage.
- A palette exists with roles assigned, so there are real pairs to compute contrast for.
- Both themes are defined, or the theme stage is defining them now, so light and dark are both checked.
- The full pair list is known — text, icons, borders and focus indicators — so nothing is checked only by eye.

## How to Run

1. List every pair the design emits: text on background, icon on surface, border on surface, focus indicator on its background.
2. Compute the contrast ratio for each pair in the light theme and again in the dark theme.
3. Reject any pair below its threshold: 4.5:1 for normal text, 3:1 for large text and UI components/icons.
4. Reject light-grey-on-white text outright, whatever the computed ratio says about the pair.
5. Pair colour with an icon or text label for every status, so meaning never rests on colour alone.
6. Check the result in greyscale: an error must still be understandable with colour removed.
7. Re-compute after any palette or surface change — a new background can break a pair that passed before.
8. Record the results as the contrast table in the colour stage record, and the checked surfaces in the theme stage record.
9. Check borders and focus indicators as pairs, not as decoration: they carry meaning and need 3:1.
10. Confirm status pairs twice: once for the text and once for the icon or label that carries the same meaning.
11. Keep the table current: any pair added after the table was recorded goes through the same check before it ships.

## Quick Reference

- WCAG AA: 4.5:1 for normal text; 3:1 for large text and UI components/icons.
- WCAG AAA: 7:1 for normal text; 4.5:1 for large text.
- About 8% of men have some colour-vision deficiency — colour must never be the only way to convey meaning.
- Check every pair in both light and dark themes.
- Reject light-grey-on-white text.
- Pairs to check: text/background, icon/surface, border/surface, focus indicator/background.
- Greyscale check: meaning must survive with colour removed.
- Re-compute after any palette or surface change.
- A pair checked at large-text size must not be used at normal text size.
- Borders and focus indicators are pairs, not decoration; they need 3:1.
- The table stays current with the latest palette and surfaces.

## Procedure

### 1. What it is

WCAG contrast: AA 4.5:1 for normal text and 3:1 for large text and UI components/icons; AAA 7:1 / 4.5:1. Colour must never be the only way to convey meaning, since ~8% of men have some colour-vision deficiency.

### 2. How Hermes applies it

Hermes computes contrast for every pair it emits, rejects light-grey-on-white text, pairs colour with icon/text labels for status, and its judger runs a contrast check before judging a design done.

### 3. What it returns to the stage

- Colour stage: `roles` — the palette roles whose pairs were checked; `contrast_table` — the computed ratio for every pair, with pass or fail against its threshold.
- Theme stage: `default` — the default theme, with its pairs checked; `surfaces` — the surfaces of both themes, each with its checked pairs.

The contrast table is the value both stages record. The colour record carries the ratio for every pair; the theme record carries the checked surfaces of both themes. If a record key is missing, the stage does not complete.

### 4. Good looks like

All body text passes AA, large text/UI pass 3:1, and an error is still understandable in greyscale.

## Pitfalls

- Colour as the only way to convey meaning: an error shown in red alone is unreadable to someone with a colour-vision deficiency, and invisible in greyscale.
- Light-grey-on-white text that passes a casual look but fails the ratio.
- Pairs checked in the light theme only, with the dark theme unchecked.
- A pair computed once for the palette and never re-checked after a colour or surface change.
- Focus indicators that fail 3:1, so keyboard users cannot see where they are.
- Icons and borders treated as decoration and never checked, though they carry meaning too.
- A pair that passes at AA for large text but is used at normal text size, where it needs 4.5:1.
- Status pairs checked for text but not for the icon that carries the same meaning.
- A contrast table recorded for the palette and never updated when the theme surfaces change.
- AAA claimed where only AA was measured.
- A pair that passes in the light theme assumed to pass in the dark theme without computing it.
- An icon checked for contrast but its label left unchecked, so the meaning fails in text form.

## Verification

- Every body-text pair meets 4.5:1; every large-text and UI pair meets 3:1.
- Every pair is checked in both light and dark themes.
- Status meaning is carried by icon or text label as well as colour.
- An error is still understandable in greyscale.
- Focus indicators meet 3:1 on their backgrounds.
- The contrast table is recorded in the colour stage and the checked surfaces in the theme stage.
- No pair is used at a size below the threshold it was checked against.
- The table is current with the latest palette and surfaces.

The skill does the work and the a11y judger checks it, running its own contrast check before judging a design done. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: colour, theme. Returns: `roles`, `contrast_table` (colour stage); `default`, `surfaces` (theme stage). Judger boundary: the a11y judger checks contrast against WCAG 2.2 AA and blocks delivery on failure.
