---
name: review-changes
description: "[Review & Quality] Review all uncommitted changes before commit"
infer: true
---

# Code Review: Uncommitted Changes

Perform a comprehensive code review of all uncommitted git changes following EasyPlatform standards.

## Summary

**Goal:** Review all uncommitted changes via a report-driven three-phase process before commit.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Get changes & create report | `git diff HEAD`, create `plans/reports/code-review-*.md` |
| 2 | File-by-file review | Read each diff, update report with summary/purpose/issues |
| 3 | Holistic review | Re-read accumulated report for architecture coherence |
| 4 | Generate final findings | Critical issues, warnings, suggestions, commit message |

**Key Principles:**
- Build report incrementally -- update after EACH file, not at the end
- Check logic placement in lowest layer (Entity > Service > Component)
- Always suggest conventional commit message based on changes

## Review Approach (Report-Driven Three-Phase - CRITICAL)

**⛔ MANDATORY FIRST: Create Todo Tasks for Review Phases**
Before starting, call TodoWrite with:

- [ ] `[Review Phase 0] Get git changes and create report file` - in_progress
- [ ] `[Review Phase 1] Review file-by-file and update report` - pending
- [ ] `[Review Phase 2] Re-read report for holistic assessment` - pending
- [ ] `[Review Phase 3] Generate final review findings` - pending

Update todo status as each phase completes. This ensures review is tracked.

---

## Phase 0: Get Changes & Create Report

### 0.1 Get Change Summary

```bash
# See all changed files
git status

# See actual changes (staged and unstaged)
git diff HEAD
```

### 0.2 Create Report File

- [ ] Create `plans/reports/code-review-{date}-{slug}.md`
- [ ] Initialize with Scope (list of changed files), Change Type (feature/bugfix/refactor)

---

## Phase 1: File-by-File Review (Build Report Incrementally)

For EACH changed file, read the diff and **immediately update report** with:

- [ ] File path
- [ ] Change Summary: what was modified/added/deleted
- [ ] Purpose: why this change exists (infer from context)
- [ ] Issues Found: naming, typing, responsibility, patterns
- [ ] Continue to next file, repeat

### Review Checklist Per File

#### Architecture Compliance

- [ ] Follows Clean Architecture layers (Domain, Application, Persistence, Service)
- [ ] Uses correct repository pattern (I{Service}RootRepository<T>)
- [ ] CQRS pattern: Command/Query + Handler + Result in ONE file
- [ ] No cross-service direct database access

#### Code Quality

- [ ] Single Responsibility Principle
- [ ] No code duplication (DRY)
- [ ] Appropriate error handling with PlatformValidationResult
- [ ] No magic numbers/strings (extract to named constants)
- [ ] Type annotations on all functions
- [ ] No implicit any types
- [ ] Early returns/guard clauses used

#### Naming Conventions

- [ ] Names reveal intent (WHAT not HOW)
- [ ] Specific names, not generic (`employeeRecords` not `data`)
- [ ] Methods: Verb + Noun (`getEmployee`, `validateInput`)
- [ ] Booleans: is/has/can/should prefix (`isActive`, `hasPermission`)
- [ ] No cryptic abbreviations (`employeeCount` not `empCnt`)

#### Platform Patterns

- [ ] Uses platform validation fluent API (.And(), .AndAsync())
- [ ] No direct side effects in command handlers (use entity events)
- [ ] DTO mapping in DTO classes, not handlers
- [ ] Static expressions for entity queries

#### Security

- [ ] No hardcoded credentials or secrets
- [ ] Proper authorization checks
- [ ] Input validation at boundaries
- [ ] No SQL injection risks

#### Performance

- [ ] No O(n²) complexity (use dictionary for lookups)
- [ ] No N+1 query patterns (batch load related entities)
- [ ] Project only needed properties (don't load all then select one)
- [ ] Pagination for all list queries
- [ ] Parallel queries for independent operations
- [ ] Appropriate use of async/await

### Backend-Specific Checks

- [ ] CQRS patterns followed correctly
- [ ] Repository usage (no direct DbContext access)
- [ ] Entity DTO mapping patterns
- [ ] Validation using PlatformValidationResult

### Frontend-Specific Checks

- [ ] Component base class inheritance correct (AppBase*)
- [ ] State management via PlatformVmStore
- [ ] Memory leaks (missing .pipe(this.untilDestroyed()))
- [ ] BEM classes on ALL template elements

### Common Anti-Patterns to Flag

- [ ] Unused imports or variables
- [ ] Console.log/Debug.WriteLine left in code
- [ ] Hardcoded values that should be configuration
- [ ] Missing async/await keywords
- [ ] Incorrect exception handling
- [ ] Missing validation

---

## Phase 2: Holistic Review (Review the Accumulated Report)

After ALL files reviewed, **re-read the report** to see big picture:

- [ ] Overall technical approach makes sense?
- [ ] Solution architecture coherent as unified plan?
- [ ] New files in correct layers (Domain/Application/Presentation)?
- [ ] Logic in LOWEST appropriate layer?
- [ ] Backend: mapping in Command/DTO (not Handler)?
- [ ] Frontend: constants/columns in Model (not Component)?
- [ ] No duplicated logic across changes?
- [ ] Service boundaries respected?
- [ ] No circular dependencies?

---

## Phase 3: Generate Final Review Result

Update report with final sections:

### Output Format

**Summary:** Brief overall assessment of the changes

**Critical Issues:** (Must fix before commit)

- Issue 1: Description and suggested fix
- Issue 2: Description and suggested fix

**Warnings:** (Should consider fixing)

- Warning 1: Description
- Warning 2: Description

**Suggestions:** (Nice to have)

- Suggestion 1
- Suggestion 2

**Positive Notes:**

- What was done well

**Architecture Recommendations:** (If applicable)

- Recommendation 1

**Suggested Commit Message:** Based on changes (conventional commit format)

```
<type>(<scope>): <description>

<body - what and why>
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
