---
name: arena
description: "Use for \"arena this\", or when one attempt at a non-trivial artifact would lock in the wrong shape. Spawns N candidates at the same task, picks the strongest as a base, grafts the best parts of the others into it, verifies the result. Ships one artifact."
disable-model-invocation: true
---

# Arena

N parallel attempts at the same task. Read every one end to end. Pick the strongest as the base. Graft the best ideas from the rest into it. Verify. Ship one thing.

## Start

A todo list with one entry per phase. Frame, fan out, cross-judge, pick, graft, verify. The list is what keeps a phase from quietly disappearing.

## Frame

Every candidate gets the same prompt, so the prompt is the contract. Get it right first.

1. **State the artifact** each candidate produces.
2. **Write the rubric.** What success looks like for this task, as three to six criteria you can grade. Concrete, "adds a --dry-run flag that skips writes". Not "code is correct". The rubric is for the judge and for you. Candidates see only the task.
3. **Pick the runners.** Different models by default, one each. More when the arena covers several design directions. The same model N times when the work is generation-bound rather than judgment-bound.
4. **Give each candidate its own output path.** A worktree where possible, otherwise its own directory. N candidates writing to one path is shared state and fails `no-shared-writes`.

## Fan out

Spawn all N at once, in the background. Each gets the task, the shared grounding, its own output path, and an instruction to produce the artifact plus a short rationale.

The rationale is mandatory. Without it you can't tell whether a candidate's shape is principled or accidental. Each rationale names the alternatives it considered and what it rejected.

If a candidate produces nothing, continue with N minus one and note the dropout.

## Cross-judge

Once every candidate is done, spawn one read-only judge on a different model family from your own. It gets the rubric and the candidates by path label. It scores each criterion and recommends a base with a reason. Don't spawn it while candidates are still writing, or it grades half-finished work as dropouts.

## Pick

Read every candidate end to end before choosing. Skimming finds the one that looks most familiar, not the best one.

Score against the rubric criterion by criterion, not on feel. Compare with the judge. Agreement confirms the pick. Disagreement means one of you is biased or the rubric was vague. Read both reasons before deciding.

Pick the base a future maintainer can extend most easily without breaking anything. When two feel tied, take the cleaner boundary or the smaller interface.

Write down the pick and the reason in a short synthesis note beside the base, including what the judge said.

## Graft

Walk each losing candidate once more. What's worth porting into the base? Usually one or two things per candidate, not most of it.

Fold each graft in by hand, as if it had been part of the design from the start. Don't paste.

Record what was grafted, from which candidate, and what was rejected and why. The rejections are the most useful part of the record.

When N candidates converge on the same shape, that's a strong signal. Note it, ship the consensus, skip grafting. When they diverge wildly, the frame was too loose. Reframe and rerun instead of averaging.

## Verify

The synthesized artifact gets the same scrutiny as anything else. Run it, prove it, attach the evidence.

If verification finds something the arena missed, either the frame was wrong and you rerun, or one candidate caught it and you missed the graft. Go back. Don't paper over.

## Output

One artifact. One synthesis note beside it naming the base, the grafts with their source, the rejections, any dropouts, and the verification result.
