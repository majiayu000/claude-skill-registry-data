---
name: wireframing
description: "Greyscale structure agreed before any visual design."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, wireframe]
    category: web
    related_skills: [web-design, information-architecture, prototyping]
    web_designer_stages: [wireframe]
---

# Wireframing Skill

Draw low-fidelity, usually greyscale layouts that show what goes where and in what order, so structure, priority and behaviour are agreed before any visual design. This skill covers wireframes for key screens on mobile and desktop. It does not cover visual design — colour, imagery and brand styling come later — and it does not cover clickable prototypes, which have their own skill. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- After IA and journeys, before visual design, for key screens on mobile and desktop.
- When the team must agree on content order and priority without debating shades of blue.
- When empty and error states must be decided while they are still cheap to change.
- When a screen's behaviour — what happens on interaction — must be agreed before it is built.
- When a desktop and a mobile form of the same screen must be agreed together.
- Not for polishing a layout: a wireframe that carries brand styling has stopped being a wireframe.
- Not as a substitute for the IA stage: wireframes need the sitemap and flows first.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- IA is done: the sitemap and the flows say which screens exist and in what order.
- The top tasks are known, so each wireframe follows a real task rather than a generic page.
- The wireframe gate is the checkpoint: structure is agreed here, before visual design begins.

## How to Run

1. Take the sitemap and the flows, and list the key screens to wireframe on mobile and desktop.
   - Every key screen gets both a mobile and a desktop wireframe.
   - A screen with no task behind it is not wireframed; the task list decides the screens.
2. Produce a plain wireframe first, in code or as a described layout: greyscale, no colour, no imagery, no brand styling.
   - Boxes and labels stand in for the real content, in the real order.
   - Nothing in the wireframe depends on styling to be understood.
3. Show structure, priority and behaviour in each wireframe: what goes where, in what order, and what happens on interaction.
   - The primary action and the primary content lead; supporting content follows.
   - Each interactive element notes what it does when used.
4. Decide priorities, content order, and empty and error states inside the wireframe.
   - An empty list, a failed load and a form error each get their wireframe state.
   - The states are decided now, while they are cheap to change.
5. Get the structure agreed at the wireframe gate before any visual design begins.
   - The gate sends the wireframe and IA card for approval; visual work waits for that decision.
6. Record the wireframe pages in the stage record, each with its sections.
   - Every page carries a non-empty sections list, so the record matches the machine contract.
7. Re-check after any fix, and record what changed.
   - A changed page is read again without styling before the stage closes.
   - The pages recorded are the ones the gate approved, not earlier drafts.

## Quick Reference

- Fidelity: low, usually greyscale.
- Content: structure, priority and behaviour — without colour, imagery or brand styling.
- Screens: key screens on mobile and desktop.
- Decided in the wireframe: priorities, content order, empty states, error states.
- Gate: structure agreed before visual design; no debate about shades of blue at wireframe stage.
- Record: `wireframe.pages` is a non-empty list; every page carries a non-empty `sections` list.
- Boxes and labels: stand in for the real content, in the real order.
- Behaviour: noted for every interactive element.
- States: empty and error states decided in the wireframe.
- Viewports: key screens on mobile and desktop.
- Gate: structure agreed before visual design begins.

## Procedure

### 1. What it is

Low-fidelity, usually greyscale layouts showing what goes where and in what order — structure, priority and behaviour — without colour, imagery or brand styling, so discussion stays on content and flow.

### 2. How Hermes applies it

Hermes produces a plain wireframe first (in code or as a described layout), gets the structure agreed, and only then applies visual design; it does not debate shades of blue at wireframe stage.

### 3. What it returns to the stage

- `wireframe` stage record: `pages` is a non-empty list, and every page carries a non-empty `sections` list — the structure, priority and behaviour of that screen, including its empty and error states.

### 4. Good looks like

A wireframe that can be read without any styling; priorities, content order and empty/error states are already decided in it.

## Pitfalls

- Colour or brand styling in the wireframe: discussion drifts to shades of blue while structure stays undecided.
- A wireframe for one viewport only: the mobile structure is invented later, under build pressure, and diverges from the desktop.
- Empty and error states left out: the build meets them for the first time and invents them on the spot.
- Content order undecided: the wireframe shows boxes without saying which content leads, so the build guesses the priority.
- Wireframing before IA: screens drawn with no sitemap and no flows behind them, so the set of screens is a guess.
- Treating the wireframe as the design: visual design skipped because the wireframe "looks done" in greyscale.
- Behaviour left undescribed: an element that looks interactive with no note of what it does, so the build guesses.
- A wireframe page with no sections list: the record fails the machine contract, and the stage refuses to complete.
- Wireframing every screen at once: the key screens are lost among minor ones, and the gate reviews a pile instead of a structure.

## Verification

- Every wireframe page can be read without any styling, and priorities and content order are visible in it.
- Every key screen exists for mobile and desktop.
- Empty and error states are decided in the wireframe, not left to the build.
- Behaviour is noted for every interactive element.
- The structure was agreed at the wireframe gate before visual design began.
- The stage record holds a non-empty `pages` list, and every page carries a non-empty `sections` list.
- Boxes and labels stand in for the real content, in the real order, and nothing depends on styling to be understood.
- No wireframe page carries colour, imagery or brand styling.
- The wireframe covers the key screens only; minor screens do not crowd the gate review.
- Behaviour is noted for every interactive element.
- The stage record carries the pages the gate approved, not earlier drafts.
- The visual judger checks hierarchy and reading order on the wireframe; the wireframe gate records the human decision. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: wireframe. Returns: `wireframe.pages` (non-empty list; every page with a non-empty `sections` list covering structure, priority, behaviour, empty and error states). Judger boundary: visual judger checks hierarchy and reading order; the wireframe gate is the human checkpoint for the agreed structure.
