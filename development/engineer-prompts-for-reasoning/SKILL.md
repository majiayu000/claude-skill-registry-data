---
name: engineer-prompts-for-reasoning
description: >-
  Write or fix a prompt for a reasoning model (Gemini Pro, GPT-4o, Claude
  Sonnet) so it holds context across a multi-step task. Use for any request to
  draft, structure or debug such a prompt. Not for fast models (use
  engineer-prompts-for-instant).
---

# HOW TO WRITE PROMPTS FOR REASONING MODELS

This guide helps you get the best out of "smart" models (like Gemini 1.5 Pro,
Claude 3.5 Sonnet, GPT-4o). These models are capable of complex logic, coding,
and creative work, but they need **Context** and **Structure** to stay on track.

## 1. THE CORE CONCEPT: "STRUCTURED CONTEXT"

Reasoning models thrive when you organize information clearly. Think of it like
briefing a senior colleague. You don't just give an order; you explain the
**Background**, the **Goal**, and the **Constraints**.

We use **XML-style tags** (like `<context>`, `<rules>`) to help the model
understand the structure of your prompt.

## 2. THE REASONING FRAMEWORK (BEGINNER TEMPLATE)

Copy this structure for complex tasks.

```markdown
# ROLE

You are an expert [Role Name].

# GOAL

<objective>
[Clearly state what you want to achieve in 1-2 sentences]
</objective>

# CONTEXT (The "Why" and "What")

<context>
[Provide background info. Who is the audience? What is the current state? What are the definitions?]
</context>

# RULES & CONSTRAINTS

<rules>
1. [Constraint 1 - e.g., Code style]
2. [Constraint 2 - e.g., Word count limit]
3. [Constraint 3 - e.g., "Do not use external libraries"]
</rules>

# INSTRUCTIONS (The "How")

<instructions>
1. First, analyze the request and the context.
2. Think step-by-step about the best approach.
3. [Specific Step 1]
4. [Specific Step 2]
5. Output the final result in [Format].
</instructions>
```

## 3. KEY TECHNIQUES FOR BEGINNERS

### A. Use XML Tags for Clarity

Tags like `<context>`, `<code_snippet>`, `<examples>` help the model separate
different parts of your prompt. It prevents the model from getting confused
between instructions and data.

### B. Ask for a Plan First

For coding or writing tasks, ask the model to outline its plan or "think" before
generating the final output.

- **Prompt:** "Draft a plan in `<plan>` tags, then write the code."
- **Why:** It catches misunderstandings early.

### C. Define Success Criteria

Tell the model exactly what "good" looks like.

- "A successful response will cover all edge cases and pass the linter."
- "A successful response will be friendly but professional."

## 4. EXAMPLE: CODE REFACTORING

```markdown
# ROLE

You are a Senior TypeScript Engineer.

# GOAL

<objective>
Refactor the provided legacy function to be more readable and performant.
</objective>

# CONTEXT

<context>
This function is part of a high-traffic e-commerce checkout. It handles cart validation.
We are moving to functional programming patterns.
</context>

# RULES

<rules>
1. Use arrow functions.
2. Add JSDoc comments.
3. Do not change the external API signature.
4. Return early to avoid deep nesting.
</rules>

# INPUT CODE

<code_snippet> function validate(cart) { // ... messy code ... } </code_snippet>

# INSTRUCTIONS

<instructions>
1. Analyze the complexity of the current function.
2. Refactor step-by-step.
3. Explain why the new version is better.
</instructions>
```

## 5. CHECKLIST FOR SUCCESS

Before sending your prompt, ask yourself:

1. **Role:** Did I say _who_ the AI is?
2. **Context:** Did I explain _why_ we are doing this?
3. **Format:** Did I specify _how_ the output should look?
4. **Tags:** Did I use `<tags>` to organize big blocks of text?
