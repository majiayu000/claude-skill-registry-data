---
name: engineering-claude-context
description: Curates context, optimizes prompts with XML, and manages extended thinking for Anthropic Claude models. Use when building Claude-based agents, designing system prompts, or handling long-context tasks.
---

# Claude Context Engineering

## Instructions

Follow these strategies to maximize reliability and performance for Anthropic Claude models within limited attention budgets.

1.  **Curate High-Signal Context**
    *   Treat context as a finite resource; every token dilutes attention.
    *   Prune low-value information (e.g., repetitive logs, unused tool outputs).
    *   Use **"Just-in-Time" Retrieval**: Provide lightweight identifiers (file lists, summaries) initially, allowing Claude to load full details only when needed.

2.  **Structure with XML Tags**
    *   Use XML tags to strictly delineate prompt sections (Claude is optimized for this).
    *   Common tags: `<instructions>`, `<context>`, `<tools>`, `<examples>`, `<formatting>`.
    *   Nest tags for hierarchy (e.g., `<examples><example>...</example></examples>`).
    *   Reference tags explicitly in instructions (e.g., "Analyze the data in `<context>`").

3.  **Optimize for Long Horizons**
    *   **Compaction**: Periodically summarize conversation history to free up context while preserving key state (decisions, bugs).
    *   **Memory**: Implement an external "notebook" (e.g., `scratchpad.md`) where Claude reads/writes persistent state, freeing it from the context window.
    *   **Sub-Agents**: Delegate distinct, context-heavy sub-tasks to ephemeral sub-agents that return only distilled results.

4.  **Leverage Extended Thinking**
    *   Use for: Complex STEM problems, constraint optimization, and multi-step strategic frameworks.
    *   **Prompting**: Use open-ended, high-level instructions ("Think thoroughly about X") rather than rigid step-by-step constraints for reasoning.
    *   **Few-Shot**: Include `<thinking>` blocks in your examples to demonstrate the *reasoning process*, not just the final output.
    *   **Budget**: Start small (1024 tokens) and scale up for complexity (up to 32k+ with batch processing).

5.  **Design Token-Efficient Tools**
    *   Ensure tools return only necessary data (e.g., `grep` output vs. full file).
    *   Keep tool definitions clear and distinct to avoid ambiguity.

## Critical Rules

*   **No Brittle Logic**: Avoid hardcoding complex if/else chains in prompts; use examples ("pictures") to guide behavior instead.
*   **Don't Prefill Thinking**: Never prefill Claude's response when using Extended Thinking mode.
*   **Progressive Disclosure**: Don't dump all data at once. Let Claude discover information layer by layer (hierarchy -> summary -> detail).
*   **Clear Separation**: Always separate `System Instructions` from `User Data` to prevent prompt injection and confusion.

## Checklist

- [ ] **Tags**: Are distinct sections wrapped in XML tags?
- [ ] **Efficiency**: Is the initial context free of unnecessary bulk?
- [ ] **Retrieval**: Does Claude have tools to fetch details "just-in-time"?
- [ ] **Memory**: Is there a mechanism (compaction or external file) for long-term persistence?
- [ ] **Examples**: Do few-shot examples demonstrate the *reasoning* (if using thinking) or *format* required?
- [ ] **Thinking**: Is Extended Thinking enabled only for complex/planning tasks, not simple lookups?

## Detailed Guidance

For deep dives on context anatomy, compaction strategies, and extended thinking patterns, see [REFERENCE.md](REFERENCE.md).
