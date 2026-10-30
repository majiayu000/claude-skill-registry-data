---
name: thatch-refine-personal
description: Type-specific requirements for refining a plan in a solo personal project with no downstream consumers. Loaded by thatch-refine after classification; assumes the core loop in thatch-plan-refinement. Relaxes coordination requirements and allows cleverness and experimentation, while keeping premise verification honest.
---

You are refining a plan for a **personal** project: solo code with no
downstream consumers. The coordination constraints that govern team code
are relaxed. This is the place to show off cleverness and experiment with
interesting techniques that would be inconsiderate in a shared codebase.
Load `thatch-plan-refinement` for the core loop and apply the deltas
below; where they disagree, these win.

## What this type owes

- **Almost nothing to anyone else.** No consistency obligation to
  teammates, no reviewer to orient, no downstream API to protect.
- **Still honest about facts.** Relaxed style does not mean relaxed
  reality: every factual premise still carries a verified `file:line`
  citation, and "unverified" is still marked. A plan built on a wrong
  premise wastes your time in any project.

## How this changes the loop

- **The skip threshold drops.** Most personal-project plans can be tried
  faster than they can be refined. Skip refinement whenever the change is
  cheap to build and cheaper to rewrite; run the loop only when the plan
  touches something expensive to get wrong (persistent state, a
  hard-to-reverse migration, hours of build effort).
- **Fewer rounds.** One quiet review round is enough consensus. The cap
  drops from three rounds to two; a personal plan that has not converged
  by then should just be built or abandoned.
- **Degraded review is fine.** If the host cannot dispatch sub-agents, a
  same-context self-review pass is usually enough. Saying so out loud, as
  the core skill requires, is still worthwhile but the stakes are lower.
- **Round counts drop, not mode selection.** These deltas relax how many
  rounds a run needs. If a deep-mode trigger in `thatch-plan-refinement`
  is met (shared persistent state, many files or hosts, a new
  abstraction, table, or contract, or the user asks for depth), the lens
  fan-out still runs.

## Lens weights

- **Premise verification is the only load-bearing lens.** The fresh
  reviewer's core job is checking the plan's factual model of the code.
- **Pattern and reuse mostly skips.** There is no team to stay consistent
  with. Flag reuse only when reinventing an existing wheel will genuinely
  bite future-you.
- **Alternatives turns exploratory.** The question shifts from "what is
  safest?" to "what would I learn?" - one alternative worth trying for
  the technique is a valid result even when the plan's choice is fine.
- **Hidden problems shrinks to future-self.** The only consumer to
  enumerate is you, six months from now, with no memory of this code.

## Extra plan sections

None required. Blast radius, migration plans, and reviewer orientation
sections are skipped unless the change is in the expensive-to-get-wrong
category that triggered refinement at all.

## Docs bar

- Future-self breadcrumbs only: comment the surprising spots, not the
  obvious ones.
- When a plan deliberately uses an experimental technique, record that in
  one line (in the plan or a comment) so a future session knows the
  oddity was chosen, not accidental.
