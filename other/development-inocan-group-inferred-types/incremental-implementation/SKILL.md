---
name: incremental-implementation
description: Use when building multi-day features, avoiding long-lived branches, features taking >1 day, changes touching multiple systems, or high-risk changes needing gradual rollout - break features into deployable increments that each provide value
---

# Incremental Implementation

**Persona:** Surgeon who makes small, precise incisions - each cut is complete and leaves the patient stable.

**Core principle:** Every commit to main should be deployable. No "work in progress" merges.

## Should NOT Attempt

- PRs >500 lines without explicit approval
- "Part 1 of N" where parts aren't independently deployable
- Horizontal slicing (all UI, then all API, then all DB)
- Breaking changes without migration path
- Merging incomplete features behind no flag
- Bundling unrelated changes "while I'm here"

## Vertical Slicing (Preferred)

```
BAD (Horizontal)          GOOD (Vertical)
Week 1: All UI            Day 1: Login (UI+API+DB)
Week 2: All API           Day 2: Register (UI+API+DB)
Week 3: All Database      Day 3: Profile (UI+API+DB)
```

**INVEST criteria:** Independent, Negotiable, Valuable, Estimable, Small, Testable

## Increment Patterns

| Pattern | When to Use |
|---------|-------------|
| API-First | Backend-heavy, multiple clients |
| UI-First with Stub | UI/UX feedback needed early |
| Database-First | Complex data model, careful schema planning |
| Feature Flag | High risk, gradual validation needed |

## Example: Good vs Bad

```
BAD: PR #1: "Add user profile" (2000 lines - everything)

GOOD:
PR #1: "Add user_profiles table" (50 lines)
PR #2: "Add Profile model/repository" (100 lines)
PR #3: "Add GET /api/profile" (80 lines)
PR #4: "Add profile page UI" (150 lines)
PR #5: "Add PUT /api/profile" (100 lines)
PR #6: "Add profile edit form" (200 lines)
```

## Backward Compatibility

**Adding fields:** nullable first -> backfill -> make non-nullable
**Changing APIs:** add new alongside old -> update clients -> deprecate old -> remove
**Renaming:** add alias -> update callers -> remove old name

## Planning Steps

1. **List all changes** - Database, models, APIs, UI
2. **Find dependencies** - What needs what?
3. **Order by dependencies** - Bottom-up
4. **Size each increment** - Target <500 lines

## Checkpoint Criteria

Each increment must:
- [ ] All tests pass
- [ ] Can be deployed independently
- [ ] Doesn't break existing functionality

## Escalation Triggers

**Escalate to architect/lead when:**
- Feature cannot be sliced without breaking existing API contracts
- Increment requires data migration affecting >10% of production data
- Dependencies form a cycle that prevents clean ordering
- Smallest viable increment exceeds 500 lines
- Feature requires coordinated deployment across multiple services

**How to escalate:**
```
SLICING BLOCKED: [feature name]
Minimum viable increment: [size estimate]
Blocking dependency: [what prevents smaller slices]
Options considered: [A, B, C]
Recommendation: [path forward]
```

## Failure Behavior

**When increment cannot be made deployable:**
1. State what blocks independent deployment
2. Present options: feature flag, temporary compatibility layer, or accept larger increment
3. Document the technical debt if larger increment accepted

**When slicing introduces complexity:**
1. Compare: complexity of slicing vs. complexity of large PR review
2. If slicing adds more risk than it removes, accept larger increment with extra review

## Red Flags

- PR >500 lines without good reason
- "WIP" commits on main
- "Part 1 of 3" where parts aren't independent
- Features that "only work when everything is done"

## Related Skills

- **git-workflow**: Isolate incremental work in worktrees, handle completion
- **test-driven-development**: TDD for each increment

## Integration

- **git-workflow** skill - Isolate each increment in worktree, merge/PR when complete
- **orchestrator** agent - Help plan increment ordering
- **test-driven-development** skill - Each increment needs tests
- **verification-before-completion** skill - Verify before merging each increment
