---
name: test-driven-development
description: "Use when implementing any feature or bugfix: write the test FIRST, watch it fail, then write minimal code to pass. For complex work, creates an epic with phased issues. Ensures tests verify behavior by requiring failure before implementation."
version: 3.0.0
triggers:
  - implementing a feature
  - fixing a bug
  - writing new code
  - adding functionality
---

# Test-Driven Development (TDD)

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over. No exceptions.**

## Step 0: Assess Complexity

Before starting ANY work, assess whether this is a **single-phase** or **multi-phase** effort.

### Single-Phase (Simple)

Use single-phase when ALL of these are true:
- Touches 1-3 files
- One logical concern (e.g., a bug fix, small feature, refactor)
- Can be completed in a single branch and PR
- No database migrations required, OR only trivial additive changes

**Action**: Proceed directly to [The Cycle](#the-cycle) below.

### Multi-Phase (Complex)

Use multi-phase when ANY of these are true:
- Touches 4+ files across multiple modules
- Multiple logical concerns (e.g., schema + processing + API + integration)
- Requires database migrations that other phases depend on
- Has natural dependency ordering (Phase 2 can't start until Phase 1 is done)
- Would benefit from parallel work streams

**Action**: Follow the [Epic & Phased Workflow](#epic--phased-workflow) before writing any code.

---

## The Cycle

```
RED → Verify Fails → GREEN → Verify Passes → REFACTOR → Repeat
```

### 1. RED - Write Failing Test

Write ONE minimal test showing what SHOULD happen.

```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

### 2. Verify RED - Watch It Fail

**MANDATORY. Never skip.** Run the test, confirm it fails for the expected reason.

### 3. GREEN - Minimal Code

Write the **simplest** code to pass the test. Don't add features beyond the test.

### 4. Verify GREEN - Watch It Pass

**MANDATORY.** All tests pass, no warnings.

### 5. REFACTOR - Clean Up

Only after green. Keep tests green. Don't add behavior.

---

## Epic & Phased Workflow

When complexity requires multiple phases, structure the work as an **epic** with **interconnected phase issues** before writing any code.

### 1. Create the Epic Issue

Create a GitHub issue labeled `epic` that serves as the master tracking issue. It must contain:

- **Scope summary**: What the entire body of work accomplishes and why
- **Phase list**: Numbered phases with titles, each linking to its dedicated issue (fill in links after creating phase issues)
- **Dependency graph**: ASCII or text diagram showing which phases block which
- **Architecture decisions**: Key technical choices that span phases
- **Success criteria**: What "done" looks like for the entire epic
- **File-level conflict analysis**: Which files each phase touches, to identify safe parallelism vs. serialization needs

**Epic issue template**:
```markdown
# Epic: [Title]

## Summary
[1-2 paragraphs: what this accomplishes and why it matters]

## Phases

| # | Title | Issue | Depends On | Files Touched |
|---|-------|-------|------------|---------------|
| 1 | [Phase 1 title] | #__ | — | list key files |
| 2 | [Phase 2 title] | #__ | Phase 1 | list key files |
| 3 | [Phase 3 title] | #__ | Phase 2 | list key files |

## Dependency Graph
Phase 1 → Phase 2 → Phase 3
                  ↘ Phase 4 (parallel with 3)

## Architecture Decisions
- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] All tests pass, TypeScript clean
```

### 2. Create Phase Issues

Each phase gets its own GitHub issue. Every phase issue must:

- **Reference the parent epic** in its title or first line (e.g., "Epic #XX — Phase 1: ...")
- **Declare dependencies** explicitly: "Blocked by: #YY" or "Can start immediately"
- **Include all mandatory sections** from the `github-issue-creator` skill:
  - TDD workflow (with phase-specific RED-GREEN-REFACTOR steps)
  - User Integration
  - Proposed Data Model Changes
- **Be self-contained**: A developer picking up this issue should not need to read other phase issues to implement it (though they should read the epic for overall context)
- **Define clear boundaries**: What's in scope for THIS phase and what's explicitly deferred to later phases

### 3. Analyze Parallelism

Before starting implementation, map file-level overlap between phases:

- **No overlap** → phases can run in parallel safely
- **Additive overlap** (both add to the same file, e.g., new exports in an index) → usually safe in parallel with minor merge coordination
- **Conflicting overlap** (both modify the same lines/functions) → must be serialized

Document this analysis in the epic issue.

### 4. Consider an Agent Team

**You can and should create an agent team when it would improve the quality or speed of the work.** This is especially valuable when:

- Multiple phases can run in parallel (no file conflicts)
- Phases are large enough that dedicated focus improves quality
- The dependency graph has a "wide" shape (many independent branches)

**Agent team structure**:
- **Team lead**: Owns the epic, creates all tasks with `blockedBy` dependencies, assigns phases to teammates, verifies completions, and handles merge coordination
- **Phase agents**: Each assigned to one phase issue. Works autonomously following TDD within their phase. Reports completion back to team lead
- **Dependency cascade**: When Phase 1 completes, team lead assigns Phase 2 (and any other phases unblocked by Phase 1)

**When NOT to use a team**:
- Phases are strictly sequential with no parallelism opportunity
- The work is small enough that context-switching overhead outweighs parallel gains
- Phases have heavy file-level conflicts requiring constant coordination

See `reference/agent-team-pattern.md` for the detailed playbook.

### 5. Execute Phase by Phase

For each phase (whether solo or via agent team):

1. **Check out a feature branch**: `feature/<issue-number>-<description>`
2. **Invoke this skill's TDD cycle** for all code in the phase
3. **Run full test suite** — no regressions
4. **TypeScript clean** — `npm run typecheck` passes
5. **Create PR** referencing the phase issue
6. **Merge to main** before starting dependent phases
7. **Update epic issue** — check off the completed phase

---

## Before Writing Tests

**ALWAYS investigate the codebase first:**

1. Find existing tests (`**/*.test.ts`, `__tests__/`)
2. Identify test framework (Jest, Vitest, etc.)
3. Discover patterns and helpers
4. Check for cleanup scripts in `package.json`

## Test Data Cleanup

**Tests MUST NOT pollute the database.** See: `reference/database-cleanup-strategies.md`

## Supabase Auth (impactOS Critical)

Test these BEFORE implementing:
1. **Tenant isolation** - RLS blocks cross-tenant access
2. **JWT claims** - tenant_id in access token
3. **DAL pattern** - requireAuth() enforced

See: `reference/supabase-auth-patterns.md`

## Red Flags - STOP and Start Over

- Code written before test
- Test passes immediately
- Can't explain why test failed
- Rationalizing "just this once"

See: `reference/common-rationalizations.md`

## Verification Checklist

- [ ] Every new function has a test
- [ ] Watched each test fail first
- [ ] Wrote minimal code to pass
- [ ] Test data cleanup implemented

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API first |
| Test too complicated | Design too complicated |
| Must mock everything | Code too coupled |

See: `reference/troubleshooting.md`

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without human approval.
