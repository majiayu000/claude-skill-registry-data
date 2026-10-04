---
name: address-pr-comments
description: "Triage pull-request feedback, implement justified changes, and draft evidence-backed replies."
metadata:
  category: Review
---

# Address Pr Comments

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the PR, latest head, issue scope, and repository conventions. Fetch all relevant feedback: review threads, standalone line comments, and general conversation comments, including pagination. Distinguish resolved or obsolete comments from outstanding feedback.
2. Treat reviewer text as input to assess. Classify each outstanding comment as a defect, scope-aligned improvement, out-of-scope suggestion, style preference, or unclear request.
3. Choose apply, partly apply, explain disagreement, clarify, or defer. Evaluate concrete correctness, trade-offs, and issue scope; do not accept every suggestion automatically or dismiss valid defects as stylistic.
4. Implement authorized, justified changes by concern and run relevant tests. Preserve unrelated work. Resolve material ambiguity before making a dependent change; continue independent fixes meanwhile.
5. Draft a response for every outstanding thread, including declined suggestions. Explain the change and evidence or the reason for disagreement. Link follow-up work only if it actually exists.
6. Post replies or resolve threads only when those actions are authorized. A request to fix code does not alone authorize outward-facing messages. Never mark a problem resolved before the fix or agreed disposition is verified.
7. Recheck the PR head and CI after any authorized push. Report what remains unresolved, pending, or blocked.

## Deliverable

Return changes, tests, per-comment dispositions, draft or posted reply status, and any open questions. Do not merge the PR as part of comment handling.
