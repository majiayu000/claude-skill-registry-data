---
name: meta-improve
agent: none
description: Canonical constrained self-improvement protocol. Reads operator-approved Dream candidates and never self-merges or self-approves.
allowed-tools: Read, Write, Bash
user-invocable: false
status: PRODUCTION - invoke through /meta-improve-vault
---

# Constrained self-improvement

The public verb is `/meta-improve-vault`.

## Input and gate

Select only from canonical `vault/memory/DREAM_LOG.md`: an exact candidate
whose `status` is `approved` and whose approval was written by
`/dream --set-status` from a direct operator decision. `proposed` is not
approval.

Read only the exact evidence references named by that approved candidate from
`vault/memory/runtime/LESSONS.jsonl` and
`vault/memory/runtime/NIGHTLY_CAPTURE_CANDIDATES.jsonl`. Those products provide
traceability; they never provide approval by themselves.

Before Build:

```text
node daemons/nightly-contracts.mjs meta --root <aigent-root> \
  --candidate <candidate-id>
```

Require `META_GATE PASS`. It checks the canonical block for exact approved
status and non-placeholder operator evidence. This is the executable
`nightly-contracts.mjs meta` gate.

## Build

For one approved candidate:

1. Re-read its evidence, proposed change, mutation proof, and scope.
2. Use repository isolation where normal policy requires it.
3. Apply the smallest change satisfying the proposal.
4. Run the real red-before and green-after proof plus relevant system checks.
5. Produce a review artifact with exact diff, commands, exits, residual risks,
   and rollback.
6. Surface `accept / reject / revise` to the operator.

Never merge, push, deploy, broaden scope, modify an operator gate, approve
another candidate, or infer approval. A failed proof asks the Dream writer to
set the candidate `blocked`.

## Status ownership

This skill never edits Dream directly. The Dream writer owns:

- direct operator approval: `proposed -> approved`;
- verified build failure: `approved -> blocked`;
- direct rejection: `approved -> rejected`;
- independently verified merge: `approved -> merged`.

The complete flow is:

`propose -> operator gate -> build -> independent review -> operator outcome`
