---
name: pstack-interrogate
description: "Perform an adversarial review with independent passes using the active chat model. Use when asked to challenge a diff, find blind spots, or stress-test a design; return findings without applying fixes."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/interrogate
  upstream-commit: e5136d82418d2db3165ea1050d17577cd618cc05
  adaptation: portable-chat-inherited
---

# Interrogate

Challenge the intended contract with concrete failure cases. The deliverable is a review verdict.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Frame the review

Record exact base and head, dirty state, user intent, applicable instructions, and the relevant surrounding source. Preserve active checkouts. Confirm the base rather than assuming a main branch.

## Independent review

If supported and authorized, run two fresh read-only reviewers with the same intent, diff, context, and rubric. They use the active chat model without overrides. Their outputs stay separate until synthesis.

If delegation is unavailable or inheritance cannot be guaranteed, perform explicit sequential review passes and label them as self-review. Do not describe them as independent reviewers. This adaptation deliberately lacks cross-model diversity; same-model agreement is not independent confirmation of truth.

Apply the rubric in [references/rubric.md](references/rubric.md). Trace every suspected defect through the real inputs and call chain. Broaden source inspection to relevant consumers, not unrelated changes. Reviewers do not edit files, post comments, or run state-mutating live operations.

## Lead judgment

Read and verify each finding against current artifacts. Deduplicate by mechanism. Keep lone findings when their proof is sound. Agreement helps prioritize checking; it is never the acceptance rule. Record disagreements and the evidence resolving them.

Classify findings as act on, consider, noted, or dismissed. A blocking finding requires a concrete trigger, bad result, affected path, and evidence. Separate observations from unverified concerns. Missing test infrastructure is a gap, not proof of a product bug.

## Deliver

Lead with actionable findings ordered by practical impact, with tight source references and reproductions where available. Summarize reviewed scope, performed verification, and limitations. State when no actionable issue was found. Leave fixes and public review comments for the user's authorized request.
