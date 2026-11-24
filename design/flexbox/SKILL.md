---
name: flexbox
description: "Single-axis alignment inside components and groups."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, layout]
    category: web
    related_skills: [web-design, css-grid]
    web_designer_stages: [build]
---

# Flexbox Component Layout Skill

The one-dimensional CSS layout system for distributing space along a row or a column: nav bars, button groups, card internals, form rows and centring. This skill aligns content inside components and groups. It does not build the two-dimensional page skeleton — that is the css-grid skill — and it does not set spacing values — that is the spacing-system skill.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- Inside components and for single-axis alignment.
- For nav bars, button groups, card internals, form rows and centring.
- When the build stage needs alignment, wrapping and gap inside Grid cells.
- When content of different lengths must align cleanly in the same component.
- When a component's content wraps and must reflow gracefully instead of clipping.

It is NOT a substitute for a two-dimensional page grid, and it is NOT for judging the finished layout.

## Prerequisites

- The run is active and the coordinator loaded this skill for the build stage.
- The wireframe is approved, so component alignment follows an agreed structure.
- Tokens are defined, so gaps and alignment use token values rather than hardcoded sizes.
- The component inventory is known, so alignment is set per component, not per page.

## How to Run

1. Use Flexbox inside Grid cells for alignment, wrapping and gap.
2. Choose flex versus grid by dimensionality: one axis means flexbox, two axes means Grid.
3. Let content wrap gracefully with gap, so longer content reflows instead of clipping.
4. Avoid float and negative-margin hacks for alignment.
5. Check alignment at short and long content lengths: nav, buttons and card content must align cleanly at any content length.
6. Check wrapping at the longest realistic content: a button group or form row must reflow, not clip or overflow.
7. Check centring the same way: centred content must stay centred when its length changes.
8. Record the built files, the build log and any token drift in the build stage record.
9. Check the nav bar at the longest labels: it must wrap or reflow, never clip a label.
10. Confirm the gap between items comes from the tokens, not from a hardcoded value.
11. Check card internals at short and long content: the same card must align cleanly either way.

## Quick Reference

- Flexbox controls one axis: a row or a column.
- Use for nav bars, button groups, card internals, form rows, centring.
- Wrapping is graceful, not clipped; gap separates items.
- Never float or negative-margin hacks for alignment.
- Choose flex versus grid by dimensionality.
- Use inside Grid cells for alignment, wrapping and gap.
- Alignment must hold at any content length, short or long.
- Check the nav bar at the longest labels and the card at the longest content.
- The gap between items comes from the tokens, not from a hardcoded value.
- The nav bar wraps or reflows at the longest labels, never clipping one.
- Card internals align the same way at short and long content.

## Procedure

### 1. What it is

The one-dimensional CSS layout system for distributing space along a row or column — nav bars, button groups, card internals, form rows and centring.

### 2. How Hermes applies it

Hermes uses Flexbox inside Grid cells for alignment, wrapping and gap, chooses flex vs grid by dimensionality, and avoids float/negative-margin hacks.

### 3. What it returns to the stage

- Build stage: `files` — the built files carrying the flexbox component layouts; `build_log` — the build record showing the layouts were built from tokens; `token_drift` — any hardcoded value that crept in instead of a token, which must be none.

The component layouts are the value the build stage records. The files record carries the layouts themselves; the build log carries the record of how they were built; token drift must be none. If a record key is missing, the stage does not complete.

### 4. Good looks like

Nav, buttons and card content align cleanly at any content length; wrapping is graceful, not clipped.

## Pitfalls

- Flexbox used as a substitute for a two-dimensional page grid, which forces hacks to control the second axis.
- Clipped content where wrapping should have been graceful.
- Float or negative-margin hacks for alignment, which break when content length changes.
- Alignment that holds at one content length and breaks at another.
- Hardcoded gaps instead of token values, which the build record flags as token drift.
- A component aligned by eye in one place and by flexbox in another, so the same component looks different across pages.
- A nav bar that aligns at short labels and breaks when a label gets longer.
- A button group that clips instead of wrapping when the buttons do not fit one row.
- Centring done with margins instead of flexbox, which fails when the content length changes.
- Card internals aligned per card instead of by the shared component, so cards drift apart.
- A form row that wraps but leaves its labels behind, so the wrapped fields lose their meaning.
- Gap set per component by eye instead of from the tokens, so spacing drifts between components.

## Verification

- Nav, buttons and card content align cleanly at short and long content lengths.
- Wrapping is graceful, never clipped.
- No float or negative-margin hacks in the built files.
- The built files, build log and token drift are recorded in the build stage record.
- Token drift is none: no hardcoded gaps in the built files.
- Centring holds when content length changes.
- The nav bar wraps or reflows at the longest labels, never clipping one.
- Card internals align the same way at short and long content.

The skill does the work and the visual judger checks alignment. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: build. Returns: `files`, `build_log`, `token_drift` (build stage). Judger boundary: the visual judger checks component alignment and wrapping; the responsive judger checks behaviour across viewports.
