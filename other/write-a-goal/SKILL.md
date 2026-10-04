---
name: write-a-goal
description: Turn a rough ambition into a measurable, REACHABLE goal — a capability statement, a precisely-named metric, ≥2 numeric evals, an acceptance rule, and non-goals — with a feasibility check that catches impossible or game-able targets before you chase them. Pair with /goal (which pursues a goal autonomously).
---

# /write-a-goal

Usage: `/write-a-goal <the ambition, or what "good" looks like>`

A goal you can't measure is a wish. A goal you can't reach is a trap. A goal a
degenerate output can fake is a lie. This skill turns an ambition into a goal that
`/goal` can autonomously pursue and a fresh-eyes agent can actually certify —
**and it refuses to hand you a target that's impossible or game-able.**

## The shape a good goal must clear

1. **Capability statement** — one sentence: *"Given X, the system does Y."* Concrete, observable.
2. **The exact metric** — the single thing measured, named precisely enough that two people would compute the same number (see Check A).
3. **≥2 numeric evals** — real test cases, each with a target number and how it's scored. One eval is an anecdote; two+ is a bar.
4. **Acceptance rule** — when is it *done*? (e.g. "every eval ≥ target on a fresh run, confirmed by a fresh-eyes agent.")
5. **Non-goals** — what this explicitly is *not*, so the loop doesn't gold-plate the wrong thing.

## The two checks that make or break it (hard-won)

### Check A — Pin the exact metric (kill vague percentages)
*"Make it 99% similar"* is meaningless until you answer **similar HOW**. The same
artifact can score 20% or 95% depending on the measure. Force the choice:
- Name the measure (e.g. *visual SSIM on edge maps*, not "looks the same"; *structural
  token overlap*, not "matches the design"; *p95 latency*, not "fast").
- State how it's computed and what tool reports it.
- If one number hides several things, split it (e.g. "fidelity" → *visual* + *structural* + *copy*).
- **Robustness clause:** require the metric to resist gaming. Ask *"what's the dumbest
  output that could score high?"* — if a blank/empty/degenerate result can fake the
  target, the metric is broken; add a guard before you trust it.

### Check B — Feasibility / ceiling check (don't set a trap)
Before committing the target, pressure-test it against what the architecture can
*actually* reach:
- What's the theoretical ceiling for this approach? (e.g. a small local model
  reconstructing from a text description can't pixel-match a real site — the inputs
  it's missing cap it far below 100%.)
- Is the target inside that ceiling, with headroom? If not, **say so plainly and
  propose a reachable target instead** — never accept an impossible number silently.
- Name the lever that would *raise* the ceiling (a different input, a different model
  class) vs. the levers that just optimize *within* it — so effort goes where it pays.

## What you do as the assistant when this is invoked

1. **Extract the ambition** — what does the user actually want, and what would make
   them say *"yes, that's it"*? Ask at most one clarifying question if it's truly ambiguous.
2. **Draft the 5-part goal** (capability · metric · ≥2 evals · acceptance · non-goals).
3. **Run Check A** — pin the exact metric; split vague numbers; add the robustness guard.
4. **Run Check B** — feasibility. If the target is unreachable or game-able, **lead with
   that**, and offer a reachable, robust alternative target (recommended-first).
5. **Output the goal spec** as a small artifact (capability, metric+tool, evals with
   numbers, acceptance, non-goals, and the feasibility verdict).
6. **Offer to hand off to `/goal`** to pursue it autonomously, or `/full-cycle` if it's
   a build.

## Anti-patterns — real cases this skill exists to prevent

- **Vague + impossible:** *"Replicate this homepage to 99%."* Two failures at once — the
  metric is undefined (visual? structural? pixel?), *and* the target is unreachable for
  the architecture (a local 14B reconstructing from a text digest plateaus ~30% visual;
  placeholder-vs-real images alone cap it). The fix: define the measure (visual SSIM with a
  blank-guard), and set a reachable bar (e.g. *structural ≥ 85% + visual ≥ 70% with real
  images*), naming "a vision model" as the lever that would raise the ceiling.
- **Game-able metric:** a blank page scoring 98% because it matched the site's dark
  background. A target with no robustness guard rewards the dumbest output.
- **Single anecdote as a bar:** one passing example ≠ a goal. Require ≥2 evals.
- **A vibe with no number:** *"make it feel premium."* Either find a measurable proxy or
  admit it's a taste call, not a goal.

> Companion: [`meta/learning-loop-rubric.md`](../../../meta/learning-loop-rubric.md) (scoring what to
> promote) and [`meta/always-recommend.md`](../../../meta/always-recommend.md) (lead with the
> recommendation — including when proposing a reachable target). `/goal` *pursues* a goal;
> `/write-a-goal` *forges* one worth pursuing.
