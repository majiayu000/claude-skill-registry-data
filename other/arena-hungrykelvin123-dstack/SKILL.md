---
name: arena
description: "Compare isolated, parent-defined alternatives against a concrete rubric and synthesize the result. Use for $arena or an explicitly requested candidate comparison."
---

# Arena

Before delegating or using optional capabilities, read [the runtime contract](../david-mode/references/agent-runtime.md). It owns eligibility, model selection, limits, and fallback.

Fan out N isolated attempts at the same bounded task under the runtime worker policy. The parent frames alternatives and invariants, reads every candidate, chooses a base, and integrates the useful parts. Difficult production code and final architecture stay with the parent; workers can supply evidence, bounded sketches, or disposable prototypes for those decisions.

## Start

Open a todolist with one entry per phase before launching anything. The arena runs autonomously and the list keeps phases from silently disappearing.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract. Get it right before spawning anything.

1. State the artifact each candidate is producing and why the requested comparison earns its repeated-context and review cost. Settle shared constraints in the parent before dispatch; candidates must not depend on each other's intermediate work.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. Concrete: `Adds a --dry-run flag that skips writes`. Vague: `code is correct`. The rubric is the picker's tool in Phase D; candidates only see the task.
3. Choose the smallest candidate set that tests distinct parent-defined alternatives, normally two. Classify the candidate before dispatch: use the narrow tier for a search or disposable sketch and the complex tier for bounded implementation or multi-step reasoning. Every candidate uses the active client's selected route from the runtime contract. Apply its concurrency limit and queue excess candidates. More attempts do not provide model diversity.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp1-<slug>/candidate-<n>/`). N candidates writing to the same path is shared mutable state and fails the **separate-before-serializing-shared-state** principle skill test.

## Phase B: Fan out

Dispatch ready candidates within the runtime limit after isolation, each with the task, shared grounding, its own output path, and instructions to produce both the artifact and a short rationale. Candidates do not delegate further.

The rationale is mandatory. Without it, the parent cannot tell whether a candidate's structure is principled or accidental, which makes Phase E grafting unreliable. Each rationale names the alternatives the candidate considered and what it rejected.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all Phase B candidates complete, use one fresh read-only worker under the same selected tier as an independent judge when it can resolve a concrete comparison risk. It sees the rubric and completed candidates, scores each criterion, and recommends a base. It may run alongside the parent's reading in Phase D. If no extra judgment is needed or the selected worker route is unavailable, the parent scores directly and labels this phase parent-only. The parent owns the final decision.

## Phase D: Pick a base

Read every candidate end to end before picking. Skimming N candidates surfaces only the candidate whose surface looks most familiar.

Score each candidate against the rubric criterion by criterion. Compare against the judge when one ran and resolve disagreements from evidence. Agreement between workers using the same model is not proof of correctness.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller surface area when two feel tied, per the Laziness Protocol.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each graft in by hand, per the **redesign-from-first-principles** principle skill. Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why. The rejection notes are the highest-signal part of the record. Future readers learn from what you considered and dropped, not just what you kept.

When candidates converge, verify their shared assumptions before accepting the shape. When they diverge, the parent resolves the disputed constraints and decides which evidence is missing. Apply the runtime revision limit; repeated retries go back to the parent.

## Phase F: Verify

The synthesized artifact has to hold up under the same scrutiny as any other output, per the **prove-it-works** principle skill. The arena does not earn you a pass.

If verification exposes a missed constraint or graft, the parent fixes the framing or integration and rechecks the result. Another candidate run must fit the runtime revision limit; otherwise the parent takes over.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.
