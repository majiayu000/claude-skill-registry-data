---
name: create-pull-request
description: 'Use this skill when creating or updating a pull request in the TTA.dev repository. Covers PR title format, description template, review expectations, and pre-submit checklist. Invoke when the user says "create a PR", "open a pull request", "submit my changes", or "make a PR".'
---

### Create Pull Request (TTA.dev)

Guide for creating well-structured pull requests.

#### PR Title

Follow Conventional Commits format: `<type>: <description>`

Examples:
- `feat: add CachePrimitive metrics integration`
- `fix: resolve timeout in RetryPrimitive backoff`
- `docs: update primitives catalog with new skills API`

#### PR Description Template

```markdown
## Summary
Brief description of what this PR does.

## Changes
- List of specific changes made.

## Testing
- How the changes were tested.
- Coverage impact.

## Checklist
- [ ] Quality gate passes (format, lint, type check, tests)
- [ ] 100% test coverage on new code
- [ ] Documentation updated if applicable
- [ ] No new anti-patterns introduced
```

#### Before Submitting

1. Run the full quality gate (see `build-test-verify` skill).
2. Self-review your diff (see `self-review-checklist` skill).
3. Ensure all new code uses primitives for workflow patterns.
4. Verify no secrets or credentials are committed.

#### Deep Reference

For full Python coding standards, see [`docs/agent-guides/python-standards.md`](../../docs/agent-guides/python-standards.md).
