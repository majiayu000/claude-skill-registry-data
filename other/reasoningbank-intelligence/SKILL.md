---
name: "reasoningbank-intelligence"
description: "Adaptive learning for moflo agents via ReasoningBank: trajectory storage, verdict judgment, memory distillation, consolidation, and MMR retrieval. Use when building agents that should improve from experience across runs."
---

# ReasoningBank Intelligence

Trajectory-based learning pipeline for moflo-enabled agents. Records what an agent did, judges the outcome, distills successful runs into reusable patterns, and retrieves relevant prior experience on the next task.

## Prerequisites

- moflo (the neural subsystem ships inline as part of the moflo package)
- Moflo's memory DB at `.swarm/memory.db` (created on first run)

## Quick Start

```typescript
import { createInitializedReasoningBank } from 'moflo/dist/src/cli/neural/reasoning-bank.js';

const rb = await createInitializedReasoningBank({
  namespace: 'reasoning-bank',
  vectorDimension: 768,
  retrievalK: 3,
  mmrLambda: 0.7,              // 0=pure relevance, 1=pure diversity
  distillationThreshold: 0.6,  // min verdict score to keep
  dedupThreshold: 0.95,
});
```

## The Pipeline

Four stages. You typically call each once per task:

```text
1. Record trajectory  →  storeTrajectory({ id, input, actions, outcome, reward, ... })
2. Judge              →  const verdict = await rb.judge(trajectory)
3. Distill            →  const memory  = await rb.distill(trajectory)   // if verdict good enough
4. Retrieve (next task) →  const hits  = await rb.retrieveByContent(query, k)
```

### 1. Record

```typescript
const trajectory = {
  id: taskId,
  input: userRequest,
  actions: ['read_file', 'edit_file', 'run_tests'],
  outcome: 'success' as const,
  reward: 1.0,                // 0..1
  metadata: { toolCalls: 3, durationMs: 1800 },
  timestamp: new Date(),
};

rb.storeTrajectory(trajectory);
```

### 2. Judge

The built-in judge scores on outcome + reward + action-step quality. No external LLM call.

```typescript
const verdict = await rb.judge(trajectory);
// { score: 0-1, outcome: 'success' | ..., reasoning: string }
```

Swap in your own judge by extending `ReasoningBank` if you want LLM-in-the-loop scoring — this was designed as a rule-based baseline so the hot path stays cheap.

### 3. Distill

Compresses a trajectory into a reusable `DistilledMemory` (signature, approach, outcome-tagged). Skips if the verdict is below `distillationThreshold`.

```typescript
const memory = await rb.distill(trajectory);
// null if verdict below threshold → not worth learning from
```

For batch runs (nightly, offline replay):

```typescript
const memories = await rb.distillBatch(trajectories);
```

### 4. Retrieve

Query by text (embedding generated for you) or by pre-computed vector:

```typescript
const hits = await rb.retrieveByContent(newTaskDescription, 5);
// [{ memory, relevanceScore, diversityScore, combinedScore }]
```

MMR (maximal marginal relevance) prevents the top-K from collapsing to "five slight variations of the same thing" — tune `mmrLambda` to push more diversity.

## Consolidation

Memory quality degrades over time without maintenance. Run consolidation periodically (once a week, once after N new entries, etc.):

```typescript
const result = await rb.consolidate();
// { removedDuplicates, contradictionsDetected, prunedPatterns, mergedPatterns }
```

Consolidation:
- Removes duplicates above `dedupThreshold` similarity.
- Detects contradictions (same signature, opposite outcomes) if `enableContradictionDetection`.
- Prunes entries older than `maxPatternAgeDays`.
- Merges semantically-adjacent patterns.

## Persistence

ReasoningBank persists through `MofloDbAdapter` to `.swarm/memory.db`. Set `enableMofloDb: false` for ephemeral in-memory use (tests).

The `namespace` config isolates reasoning-bank entries from general memory. Default is `reasoning-bank`.

## Anti-Patterns

- **Don't record every step as a separate trajectory.** A trajectory = one task. Steps are a field inside the trajectory.
- **Don't skip the judge.** Distilling every trajectory poisons the pool with failures — that's what `distillationThreshold` guards against.
- **Don't run consolidation on the hot path.** It's a sweep — do it out-of-band.
- **Don't share `namespace` between different agent roles.** Keep `reasoning-bank:reviewer`, `reasoning-bank:researcher`, etc. separate; signatures overlap otherwise.
- **Don't raise `retrievalK` to tame bad retrieval.** Tune `mmrLambda` or the embedder instead — more K just dilutes the top results.

## Integration with moflo's Hooks

Moflo's session/hook system already wires ReasoningBank into the `/flo` spell and the SubAgentStart hook. If you're building a custom agent that should participate, hook into `post-task`:

```typescript
await mcp.hooks_post_task({
  trajectoryId: taskId,
  outcome: 'success',
  reward: 1.0,
});
```

That records, judges, and distills in one call.

## Performance

- Retrieve (k=5, corpus of 10k): ~3–8ms.
- Distill: single call ≈ vector embed + a few similarity checks; ~10–50ms.
- Consolidate: O(n²) in the namespace — run offline for corpora > 10k.

## See Also

- `memory-patterns` skill — for non-trajectory memory (sessions, knowledge)
- `memory-optimization` skill — HNSW tuning, quantization
- `src/cli/neural/reasoning-bank.ts` — full API
- `src/cli/services/learning-service.ts` — trajectory types
