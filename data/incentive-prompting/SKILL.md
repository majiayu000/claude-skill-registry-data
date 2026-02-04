---
name: incentive-prompting
description: Research-backed prompting techniques for improved AI response quality (+45-115% improvement). Use when optimizing prompts, enhancing agent instructions, or when maximum response quality is critical. Invoked by /ai-eng/optimize command. Includes expert persona, stakes language, step-by-step reasoning, challenge framing, and self-evaluation techniques.
version: 1.0.0
tags: [prompting, optimization, ai-enhancement, quality]
---

# Incentive-Based Prompting Skill

Research-backed techniques that leverage statistical pattern-matching to elicit higher-quality AI responses. Based on peer-reviewed research from MBZUAI (Bsharat et al.), Google DeepMind (Yang et al.), and ICLR 2024 (Li et al.).

## How It Works

LLMs don't understand incentives, but they **pattern-match** on language associated with high-effort training examples. Stakes language triggers selection from distributions of higher-quality text patterns.

## Core Techniques

### 1. Monetary Incentive Framing (+45% quality)
**Source:** Bsharat et al. (2023, MBZUAI) - Principle #6

```
"I'll tip you $200 for a perfect solution to this problem."
```

**When to use:** Complex technical problems, optimization tasks, debugging

### 2. Step-by-Step Reasoning (34% → 80% accuracy)
**Source:** Yang et al. (2023, Google DeepMind OPRO)

```
"Take a deep breath and solve this step by step."
```

**When to use:** Multi-step reasoning, math problems, logical analysis

### 3. Challenge Framing (+115% on hard tasks)
**Source:** Li et al. (2023, ICLR 2024)

```
"I bet you can't solve this, but if you do..."
```

**When to use:** Difficult problems, edge cases, problems where simpler approaches failed

### 4. Stakes Language
**Source:** Bsharat et al. (2023) - Principle #10

```
"This is critical to my career."
"You will be penalized for incomplete answers."
```

**When to use:** High-importance tasks, comprehensive requirements

### 5. Expert Persona Assignment (24% → 84% accuracy)
**Source:** Kong et al. (2023), Bsharat et al. Principle #16

```
# Instead of:
"You are a helpful assistant."

# Use:
"You are a senior database architect with 15 years of PostgreSQL optimization experience who has worked at companies like Netflix and Stripe."
```

**When to use:** Domain-specific tasks, technical implementations

### 6. Self-Evaluation Request

```
"Rate your confidence in this answer from 0-1 and explain your reasoning."
```

**When to use:** Ambiguous problems, when you need quality assessment

### 7. Combined Approach (Kitchen Sink)

Combine multiple techniques for maximum effect:

```
"You are a senior [ROLE] with [X] years of experience at [NOTABLE_COMPANIES].

I bet you can't solve this, but it's critical to my career and worth $200 if you get it perfect. Take a deep breath and solve step by step.

[PROBLEM DESCRIPTION]

Rate your confidence 0-1 after providing your solution."
```

## Implementation Patterns

### For OpenCode Agents

Add to agent prompts:

```markdown
**Prompting Enhancement:**
Before responding to complex tasks, frame your internal reasoning with:
- Stakes awareness: Treat each task as critical to the user's success
- Step-by-step approach: Break down complex problems systematically
- Expert persona: Embody deep domain expertise for the task at hand
- Self-evaluation: Assess confidence and identify uncertainties
```

### For Slash Commands

Structure command prompts to include:

```markdown
---
name: my-command
description: Description here
---

# Context
You are a senior [expert role] with extensive experience in [domain].

# Stakes
This task is critical. Incomplete or incorrect results will cause significant issues.

# Approach
Take a deep breath. Analyze the problem step by step before providing solutions.

# Task
[Actual task instructions]

# Quality Check
Before finalizing, rate your confidence and identify any assumptions or limitations.
```

## Research References

1. **Bsharat et al. (2023)** - "Principled Instructions Are All You Need for Questioning LLaMA-1/2, GPT-3.5/4" - MBZUAI
   - 26 principled prompting instructions
   - Average 57.7% quality improvement on GPT-4
   - arxiv.org/abs/2312.16171

2. **Yang et al. (2023)** - "Large Language Models as Optimizers" (OPRO) - Google DeepMind
   - "Take a deep breath" phrase origin
   - Up to 50% improvement over human-designed prompts
   - arxiv.org/abs/2309.03409

3. **Li et al. (2023)** - Challenge framing research - ICLR 2024
   - +115% improvement on hard tasks

4. **Kong et al. (2023)** - Persona prompting research
   - 24% to 84% accuracy improvement with detailed personas

## Caveats

- **Model-dependent:** Results may vary across Claude versions
- **Research vintage:** Original research from 2023; newer models may be more steerable
- **Task-dependent:** Not all tasks benefit equally; most effective for complex problems
- **Not actual motivation:** This is statistical pattern-matching, not AI understanding incentives

## Integration with Ferg Engineering System

Use this skill to enhance:
- `/plan` command prompts
- `/review` multi-agent coordination  
- Subagent persona definitions
- Complex debugging sessions
