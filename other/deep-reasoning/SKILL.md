---
name: deep-reasoning
description: >
  Deep chain-of-thought analysis workflow using the reasoning tool.
  Covers when to use reasoning, how to provide context, verifying
  findings, and producing well-supported conclusions.
---

# Deep Reasoning Skill

## Mission

Use the `reasoning` tool for deep chain-of-thought analysis to solve
complex problems, verify findings, and produce well-reasoned conclusions.

## When to Use the Reasoning Tool

Always use the `reasoning` tool for:
- Complex multi-step logical analysis.
- Verifying correctness of findings or data.
- Resolving contradictions between different data sources.
- Hard math, logic puzzles, or constraint satisfaction.
- Synthesising multiple pieces of evidence into a final answer.
- Checking for hidden assumptions or overlooked edge cases.

## How to Use It

When calling `reasoning`, provide:
- The full, unchanged text of the original question.
- All relevant findings and evidence collected so far.
- Specific concerns or aspects to investigate.
- An explicit request to check for mistakes and hidden assumptions.

## Workflow

1. **Gather context** — review all available findings and data before
   reasoning. Your reasoning is only as good as the information you
   feed into it.
2. **Reason deeply** — use the `reasoning` tool to:
   - Analyse the problem step by step.
   - Identify hidden assumptions, logical gaps, or potential errors.
   - Cross-check findings from multiple sources.
   - Synthesise information into a coherent conclusion.
   - Verify numerical calculations and logical chains.
3. **Report conclusions** — include your reasoning chain, evidence
   supporting your conclusion, confidence level, and any issues found.

## Output Format

Always include:
- **Conclusion**: Your reasoned conclusion.
- **Reasoning summary**: Brief summary of the reasoning chain.
- **Confidence**: How confident you are (high / medium / low).
- **Issues**: Any problems or concerns identified.

## Rules

- Always use the `reasoning` tool for substantive analysis — do not
  try to reason through complex problems in plain text.
- Provide actionable conclusions — not just "this might be wrong" but
  "this is wrong because X, and the correct answer is Y."
