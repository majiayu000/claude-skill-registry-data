---
name: propose-implementation-plan
description: Create an implementation plan with atomic commits that build toward a complete feature
---

# Propose Implementation Plan Skill

## Purpose

Create a detailed implementation plan that breaks a feature into atomic, reviewable commits.
The plan serves as a roadmap for implementation, ensuring each commit is self-contained, tested, and buildable.

## When to Use

- Feature design document exists and is approved
- Ready to begin implementation
- Need to coordinate work or track progress
- Want to ensure commits are appropriately sized

## Prerequisites

- Feature design exists in `docs/features/NNNN-feature-name/design.md`
- Test plan exists in `docs/features/NNNN-feature-name/test-plan.md`
- Design and test plan have been reviewed and approved
- Implementor understands the technical approach

## Procedure

### 1. Verify Design Exists

```bash
ls ./docs/features/NNNN-feature-name/design.md
```

If it doesn't exist, use `propose-feature-design` skill first.

### 2. Create Planning Directory and Copy Template

Implementation plans go in `./planning/` (gitignored scratch space), not `./docs/features/`.

```bash
mkdir -p ./planning/NNNN-feature-name
cp ./docs/features/0000-templates/implementation-plan.md ./planning/NNNN-feature-name/
```

### 3. Study the Design Document

Read the design thoroughly, noting:
- Module structure and affected files
- Dependencies between components
- Migration requirements from current state
- Critical Constraints table

### 3a. Study the Test Plan

Read `./docs/features/NNNN-feature-name/test-plan.md` and note:
- Which requirements map to which test types (unit/integration/out-of-scope)
- Which Critical Constraints have test coverage vs. require review
- Test names and descriptions that will be assigned to commits

### 3b. Extract Critical Constraints

Review the design's Critical Constraints table (CC-1, CC-2, etc.).
For each constraint:
1. Identify which commit(s) implement it
2. Copy the constraint and anti-pattern to those commits' Acceptance Criteria
3. These become explicit review checkpoints

**This step prevents the most common implementation mistakes.**
If the design lacks critical constraints, ask for clarification before proceeding.

### 4. Identify Natural Boundaries

Look for **capability boundaries**, not code artifact boundaries.
A good commit tells a story about impact—"here's a new capability" or "here's a behavior change"—not "here's a struct" followed by "here's its methods."

Good boundaries:
- A new module with its types, implementation, and tests together
- A user-visible capability (e.g., a new CLI command with its handler)
- A requirement being satisfied end-to-end
- A refactoring that prepares for new functionality

**Anti-pattern**: Splitting by code artifact (types in one commit, impl in another, tests in a third).
This fragments the reviewable story and undermines TDD—the implement-commit workflow expects types, implementation, and tests to be developed together within a single commit.

### 5. Plan Commits Following the Atomic Commit Rules

**Each commit MUST be:**

1. **Buildable** - The project compiles after this commit
2. **Tested** - New code has tests; existing tests pass (or are explicitly disabled with TODO)
3. **Focused** - Does one logical thing
4. **Reviewable** - Small enough to review in one sitting (target: <400 lines changed)

**Each commit SHOULD:**

1. **Be independently valuable** - Provides some benefit even if later commits aren't merged
2. **Have a clear purpose** - The commit message explains why, not just what
3. **Minimize risk** - Smaller commits are easier to revert if problems arise

### 5a. Handle Test Breakage During Refactors

When a commit breaks tests in distant modules (e.g., schema changes that break integration tests), **do not leave broken tests**.
Instead, explicitly disable them with a TODO that references when they should be re-enabled.

**Pattern for disabling tests:**

```rust
// TODO: Re-enable in Commit 9a after updating domain types
#[cfg(all(test, feature = "enable_broken_tests"))]
mod tests {
    // ...
}
```

Or for individual tests:

```rust
#[test]
#[ignore] // TODO: Re-enable in Commit 12a after facade integration
fn test_search_returns_results() {
    // ...
}
```

**When planning commits that break existing tests:**

1. **Identify which tests will break** - Note them in the commit description
2. **Disable tests explicitly** - Use `#[ignore]` or feature flags, not deletion
3. **Add a TODO comment** - Reference the specific commit that will re-enable them
4. **Plan a re-enablement commit** - Add a commit (e.g., "9a", "12a") that fixes and re-enables the tests
5. **Place re-enablement after dependencies are ready** - The re-enable commit comes after all changes needed to fix the tests

**Example from a real plan:**

```markdown
- [ ] **Commit 4**: Update database schema (disables incompatible tests)
- [ ] **Commit 8**: Update IndexedFile to include new fields
- [ ] **Commit 9**: Update Chunk to use content-addressed storage
- [ ] **Commit 9a**: Re-enable and fix storage layer tests  ← Re-enablement commit
```

This approach:
- Keeps the build green at every commit
- Makes test debt explicit and trackable
- Ensures tests aren't forgotten
- Gives coders clear guidance on when to fix tests

### 6. Size Commits Appropriately

**Too Small** (avoid):
- Adding types without their implementation
- Trait definitions without at least one implementation
- Implementation without its tests
- Changes that don't stand alone as a reviewable story

**Too Large** (avoid):
- Entire feature in one commit
- Multiple unrelated capabilities
- Changes that take days to review
- Modules exceeding ~500 lines (see lint_loc.py for project limits)

**Just Right** (target):
- A new module with types, implementation, and tests (~200-400 lines)
- A new CLI command with handler and tests (~150-350 lines)
- A complete adapter implementation with tests (~200-400 lines)
- A refactoring that prepares for new functionality (~100-300 lines)

