---
name: optimizing-llm-prompts
description: Refine and structure prompts for LLMs to ensure clarity, reliability, and optimal performance. Use when writing system prompts, complex instructions, or debugging agent behaviors.
---

# Optimizing LLM Prompts

## Instructions

Follow these steps to create robust and effective prompts for LLMs (specifically Claude).

1.  **Define the Goal**: Clearly identify the desired output and behavior. Be specific about format, tone, and constraints.
2.  **Structure with XML**: Use XML tags to delineate sections.
    *   `<system>`: High-level role and identity.
    *   `<context>`: Static background information.
    *   `<rules>`: Specific constraints and instructions.
    *   `<examples>`: Few-shot demonstrations.
3.  **Draft Instructions**:
    *   Use **imperative voice** ("Do this", not "You should").
    *   **Quantify** everything (e.g., "3 sentences" not "concise").
    *   Use **positive framing** (what to do, not just what not to do).
4.  **Add Examples**: Provide 1-3 examples of input -> output mapping to "show" the model what you want.
5.  **Iterate**: Test with edge cases. If the model fails, add a specific rule or example to address that failure mode.

## Best Practices Summary

*   **XML Structure**: Essential for Claude to distinguish between instructions and data.
*   **Chain of Thought**: Ask the model to "think step-by-step" before answering complex queries.
*   **Progressive Disclosure**: Don't dump all context; allow the model to request more if needed.
*   **Input Sanitation**: Wrap user input in distinct tags (e.g., `<user_query>`) to prevent prompt injection.

## Checklist

- [ ] **Structure**: Are sections clearly separated (XML/Headers)?
- [ ] **Clarity**: Are instructions imperative and quantified?
- [ ] **Safety**: Is there a catch-all override for conflicting user requests?
- [ ] **Examples**: Are there few-shot examples for complex behaviors?
- [ ] **Context**: Is static context separated from dynamic user queries?
- [ ] **Output**: Is the output format explicitly defined (JSON, Markdown, etc.)?

## Detailed Guidance

For a deep dive on critical rules, forbidden practices, and optimization patterns, see [REFERENCE.md](REFERENCE.md).
