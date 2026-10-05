---
name: permadeath-and-lethality
description: Use when designing high-lethality / permadeath / single-save combat and the systems around it — making death fair and readable, mitigating the cost of failure without removing stakes (short runs, opt-in difficulty, deterministic anti-save-scum), meta-progression and diegetically-integrated death (roguelike vs. roguelite), and the hard open problem of single-save permadeath in a long-form open world. Also use to diagnose deaths that feel unfair, a game churning players at the first big loss, or grind-to-win meta-progression. Triggers on "permadeath", "single-save", "high-lethality", "roguelike", "roguelite", "meta-progression", "save-scumming", "Ironman", "God Mode", "fairness", "telegraphing", "death is progress", "succession", "heir", "Hardcore mode".
---

# Permadeath, Lethality & Meta-Progression

How to make death *create* stakes instead of frustration: a hand-authored fairness/readability backbone first, mitigations that cut the cost of failure without removing stakes, meta-progression that makes failure progress, and an honest treatment of the genuinely-unsolved case — single-save permadeath over a long-form open world.

## When to use this

- Designing permadeath / single-save / high-lethality combat and its difficulty curve
- Deciding the roguelike↔roguelite position (what persists across death)
- Designing meta-progression and a diegetic death/return frame
- Picking an anti-save-scum model (delete-on-load, deterministic seed, hyper-RNG, consequence-delay)
- Tackling long-form open-world permadeath (the novel, playtest-required case — Area 4)
- Diagnosing unfair deaths, first-big-loss churn, grind-to-win, or audience-cliff problems

## Scope

This skill owns **failure, lethality, and persistence-across-death.** Adjacent concerns live in siblings:
- Telegraphing/readability as combat craft → `combat-design` (this skill treats it as a *fairness backbone* for generation)
- Loot/economy/progression numbers (incl. the finite-legendary manifest) → `rpg-systems`
- The lore that *justifies* death/persistence diegetically → `worldbuilding-and-lore` (ludonarrative harmony)
- "Interesting decisions," flow, loss-aversion framing → `game-design-fundamentals`
- Generating fair encounters + gating them → `procedural-generation`, `procgen-review`
- The world-state persistence schema as content → `systemic-emergent-design`

## How the pieces fit

- **`GUIDE.md`** — the *why*: four areas (fairness, mitigations, meta-progression, the single-save long-form open-world open question), each with exemplars, citations, a "test for" criterion, a named failure mode, and the procedural/AI-authoring implication.
- **`CHECKLIST.md`** — the *what to do*: Do/Don't + Test-for, grouped by area.

**Source & epistemic status.** Distilled from a deep-research synthesis (Sid Meier on interesting decisions; Spelunky/Derek Yu on fairness; Kasavin on Hades; XCOM RNG determinism; the Berlin Interpretation; Kahneman & Tversky loss aversion; Crusader Kings / Dwarf Fortress / Rogue Legacy / NetHack for succession). **Areas 1–3 rest on shipped short-run games. Area 4 — single-save + long-form open world — is genuinely under-explored; every Area-4 rule is an *extrapolation from adjacent genres and must be playtested.*** The two **⚠️ HEAVY FLAGS** from the source are preserved verbatim in `GUIDE.md §4`.

## The one idea to anchor on

> **Lethality without fairness is a random-death generator — the single worst outcome for a permadeath game.** Permadeath only converts decisions into stakes if every death is the player's fault, telegraphed, and readable. So author a hand-authored **fairness/readability backbone** (telegraph budgets, guaranteed escape/counter-options, lighting/LoS minimums, hazard ceilings, an automated survivability check) *before* generating any content — and in a long-form single-save game, where one unfair death can cost the whole run, make it *stricter*, not looser.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
