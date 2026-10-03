---
name: hig-content-states
description: "Improve interface language, terminology, feedback, and loading, empty, error, success, offline, and recovery states."
---

# Make the interface explain what is actually happening

Follow the [root contract](../../SKILL.md). Use [state-matrix.md](../../references/state-matrix.md). Relevant Apple context: HIG-012/020 and APPLE-004/005 in [Apple rule cards](../../references/apple-rule-cards.md). The state machine and writing tests here are WORKFLOW.

## Inventory the language in context

Inspect navigation labels, page titles, actions, field labels, helpers, validation, notifications, dialogs, and system-state messages. Read them in the actual flow, not as an isolated string spreadsheet. Identify whether a string describes a destination, action, object, state, or consequence.

Create a small terminology table: preferred term, meaning, rejected synonyms, and exceptions. Distinguish user-facing language from implementation names. Preserve recognizable product terms unless there is a documented comprehension problem.

Evaluate each label by prediction: after reading it, what would the user reasonably expect? Compare that expectation with the real result. Prefer an accurate longer label over a short ambiguous one. Remove redundant filler without removing prerequisites, consequences, or recovery instructions.

## Define state before copy

For every asynchronous or multi-step feature, write a state table with entry condition, visible content, allowed actions, accessible announcement, persistence, exit condition, and recovery. Derive copy from the system’s actual knowledge.

Distinguish these cases rather than mapping all of them to a blank screen:

- There is no content yet.
- The query or filters produced no matches.
- The user cannot access the content.
- The request has not finished.
- Some content is available but another part failed.
- Data is cached, stale, offline, or awaiting synchronization.
- An operation succeeded, failed, or has an unknown outcome.

Do not display a success message just because the user clicked a button. Do not call an uncertain write a failure if it may already have reached the server. Offer reconciliation or safe status checking where the operation requires it.

## Feedback and loading

Keep the useful stable context visible while a local section loads. Reserve skeletons for predictable structure; do not replace real content unnecessarily or show placeholders that imply invented data.

Use determinate progress only when the application can represent meaningful progress. Do not fabricate percentages or estimated completion times. Make cancellation available when supported and safe; explain what cancellation does to already-completed work.

Prevent repeat activation from duplicating a transaction. Mark the action’s actual busy state rather than freezing unrelated work. Test immediate completion, extended delay, timeout, partial response, cancellation, and responses arriving out of order.

## Errors and recovery

Write failures around three questions: what happened, what is affected or preserved, and what can the user do next? Add technical identifiers only when useful for support, and avoid exposing secrets or raw internal details.

Keep field-level problems close to the field and provide an accessible relationship. For multi-error forms, provide a discoverable route through the errors. Preserve valid input. Do not suggest retry when retry cannot help, or tell the user to contact support without a working path.

Reserve interruptive messaging for decisions that require it. A persistent action outcome may need a durable receipt or history entry rather than a transient toast. Do not hide the only recovery action inside an auto-disappearing message.

## Tone and localization

Match tone to consequences. Friendly copy should not trivialize lost work, denied access, money, health, or privacy. Do not use shame to discourage cancellation or refusal. Do not add exclamation marks to manufacture reassurance.

Test long translations, plurals, dates, numbers, currencies, user-generated names, mixed scripts, and right-to-left layouts. Avoid assembling sentences from fragments that assume English grammar. Keep source strings and terminology maintainable in the project’s existing localization system.

Consider whether supporting text is read before, during, or after a decision. Move the explanation to the moment it can prevent a mistake instead of adding another onboarding screen.

## Output and gate

Deliver a before/after string table with context and rationale, terminology decisions, and the complete state contract for changed flows. Pass only when messages reflect actual state, the user can take the promised action, sensitive input is preserved appropriately, and adverse states have tested recovery paths.
