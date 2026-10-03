---
name: seed-prover-1-5
title: "Seed-Prover 1.5: Mastering Theorem Proving via Learning from Experience"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.17260
keywords: [theorem-proving, lean, reinforcement-learning, tool-use, formal-methods]
description: "Enable LLM agents to incrementally construct formal proofs through strategic tool orchestration rather than one-shot generation. Combines natural language reasoning, sketch translation, and formal verification in an agentic workflow trained via PPO and Rubric RL, achieving competitive performance on undergraduate and graduate proof problems."
---

## Overview

Seed-Prover 1.5 bridges natural language mathematical reasoning and formal theorem proving by decomposing the task into three specialized agents: natural language proving, sketch-to-Lean translation, and formal verification. This hierarchical approach enables parallel sub-goal solving and efficient test-time scaling.

## Core Technique

The system employs three coordinated agents with distinct roles:

**Agent Orchestration:**
Rather than monolithic end-to-end proving, the framework decomposes work into independent stages that enable parallelization and leverage each agent's strengths.

```python
# Three-agent orchestration pattern
def prove_theorem(problem):
    # Stage 1: Natural language prover
    nl_proof = nl_prover_agent.prove(problem)

    # Stage 2: Sketch translator (Rubric RL trained)
    lean_sketch = sketch_translator.translate(nl_proof, problem)

    # Stage 3: Agentic verifier
    verified_lemmas = verifier_agent.verify_and_build(lean_sketch)

    return verified_lemmas if verified_lemmas else None
```

**Tool-Augmented Verification:**
The verifier agent uses three key tools: Lean compilation for correctness checking, Mathlib search for relevant lemmas, and Python execution for computational validation. Tool usage patterns are learned through PPO-based training.

```python
# Verifier's tool integration
class AgenticProver:
    def __init__(self):
        self.tools = {
            'lean_verify': compile_lean_proof,
            'search_mathlib': find_relevant_lemmas,
            'compute': execute_python
        }

    def prove_incremental(self, sketch):
        while not complete:
            action = select_tool()  # Learned via PPO
            result = self.tools[action](current_state)
            update_internal_state(result)
```

**Hierarchical Reward Structure:**
Large-scale RL training uses outcome rewards from Lean compilation. Rubric RL for the sketch model decomposes complex proofs into lemma-style sub-goals with separate reward signals.

## When to Use This Technique

Use Seed-Prover 1.5 when:
- Proving Lean theorems from mathematical problem statements
- You want interpretable intermediate (sketch) representations
- Problems decompose naturally into independent lemmas
- Combining natural language and formal reasoning is beneficial

## When NOT to Use This Technique

Avoid this approach if:
- Working with non-Lean formal systems (requires agent retooling)
- Proof states are highly interdependent (decomposition ineffective)
- Real-time single-pass proving is required
- Mathematical domain is completely novel (limited Mathlib coverage)

## Implementation Notes

The framework requires:
- Three separately trained agents with coordinated interfaces
- PPO training infrastructure for tool-use learning
- Rubric RL for intermediate sketch-to-Lean translation
- Integration with Lean compiler and Mathlib repository
- Handles both undergraduate (PutnamBench) and graduate (FATE-H) difficulty levels

## Key Performance

- 88% on PutnamBench (undergraduate-level)
- 80% on FATE-H (graduate-level)
- Efficient through hierarchical decomposition

## References

- Multi-agent orchestration for theorem proving
- Tool-augmented LLM agents with PPO training
- Rubric-based reward learning for structured outputs
