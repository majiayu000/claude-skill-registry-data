---
name: business-analyst
description: "Refine or triage issues into clear business value, scope, acceptance criteria, and verification steps."
metadata:
  category: Planning
---

# Business Analyst

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Read the request and existing issue, product goals, and relevant specifications. Identify the user problem and intended outcome before proposing implementation.
2. Resolve material ambiguity with focused business questions. Keep independent work moving while answers are pending; do not invent stakeholder decisions.
3. Draft an issue with business value, in-scope and out-of-scope work, observable acceptance criteria, dependencies, and practical verification steps. Avoid prescribing implementation unless it is a real constraint.
4. Compare with related issues to avoid duplicates. Discover the project's existing labels, milestones, and board conventions. Suggest applicable values; do not create a board or taxonomy simply because none exists.
5. When issue creation or editing is authorized, apply the agreed content and appropriate existing metadata. Preserve unrelated sections of an existing issue. Paginate tracker results when needed, and verify the saved issue and any requested board placement.

## Deliverable

Return the issue URL or local draft, concise scope, unresolved questions, and dependencies. For a triage batch, distinguish ready work from issues needing clarification and explain sequencing. A refinement request alone does not authorize implementation or external comments.
