---
name: skill.md---llm-mathematical-contest-evaluation-fra
description: Skill for AI agent capabilities
---

# SKILL.md - LLM Mathematical Contest Evaluation Framework

## Paper Reference
- **arXiv ID**: 2604.04791
- **Title**: How Far Are We? Systematic Evaluation of LLMs vs. Human Experts in Mathematical Contest in Modeling
- **Authors**: Yuhang Liu et al.
- **Date**: April 2026
- **URL**: https://arxiv.org/abs/2604.04791

## Utility Score
**0.86** - High utility for LLM evaluation methodology

## Core Insight
LLMs show a **comprehension-execution gap**: strong at problem identification and formulation, but fail at execution stages (model solving, code implementation, result analysis). This gap persists with model scaling.

## Key Methods
### Stage-Wise Evaluation Framework
Problem-oriented evaluation across modeling stages:
1. **Problem Identification**
2. **Formulation**
3. **Model Solving** ← Gap here
4. **Code Implementation** ← Gap here
5. **Result Analysis** ← Gap here

### Validation
- Automatic scores compared with independent human expert judgments
- Stronger alignment than existing evaluation schemes
- Expert-verified criteria from China Postgraduate Mathematical Contest in Modeling

### Failure Analysis
Errors traced to:
- Insufficient specification
- Missing verification
- Lack of validation
- Error propagation across stages without correction

## When to Apply
- End-to-end LLM capability evaluation
- Benchmarking real-world problem solving
- Identifying model limitations
- Complex task evaluation methodology

## Practical Applications
1. **Evaluation Design**: Stage-wise framework for complex tasks
2. **Gap Identification**: Pinpoint where models fail
3. **Benchmark Creation**: Expert-validated criteria
4. **Model Development**: Focus on execution-oriented improvements

## Key Takeaways
- **Scaling alone won't bridge the gap**
- **Need approaches beyond model size**
- **Comprehension ≠ execution**: different capabilities
- **Error propagation**: failures cascade without correction

## Implications
- Current LLMs excel at understanding but struggle with doing
- Complex real-world problems require end-to-end workflows
- Execution stages need specialized attention

## Tags
`llm-evaluation` `benchmark` `mathematical-modeling` `comprehension-gap` `execution-gap` `stage-wise-evaluation` `expert-validation`

## Activation Keywords

- "paper-llm-eval"
- "paper llm eval"
- "use paper llm eval"
- "paper llm eval help"
- "paper llm eval tool"

## Tools Used

- `Read` - Read existing files and documentation
- `Write` - Create new files and documentation
- `Bash` - Execute commands when needed

## Instructions for Agents

1. Identify user's intent and specific requirements
2. Gather necessary context from files or user input
3. Execute appropriate actions using available tools
4. Provide clear results and suggest next steps

## Examples

### Basic Paper Llm Eval usage
```
User: "Help me with paper llm eval"
→ Understand requirements → Execute actions → Provide results
```

### Advanced usage
```
User: "I need detailed paper llm eval assistance"
→ Clarify scope → Provide comprehensive solution → Follow up
```
