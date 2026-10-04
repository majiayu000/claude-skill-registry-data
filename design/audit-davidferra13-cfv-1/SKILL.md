---
name: audit
description: Thread completeness audit, cohesion check, hidden dependency scan, stress-test question set, and improvement pass. Use after discussing a feature to lock it down.
---

# THREAD AUDIT (Feature Completeness Gate)

Audit this entire thread for completeness. Execute all 5 phases in order.

## Phase 1: Gap Analysis

What did we miss or leave ambiguous? Scan every claim, assumption, and decision in this thread. List anything that is:

- Stated but not resolved
- Assumed but not verified
- Referenced but not defined
- Contradicted elsewhere in the thread

## Phase 2: Cohesion Check

Do all pieces of this feature connect internally? Map every component, endpoint, action, and UI surface discussed. Verify:

- Every input has a consumer
- Every output has a source
- Every state change propagates correctly
- No orphaned logic or dead paths

## Phase 3: Hidden Dependency Scan

Find connections between endpoints, components, or behaviors we treated as unrelated. Look for:

- Shared data that two features mutate independently
- Cache/revalidation gaps between related surfaces
- State that one feature assumes another feature sets
- Side effects that cross feature boundaries

## Phase 4: Stress-Test Question Set

Generate high-leverage questions that expose every failure point and force the spec into a fully verifiable state. Rules:

- Real-world scenarios only, no hypotheticals
- Each question must have a testable answer
- Questions should target edge cases, race conditions, error states, and boundary conditions
- Organize by domain (data integrity, UX, performance, security, etc.)

## Phase 5: Improvement Pass

What can we build or strengthen in the existing system based on this discussion? Identify:

- Quick wins (< 1 hour, high impact)
- Structural improvements that prevent future bugs
- Existing patterns that should absorb this feature's logic

## Constraint

All changes must benefit all users unless the feature is explicitly user-specific. Flag anything that only serves a narrow case.
