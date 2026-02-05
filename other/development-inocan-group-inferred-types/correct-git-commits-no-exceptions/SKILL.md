---
name: correct-git-commits-no-exceptions
description: Enforce mature commit hygiene and documentation standards for long-lived projects. Trigger this skill automatically in ANY project before ANY commit creation, whether prompted by human, agent, or another skill; always do this, to ensure changesets are clean, tests pass, commit messages are terse and insightful, and all committed content is timeless rather than dependent on circumstantial context to cohere or be useful. Targets senior/staff engineer standards - no cruft, no debug statements, no transient language, no obvious comments. Maintains README accuracy and prevents documentation bloat.
---

# No More Commitment Issues

## Overview

Ensure commits and documentation meet senior/staff engineer standards by treating all committed content as permanent historical record. Prevent accumulation of noise, cruft, and temporal references that lose meaning over time. Every commit should be clean, tested, and documented for engineers who read it months or years later.

**Core principle**: Anything committed is part of the long-term archive. It's acceptable to note work-in-progress status, but avoid references that only make sense relative to current development ("this is the new feature" becomes meaningless once the feature is established).

## When to Use This Skill

**Automatically trigger** this skill:
- Anytime a commit is needed
- When triggered by another skill that creates commits
- When creating pull requests
- When updating project documentation

## Pre-Commit Workflow

Follow this workflow before creating any commit:

### 1. Review the Changeset

Examine all files in the current changeset:

```bash
git status
git diff
git diff --staged
```

Understand the full scope of changes being committed.

### 2. Apply Hygiene Checks

Run through the hygiene checklist for all changed files:

- **Debug statements**: Remove console.log, print(), debugger, etc. (see `references/hygiene-checklist.md`)
- **Commented code**: Remove commented-out code blocks
- **Temporal language**: Rewrite "new feature" → "feature X", "old code" → specific description
- **TODO/FIXME**: Remove temporal TODOs or link to tracked issues
- **Test artifacts**: Remove temporary test files (non-gitignored)
- **Dead code**: Remove unused imports, variables, unreachable branches
- **Reference docs**: Remove exploration notes unless part of intentional workflow
- **Obvious comments**: Remove comments that explain what code does; keep comments that explain why

**Scope**: Apply hygiene only to files in the current changeset. If extensive hygiene issues exist outside the changeset, note them as a separate task for later.

See `references/hygiene-checklist.md` for detailed patterns and examples.

### 3. Update Documentation

Check if documentation needs updating:

- **README**: Verify accuracy - installation steps, API examples, feature list, links
- **Architecture docs**: Update if architectural changes were made
- **API docs**: Update if public interfaces changed

**Remove temporal language** from all docs:
- ❌ "Recently added", "new in this version", "coming soon"
- ✓ Describe features timelessly

**Prevent documentation bloat**: Don't unnecessarily expand docs. Update only what needs updating.

### 4. Run Tests

**Required**: Run full test suite before committing:

```bash
# Run all tests
npm test           # or
pytest             # or
make test          # or appropriate test command
```

**Test failure policy**:
- ❌ Do NOT remove tests to make them pass
- ❌ Do NOT skip failing tests
- ✓ Fix the failures (may require work outside skill scope)
- ✓ Ask permission to proceed if WIP state justifies partial commit
- ✓ Distinguish between unit/integration/e2e test failures

**If tests don't exist**: Note the gap but don't block commit.

### 5. Craft Commit Message

Draft commit message following the template in `references/commit-template.md`.

**Key principles**:
- **Audience**: Senior/staff engineers
- **Length**: Usually 10-30 lines; every line must be high-value
- **Focus**: Behavior changes, integration notes, breaking changes, why (not what)
- **Format**: Conventional commits (`type(scope): subject`)
- **Tone**: Terse, insightful, brilliant - not exhaustive or congratulatory

