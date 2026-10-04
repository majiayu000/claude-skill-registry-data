---
license: BSL-1.1
name: dag-runtime
description: Executes DAG workflows with parallel wave processing, agent spawning, context isolation, permission enforcement, and full execution tracing. Use when running a planned DAG, managing concurrent agent execution, enforcing isolation boundaries, or tracing execution for debugging. Activate on "execute DAG", "run workflow", "spawn agents", "parallel execution", "execution trace", "agent isolation". NOT for planning DAGs (use dag-planner), validating outputs (use dag-quality), or matching skills (use dag-skills-matcher).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
metadata:
  category: DAG Framework
  tags:
    - dag
    - runtime
    - execute-dag
    - run-workflow
    - spawn-agents
category: Agent & Orchestration
tags:
  - dag
  - runtime
  - execution
  - engine
  - management
---

# DAG Runtime

Executes DAG workflows with parallel wave processing, agent spawning, context isolation, permission enforcement, and full execution tracing.

## Decision Points

### Isolation Level Selection
```
Input: threat model + node characteristics
├── Untrusted code execution?
│   └── YES → Container isolation
├── Resource limits needed?
│   └── YES → Process isolation
├── Context contamination risk?
│   └── YES → Context isolation
└── Cooperative nodes on same task?
    └── YES → None isolation
```

### Failure Escalation Strategy
```
Node fails → Check failure type:
├── Timeout/Rate limit?
│   └── Retry with exponential backoff (max 3x expensive models, 10x cheap)
├── Invalid output schema?
│   └── Retry with schema reminder + example (max 2x)
├── Permission denied?
│   └── Check parent permissions → escalate to human if mismatch
├── Skill not found?
│   └── Mutate DAG: remove node or find alternative skill
└── Persistent failure after max retries?
    └── Human review required
```

### Wave Completion Criteria
```
All nodes in wave complete → Check status:
├── All succeeded?
│   └── Advance to next wave
├── Some failed but non-blocking?
│   └── Mark outputs as null, advance with warning
├── Critical node failed?
│   └── Halt execution, trigger failure handling
└── Mixed success/retry?
    └── Wait for retries to complete
```

## Failure Modes

### **Permission Creep**
- **Symptoms**: Child nodes have more permissions than parent
- **Detection**: `if child.permissions.tools ⊃ parent.permissions.tools` 
- **Fix**: Intersect child permissions with parent before execution

### **Context Pollution**
- **Symptoms**: Node sees conversation history from unrelated nodes
- **Detection**: Node prompt contains references to other node IDs
- **Fix**: Enforce context isolation, only pass declared inputs

### **Zombie Wave**
- **Symptoms**: Wave never completes, some nodes stuck in "running" state
- **Detection**: Wave active > 2x max node timeout with no status updates
- **Fix**: Force-kill hung nodes, escalate to failure handling

### **Resource Exhaustion**
- **Symptoms**: New agents fail to spawn, memory/CPU limits hit
- **Detection**: Agent spawn returns resource error
- **Fix**: Queue remaining nodes, increase isolation level if needed

### **Cost Spiral**
- **Symptoms**: Nodes repeatedly retry expensive operations
- **Detection**: Node cost > 10x budget or total DAG cost > safety limit
- **Fix**: Halt execution, require human approval to continue

## Worked Examples

### Multi-Wave DAG with Failure Recovery

**Scenario**: 3-wave codebase analysis DAG where Wave 2 node fails

```yaml
# Initial DAG state
Wave 1: [scan-files] → completed
Wave 2: [analyze-architecture, check-security] → analyze-architecture fails
Wave 3: [generate-report] → blocked
```

**Decision Navigation**:
1. **Failure occurs**: `analyze-architecture` returns malformed JSON
2. **Failure type check**: Invalid schema → retry with schema reminder
3. **Retry fails**: Still malformed → escalate to human
4. **Wave completion check**: One node failed, one succeeded
   - `check-security` succeeded, output available
   - `analyze-architecture` failed, mark output as null
5. **Dependency check**: `generate-report` requires both outputs
   - **Decision**: Can proceed with partial data? Check node config
   - If `required: false` → advance with warning
   - If `required: true` → halt execution

**Expert catches**: Checking dependency requirements before advancing wave
**Novice misses**: Would either block forever or advance with missing critical data

### Isolation Trade-offs

**Scenario**: Code execution node needs filesystem access but has security concerns

```yaml
node: code-formatter
skills: [python-formatter]
inputs: {source_files: [...]}
permissions: {tools: [Read, Write, Bash], paths: ["/workspace/src"]}
```

**Decision Navigation**:
1. **Threat assessment**: Bash tool + external code = high risk
2. **Isolation decision tree**:
   - Untrusted code? YES → Container isolation
   - But: Container isolation blocks filesystem writes to host
3. **Trade-off resolution**:
   - Use container with mounted volume: `/workspace/src` → `/container/workspace`
   - Restrict bash to safe commands only
   - Set resource limits: 1GB RAM, 30s timeout

**Expert catches**: Need to balance security with functionality
**Novice misses**: Would either over-isolate (breaking functionality) or under-isolate (security risk)

## Quality Gates

- [ ] All wave dependencies satisfied before execution starts
- [ ] Each node has valid isolation level for its threat profile
- [ ] Permission inheritance properly restricted (child ⊆ parent)
- [ ] All required trace fields populated (node_id, model, tokens, cost, duration)
- [ ] Node timeouts set and enforced (default 300s)
- [ ] Cost budgets defined and monitored per node
- [ ] Retry limits configured (max 3 expensive, 10 cheap models)
- [ ] Context isolation prevents cross-node conversation leakage
- [ ] Failed node outputs properly marked as null/unavailable
- [ ] Execution can be resumed from any completed wave

## NOT-FOR Boundaries

**Don't use dag-runtime for**:
- **DAG structure planning** → Use `dag-planner` instead
- **Output quality validation** → Use `dag-quality` instead  
- **Skill-to-task matching** → Use `dag-skills-matcher` instead
- **Real-time interactive workflows** → Use direct agent calls
- **Single-step tasks** → Use individual skills directly

**Delegate to other skills when**:
- Output doesn't meet quality standards → `dag-quality`
- Need to modify DAG structure mid-execution → `dag-planner`
- Agent needs different skill for retry → `dag-skills-matcher`