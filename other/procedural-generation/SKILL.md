---
name: procedural-generation
description: Use when designing or building a content generator — terrain, dungeons, quests, items, lore, history — or diagnosing generated content that feels samey, generic, or soulless. Covers the "10,000 bowls of oatmeal" problem, perceptual vs. mathematical uniqueness, the handcrafted-anchor + constrained-fill hybrid, voice-consistent corpora, multiplicative systems, and tying generation to meaning. Core skill for headless / AI-authored games. Triggers on "procedural generation", "procgen", "generator", "my generated content is samey", "infinite content", "world generation", "AI-authored content".
---

# Procedural Generation

How to make generators whose output is *perceptually* rich, not just mathematically infinite — the central skill for a headless, AI-authored game.

## When to use this

- Designing any generator (terrain, dungeons, quests, items, NPCs, lore, history)
- Diagnosing generated content that reads as samey / generic / soulless
- Deciding the handcrafted-vs-procedural ratio
- Setting up an AI authoring engine that needs one coherent voice

## Scope

This is the *how to generate* knowledge skill. Its companion is **`procgen-review`** — the process skill that *gates* generated output against these principles (oatmeal test, fanfic test, sameness scan). Generate with this; review with that.

Related: `open-world-design` (generating space), `worldbuilding-and-lore` + `ai-authored-content-coherence` (generating lore coherently), `systemic-emergent-design` (multiplicative systems).

## How the pieces fit

- **`GUIDE.md`** — the *why*: the oatmeal problem, perceptual uniqueness, the hybrid model, corpus voice, intentionality/local logic, multiplicative systems, curated randomness, apophenia. Cited.
- **`CHECKLIST.md`** — the *what to do*: Do/Don't + test-for criteria.

## The one idea to anchor on

> **Perceptual uniqueness is the only metric that matters.** You can generate 10,000 mathematically-unique bowls of oatmeal; the player still just sees oatmeal (Kate Compton). Intentionality — constraints, handcrafted anchors, local meaning, and a single voice — is what separates great procedural content from infinite filler.

Start with `GUIDE.md`; gate everything you generate with `procgen-review`.
