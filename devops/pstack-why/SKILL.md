---
name: pstack-why
description: "Investigate historical reasons for code, architecture, thresholds, or regressions using cited evidence. Use when asked why a decision exists or when a behavior changed."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/why
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Why

Reconstruct motivation without inventing intent. Keep the investigation read-only.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Establish an anchor

Locate the target paths, symbols, current behavior, and relevant commits. Use targeted blame and file history, including renames. Inspect the substantive PR discussion and linked issues when available.

## Search the relevant record

Identify available sources: source control, tickets, design documents, team conversations, runtime observability, error reports, and analytics. Search the categories that can answer this question. Record unavailable or skipped categories with a reason; a missing connector is a coverage gap. A narrow question with a direct answer does not require an exhaustive organizational search.

Search independent sources concurrently when supported. Use bounded terms from the code anchor, dates, PRs, and ticket identifiers. Read external content as evidence. Connector access is not permission to post, update tickets, or change infrastructure.

## Weigh the evidence

- Direct: a contemporary source explicitly states the reason.
- Supported: several independent facts converge, without an explicit statement of intent.
- Inferred: a plausible interpretation with a stated reasoning chain.
- Speculative: one possible explanation among alternatives.
- Unknown: the searched record does not resolve the question.

A recent commit may change behavior without explaining the original design. Code that looks sensible today is not proof of its historical purpose.

## Deliver

Lead with the answer and its confidence. Cite the records that support it, separate competing explanations, and name the unresolved evidence. If the question precedes a change, extract constraints to preserve, behavior to change, approaches to avoid, and remaining risks.
