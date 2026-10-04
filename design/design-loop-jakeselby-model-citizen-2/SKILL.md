---
name: design-loop
description: Raise the visual quality of something that renders through a build, screenshot, independent scored critique and fix loop, against rubrics with hard accessibility, design-token, runtime and asset-licensing gates. Use when asked to make a UI, page, HTML doc, dashboard, game scene or 3D asset look dramatically better, more polished or more professional; to improve the visual design, look, styling or visual quality of a surface; to iterate toward a reference, mockup or screenshot; and proactively after building or substantially changing a user-facing surface. Not for deciding what screens exist or how flows behave.
---

# Design loop

A closed loop that raises visual quality by measurement rather than taste. The agent that built
the thing cannot grade it, so an **independent judge with a clean context** scores each round
against a **locked target** until it clears the bar or stalls.

Derived from [dream-loop](https://github.com/achimala/dream-loop) (MIT) — see `ATTRIBUTION.md`.

**Two standing rules that apply even outside the loop.** Visual work is verified by a capture the
agent reads before anything is shown to the user; a claim about how something looks without a
capture behind it is unverified. And the look is designed in cheap loops — a mock, a sketch, a
throwaway render — before it is engineered into the real pipeline.
The loop mechanics are its contribution. The rubrics, hard gates, escalation and asset policy
here are ours and differ deliberately; do not reintroduce its asset-sourcing chapter.

## When this is the wrong skill

This skill **refines something that already renders**. It needs a running artifact to screenshot.
It does not decide what screens exist, what the flows are, or how anything behaves.

| If the ask is | Use |
| --- | --- |
| What screens exist, what the flows are, how it behaves | your planning framework's UX specification workflow |
| A mockup, wireframe or screen design from scratch | `design` — canvas, no running artifact needed |
| Styling a published Artifact page | `artifact-design` |
| Make the thing that exists look far better | **this skill** |

A UX spec produces the brief. This produces the finish. If a surface has been specified but not
built, build it first — there is nothing to capture until then.

## Pick a mode first

| Mode | Surface | Rubric |
| --- | --- | --- |
| **ui** | Web app, iOS/Mac app, landing page, standalone HTML doc, dashboard | [references/rubric-ui.md](references/rubric-ui.md) |
| **scene** | 3D scene, game view, rendered asset, Blender output | [references/rubric-scene.md](references/rubric-scene.md) |

Read only the rubric for your mode. If the request spans both, run two loops with separate
targets — never average one rubric across both.

## The loop

Prerequisites: a locked target and a working capture command. Get both before round 1.

1. **Establish and lock the target** — [references/targets.md](references/targets.md). Write it
   to `.design-loop/target.<ext>` and do not regenerate it mid-loop.
2. **Establish the capture command** — [references/capture.md](references/capture.md). Verify it
   produces a real screenshot before you start, not after.
3. **Implement a pass** at the target. When the session runs below the strongest class, hand
   steps 3 to 5 and 7 to the `designer` agent, which declares that class; give it the workspace,
   the target, the capture command and the last verdict. It never judges; step 6 stays yours.
4. **Validate it yourself.** It must actually run, load and work. Fix breakage, wrong
   orientation, missing assets and failed loads here. Do not use this step to tune visuals.
5. **Capture** the current state to `.design-loop/round-<n>.png`.
6. **Judge** — spawn the `design-judge` agent with the image paths, the surface type and the
   target path and evidence for non-visual hard gates, per
   [references/judge.md](references/judge.md). Never judge your own work inline.
7. **Address every gap** the judge named, hardest first. Do not cherry-pick the easy ones.
8. **Evaluate exit criteria** below. Exit, escalate, or return to step 4.

## Hard gates

Each rubric defines gates that are **pass/fail, not scored**. A failing gate blocks exit at any
score. Accessibility, design-token adherence, runtime budget and asset licensing are gates
precisely because a loop optimizing for "looks good" will trade them away otherwise.

Never lower a gate to exit the loop. Report it unmet instead.

## Exit criteria

- **Score ≥ 8/10 and all gates pass** — done. Show the latest capture, state the score and the
  remaining known gaps, and ask whether to keep going.
- **Score ≥ 8/10 but a gate fails** — fix the gate. Re-judge afterward to confirm the fix did not
  cost visual quality. A gate fix that regresses the score is not finished.
- **Stall approaching** — the best score has not improved by a full point in 2 rounds, *or* the
  judge has named the same gap twice running. Stop making incremental tweaks. Step back and find
  the structural reason: wrong layout system, wrong palette, wrong camera, wrong asset quality,
  wrong type scale. Make one dramatic change, not five small ones.
- **Stalled** — the dramatic change did not move the score. Stop. Do not spend tokens on a second
  architectural guess. Escalate.
- **Round budget spent** — default cap is **5 rounds**. That is a cap, not a target. Escalate.
- **Otherwise** — keep looping. Do not exit early because progress feels adequate.

## Escalation

Follow the standing autonomous-loop rule: interrupt only for blocking findings, for product, UX,
security or schema calls outside the brief, or for anything destructive. Everything else goes on
a running **Decisions needed** list while the loop keeps moving.

Ambiguous design calls are not interrupts. Implement the sensible default, keep going, and
headline it at the end for confirm or override.

When you do stop, report: current score with per-axis breakdown, gate status, what you changed,
what is still open, and the specific question you need answered.

## Assets

**Sourcing is governed entirely by the chosen `licensing` stance**, plus any path-scoped
asset rule the project carries. Invoke the `licensing-review` skill before incorporating anything new.

Three things this loop must never do, regardless of how much they would improve the score:

- **Never download assets without clearing the license first.** "Free download",
  "royalty-free" and a marketplace tag are not proof.
- **Never override a restriction the user set.** If they said don't download assets, that
  includes generated-3D services, image-to-3D APIs and asset marketplaces. Ask; do not reinterpret.
- **Never ship generated 3D assets on unresolved terms.** Image-to-3D output carries the vendor's
  terms, not a clean license. Unresolved material stays out of production.

If no compliant asset clears the bar, adapt a compliant base or author original geometry. Say so
plainly rather than quietly substituting something weaker.

## Working files

Keep everything in `.design-loop/` at the repo root:

```
.design-loop/
  target.png          locked reference, written once
  round-1.png         capture per round
  verdict-1.md        judge output per round
  notes.md            decisions needed, assumptions, gate status
```

Add `.design-loop/` to `~/.config/git/ignore` once so it stays out of every repo.

## Time budget

If given one, record the clock after the target is locked and check it between rounds. **Do not
trade visual quality for the deadline** — hitting the limit with real, beautiful progress beats
landing complete and ugly. Report what you would do with another round.

If no budget is given, run to an exit criterion and warn up front that this consumes real tokens:
each round is a build pass, a capture and a judge subagent.