Use judgment: if a module will exceed ~500 lines, split by capability (e.g., "config loading" vs "config validation"), not by artifact type.

### 7. Order Commits by Dependency

Structure commits so each builds on previous work:

```
Phase 1: Foundation
  Commit 1: Add new types (no behavior yet)
  Commit 2: Add trait definitions (interfaces only)
  
Phase 2: Core Implementation  
  Commit 3: Implement trait for primary adapter
  Commit 4: Wire into application layer
  
Phase 3: Integration
  Commit 5: Add CLI commands
  Commit 6: Add integration tests
```

### 8. Write the Commit Checklist

Create the high-level checklist at the top of the document.
Keep descriptions to one line—details go in the commit sections.

```markdown
- [ ] **Commit 1**: Add Context and ContextId types
- [ ] **Commit 2**: Add ContextRepository trait
- [ ] **Commit 3**: Implement SqliteContextRepository
```

### 9. Write Detailed Commit Descriptions

For each commit, document:

**Summary**: What and why in one paragraph.

**Files Changed**: List files with brief description of changes.

**Key Changes**: Bullet points of specific modifications.

**Requirements Addressed**: List requirement IDs (REQ-*) this commit implements or advances. Reviewers use this as a checklist independent of test coverage.

**Constraints Addressed**: List constraint IDs (CC-*) this commit must satisfy. Copy the constraint and anti-pattern from the design doc for reviewer reference.

**Testing**: Reference tests from the test plan that cover this commit's changes. Include test names and requirement IDs (e.g., "Adds test_search_returns_results for REQ-3"). For requirements marked not-testable, note what reviewers should verify manually.

**Dependencies**: Which prior commits must be complete.

### 10. Identify Parallelization Opportunities

Note which commits have no dependencies on each other.
These can be implemented simultaneously by different people or in any order.

```markdown
## Parallelization Notes

- Commits 3 and 4 can be developed in parallel (both depend only on 1-2)
- Phase 2 requires all of Phase 1 to be complete
```

### 11. Document Open Questions

Track decisions that need resolution during implementation:

```markdown
## Open Questions

- [ ] Should we use async for the repository trait?
- [ ] What's the migration strategy for existing databases?
```

## Commit Sizing Guidelines

### Indicators a Commit is Too Large

- More than 500 lines changed
- Touches more than 5-6 files
- Implements multiple unrelated capabilities
- Commit message needs to explain several distinct changes
- Reviewer can't hold the whole change in their head

### Indicators a Commit is Too Small

- Introduces types without their implementation or tests
- Defines traits without at least one implementation
- Creates code that only makes sense with later commits
- Splits what should be one reviewable story into fragments
- Separates tests from the code they test

### Splitting Large Changes

If a change seems too large, look for **capability boundaries**:

1. **Separate capabilities**: Does this module do two distinct things? (e.g., "loading" vs "validation")
2. **Layer boundaries**: Can storage, logic, and CLI be separate commits?
3. **Refactor then change**: Can existing code be restructured in a prep commit?
4. **Integration points**: Can the core capability land before integrating it everywhere?

Keep types, implementation, and tests together within each split.
The goal is commits that each tell a complete story, not commits that each touch one kind of artifact.

### Example: Splitting a Large Feature

Instead of one commit "Add multi-context support", split by **capability**:

```
Commit 1: Add context storage layer (types, repository, schema, tests)
Commit 2: Add context discovery from workspace (scanner, tests)
Commit 3: Add context CLI commands (list, remove, tests)
Commit 4: Integrate context into indexing (scoped storage, tests)
Commit 5: Integrate context into search (filtering, tests)
```

Each commit delivers a complete capability with its tests.
A reviewer can understand what Commit 1 accomplishes without needing to see Commits 2-5.

**Anti-pattern** (too granular):
```
Commit 1: Add Context type and ContextId newtype
Commit 2: Add ContextRepository trait definition
Commit 3: Update database schema with contexts table
Commit 4: Implement SqliteContextRepository
Commit 5: Add tests for context storage
...
```

This splits one capability (context storage) across 5 commits, making review harder and breaking TDD.

## Validation

Verify the implementation plan:

```bash
# Check file exists
ls ./planning/NNNN-feature-name/implementation-plan.md

# Verify it has the checklist
grep -E "^\- \[ \]" ./planning/NNNN-feature-name/implementation-plan.md

# Count commits planned
grep -c "^#### Commit" ./planning/NNNN-feature-name/implementation-plan.md
```

Review the plan for:
- [ ] Each commit is atomic and buildable
- [ ] Commits are appropriately sized (target <400 lines)
- [ ] Dependencies are clearly stated
- [ ] Testing approach is documented for each commit
- [ ] Phases group related work logically

## Common Issues

**Commits too large**: Split by type/trait/implementation boundaries.

**Commits too small**: Combine related changes that don't make sense alone.

**Unclear dependencies**: Draw a dependency graph if needed.

**Missing tests**: Every commit should include tests for new code.

**Vague descriptions**: Be specific about files and changes.

**Refactor breaks distant tests**: Don't leave tests broken or delete them. Disable with `#[ignore]` or feature flag, add a TODO referencing the re-enablement commit, and plan a specific commit to fix and re-enable them. See section 5a.

## Next Steps

After creating the implementation plan:
1. Review with team for feasibility and sizing
2. Adjust based on feedback
3. Begin implementation, checking off commits as completed
4. Update plan if implementation reveals needed changes
5. Use the checklist to track progress
