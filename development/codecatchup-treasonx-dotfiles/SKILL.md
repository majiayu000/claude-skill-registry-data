---
name: codecatchup
description: Reviews git history to summarize changes merged while you were away from a consulting project, identifying PRs, code changes, and potential concerns to discuss with the development team.
---

# Code Catchup Guide

## Overview
This skill helps consultants review changes made to a project during their absence. It analyzes git history to identify merged changes, associated pull requests, and flags potential code quality or architectural concerns that warrant discussion with the development team.

## Scope
By default, analyze the current directory as the project root. Users can specify a different directory if needed.

## Output
Generate a code catchup report and write it to `@docs/code-catchup.md` in the project directory.

## Time Range Determination

### Finding Your Last Commit
1. Get the current git user configuration:
   ```bash
   git config user.name
   git config user.email
   ```

2. Find your most recent commit on main/master:
   ```bash
   git log main --author="<email>" --format="%H %ai" -1
   ```
   OR if main doesn't exist:
   ```bash
   git log master --author="<email>" --format="%H %ai" -1
   ```

3. **Start Date**: Use the date of your last commit
4. **End Date**: Use today's date (current date)
5. **Fallback**: If no commits from you are found in recent history, analyze the last 30 days

### Branch Detection
- Check if `main` branch exists, otherwise use `master`
- Command: `git rev-parse --verify main` (exit code 0 = exists)

## Analysis Process

### Step 1: Get Commit History
1. Retrieve all commits in the time range on main/master:
   ```bash
   git log main --since="<start-date>" --until="<end-date>" --format="%H|%an|%ae|%ai|%s" --no-merges
   ```

2. For merge commits specifically (to find PRs):
   ```bash
   git log main --since="<start-date>" --until="<end-date>" --merges --format="%H|%an|%ae|%ai|%s"
   ```

3. Extract information:
   - Commit hash
   - Author name
   - Author email
   - Commit date
   - Commit message

### Step 2: Identify Pull Requests
Extract PR numbers from commit messages using patterns like:
- "Merge pull request #123"
- "PR #123"
- "#123" in merge commits
- "(#123)" at end of messages

### Step 3: Determine GitHub Repository
Get the remote URL to build PR links:
```bash
git remote get-url origin
```

Parse to extract owner and repo:
- SSH format: `git@github.com:owner/repo.git`
- HTTPS format: `https://github.com/owner/repo.git`

Build PR URLs: `https://github.com/{owner}/{repo}/pull/{number}`

### Step 4: Analyze Each Commit's Changes

For each commit in the time range:

1. **Get changed files**:
   ```bash
   git show --stat --format="" <commit-hash>
   ```

2. **Get actual code diff**:
   ```bash
   git show <commit-hash>
   ```

3. **Analyze the diff** for:

#### Code Quality Issues
- **Poor error handling**:
  - Try/catch blocks that catch generic exceptions without handling
  - Missing error handling around risky operations (network, file I/O, parsing)
  - Swallowed exceptions (empty catch blocks)
  - No validation before operations

- **Lack of validation**:
  - Missing input validation
  - No null/undefined checks
  - Missing type checking in dynamic languages
  - Unvalidated user input used directly

- **Code duplication**:
  - Similar code blocks copied across files
  - Repeated logic that could be extracted
  - Duplicated constants or configuration

- **Overly complex logic**:
  - Deeply nested conditionals (>3 levels)
  - Long functions (>50 lines)
  - Complex boolean expressions
  - Methods with too many parameters (>4)

#### Architectural Concerns
- **Breaking changes**:
  - Modified public API signatures
  - Removed public methods/functions
  - Changed return types
  - Modified database schemas without migrations

- **Tight coupling**:
  - New direct dependencies between modules
  - Hardcoded references to specific implementations
  - Global state access

- **Missing abstractions**:
  - Business logic mixed with framework code
  - Database queries in UI/presentation layer
  - No interfaces for external dependencies

