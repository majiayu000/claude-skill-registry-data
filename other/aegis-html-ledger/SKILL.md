---
name: aegis-html-ledger
description: 'Use when project execution needs durable local checkpoint state. USE FOR: "HTML checkpoint ledger", "project resume ledger", "proof-gap ledger". DO NOT USE FOR: "standalone design page", "canonical architecture doc", "tiny one-shot answer".'
disable-model-invocation: true
---

# Aegis HTML Ledger

Use this skill to maintain durable project state without flooding chat.

## Contract

- Prefer the repo's existing progress or checkpoint surface when it exists.
- If no suitable surface exists and the work is project-level, maintain one compact `aegis-ledger.html` or project-approved equivalent.
- Update the active project or slice ledger; do not create a new HTML file for every micro-action.
- Record only useful resume state: step, action, result, validation, checkpoint, status, proof gaps, contradictions, and next safe action.
- Keep the ledger local and dependency-light.
- Treat the ledger as review and handoff state, not canon, unless the repo explicitly promotes it.

## Completion Criteria

The ledger is useful when another agent can resume the work from it without rereading the whole chat, and when it does not inflate proof level or duplicate canonical docs.

## Red Flags

- A new ledger file is created for every command.
- HTML polish is treated as proof.
- The ledger duplicates canon instead of pointing to it.
- Tiny one-shot work creates standalone ceremony.

## Boundary

This skill governs checkpoint materialization. Pair with `aegis-communication-discipline` when the goal is lower chat token usage.
