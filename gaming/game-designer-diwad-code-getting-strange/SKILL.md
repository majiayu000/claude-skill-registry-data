---
name: game-designer
description: "Game concept and mechanics design. Invoked by game-orchestra when no design document exists. Covers genre, mechanics, progression, content mapping, and architecture decisions for canvas/DOM/hybrid games."
---

<!-- EXPECTED GATES: 6 -->

# Game Designer

Guides the design of a web game — concept, mechanics, progression, and
content structure.

## When Invoked

By game-orchestra when no design document exists in the project.

## STEP 1 — Research and Brief

Understand the brief — What kind of game? Who is it for? What should
players learn or experience?

- Identify genre and theme
- Identify target audience and age range
- Research 2-3 reference games in the genre
- List candidate mechanics that fit the brief
- Learning objectives (if educational)
- Core emotional experience (fun, curiosity, challenge, calm)

### GATE 1 OUTPUT
> STEP 1 COMPLETE: Genre is [genre]. Reference games: [list]. Target audience: [audience]. Candidate mechanics: [list].

## STEP 2 — Core Mechanics Design

Design the core mechanics that drive gameplay.

- Game loop: what does the player do repeatedly?
- Win/lose conditions (or success criteria for educational games)
- Controls: keyboard, mouse/touch, or both
- Feedback: what happens on correct/wrong/success/fail actions

### GATE 2 OUTPUT
> STEP 2 COMPLETE: Core mechanic is [mechanic description]. Win condition: [condition]. Controls: [input type]. Feedback loop: [description].

## STEP 3 — Progression Design

Design how challenge and content evolve over time.

- Difficulty curve: how does challenge increase?
- Level/stage design (if applicable)
- Unlockables, rewards, achievements
- Session length: how long is one play session?

### GATE 3 OUTPUT
> STEP 3 COMPLETE: Difficulty curve is [description]. Stages/levels: [count and structure]. Session length: [duration]. Rewards: [list].

## STEP 4 — Content Mapping

Map content to gameplay (especially for educational games).

- What content is taught?
- How does gameplay reinforce learning?
- Where do facts/concepts appear in the game flow?
- List all content items and their categories

### GATE 4 OUTPUT
> STEP 4 COMPLETE: Content items: [list with categories]. Content appears during [game flow points]. Learning reinforced via [mechanism].

## STEP 5 — Architecture Decision

Choose the technical architecture for the game.

- Canvas vs DOM vs hybrid (see `references/game-patterns.md`)
- Single file vs modular structure
- State management approach

### GATE 5 OUTPUT
> STEP 5 COMPLETE: Architecture is [canvas/DOM/hybrid] because [rationale]. File structure: [single/modular]. State management: [approach].

## STEP 6 — Write Design Document

Write the game design document and save to `game-design.md` at the project root.
Include all decisions from previous steps in a scannable format.

### GATE 6 OUTPUT
> STEP 6 COMPLETE: Design document written to `game-design.md`. Sections: [list of section headings].

## Checklist Before Handoff

- [ ] Genre and theme defined
- [ ] Core mechanic described (what player does)
- [ ] Win/lose or success criteria defined
- [ ] Controls specified
- [ ] Difficulty progression outlined
- [ ] Content-to-gameplay mapping documented (if educational)
- [ ] Canvas/DOM/hybrid decision made with rationale
- [ ] Session length estimated
