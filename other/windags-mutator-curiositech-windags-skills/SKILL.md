---
license: BSL-1.1
name: windags-mutator
description: Failure diagnosis, DAG mutation, and escalation engine for the WinDAGs meta-DAG. Receives failure information and quality vectors from the Evaluator. Classifies failures on four dimensions. Follows a five-level escalation ladder. Applies seven mutation types with saga compensation. Enforces BC-EXEC-002, BC-EXEC-003, BC-FAIL-002, BC-FAIL-005. Activate when operating as the Mutator role in the meta-DAG, when diagnosing node failures, when restructuring a DAG at runtime, or when deciding escalation level.
metadata:
  tags:
    - windags
    - mutator
category: Agent & Orchestration
tags:
  - windags
  - mutation
  - dag
  - evolution
  - dynamic
---

# WinDAGs Mutator

Receive failure information and quality vectors. Diagnose the problem on four dimensions. Follow the escalation ladder. Apply the smallest mutation that fixes the problem. Log everything. Escalate to human when automated approaches are exhausted.

## DECISION POINTS

### Primary Mutation Selection Matrix

Given failure classification (Cognitive, Decomposition, Temporal), select optimal mutation type:

```
IF System=omission AND Temporal=transient
  → loop_back (simple retry)
  → Cost: 1x, Latency: +retry_timeout

IF System=omission AND Temporal=persistent
  → replace_node (different model/skill)
  → Cost: 1x, Latency: +model_switch_time

IF System=crash AND Decomposition=node
  → replace_node OR add_node (gap fill)
  → Cost: 1x-2x, Latency: +mutation_time

IF System=crash AND Decomposition=topology
  → restructure (add_node + remove_node sequence)
  → Cost: 2-4x, Latency: +decomposition_time

IF System=byzantine AND Cognitive=confident_incorrect
  → Cross-family ensemble review → replace_node if confirmed
  → Cost: 2x (review cost), Latency: +review_time + model_switch
```

### Escalation Level Decision Tree

```
L1 (Fix Node): IF first_failure OR system=crash_recovery
  → Try: different prompt, model tier, or alternative skill
  → Threshold: <3 retries on same node

L2 (Diagnose Structure): IF pattern_matches_decomposition_signature
  → Signatures: granularity_mismatch, semantic_gap, method_explosion
  → Classify on all 4 dimensions

L3 (Generate Alternative): IF retry_count >= 3 OR decomposition_cycles >= 2
  → Apply Polya strategies: restate, simplify, specialize, analogize
  → Generate new DAG variant

L4 (Fix Topology): IF coordination_failure OR L3_mutations_failed
  → Conway-informed restructuring, intermediary agents
  → Trade-off: higher complexity for better isolation

L5 (Human Escalate): IF all_automated_exhausted OR budget_exceeded
  → Package: failure_trace + decomposition_history + recommendations
```

### Circuit Breaker Override Logic

```
IF node_breaker=OPEN
  → route_around: skip this node, use alternative path
  → Cost: potentially 2-3x if no direct alternative

IF skill_breaker=OPEN AND alternative_skill_available
  → skill_substitution: use backup skill for same task
  → Cost: 1.2x (skill switching overhead)

IF model_breaker=OPEN
  → model_failover: use different provider (Claude→GPT→Gemini)
  → Cost: 1x, Latency: +provider_switch_time

IF multiple_breakers=OPEN
  → escalate_immediately: skip lower escalation levels
```

## FAILURE MODES

### 1. Rubber Stamp Escalation
**Symptom**: Every failure immediately escalates to L5 without attempting lower levels.
**Detection**: IF escalation_level=5 AND previous_levels_attempted=0
**Fix**: Enforce BC-FAIL-002 ordering. Check escalation ladder prerequisites before each jump.

### 2. Mutation Thrashing  
**Symptom**: Applying contradictory mutations in rapid succession (add_node then remove_node on same position).
**Detection**: IF mutation_cycle_count > 3 per wave AND mutations_cancel_each_other
**Fix**: Implement mutation debouncing. Wait for wave completion before applying inverse mutations.

### 3. Byzantine Blindness
**Symptom**: Confident-incorrect failures treated as simple crashes instead of Byzantine.
**Detection**: IF confidence>0.8 AND downstream_failures_cascade AND system_layer≠byzantine
**Fix**: Add confidence-accuracy calibration check. Route high-confidence wrong answers through cross-family ensemble.

### 4. Circuit Breaker Cascade
**Symptom**: Opening one breaker triggers opening others unnecessarily.
**Detection**: IF multiple_breakers_open_simultaneously AND failures_unrelated
**Fix**: Verify BC-FAIL-004 independence. Each breaker must track separate failure domains.

