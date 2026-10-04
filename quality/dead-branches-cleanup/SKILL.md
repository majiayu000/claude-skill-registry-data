---
id: quality.no-dead-code.dead-branches-cleanup
name: Dead Branches Cleanup
description: >
  Removes unreachable or obsolete logic branches caused by legacy flags, impossible conditions, or retired compatibility paths while preserving intentional behavior.
stack:
  - JavaScript
  - TypeScript
category: no-dead-code
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - dead branches
  - unreachable code
  - obsolete branch
  - legacy flags
  - conditional cleanup
compatibility:
  runtime:
    browser: true
    node: true
---

# Dead Branches Cleanup

## Purpose

Use this skill to remove unreachable or obsolete logic branches.

The goal is to simplify control flow after migrations, flag removals, or compatibility drops.

The core rule is simple:

```txt
Delete only branches you can prove are dead.
```

## When to Use

Use this skill when:

- old feature flags are retired
- legacy compatibility paths are gone
- impossible conditions remain
- code after return or throw is still present

## Do

Verify the branch against:

- current feature flags
- current versions
- runtime contracts
- tests

## Do Not

Avoid removing branches that still serve real compatibility.

Avoid broad refactors that are unrelated to the dead branch.

## Review Checklist

- [ ] The branch is provably dead.
- [ ] Compatibility implications were checked.
- [ ] Tests still describe the intended behavior.

## Expected Output

1. Prove the branch is dead.
2. Remove it safely.
3. Keep compatibility in view.
4. Validate behavior.
5. Keep the cleanup bounded.
