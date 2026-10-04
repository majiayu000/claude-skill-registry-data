---
name: grill-me
description: Relentlessly stress-test a plan or design through a one-question-at-a-time interview that researches available context first and includes a recommended answer with every question. Use when the user asks to "grill me", wants a plan/design challenged, or needs decisions resolved before implementation.
---

# grill-me

Interview the user relentlessly about a plan, design, or implementation direction until there is shared understanding. Walk the decision tree branch by branch, resolve dependencies between decisions in order, and keep pressure on vague or untested assumptions.

## When to Use

- The user says "grill me" or asks to be challenged on a plan/design.
- A feature plan, architecture decision, PRD, or implementation approach needs stress-testing before work starts.
- The next useful step is not coding yet, but reducing ambiguity and surfacing missing decisions.

## Ground Rules

1. Research before asking. Inspect available context first: the conversation, provided files, `bd show <id>`, alignment docs, `knowledge/`, existing plans, relevant code, and tests.
2. Do not ask questions that the codebase or supplied context can answer. Answer those through exploration and add the result to the shared understanding.
3. Ask exactly one user-facing question per turn. Do not batch questions, even when several are obvious.
4. Every question must include your recommended answer and a brief reason for that recommendation.
5. Traverse the decision tree deliberately. Resolve upstream choices before dependent branches.
6. Keep a running shared-understanding summary with confirmed facts, assumptions, decisions, open questions, risks, and next steps.
7. Be relentless about ambiguity, but stay constructive. The goal is decision quality, not debate for its own sake.

## Process

### 1. Establish the Target

Identify the plan or design being grilled. If the target is already clear from context, do not ask the user to restate it. Summarize the target in one or two sentences before the first question.

### 2. Explore Answerable Context

Before asking anything, gather enough context to avoid wasting the user's attention.

Use the appropriate read-only sources for the situation:

- Current conversation and attached files.
- Beads issue details with `bd show <id>` when a task is named.
- Alignment or contract documents when provided.
- Relevant `knowledge/` YAML files.
- Existing plans under `plans/`.
- Related source, tests, scripts, or docs.

Record discovered facts in the running summary. If exploration answers a likely question, state the answer instead of asking it.

### 3. Build the Decision Tree

Privately map the main branches:

- Goal and success criteria.
- Users, stakeholders, and failure modes.
- Scope boundaries and non-goals.
- Data model, interfaces, dependencies, and migration concerns.
- Test strategy and verification evidence.
- Operational, security, performance, and maintainability risks.

Start with the branch that blocks the most other decisions.

### 4. Ask One Question

Use this format for every user-facing question:

```md
Shared understanding so far:
- Confirmed: <facts discovered from context or prior answers>
- Assumption: <current working assumption, if any>
- Open risk: <risk this question addresses>

Question:
<one question only>

Recommended answer:
<the answer you recommend>

Why:
<brief rationale and consequences>
```

The question may include choices, but it must still ask for one decision. If the user accepts the recommended answer, apply it and move to the next branch. If the user rejects it, update the shared understanding and follow the implications.

### 5. Maintain Shared Understanding

After each answer:

1. Add or update the relevant confirmed fact, assumption, decision, risk, or next step.
2. Note any dependent branch unlocked by the answer.
3. Ask the next single question with a recommended answer.

Do not restart the interview from scratch unless the user changes the target.

### 6. Finish the Grill

Stop when the important branches are resolved, the user asks to stop, or the remaining uncertainty is explicitly accepted.

End with a concise shared-understanding summary:

- Confirmed facts.
- Decisions made.
- Assumptions being carried forward.
- Open questions or accepted risks.
- Recommended next steps.

If the result should become an implementation plan, PRD, or Beads issue, say so and name the appropriate follow-up skill or workflow.
