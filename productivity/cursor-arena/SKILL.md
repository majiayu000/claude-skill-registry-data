---
name: cursor-arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

## Codex runtime mapping

This published workflow is explicit-only through `agents/openai.yaml`; the proven branch is a bounded local design Arena. Before starting, require at least two authorized, isolated candidates and an available independent judge; retain the same rubric and verification contract. Outside that proven scope, report the workflow as unavailable unless a separate task-specific proof supports it. Use native Codex subagents and isolated paths for parallel candidates, not Cursor `Task`, Work cloud, or `~/.cursor/rules`. In the observed native path, candidates used `collaboration.spawn_agent` with `agent_type=general-worker` and the cross-judge used `agent_type=reviewer`; the exact upstream Cursor roles and automatic trigger are not proven. Keep the same rubric, full-candidate read, cross-judge, base selection, named graft, redesign-on-failure, and verification phases. Follow the standing model router and task authority; record invocation metadata separately from worker self-report.

# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. The rubric is the picker's tool in Phase D. Candidates only see the task.
Choose available native Codex runners under the standing `model-capability-router` policy and the operator’s explicit selection. Use structurally distinct prompts or models when comparison needs diversity; record the actual runners.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per `cursor-principle-separate-before-serializing-shared-state`.

## Phase B: Fan out

Launch N independent Codex subagents in parallel when authorized, each with the same task contract, the shared grounding path, its own isolated output path, and a short rationale. Keep one writer per path and wait for each artifact before judging.

Each rationale names the alternatives the candidate considered and what it rejected.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record. Mark the aggregate PARTIAL. If fewer than two candidates completed, do not select a winner or claim Arena competition; report the surviving artifact as a single attempt.

## Phase C: Cross-judge

choose an available native Codex judge under the standing `model-capability-router` policy, preferably with an independent model perspective when available. Spawn one read-only judge subagent after candidate writes finish. If no authorized independent judge is available, the coordinator may assess the candidates but must mark the aggregate PARTIAL and must not call its own assessment a cross-judge verdict.

## Phase D: Pick a base

Read every candidate end to end before picking.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller API when two feel tied, per the Laziness Protocol.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each graft in by hand, per `cursor-principle-redesign-from-first-principles`. Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why.

When N candidates converge on the same shape, that is a strong agreement signal. Note the convergence in the record and ship the consensus shape. No graft is needed. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

The synthesized artifact has to hold up under the same scrutiny as any other output, per `cursor-principle-prove-it-works`.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Don't paper over.

## Outputs

One synthesized artifact when competition and independent judgment completed; otherwise label the result PARTIAL and state which phase was missing. One short synthesis note alongside, naming the base if selected, the grafts (with source candidate), the rejections, the dropouts if any, the actual judge or coordinator assessment, and the verification result.
