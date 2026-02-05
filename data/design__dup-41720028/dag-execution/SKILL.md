---
name: DAG Execution
description: This skill should be used when the user asks about "DAG execution", "directed acyclic graph", "task dependencies", "parallel task execution", "topological sort", "level-based execution", "dependency resolution", or needs guidance on executing tasks with dependencies efficiently.
version: 1.0.0
---

# DAG Execution

Establish efficient parallel execution of tasks using Directed Acyclic Graph (DAG) structures to maximize throughput while respecting dependencies.

## What is DAG Execution?

A DAG (Directed Acyclic Graph) represents tasks as nodes and dependencies as directed edges. This structure enables:

- **Parallel Execution**: Independent tasks run simultaneously
- **Dependency Respect**: Tasks wait for prerequisites
- **Optimal Ordering**: Topological sort ensures valid execution
- **Clear Visualization**: Easy to understand task flow

## DAG Structure

### Node Definition

```typescript
interface TaskNode {
  id: string;              // Unique task identifier
  name: string;            // Human-readable name
  agent: string;           // Assigned agent type
  dependencies: string[];  // IDs of prerequisite tasks
  level: number;           // Execution level (computed)
  status: 'pending' | 'running' | 'completed' | 'failed';
  priority: number;        // Higher = more important
  outputs?: any;           // Task results
}
```

### Edge Definition

```typescript
interface DependencyEdge {
  from: string;  // Source task ID
  to: string;    // Target task ID
  type: 'hard' | 'soft';  // hard = blocking, soft = preferred
}
```

## Level Computation

Tasks are assigned execution levels based on dependencies:

### Algorithm (Topological Sort)

```
1. Find all nodes with no dependencies → Level 0
2. Remove Level 0 nodes from graph
3. Find nodes whose dependencies are all assigned → Level 1
4. Repeat until all nodes assigned
```

### Example

```
Task A (no deps)      → Level 0
Task B (no deps)      → Level 0
Task C (depends on A) → Level 1
Task D (depends on B) → Level 1
Task E (depends on C, D) → Level 2
```

### Visual Representation

```
Level 0:  [Task A] ←→ [Task B]     Execute in parallel
              ↓           ↓
Level 1:  [Task C] ←→ [Task D]     Wait for L0, then parallel
              ↓           ↓
Level 2:      [Task E]              Wait for L1
```

## Execution Strategy

### Level-Based Parallel Execution

1. **Initialize**: Compute levels for all tasks
2. **Execute Level 0**: Launch all L0 tasks in parallel
3. **Wait**: Block until all L0 tasks complete
4. **Proceed**: Move to Level 1, repeat
5. **Continue**: Until all levels complete

### Parallel Execution Rules

| Rule | Description |
|------|-------------|
| **Same Level** | All tasks at same level can run in parallel |
| **Cross Level** | Tasks at Level N+1 wait for all Level N |
| **Resource Limit** | Max 13 concurrent agents |
| **Priority** | Higher priority tasks scheduled first |

### Failure Handling

When a task fails:

1. **Mark Failed**: Update task status
2. **Cascade Check**: Find dependent tasks
3. **Block Dependents**: Mark as blocked
4. **Continue Others**: Execute unaffected tasks
5. **Recovery Option**: Retry or manual intervention

## Building a DAG

### From Task List

```yaml
tasks:
  - id: explore-codebase
    name: "Explore existing codebase"
    agent: code-explorer
    dependencies: []

  - id: gather-requirements
    name: "Gather requirements"
    agent: requirements-analyst
    dependencies: []

  - id: design-architecture
    name: "Design solution architecture"
    agent: architect-supreme
    dependencies: [explore-codebase, gather-requirements]

  - id: implement-core
    name: "Implement core functionality"
    agent: coder
    dependencies: [design-architecture]

  - id: implement-tests
    name: "Write test suite"
    agent: unit-tester
    dependencies: [design-architecture]

  - id: run-tests
    name: "Execute test suite"
    agent: test-runner
    dependencies: [implement-core, implement-tests]
```

### Resulting Levels

```
Level 0: explore-codebase, gather-requirements
Level 1: design-architecture
Level 2: implement-core, implement-tests
Level 3: run-tests
```

## DAG Validation

Before execution, validate the DAG:

### Validation Checks

| Check | Purpose |
|-------|---------|
| **Cycle Detection** | Ensure no circular dependencies |
| **Orphan Detection** | Find unreachable nodes |
| **Dependency Exists** | All referenced tasks exist |
| **Agent Available** | Required agents are defined |

### Cycle Detection Algorithm

```
1. Perform DFS from each node
2. Track visited nodes in current path
3. If revisit node in current path → CYCLE
4. If complete without revisit → VALID
```

## Optimization Strategies

### Critical Path Analysis

Identify the longest path through the DAG:
- These tasks determine minimum completion time
- Prioritize critical path tasks
- Allocate best resources to critical path

### Load Balancing

Distribute work evenly across agents:
- Track agent workload
- Assign new tasks to least-loaded agent
- Consider task complexity in assignment

### Speculative Execution

For soft dependencies:
- Start task before dependency completes
- Cancel if dependency fails
- Commit if both succeed

## State Management

### Task State Transitions

```
PENDING → RUNNING → COMPLETED
                  ↘ FAILED → RETRYING → COMPLETED
                                      ↘ BLOCKED
```

### State Persistence

Checkpoint task states for recovery:

```yaml
dag_checkpoint:
  timestamp: "2025-12-13T10:00:00Z"
  tasks:
    - id: "task-1"
      status: "completed"
      outputs: {...}
    - id: "task-2"
      status: "running"
      started_at: "2025-12-13T09:55:00Z"
    - id: "task-3"
      status: "pending"
```

## Integration with Phases

DAG execution integrates with the 6-phase protocol:

| Phase | DAG Role |
|-------|----------|
| **EXPLORE** | Build initial task graph |
| **PLAN** | Optimize and validate DAG |
| **CODE** | Execute implementation DAG |
| **TEST** | Execute test DAG |
| **FIX** | Dynamic DAG for fixes |
| **DOCUMENT** | Execute documentation DAG |

## Saga Pattern for Recovery

When tasks fail, use saga pattern for compensation:

### Compensation Chain

```
Task A completes → Task B fails
                    ↓
         Compensate A (rollback)
                    ↓
         Return to known good state
```

### Compensation Actions

| Task Type | Compensation |
|-----------|--------------|
| File Create | Delete file |
| File Modify | Restore backup |
| Database Change | Rollback transaction |
| External API | Reverse API call |

## Additional Resources

### Reference Files
- **`references/dag-algorithms.md`** - Detailed algorithms
- **`references/optimization.md`** - Advanced optimization techniques

### Examples
- **`examples/sample-dag.json`** - Complete DAG example
- **`examples/execution-trace.json`** - Execution log example
