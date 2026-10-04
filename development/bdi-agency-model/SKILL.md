---
license: Apache-2.0
name: bdi-agency-model
description: BDI (Beliefs-Desires-Intentions) agency framework for designing autonomous agents with mental state architectures
category: Research & Academic
tags:
  - bdi
  - agents
  - agency
  - mental-states
  - architecture
---

# SKILL.md: The Belief-Desire-Intention Model of Agency

license: Apache-2.0
## Metadata
- **Skill Name**: bdi-agency-model
- **Source**: "The Belief-Desire-Intention Model of Agency" (Georgeff, Pell, Pollack, Tambe, Wooldridge)
- **Domain**: Intelligent systems architecture, multi-agent systems, adaptive planning
- **Activation Triggers**: 
  - Designing autonomous agents or adaptive systems
  - Debugging planning/replanning behavior
  - Evaluating when systems should reconsider decisions
  - Architecting systems for dynamic environments
  - Coordinating multiple intelligent agents
  - Questions about goal vs. task representation

## When to Use This Skill

Load this skill when facing:

- **Architecture decisions**: How to structure an intelligent agent's internal representation and control flow
- **Commitment problems**: System thrashing between plans or stubbornly pursuing obsolete goals
- **Dynamic environment design**: Systems must adapt to changing conditions without complete replanning
- **Resource constraints**: Limited computation time for decision-making in real-time systems
- **Recovery challenges**: Systems can't automatically recover when plans fail
- **Multi-agent coordination**: Multiple agents need to form and maintain joint commitments
- **Goal vs. implementation gap**: Distinguishing what systems should achieve from how they achieve it
- **Learning integration**: Adding adaptive capabilities to planning systems

This skill applies beyond robotics/AI agents—it's relevant for any system that must make decisions over time with partial information, including business process systems, game AI, automated trading, and organizational design.

## Core Mental Models

### 1. The Three Components Are Computationally Necessary, Not Optional

**Beliefs** (informational state), **Desires** (motivational state), and **Intentions** (deliberative state) aren't philosophical conveniences—they're architectural necessities for resource-bounded agents in dynamic environments.

- **Beliefs**: What you currently know about the world (may be wrong, incomplete)
- **Desires**: All goals/outcomes you'd like to achieve (may be conflicting, unachievable)
- **Intentions**: Subset of desires you've *committed* to pursuing (chosen, planned, actionable)

**Why separate?** Because conflating them creates impossible computational requirements:
- Beliefs + Desires merged → must constantly recompute feasibility of every desire
- Desires + Intentions merged → no distinction between "would be nice" and "actively pursuing"
- Beliefs + Intentions merged → when beliefs change, must immediately replan everything

The separation enables local updates and selective reasoning.

### 2. The Commitment-Reconsideration Balance

**The core tension**: 
- Replan too often (classical decision theory) → waste resources thrashing, never execute
- Replan too rarely (conventional software) → miss opportunities, pursue obsolete goals

**The empirical finding** (bold vs. cautious agents):
- Static environments → bold agents win (commit strongly, rarely reconsider)
- Highly dynamic environments → cautious agents win (reconsider frequently)
- Real environments → need meta-level strategy for *when* to reconsider

**Rational commitment** = maintaining intentions until there's sufficient reason to reconsider, where "sufficient" depends on environment dynamics and computational costs.

### 3. Task-Orientation vs. Goal-Orientation

**Task-oriented systems**: Execute procedures without maintaining why
- "Run script X" → executes blindly
- Cannot automatically recover from failures
- Cannot exploit opportunistic improvements
- Cannot explain behavior

**Goal-oriented systems**: Maintain explicit desired states and plans to achieve them
- "Achieve state Y via plan Z" → knows current beliefs, goal, and chosen approach
- Can detect when goals already achieved (stop early)
- Can recognize when goals become impossible (abandon gracefully)
- Can find alternative plans when current fails
- Can explain actions in terms of goals

**The gap**: Most software is task-oriented. BDI provides the minimal architecture for goal-orientation.

