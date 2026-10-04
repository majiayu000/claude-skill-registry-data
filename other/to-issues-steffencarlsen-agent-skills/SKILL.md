---
name: to-issues
description: Break a PRD, feature spec, plan, or issue into independently implementable vertical-slice issues. Use when the user invokes to-issues, asks to split work into tickets, wants a Kanban-ready breakdown, or needs implementation tasks with dependencies.
---

# To Issues

Break a plan into small vertical slices that can be implemented and verified independently.

## Process

1. Read the PRD, plan, issue, or conversation context.
2. Inspect the codebase when current architecture affects the issue boundaries.
3. Prefer slices that deliver end-to-end behavior through all needed layers. Avoid layer-only tickets unless they are true prefactoring blockers.
4. Order issues by dependency. Blockers come first.
5. Show the proposed issue list to the user before publishing.
6. Publish only after approval and only when issue-tracker tooling is available.

## Issue Draft Format

For each issue, provide:

```markdown
## Title

<short action-oriented title>

## What to build

Describe the end-to-end behavior this slice adds or changes.

## Acceptance criteria

- [ ] Observable behavior is implemented.
- [ ] Relevant tests or validation prove the behavior.
- [ ] Existing behavior stays intact.

## Blocked by

None - can start immediately.
```

Include parent issue links when the source is an existing tracker issue. Do not close or modify parent issues.
