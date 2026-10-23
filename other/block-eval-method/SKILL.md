---
name: block-eval-method
description: "Use when a block, rule set or agent definition has to be measured against the same agent without it on a real task set, not argued about: isolate each run so nothing leaks, prove the instruments before spending, compare arms task by task with a sign test, check that shorter output still does the whole job, and judge replies blind with gated judges."
---

# block-eval-method

Cross-cutting, meta (`WORKFLOW.md` §2). It is the measurement layer under the 🟡 to 🟢 decision: how to run
"with the block" against "without it" on real tasks so that the difference is the block's and not the
harness's. The protocol that says *what to test* is `skills/testing-blocks` (pressure scenarios §1 to §6,
compliance §7, the three arms, the model matrix and the exit gate §8). The pitfalls of baselines, assertions
and judges in general are in `skills/llm-eval-regression-pitfalls`. This block carries what those two do not:
the run hygiene and the judging machinery of one concrete method.

The method is a way of working, not a tool. It needs a way to start a headless agent session per task and read
what it left behind. Nothing here installs a harness; if you have none, `skills/testing-blocks` runs the two
arms by hand.

## When
- A block, a rule set or an agent definition is about to be called "better" on the strength of runs.
- An earlier run mixed arms in one context, or one arm saw a file the others did not.
- Output got shorter and someone says it is no worse: that claim needs the completeness check of §4.

## Steps

Read the rows whose trigger the task meets: a section read is a section applied.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Isolating each run: workspace, loaded instructions, tools, proof of what was injected | any run is designed or a result looks contaminated | [`01-isolation.md`](./references/01-isolation.md) |
| 2 | Instruments before spend: hidden checks, reference answers, what counts as quality | a task set is written | [`02-instruments.md`](./references/02-instruments.md) |
| 3 | Measures and the per-task comparison, sign test | results have to be turned into a claim | [`03-measures-and-comparison.md`](./references/03-measures-and-comparison.md) |
| 4 | Judges: completeness, over-building, reply quality, pairwise, and their gates | an LLM scores what no script can | [`04-judges.md`](./references/04-judges.md) |

## Output / checkpoint
A claim of the form "on this task set, on this model, in this harness, arm B beat arm A on X of Y tasks, with
no completeness loss", plus the limits (§3.15) and the fixture version of `skills/testing-blocks` §8. It says
*measured on a fixture*, which is weaker than *used on real work* and promotes nothing past 🟡 on its own.

## Guardrails
- **Every claim carries its limits:** one model, one harness, the tools that were off, and which tasks had a
  deterministic check. A pass rate is never quoted for tasks without one.
- **No judge scores anything before its own gate passes** (§4). A judge that cannot rank a known-good answer
  above a known-bad one is not an instrument.
- **A run that leaked is thrown away,** not corrected for. Re-run it isolated.
- **Another author's figures are not ours.** Cite a published result as that author's, never as a fact about
  this repository's blocks.

## Origin
The method of the agentic benchmark of a public repository (MIT), read 2026-10-19: its README, its results
page and its run, comparison and judge scripts. Sources, what was dropped for lack of a script, and what was
not verified are in [`origin.md`](./references/origin.md). Status 🟡: written, never run by us.
