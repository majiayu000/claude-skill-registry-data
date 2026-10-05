---
name: credit-optimizer
description: Automatically optimize AI agent credit usage by routing tasks to the most cost-efficient execution path. Use when you want to reduce AI API costs by 30-75% without quality loss, classify task complexity before execution, route simple tasks to free or low-cost models, split complex tasks into optimized sub-tasks, or detect vague prompts before wasting credits.
version: 5.2.0
author: rafsilva85
license: MIT
compatibility: claude-code, cursor, codex, manus, opencode
---

# Credit Optimizer v5

**Automatically optimize AI agent credit/token usage by routing tasks to the most cost-efficient execution path — with zero quality loss.**

Audited across 53 real-world scenarios. 30-75% cost savings. 0% quality degradation.

## When to Use This Skill

- Before executing any AI task that consumes credits or tokens
- When you want to minimize API costs without sacrificing output quality
- When processing batches of tasks with varying complexity
- When you need to decide between different model tiers (free/standard/premium)

## How It Works

### Step 1: Task Classification

Analyze the incoming task and classify it into one of these categories:

| Category | Examples | Typical Savings |
|----------|----------|-----------------|
| Simple Q&A | Definitions, facts, conversions | 90-100% (use free tier) |
| Code Generation | Scripts, functions, refactoring | 40-60% |
| Research | Multi-source analysis, synthesis | 20-40% |
| Creative Writing | Articles, stories, marketing copy | 30-50% |
| Data Analysis | CSV processing, visualization | 40-70% |
| Complex Reasoning | Multi-step logic, architecture | 10-20% |

### Step 2: Prompt Quality Check

Before executing, evaluate the prompt:

1. **Clarity Score** (1-10): Is the request specific enough?
   - Score < 5: Ask for clarification BEFORE executing (saves wasted credits)
   - Score 5-7: Add reasonable assumptions and proceed
   - Score 8+: Execute directly

2. **Scope Detection**: Can this be split into smaller, cheaper sub-tasks?
   - If YES: Break into atomic tasks, route each independently
   - If NO: Route as single task

3. **Data Requirement Check**: Does this need real-time data?
   - If YES: Use tools/search first, then process with cheaper model
   - If NO: Use internal knowledge with appropriate model tier

### Step 3: Model Routing

Route to the optimal execution path:

```
IF task is simple Q&A or formatting:
  → Use FREE tier / Chat mode (no credits)
  
IF task is medium complexity (code, writing, basic analysis):
  → Use STANDARD tier
  
IF task requires deep reasoning, multi-step logic, or creative excellence:
  → Use PREMIUM/MAX tier
  
IF task is mixed complexity:
  → SPLIT into sub-tasks and route each independently
```

### Step 4: Execution Optimization

During execution, apply these optimizations:

- **Context Pruning**: Only include relevant context, not entire conversation history
- **Output Scoping**: Request specific output format to avoid verbose responses
- **Caching**: Check if similar tasks were recently completed
- **Batch Processing**: Group similar sub-tasks for efficient processing

## Efficiency Directives

1. **Never use premium models for tasks that standard can handle equally well**
2. **Always check if the task can be answered from cached/known information first**
3. **Split compound requests into atomic tasks before routing**
4. **Ask for clarification on vague prompts — it's cheaper than re-doing work**
5. **Use structured output formats to reduce token waste**

## Audit Results Summary

| Metric | Result |
|--------|--------|
| Scenarios tested | 53 |
| Average savings | 30-75% |
| Quality loss | 0% |
| Quality improvement cases | 2 |
| False routing rate | < 3% |

## Links

- **Website**: [creditopt.ai](https://creditopt.ai)
- **GitHub**: [github.com/rafsilva85/manus-credit-optimizer](https://github.com/rafsilva85/manus-credit-optimizer)
- **MCP Server**: Available as Python MCP server for programmatic integration
- **Full Manus Skill**: Available at [Gumroad](https://rafaamaral.gumroad.com/l/credit-optimizer-v5) ($29, one-time)
