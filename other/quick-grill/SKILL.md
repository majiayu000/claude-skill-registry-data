---
name: quick-grill
description: Clarify a task and pause for plan approval before execution. Use only when the user explicitly requests Quick Grill.
---

# Quick Grill

Run a short preflight before doing the user's requested work. Clarify just enough to avoid misframing; do not turn the session into a long interview.

## Core Behavior

Do not execute the task immediately.

First identify:

- the likely goal
- the expected deliverable
- the main constraints
- any hidden risk, ambiguity, or authority issue
- whether the next action is obvious enough to propose directly

If a question can be answered by inspecting local files, repo context, attached material, or available docs without meaningful cost, inspect that source instead of asking the user.

## Questioning

Use the available question tool for design or scope preferences when its contract permits it. Otherwise ask a concise plain-text question. Request plan approval through the environment's permitted approval mechanism, using plain text when a question tool is preference-only.

Ask at most three questions in the first round. Prefer one or two when enough.

For each question:

- make it specific to the user's prompt
- provide 2-3 concrete options
- put the recommended option first and mark it as recommended
- explain the tradeoff in each option description
- avoid generic discovery questions unless the task truly lacks direction

Continue with another short round only if a material blocker remains after the user's answers.

## Clear Tasks

If the prompt is clear enough, still pause before execution.

Present a concise plan and ask for any missing approval. Existing explicit approval of the unchanged plan remains valid, so do not repeat the preflight after approval.

Keep the plan short. State the intended result, material scope boundaries, and relevant verification.

## Output Shape

Before approval, respond with:

1. a brief preflight summary
2. focused questions, or a yes/no approval request
3. a recommended path

After approval, proceed normally and execute the task end to end unless the user redirects.

## Guardrails

Do not ask questions for routine details the model can reasonably decide.

Do not perform file edits, commits, destructive commands, deployments, purchases, or external side effects before approval.

For high-risk work, make the risk visible and ask for explicit approval.

For simple low-risk work, use one short preflight followed by one approval question, then execute.
