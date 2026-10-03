---
name: explain-pr-step-by-step
description: Explain a pull request incrementally with concept teaching and confirmation gates between steps. Use when the user asks for a step-by-step PR walkthrough, what changed and why, or asks to pause after each step for deeper understanding.
---

# Explain PR Step by Step

Use this skill to teach a PR in guided, checkpointed steps.

## Goal

Produce a clear sequence of changes where each step includes:
- what changed,
- why it changed,
- the concept behind it,
- a pause question before moving on.

## Required workflow

1. **Collect PR evidence first**
   - Fetch PR metadata (title, summary/body, commits, files).
   - Fetch the full diff and per-file patches if needed.
   - Do not infer chronology without checking commit/diff evidence.

2. **Build a teaching sequence**
   - Group changes into understandable phases, typically:
     1) feature flag/config enablement,
     2) contracts/types,
     3) state domain/data flow,
     4) UI renderer,
     5) runtime registration/wiring,
     6) tests and safety updates.
   - Keep each step focused on one core idea.

3. **Deliver one step at a time**
   - For each step, include:
     - changed files/components,
     - behavioral outcome,
     - concept explanation (for example lifecycle, caching, hydration).
   - End each step with an explicit checkpoint question:
     - "Need more detail before we continue to Step N+1?"

4. **Honor drill-down questions immediately**
   - If user asks "where?", "show example", "what does X mean?", pause progression.
   - Provide concrete code references and minimal examples.
   - Resume next numbered step only after user confirms.

5. **Use collaborative language**
   - Prefer "we" and "our" phrasing.
   - Avoid over-abstract explanations detached from repo code.

## Concept teaching rules

- Always link concepts to concrete implementation, deriving examples from the PR's own diff. For example:
  - Feature flag -> rollout safety and gating behavior.
  - Schema/type change -> contract compatibility between producer and consumer.
  - New state field -> data flow and where the source of truth lives.
  - Lifecycle/status values -> what each state renders or triggers.
- Keep examples small and directly relevant to current files.

## Response template per step

Use this structure:

1. `Step N: <short title>`
2. `What we changed` (files and behavior)
3. `Concept` (plain-language explanation)
4. `Why this matters`
5. `Checkpoint question` ("Need more understanding before Step N+1?")

## Quality bar

- Steps must be accurate to the diff.
- Concepts must be technically correct and simple.
- User must control pacing; never dump all steps unless asked.
