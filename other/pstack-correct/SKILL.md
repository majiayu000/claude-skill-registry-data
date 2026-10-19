---
name: pstack-correct
description: "Turn recurring, evidenced repository mistakes into enforceable structure. Use when asked to prevent repeated errors with ownership, types, lint, or meaningful behavior checks."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/correct
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Correct

Fix demonstrated mistake classes at the strongest practical layer. One correction does not imply authorization to redesign the repository.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Find repeated mechanisms

Read the relevant corrections, commits, reverts, reviews, and current source. Group errors by mechanism. Require at least two demonstrated occurrences for a recurring class; treat a single incident as a case to investigate.

Separate product bugs, environment failures, stale instructions, and missing authorization. Their remedies differ.

## Choose enforcement

Prefer removing duplicate ownership or invalid construction when a narrow structural change solves the class. Otherwise use the existing type system, a targeted lint/CI check, or an observable behavior test.

Compare the enforcement cost with the demonstrated problem. A one-caller wrapper or runtime guard is not automatically wrong. Preserve externally used APIs and design-system consumers unless coordinated breaking changes are authorized.

For judgment that cannot be enforced, improve the relevant existing instruction rather than adding a second rules document. Repository or global policy edits require scope that includes them. Respect restrictions on creating tests and memory updates.

## Prove the mechanism

Use an isolated copy of a real past mistake to show that the enforcement rejects it. Show that the valid implementation still passes. Run required checks through the host's resource controls.

When implementation is authorized, make the smallest justified change. Do not auto-commit, create issues, or open PRs. When asked only for an audit, provide the concrete recommendation and evidence.

## Deliver

For each class, identify occurrences, chosen enforcement, rejected stronger options, rejection/acceptance evidence, and remaining gaps.
