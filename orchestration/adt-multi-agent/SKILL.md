---
name: multi-agent
description: Orchestrate teams of agents — DAG execution, routing, state sharing, failure recovery. Use when coordinating parallel agents in task pipelines with dependencies or distributing work by capability.
triggers:
  - multi-agent
  - parallel agents
  - agent orchestration
  - dag execution
---

# Multi-Agent Orchestration

## What It Does

Coordinates multiple specialized agents. Handles task DAGs, capability routing, state sharing, and failure recovery.

## When to Use

- Multi-agent team patterns (orchestrator-worker, peer, pipeline)
- Task DAGs with dependencies and parallel execution
- Capability-based routing
- State sharing with checkpoints
- Failure recovery (retries, escalation)

## Spawn vs Inline

Spawn when: tasks >30s, parallelizable, or isolated context. Otherwise inline.

## Core Patterns

### 1. Orchestrator-Worker

Central coordinator delegates to specialized workers.

```typescript
class Orchestrator {
  async executeTask(task: Task) {
    const results = [];
    for (const subtask of this.decompose(task)) {
      results.push(await this.selectWorker(subtask).work(subtask));
    }
    return this.synthesize(results, task);
  }
}
```

### 2. DAG Task Execution

Topological sort; execute levels in parallel.

```typescript
class DAG {
  async execute(input: unknown) {
    for (const level of this.partitionIntoLevels(this.topologicalSort())) {
      const results = await Promise.allSettled(
        level.map(id => this.executeTask(id))
      );
      for (let i = 0; i < results.length; i++) {
        if (results[i].status === "rejected") {
          const node = this.nodes.get(level[i])!;
          if (!node.skipOnError) throw results[i].reason;
        }
      }
    }
    return this.exitNodes.map(id => this.results.get(id));
  }
}
```

### 3. Capability-Based Routing

Match task requirements to agent specializations.

```typescript
selectAgent(task: Task): Agent {
  const required = this.extractRequirements(task);
  const candidates = this.agents.filter(a =>
    required.every(r => a.specialties.includes(r))
  );
  return candidates.reduce((best, c) =>
    c.load < best.load ? c : best
  );
}
```

### 4. Shared Context + Checkpoints

Pass mutable context; save snapshots for resumption.

```typescript
class CheckpointedDAG {
  async execute(input: unknown) {
    const context = { requestId: uuid(), data: input, breadcrumbs: [] };
    for (const nodeId of this.topologicalSort()) {
      try {
        await this.nodes.get(nodeId)!.agent.executeWithContext(context);
      } catch (err) {
        if (!this.nodes.get(nodeId)!.skipOnError) throw err;
      }
    }
    return context;
  }
}
```

## Rules

1. One job per agent
2. Explicit contracts (schemas, errors)
3. Shared context only (no global state)
4. Versioned checkpoints
5. Exponential backoff (retries)
6. Escalate non-recoverable errors
7. Cap concurrency
8. Detect cycles
9. Log breadcrumbs
10. Spawn decision: >30s? parallelizable? isolated? if yes: spawn; else inline

See REFERENCE.md for algorithms, retry patterns, and testing.
