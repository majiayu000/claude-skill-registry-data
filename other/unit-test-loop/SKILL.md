---
name: unit-test-loop
description: |
  This skill should be used when the user asks to "improve test coverage",
  "add unit tests", "TDD", "test this module", "write tests for", "increase
  coverage", "/ut command", or discusses unit testing strategies. Covers the
  unit test loop workflow, React Testing Library best practices, query
  priorities, and coverage improvement strategies.
version: 2.0.0
---

# Unit Test Loop - Coverage Improvement

**Current branch:** !`git branch --show-current 2>/dev/null || echo "not in git repo"`

The unit test loop uses a 2-phase workflow with Dex task tracking for
persistent, cross-session test coverage improvement.

## The 2-Phase Approach

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | Coverage Analysis | Identify gaps, prioritize files |
| 2 | Dex Handoff | Create epic + tasks from analysis |

After Phase 2, use `/complete <task-id>` for each test task.

## Starting the Loop

```bash
/ut "Improve coverage for auth module"            # Basic
/ut "Add tests" --target 80%                      # With target
```

## Phase 1: Coverage Analysis

1. Run coverage command to see current state
2. Identify files with low coverage
3. Prioritize 3-7 test tasks for user-facing behavior

**Output:** `<phase_complete phase="1"/>`

## Phase 2: Dex Handoff

Create Dex epic with target, then tasks for each gap:

```bash
# Create epic
dex create "Unit Test Coverage" --description "Target: 80% coverage"

# For each gap
dex create "Test: login validation" --parent <epic-id> --description "
File: src/auth/login.ts
Current: 45%

Test should verify:
- [ ] Valid credentials succeed
- [ ] Invalid credentials show error
"
```

**Output:** `<phase_complete phase="2"/>` or `<promise>UT SETUP COMPLETE</promise>`

## Working on Tasks

Use Dex + /complete workflow:

```bash
dex list --pending      # See what's ready
dex start <id>          # Start working
/complete <id>          # Run reviewers and complete
```

## React Testing Library Patterns

> "The more your tests resemble the way your software is used,
> the more confidence they can give you."

### Query Priority (Use in Order)

| Priority | Query | Use Case |
|----------|-------|----------|
| 1 | `getByRole` | Default choice, use `name` option |
| 2 | `getByLabelText` | Form fields with labels |
| 3 | `getByPlaceholderText` | Only if no label available |
| 4 | `getByText` | Non-interactive elements |
| 5 | `getByTestId` | **Last resort only** |

### Query Types

| Type | When to Use |
|------|-------------|
| `getBy`/`getAllBy` | Element exists (throws if not found) |
| `queryBy`/`queryAllBy` | **Only** for asserting absence |
| `findBy`/`findAllBy` | Async elements (returns Promise) |

### Best Practices

```typescript
// Use screen
screen.getByRole('button', { name: /submit/i })

// Use userEvent.setup()
const user = userEvent.setup()
await user.click(button)

// Use jest-dom matchers
expect(button).toBeDisabled()  // Not: expect(button.disabled).toBe(true)

// Avoid act() - RTL handles it
await screen.findByText('Loaded')  // Not: act(() => ...)
```

## Quality Standards

- **ONE test per task** - Focused, reviewable commits
- **User-facing behavior only** - Test what users depend on
- **Quality over quantity** - One great test beats ten shallow ones
- **No coverage gaming** - Use `/* v8 ignore */` for untestable code

## Command Reference

```bash
/ut "prompt"                  # Start analysis
/ut "prompt" --target 80%     # With target
/cancel-ut                    # Cancel loop
/complete <task-id>           # Complete task with reviewers
```

## Related

- `/complete` - Run reviewers and mark Dex task complete
- `dex list` - View pending tasks
- `dex-workflow` skill - Full Dex usage patterns
