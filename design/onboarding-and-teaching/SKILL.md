---
name: onboarding-and-teaching
description: Use when designing, reviewing, or generating the introduction to ANY mechanic in ANY genre — the four-beat teaching pattern (introduce→test→combine→twist), show-don't-tell level design, progressive disclosure and scaffolding, the mechanic dependency graph, FTUE (first-time user experience), early retention funnels, and the skill-atom ramp. Also use to diagnose tutorials that are too long, that players skip, or where players quit before reaching the core loop. Triggers on "onboarding", "tutorial", "tutorialization", "teach the player", "FTUE", "first-time user experience", "new player experience", "players quit early", "players don't understand the mechanic", "tutorial ramp", "skill ramp", "progressive disclosure", "show don't tell", "safe space introduction", "information overload", "tutorial tax".
---

# Onboarding & Teaching

How to introduce *any* mechanic — in any genre, on any platform — so that instruction is invisible, comprehension is measurable, and the player's first hours build competence instead of confusion.

> **Tier:** universal craft (→ `gamestack-core`). Applies to every genre and every game. The spatial side of teaching (teaching through space) lives in `level-design`; the early difficulty curve lives in `difficulty-and-balancing`.

## When to use this

- Designing a mechanic's first appearance: safe-space room, skill gate, combination encounter, twist
- Reviewing a tutorial for working-memory overload, anti-patterns, or implicit/explicit balance
- Building a FTUE (first-time user experience) with a funnel and a measurable early win
- Generating a teaching ramp for a procedurally defined mechanic set

## Scope

This skill owns **how mechanics are introduced and learned**. Adjacent concerns live in sibling skills:
- Flow theory, intrinsic motivation, and the skill atom cycle → `game-design-fundamentals`
- Teaching through spatial layout, landmarks, and affordances → `level-design`
- Difficulty curve and the early challenge ramp → `difficulty-and-balancing`
- Tutorial UI, tooltip and HUD design, and feedback overlays → `ui-ux-and-feedback`
- First-hour pacing and session arc → `pacing-and-the-player-journey`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: the four-beat teaching pattern (introduce→test→combine→twist); show-don't-tell and implicit tutorial methods; progressive disclosure, scaffolding, and the mechanic dependency graph; FTUE and early retention design; and the five named anti-patterns. Every rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The one idea to anchor on

> **The best tutorial is a level, not a pop-up.** Working memory holds ~3 novel items; exceed it and the mechanic goes untaught even if displayed. Teach one thing at a time — safe and consequence-free first, gated for mastery second, combined with a prior mechanic third, twisted into an unexpected application fourth. Every text box you add is a tacit admission that the level design failed to communicate it; every pop-up a player can skip is instruction that will not be received.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
