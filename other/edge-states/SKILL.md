---
name: edge-states
description: "Loading, empty and error states for every data view."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, states]
    category: web
    related_skills: [web-design, empty-states, component-states]
    web_designer_stages: [components, build]
---

# Error, Loading and Edge States Skill

This skill applies the four-states rule: every data view has loading, populated, empty and error states. It covers skeletons, progress, translated error copy, and the 404/500/403 pages. It does not cover the empty state's headline and CTA design in detail — the empty-states skill owns that — and it does not cover form field validation — the form-validation skill owns that. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For every async surface, route and API-dependent widget.
- When a view fetches data, paginates, or can fail: lists, dashboards, search, detail pages, and the site's own 404/500/403 pages.
- When a slow load currently shows a frozen spinner or nothing at all.

It is NOT for:

- The empty state's content per origin — that is empty-states.
- Form field errors — that is form-validation.
- The offline path as a whole product decision; it covers the offline state's design, not whether the product works offline.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The components inventory lists the data views, so each view's four states can be attached to its component.
- The build stage is in progress or complete, so the states can be checked in the built views.

## How to Run

1. List every data view and give it all four states: loading, populated, empty, error.
2. For loading, use skeletons shaped like the content, not bare spinners; show progress after ~3s.
3. For errors, name the failure in the user's words and offer a recovery: retry, search, or home. Translate codes — '500' becomes 'Couldn't load projects. Try again.'
4. Distinguish recoverable/transient errors from irrecoverable/permission errors, and give each the recovery it allows.
5. Design the 404/500/403 pages as brand moments with a path forward: search and popular pages on a 404, retry on a 500.
6. Never show a stack trace or raw 'undefined' to the user.
7. Record the four states per view in the components inventory and the build log, then hand the work to the judger; do not grade it here.

## Quick Reference

- Four-states rule: loading, populated, empty, error — for every data view.
- Loading: skeletons shaped like the content, over bare spinners; progress shown after ~3s.
- Errors: named in the user's words, with a recovery (retry, search, home).
- Codes translated: '500' becomes 'Couldn't load projects. Try again.'
- Never a stack trace or raw 'undefined'.

## Procedure

### 1. What it is

The four-states rule: every data view has loading, populated, empty and error states. Loading uses skeletons (shape of the content) over bare spinners, shows progress after ~3s; errors name the failure in the user's words with a recovery (retry, search, home), 404/500/403 as brand moments with a path forward; never show a stack trace or raw 'undefined'.

### 2. How Hermes applies it

Hermes designs all four states per view, uses skeleton screens, translates codes ('500' becomes 'Couldn't load projects. Try again.'), distinguishes recoverable/transient from irrecoverable/permission errors, and its judger checks the 404 and offline paths.

### 3. What it returns to the stage

- `components` stage — `inventory`: each data-view component records its four states — loading (skeleton shape), populated, empty, and error (message and recovery).
- `build` stage — `files`: the built views carry all four states. `build_log`: notes the states built per view and the translated error copy. `token_drift`: nothing new; states add no tokens.

### 4. Good looks like

A failed load offers a retry and a way forward; a 404 offers search and popular pages; a slow load shows progress, not a frozen spinner.

## Pitfalls

- A view shipped with only its populated state, so a slow or failed load shows a blank area or a crash.
- A bare spinner with no shape of the content and no progress after ~3s — the user cannot tell whether anything is happening.
- Raw codes ('500', 'undefined', a stack trace) shown to the user instead of a translated message.
- An error with no recovery: no retry, no search, no way home.
- Treating a recoverable transient failure the same as a permission failure, so the user is offered a retry that can never work — or denied one that would.
- A 404 that is a dead end instead of a brand moment with search and popular pages.

## Verification

- Every data view has all four states: loading, populated, empty, error.
- Loading uses skeletons; progress appears after ~3s on slow loads.
- Every error names the failure in the user's words and offers a recovery; no stack trace or raw 'undefined' survives.
- The 404 and offline paths exist and offer a way forward.
- The visual judger checks the four states exist per view and the 404 and offline paths; the skill does the work and the judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: components, build. Returns: `components` — `inventory`; `build` — `files`, `build_log`, `token_drift`. Judger boundary: visual judger checks the four states per view and the 404 and offline paths.
