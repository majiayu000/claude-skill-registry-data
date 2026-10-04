---
license: BSL-1.1
name: windags-evaluator
description: Two-stage review engine with four-layer quality model for the WinDAGs meta-DAG. Receives completed node outputs and produces ReviewResult containing QualityVector. Stage 1 (Haiku) checks Floor + Wall on every node. Stage 2 (Sonnet) runs Ceiling evaluation conditionally using economic escalation formula. Enforces BC-EVAL-001 through BC-EVAL-006. Activate when operating as the Evaluator role in the meta-DAG, when reviewing node outputs, when computing quality vectors, or when deciding Stage 2 escalation.
metadata:
  tags:
    - windags
    - evaluator
category: Agent & Orchestration
tags:
  - evaluation
  - windags
  - quality
  - assessment
  - meta
---

# WinDAGs Evaluator

Receive completed node outputs. Produce a `ReviewResult` containing a `QualityVector`. Enforce the four-layer quality model as a runtime protocol gate. Run Stage 1 on every node. Escalate to Stage 2 only when the economic formula justifies it.

## DECISION POINTS

### Main Evaluation Flow
```
1. Node output received
   ├─ Floor check passes? 
   │  ├─ YES → Continue to Wall check
   │  └─ NO → Return floor_failed ReviewResult (skip Wall, Ceiling, Envelope)
   │
   ├─ Wall check passes?
   │  ├─ YES → Evaluate Stage 2 escalation
   │  └─ NO → Skip Ceiling, compute Envelope only
   │
   └─ Stage 2 escalation needed?
      ├─ YES (feeds human gate) → Run Stage 2 Ceiling
      ├─ YES (final deliverable) → Run Stage 2 Ceiling  
      ├─ YES (irreversible) → Run Stage 2 Ceiling
      ├─ YES (P(fail) * waste > cost) → Run Stage 2 Ceiling
      └─ NO → Stage 1 only, compute Envelope
```

### Partial Wall Grade Resolution
```
Wall grade is 0.4 (partial pass):
├─ Grade >= 0.6? → Treat as PASS, continue to Stage 2 decision
├─ Grade < 0.3? → Treat as FAIL, skip Ceiling
└─ Grade 0.3-0.6? → Check downstream criticality:
   ├─ Node feeds critical path? → Treat as FAIL
   └─ Node feeds non-critical? → Treat as PASS with warning
```

### Conflicting Evaluator Sources
```
Peer=0.8, Downstream=0.3 (high disagreement):
├─ Difference > 0.4? → Flag for human review
├─ Downstream consumer is critical? → Weight Downstream 0.5, Peer 0.2
├─ Peer has domain expertise? → Weight Peer 0.4, Downstream 0.25
├─ Historical Peer reliability < 0.7? → Trust Downstream more
└─ Default → Use standard weights: Peer 0.25, Downstream 0.35
```

### Economic Escalation Formula
```
Cost-benefit calculation:
├─ downstreamWaste = sum(dependent_node_costs) * cascade_probability
├─ failureProbability = skill_failure_rate * stage_factor * breaker_penalty
├─ expectedWaste = failureProbability * downstreamWaste
└─ escalate = expectedWaste > stage2_cost
```

## FAILURE MODES

### Missing Envelope Syndrome
**Symptoms**: ReviewResult returned without envelope field populated
**Diagnosis**: Floor check short-circuited the evaluation flow improperly
**Fix**: Envelope computation is mandatory for ALL nodes regardless of Floor result; run envelope calculation before returning any ReviewResult

### Rubber Stamp Review  
**Symptoms**: All evaluations scoring 0.9+ with minimal variation across different node types
**Diagnosis**: Evaluator not applying layer-specific criteria; treating all outputs as equally good
**Fix**: Implement per-layer scoring rubrics; require justification for scores above 0.8; cross-check with historical distributions

### Escalation Cascade Explosion
**Symptoms**: >60% of nodes escalating to Stage 2 when historical rate should be 15-20%
**Diagnosis**: Economic formula over-weighting failure probability or downstream costs
**Fix**: Recalibrate failure probability floor to 0.01; cap downstream waste calculation at 5x node cost; audit cascade_probability multiplier

### Bias Amplification Loop
**Symptoms**: Position-swapped evaluations showing >0.3 variance consistently  
**Diagnosis**: Neural evaluators not properly applying bias mitigation techniques
**Fix**: Enforce position swapping on ALL pairwise comparisons; apply length normalization; flag and retry when position bias detected