- **Unclear responsibilities**:
  - Classes/modules doing multiple unrelated things
  - Mixed concerns (e.g., UI rendering + business logic)
  - Lack of separation of concerns

### Step 5: Calculate Statistics
- Total commits analyzed
- Total PRs merged
- Total files changed
- Lines added/removed
- Most frequently changed files
- Most active contributors
- Breakdown by commit type (feature, fix, refactor, etc.)

## Report Format

Structure the output document (`@docs/code-catchup.md`) as follows:

```markdown
# Code Catchup Report
Generated: [Date]
Period: [Start Date] to [End Date]

## Executive Summary
- **Total Commits**: [number]
- **Pull Requests Merged**: [number]
- **Files Changed**: [number]
- **Lines Added**: [number]
- **Lines Removed**: [number]
- **Active Contributors**: [number]
- **Concerns Flagged**: [number]

## High-Level Overview
[2-3 paragraph summary of major changes, themes, and overall activity during the period]

## Pull Requests Merged

| PR # | Author | Date | Title | Status |
|------|--------|------|-------|--------|
| [#123](https://github.com/owner/repo/pull/123) | John Doe | 2024-10-15 | Add user authentication | ⚠️ Concerns |
| [#124](https://github.com/owner/repo/pull/124) | Jane Smith | 2024-10-16 | Fix login bug | ✅ Clean |

## Detailed Analysis

### PR #123: Add user authentication
- **Author**: John Doe (john@example.com)
- **Merged**: 2024-10-15
- **Link**: https://github.com/owner/repo/pull/123
- **Files Changed**: 12 files (+450, -120 lines)

#### Changes Overview
[Brief description of what this PR does]

#### Key Files Modified
- `src/auth/login.ts`: New authentication logic
- `src/middleware/auth.ts`: JWT validation middleware
- `config/security.ts`: Security configuration

#### Concerns Flagged 🚩

##### Code Quality Issue: Poor Error Handling
**Location**: `src/auth/login.ts:45-60`
**Severity**: Medium

**Issue**: The login function catches all exceptions but doesn't differentiate between authentication failures and system errors. This makes debugging difficult and could leak sensitive error information.

```typescript
try {
  await authenticateUser(username, password);
} catch (error) {
  return { success: false, message: 'Login failed' };
}
```

**Recommendation**: Implement specific error handling for different failure scenarios (invalid credentials, network issues, database errors).

**Discussion Points**:
- Should we have separate error codes for different failure types?
- Is there logging for failed login attempts?

---

##### Architectural Concern: Tight Coupling
**Location**: `src/components/LoginForm.tsx:120`
**Severity**: High

**Issue**: The UI component directly imports and calls the authentication service, creating tight coupling between presentation and business logic layers.

```typescript
import { authService } from '../../services/auth';
// ...
const result = await authService.login(username, password);
```

**Recommendation**: Use dependency injection or a hook pattern to decouple the component from the concrete service implementation.

**Discussion Points**:
- Is there a pattern already established for service access in components?
- Should we introduce a custom hook like `useAuth()`?

---

[Repeat for each concern in this PR]

---

### PR #124: Fix login bug
[Same structure as above]

## Activity Statistics

### Most Active Areas
| Directory/Component | Commits | Files Changed | Lines Modified |
|---------------------|---------|---------------|----------------|
| src/auth/ | 8 | 15 | +620, -340 |
| src/api/ | 5 | 8 | +230, -120 |
| tests/ | 12 | 20 | +890, -450 |

### Most Changed Files
1. `src/auth/login.ts` - 6 changes
2. `src/middleware/auth.ts` - 5 changes
3. `tests/auth.test.ts` - 8 changes

### Contributors Activity
| Developer | Commits | PRs | Lines Changed |
|-----------|---------|-----|---------------|
| John Doe | 15 | 4 | +1200, -450 |
| Jane Smith | 10 | 3 | +800, -320 |

### Commit Themes
- **Features**: 8 commits (new authentication, user profile)
- **Bug Fixes**: 12 commits (login issues, validation bugs)
- **Refactoring**: 5 commits (code cleanup, test improvements)
- **Documentation**: 2 commits

## Summary of Concerns

### High Priority (Discuss ASAP)
1. **Tight coupling in authentication flow** - PR #123
   - Impacts: Testability, maintainability
   - Files: `src/components/LoginForm.tsx`, `src/pages/Dashboard.tsx`

2. **Missing error handling in API layer** - PR #126
   - Impacts: User experience, debugging
   - Files: `src/api/users.ts`, `src/api/posts.ts`

### Medium Priority (Review when convenient)
1. **Code duplication in validation logic** - Multiple PRs
   - Affects: Maintainability
   - Files: Several validation files

2. **Complex conditional logic** - PR #125
   - Affects: Readability
   - Files: `src/utils/permissions.ts`

### Low Priority (Minor observations)
1. **Inconsistent naming conventions** - Various commits
2. **Missing JSDoc comments** - PR #123, #124

## Questions for the Team

Based on the analysis, here are suggested discussion points:

### For PR #123 (Authentication)
- [ ] What's the strategy for handling different types of auth failures?
- [ ] Should we implement rate limiting for login attempts?
- [ ] Is the JWT secret configuration properly externalized?

### For PR #126 (API Refactor)
- [ ] Why was the error handling approach changed?
- [ ] Are there integration tests covering the new error scenarios?
- [ ] What's the plan for migrating existing error handling?

### General Architecture
- [ ] Is there a documented pattern for service access in components?
- [ ] Should we establish coding standards for error handling?
- [ ] Are we tracking technical debt items anywhere?

## Recommended Next Steps

1. **Review High Priority Concerns**: Schedule time with John Doe to discuss authentication coupling
2. **Code Review**: Deep dive into error handling changes in PR #126
3. **Team Discussion**: Propose error handling standards in next team meeting
4. **Documentation**: Update architecture docs with authentication flow
5. **Testing**: Review test coverage for new authentication features

## Notes
- Analysis based on commits from [start-date] to [end-date]
- Flagged concerns are suggestions for discussion, not definitive issues
- Context from PRs and discussions may provide additional justification
- This is an automated analysis; manual code review is still recommended for critical changes
```

