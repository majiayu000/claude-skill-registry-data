---
name: experience-and-transmission
shapes: [experience-and-transmission]
description: >
  The artifact is correct and nobody can use, learn, or read it. Use when every
  component metric is green but the end-to-end experience is broken, when
  onboarding is too slow or documentation goes unread, when the observer is
  inside the system being studied (UX research, dogfooding), or when code is
  right but unreadable by the next maintainer.
---

# Experience and Transmission

**Problem shape:** correctness is not the bottleneck — arrival is. The system
passes its tests and fails its user, the documentation exists and is not read,
the code runs and cannot be maintained, or the thing being studied changes
because the studier is part of it. The deliverable is comprehension and use,
measured on the receiving end rather than asserted on the producing end.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [jobs](../../agents/genius/jobs.md) | the product "works" per component metrics but the integrated experience is broken — treat the whole experience as the spec, hunt the seams, edit ruthlessly rather than add |
| [vygotsky](../../agents/genius/vygotsky.md) | onboarding is too slow or too overwhelming, or documentation exists and nobody reads it — locate the zone of proximal development, scaffold inside it, and plan the fading; diagnose the misconception rather than repeating the explanation |
| [varela](../../agents/genius/varela.md) | the observer cannot be separated from the system studied (UX research where the experience *is* the product, dogfooding, introspective debugging) — run trained first-person observation and third-person measurement concurrently and report their mutual constraints |
| [knuth](../../agents/genius/knuth.md) | the program is correct and unreadable — literate programming, writing for the human reader first; and building the tool before using it when no adequate one exists. **Entry point is transmission, not performance:** for profiling and optimization work, knuth is routed via the performance path, not this shape |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. The evidence must come from the receiving end — an
   observed user, a real ramp-up, a maintainer who was not the author. A claim
   that something "is clear" asserted by its own author does not satisfy this
   shape.
4. Typical chain: varela gathers first-person data without pretending the
   observer is outside → jobs specifies the integrated experience from it →
   vygotsky sequences the scaffolding that gets people there. Run via
   `tools/genius-invoker.sh compose varela jobs vygotsky -- "<problem>"`.
5. If no shape above matches, do not force a genius — use a standard team agent
   (INDEX.md routing rule).

## Refuse when

- No contact with an actual recipient is possible or planned — this shape
  measures arrival, and with no receiving end there is nothing to measure.
- The request is to make the experience *feel* better while a known defect
  behind it stays unfixed.
- First-person report is offered as the sole evidence with no third-person
  measurement alongside it (varela's constraint is mutual, not one-sided).
