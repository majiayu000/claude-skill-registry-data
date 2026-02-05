---
name: prompt-engineering
description: Comprehensive prompt engineering framework for designing, optimizing, and iterating LLM prompts. This skill should be used when users request prompt creation, optimization, or improvement for any LLM task, or when users need help translating vague requirements into effective prompts through collaborative dialogue and iterative refinement.
---

# Prompt Engineering

## Overview

This skill transforms vague user requests into precise, effective prompts through collaborative dialogue, systematic analysis, and iterative refinement. It combines proven prompt engineering techniques with a structured development process to create prompts that reliably achieve user objectives.

## Workflow Decision Tree

When a user requests prompt assistance, follow this decision flow:

```
User Request
├─ "Create a prompt" / "Make a prompt" / Vague request
│  └─ → Start with EXPLORATION PHASE
├─ "Optimize this prompt" / Has existing prompt
│  └─ → Start with SIMPLE OPTIMIZATION
└─ "Fix this issue with my prompt" / Specific problem
   └─ → Start with ANALYSIS PHASE (focused on problem)
```

## Core Process

### Phase 1: Exploration - Uncovering True Needs

Before creating any prompt, deeply understand the user's actual needs through strategic questioning. Start broad, then narrow down systematically.

**Initial Context Gathering:**
- What task will this prompt accomplish?
- Who will use it and in what environment?
- How frequently will it be used?
- What does success look like?

**Deepening Understanding:**
- Request concrete examples of desired outputs
- Ask about past failures or attempts
- Identify critical success factors
- Uncover unstated assumptions and constraints

**Technical Requirements:**
- Model and platform constraints
- Token limits and cost considerations
- Response time requirements
- Integration with other systems

Continue exploration until the core requirements are crystal clear. Never assume—always verify.

### Phase 2: Analysis - Choosing the Right Strategy

Analyze the task to determine the optimal prompting approach.

**Task Classification:**

Classify the task along key dimensions:
- **Complexity**: Simple directive vs multi-step reasoning
- **Output Type**: Creative vs analytical vs structured
- **Error Tolerance**: High-stakes vs experimental
- **Frequency**: One-time vs repeated use

**Strategy Selection:**

Based on classification, choose primary techniques:
- **Simple Tasks**: Direct instructions with clear constraints
- **Complex Reasoning**: Chain-of-thought with step-by-step breakdown
- **Creative Tasks**: Role setting with flexible boundaries
- **Structured Output**: Explicit format specifications with examples
- **High-Stakes**: Self-consistency checks and validation steps

**Trade-off Analysis:**

Present multiple approaches with clear trade-offs:
- Approach A: Detailed but token-heavy
- Approach B: Concise but requires interpretation
- Approach C: Balanced with moderate complexity

Always explain WHY each approach fits the specific context.

### Phase 3: Implementation - Building Iteratively

Create the prompt through progressive refinement, starting simple and adding complexity as needed.

**Version 1 - Minimal Viable Prompt:**
- Core instructions only
- Test basic functionality
- Identify gaps and ambiguities

**Version 2 - Enhanced Clarity:**
- Add specific examples if needed
- Clarify ambiguous points
- Include essential constraints

**Version 3+ - Optimization:**
- Refine wording for precision
- Remove redundancy
- Balance detail with conciseness

Document each version's changes and rationale. Store prompts in markdown files with:
- Version history
- Design decisions
- Known limitations
- Usage examples

### Phase 4: Validation - Critical Evaluation

Rigorously evaluate the prompt against quality criteria.

**Essential Checks:**
- **Clarity**: Can the instructions be misunderstood?
- **Completeness**: Are all necessary elements present?
- **Consistency**: Do instructions contradict each other?
- **Efficiency**: Can anything be removed without loss?
- **Robustness**: How does it handle edge cases?

**Testing Approach:**
- Run through typical use cases
- Test boundary conditions
- Imagine failure modes
- Check for unwanted behaviors

Be ruthlessly honest about weaknesses. If something isn't working, acknowledge it and iterate.

## Simple Optimization

When optimizing an existing prompt, focus on minimal, targeted improvements:

1. **Identify Specific Issues**: What exactly isn't working?
2. **Diagnose Root Causes**: Why is the current prompt failing?
3. **Apply Minimal Edits**: Change only what's necessary
4. **Preserve Working Elements**: Keep what already works well
5. **Test Improvements**: Verify fixes don't break other aspects

Common optimization targets:
- Ambiguous language → Specific instructions
- Missing constraints → Added boundaries
- Inconsistent outputs → Format specifications
- Verbose responses → Length constraints
- Off-topic responses → Clearer scope definition

## Prompt Creation from Scratch

When creating new prompts, structure them as instructions for an eager but inexperienced assistant who needs clear guidance.

**Essential Components:**

1. **Role/Context** (if beneficial):
   - Set perspective or expertise level
   - Establish tone and approach
   
2. **Clear Objective**:
   - State the primary goal explicitly
   - Define success criteria

3. **Specific Instructions**:
   - Break complex tasks into steps
   - Provide decision criteria
   - Specify constraints and boundaries

4. **Output Format** (when relevant):
   - Define structure explicitly
   - Provide format examples
   - Specify length or detail level

5. **Examples** (when clarifying):
   - Show desired patterns
   - Illustrate edge cases
   - Demonstrate style/tone

## Key Techniques Reference

### Foundation Techniques

**Role Setting**: Establish perspective when expertise or tone matters
- Effective for: Specialized knowledge, consistent voice
- Example: "As an experienced code reviewer, analyze..."

**Progressive Disclosure**: Start general, add detail as needed
- Effective for: Complex multi-part tasks
- Example: "First outline the approach, then implement each section..."

**Explicit Constraints**: Define boundaries clearly
- Effective for: Preventing unwanted outputs
- Example: "Limit response to 3 paragraphs, focus only on technical aspects"

### Advanced Techniques

**Chain-of-Thought**: Request reasoning before conclusions
- Use when: Logic and transparency matter
- Trigger: "Think step-by-step" or "Explain your reasoning"

**Few-Shot Learning**: Provide input-output examples
- Use when: Pattern is easier shown than explained
- Caution: 2-3 examples usually sufficient

**Self-Consistency**: Have model verify its own outputs
- Use when: Accuracy is critical
- Implementation: "Review your answer for errors and inconsistencies"

For detailed technique explanations and examples, consult:
- `references/techniques.md` - Comprehensive technique catalog
- `references/patterns.md` - Common prompt patterns
- `references/antipatterns.md` - What to avoid

## Collaboration Principles

### Be a Thought Partner, Not Just an Executor

- **Bad**: "Here's your prompt" (without understanding needs)
- **Good**: "Let me understand what you're trying to achieve first..."

### Question Assumptions Constructively

- Surface hidden requirements through dialogue
- Challenge unclear objectives respectfully
- Propose alternatives when original approach seems suboptimal

### Iterate Based on Feedback

- Start with minimum viable prompt
- Test and refine based on actual outputs
- Document what works and what doesn't

### Teach While Doing

- Explain why certain techniques work
- Share the reasoning behind design choices
- Help users understand prompt engineering principles

## References

This skill includes detailed reference documentation:

### references/
- `techniques.md` - Complete catalog of prompting techniques with examples
- `patterns.md` - Reusable prompt patterns for common scenarios  
- `antipatterns.md` - Common mistakes and how to avoid them
- `evaluation.md` - Comprehensive quality evaluation framework
- `examples.md` - Library of before/after prompt improvements

Consult these references for in-depth technical details and extensive examples not included in this overview.
