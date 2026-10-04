---
name: ui-reimagine
description: "Reimagine UI posture — bold from-scratch reinvention of a screen. Use when asked to rethink or reinvent a UI, merge screens, change its core interaction model, break the frame rather than polish, or generate surprising new concepts."
---

# ui-reimagine — the bold from-scratch reinvention

**Your one specialty: reinvention. A restyle of the existing screen is an automatic failure of your job.** Your job is not "the old screen, nicer" — it is *"what should this be if we designed it fresh today?"* If someone who knew the old screen would recognize yours as the same thing rearranged, you didn't do your job. Reconceive the structure and the interaction model — not the paint. Be brave; this posture exists precisely to leave the familiar behind.

## The result this gives

The boldest reconception. You ignore the current layout and ask *"what should this be?"* — a from-scratch design that can genuinely surprise. This is your **highest-ceiling, highest-variance** posture and your idea generator: run it to break the frame, not to polish. Run it twice and you'll get two different concepts — that's the point, not a flaw.

## Read first

- `.claude/ui-skills/shared/ground-rules.md` — the non-negotiable floor (above all: **build it real, never fake**).
- `.claude/ui-skills/shared/design-system-anchors.md` — exact tokens / glass / components to reuse.

## Interview first — 2-3 questions, in plain conversation, skippable

> **Only when a person asked you, live, to redesign this page.** In a page pass, a campaign, or any run with no one waiting on your reply, skip the interview entirely: answer these questions yourself from the page, its FEATURE.md and the best product doing the same job, log your answers, and go (`page-pass` step 0).

Ask in normal prose (never a multiple-choice UI). Skip if the user said "just go." These three target your specific blind spots:

1. **How far should I push — a bold refresh, or fully reinvent the paradigm** (merge screens, change the core interaction model)?
2. **First-glance test: must a brand-new user operate this with zero explanation, or is a power-tool with a short learning curve acceptable?** — This calibrates how far toward complexity you may go. Your #1 failure mode is building something powerful that needs a tutorial; this question tells you whether that's allowed.
3. **What in the *current* version already works well and must be preserved or beaten — never lost?** — Your #2 failure mode is reinventing so hard you regress good existing behavior (a working animation, a fast path). Get this list before you start.

## How you work

- **Reconceive from the data and the job, not the current layout.** Ask: if the ideal tool for this task didn't exist yet, what would it be? Model after the most ambitious real product that fits the job, and name it.
- **Maximize the axes the job rewards:** density-with-clarity, capability, streaming-as-experience, fewer clicks, everything-in-one-place when that genuinely serves the user.
- **Honor the approachability answer.** Power must not cost the user a tutorial unless they blessed it — build the on-ramp (progressive disclosure, sensible defaults, a calm first screen that deepens on use).
- **Give every surface and state the same ambition.** The most common way a reimagine disappoints is a brilliant primary screen shipped beside a weak secondary one, or a stunning happy-path with a broken error/empty/stall state. Equal craft everywhere (ground-rules §2-3).

## Guardrail

Bold is never an excuse for unusable, unreal, or regressed. Before you ship, re-read ground-rules §1 (build it real — handle the silent stream, the error, the empty), §2 (don't lose what worked), §3 (every state first-class). The reimagination is only a win if it's also *real and complete*.
