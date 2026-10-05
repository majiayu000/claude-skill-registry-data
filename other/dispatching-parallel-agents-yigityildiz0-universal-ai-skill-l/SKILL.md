---
name: dispatching-parallel-agents
description: "Partition and coordinate two or more independent workstreams without duplicating work, leaking expected conclusions, or creating shared-file conflicts. Use for parallel research, multi-area diagnosis, independent reviews, comparisons, test investigation, or large tasks that benefit from bounded concurrent or batched execution. Turkish triggers: işi paralel ajanlara böl, bağımsız alt görevleri dağıt, sonuçları birleştir."
---

# Dispatch Parallel Work

Reduce elapsed time or improve independent verification without weakening integration. Use only capabilities exposed by the active host; do not assume a vendor, model, or named orchestration tool.

## Decide whether to split

Parallelize only when all are true:

- at least two workstreams can progress independently;
- each has bounded inputs and a concrete output;
- workers will not edit the same files or mutate the same external object;
- one owner can verify and integrate the results;
- coordination cost is lower than the expected benefit.

Stay sequential when one result determines the next step, the task is small, or workstreams compete for shared state.

## Capability ladder

Choose the first available mode:

1. Independent subagents or workers.
2. Concurrent tool calls for independent reads, searches, or checks.
3. Batched tool calls containing multiple independent queries or inputs.
4. Sequential execution that preserves separate workstream contracts and evidence.

Hosts without subagents should normally use concurrent or batched retrieval when supported. Never report parallel execution that did not happen.

## Partition the work

Split by independent question, component, data source, failure hypothesis, or review lens. Do not split by arbitrary line count when workstreams need the same reasoning context.

Give each workstream:

1. one objective and explicit exclusions;
2. the minimum source paths or context needed;
3. permission boundaries and whether work is read-only;
4. an output contract: findings, evidence, changes, tests, risks, and open questions;
5. a unique output path if it writes an artifact;
6. a stop condition and expected level of depth.

Do not reveal the expected answer to an independent verifier.

## Protect shared state

- Assign disjoint files and directories for edits.
- Never let two workers update the same config, lockfile, branch, issue, database record, or external object concurrently.
- Tell workers that unrelated changes belong to the user or another worker.
- Give cross-cutting edits to one integration owner.
- Prefer read-only parallel exploration before mutating work.
- Stop or redirect a workstream when its premise becomes invalid.

## Integrate

1. Confirm every requested workstream returned a result or explicit blocker.
2. Inspect evidence, diffs, and artifacts instead of trusting summaries alone.
3. Compare overlapping claims and investigate disagreements.
4. Merge in dependency order through one owner.
5. Run combined verification after integration.
6. Report the integrated result, remaining uncertainty, and exclusions.

## Failure handling

- Retry only transient failures or unclear contracts.
- Narrow or split an oversized assignment instead of repeating it unchanged.
- Continue independent workstreams if one is blocked.
- Treat partial output as evidence, not completion.
- Fall back one level in the capability ladder when concurrency is unavailable or exhausted.

## Completion check

- No duplicate work remained unexplained.
- No two writers touched the same state concurrently.
- All claims and changes have an owner and evidence.
- Cross-workstream contradictions were resolved or surfaced.
- Combined tests ran after merge, not only inside isolated workstreams.
