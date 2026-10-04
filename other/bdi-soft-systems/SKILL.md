---
license: Apache-2.0
name: bdi-soft-systems
description: Integration of BDI agent architecture with soft systems methodology for complex organizational problem-solving
category: Research & Academic
tags:
  - bdi
  - soft-systems
  - methodology
  - agents
  - design
---

# SKILL: Modeling Organizations as BDI Agents

## When to Use This Skill

Load this skill when facing:
- **The formalization gap**: You have rich qualitative data about organizational behavior but need predictive models
- **The black box problem**: Existing process models describe WHAT happens but not HOW decisions get made internally
- **Multi-agent coordination puzzles**: Agents must work together despite different perceptions, goals, and expertise levels
- **Implementation resistance**: Technical systems fail because they don't match how organizations actually think and decide

## Decision Points

### 1. Choosing Abstraction Level for Modeling

```
IF need to predict specific decisions → Micro-level (individual agents)
├─ Map each person/department as separate BDI agent
├─ Model conflicts and negotiations explicitly
└─ Use when: budget allocation, hiring decisions, project prioritization

IF need to understand process patterns → Meso-level (process as agent)
├─ Model entire workflow as single distributed agent
├─ Focus on recurring behaviors and bottlenecks
└─ Use when: IT development cycles, approval chains, quality control

IF need to explain culture/identity → Macro-level (organization as agent)
├─ Model whole organization as one meta-cognitive system
├─ Focus on identity, values, and strategic direction
└─ Use when: M&A integration, culture change, strategic pivots
```

### 2. Designing Agent Commitment Levels

```
Environment Stability × Information Cost Decision Matrix:

Stable Environment:
├─ Cheap Information → Moderate intentions (monthly review cycles)
└─ Expensive Information → Strong intentions (annual planning cycles)

Volatile Environment:
├─ Cheap Information → Weak intentions (daily standups, rapid iteration)
└─ Expensive Information → ESCALATE: Need higher-level coordination

IF coordination cost > decision complexity → Synchronize intention formation
IF agents have conflicting perceptual filters → Design accommodations, not consensus
```

### 3. Handling Agent Disagreements

```
Type of Disagreement → Diagnostic Check → Action

Factual Disagreement:
├─ Check: Different roles/expertise/positions?
├─ If YES → Map perceptual filters, design information accommodations
└─ If NO → Look for hidden goal conflicts

Goal Disagreement:
├─ Check: Has genuine negotiation occurred?
├─ If NO → Facilitate discourse process for desire formation
└─ If YES → Design accommodation mechanisms for persistent differences

Action Despite Disagreement:
├─ Check: Are there implicit accommodations?
├─ Surface and formalize working agreements
└─ Don't force consensus—optimize for coordination
```

## Failure Modes

### 1. **Consensus Paralysis**
**Symptoms**: Endless meetings, recurring discussions, "we need alignment" language, delayed decisions waiting for agreement
**Detection Rule**: If same decision requires 3+ consensus-building sessions, you're in consensus paralysis
**Fix**: Switch to accommodation design—create working agreements that allow action despite disagreement

### 2. **Intention Drift** 
**Symptoms**: Agents constantly reconsider commitments, plans change weekly, "keeping options open" becomes paralysis
**Detection Rule**: If agents spend >30% of cycles reconsidering prior commitments, intentions are too weak
**Fix**: Strengthen intention commitment thresholds; only reconsider on explicit trigger events

### 3. **Perceptual Projection**
**Symptoms**: Assuming others have access to same information, designing systems around "shared situational awareness"
**Detection Rule**: If coordination failures blamed on "communication issues" without role/expertise analysis
**Fix**: Map perceptual filters by role; design for subjective beliefs, not objective world state

### 4. **Goal Optimization Fallacy**
**Symptoms**: Treating organizational objectives as fixed inputs to optimize, missing how goals emerge from discourse
**Detection Rule**: If designing for given objectives without modeling goal formation process
**Fix**: Model the discourse mechanisms that create desires; include power dynamics and negotiation processes

