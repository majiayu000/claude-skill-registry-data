---
name: design-tokens
description: "Named values as the single source of truth."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, tokens]
    category: web
    related_skills: [web-design, design-systems, dark-mode]
    web_designer_stages: [tokens]
---

# Design Tokens Skill

Design tokens are named, curated values for recurring decisions, held as a single source of truth. This skill covers encoding every repeated value as a token in three tiers — primitive, semantic, component — so a change in one place updates every screen. It does not hardcode values in components. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- Whenever a value repeats — colours, spacing, type sizes — and whenever theming (light/dark) is needed.
- At the tokens stage, before the build, so the build consumes tokens only.
- When a rebrand or theme change is needed: the change is a token edit, not a page-by-page hunt.
- When two screens use the same value and should stay in step with each other.
- When a value is about to be copied into a second component and should be named once instead.

It is not for one-off values that genuinely occur once and carry no meaning elsewhere. It is not a second copy of the values in the build: the token set is the source, and the build reads it.

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- Font, colour and theme decisions are settled, so tokens encode decisions already made rather than guessing them.
- The token file location is known: the tokens stage record holds `tokens_path`.
- The design-systems skill is available for the foundations the tokens form.
- Both themes are in scope where theming is needed, so the token set holds the light and dark values together.

## How to Run

1. List every value that repeats: colour, type, spacing, radius, shadow, motion.
2. Encode each as a primitive token first: the raw value, named by what it is (for example `color.blue.500`).
3. Build the semantic layer on top: tokens named by purpose (for example `color.action.primary`), each pointing at a primitive.
4. Build the component layer: tokens named for the component and state that consume them, each pointing at a semantic token.
5. Replace every hardcoded value in the build with a token reference; no raw hex or magic number stays in markup.
6. Change a value by editing the token, once, and confirm every screen that consumes it updates.
7. Check the build for token drift after the change: any raw hex or arbitrary spacing that has crept in is replaced with a token reference.
8. Record the token file path in the tokens stage record, so the build stage can measure drift against it.
9. Name a new token by its role before assigning its value, so the name survives a value change.
10. When a value is used in two places, confirm both places read the same token rather than two copies of the value.
11. After any token change, walk the screens that consume it and confirm they updated together.
12. Keep the token file as the only place values live: a value copied into a component is a value that will drift.

## Quick Reference

- Layers: primitive (raw value), semantic (purpose), component — three tiers.
- Primitive example: `color.blue.500`.
- Semantic example: `color.action.primary`.
- Format: ideally W3C Design Tokens JSON.
- Rule: no raw hex or magic numbers in markup; no hardcoded spacing in components.
- Effect: a rebrand or theme change is a token edit, not a page-by-page hunt.
- Naming: by role or purpose, never by look — so a theme change does not break the name.
- Drift check: raw hex or arbitrary spacing in the build is token drift, flagged and replaced.
- Naming: role first, value second — the name survives a value change.
- Shared values: two uses read the same token, never two copies of the value.
- Source rule: the token file is the only place values live.

## Procedure

### 1. What it is

Named, curated values for recurring decisions — colour, type, spacing, radius, shadow, motion — in primitive (raw value, e.g. color.blue.500) and semantic (purpose, e.g. color.action.primary) layers, as a single source of truth, ideally in W3C Design Tokens JSON.

### 2. How Hermes applies it

Hermes encodes every repeated value as a token, never hard-codes hex/spacing in components, and changes a value in one place so every screen updates; its judger flags raw hex or arbitrary spacing (token drift).

### 3. What it returns to the stage

The tokens stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `tokens_path`. This skill's work fills that key with the path to the token file, and the file itself holds the three tiers: primitive tokens with raw values, semantic tokens named by purpose, and component tokens for the states that consume them. The build stage later records `token_drift` against this set, so any raw hex or arbitrary spacing that slips into the build is measured against the tokens recorded here. A token set that leaves a repeated value hardcoded in a component is incomplete.

The record is the contract for the build: the build consumes the tokens at the recorded path and nothing else. Where a theme needs both light and dark values, the file holds both sets under the same semantic names, so a theme change is a switch of values behind one name rather than a second set of names.

The three tiers exist so that a change lands in exactly one place: a raw value changes in a primitive, a purpose changes in a semantic token, a component's use changes in a component token. Skipping a tier collapses that separation, and the next change touches every consumer instead of one token. The record therefore holds all three tiers, and a token set missing a tier is incomplete even when every value is present.

### 4. Good looks like

No raw hex or magic numbers in markup; a rebrand or theme change is a token edit, not a page-by-page hunt.

A token set that a rebrand can be done through is a token set that did its job. The single edit is the test, not the file's length. Where a value still lives outside the tokens, the token set is incomplete, and the build will drift at exactly that point. That is why the drift check runs after every change, not once at the start.

## Pitfalls

- Hardcoding a hex value or a spacing value in a component instead of consuming a token.
- Naming tokens by look (a colour value) instead of by role or purpose, so a theme change breaks the name.
- Skipping the semantic layer and pointing components straight at primitives, so a purpose change means touching every component.
- Token drift: raw hex or arbitrary spacing creeping into the build after the tokens were defined.
- Keeping a token file that the build does not actually read.
- Encoding decisions in tokens before the font, colour and theme decisions are settled, so the tokens encode guesses.
- Holding light and dark values under different names, so a theme change means renaming rather than switching values.
- Copying a value into a component instead of reading the token.
- Naming a token by its value, so the name breaks when the value changes.
- Changing a token without walking the screens that consume it.

## Verification

- Every repeated value is a token; no raw hex or magic number remains in markup.
- The three tiers are present: primitive, semantic, component.
- Editing one token updates every screen that consumes it.
- The token file at the recorded path is the file the build reads.
- Light and dark values share semantic names where both themes exist.
- A new token is named by role before its value is assigned.
- Two uses of one value read the same token.
- After a token change, the consuming screens are walked and confirmed updated.
- The visual judger checks the related rules and flags token drift. The skill does the work and the judger checks it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: tokens. Returns: tokens stage-record key `tokens_path`. Judger boundary: visual judger checks the related token-drift rules.
