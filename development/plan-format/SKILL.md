---
name: plan-format
description: This skill should be used when creating plan files, writing Gherkin requirements, generating tasks with verification commands, or parsing plan file structure. Provides the plan file template and format specifications.
version: 0.1.0
---

# Plan File Format

Specification for plan files used by the tommymorgan plugin. Plan files capture feature requirements as Gherkin scenarios and tasks with verification commands.

## Plan File Purpose

Plan files serve as the single source of truth for feature development:
- Capture requirements as executable Gherkin scenarios
- Define tasks with verification commands that prove completion
- Track progress across Claude sessions
- Enable autonomous TDD execution

## File Location

Plan files live in the project's plans directory:

```
<project>/plans/YYYY-MM-DD-<slug>.md
```

Where:
- `<project>` is the project path (e.g., `apps/web`, `libs/shared`, `tools/cli`)
- `YYYY-MM-DD` is the creation date
- `<slug>` is a kebab-case version of the feature name

Example: `apps/web/plans/2024-12-15-user-authentication.md`

## Plan File Template

```markdown
# Feature: <Title>

**Created**: YYYY-MM-DD
**Branch**: feat/<slug>
**Goal**: <One-sentence description of user-facing outcome>

## Requirements

Feature: <Feature Name>
  Scenario: <Scenario name>
    Given <precondition>
    When <action>
    Then <expected outcome>
    And <additional outcome>

  Scenario: <Another scenario>
    Given <precondition>
    When <action>
    Then <expected outcome>

## Tasks

### 1. <Task description>
**Verify**: `<command that exits 0 on success>`
**Status**: pending

### 2. <Task description>
**Verify**: `<command>`
**Status**: pending

### N. Refactor tests for maintainability
**Verify**: `<full test suite command>`
**Status**: pending
**Notes**: Reorganize from implementation-coupled to feature-focused tests

## Notes

<Design decisions, constraints, and context for future sessions>
```

## Section Specifications

### Header Section

**Required fields:**
- `**Created**`: Date in YYYY-MM-DD format
- `**Branch**`: Git branch name, typically `feat/<slug>`
- `**Goal**`: Single sentence describing user-facing outcome

### Requirements Section

Write Gherkin scenarios that fully capture the feature requirements.

**Gherkin syntax:**
- `Feature:` - Groups related scenarios
- `Scenario:` - Specific behavior to test
- `Given` - Preconditions/setup
- `When` - Action being tested
- `Then` - Expected outcome
- `And` - Additional conditions

**Coverage requirements:**
- Happy path scenarios (successful operations)
- Error cases (invalid input, failures)
- Edge cases (boundaries, empty states)
- Security considerations (authorization, validation)

**Writing tips:**
- Use concrete values in examples ("user@example.com" not "an email")
- One behavior per scenario
- Focus on user-observable outcomes
- Avoid implementation details in scenarios

### Tasks Section

Each task maps 1:1 with a test file. Task format:

```markdown
### N. <Task description>
**Verify**: `<verification command>`
**Status**: pending|complete|blocked
```

**Verification command requirements:**
- Must exit 0 on success, non-zero on failure
- Typically runs a specific test file
- Must be deterministic and repeatable

**Common verification patterns:**
- TypeScript/JavaScript: `pnpm test src/path/to/test.test.ts`
- Python: `pytest src/path/to/test_file.py`
- Go: `go test ./path/to/package -run TestName`
- Rust: `cargo test test_name`

**Status values:**
- `pending` - Task not yet completed
- `complete` - Verification command passes
- `blocked` - Cannot proceed, includes root cause

**For blocked tasks, add root cause:**
```markdown
### 3. Add authentication middleware
**Verify**: `pnpm test src/middleware/auth.test.ts`
**Status**: blocked
**Root Cause**: Requires JWT library upgrade in shared-lib, out of scope for this feature.
```

**Final task requirement:**
Every plan must end with a test refactoring task:
```markdown
### N. Refactor tests for maintainability
**Verify**: `<full test suite command>`
**Status**: pending
**Notes**: Reorganize from implementation-coupled to feature-focused tests
```

### Notes Section

Preserve context for future sessions:
- Design decisions and rationale
- Constraints and dependencies
- Implementation approach chosen
- Rejected alternatives and why
- Links to relevant documentation

## Parsing Plan Files

To extract tasks from a plan file:

1. Find lines matching `### \d+\. `
2. Extract description (text after number and period)
3. Find next line matching `**Verify**: \`(.+)\``
4. Extract command from backticks
5. Find next line matching `**Status**: (.+)`
6. Extract status value

To update task status:

1. Locate the specific task by number
2. Find the `**Status**: ` line
3. Replace status value (pending → complete)
4. Preserve all other content

## Validation Rules

**Plan file validation:**
- [ ] Has title starting with `# Feature:`
- [ ] Has Created, Branch, Goal header fields
- [ ] Has Requirements section with Gherkin scenarios
- [ ] Has Tasks section with numbered tasks
- [ ] Each task has Verify and Status fields
- [ ] Verification commands are in backticks
- [ ] Status values are valid (pending|complete|blocked)
- [ ] Final task is test refactoring

**Gherkin validation:**
- [ ] At least one Feature block
- [ ] Each Scenario has Given/When/Then
- [ ] Scenarios are independent
- [ ] No implementation details in scenarios

## Example Plan File

See `references/example-plan.md` for a complete working example.
