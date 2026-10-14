---
name: plan-mode-teach
description: Teach a concept or method so the user can apply it. Use when the user asks to learn, understand how something works, or work through an unfamiliar idea.
license: MIT
---

# Teach

Build a usable mental model, not a glossary entry.

1. Infer what the user already knows from their question and context. Start with the answer or central mechanism; do not gate the explanation behind an interview.
2. Walk through one concrete example, showing the key step or causal link at each stage. Define unfamiliar terms at first use and distinguish a helpful analogy from the real mechanism.
3. Explain where the model stops working: an important exception, common misconception, or boundary that would cause a wrong application.
4. Give the user a nearby case they can now reason through, or a brief check question when an interactive lesson is welcome. Adapt to their response rather than repeating the same explanation.

The lesson is complete when the user has an explanation and an example they can transfer to a similar case. Match depth to the question; a narrow question can have a short lesson.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
