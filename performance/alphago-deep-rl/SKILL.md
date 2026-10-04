---
license: Apache-2.0
name: alphago-deep-rl
description: Strategic patterns for solving intractable problems through cascading approximation, self-improvement, and heterogeneous evaluation from DeepMind's AlphaGo system
category: Research & Academic
tags:
  - reinforcement-learning
  - deep-learning
  - game-playing
  - monte-carlo-tree-search
  - neural-networks
---

# AlphaGo Architecture Skill

## Decision Points

### When to Use Single vs. Cascaded Evaluators

```
Problem characteristics:
├── Search space tractable (b^d < 10^9)
│   └── Use single best evaluator → standard optimization
└── Search space intractable (b^d > 10^12)
    ├── Uniform evaluation budget available
    │   └── Use cascading approximation:
    │       1. Fast pruning (policy network) → narrow beam
    │       2. Medium evaluation (value network) → estimate quality
    │       3. Cheap exploration (rollouts) → breadth coverage
    └── Non-uniform evaluation budget
        └── Adaptive allocation:
            ├── Critical positions → expensive evaluation
            └── Routine positions → cheap heuristics
```

### Accuracy vs. Latency Requirements Decision Tree

```
System requirements:
├── Latency critical (<1ms response)
│   ├── Accuracy tolerance high (>10% error acceptable)
│   │   └── Fast rollouts only (2µs/evaluation)
│   └── Accuracy tolerance low (<5% error)
│       └── Cached policy network + heuristic fallback
├── Latency moderate (1-100ms response)
│   ├── High accuracy needed
│   │   └── Value network (3ms) + policy network guidance
│   └── Balanced accuracy/speed
│       └── Mixed evaluation: λ=0.5 value + rollouts
└── Latency tolerant (>100ms)
    └── Full cascade: policy → value → rollouts with MCTS
```

### Error Mode Diversity Assessment

```
When choosing multiple evaluators:
├── All evaluators have similar failure modes
│   └── Use single best evaluator (no diversity benefit)
├── Evaluators have complementary errors
│   ├── Fast/noisy + slow/accurate pairing
│   │   └── Mix at λ=0.3-0.7 (bias toward accurate)
│   ├── Conservative + exploratory pairing
│   │   └── Mix at λ=0.5 (equal weighting)
│   └── Learned + handcrafted pairing
│       └── Dynamic mixing based on confidence scores
└── Unknown error correlation
    └── Empirical testing: measure performance on holdout set
```

## Failure Modes

### Schema Bloat (Detection: >5 approximation layers)
**Symptom**: Adding more approximation layers but seeing diminishing returns
**Root cause**: Each layer adds overhead without proportional accuracy gain
**Fix**: Profile computational cost vs. accuracy improvement; remove layers with poor ROI
**Detection rule**: If adding layer N improves accuracy <5% but increases latency >20%, you have schema bloat

### Synchronous Coupling (Detection: Fast components waiting idle)
**Symptom**: CPU utilization drops while waiting for GPU evaluation
**Root cause**: Tight coupling between fast search and slow neural network evaluation
**Fix**: Implement asynchronous queuing with stale value tolerance
**Detection rule**: If fast components (search, rollouts) have >50% idle time, you have synchronous coupling

### Proxy Metric Fixation (Detection: Metric improving but performance degrading)
**Symptom**: Move prediction accuracy improves but win rate decreases
**Root cause**: Optimizing for human imitation instead of objective success
**Fix**: Switch from supervised learning to reinforcement learning with true objective
**Detection rule**: If proxy metric and outcome metric trend in opposite directions >10 evaluations, you have proxy fixation

### Single Evaluator Fallacy (Detection: Rejecting "worse" individual components)
**Symptom**: Discarding rollouts because value network has higher individual accuracy
**Root cause**: Assuming best individual component makes best system component
**Fix**: Test mixture performance empirically; diversity often beats individual quality
**Detection rule**: If you're selecting components by individual performance without testing combinations, you have single evaluator fallacy

