---
name: pstack-teach
description: "Explain a change or subsystem plainly, connecting how it works with evidenced reasons. Use when the user wants understanding rather than implementation or a comprehension quiz."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/teach
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Teach

Build understanding from the user's question and current knowledge.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Ground and explain

Trace the current code for mechanism. Consult relevant history for motivation. The pstack-how and pstack-why skills can supply these procedures when installed, but direct investigation with the same evidence standard is enough.

Start with the main point and a concrete example. Explain the flow as the person uses it, then the invariant, tradeoff, or failure case that matters. Use real symbols where they help rather than listing files.

Separate demonstrated behavior from inferred rationale. Keep uncertainty that reflects missing evidence. Match the user's language; no fixed English-only voice.

Give the smallest complete answer first. Deepen where the user asks or where the requested explanation needs it. A flow diagram helps when it reduces reading effort; use a text diagram or available visualization without requiring an image-generation provider.

## Boundaries

The deliverable is understanding, not edits, a quiz, or a gate on completed implementation. Use a separate explicitly requested comprehension workflow if the user wants one.
