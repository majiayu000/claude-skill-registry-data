---
name: art-direction-and-readability
description: Use when making design-level (not asset-production) decisions about how a game looks and reads — readability vs. fidelity, silhouette design, value/contrast as eye-direction, reserved signal colors, visual-language consistency, and how an AI engine keeps a coherent house style across generated content. Triggers on "art direction", "readability", "silhouette", "signal color", "yellow paint", "visual hierarchy", "style guide", "make it readable", "stylization vs realism", "how should the game look".
---

# Art Direction & Readability

How to make a game **read** — so the player can instantly answer the gameplay questions the scene poses (friend or foe? safe to touch? where do I go?) — and how an AI content engine holds one coherent visual language across thousands of generated pieces. This is the *design discipline* of visual communication, not asset production.

## When to use this

- Setting a project's visual direction (stylization vs. fidelity, reference set, palette)
- Auditing a scene, character, or generated asset for readability
- Designing or policing a signal-color language
- Giving an AI generator a checkable "house style" and per-asset read contract

## Scope

This skill owns **visual communication at the design level**. Adjacent concerns live in siblings:
- Where landmarks/signal-color sit *in space* → `open-world-design`
- *What* gets generated and its sameness problem → `procedural-generation`, `procgen-review`
- Coherence of generated *text/lore* (the non-visual analogue) → `ai-authored-content-coherence`
- General feedback/clarity theory → `game-design-fundamentals`

## How the pieces fit

- **`GUIDE.md`** — the *why*, with exemplars and citations. **Sections 1–6 are verification-confirmed** (Team Fortress 2 primary sources, adversarially checked 3-0). **Sections 7+ are sourced but unverified** — see the verification banner in the guide.
- **`CHECKLIST.md`** — the *what to do*: Do/Don't plus "Test for" criteria you can run against a scene, a character, or a generated asset.

## The one idea to anchor on

> **Readability is an engineerable requirement, not a taste call.** Every visual element should be able to name the gameplay question it answers; one that answers none is decoration competing with the ones that do. Order of priority: **readability first, personality second, fidelity never.**

⚠️ **Verification note:** This skill was built from a deep-research pass whose adversarial-verification phase was cut short by a session limit. The TF2-grounded core (GUIDE §1–6) is confirmed; the signal-color case studies (BotW, Mirror's Edge, Naughty Dog/yellow-paint) are **sourced but not verification-confirmed**. Treat the latter as strong defaults to re-verify, not settled fact.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
