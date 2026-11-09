---
name: design-action-gameplay
description: Specify fair, readable action gameplay across player verbs, combat timing, enemy decisions, perception, encounters, feedback, and deterministic tests. Use for melee, ranged, ability, dodge, lock-on, enemy AI, fog or visibility, and encounter tuning.
engines: [AGNOSTIC]
---

# Design Action Gameplay

## When to use

- Designing or revising an action combat loop.
- Tuning enemy behavior, perception, counterplay, or encounter roles.
- Turning gameplay feedback goals into implementable state and timing contracts.

## Workflow

Use `build-model-actions` when reviewed clips need an authored dance, chained combination or charge/cast presentation. Specify anticipation, release/contact cues, recovery, interruptions and readable effect timing. Interactive input buffers, branching combo rules, combat validation and networking remain part of the gameplay design/implementation contract; a composed animation sequence does not decide those outcomes.

1. Define every player verb with inputs, eligibility, commitment, timing phases, costs, outcomes, cancellation, and feedback.
2. Separate authoritative combat truth from animation, VFX, camera, audio, and UI presentation.
3. Model enemy perception, intent, action selection, motion, recovery, and return behavior explicitly.
4. Compose encounters from readable roles, space, pacing, pressure, recovery, and escalation.
5. Require anticipation, counterplay, consistent hit rules, and visible failure causes.
6. Create deterministic tests for state transitions, timing boundaries, targeting, occlusion, damage, and fairness.
7. Map accepted events to bounded animation, VFX, audio, camera, HUD, and optional haptic feedback. Specify clock ownership, overlap, interruption, reduced-intensity alternatives, and cancellation; keep physical knockback and damage in authoritative rules. Use `build-gameplay-runtime` for feedback adapters and compatible engine skills resolved through `resolve-skill.sh` for API work.
8. State a balance hypothesis for each tuning change and playtest the intended decision, counterplay, and failure explanation. Separate measured behavior from player interpretation; deterministic timing tests alone do not establish that a fight is readable or enjoyable.

## References

- Read `skills/build-gameplay-runtime/references/input-and-locomotion-feel.md` in the resolved Hephaera baseline (`.hephaera/skills/build-gameplay-runtime/references/input-and-locomotion-feel.md` from an installed host's root) when a selected verb needs jump grace, buffered intent, or movement-response tuning. Specify eligibility, clocks, priority, consumption, and reset behavior before choosing compatible engine APIs.
- Read `skills/build-gameplay-runtime/references/damage-windows-and-contact.md` in the resolved Hephaera baseline (`.hephaera/skills/build-gameplay-runtime/references/damage-windows-and-contact.md` from an installed host's root) when designing damage windows, multi-hit rules, immunity, or interruption. Declare attack/strike/recipient identities and authority before adding cosmetic feedback.
- Read [perception-and-fog.md](references/perception-and-fog.md) for shared perception truth, line-of-sight blockers, presentation-only fog, and AI/targeting integration.
- Read [encounter-acceptance.md](references/encounter-acceptance.md) for role composition, pressure budgets, fair transitions, tuning, and deterministic encounter fixtures.

## Output

- A combat and enemy decision specification.
- Encounter composition and tuning ranges.
- Feedback requirements and deterministic acceptance scenarios.

## Guardrails

- Do not hide unfair damage behind visual spectacle.
- Do not infer combat truth from rendered pixels or animation completion.
- Do not tune only from static numbers when playtest evidence contradicts them.
