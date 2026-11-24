---
name: spacing-system
description: "Consistent gaps that group related items together."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, layout]
    category: web
    related_skills: [web-design, design-tokens, visual-hierarchy]
    web_designer_stages: [tokens, build]
---

# Spacing System and Whitespace Skill

A consistent spacing scale on a 4px or 8px base, with micro-whitespace inside components and macro-whitespace between sections. Whitespace is an active grouping tool, not wasted space: related items sit closer than unrelated ones. This skill defines the scale and applies it to every layout decision. It does not choose the layout system itself — that is the css-grid and flexbox skills.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- For every layout decision — padding, margins, section gaps, form field grouping.
- When the tokens stage needs the spacing scale encoded, or the build stage needs it applied.
- When a page feels cramped, or when groups are only obvious because of divider lines everywhere.
- When form fields need grouping so related fields sit closer than unrelated ones.
- When a page's gaps were set by eye and the rhythm changes from section to section.

It is NOT for choosing grid versus flexbox, and it is NOT for judging the finished page — the visual judger checks the result.

## Prerequisites

- The run is active and the coordinator loaded this skill for the tokens or build stage.
- The wireframe is approved, so spacing follows an agreed grouping of content.
- The direction stage is complete, so the density of the spacing matches the chosen direction.
- The component inventory is known, so micro-whitespace is set per component rather than per page.

## How to Run

1. Use only scale values: 4, 8, 16, 24, 32, 48, 64px on a 4px or 8px base.
2. Encode the scale as spacing tokens in the tokens stage.
3. Apply micro-whitespace inside components and macro-whitespace between sections.
4. Make related items closer than unrelated ones, following Gestalt proximity: groups form by space before any boxes are added.
5. Check the rhythm: related fields 4–8px apart, groups 16–24px apart, sections 48–64px apart.
6. Check form field grouping the same way: fields that belong together sit 4–8px apart, field groups 16–24px apart.
7. Check sections for breathing room: a cramped section means the macro-whitespace was skipped, not that the content is too long.
8. Record the token path in the tokens stage record, and the built files, build log and token drift in the build stage record.
9. Check the rhythm down the whole page: the same gaps must repeat, not change from section to section.
10. Confirm no gap in the build sits outside the scale, including padding and margins set per component.
11. Check that groups are obvious from space alone, with no divider line doing the grouping work.

## Quick Reference

- Scale: 4/8/16/24/32/48/64px on a 4px or 8px base.
- Related fields: 4–8px apart.
- Groups: 16–24px apart.
- Sections: 48–64px apart.
- Use only scale values; arbitrary pixel values are flagged.
- Micro-whitespace inside components; macro-whitespace between sections.
- Whitespace is an active grouping tool, not wasted space.
- The same rhythm repeats down the whole page.
- Groups are obvious from space alone, with no divider line doing the grouping work.
- Form field grouping follows the same rhythm as the rest of the page.
- Section gaps hold on mobile; sections do not run together.

## Procedure

### 1. What it is

A consistent spacing scale on a 4px or 8px base (4/8/16/24/32/48/64px), with micro-whitespace inside components and macro-whitespace between sections; whitespace is an active grouping tool, not wasted space.

### 2. How Hermes applies it

Hermes uses only scale values, makes related items closer than unrelated ones (Gestalt proximity), and its judger flags arbitrary pixel values and cramped sections.

### 3. What it returns to the stage

- Tokens stage: `tokens_path` — the path to the token file where the spacing scale is encoded.
- Build stage: `files` — the built files carrying the spacing; `build_log` — the build record showing spacing came from tokens; `token_drift` — any arbitrary pixel value that crept in instead of a scale value, which must be none.

The scale is the value the stages record. The tokens record carries the path where the scale lives; the build record carries the files, the log and the drift check. If a record key is missing, the stage does not complete.

### 4. Good looks like

Related fields sit 4-8px apart, groups 16-24px apart, sections 48-64px apart; the page breathes and groups are obvious without divider lines everywhere.

## Pitfalls

- Arbitrary pixel values outside the scale, which the judger flags and which break the rhythm.
- Cramped sections where macro-whitespace was skipped.
- Equal gaps between related and unrelated items, so no grouping is visible.
- Divider lines everywhere to fake grouping that spacing should have done.
- A scale encoded in tokens but ignored in the build, so the build record flags token drift.
- Micro-whitespace skipped inside components, so dense content reads as one block.
- Form fields spaced evenly instead of grouped, so fields that belong together read as unrelated.
- Section gaps set by eye per section instead of from the scale, so the rhythm changes down the page.
- Macro-whitespace used inside a component, which pulls it apart instead of holding it together.
- A scale chosen on the 8px base and then broken with 4px values that are not in it — or the reverse.
- Padding and margins set per component by eye, so the rhythm drifts between components.
- Section gaps that shrink on mobile until the sections run together.

## Verification

- Every gap in the build is a scale value: 4, 8, 16, 24, 32, 48 or 64px.
- Related fields sit 4–8px apart, groups 16–24px apart, sections 48–64px apart.
- Groups are obvious without divider lines everywhere; the page breathes.
- The token path, built files, build log and token drift are recorded in their stage records.
- Token drift is none: no arbitrary pixel values in the built files.
- Form field grouping follows the same rhythm as the rest of the page.
- The rhythm repeats down the whole page, not only on the first section.
- Groups are obvious from space alone, with no divider line doing the grouping work.

The skill does the work and the visual judger checks spacing and grouping. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: tokens, build. Returns: `tokens_path` (tokens stage); `files`, `build_log`, `token_drift` (build stage). Judger boundary: the visual judger checks spacing values and section rhythm.
