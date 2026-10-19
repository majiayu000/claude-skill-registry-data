---
name: pstack-blast-radius
description: "Analyze what a change can break outside its diff and verify the critical safety assumptions. Use for impact analysis, shared component changes, API migrations, permissions, or risky reviews."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/blast-radius
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Blast radius

Find the breakage that a symbol search alone misses. Keep reviews read-only unless fixes are requested.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Establish what changed

Record the exact base and head, plus whether the worktree is dirty. Read the intended behavior and the effective change, including altered defaults, removed guarantees, and unchanged-looking consumers.

Trace callers and dependencies, then cross representations: DTOs, persisted data, wire formats, other languages, feature flags, time zones, permissions, background jobs, lifecycle ordering, and installed library versions. Inspect relevant dependency source when the safety claim relies on its behavior.

## Prove the critical assumption

Find the one or two facts on which the change's safety depends. State a falsifiable example. Advance the proof as far as the authorized environment allows:

1. Cite the current implementation.
2. Trace the failure case and explain why it is reachable or excluded.
3. Run a focused check against real code.
4. Exercise the affected path in the running application.

Prefer existing checks. Add a script or test only when it provides meaningful evidence and is within scope. Respect instructions limiting tests or reruns. A production hypothesis does not authorize production writes.

## Deliver

Report confirmed risks, checked-and-cleared cases, and unproven assumptions separately. Each risk needs its triggering condition, mechanism, affected consumer, evidence, and practical impact. Avoid numerical probabilities without data.

Green compilation or CI does not prove compatibility with existing data or hidden consumers. Call out unavailable database, browser, or provider validation. Recommend the cheapest remaining check without widening the work.
