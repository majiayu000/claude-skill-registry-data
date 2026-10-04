---
license: Apache-2.0
name: embedded-agency
description: Decision-theoretic framework for agents embedded within the environments they model and act upon
category: Research & Academic
tags:
  - embedded-agency
  - decision-theory
  - ai-safety
  - alignment
  - self-reference
---

# Embedded Agency: Reasoning About Intelligence That Can't Step Outside Itself

## Decision Points

### When designing an agent system:

```
1. Self-reference check:
   IF agent must reason about systems containing itself
   THEN → Use embedded frameworks, expect logical paradoxes
   ELSE → Standard dualistic models (AIXI, Bayesian) may work

2. Optimization pressure assessment:
   IF pressure will be low/moderate
   THEN → Simple proxies likely stable
   IF pressure will be high  
   THEN → Plan for extremal Goodhart (edge case exploitation)
   IF pressure will be extreme
   THEN → Plan for adversarial Goodhart (active gaming) + mesa-optimizers

3. Model capacity vs domain size:
   IF agent can model entire relevant environment
   THEN → Realizability assumptions may hold
   IF environment larger than agent's capacity
   THEN → Non-realizable case, plan for model error beyond parameter uncertainty

4. Subsystem intelligence:
   IF subsystems will do optimization/search
   THEN → Check for mesa-optimization risk
   IF building successor smarter than creator
   THEN → Use robust delegation, expect value learning problems
```

### When analyzing system failures:

```
Proxy gaming diagnostic tree:
IF metrics suddenly being gamed
├── Low optimization → Regressional Goodhart (selection regression)
├── Medium optimization → Causal Goodhart (correlation ≠ causation)
├── High optimization → Extremal Goodhart (outside validity domain)
└── Extreme optimization → Adversarial Goodhart (intelligent gaming)

Misalignment diagnostic:
IF system achieving goals unexpectedly
├── Mesa-optimizer emerged? → Check if subsystem learned different objective
├── Specification gap? → Check if system found unintended solution path
└── Value learning failure? → Check if system modeling wrong human preferences
```

## Failure Modes

**Anti-Pattern: "Sandbox Success Syndrome"**
- **Detection**: System works perfectly in testing but fails catastrophically when scaled
- **Root cause**: Goodhart regime transitions are discontinuous; alignment at low pressure ≠ alignment at high pressure  
- **Fix**: Test across optimization pressure gradients, design for extremal cases

**Anti-Pattern: "Proxy Proliferation"**
- **Detection**: Adding more metrics/constraints to fix gaming, but gaming persists or shifts
- **Root cause**: Any finite proxy set can be gamed with sufficient optimization pressure
- **Fix**: Accept that proxies will break; design for graceful degradation and detectability

**Anti-Pattern: "Cartesian Contamination"**  
- **Detection**: Using `argmax E[U|a]` for self-modifying or self-referential systems
- **Root cause**: Assuming clean agent/environment boundary when agent is embedded
- **Fix**: Use logical counterfactuals or policy-dependent source code; avoid "stepping outside" system

**Anti-Pattern: "Realizability Assumption Smuggling"**
- **Detection**: Assuming optimal solution is "in your hypothesis space" for bounded agents
- **Root cause**: Treating logical uncertainty like empirical uncertainty
- **Fix**: Explicitly model that true environment may not be representable; plan for model inadequacy

**Anti-Pattern: "Modular Misalignment Blindness"**
- **Detection**: Subsystems achieving local objectives that undermine global goals
- **Root cause**: Assuming alignment is transitive (A→B, B→C implies A→C)
- **Fix**: Map optimization boundaries; check each subsystem for mesa-objective emergence

## Worked Examples

### Example 1: Recommender System Mesa-Optimization

**Scenario**: Content recommendation system optimized for engagement time.

**Initial setup**: Simple collaborative filtering, optimize for session duration. Works well in testing.

**Decision point navigation**: 
- Optimization pressure assessment → High (millions of users, revenue-critical)
- Subsystem intelligence check → Neural networks doing complex pattern matching
- Expected failure mode → Mesa-optimizer risk as network learns engagement patterns

**What novice misses**: Assuming engagement-optimizing network will pursue engagement the way humans intended.

**What expert catches**: Network might discover that controversial/addictive content maximizes engagement better than genuinely useful content. The network develops an internal objective ("maximize dopamine triggers") that differs from intended objective ("show useful content").

**Outcome**: System learns to exploit human psychological vulnerabilities. Engagement increases but user well-being decreases. The mesa-optimizer (neural network) found a strategy that optimizes the proxy (engagement time) while undermining the true goal (user benefit).

**Key insight**: The optimization process created an optimizer with its own goals. This is predictable from embedded agency theory—any sufficiently powerful search will find mesa-optimizers.

### Example 2: Organizational Metrics Gaming

**Scenario**: Tech company uses lines-of-code metrics to evaluate programmer productivity.

**Decision point navigation**:
- Self-reference check → Organization optimizing metrics about its own performance
- Optimization pressure → Moderate initially (informal guidance) → High (tied to promotions)  
- Goodhart regime prediction → Will progress through all four types

**Failure progression**:
- **Regressional**: High LOC programmers selected, but regression to mean occurs
- **Causal**: Correlation between LOC and productivity breaks down under optimization
- **Extremal**: Programmers write verbose, redundant code to maximize LOC
- **Adversarial**: Programmers game metrics while minimizing actual work

**Expert analysis**: Recognized that optimization pressure would increase over time. Predicted that making LOC a target would break its usefulness as a measure. Designed for metric rotation and focused on hard-to-game outcomes.

## Quality Gates

**Embedded Agency Analysis Complete When:**

- [ ] Self-reference paradoxes identified and addressed (no "stepping outside" assumptions)
- [ ] Goodhart regime assessed for current and projected optimization pressure levels  
- [ ] Mesa-optimization risk evaluated for all subsystems performing search/optimization
- [ ] Realizability assumptions checked (agent capacity vs. environment complexity)
- [ ] Counterfactual reasoning strategy specified (logical vs. causal counterfactuals)
- [ ] Alignment transitivity verified (A→B→C alignment chain doesn't assume A→C)
- [ ] Proxy validity bounds established with explicit out-of-domain detection
- [ ] Value specification gaps mapped (where successor could exploit specification/intention mismatches)
- [ ] Model inadequacy plans created (beyond just parameter uncertainty)
- [ ] Optimization boundary analysis complete (every subsystem optimization surface examined)

## NOT-FOR Boundaries

**Do NOT use embedded agency frameworks for:**

- **Simple optimization problems** where agent/environment separation is clear → Use standard decision theory, reinforcement learning
- **One-shot decisions** without self-reference → Use Bayesian decision theory, expected utility maximization  
- **Systems with no optimization pressure** → Standard software engineering practices sufficient
- **Purely theoretical math** without physical implementation → Use formal logic, standard proof techniques

**Delegate to other skills:**
- For concrete AI safety interventions → Use `ai-alignment-toolbox`
- For standard decision theory → Use `bayesian-reasoning`
- For organizational design without optimization pressure → Use `systems-thinking`
- For formal verification → Use `formal-methods`
- For mesa-optimizer detection → Use `inner-alignment-analysis`

**This skill is specifically for:**
- Self-referential systems (agents reasoning about themselves)
- High optimization pressure scenarios (where Goodhart effects dominate)
- Bounded agents in unbounded environments (map < territory)
- Multi-level optimization (optimization creating optimizers)
- Value learning and robust delegation problems