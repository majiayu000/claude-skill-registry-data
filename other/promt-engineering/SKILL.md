---
name: prompt-engineering
description: "Write, optimize, and debug LLM prompts — system prompts, task prompts, and prompt templates. Trigger when: the user wants to write or improve a system prompt; asks 'how do I prompt Claude/GPT/Gemini to [X]'; a prompt keeps giving bad or inconsistent outputs; wants to build a prompt template; asks about few-shot, chain-of-thought, or role-based prompting; wants to reduce hallucinations or improve AI output quality; or asks to evaluate or critique a prompt. Key capabilities: role assignment, output format specification, few-shot examples with 2–3 input→output pairs, chain-of-thought reasoning, XML tag structure, positive over negative framing, and a 7-field system prompt template (Role/Goal/Context/Instructions/Output Format/Constraints). Also for: rewriting vague requests as structured prompts, debugging prompt output problems with a 5-step checklist, generating prompt templates for recurring tasks, and evaluating prompt clarity with a 5-dimension rubric (clarity, specificity, example quality, constraint completeness, format spec). Does NOT trigger for general code writing or non-AI tasks."
---

# Prompt Engineering Skill

## Core Techniques

### 1. Be Specific About Output Format
Always specify: format (JSON, markdown, bullet list), length, tone, and structure.
```
Bad:  "Summarize this article"
Good: "Summarize this article in 3 bullet points, each under 20 words, focusing on business impact"
```

### 2. Give the Model a Role
```
"You are a senior software engineer reviewing code for production readiness. 
Your goal is to find bugs, security issues, and performance problems."
```

### 3. Use Examples (Few-Shot)
Include 2-3 examples of input → output pairs before the actual task.

### 4. Chain of Thought
For reasoning tasks, add: *"Think step by step before giving your final answer."*

### 5. XML Tags for Structure
```xml
<context>Background information here</context>
<task>What you want done</task>
<constraints>Rules to follow</constraints>
<output_format>Expected format</output_format>
```

### 6. Positive Instructions Over Negative
```
Bad:  "Don't write long responses"
Good: "Keep responses under 100 words"
```

## Concrete Examples

### Before/After Prompt Improvement

**Weak:** "Summarize this article"
**Strong:** "Summarize this article in 3 bullet points, each under 20 words, focusing on business impact. Start with the most important finding."

**Weak:** "Review my code"
**Strong:** "You are a senior software engineer reviewing code for production readiness. Find bugs, security issues, and performance problems. For each issue found: state the file, line, problem, and recommended fix. If none found, say so explicitly."

**Weak:** "Help me with this API"
**Strong:** "Write a Python function that calls the /users endpoint with bearer token auth, handles 401/429/500 errors with different retry strategies, and returns a typed User object. Include docstring with parameters and return type."

### Trigger-Specific Guidance

**"How do I prompt Claude to..."** - Rewrite the user's idea as a structured system prompt with role, constraints, and output format.

**"This prompt keeps giving bad outputs"** - Debug using the prompt debugging checklist: add format spec -> reduce ambiguity -> break into sub-tasks -> add "if unsure, say so".

**"Build a prompt template"** - Start with the system prompt template in this skill, then customize role/goal/context/instructions/output_format/constraints for the specific use case.

**"Chain-of-thought prompt"** - Add "Think step by step before giving your final answer" or use explicit reasoning steps as few-shot examples.

**"Few-shot prompt"** - Include 2-3 input->output pairs that span the key cases (success, edge case, failure mode).

## System Prompt Template
```
# Role
[Who the AI is and its expertise]

# Goal  
[What it should accomplish]

# Context
[Background the AI needs]

# Instructions
[Step-by-step behavior]

# Output Format
[Exact structure of responses]

# Constraints
[Hard rules it must follow]
```

## Debugging Prompts
When a prompt gives bad outputs:
1. Add explicit output format with an example
2. Reduce ambiguity — reread as if you know nothing
3. Break into smaller sub-tasks
4. Add "If unsure, say so" to reduce hallucinations
5. Test with edge cases

## Evaluation Checklist

Rate each prompt 1-5 on:
- **Clarity**: Is the goal unambiguous?
- **Specificity**: Are output format, length, and constraints explicit?
- **Example Quality**: Are few-shot examples covering key cases?
- **Constraint Completeness**: Are edge cases and failure modes handled?

**Below 15/25**: Rewrite the prompt.