### 5. **System-Organization Conflation**
**Symptoms**: Designing IT/AI systems as if they constitute organizational cognition, expecting radical behavior change from system deployment
**Detection Rule**: If system failure would halt organizational function entirely (vs. reducing efficiency)
**Fix**: Design systems as cognitive prosthetics that extend but don't replace organizational thinking

## Worked Examples

### Example 1: IT Department Resistance to New DevOps Platform

**Scenario**: CTO mandates transition to new DevOps platform. Development teams resist, claiming it "doesn't fit our workflow." Project stalls.

**Novice Analysis**: "They're just resistant to change. Need better training and change management."

**Expert BDI Analysis**:
1. **Level Selection**: Use micro-level (individual agent) modeling—need to predict specific adoption decisions
2. **Perceptual Filter Mapping**: 
   - CTO perceives: strategic efficiency, vendor relationships, industry standards
   - Developers perceive: daily tool friction, debugging complexity, deployment reliability
3. **Intention Analysis**: CTO formed strong intention (annual planning cycle), developers have weak intentions (sprint-level)
4. **Accommodation Design**: Instead of forcing consensus, create accommodation—parallel toolchain during transition, developer input on configuration

**Trade-offs Identified**: 
- CTO's strategic intention vs. developers' operational flexibility
- Platform standardization vs. workflow customization
- Short-term productivity loss vs. long-term efficiency gains

**Resolution**: Design accommodation allowing gradual migration with developer customization input, rather than forcing consensus on "best" approach.

### Example 2: M&A Integration Failure

**Scenario**: Large corp acquires startup. 18 months later, startup talent has fled, innovation has stopped, integration deemed failure.

**Expert BDI Analysis**:
1. **Level Selection**: Macro-level—examining organizational identity and culture clash
2. **Belief-Desire-Intention Mapping**:
   - **Large Corp Agent**: Beliefs (process standardization works), Desires (predictable outcomes), Intentions (integrate within 12 months)
   - **Startup Agent**: Beliefs (agility requires flexibility), Desires (rapid innovation), Intentions (maintain autonomy)
3. **Discourse Analysis**: No genuine negotiation occurred—integration was mandated, not accommodated
4. **Failure Mode**: Consensus assumption—assumed shared goals without modeling desire formation process

**What Novice Missed**: Treated integration as operational problem rather than cognitive coordination challenge between incompatible agent architectures.

**Expert Intervention**: Design dual-agent accommodation—startup maintains separate BDI structure while creating interface protocols for coordination with parent org.

## Quality Gates

- [ ] All key organizational agents identified at appropriate abstraction level
- [ ] Each agent's perceptual filters explicitly mapped (role, expertise, position-based)
- [ ] Intention formation and commitment thresholds specified for each agent type
- [ ] Disagreement accommodation mechanisms designed (not consensus requirements)
- [ ] Model predictions compared against actual organizational behavior patterns
- [ ] System interfaces aligned with organizational abstraction level boundaries
- [ ] Desire formation processes modeled (not just satisfaction of given goals)
- [ ] Information flow designed for subjective beliefs, not objective shared state
- [ ] Escalation triggers defined for when abstraction level coordination breaks down
- [ ] Failure mode detection rules testable against observable organizational symptoms

## NOT-FOR Boundaries

**This skill is NOT for:**
- **Simple process automation** → Use standard workflow modeling instead
- **Individual psychology modeling** → Use cognitive psychology frameworks instead  
- **Technical system optimization** → Use operations research methods instead
- **Legal/compliance requirements** → Use regulatory framework analysis instead
- **Financial modeling** → Use economic analysis frameworks instead

**Delegate to other skills when:**
- Need individual behavioral prediction → Use `cognitive-behavioral-modeling`
- Need technical performance optimization → Use `system-performance-analysis`  
- Need regulatory compliance design → Use `compliance-framework-design`
- Need pure multi-agent coordination → Use `distributed-systems-coordination`
- Need organizational change management → Use `change-management-strategy`

**This skill specifically addresses**: The cognitive architecture of organizational decision-making where multiple agents with different expertise levels must coordinate through discourse and accommodation rather than consensus or authority.