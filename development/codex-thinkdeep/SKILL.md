---
name: codex-thinkdeep
description: Use for deep multi-step investigation and analysis with Codex. Triggers on "codex deep analysis", "investigate with codex", "codex thorough investigation", "have codex think deeply".
---

# Codex ThinkDeep Skill

Multi-step investigation and deep reasoning with Codex (gpt-5.2) using extra-high reasoning.

## When to Use

- Complex problems requiring step-by-step analysis
- Architecture decisions
- Performance deep-dives
- Security analysis
- When user asks for "deep", "thorough", or "comprehensive" Codex analysis

## Reasoning Level

**xhigh** (always - this skill is for deep analysis)

## Execution

1. Understand the problem fully
2. Gather all relevant files and context
3. Formulate a structured prompt:
   ```
   Investigate this step by step. Form hypotheses, test them, and build confidence.

   Question: <user's question>

   Context:
   <relevant file contents>

   Please:
   1. Break down the problem
   2. Form initial hypotheses
   3. Analyze each hypothesis
   4. Reach a well-reasoned conclusion
   ```
4. Run: `codex exec -c model_reasoning_effort="xhigh" "<prompt>"`
5. Return the comprehensive analysis

## Response Format

```
**Deep Analysis from Codex:**

**Problem Breakdown:**
[Step-by-step analysis]

**Hypotheses Explored:**
[Each hypothesis and findings]

**Conclusion:**
[Final recommendation with confidence level]

**Session ID:** [id]
```
