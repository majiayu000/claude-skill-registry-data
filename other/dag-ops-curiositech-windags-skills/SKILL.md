---
license: BSL-1.1
name: dag-ops
description: Operations, debugging, and optimization for DAG workflows. Performs root cause analysis on failures, profiles execution performance, aggregates results from parallel branches, bridges context between nodes, and learns patterns from execution history. Activate on "DAG failed", "why did it fail", "root cause", "performance profile", "aggregate results", "merge branches", "execution patterns", "optimize DAG". NOT for planning DAGs (use dag-planner), executing DAGs (use dag-runtime), or validating outputs (use dag-quality).
allowed-tools: Read,Write,Edit,Grep,Glob
metadata:
  category: DAG Framework
  tags:
    - dag
    - ops
    - dag-failed
    - why-did-it-fail
    - root-cause
category: Agent & Orchestration
tags:
  - dag
  - operations
  - monitoring
  - management
  - execution
---

# DAG Ops

Operations, debugging, and optimization for DAG workflows. Handles failure analysis, performance profiling, result aggregation, and pattern learning.

## Decision Points

### Failure Response Strategy
```
If failure is transient (timeout, rate limit):
├── Immediate retry with exponential backoff
├── If retries exhausted → escalate with timeline

If failure is model-related (refusal, format error):
├── Try alternative model with same tier
├── If all models fail → escalate with prompt review needed

If failure is contract violation (schema mismatch):
├── Check upstream node outputs for corruption
├── If upstream OK → retry with explicit schema validation
├── If upstream corrupt → trace to root cause

If failure is cascade (downstream propagation):
├── Find first failing node in dependency chain
├── If root cause confidence > 80% → auto-fix and re-execute
├── If root cause confidence < 80% → escalate with partial diagnosis

If failure is resource constraint (cost/token limits):
├── Check if downgrade possible (Sonnet → Haiku)
├── If downgrade viable → auto-apply and retry
├── If no viable downgrade → escalate with resource request
```

### Performance Optimization Routing
```
If bottleneck is on critical path:
├── Duration > 30s → check for parallelization opportunities
├── Cost > $0.50 per node → evaluate model downgrade
├── Retry count > 2 → flag for prompt optimization

If resource utilization is suboptimal:
├── Parallel capacity unused → recommend dag-planner restructure
├── Model overkill detected → auto-route to cheaper alternative
├── Queue wait time > execution time → flag resource scaling
```

### Result Aggregation Strategy
```
If parallel branches produce same data type:
├── Content similarity > 90% → deduplicate and merge
├── Content similarity 50-90% → synthesize with conflict resolution
├── Content similarity < 50% → concatenate with clear attribution

If parallel branches produce different formats:
├── Compatible schemas → normalize and merge
├── Incompatible schemas → escalate for format reconciliation

If results conflict (contradictory facts):
├── Confidence scores available → select highest confidence
├── No confidence scores → escalate for human resolution
```

## Failure Modes

### Symptom Chasing
**Detection:** Multiple downstream failures after single upstream error, with separate remediation attempts for each failure.
**Diagnosis:** Not tracing failures back to root cause, treating symptoms as independent problems.
**Fix:** Always trace backward through dependency graph until finding first deviation from expected output.

### Auto-Fix Overconfidence
**Detection:** Automatic remediation applied when root cause confidence < 70%, leading to repeated failures.
**Diagnosis:** Acting on weak diagnosis without escalating for human review.
**Fix:** Set confidence threshold at 80% for auto-fix, escalate below threshold with partial analysis.

### Context Drop
**Detection:** Downstream nodes failing due to missing context that was available in earlier waves.
**Diagnosis:** Not bridging context across non-adjacent nodes in the DAG.
**Fix:** Maintain context registry with node dependencies, propagate relevant context forward.

### Aggregation Blindness
**Detection:** Parallel branch results merged without conflict detection, producing incoherent output.
**Diagnosis:** Assuming parallel results are always compatible without validation.
**Fix:** Always run similarity analysis and conflict detection before merging parallel results.

### Performance Tunnel Vision
**Detection:** Optimizing individual node performance while ignoring overall DAG efficiency.
**Diagnosis:** Focusing on local metrics without considering critical path and resource allocation.
**Fix:** Analyze critical path first, then optimize bottlenecks that actually impact total execution time.

## Worked Examples

### Example 1: Cascade Failure with Remediation Choice
```
DAG State: research-node → analysis-node → summary-node
Failure: summary-node returns "Error: Cannot summarize incoherent analysis"

Step 1: Trace backward
- Check analysis-node output: "The data is unclear and contradictory..."
- Check research-node output: Mix of valid research + API error responses

Step 2: Classify failure
- Root cause: research-node partially failed (got some API errors)
- Symptom: analysis-node tried to work with corrupted data
- Downstream: summary-node failed on corrupted analysis

Step 3: Calculate confidence
- Research-node error pattern clear (API timeouts) → confidence 85%
- Remediation path clear (retry research with backoff) → confidence 90%
- Overall confidence: 85% > 80% threshold

Step 4: Auto-remediation
- Retry research-node with exponential backoff
- Re-execute analysis-node and summary-node
- Result: Full DAG completion without escalation
```

### Example 2: Aggregation Conflict Resolution
```
Scenario: Parallel code review branches (security-review + performance-review)

Security output: "Function validate_input() needs input sanitization"
Performance output: "Function validate_input() should be removed for speed"

Step 1: Detect conflict
- Similarity analysis: Both mention same function → 60% overlap
- Contradiction detection: "needs X" vs "remove" → conflict flagged

Step 2: Conflict resolution routing
- No confidence scores in outputs
- Conflicting recommendations on same code element
- Route: Escalate for human resolution with structured conflict summary

Step 3: Structure escalation
- Conflict: Function validate_input() handling
- Security perspective: Add input sanitization
- Performance perspective: Remove for speed optimization
- Human decision needed: Security vs performance tradeoff
```

## Quality Gates

- [ ] Root cause confidence score calculated and documented (must be ≥70% to proceed)
- [ ] All downstream failures traced to single root cause or marked as independent
- [ ] Remediation strategy selected with clear rationale (auto-fix vs escalate decision)
- [ ] Performance bottlenecks identified on critical path (if profiling requested)
- [ ] Parallel branch conflicts detected and resolution strategy applied
- [ ] Context dependencies mapped across all node waves
- [ ] Pattern learning insights extracted and formatted for upstream consumption
- [ ] Cost/performance metrics captured for optimization feedback loop
- [ ] Escalation package complete with actionable diagnosis (if human intervention needed)
- [ ] All auto-fix attempts logged with success/failure outcomes

## NOT-FOR Boundaries

**What this skill should NOT handle:**
- Initial DAG structure planning → Use `dag-planner` instead
- Real-time DAG execution → Use `dag-runtime` instead  
- Individual node output validation → Use `dag-quality` instead
- Business logic decisions within nodes → Let individual agents handle
- Cross-DAG orchestration → Use higher-level orchestrator
- User interface or presentation → Use presentation-focused skills

**Delegation rules:**
- For DAG restructuring needs → Pass insights to `dag-planner` with optimization recommendations
- For execution environment issues → Pass to `dag-runtime` with resource requirement updates
- For persistent quality issues → Pass to `dag-quality` with failure pattern analysis
- For cost/performance alerting → Pass to monitoring system with threshold breach data