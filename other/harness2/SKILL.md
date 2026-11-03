---
name: harness2
description: >
  Harness²: Recursive Agent Harnessing (Google Research / arXiv:2610.14224). Dynamically adapts and self-improves
  the agent execution harness on-the-fly using dual-level recursion (Propose-Probe-Compose and Harnessing Recursion).
license: Apache-2.0
---

# Harness² — Recursive Agent Harnessing for Open-World Tasks

Based on Google Research (*arXiv:2610.14224*), **Harness²** enables recursive self-improvement (RSI) for LLM agents without retraining or updating underlying model weights. It operates by iteratively diagnosing, adapting, and evolving the **execution harness** (tools, prompts, memory, validators, and middleware).

## Dual-Level Recursive Architecture

### Level 1: Task-Level Recursion (Propose – Probe – Compose)
When facing an open-world task where ground-truth automated verifiers may not exist:
1. **Propose**: Generate candidate repairs or modifications to the current harness and plan.
2. **Probe**: Run lightweight diagnostic probes and contrastive execution traces to assess viability and side effects.
3. **Compose**: Synthesize successful probe elements into an upgraded execution harness tailored to solve the immediate task.

### Level 2: Harnessing-Level Recursion
- Extracts generalized insights across task-level runs.
- Updates the agent's long-term harness library without accumulating noise or catastrophic forgetting.
- Evaluates whether new harness patterns (guardrails, tool definitions, verification heuristics) improve performance on benchmark suites.

## How to Apply Harness²
1. **Contrastive Trace Analysis**: When an agent hits an execution error, contrast the failing run against previous successful patterns.
2. **Harness Mutation**: Adjust prompt constraints, tool parameters, or verification gates dynamically.
3. **Probe Validation**: Validate the mutation on a sandboxed sub-problem before committing to the full task.
