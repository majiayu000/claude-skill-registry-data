---
name: ui-sharp
description: "Lean, sharp UI posture — the everyday default for building or redesigning a UI. Use when asked to build or make a page, panel, list, form, or dashboard good, cleaner, or nicer, or for a fast confident refresh where the agent uses its judgment instead of asking for a spec."
---

# ui-sharp — the lean, inviting redesign

**Your one specialty: making a UI feel effortless.** Not a flavor you add if there's time — it is the whole job. Every cut and every layout choice serves that one feeling. If a first glance doesn't say *"oh, this is easy,"* you haven't delivered your specialty yet — go again.

## The result this gives

A fast, clean, **inviting** UI. Sharp, minimal, confident. The user's first reaction is *"I could do this"* — not "I need a tutorial." You keep what works, cut the clutter, elevate the rest, and then you stop. You don't gold-plate and you don't reinvent the paradigm. This is the everyday default for "make this page good."

## Read first

- `.claude/ui-skills/shared/ground-rules.md` — the non-negotiable floor (above all: **build it real, never fake**).
- `.claude/ui-skills/shared/design-system-anchors.md` — exact tokens / glass / components to reuse.
- [project-conventions.md](project-conventions.md) (in this skill; absorbed the former `modern-web-design-expert` skill) — the "how to write conformant CSS" layer: migration priorities (fluid `clamp()` type, `@container` queries, `@starting-style` entrance animations, shadcn wrappers), textures/scrollbars, layout components, and key-file map. Applies to every ui-* posture, not just this one.

## Interview first — 2 questions, in plain conversation, skippable

> **Only when a person asked you, live, to redesign this page.** In a page pass, a campaign, or any run with no one waiting on your reply, skip the interview entirely: answer these questions yourself from the page, its FEATURE.md and the best product doing the same job, log your answers, and go (`page-pass` step 0).

Give the user one moment to aim you, then go. Ask in normal prose (never a multiple-choice UI), keep it to ~2 sharp questions, and **skip entirely** if they already told you or said "just go" — lean means trusting yourself for the rest.

1. **Who is this for, and what's the one job they came here to do?** (sets the persona and the single thing that must be effortless)
2. **Is there a product or app whose feel you want this to evoke?** (your reference model — if they don't have one, *you* pick it and name it)

Why exactly these two: your failure mode in lean mode is cutting something they actually needed, or modeling after the wrong thing. These two cover both. Don't ask more.

## How you work

- **Name the real product you're modeling after, out loud**, then build toward it. This is the single biggest quality lever — "make it modern/beautiful" averages to the generic AI mean; "model it after macOS Reminders / Linear / Stripe" inherits real layout, density, and interaction for free (ruled set + the bones-not-skin rule: ground-rules §4).
- **Cut hard:** kill narration, restated page titles, redundant chrome, card-in-card nesting. Surface the primary job; tuck secondary detail one interaction away (hover, expand, drawer).
- **Density with clarity** at the persona's level. One confident accent. Our glass where it invites, not everywhere.
- Make the **primary action unmistakable**. Make first glance say *easy*.
- Then **stop.** The win is sharp + inviting + done — not maximal.

## Guardrail

Inviting ≠ empty. Sparse, centered, under-filled, padding-to-fill is a *different* failure, not "clean." The target is **dense-but-calm**: a lot of useful information, made to feel effortless through hierarchy and spacing — the way Apple and Linear do it.
