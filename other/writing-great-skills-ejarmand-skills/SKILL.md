---
name: writing-great-skills
description: Reference for writing and editing skills — what a skill should afford and how to keep it lean.
disable-model-invocation: true
---

A skill exists to **afford**: to give the model or the user direction and capability they would not otherwise have. **Affordance** is the root virtue — every skill, and every line in one, earns its place by it.

This file is also the review standard for skills and agent-facing docs: judge such diffs against these terms (the code standard in `codebase-design/STANDARD.md` does not apply).

**Bold terms** are defined in [`GLOSSARY.md`](GLOSSARY.md).

## What a skill affords

- **Tools for the model** — capability or parameterization distant from its training defaults. Models don't interrogate their users, so a grilling skill affords interrogation; they arrive using only native subagents, so a dispatch skill affords access to other models. 
- **Tools for the user** — leverage beyond their own: autonomy, decomposition past human working memory, faster comprehension.
- **A shared destination** — alignment on what done looks like, with the route left to the model's judgment.

The existence test runs at two levels. A *skill* can earn its place on either axis, model or user. A *line* earns its place by the **no-op** test — does it change model behaviour? — excepting the few lines written for human eyes, like a **user-invoked** description.

**Path-teaching** — walking the model from A to B — was written for models that couldn't find the way; today it boxes the one that can. State the **destination**, and trust the model with the route. 
**Predictability** matters within affordance — a capability that fires erratically isn't afforded — but process specified past what the destination needs is **the box**.

Affordance decays: behaviour that needed a skill last year is native now. Grade against current models. 

## Invocation

Two choices, trading different costs:

- A **model-invoked** skill keeps a description the agent can see: it can fire autonomously, and other skills can reach it. It pays **context load** — the description sits in the window every turn.
- A **user-invoked** skill (`disable-model-invocation: true`) strips the description from the agent: only you can fire it, and no other skill can. Zero context load, but it spends **cognitive load** — you are the index that must remember it exists.

Pick model-invocation only when the agent, or another skill, must reach it on its own. Split off a new model-invoked skill only when a distinct **leading word** should trigger it independently. 

When user-invoked skills multiply past what you can remember, a **router skill** cures the pile-up.

A model-invoked description does two jobs: state what the skill is, and list the triggers that should fire it. Front-load the skill's **leading word**, collapse synonym triggers, and cut identity that's already in the body. A user-invoked description is human-facing: one line.

## Arranging content

The primary content is the **destination** and the tools for reaching it; reference — definitions, rules, facts — supports on demand. **Steps** earn a place only when necessary.

Progressive disclosure keeps the top legible: push behind a **context pointer** what only some runs need, inline what every run needs. A pointer's wording, not its target, decides whether the material is reached. Keep a concept's definition, rules, and caveats under one heading, so reading one part brings its neighbours.

## Trusting the agent

- The **stakes test** decides whether a guard earns its place: guard failures that are frequent or hard to recover. Rare and hand-recoverable earns nothing.
- **Loosening** resolves open questions: default to deleting the constraining text rather than writing the clarifying answer. Ambiguity is an acceptable resting state.

## Leading words

A **leading word** is a compact concept already in the model's pretraining that anchors a whole region of behaviour in one token (_lesson_, _seam_, _tracer bullets_). Repeat it as a token, never as a sentence; a coined word recruits no priors — reach for an existing one. In the body it anchors execution; in the description it anchors invocation — when the same word lives in your prompts, docs, and code, the skill fires more reliably. A triad spelled out at three sites, a description spending a sentence to gesture at one idea — each is a passage begging to collapse into a single word.

## Pruning

Keep each meaning in one authoritative place. Check every line for relevance, hunt **no-ops** sentence by sentence, and when a sentence fails, delete it whole rather than trim it. Watch for:

- *Sediment* — stale layers that settle because adding feels safe and removing feels risky.
- *Sprawl* — a skill too long even when every line is live; cure by disclosure, not compression.
- *Duplication* — one meaning in two places: a maintenance cost and a false weight. Its commonest shape is the em-dash paraphrase: "I'm walking south — the opposite of north."
- **Historical contrast** — "we do this now, not what we used to do." Contrast earns its place only when it disambiguates a live fork the model might take.
