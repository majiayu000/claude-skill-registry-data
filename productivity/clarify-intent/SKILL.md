---
name: clarify-intent
description: Clarify a user request when its wording supports materially different intended outcomes that current context cannot resolve. Offer the most plausible options and accept a custom answer before dependent work. Use on an explicit invocation or when using-axiom selects this ambiguity boundary; do not trigger on tentative wording alone, routine implementation choices, or facts available through inspection.
---

# Clarify Intent

Turn a material ambiguity into a user decision while preserving the requested
outcome, constraints, and existing authorization.

Defaults you may adapt, saying so: question and option counts, how independent questions are batched, and wording. Every other rule here binds.

## Entry And Scope

- `using-axiom` may select this skill before choosing an action route when a request has multiple plausible meanings with different results, scope, targets, write surfaces, or authorization boundaries.
- Read the request and relevant conversation first. Inspect readily available task evidence when it can settle a factual gap without making the choice.
- Tentative phrases such as "maybe" do not alone require clarification. Keep working when the intended result is clear and an ordinary reversible implementation choice can be made within the user's constraints.
- Ask from need, not caution. The request, context, the user's environment, and inspection may settle facts and a delegated choice whose alternatives are all reversible and already authorized, never an undelegated choice between alternatives with different route sets, write surfaces, or authority or safety boundaries. Ask only for a material decision they leave open, never for reassurance or as a defensive pause.
- Do not use a question to reopen a settled decision or request authorization already established for the same action. A permission-bypass mode does not resolve an ambiguous intended result.

## Ask Focused Questions

1. Ask one concise, self-contained question per unresolved material decision. Ask independent decisions together, in one call when the host's question tool supports several questions; never split one decision into several questions.
2. Offer the distinct, plausible interpretations, usually two to four and within the host tool's limits, grounded in the user's words and current context. State the outcome or tradeoff of each; do not invent unrelated requirements to fill the choices.
3. Let the user enter a custom answer. Use the host's native question tool when available in the current mode and follow its option and free-text conventions. If that tool is unavailable, ask in ordinary conversation.
4. Recommend an option only when known user priorities support it and the host's question format calls for a recommendation. A default, recommendation, silence, or elapsed time is not a submitted decision; a delegated answer such as "choose one" counts only when every alternative is reversible and already authorized; then choose the one that fits the user's environment and goal, and say which and why before acting. An offered option authorizes no persistent system change, external or remote-state change, deletion, credential use, or material cost.
5. Wait before work that depends on a material choice. Continue authorized independent work when useful. Do not poll, repeat the same question, or manufacture additional interview rounds.

If there is only one plausible interpretation but a required value is missing,
ask for that value directly instead of manufacturing multiple choices. If the
host requires progress after an unanswered optional question, proceed only
with independent work or an assumption that stays inside established authority.

## Resume

Use the user's selected or custom answer to resolve only the open issue.
Preserve unaffected instructions and acceptance criteria. Return the clarified
request to `using-axiom` for normal route selection; the answer is not blanket
permission for edits, delegation, external actions, or persistent changes.

Do not run a downstream workflow merely because its option was displayed.
When the answer introduces a new material ambiguity, ask only the necessary
follow-up. Otherwise resume the task without restating a questionnaire.

## Acceptance Examples

| Request and context | Expected behavior |
| --- | --- |
| "Clean up the old records" without a target or retention meaning | Ask whether the user means archive, remove duplicates, or another intended cleanup; accept custom details before changes |
| "Maybe fix this typo" with one identified typo | Continue with the clear correction; tentative wording alone is not a trigger |
| The project's files settle a factual point, such as the build output folder | Use that fact, say so, and continue; do not ask for reassurance |
| "Export the report" with the destination and the file format both unresolved | Ask both independent decisions together, one question each, in one round |
| "Use either deployment destination" with different authority boundaries | Ask one destination question; do not pick an action route first |
| User answers "your call" and every option is reversible and already authorized | Choose the one that fits the user's environment and goal; say which and why before acting |
| User supplies a custom answer or corrects an option | Preserve that answer and reroute the resolved request |
| A permission-bypass mode with an unresolved target | Ask; execution permissions do not identify the intended target |
