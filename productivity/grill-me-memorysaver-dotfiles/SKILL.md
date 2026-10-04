---
name: grill-me
description: Stress-test a user's plan or design by interviewing them through the decision tree until shared understanding is reached. Use when the user wants to be grilled, stress-test a plan, sharpen a design, or mentions "grill me".
license: MIT
version: 0.1.0
homepage: https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me
compatibility:
  claude-code: supported
  codex: supported
  pi-agent: supported
metadata:
  upstream: mattpocock/skills/skills/productivity/grill-me
---

# Grill Me

Interview the user relentlessly about their plan until there is shared understanding.

## Workflow

Ask one question at a time. Walk down each branch of the design tree and resolve dependencies between decisions one by one.

For each question, include the recommended answer so the user can react to a concrete position instead of starting from a blank page.

If a question can be answered by exploring the codebase, inspect the codebase instead of asking the user.

## Question Style

Keep questions specific, consequential, and grounded in the user's stated goal. Prefer questions that expose tradeoffs, hidden assumptions, missing constraints, failure modes, sequencing risks, or ownership boundaries.

When the user answers, summarize the decision in one sentence, then move to the next unresolved branch.

Stop when the major branches are resolved, the remaining unknowns are explicit, and there is a clear next action.
