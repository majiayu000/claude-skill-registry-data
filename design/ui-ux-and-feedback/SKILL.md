---
name: ui-ux-and-feedback
description: Use when designing, auditing, or generating a HUD, menu system, or feedback vocabulary for any genre — information hierarchy, diegetic vs. non-diegetic classification, cognitive load budgeting, feedback channel design, menu flow, input modality, and accessibility. Also use to diagnose a UI that is cluttered, that players ignore, that confuses state, or where players miss critical information. Triggers on "UI", "UX", "HUD", "menus", "interface", "diegetic UI", "non-diegetic", "information hierarchy", "cognitive load", "the UI is cluttered", "players miss important info", "feedback vocabulary", "onboarding UI", "accessibility", "colorblind", "button remapping", "contextual HUD", "minimap", "waypoints", "icon soup", "menu hell", "screen shake", "feedback loop", "affordances", "signifiers".
---

# UI/UX & Information Design

How to give players exactly the information they need to decide right now — no more, no less — and communicate every game-state change through channels they can read under pressure.

> **Tier:** universal craft (→ `gamestack-core`). Applies to every genre and every game. The feel of individual UI elements (squash on button press, easing on transition) lives in `game-feel-and-juice`, which cites *up* to this skill; this skill owns the information architecture and UX layer.

## When to use this

- Classifying each HUD element on the Fagerholt axes (diegetic / non-diegetic / spatial / meta) and writing a HUD spec contract
- Auditing why players miss critical state, pause constantly to check info, or describe the UI as cluttered or confusing
- Designing or reviewing the feedback vocabulary (visual / audio / haptic / camera) for a mechanic set
- Specifying menu depth, input modality, navigation flow, and settings infrastructure
- Generating a reflowable, data-driven HUD spec from a mechanic inventory

## Scope

This skill owns **information architecture and UX** — what to show, when, in what form, and how to communicate state change. Adjacent concerns live in sibling skills:

- The *feel* of UI elements — button squish, easing curves, transition timing, UI juice → `game-feel-and-juice` (owns the feedback layer; this skill sets what to communicate, that skill sets how good it feels)
- Visual contrast, signal color, silhouette, and legibility at the pixel level → `art-direction-and-readability`
- Tutorial and first-play onboarding sequencing (the *teaching* layer, not the HUD layer) → `onboarding-and-teaching`
- Reward structure, flow, and motivation theory underneath the feedback → `game-design-fundamentals`
- Session rhythm and how menu transitions pace the experience → `pacing-and-the-player-journey`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: the Fagerholt–Lorentzon four-type taxonomy (diegetic / non-diegetic / spatial / meta); information hierarchy and cognitive load (Sweller, Hodent); feedback and game-state communication; menu and navigation flow / input modality; accessibility-adjacent UX. Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural / headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The one idea to anchor on

> **The HUD's only job is to give the player what they need to decide right now.** Every element that isn't serving the current decision is extraneous cognitive load — a tax the player pays with attention and performance (Sweller 1988; Hodent 2017). Show Tier-1 state (health, ammo, objective) permanently at the periphery; surface Tier-2 state on context; hide Tier-3 state in menus. Diegetic where the world can carry it plausibly; non-diegetic where it can't; never pure-diegetic for data that changes faster than world-object animation can track.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
