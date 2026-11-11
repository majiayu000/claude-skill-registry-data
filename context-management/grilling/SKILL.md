---
name: grilling
description: Grill the user through a dependency-ordered design tree, present the resolved plan for approval, then turn the approved plan into tickets. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

# Grilling

Interview the user until every relevant branch of the decision tree is resolved. The result is an approved plan and a set of tickets, not product-code changes.

## Invariants

- **Facts are the agent's job.** Resolve anything available from the repository, tools, documentation, or external research. Never ask the user for a fact you can find.
- **Decisions are the user's job.** Ask rather than silently choosing a load-bearing product, scope, or trade-off decision.
- **Dependencies determine order.** A question is ready only when every answer it depends on is settled.
- **Every question carries a recommendation.** The user should be approving or redirecting an informed choice, never choosing from a blank slate.

## Durable session state

Every grill MUST keep recoverable state in the current project at `.work/grilling/<grill-name>/`. Derive a short, filesystem-safe semantic name from the subject. Reuse that name when resuming the same grill.

Before creating a session, inspect `.work/grilling/`. If the intended name already exists, read its `state.md` and resume it only when its objective matches; otherwise choose a distinct name. If the session name is missing from conversational context, inspect the existing checkpoints and recover the one whose objective matches instead of creating a duplicate.

`state.md` is the authoritative checkpoint, not conversational memory. At the start of every grilling turn, read it before processing the user's latest input. If it already exists, resume from it; never rebuild or overwrite settled state from memory. Create it before the first question with these sections:

- status and exact next action;
- problem and desired outcome;
- current-state evidence with repository paths or external sources;
- settled decisions, their stable question IDs, exact answers, and rationale;
- constraints and non-goals;
- the complete decision tree, including dependencies and each node's status;
- the current frontier;
- plan feedback and its disposition.

Keep `state.md` concise and self-contained; do not copy the conversation into it. Put only bulky evidence extracts in an optional `research/` directory beside it, and link them from `state.md`.

Checkpoint in this order:

1. Persist new research, the design tree, and the current frontier before calling `ask` or presenting fallback questions.
2. When answers return, persist the exact selected option or custom answer and the resulting settled decision before doing further research or recomputing the tree.
3. Update the checkpoint after every later fact-finding result and every round of plan feedback.
4. Re-read and reconcile the checkpoint immediately before drafting the final plan and before materializing tickets.

Use the same stable semantic ID for a decision-tree node, its `ask.id`, and its entry in `state.md`. If an answer changes, retain the prior answer as superseded, record the replacement, and reopen or invalidate every dependent node. Never silently delete decision history.

If the user cancels a question round, record the session as paused before stopping. If the plan is dismissed, record it as dismissed. After ticket creation, record it as ticketed and include the final plan and ticket paths.

## 1. Map the design tree

Map decisions as a tree: every answer may expose decisions that hang from it. The **frontier** is the complete set of unresolved decisions whose prerequisites are already settled. Give every node a stable semantic ID and record the initial tree in `state.md`.

Research factual prerequisites before computing the frontier. If research for one branch is still running, leave that branch blocked and continue with any independent ready branches. Delegate independent fact-finding only when useful; do not make the user do it.

## 2. Ask one frontier per round

Before asking, checkpoint the complete current frontier and its recommendations in `state.md`. When the `ask` tool is available, MUST use it instead of printing a wall of questions in chat. Make one `ask` call containing every question on the current frontier. The Work App presents a multi-question call as a step-by-step wizard with a review screen.

For every question:

- Use a stable semantic `id` and a short `header`.
- State the decision and the relevant constraint or trade-off in `question`.
- Offer 2–5 concrete options. Put concise consequences in each option's `description`.
- Set `recommended` to the zero-based index of the recommended option.
- Set `multi: true` only when more than one option can validly apply.
- Do not add a redundant “Other” option; the tool already permits a custom answer.

A question whose answer depends on another open question does not belong in the same call. If the user cancels the tool, mark the checkpoint paused and stop without guessing or advancing the tree.

Only when `ask` is unavailable, fall back to numbered chat questions. Include the choices and a clearly labelled recommended answer for each question, then wait for all answers in that frontier.

## 3. Recompute the frontier

Apply the answers to `state.md` first, then reshape the tree, research any newly exposed factual prerequisites, and ask the next frontier. Repeat until the frontier is empty: every relevant branch has been visited and nothing remains silently assumed.

Do not ask for a separate “shared understanding” confirmation. The final plan is the confirmation and approval gate.

## 4. Present the resolved plan

Before drafting the plan, MUST re-read `state.md`, then read `skill://to-tickets`. It is hidden from automatic model matching, so the explicit read is required. Use the checkpoint as the source of truth for the resolved design and use the current `to-tickets` exploration, vertical-slice, blocking-edge, and final verify-and-fix rules to draft the ticket breakdown that appears in the plan.

The plan must be self-contained and include:

- the problem, desired outcome, and relevant current-state evidence;
- every settled decision and constraint;
- the implementation approach, scope, non-goals, risks, and verification;
- a numbered ticket breakdown showing each title, blockers, and complete behavior delivered.

There must be no unresolved decision in the plan. If synthesis exposes one, return to `ask`, resolve it, and regenerate the plan.

When the `plan` tool is available, MUST write the required self-contained HTML under `.work/plans/<slug>/` and call `plan`. Handle its result as follows:

- **Feedback or reply:** record the feedback and its disposition in `state.md`, incorporate it, reopen the design tree if it introduces a decision, and present the revised plan again.
- **Dismissal:** mark `state.md` dismissed and stop. Do not create tickets.
- **Approval:** continue immediately to ticket creation below.

Only when `plan` is unavailable, present the same plan in chat and obtain explicit approval there. Use `ask` for that approval when it is available.

## 5. Materialize the approved tickets

Plan approval also approves the exact ticket breakdown shown in that plan. Continue under the loaded `to-tickets` skill, treating its ticket-breakdown quiz and approval step as already complete. Do not ask for a second ticket approval.

Re-read and reconcile `state.md`, then follow the current `to-tickets` instructions to write the ticket files and return its implementation handoff. After writing them, mark the grilling session ticketed and record the final plan and ticket paths. If the plan tool's generic approval result says “Implement it now,” this workflow overrides that wording: create tickets only. Do not edit product code or invoke `implement-tickets`.

Stop after the `to-tickets` handoff prompt.
