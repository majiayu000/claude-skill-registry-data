---
name: interview-me
description: Use when the user explicitly asks for a one-question-at-a-time intent interview before planning or implementation, such as "interview me", "help me clarify what I actually want", or "grill me". Do not use for ordinary underspecified implementation requests, direct fixes, explanations, mechanical work, or reliability review of an existing decision.
---

# Interview Me

Clarify product intent before planning or implementation when the user explicitly asks for an interview. The output is a confirmed intent statement in the conversation, not a spec, plan, task list, or automatically persisted artifact.

## First Decision

Use this skill only when the user clearly requests the interview itself, for example:

- "Interview me before we plan this."
- "Help me clarify what I actually want."
- "Grill me one question at a time about this idea."

Do not activate it merely because an implementation request is vague. For an ordinary underspecified request, stay in the base flow and ask the smallest question that changes the outcome, scope, risk, or approach. Direct fixes, explanations, mechanical operations, and already-settled plans stay with their existing owners.

If the user is challenging an existing plan, conclusion, source, or direction with wording such as "are we sure?" or "stress-test this decision," use `reliability-check` or `review-and-finish` as applicable instead of reopening product-intent discovery.

This skill needs a live, responsive user. In CI, a scheduled run, `/loop`, or another non-interactive context, report that the interview cannot proceed and do not guess, write an intent file, or invent confirmation.

## Process

### 1. State the current hypothesis

In the first interview turn, state one sentence describing the current read and an honest confidence number:

```text
HYPOTHESIS: You want <current best read of the underlying outcome>.
CONFIDENCE: ~<0-100>% — missing: <the material detail that could change the direction>.
```

Give a reason whenever confidence is below roughly 70%. Treat the number as an uncertainty signal, not as a universal approval threshold.

### 2. Ask one focused question with a guess

Ask exactly one question, then wait for the user's answer:

```text
Q: <one focused question>
GUESS: <the answer you currently expect and why; make it easy to correct>
```

Choose the next question from the material gaps in outcome, user, why now, success, constraint, and out of scope. Do not ask a batch of questions or silently fill a gap that could change the work. Update the hypothesis and confidence after each answer when the read changes.

### 3. Probe stated ideals when needed

If the user answers with a convention, best-practice phrase, or value such as "scalable", "modern", "clean architecture", or "the standard approach" instead of an observable outcome, ask what they would actually want if they did not need to justify it. Use this probe only when the answer could change the intended result; do not challenge ordinary preferences for its own sake.

### 4. Restate the intent

When the material gaps are resolved, write a short, line-by-line restatement using the user's language where possible:

```text
Here is what I now think you want:

- Outcome:      <what should change>
- User:         <who benefits or uses it>
- Why now:      <the current reason or trigger>
- Success:      <how the result will be recognized>
- Constraint:   <the binding limit or non-negotiable>
- Out of scope: <what is explicitly not being built or changed>

Yes / no / refine?
```

Keep the fields that materially constrain the next decision, but do not omit out of scope when it is relevant. The restatement is an intent check, not permission to begin implementation.

### 5. Confirm without inventing agreement

Treat an explicit, specific yes to the restatement as confirmation. If the user corrects it, incorporate the correction and restate it. If they say "whatever you think", "sounds good", or another ambiguous assent, ask one focused follow-up rather than claiming that intent is confirmed.

Stop when the restatement is sufficient to guide the user's requested next decision and the next material question is predictable. Do not keep interviewing to reach a numeric confidence target. If several rounds do not resolve a foundational gap, report the unresolved point and stop instead of grinding or guessing.

## Output And Handoff

The default output is the confirmed intent statement in chat. Do not automatically:

- create `docs/intent/[topic].md` or any other path;
- write a spec, plan, task list, issue, or decision map;
- invoke another skill, fan out agents, commit, push, publish, or create a PR.

If the user explicitly requests the next step after confirmation, leave this skill and use the smallest applicable owner: `plan-work` for implementation planning, `design-codebase` for an unresolved architecture boundary, `issue-workflow` for a requested tracker artifact, or the ordinary implementation flow for a settled direct change. Persist the intent only when the user explicitly asks and names or approves the exact target path.

## Verification

After an interview, check that:

- the user explicitly requested intent discovery and the context was interactive;
- the first interview turn included `HYPOTHESIS` and `CONFIDENCE`, with a reason for material low confidence;
- every question was singular, focused, and paired with a visible `GUESS`;
- a want-versus-should probe was used when a convention or best-practice answer concealed the desired outcome;
- the restatement covered the material parts of Outcome, User, Why now, Success, Constraint, and Out of scope;
- confirmation was explicit, or the result is clearly marked unconfirmed;
- no automatic file, handoff, plan, task, downstream invocation, or side effect was introduced.

## Boundaries

This skill clarifies intent; it does not own architecture, implementation planning, tracker publication, reliability reassessment, review, or branch actions. A vague request alone is not permission to start it, and an intent confirmation is not authorization for a durable artifact or external action.