### 4. Intentions as Computational Filters

Intentions don't just represent commitments—they actively **constrain future reasoning**:

- **Filter practical reasoning**: Only consider options compatible with existing intentions
- **Reduce option space**: Avoid reconsidering entire action space at each step
- **Enable predictability**: Others can predict your behavior (crucial for coordination)
- **Structure persistence**: Provide default continuity unless reasons to change

This is **not** bounded rationality or satisficing—it's a rational strategy for resource-bounded agents. The alternative (consider all options always) is computationally intractable.

### 5. Convergent Evolution Signals Universal Principles

BDI (philosophy/logic tradition) and Soar (cognitive psychology tradition) independently converged on isomorphic architectures:

| BDI Component | Soar Component | Computational Role |
|---------------|----------------|-------------------|
| Beliefs | States | World representation |
| Desires | Subgoals | Motivational targets |
| Intentions | Operators | Chosen actions |
| Plans | Problem spaces | Action sequences |

**Implication**: These components aren't arbitrary design choices but discovered necessities—like multiple cultures independently inventing the wheel. Any system facing similar constraints (bounded resources, partial information, dynamic environments, real-time action) will need similar structures.

## Decision Frameworks

### When to Reconsider Intentions

**IF** environment is highly static **THEN** bias toward bold commitment (rarely reconsider)
**IF** environment is highly dynamic **THEN** bias toward cautious reconsideration (frequently reevaluate)

**IF** computational resources abundant **THEN** can afford more frequent reconsideration
**IF** computational resources scarce **THEN** must commit more strongly to amortize planning cost

**IF** action execution is expensive **THEN** reconsider before acting
**IF** deliberation is expensive **THEN** commit and act quickly

**IF** new information directly contradicts intention's preconditions **THEN** reconsider immediately
**IF** new information merely opens alternatives **THEN** reconsider only if significantly better

### When to Separate Beliefs, Desires, and Intentions