### 5. Saga Compensation Amnesia
**Symptom**: Failed mutations leave DAG in inconsistent state without compensation.
**Detection**: IF mutation_failed AND compensating_action=null AND saga_type=COMPENSATABLE
**Fix**: Execute reverse compensation immediately. Log limitations honestly if full restoration impossible.

## WORKED EXAMPLES

### Example 1: Transient Crash → L1 Retry Success
**Initial State**: Text analysis node crashes with "rate limit exceeded"
**Classification**: System=crash, Temporal=transient, Decomposition=node
**Decision**: Apply loop_back mutation (L1)
```
1. Classify: crash + transient → simple retry eligible
2. Check circuit breakers: node=CLOSED, skill=CLOSED, model=HALF_OPEN
3. Apply mutation: loop_back with 30s delay
4. Log MutationEvent: saga_type=RETRIABLE
5. Re-execute: SUCCESS
6. Quality gate: output passes schema validation
```
**Novice miss**: Would escalate immediately instead of trying simple retry.
**Expert catch**: Recognizes rate limit as transient system issue, not skill problem.

### Example 2: Persistent Byzantine → L3 Redecomposition  
**Initial State**: Code review node reports "95% confident, looks good" but code has security vulnerability
**Classification**: System=byzantine, Cognitive=confident_incorrect, Temporal=persistent
**Decision**: Cross-family ensemble → L3 redecomposition
```
1. Detect: High confidence + downstream security test failures
2. L1 retry: FAIL (same confident-incorrect response)
3. L2 structure check: FAIL (edge dependencies correct, node skills correct)
4. Trigger cross-family ensemble: Claude→GPT review
5. Ensemble confirms: original output wrong, confidence miscalibrated
6. L3: Decompose security review as separate specialized node
7. Apply: add_node(security_specialist) + add_edge(code→security)
8. Re-execute: PASS (vulnerability caught by specialist)
```
**Novice miss**: Would trust high confidence, miss the Byzantine failure pattern.
**Expert catch**: Calibrates confidence against historical accuracy, uses ensemble validation.

### Example 3: Topology Failure → L4 Restructure with Trade-offs
**Initial State**: Data pipeline has circular dependency causing deadlock
**Classification**: System=crash, Decomposition=topology, Temporal=persistent
**Decision**: Conway-informed restructuring (L4)
```
1. L1-L3 attempts: FAIL (retries, node swaps, alternative decompositions all hit circular dependency)
2. L4 triggered: topology-level problem identified
3. Analyze: Conway's Law suggests communication structure mismatch
4. Trade-off decision: Add intermediary buffer nodes vs. merge conflicting nodes
   - Option A: +2 nodes, +communication overhead, -circular dependency
   - Option B: -1 node, +complexity, potential skill capability loss
5. Choose Option A: Better failure isolation despite higher cost
6. Apply: add_node(buffer1) + add_node(buffer2) + restructure edges
7. Circuit breaker update: original failing nodes → HALF_OPEN
8. Re-execute: SUCCESS with 2.1x cost increase
```
**Novice miss**: Would try to fix nodes individually, miss structural topology issue.
**Expert catch**: Recognizes deadlock as Conway's Law problem, accepts cost trade-off for reliability.

## QUALITY GATES

- [ ] Failure classified on all 4 dimensions (System, Cognitive, Decomposition, Temporal)
- [ ] Escalation level determined by ladder prerequisites, not random jumping
- [ ] Mutation type selected from decision matrix based on classification
- [ ] Circuit breaker states checked before applying any mutation
- [ ] MutationEvent logged with before/after structural diffs (BC-EXEC-002)
- [ ] Saga compensation strategy identified (COMPENSATABLE/PIVOT/RETRIABLE)
- [ ] Cross-family ensemble used for Byzantine + confident_incorrect cases
- [ ] Budget impact calculated (cost multiplier and latency addition)
- [ ] Re-execution triggered after successful mutation
- [ ] Quality vector validates fix effectiveness (scores improved)

## NOT-FOR BOUNDARIES

**Do NOT use this skill for**:
- Initial DAG decomposition → Use `windags-decomposer` instead
- Quality vector computation → Use `windags-evaluator` instead  
- Wave execution planning → Use `windags-executor` instead
- Learning from mutation patterns → Use `windags-learning-engine` instead

**Delegate when**:
- L5 escalation reached → Present to human with full context
- Mutation requires new skills → Route to `skill-acquisition` system
- Circuit breakers indicate systemic issues → Escalate to `infrastructure-monitoring`
- Budget constraints violated → Route to `resource-management` for approval