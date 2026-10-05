---
name: systemic-emergent-design
description: Use when designing, auditing, or generating the systemic substrate of a game — the small set of consistent, interacting rules (a "chemistry engine") that produce emergent play, rather than scripted set-pieces. Covers immersive-sim principles (intention & perceivable consequence), multiplicative vs. additive design, the "tabletop RPG with a good GM" analogy, and how emergent systems make procedural generation cohere instead of becoming "oatmeal". Also use to diagnose "the world feels inert", "all the variety is scripted", "my generated content is samey", "players can only do what I imagined", or single-solution gates. Triggers on "systemic design", "emergent gameplay", "immersive sim", "multiplicative gameplay", "chemistry engine", "affordances not solutions", "intention and consequence", "interacting systems", "oatmeal", "every quest is the same".
---

# Systemic-Emergent Design

How to author **affordances, not solutions**: a small set of consistent, deeply-simulated, interacting rules that produce more meaningful play than any volume of scripted content — and, for a procedural/AI-authored game, the only thing that makes generated content *cohere* rather than collapse into "10,000 bowls of oatmeal."

## When to use this

- Designing the rule substrate / "chemistry engine" before authoring or generating content
- Deciding whether to add a system, a verb, or a scripted set-piece
- Auditing for emergence: are systems actually interacting, or siloed behind scripts?
- Making procedural generation produce *perceptual* variety, not just numerical variety
- Diagnosing: "the world feels inert", "all variety is scripted", "every generated quest is the same", single-solution gates

## Scope

This skill owns the **emergence-from-interacting-systems** discipline. Adjacent concerns live in sibling skills, cross-linked from the guide:
- The "interesting decision" test and general theory → `game-design-fundamentals`
- Perceptual uniqueness, the oatmeal problem, handcrafted-anchor + constrained-fill → `procedural-generation`, `procgen-review`
- Combat verbs, telegraphing, the feel of interactions → `combat-design`
- Currencies/items as systemic chains (currency-as-material) → `rpg-systems`
- The spatial affordances systems act on → `open-world-design`
- Quests that emerge vs. branch → `narrative-and-quest-design`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: the immersive-sim lineage (universal rules; intention & perceivable consequence), emergence from few deep systems vs. scripted events, the "good GM" analogy and its honest limit, multiplicative vs. additive design (Nintendo's chemistry engine), and how emergence + procedural generation multiply each other. Each rule carries an exemplar, source, **test-for** criterion, named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain, written to be enforced as automated gates in a generation loop.

## The one idea to anchor on

> **You never design play directly — only the rules that give rise to it (the "second-order design problem").** Author orthogonal affordances and let them combine; keep the rules near-exceptionless and mapped to real-world expectation so players learn them by exposure; guarantee every verb has *intention* and *perceivable consequence*; and freeze the rule substrate before you generate, so the simulation — not the AI's whim — validates emergent solutions.

> **Why this matters doubly for a generator:** producing more *content* is cheap; producing more *interactions* is hard, so a generator told to "maximize variety" produces oatmeal, and one that "helpfully" adds bespoke interactions reintroduces exceptions that break learnability. Score the agent on **interaction density**, constrain it to **tag-assignment and situation-composition over a frozen rule table**, and forbid it from ever inventing a new rule or exception.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