### Quality Vector Collapse
**Symptoms**: Multi-dimensional quality getting converted to single scalar scores in downstream processing
**Diagnosis**: Consuming systems incorrectly aggregating QualityVector dimensions
**Fix**: Audit all QualityVector consumers; enforce per-dimension access patterns; remove any automatic scalar conversion utilities

## WORKED EXAMPLES

### Example 1: Floor Failure Case
**Scenario**: Code generation node produces syntactically invalid Python
```
Input: "Generate a Flask route handler"
Output: "def handle_route(
    return jsonify({'status': 'ok')"  // Missing closing paren, incomplete

Stage 1 Floor Check:
1. Parse against Python AST → FAIL (SyntaxError)
2. Schema validation → FAIL (incomplete function)
3. Contract check → FAIL (not valid Python)

Decision: Floor failed → Skip Wall, Ceiling, Envelope
Action: Return ReviewResult{stage1: {passed: false, floor: {passed: false, violations: ["SyntaxError", "IncompleteFunction"]}}, envelope: null}
```

**Expert catches**: Floor failure should immediately terminate evaluation - don't waste compute on Wall/Ceiling for fundamentally broken output
**Novice misses**: Trying to evaluate "style" or "approach" of syntactically invalid code

### Example 2: Escalation Decision with Cost/Waste Trade-off
**Scenario**: API documentation generation for internal service
```
Node: doc-generator (skill success_rate: 0.85, novice stage)
Downstream: 3 dependent nodes worth $0.12 total cost
Stage 2 review cost: $0.045

Calculation:
- failureProbability = (1 - 0.85) * 1.5 * 1.0 = 0.225
- downstreamWaste = $0.12 * 0.6 = $0.072 
- expectedWaste = 0.225 * $0.072 = $0.016
- escalate? $0.016 < $0.045 → NO

Decision: Stage 1 only
Reasoning: Low downstream impact, novice penalty not enough to justify deep review
```

**Expert catches**: Economic formula must account for cascade probability (0.6) not just raw downstream costs
**Novice misses**: Forgetting to apply stage factor for novice skills, leading to under-escalation

### Example 3: Conflicting Peer vs Downstream Signals
**Scenario**: SQL query optimization node evaluated by peer optimizer and downstream execution engine
```
Peer evaluation: 0.85 ("Elegant use of window functions, good indexing strategy")
Downstream evaluation: 0.35 ("Query times out on large datasets, missing LIMIT clause")

Resolution Decision Tree:
1. Difference = |0.85 - 0.35| = 0.5 > 0.4 → Flag for human review
2. Downstream is execution engine (critical for performance) → Weight downstream higher
3. Check peer historical reliability: 0.82 (good)
4. Final weights: Peer 0.15, Downstream 0.45

Composite Score: (0.15 * 0.85) + (0.45 * 0.35) = 0.285
Action: Mark as failing Wall check due to performance issues despite elegant structure
```

**Expert catches**: Performance trumps elegance; downstream execution failures are more costly than aesthetic suboptimality
**Novice misses**: Over-weighting peer review because it "sounds more technical"; ignoring real-world execution constraints

## QUALITY GATES

- [ ] ReviewResult contains valid QualityVector with all required dimensions populated
- [ ] Envelope computed for every node regardless of Floor/Wall results  
- [ ] Stage 2 escalation decision logged with economic calculation breakdown
- [ ] Position swapping applied to all neural evaluations with bias detection
- [ ] Self-evaluation outcome excluded from quality scoring (process self-check retained at 0.15 weight)
- [ ] Near-miss events detected and logged for quality margins < 10%, timeout margins < 20%
- [ ] Cognitive telemetry recorded for all failures, mutations, and Stage 2 escalations
- [ ] Multiple evaluator sources properly weighted according to trust levels
- [ ] Floor failure short-circuits Wall/Ceiling evaluation correctly
- [ ] Quality vectors stored per-dimension without automatic scalar collapse

## NOT-FOR BOUNDARIES

**Do not use windags-evaluator for:**
- Real-time streaming evaluation (use stream-evaluator instead)
- Evaluating human-generated content (use human-content-reviewer instead)  
- Binary pass/fail decisions without quality scoring (use simple-validator instead)
- Evaluating non-DAG workflow outputs (use workflow-evaluator instead)
- Cross-domain skill comparison without context (use skill-comparator instead)

**Delegate to other skills when:**
- Node output requires domain-specific validation → Use domain-validator-{domain}
- Evaluation needs human-in-the-loop verification → Use human-gate-evaluator  
- Quality assessment needs historical trend analysis → Use quality-trend-analyzer
- Evaluation requires cross-model consensus → Use ensemble-evaluator
- Assessment needs explanation generation → Use explainable-evaluator