### Uniform Budget Allocation (Detection: Same computation for all decisions)
**Symptom**: Spending equal evaluation time on obvious moves and critical positions
**Root cause**: Not adapting computational budget to decision importance
**Fix**: Implement adaptive allocation based on position uncertainty and outcome sensitivity
**Detection rule**: If evaluation time variance across positions <20% of mean, you have uniform allocation

## Worked Examples

### Implementing Cascading Approximation for Code Review

**Scenario**: Design AI system for reviewing pull requests with 50-500 changed lines, need <10s response time, must catch 95% of bugs.

**Step 1: Analyze computational constraints**
- Static analysis: 10ms per file
- ML bug detector: 2s per file  
- Deep semantic analysis: 30s per file
- Available budget: 10s total

**Step 2: Apply cascading decision tree**
Following "search space intractable" path since exhaustive analysis exceeds budget:
1. **Fast pruning layer** (static analysis): Eliminate files with no complexity changes
2. **Medium evaluation layer** (ML detector): Score remaining files for bug likelihood  
3. **Expensive analysis layer** (semantic): Deep dive on highest-scoring files only

**Step 3: Budget allocation strategy**
- Reserve 2s for ML evaluation of all remaining files
- Allocate remaining 8s to semantic analysis based on ML scores
- Files scoring >0.8: get 4s each (max 2 files)
- Files scoring 0.5-0.8: get 2s each  
- Files scoring <0.5: get ML score only

**Step 4: Mixture evaluation implementation**
Instead of using "best" evaluator (semantic analysis), mix ML + semantic scores:
- ML detector: fast, good at pattern matching, misses novel bugs
- Semantic analysis: slow, catches complex logic errors, high false positive rate
- Mixture at λ=0.6: `final_score = 0.6 * semantic + 0.4 * ml`

**Novice approach**: Run semantic analysis on everything → timeout after first few files
**Expert insight**: The cascade allows spending expensive compute only where it matters most, while ensuring every file gets some evaluation

## Quality Gates

[ ] **N evaluators tested**: Minimum 3 evaluators with different speed/accuracy profiles implemented and benchmarked
[ ] **Error correlation measured**: Pairwise correlation matrix computed showing evaluators have <0.7 correlation on test set  
[ ] **Mixture vs. single evaluated**: Empirical comparison showing mixture outperforms best individual component by >5%
[ ] **Latency requirements met**: 95th percentile response time under specified threshold with full cascade
[ ] **Accuracy requirements met**: Error rate on holdout set meets specified threshold (e.g., <5% false negative rate)
[ ] **Budget allocation profiled**: Computational cost breakdown shows budget distributed according to decision importance
[ ] **Failure mode testing**: System tested under adversarial conditions (distribution shift, resource constraints, edge cases)
[ ] **Asynchronous coordination verified**: Fast components maintain >80% utilization even when slow components are saturated
[ ] **Scalability validated**: Performance degrades gracefully when increasing load 10x beyond nominal capacity
[ ] **Monitoring instrumentation**: Metrics track proxy vs. outcome alignment, component utilization, and cascade effectiveness

## NOT-FOR Boundaries

**Do NOT use this skill for**:
- Simple optimization problems with tractable search spaces → use **standard-optimization** instead
- Single-model training or tuning → use **deep-learning-training** instead  
- Real-time systems requiring <1ms latency → use **low-latency-systems** instead
- Problems where one evaluator is clearly superior and others add no value → use **single-model-deployment** instead
- Sequential decision processes without search tree structure → use **reinforcement-learning-fundamentals** instead

**Delegate to other skills when**:
- Need to implement specific neural network architectures → **deep-learning-architectures**
- Designing distributed systems infrastructure → **distributed-systems-design** 
- Optimizing individual component performance → **performance-optimization**
- Handling training data collection and labeling → **data-engineering**
- Implementing specific search algorithms → **search-algorithms**

**This skill focuses specifically on**: Architectural patterns for coordinating multiple imperfect evaluators under computational constraints, not the implementation details of individual components.