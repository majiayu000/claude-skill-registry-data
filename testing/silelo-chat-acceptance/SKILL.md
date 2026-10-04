---
name: silelo-chat-acceptance
description: Verify SILELO-style chat rooms before delivery. Use when testing chat responses, loading and error states, source links, retry behavior, custom notifications, quick actions, and calculator safety in a browser-backed acceptance workflow.
---

# SILELO Chat Acceptance

## Scope

Use this skill to prove that a chat room works before reporting delivery. Keep it separate from `silelo-ai-studio-workflow`: this package is an acceptance-test capability, not a replacement for the broader implementation workflow.

## Required Acceptance Flow

1. Open the real chat route and confirm the baseline layout on desktop and mobile.
2. Send a short non-destructive message through the configured API. Observe pending/typing state and verify duplicate send prevention.
3. Confirm that a non-empty reply is rendered, message order is correct, and the result records the real provider only when a live request occurred.
4. Send a message containing an `http` or `https` URL. Verify that it becomes a keyboard-accessible link with `target="_blank"` and `rel="noopener noreferrer"`.
5. Verify an expected failure path with a safe mock or deliberately incomplete configuration. Confirm an actionable notification appears and can be dismissed.
6. Test retry or a fresh send after failure. Record only the behavior actually observed.

## Calculator and Quick Actions

For calculator UI, use a restricted parser or evaluator with an explicit grammar. Never pass user input to `eval`, `Function`, or a dynamically built executable expression. Allow only declared operators, enforce maximum input length, reject unbalanced parentheses and division by zero, and reject non-finite results.

Require every quick action—calculation, conversion, summary, or web search—to invoke a real handler and expose `pending`, `success`, and `error` states. Do not show a success notification for a placeholder or unfinished request.

## Evidence Standard

Use Vitest for pure helper and error-path tests. Use browser verification for interactive behavior. A screenshot alone is not a pass condition. Report one of: `live-tested`, `integration-tested`, `mock-tested`, or `not yet verified`.
