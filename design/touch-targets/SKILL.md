---
name: touch-targets
description: "Controls large enough to hit first time on touch."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, mobile]
    category: web
    related_skills: [web-design, responsive-design, component-states]
    web_designer_stages: [components, build]
---

# Touch Targets and Mobile Ergonomics Skill

This skill makes targets large enough to hit reliably on touch: the WCAG 2.2 minimum of 24x24 CSS px, with 44x44px as the widely used touch minimum, thumb-zone placement for primary actions, adequate spacing between targets, and no hover-only controls on touch. It covers the sizing and placement of every tappable control. It does not cover responsive layout in general — the responsive design work owns that — and it does not cover visual styling of the controls. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For all buttons, links, icon buttons and form controls on touch devices.
- When a component is built with a small hit area, or when two targets sit close together.
- When a control currently works only on hover and has no touch equivalent.

It is NOT for:

- Responsive layout, breakpoints, or reflowing grids — that is the responsive stage's work.
- The visual design of buttons and links — that is the components and tokens stages.
- Desktop-only pointer behaviour; it governs touch, where the finger is the pointer.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The components inventory lists the interactive controls, so each one's hit area can be recorded.
- The build stage is in progress or complete, so targets can be checked at 360px width in the built pages.

## How to Run

1. Give every button, link, icon button, and form control a hit area of at least 24x24 CSS px, the WCAG 2.2 minimum.
2. Aim for 44x44px as the touch minimum for icon buttons and primary controls (Apple/Nielsen guidance).
3. Reach 44x44px with padding, not just a larger icon — the hit area is what matters, not the glyph.
4. Place primary CTAs in the thumb zone on mobile.
5. Space adjacent targets so the wrong one is not hit.
6. Remove hover-only controls on touch: every action available on hover must be reachable by tap.
7. Record the hit areas in the components inventory and the build log, then hand the work to the judger; do not grade it here.

## Quick Reference

- WCAG 2.2 minimum: 24x24 CSS px.
- Widely used touch minimum: 44x44px (Apple/Nielsen guidance).
- Icon buttons: 44x44px hit areas via padding, not just a larger icon.
- Primary CTAs: thumb-zone placement on mobile.
- Spacing: adequate between adjacent targets.
- No hover-only controls on touch.

## Procedure

### 1. What it is

Targets large enough to hit reliably: WCAG 2.2 minimum 24x24 CSS px, with 44x44px as the widely used touch minimum (Apple/Nielsen guidance); thumb-zone placement for primary actions, adequate spacing between targets, no hover-only controls on touch.

### 2. How Hermes applies it

Hermes gives icon buttons 44x44px hit areas via padding (not just a larger icon), places primary CTAs in the thumb zone on mobile, spaces adjacent targets, and its judger checks targets at 360px width.

### 3. What it returns to the stage

- `components` stage — `inventory`: each interactive component records its hit area, its spacing from neighbours, and whether it depends on hover.
- `build` stage — `files`: the built pages carry the hit areas and thumb-zone placement. `build_log`: notes the target sizes applied per component. `token_drift`: nothing new; targets add no tokens.

### 4. Good looks like

Every control can be tapped first time without zooming; no two targets are so close that the wrong one is hit.

## Pitfalls

- A large icon on a small hit area: the glyph looks tappable, the target is not.
- Targets below the 24x24px WCAG 2.2 minimum, or below 44x44px where touch is the primary input.
- Adjacent targets so close that the wrong one is hit.
- Primary CTAs placed outside the thumb zone on mobile, forcing a stretch or a second hand.
- Hover-only controls — menus, tooltips, or actions that have no tap equivalent on touch.
- Checking targets only at desktop width, where a 24px target is easy to hit with a pointer and hard with a finger.

## Verification

- Every control meets the 24x24px WCAG 2.2 minimum; icon buttons and primary controls reach 44x44px via padding.
- Every control can be tapped first time without zooming at 360px width.
- No two targets are so close that the wrong one is hit; primary CTAs sit in the thumb zone.
- No hover-only control survives on touch.
- The responsive judger checks targets at 360px width; the skill does the work and the judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: components, build. Returns: `components` — `inventory`; `build` — `files`, `build_log`, `token_drift`. Judger boundary: responsive judger checks targets at 360px width.
