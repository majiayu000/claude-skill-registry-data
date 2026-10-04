---
name: problem-reframing
shapes: [problem-reframing]
description: >
  The question itself may be the bug. Use when a debate goes in circles, both
  options of a binary feel wrong, improving one parameter degrades another,
  "we're stuck" on a problem that resists direct attack, a metaphor is doing
  hidden work in the architecture, or a trade-off is being denied rather than made.
---

# Problem Reframing

**Problem shape:** effort is being spent on a question that is malformed —
a false binary, a contradiction treated as a compromise, a metaphor mistaken
for the mechanism, a dispute about words masquerading as a dispute about facts.
The move: dissolve, restate, or invert the frame before solving anything.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [wittgenstein](../../agents/genius/wittgenstein.md) | the dispute is about how words are being used — audit the language game; some problems dissolve rather than resolve |
| [nagarjuna](../../agents/genius/nagarjuna.md) | both sides of a binary feel wrong — run the tetralemma (true / false / both / neither) |
| [aristotle](../../agents/genius/aristotle.md) | "why" questions conflated — separate the four causes; catalog the fallacies in play |
| [midgley](../../agents/genius/midgley.md) | a metaphor (machine, war, market, brain) silently shapes the design — audit where it breaks down |
| [leguin](../../agents/genius/leguin.md) | a trade-off is being denied — force the genuine cost onto the table; audit the narrative frame of the plan |
| [eco](../../agents/genius/eco.md) | the artifact will be interpreted — design for the model reader; bound the open vs closed interpretations |
| [bateson](../../agents/genius/bateson.md) | the conflict escalates symmetrically or the instructions double-bind — the pathology is in the interaction, not the parties |
| [altshuller](../../agents/genius/altshuller.md) | improving one parameter degrades another — formulate the contradiction and resolve it, don't compromise |
| [polya](../../agents/genius/polya.md) | stuck on a problem that resists direct attack — restate, work backward, find the related solved problem, specialize |
| [schon](../../agents/genius/schon.md) | the current approach keeps failing mid-action — surface the implicit frame and switch strategy deliberately |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. The deliverable is the reframed question plus what the
   new frame makes visible — then route the reframed problem to the right
   skill (estimation, causal-audit, formal-correctness, ...).
4. Typical chain: wittgenstein dissolves the verbal dispute → altshuller
   formulates the residual contradiction → polya attacks it. Run via
   `tools/genius-invoker.sh compose wittgenstein altshuller -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The frame is fine and the problem is just hard — reframing as procrastination.
- The requester wants the reframe to make a real trade-off disappear.
