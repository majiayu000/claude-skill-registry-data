---
name: critical-code-review
description: Perform critical code review with automated fix suggestions. Use when reviewing code changes, pull requests, specific files, or branch diffs. Triggers on requests like "review this code", "critical review", "code review for PR #123", or "review changes in src/". Optionally uses Codex CLI for secondary review when available.
---

# Critical Code Review

Perform context-aware critical code review with integrated fix execution.

## Review Targets

- Specific file: `src/main.ts`
- Branch diff: `main..feature/new-api`
- Recent commit: `HEAD~1..HEAD`
- Directory: `src/`
- PR: `#123`
- No argument: diff between current branch and base (main/master/develop)

## Target Resolution

1. If argument provided: use as review target
2. If no argument:
   - Get current branch: `git branch --show-current`
   - Find base branch (priority: main, master, develop)
   - Review diff: `git diff <base>...HEAD`
   - Include unstaged changes

## Review Context (Determine First)

- **Project phase**: MVP/Development/Production/Refactoring
- **Priority**: Performance/Maintainability/Extensibility
- **Tech stack**: Languages/Frameworks/Paradigms
- **File type**: Backend/Frontend/UI Component/Database/Infrastructure

## Review Criteria

### 🔴 High Priority (Critical)

1. **Security risks**: SQL/XSS injection, auth flaws, secret exposure
2. **Data corruption**: Transaction failures, race conditions, improper locking
3. **System failure**: Unhandled exceptions, resource leaks, infinite loops

### 🟡 Medium Priority (Design Quality)

1. **Type safety & Domain Modeling**: Primitive obsession, invalid state representation, missing smart constructors
2. **Functional programming violations**: Side effects, missing Result types, mutability
3. **Design principle deviations**: SOLID violations, high coupling, low cohesion
4. **Domain model inconsistencies**: Misrepresented business rules, ambiguous boundaries
5. **Maintainability issues**: Untestable design, missing documentation, implicit assumptions

### 🟢 Low Priority (Improvements)

1. **Efficiency**: N+1 queries, unnecessary computation, cache opportunities
2. **Code quality**: Duplication, naming, readability

### 🎨 UI/Frontend Specific

1. **UI state management**: Invalid state combinations, missing loading/error states
2. **Accessibility**: Missing ARIA, keyboard navigation, color-dependent information
3. **Responsive design**: Hardcoded sizes, mobile support, breakpoint inconsistencies
4. **Component boundaries**: Props drilling, excessive responsibility
5. **UI performance**: Unnecessary re-renders, heavy components, missing virtualization

## Review Process

- Perform self review and Codex review in parallel when feasible to reduce latency.

1. **Self review**: Perform critical review based on criteria above
2. **Codex review (required when tool available)**: Request review via `mcp__codex-cli__codex` tool with context. If unavailable, explicitly note it.
3. **Integrate results**: Combine self review and Codex review into final issue list
4. **Present results**: Output in the format below only after Codex review is completed or confirmed unavailable

## Heuristic Review Guidance

- Understand context, intent, and constraints before judging
- Imagine the code's evolution over the next year
- Use domain knowledge to validate business logic
- Look beyond the listed categories and report issues of equivalent severity

## Output Format

````markdown
### 🔴/🟡/🟢 [Criterion Name]
**Issue**:
- Location (file:line)
- Detailed description

**Impact**:
- Technical: Bug/Performance degradation/Maintainability
- Business: User experience/Development velocity/Cost

**Fix**:
```[language]
// Specific fix code
```
````

## Output Constraints

- **Issue count**: Max 5 by priority (guideline: 🔴2, 🟡2, 🟢1). If critical issues are numerous, adjust upward while keeping prioritization.
- **Specificity**: Include file:line, provide code examples
- **Conciseness**: Consider CLI display, be clear
- **Practicality**: Provide realistic, implementable fixes

## Post-Review Fix Flow

After presenting review results, display:

```
## 🔧 Fix Options

Execute fixes? (y/n/select)
- y: Execute all
- n: Exit without fixing
- select: Choose items to fix

Selection:
```

### Fix Item Organization

```markdown
## 🔧 Planned Fixes

### Auto-fix Items (🔴 Critical)
1. [Issue name] - file:line
   - Issue: [Brief description]
   - Fix: [What will be changed]

### Items Requiring Confirmation (🟡 Design / 🔵 Other)
2. [Issue name] - file:line
   - Issue: [Brief description]
   - Proposed fix: [Suggestion]
   - Impact scope: [Other file impacts]

### Skip Items (🟢 Suggestions)
3. [Issue name] - file:line (Manual fix recommended)
```

Ensure every item is numbered so the user can select them easily.

### Item Selection (when `select`)

```
Enter item numbers to fix (comma-separated):
Example: 1,2,4
```

### Fix Execution

#### Fix Validation Criteria

- **Impact scope**: Trace dependencies and identify side effects
- **Correctness**: Ensure expected behavior is preserved
- **Testability**: Ensure the fix can be verified by tests
- **Mathematical verification (when algorithms change)**: Check complexity, concurrency safety, and invariants

#### Pre-fix Verification

- Confirm current file state
- Verify fix code fits context
- Consider impacts on other parts

#### Fix Application

- **Minimal changes**: Only changes needed to solve the issue
- **Maintain consistency**: Preserve existing code style, naming, indentation
- **Check imports**: Add new dependencies appropriately
- **Type consistency**: Ensure type integrity
- **Backward compatibility**: Clarify impact when behavior/API changes
- **Naming conventions**: Follow existing project rules
- **Avoid magic numbers**: Prefer named constants with intent
- **Comments for complexity**: Add concise comments only when needed

#### Quality Check

- **Syntax errors**: Ensure no syntax errors after fix
- **Logical consistency**: Ensure fix doesn't introduce new issues
- **Edge cases**: Ensure proper boundary and error handling
- **Performance impact**: Ensure no performance degradation

#### Test Implementation/Update

- **Check existing tests**: Identify tests related to fix location
- **Update tests**: Update tests that fail due to fix
- **Add new tests**: Add regression tests for bug fixes, cover normal/error cases for new features
- **Test-first when feasible**: Prefer writing a failing test before applying the fix

### Fix Report

```markdown
## ✅ Fix Complete Report

### Successful Fixes
- ✅ [Issue name] - file:line
  - Changes: [Actual changes made]

### Failed Fixes
- ❌ [Issue name] - file:line
  - Error: [Failure reason]
  - Workaround: [Manual fix instructions]

### Next Steps
1. **Run tests (Required)**: Verify all tests pass
2. Run lint/format if defined
3. Run type checks if applicable
4. Provide manual test steps for uncovered flows
5. Confirm changes with `git diff`
6. Check test coverage report
7. Restore with `git checkout -- <file>` if needed
```

### Error Handling

- Do not apply fixes that fail
- Partial success is acceptable; report clearly what was applied
- Report all errors with actionable guidance

## Codex Review Integration

When `mcp__codex-cli__codex` tool is available, request secondary review:

```
Perform critical code review on the following code changes.
Focus on: security risks, data integrity, design quality, and maintainability.
Provide specific issues with file:line locations and fix suggestions.

[Include code diff or file content]
```

If the tool is unavailable but the Codex CLI is available, use:

```
codex exec -m gpt-codex-5.2 -c reasoning_effort=xhigh "Perform critical code review on the following code changes. [Include diff or file content]"
```

Integrate Codex findings with self review, removing duplicates and prioritizing by severity.
