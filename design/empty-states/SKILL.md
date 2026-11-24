---
name: empty-states
description: "No-data screens with one clear next action."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, states]
    category: web
    related_skills: [web-design, edge-states, onboarding-design]
    web_designer_stages: [wireframe, components]
---

# Empty States Skill

This skill designs the surfaces for 'no data yet': first-run, no-results, cleared, and permission-denied, each with its own headline, explanation, and one clear next action. It covers empty as a designed state, not an error. It does not cover loading spinners, failed loads, or error recovery — the edge-states skill owns those. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For every list, table, dashboard, search result and first-run screen.
- When a data surface can be empty for any reason: nothing created yet, filters that match nothing, everything deleted, or access not granted.
- At wireframe time, at the same time as the populated state — never after the build.

It is NOT for:

- Loading states or failed loads — that is edge-states.
- Onboarding flows in full — onboarding-design owns the first-run journey; this skill owns the empty surface it starts from.
- Error copy or recovery paths — that is edge-states.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The wireframe lists the data surfaces on each page, so every surface gets its empty state designed alongside its populated state.
- The origin of each empty state is known: first-run, no-results, cleared, or permission-denied.

## How to Run

1. List every data surface on the page: lists, tables, dashboards, search results, first-run screens.
2. For each surface, name its origin: first-run (onboarding, point at first win), no-results (clear filters/search), cleared (user deleted everything), or permission-denied.
3. Design the empty state at the same time as the populated state, in the wireframe.
4. Give each empty state its own headline, its own explanation, and one clear next action — one CTA, not several.
5. Never return a blank box or null for an empty surface.
6. Record the empty states in the wireframe pages and the components inventory, then hand the work to the judger; do not grade it here.

## Quick Reference

- Four origins: first-run, no-results, cleared, permission-denied.
- Each empty state: its own headline, its own explanation, one CTA.
- Empty is a state, not an error — never styled or worded like a failure.
- Never a blank box or null.

## Procedure

### 1. What it is

Designed surfaces for 'no data yet' — distinct by origin: first-run (onboarding, point at first win), no-results (clear filters/search), cleared (user deleted everything), permission-denied — each with its own headline, explanation and one CTA; empty is a state, not an error.

### 2. How Hermes applies it

Hermes designs the empty state for every data surface at the same time as the populated state, picks the shape by origin, gives it one clear next action, and never returns a blank box or null.

### 3. What it returns to the stage

- `wireframe` stage — `pages`: each wireframe page records the empty state for every data surface on it, with the origin, headline, explanation, and single CTA.
- `components` stage — `inventory`: the empty-state variants are listed as components, one per origin, with their headline, explanation, and CTA recorded.

### 4. Good looks like

A new user sees what to do first, not an apology; a filtered-to-zero user sees how to get results back; neither looks like a bug.

## Pitfalls

- A blank box or null where an empty state should be — the user cannot tell whether the page loaded or failed.
- One generic empty message for every origin, so a filtered-to-zero user gets onboarding copy and a new user gets a filter hint.
- Treating empty as an error: red styling, an apology, or a failure tone for a surface that simply has no data yet.
- More than one competing CTA, so the user cannot tell what the next action is.
- An empty state designed after the build, when the populated state has already claimed all the space.

## Verification

- Every data surface has a designed empty state, recorded in the wireframe alongside the populated state.
- Each empty state's shape matches its origin: first-run points at the first win, no-results offers a way back to results, cleared explains what happened, permission-denied explains the block.
- Each empty state has one headline, one explanation, and one CTA — and no blank box or null survives.
- The visual judger checks the empty states exist and read as designed states, not errors; the skill does the work and the judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: wireframe, components. Returns: `wireframe` — `pages`; `components` — `inventory`. Judger boundary: visual judger checks empty states exist and read as designed states.
