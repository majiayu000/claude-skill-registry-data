---
name: semantic-colour
description: "One fixed meaning for every status and action hue."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, colour]
    category: web
    related_skills: [web-design, colour-theory, design-tokens]
    web_designer_stages: [colour, tokens, components]
---

# Semantic Colour Roles Skill

A fixed role system for colour: primary, secondary, a neutral scale, and semantic success, warning, error and info — so the same colour always means the same thing across a site. This skill defines those roles once and reuses them everywhere. It does not build the palette's harmony — that is the colour-theory skill — and it does not check contrast ratios — that is the colour-contrast skill.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- When building a design system, alerts, badges, forms and dashboards where status must be read instantly.
- When the colour stage needs semantic roles recorded, the tokens stage needs them encoded, or the components stage needs them applied.
- When a page invents a new red or green instead of reusing the one already defined.
- When a new alert, badge or button is added and needs its colour from the fixed roles.
- When the same colour means different things on different pages and needs one fixed meaning.

It is NOT for palette harmony, contrast checking, or judging the finished site — the visual judger checks the result and the a11y judger checks contrast.

## Prerequisites

- The run is active and the coordinator loaded this skill for the colour, tokens or components stage.
- A palette exists, so semantic roles are drawn from real colours rather than invented per page.
- The direction stage is complete, so the roles match the chosen direction.
- The component inventory is known, or is being built now, so the roles can be applied to real components.

## How to Run

1. Define the role set once: primary, secondary, a neutral scale of 6–8 shades, and semantic success, warning, error and info.
2. Encode each role as a semantic token (for example color.success, color.error) in the tokens stage.
3. Reuse those tokens for every alert, button and badge; never invent a new red or green per page.
4. Apply the tokens to the component inventory, so each component's states use the same roles.
5. Check that the meaning holds on every page: green always means success, red always means error, primary always means the main action.
6. Check the neutral scale has enough shades: surfaces and borders must be told apart, not collapse into one tone.
7. Check that no colour carries two meanings: a colour used for success on one page must not be the main action on another.
8. Record the roles in the colour stage record, the token path in the tokens stage record, and the inventory in the components stage record.
9. Check every new component against the roles before it is added to the inventory.
10. Confirm warning and error are distinct hues before the inventory is recorded.
11. Re-check the roles after any palette change: a new palette colour must not silently take over a semantic meaning.

## Quick Reference

- Roles: primary, secondary, neutral scale (6–8 shades), semantic success/warning/error/info.
- Semantic tokens: color.success, color.error and the same pattern for the other roles.
- One definition per role, reused on every page.
- Green always means success; red always means error; primary always means the main action.
- Never invent a new red or green per page.
- Apply the roles to every alert, button and badge through the component inventory.
- Warning and error are distinct hues.
- A colour never carries two different meanings on the same site.
- Every new component is checked against the roles before joining the inventory.
- Tokens are named by role, not by look, so a rebrand does not break the meaning.

## Procedure

### 1. What it is

A fixed role system — primary, secondary, neutral scale (6-8 shades), and semantic success/warning/error/info — so the same colour always means the same thing across a site.

### 2. How Hermes applies it

Hermes defines semantic tokens (color.success, color.error etc.) once, reuses them for every alert/button/badge, and never invents a new red or green per page.

### 3. What it returns to the stage

- Colour stage: `roles` — the full role set including the semantic roles; `contrast_table` — the contrast figures for the semantic pairs, which the colour-contrast skill fills in.
- Tokens stage: `tokens_path` — the path to the token file where the semantic roles are encoded.
- Components stage: `inventory` — the component list with each component's states bound to the semantic tokens.

The role set is the value the stages record. The colour record carries the roles; the tokens record carries the path where they are encoded; the components record carries the inventory bound to them. If a record key is missing, the stage does not complete.

### 4. Good looks like

Green always means success, red always means error, primary always means the main action — on every page, without exception.

## Pitfalls

- A new red or green invented per page, so the same status reads differently in different places.
- Semantic roles defined but never encoded as tokens, so components fall back to hardcoded values.
- A colour used for success on one page and for the main action on another, which destroys the fixed meaning.
- A neutral scale with too few shades, so surfaces and borders cannot be told apart.
- Roles recorded in the colour stage but never applied to the component inventory.
- Status shown by colour alone, with no icon or text label — see the colour-contrast skill.
- A semantic role added for one alert and never reused, so the role set grows per page instead of staying fixed.
- Warning and error given the same hue, so the two statuses cannot be told apart.
- The primary role used for decoration, so the main action no longer stands out.
- Semantic tokens defined with look-based names instead of role names, so a rebrand breaks the meaning.
- A semantic role redefined after the tokens were encoded, leaving components on the old meaning.
- The neutral scale checked for count but never for whether surfaces and borders can be told apart.

## Verification

- Green means success, red means error and primary means the main action on every page, without exception.
- Every alert, button and badge uses the defined semantic tokens.
- No page invents a new red or green.
- The roles, token path and inventory are recorded in their stage records.
- Warning and error are distinct hues.
- No colour carries two different meanings anywhere on the site.
- The neutral scale has 6–8 shades, enough to tell surfaces and borders apart.
- Every new component is checked against the roles before joining the inventory.

The skill does the work and the visual judger checks role use. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: colour, tokens, components. Returns: `roles`, `contrast_table` (colour stage); `tokens_path` (tokens stage); `inventory` (components stage). Judger boundary: the visual judger checks that semantic roles are used consistently; the a11y judger checks the contrast of the semantic pairs.
