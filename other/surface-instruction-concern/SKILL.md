---
name: surface-instruction-concern
description: Runs the stop-consider-confirm protocol when executing a clear instruction as given would be counterproductive. Use when an instruction would destroy or discard committed work, reduce quality or efficiency with no offsetting benefit, contradict a goal the requestor stated, or rest on an apparently stale belief about current state; and when a brief instruction has both a harmful literal reading and a sensible charitable one. Walks the trigger test, the charitable-interpretation and stale-state checks, and the one-round named-options confirmation, calibrated so routine instructions proceed untouched and only material-impact concerns are surfaced, once, concisely.
derives_from: ../../governance/surface-counterproductive-instructions.md
---

# Surface Instruction Concern (before executing it)

## Overview

The failure mode this skill interrupts: fast, compliant execution of an
instruction that is perfectly clear and still the wrong thing to do, because its
execution as given would cost the requestor something they did not foresee. The
highest-severity shape is the silent most-destructive-literal reading: a brief
instruction ("wind down after this") taken to authorize destroying committed work
the requestor did not know existed. The requestor's actual interest, not
compliance, is the goal; a one-sentence confirmation is cheap, and unwinding
executed damage is not.

The canonical rule
([`surface-counterproductive-instructions`](../../governance/surface-counterproductive-instructions.md))
defines the five trigger classes and the calibration; this skill is its workflow
wrapper for the moment an instruction lands and something about executing it as
given feels net-negative.

## When to Use

- Executing the instruction as given would REDUCE efficiency, effectiveness, or
  productivity, with no offsetting benefit the requestor named.
- Executing it as given would lower quality or correctness (introduce a defect,
  skip a verification the work depends on, produce a worse result than the
  requestor would accept seeing it).
- The instruction, read literally, would revert, overwrite, delete, or abandon
  committed or completed work, or take another hard-to-reverse action.
- The instruction contradicts a goal the requestor stated earlier in the session
  or in durable project context.
- The instruction makes sense only under a belief about current state that is
  probably stale (it assumes a step has not started when it has, or a file state
  that has moved).
- A brief instruction admits both a harmful literal reading and a sensible
  charitable one.
- NOT for ambiguity with no harm attached (that is
  [`clarify-before-acting`](../../governance/clarify-before-acting.md) territory),
  and NOT for the optimization-dimension tradeoff among the AIQT tier, Progress, Speed, and Cost
  (the [`project-integrity`](../../governance/project-integrity.md) apex rule
  governs that escalation).

## Process

1. **Stop before the first tool call that would execute the harm.** The trigger is
   in your own internal model: "the instruction says X; doing X would lose / break
   / slow / worsen Y". That clause, present, means do not execute yet.
2. **Name the specific negative effect and cost it.** Which trigger class, and
   concretely what is lost ("this reverts four committed changes", "this re-runs
   work that already merged"). If you cannot name a material cost, the concern
   does not clear the bar: proceed with the instruction.
3. **Check the two silent resolutions before surfacing.** (a) Charitable reading:
   is there a sensible interpretation that avoids the harm? Prefer it, or include
   it in the question; never silently select the destructive literal reading.
   (b) Stale state: if the instruction rests on a checkable belief, validate it
   with a tool call first (a status read, a file read); the instruction may be
   perfectly sound once the real state is in view, or the check gives you the
   concrete cost for the question.
4. **Surface once, concisely, with named options.** One or two sentences: the
   specific downside, the better alternative if one exists, and two to four named
   options with a recommendation first. Use the structured question primitive
   where the toolchain offers one, and in a timed-degradation mode arm the short
   timer alongside the question. This is a one-round confirmation, not a debate.
5. **Act on the answer, finally.** An informed override is final: execute the
   requestor's call without re-litigating. If no answer comes and the environment
   runs a timed-degradation mode, the reversibility gate is absolute: a timeout
   NEVER auto-executes the destructive, irreversible, or work-discarding path;
   hold that action and route to other work, or wind down cleanly.
6. **Record the surfaced decision** where the project keeps its decision trail,
   so a later reader sees the instruction was questioned and how it settled.

## Red Flags

- "Of course!" followed by executing an instruction you privately assessed as
  harmful: sycophancy is the failure mode, not politeness.
- Picking the most destructive literal reading of a brief instruction without a
  confirming question.
- Asking AFTER acting ("I went ahead and reverted it; want it back?").
- Surfacing trivial, no-downside preferences as if they were material concerns:
  the over-ask erodes the signal until real concerns get waved through.
- Continuing to resist after a fully-informed confirmation.
- Reading silence, or a degradation timeout, as authorization for the harmful
  path.

## Verification

The skill's invocation is complete when:

- The concern was either dissolved by a charitable reading or a state check
  (recorded, no question asked), or surfaced ONCE with the cost and named
  options, and the requestor's answer was executed as given.
- No destructive, irreversible, or work-discarding action ran on a timeout or on
  an unconfirmed literal reading.
- The decision trail records the question and its resolution where the project
  keeps such records.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The instruction was clear; my job is to execute." | Clear is not the same as correct. The requestor's interest is the job; a foreseen cost they cannot see is yours to surface. |
| "Asking will annoy them." | One material-impact question, asked once with options, costs a sentence. Executed damage costs the work plus the trust. |
| "It is probably fine." | If the honest answer to "would they still want this seeing its effect?" is "probably not" or "unsure", the bar is met: surface it. |
| "They said it twice, so it is confirmed." | Repetition is not information about the downside. Confirmation counts when the cost was in full view. |

## See Also

- Canonical rule [`surface-counterproductive-instructions`](../../governance/surface-counterproductive-instructions.md):
  the five trigger classes, the charitable-interpretation corollary, the
  calibration section, and the exception protocol this skill wraps.
- Canonical rule [`clarify-before-acting`](../../governance/clarify-before-acting.md):
  the ambiguity-side sibling (multiple reasonable readings, no harm required) and
  the named-options question shape step 4 borrows.
- Sibling skill [`validate-inference`](../validate-inference/SKILL.md): step 3's
  stale-state check is that discipline applied at instruction intake.
- Sibling skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): the
  ambiguity-side counterpart this skill's harm-side mirrors (reciprocates that
  skill's forward "Related skill" link).