## Important Guidelines

### Read-Only Operation
- **MUST NOT** modify any code files
- **MUST NOT** run builds, tests, or other state-changing commands
- **MUST NOT** create commits or modify git history
- **ONLY** read git history and code diffs

### Analysis Approach
- **Be objective**: Flag patterns that could be issues, but acknowledge context might justify them
- **Be specific**: Always include file paths and line numbers
- **Be constructive**: Frame concerns as discussion points, not accusations
- **Be thorough**: Review actual code diffs, not just commit messages
- **Be balanced**: Note both concerns and well-implemented changes

### Tone and Framing
- Frame findings as "concerns to discuss" not "mistakes" or "bad code"
- Use phrases like:
  - "Consider discussing..."
  - "May want to review..."
  - "Potential concern..."
  - "Worth clarifying..."
- Remember: You're a consultant reviewing changes, not criticizing the team

### GitHub Integration
- Extract repository information from git remote
- Generate valid PR URLs
- Handle cases where PR numbers aren't available
- Note when commits aren't linked to PRs

### Error Handling
- Handle missing git configuration gracefully
- Work with both `main` and `master` branches
- Handle repositories without PR references
- Provide useful output even if some information is unavailable

## Completion Criteria
- Time range has been correctly determined
- All commits in range have been analyzed
- PR information has been extracted and linked
- Code diffs have been examined for concerns
- Statistics have been calculated
- Report has been written to `@docs/code-catchup.md`
- Report includes specific, actionable discussion points
- User is notified that the code catchup analysis is complete

## Future Enhancements
As you use this skill, you may want to refine:
- The specific patterns that constitute "code quality issues"
- The severity thresholds for flagging concerns
- Additional categories of concerns to track
- The level of detail in the analysis
- Integration with GitHub API for richer PR information
