---
name: branch-pr-lifecycle
description: Use feature branches, immediate push, and early draft pull requests for delivery work. Use when Builders or related agents create implementation branches, commit changes, push work, request review, and move pull requests from draft to ready-for-review.
---

# Branch and PR lifecycle

## Rules
- Do all work in feature branches
- Push branches as soon as there is a meaningful commit
- Raise a draft PR as soon as the branch exists remotely
- Convert the PR to ready for review once the scoped work is complete
- Request review from the appropriate agent archetypes through the PR

## Review flow
- Builder owns the branch and initial draft PR
- QA reviews correctness and quality
- Spec and Orchestrator decide whether the approved PR is mergeable in project context

## PR hygiene
Always include:
- visible archetype header: `> _posted by **<Archetype>**_`
- summary
- changed scope
- validation performed
- assumptions made
- follow-ups or risks

## Assumptions
All meaningful assumptions must be listed in the PR and linked to durable docs when they affect project behavior or architecture.
