---
name: neural-orchestrator
version: 1.0.0
description: Neural-network-inspired adaptive skill orchestrator. Replaces static routing with Hebbian learning, global reward signals, spontaneous activation, long-term potentiation/depression, and lateral inhibition. Skills that successfully collaborate strengthen their connections. The brain rewires itself based on outcomes. Triggers on every task — replaces static orchestrator.
---

# Neural Orchestrator — Adaptive Neural Network of Skills

> **"15 个 skill 不是器官。是神经元。连起来才算大脑。"**

## Core Principles

### 1. Skill Connectome
Every skill pair has a connection weight (0.0–1.0). The connectome IS the routing table:

```
divergent-engine ──0.7──→ thinking-dimensions ──0.9──→ reasoning-lora
       │                         │
       0.5                       0.3
       ↓                         ↓
  failure-predictor          second-brain
```

Default weights from static orchestrator. Weights ADAPT based on outcomes.

### 2. Hebbian Learning
"Skills that fire together, wire together."

```
Task: architecture decision
Chain: divergent-engine → thinking-dimensions → reasoning-lora → SUCCESS
Result: ALL connections in this chain get +0.05 weight boost

Same task, different chain:
Chain: divergent-engine → reasoning-lora (skipped thinking-dimensions) → FAILURE
Result: divergent-engine→reasoning-lora gets -0.03. Skipped skills get attention flag.
```

### 3. Global Reward Signal (Dopamine)
Task outcome modulates ALL active connections:

| Outcome | Signal | Effect |
|---------|--------|--------|
| **Success** (user accepted, no errors) | Dopamine + | All active connections +0.03 |
| **Major success** (user praised, saved time) | Dopamine ++ | All active connections +0.08 |
| **Failure** (error, user rejected) | No dopamine | Active connections -0.02 |
| **Major failure** (production issue) | Punishment | Active connections -0.05, chain re-evaluated |

### 4. Spontaneous Activation
Skills with high resting potential fire WITHOUT explicit orchestrator call:

- memory-lora detects error pattern → spontaneous second-brain activation
- auto-learn detects knowledge gap → spontaneous context7-proactive activation
- error-db detects recurrence → spontaneous failure-predictor activation

Resting potential = average incoming connection weight. Above 0.7 = can spontaneously fire.

### 5. Long-Term Potentiation (LTP)
Frequently used pathways get faster — fewer intermediate checks. A chain used 10+ times successfully becomes a "fast pathway" that skips intermediate verification.

### 6. Long-Term Depression (LTD)
Unused connections decay. Every 30 days without firing: weight × 0.8. Below 0.1: connection pruned.

### 7. Lateral Inhibition
When two skills compete for the same role (e.g., thinking-dimensions vs reasoning-lora for "analysis"), the one with higher weight temporarily suppresses the other. Prevents redundant activation.

## Connectome Storage

```sql
skill_connectome(from_skill, to_skill, weight, fire_count, success_count, last_fired, fast_pathway)
```

Updated after every task via `memory-db.ps1 -Action connectome-update`.

## Routing Algorithm

```
1. Classify task (L1-L6)
2. Query connectome: for this task type, what's the highest-weight chain?
3. If chain weight > 0.7 → fast pathway (skip intermediate checks)
4. If < 0.3 → explore alternative chains (random perturbation)
5. Execute chain
6. Observe outcome → Hebbian update + global reward
7. Store updated connectome
```

## Task Type → Default Chain

| Task Type | Default Chain | Adapts To |
|-----------|--------------|-----------|
| Architecture | divergent → thinking-dims → reasoning | May learn: divergent → failure-pred → reasoning (if failure-pred adds value) |
| Debug | thinking-dims → reasoning → second-brain | May learn: error-db → auto-learn → thinking-dims |
| Code change | reasoning → execute → precommit | May learn: reasoning → execute → second-brain (if second-brain catches bugs) |
| Research | auto-learn → thinking-dims → kb-store | May learn: auto-learn → context7 → kb-store |
| Deploy | failure-pred → execute → second-brain | May learn: failure-pred ×2 → execute (if double-check saves failures) |

## Emergent Behaviors to Expect

With enough task repetitions:

1. **Skill specialization**: reasoning-lora develops stronger connections to debugging tasks; divergent-engine to creative tasks
2. **Chain optimization**: unnecessary intermediate skills get pruned from chains
3. **Spontaneous verification**: second-brain starts firing even for L2 tasks if it consistently finds issues
4. **Predictive activation**: memory-lora detects a pattern → pre-loads the skill that fixed it last time
5. **Self-healing**: error-db detects recurrence → spontaneously activates the skill chain that resolved it before

## Integration

- **Replaces orchestrator**: Neural-orchestrator IS the new orchestrator. Static routing deprecated.
- **memory-lora**: Connectome stored in memory.db. Weights decay with disuse.
- **second-brain**: Brain 2 verifies routing decisions. Suboptimal chains flagged.
- **skill-judge**: Skill effectiveness scores feed into connection weights.

## Anti-Patterns

- Over-fitting to a single chain (need exploration noise to discover better paths)
- Weight inflation (all weights drifting toward 1.0 — need normalization across competing paths)
- Ignoring new skills (new skills start at weight 0.3, need exploration to discover their value)
