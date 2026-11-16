---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
---

# Arena

> Names in backticks, such as `spawn-worker` and `find-sessions`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here and whether a worker on another agent can be started.

Open a plan with `track-todos`, one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify, Clean up), before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the models. Read `~/.agents/skills/select-model/SKILL.md` and choose each seat's model and how to start it from it. Start every seat as the Subagents section of `../poteto-mode/SKILL.md` says, which also covers a missing `select-model`. The table says what each seat needs, not which model fills it.

   | Seat | Kind | Needs | Count and diversity |
   |---|---|---|---|
   | Runner | code, or prose and judgment, by the task | writes only its own output location | one per distinct approach, at least two on different models, from different vendors when the computer has them. More runners when the arena covers multiple design directions. The same model N times only when the work is generation-bound rather than judgment-sensitive. All start together. A request to keep the run small narrows the scope, not the number of vendors. Only the user asking for fewer vendors does. |
   | Cross-judge | judgment | read-only | one, never from your own model's vendor. Try the other vendors' models in the order `select-model` prefers them. When none of them starts, Phase C skips the judge and says so. It starts after every candidate has finished. |

   Pick each runner's reasoning level and speed for the job, per that section. When a runner's model does not start, use the nearest model of the same vendor, or drop the seat and say so. When dropped seats leave fewer than two runners, add runners until there are two, on a remaining runner's model or, when none remains, on your own model, and say so.
4. Give each candidate its own output location (`isolate-checkout` where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill.

## Phase B: Fan out

Start all N runners at once, each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, start the Cross-judge seat from step 3, read-only, as step 3 says. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't start it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Phase G: Clean up

After Phase F, remove each candidate checkout this run made, with the exact step "Removing a worktree" in `../resolve-capability/references/exact-steps.md`, as written. A candidate folder under `/tmp` that is not a worktree goes with `rm -rf <path>`. Keep the checkout that holds the synthesized artifact until the artifact is committed or copied out of it. Remove nothing this run did not make.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, the verification result, and which candidate checkouts were removed or kept.