**IF** system must act in real-time **THEN** needs intentions (can't replan from desires every cycle)
**IF** system faces conflicting goals **THEN** needs desire/intention distinction (desires can conflict, intentions cannot)
**IF** system must coordinate with others **THEN** needs explicit intentions (for commitment communication)
**IF** system must explain behavior **THEN** needs all three (explain actions via intentions, intentions via desires, desires via beliefs)
**IF** system must adapt to failures **THEN** needs goal-oriented representation (to find alternative means)

### Architecture Selection

**IF** environment is static AND goals are clear AND plans rarely fail **THEN** task-oriented architecture may suffice
**IF** environment changes OR goals conflict OR plans frequently fail **THEN** need BDI-style architecture
**IF** multiple agents must coordinate **THEN** need explicit commitment mechanisms (load multi-agent reference)
**IF** system must learn from experience **THEN** need BDI + learning extensions (load learning reference)

## Reference Table

| Reference File | Load When... | Key Content |
|----------------|--------------|-------------|
| `why-beliefs-desires-intentions-exist.md` | Justifying architectural decisions; explaining why three components are necessary | Detailed computational argument for BDI separation; what each component solves; costs of conflation |
| `rational-commitment-and-reconsideration.md` | Designing reconsideration strategies; debugging thrashing or stubbornness | Kinny-Georgeff experiments; bold vs. cautious agents; meta-level control; empirical results |
| `task-vs-goal-orientation.md` | Comparing architecture approaches; explaining need for goal representation | Deep dive on task/goal distinction; recovery capabilities; opportunistic replanning; explainability |
| `soar-bdi-convergent-evolution.md` | Validating design choices; comparing with cognitive architectures | Soar-BDI mapping; convergent evolution argument; universal principles; cross-tradition insights |
| `multi-agent-commitment-and-coordination.md` | Designing multi-agent systems; coordination protocols | Joint intentions; social commitments; team reasoning; coordination mechanisms; distributed BDI |
| `learning-the-missing-piece.md` | Adding adaptation; integrating ML with planning | BDI limitations; learning integration strategies; experience-based improvement; open challenges |

## Anti-Patterns

### 1. **Replanning Everything Always**
**Symptom**: System constantly reconsiders all options, thrashes between plans, never completes actions
**Root cause**: Treating every belief update as requiring complete replanning (classical decision theory mistake)
**BDI insight**: Rational commitment means maintaining intentions despite minor belief changes

### 2. **Blind Task Execution**
**Symptom**: System continues executing plan after goal achieved or becomes impossible
**Root cause**: Task-oriented architecture without goal representation
**BDI insight**: Maintain explicit relationship between intentions, plans, and desires to enable goal-aware execution

### 3. **Desire-Intention Conflation**
**Symptom**: System tries to pursue conflicting goals simultaneously, resources spread too thin
**Root cause**: Not distinguishing between "would like to achieve" and "committed to pursuing"
**BDI insight**: Desires can conflict; intentions cannot (must resolve conflicts during deliberation)

### 4. **Intention Without Commitment**
**Symptom**: System abandons plans at first difficulty; erratic, unpredictable behavior
**Root cause**: Treating intentions as weak preferences rather than commitments
**BDI insight**: Intentions constrain future reasoning—they're not just goals but *committed* goals

### 5. **Static Plans in Dynamic Environments**
**Symptom**: System fails when environment changes; no recovery from failures
**Root cause**: Conventional software approach (plan = fixed procedure)
**BDI insight**: Plans must be monitored against goals; reconsideration needed when environment dynamics high

### 6. **No Meta-Level Control**
**Symptom**: Fixed reconsideration strategy fails across different environment dynamics
**Root cause**: Not adapting commitment strategy to environment characteristics
**BDI insight**: Need meta-level reasoning about *when* to reconsider (the central open problem)

### 7. **Single-Agent BDI in Multi-Agent Settings**
**Symptom**: Coordination failures; agents undermine each other's plans
**Root cause**: Using individual BDI without social commitment mechanisms
**BDI insight**: Multi-agent requires joint intentions and commitment communication protocols

## Shibboleths: How to Recognize Deep Understanding

### Surface-Level (Just Read Summary)
- "BDI means beliefs, desires, and intentions"
- "It's based on Bratman's philosophy"
- "You need to balance commitment and flexibility"

### Intermediate (Understood Concepts)
- Can explain *why* three components are computationally necessary, not just *what* they are
- Recognizes commitment-reconsideration as empirical trade-off with environment-dependent optima
- Distinguishes task-oriented vs. goal-oriented architectures by recovery capabilities

### Deep (Internalized)
- **Sees BDI as resource management strategy**: Recognizes that intentions exist to constrain reasoning space, not just represent commitments
- **Treats "when to reconsider" as the central problem**: Understands bold/cautious experiments show no universal answer—context determines strategy
- **Recognizes convergent evolution**: Points to Soar-BDI mapping as evidence these are discovered necessities, not designed choices
- **Distinguishes individual vs. social commitments**: Knows single-agent BDI is insufficient for multi-agent coordination
- **Identifies learning integration as fundamental gap**: Acknowledges BDI provides structure but not adaptation mechanisms

### Master (Can Apply Cross-Domain)
- Recognizes BDI patterns in non-AI systems (business processes, organizational design, personal productivity)
- Can diagnose "commitment pathologies" (thrashing, stubbornness) and prescribe architectural remedies
- Designs meta-level control strategies tuned to specific environment dynamics
- Integrates learning mechanisms while preserving commitment semantics
- Uses task/goal distinction to evaluate system explainability and recovery capabilities

**Key diagnostic question**: "Why can't you just merge desires and intentions?"
- **Shallow answer**: "Because you need to distinguish what you want from what you're doing"
- **Deep answer**: "Because desires can be conflicting and unchosen—deliberation is the computational process of resolving conflicts and resource constraints to select a feasible subset as intentions. Merging them eliminates the structure that makes deliberation tractable and commitments meaningful."