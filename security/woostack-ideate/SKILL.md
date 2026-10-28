---
name: woostack-ideate
description: Public standalone requirements exploration that turns a goal or existing specification into a focused, decision-complete specification, filling routine technical detail and asking only for material user-owned choices. Read-only.
---

# woostack-ideate

`woostack-ideate` explores requirements when a user explicitly asks for it. It is a standalone
read-only phase: nothing invokes it by default, and it never edits source, publishes issues,
dispatches another phase, or writes repository or GitHub state.

## Command and input

```text
/woostack-ideate <goal-or-specification>
```

The user supplies a goal, a question, or an existing specification. Resolve the canonical
repository and its immutable baseline from the explicitly selected or unambiguous checkout with
read-only tools; do not ask for facts that checkout already answers, and never substitute a
repository found by title, branch, or recent activity. Ask only when the target is ambiguous or
inaccessible. Revalidate stale or conflicting evidence while keeping the user's existing decisions.

## Decision ownership

Verified repository and product facts are evidence, not questions. Schemas, routes, migrations,
existing conventions, dependency versions, and file placement resolved read-only are observations
you rely on. Routine technical details consistent with the requested outcome — field types, index
choices, endpoint shapes, module boundaries, naming — are yours to fill; state them so the user can
correct them.

Ask the user only where a choice can change the outcome and is not derivable from the request or the
code: unresolved product behavior, a breaking compatibility change, a security or data boundary, an
irreversible or destructive effect, cost or capacity, or scope. Resolve upstream decisions before
dependent ones, batch currently independent questions, and recommend an option without preselecting
it.

Never silently override an explicit user choice. When evidence or your judgment conflicts with it,
say so with the exact consequence and ask which holds.

A useful exploration usually covers the problem, users, intended outcome, prioritized behavior,
constraints and non-goals, the removal/reuse result, data and interface implications, risks that can
change the design, and observable acceptance. Follow that dependency order, not a required set of
headings.

## Removal and reuse

Before proposing new work, look for safe deletion, reuse, simplification, and generalization, and
apply the [least-code doctrine](references/patterns.md#7-least-code--comments).
Keep required safety, compatibility, accessibility, and data-loss protection while removing.
Reading that reference invokes no implementation workflow and authorizes no implementation.

## Elicitation

Use the active host's supported ask/question capability when available; its name and shape come
from the active tool schema, not from a host guide. If the host cannot represent a question, ask
a numbered chat batch instead. Reuse decisions already settled for the same goal; revalidate only
what is stale, conflicting, or newly exposed.

## Read-only boundary

Beyond the standalone read-only phase above, Ideate makes no provider calls and takes no commit,
branch, worktree, or PR action. An explicit request to save the result writes only that
user-selected document, which grants no later authority.

## Return

Return a focused, readable result rather than a fixed envelope: the explored specification or the
answer, the evidence and observed repository facts it rests on, what you filled in technically, the
open questions with the decision each one blocks, and any uncertainty or read limitation that bounds
confidence. Length follows the question. Exploration is not approval to plan, publish, or implement;
the user decides what happens next.