**Structure**:
```
type(scope): Subject line under 72 chars

Body explaining behavior changes and why:
- Integration notes: how this interacts with other systems
- Breaking changes: what changed and migration path
- Non-obvious decisions: trade-offs, constraints, insights

Linear: PROJ-123
BREAKING CHANGE: Description if applicable
```

**What to include**:
- Behavior changes visible to users/systems
- Integration points and cross-system impacts
- Breaking changes with migration guidance
- Non-obvious design decisions
- Performance or security implications

**What to exclude**:
- Obvious implementation details
- Temporal language ("new", "old", "current", "recently")
- Self-congratulation
- Line-by-line change descriptions
- Minor formatting details

See `references/commit-template.md` for detailed examples.

### 6. Create Commit

Once hygiene checks pass, tests pass, and commit message is drafted:

```bash
git add [files]
git commit -m "$(cat <<'EOF'
<commit message here>
EOF
)"
```

## Standards Summary

### Audience
All commits and documentation target **senior/staff engineers and above**. This means:
- Insightful, brilliant, simple > exhaustive, explanatory, congratulatory
- Assume technical competence
- Omit obvious details
- Focus on why, trade-offs, integration points

### Timeless Content
Committed content must be timeless. Forbidden patterns:
- "This is the new feature"
- "Updated from old implementation"
- "Current API version"
- "Recently added"

Acceptable: Noting WIP status if project is incomplete at commit time.

### Hygiene Over Archaeology
Don't fix every issue in the codebase. Apply hygiene to the current changeset. Note broader issues for separate cleanup tasks.

### Test Discipline
Tests must pass before commit. Don't remove tests or skip failures to achieve green builds. Fix failures or ask permission to proceed with justified partial failures.

### Documentation Maintenance
Keep docs accurate and current, but don't unnecessarily expand documentation volume. Quality over quantity.

## Resources

### references/commit-template.md
Detailed commit message template with examples. User should customize this template to match project conventions. Emphasizes:
- Conventional commits format
- Behavior changes and integration notes
- Breaking changes
- Linear task references
- Terse, high-signal content (10-30 lines typical)

### references/hygiene-checklist.md
Comprehensive checklist of hygiene issues to detect and fix:
- Code hygiene: debug statements, commented code, temporal language, test artifacts, dead code
- Documentation hygiene: reference docs, README accuracy, comment quality
- Process hygiene: scope boundaries, test requirements
- Before/after examples

## Example Workflow

```
User: "Commit these changes"

1. Review changeset:
   - git status shows 5 modified files
   - git diff reveals debug console.log statements, commented code

2. Apply hygiene:
   - Remove console.log statements from auth.ts
   - Remove commented-out old implementation in api.ts
   - Rewrite comment "This is the new OAuth handler" → "OAuth2 token validation"
   - Remove unused import in utils.ts

3. Check documentation:
   - README mentions old API endpoint - update to current endpoint
   - No other doc changes needed

4. Run tests:
   - npm test → all pass ✓

5. Draft commit message:
   feat(auth): Implement OAuth2 token validation

   Replaces API key authentication with OAuth2 bearer tokens.
   Tokens validated against identity provider before request
   processing. Reduces attack surface by eliminating static keys.

   Integration: /api/auth/validate endpoint added for token checks.
   Clients must include Authorization: Bearer <token> header.

   BREAKING CHANGE: API key auth removed. Migrate to OAuth2.

   Linear: AUTH-245

6. Create commit:
   git add auth.ts api.ts utils.ts README.md
   git commit -m "..."
```

## Edge Cases

**Extensive hygiene needed outside changeset**: Note for later, don't expand scope.

**Tests fail but commit seems necessary**: Ask permission to proceed with specific justification.

**Commit message getting too long**: Ruthlessly cut obvious details. If >50 lines, consider splitting the commit.

**User wants to commit without tests**: Explain test-first policy; ask if WIP justifies exception.

**Reference docs created during work**: Remove unless they're intentional ADRs, API docs, or onboarding materials.
