---
name: pstack-how
description: "Trace how a subsystem works or where a responsibility belongs. Use for code walkthroughs, ownership questions, or understanding a cross-layer flow before changing it."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/how
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# How

Produce a working mental model grounded in the current code. Stay read-only unless the user also requests implementation.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Trace the flow

1. State the bounded question and locate the existing feature map, entry point, domain types, and relevant local instructions. Verify documentation against code.
2. For a narrow question, trace directly. For a broad subsystem, split into distinct angles such as user entry, state ownership, service contract, persistence, and permissions. Use separate readers only when useful and permitted.
3. Follow one concrete input through the real call chain to its output or side effect. Name the owner of each important decision and each boundary crossed.
4. Check the relevant empty, invalid, failed, concurrent, or permission-dependent branch. Search consumers outside the named folder when ownership or shared APIs are involved.
5. Read the actual cited files before synthesizing. A worker's summary is evidence to check, not proof.

## Deliver

Explain what it does, the control and data flow, where responsibilities live, and the gotchas that affect the user's question. Cite verified paths and symbols. Distinguish source inspection from executed behavior. Historical motivation needs historical evidence; infer no author intent from code alone.
