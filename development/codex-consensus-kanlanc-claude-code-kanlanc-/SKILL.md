---
name: codex-consensus
description: Use for multi-perspective analysis with Codex exploring different viewpoints. Triggers on "codex perspectives", "pros and cons from codex", "codex evaluate options", "what are the tradeoffs".
---

# Codex Consensus Skill

Multi-perspective analysis with Codex (gpt-5.2) for balanced decision-making.

## When to Use

- Evaluating technology choices
- Architecture decisions with tradeoffs
- When user needs pros/cons analysis
- Comparing different approaches
- Making strategic decisions

## Reasoning Level

**high** (balanced analysis from multiple angles)

## Execution

1. Identify the decision or question
2. Gather relevant context
3. Formulate a multi-perspective prompt:
   ```
   Analyze this from multiple perspectives.

   Question/Decision: <what to evaluate>

   Context:
   <relevant information>

   Please provide:
   1. **FOR perspective**: Best arguments in favor
   2. **AGAINST perspective**: Best arguments against
   3. **NEUTRAL perspective**: Objective analysis of tradeoffs
   4. **SYNTHESIS**: Balanced recommendation considering all factors
   ```
4. Run: `codex exec -c model_reasoning_effort="high" "<prompt>"`
5. Return structured multi-perspective analysis

## Response Format

```
**Codex Multi-Perspective Analysis:**

**Question:** [The decision/question being analyzed]

**FOR (Arguments in Favor):**
- [Pro 1]
- [Pro 2]

**AGAINST (Arguments Against):**
- [Con 1]
- [Con 2]

**NEUTRAL (Tradeoffs & Considerations):**
- [Tradeoff 1]
- [Tradeoff 2]

**SYNTHESIS:**
[Balanced recommendation with reasoning]

**Session ID:** [id]
```
