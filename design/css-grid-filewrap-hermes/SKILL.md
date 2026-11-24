---
name: css-grid
description: "Two-dimensional page structure that reflows cleanly."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, layout]
    category: web
    related_skills: [web-design, flexbox, responsive-design]
    web_designer_stages: [build]
---

# CSS Grid Layout Skill

The two-dimensional CSS layout system for page-level structure: rows and columns together, so a page shell, dashboard, pricing table or gallery reflows as the viewport changes. This skill builds the page skeleton with Grid. It does not handle single-axis alignment inside components — that is the flexbox skill — and it does not set spacing values — that is the spacing-system skill.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- For page shells, dashboards, pricing tables, galleries and any layout needing control on both axes.
- When the build stage needs the page skeleton laid out.
- When a layout must reflow its column count with viewport width without a media query per breakpoint.
- When nested items must align with the outer grid rather than drift out of line.
- When a layout overflows on narrow viewports and needs tracks that share space instead of fixed widths.

It is NOT for nav bars, button groups, card internals or form rows — those are single-axis and belong to flexbox — and it is NOT for judging the finished layout.

## Prerequisites

- The run is active and the coordinator loaded this skill for the build stage.
- The wireframe is approved, so the skeleton follows an agreed structure.
- Tokens are defined, so the grid uses token values rather than hardcoded sizes.
- The page list is known, so the skeleton covers every page shell, not only the home page.

## How to Run

1. Use Grid for the page skeleton: rows and columns together, with named areas where the structure is fixed.
2. Size tracks with fr units and minmax(), so columns share space and never overflow.
3. Use repeat(auto-fit/auto-fill) for responsive grids that reflow column count with viewport width, without a media query per breakpoint.
4. Use subgrid for nested alignment, so items inside a cell line up with the outer grid.
5. Check every viewport width for fixed-width overflow: no horizontal scroll at any width.
6. Check the reflow: a gallery or pricing table must drop columns as the viewport narrows, not squeeze them.
7. Check nested alignment after the reflow: items inside a cell must still line up with the outer grid at each width.
8. Record the built files, the build log and any token drift in the build stage record.
9. Check the page shell at each width: header, content and footer must hold their areas without overflow.
10. Confirm the named areas match the approved wireframe at every breakpoint, not only at desktop width.
11. Check that no track is sized by a hardcoded pixel value outside the tokens.

## Quick Reference

- Grid controls both axes: rows and columns together.
- fr units, minmax(), repeat(auto-fit/auto-fill), named areas, subgrid.
- Browser support: about 97%.
- Responsive grids reflow without a media query per breakpoint.
- No fixed-width overflow; no horizontal scroll.
- Use for page shells, dashboards, pricing tables, galleries.
- Named areas for fixed structures; subgrid for nested alignment.
- Check the reflow at each width: columns drop, they do not squeeze.
- No track is sized by a hardcoded pixel value outside the tokens.
- The named areas match the wireframe at every width.
- The page shell holds its areas without overflow at each width.

## Procedure

### 1. What it is

The two-dimensional CSS layout system for page-level structure — rows and columns together, with fr units, minmax(), repeat(auto-fit/auto-fill), named areas and subgrid (~97% browser support).

### 2. How Hermes applies it

Hermes uses Grid for the page skeleton, auto-fit/minmax for responsive grids without a media query per breakpoint, and subgrid for nested alignment; its judger checks no fixed-width overflow.

### 3. What it returns to the stage

- Build stage: `files` — the built files carrying the grid skeleton; `build_log` — the build record showing the grid was built from tokens; `token_drift` — any hardcoded value that crept in instead of a token, which must be none.

The skeleton is the value the build stage records. The files record carries the skeleton itself; the build log carries the record of how it was built; token drift must be none. If a record key is missing, the stage does not complete.

### 4. Good looks like

A layout that reflows column count with viewport width, aligns nested items, and never causes horizontal scroll.

## Pitfalls

- Fixed-width tracks that overflow on narrow viewports and cause horizontal scroll.
- A media query per breakpoint where auto-fit/minmax would reflow on its own.
- Nested items aligned by eye instead of subgrid, so they drift out of line.
- Grid used for single-axis component alignment, where flexbox is the right tool.
- Named areas that do not match the approved wireframe, so the build diverges from the agreed structure.
- Hardcoded track sizes instead of token values, which the build record flags as token drift.
- A grid that reflows column count but leaves nested items misaligned after the reflow.
- fr units mixed with fixed widths in a way that squeezes one column instead of sharing the space.
- A page shell built with Grid while its galleries and pricing tables fall back to fixed columns.
- Named areas defined once and then overridden per page, so the structure stops being shared.
- A grid that reflows but leaves the page shell's header and footer fixed, so the shell overflows while the content reflows.
- auto-fit used where auto-fill was meant, so empty tracks collapse the layout.

## Verification

- Column count reflows with viewport width; nested items align.
- No horizontal scroll at any width; no fixed-width overflow.
- The grid follows the approved wireframe.
- The built files, build log and token drift are recorded in the build stage record.
- Token drift is none: no hardcoded track sizes in the built files.
- Nested alignment holds after the reflow, not only at the widest viewport.
- The named areas match the wireframe at every width, not only at desktop width.
- The page shell holds its areas without overflow at each width.

The skill does the work and the responsive judger checks reflow and overflow. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: build. Returns: `files`, `build_log`, `token_drift` (build stage). Judger boundary: the responsive judger checks behaviour across viewports; the visual judger checks the layout itself.
