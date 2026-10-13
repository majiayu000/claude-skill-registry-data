---
name: execute-task
description: "Execute a specified task by reading detailed specifications, analyzing requirements, planning the approach, and implementing step-by-step. Use this skill when: you have a task specification file or task ID that needs completion; the task is multi-step, involves architecture decisions, or requires tool orchestration; you need to track progress across subtasks and delegate work to specialist agents. Triggers on task execution requests, implementation assignments, feature builds, bug fixes, refactoring projects, or when a user provides a task spec .md file. Always use this skill for complex development work rather than tackling it directly —delegate to specialists and maintain progress visibility with task tracking."
argument-hint: "[task_id] - TaskMaster task ID (e.g., 'T1'), OR [spec_file] - Path to task specification markdown file"
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

## XP Principles

Execute-task follows Extreme Programming (XP) discipline to ensure quality deliverables:

- **Understand Problems Completely**: Read specs carefully; inspect sources; check architecture docs
- **Smallest Vertical Slices**: Break work into minimal, independently testable units
- **Test First (TDD)**: Write failing tests before implementation; cover happy paths, edge cases, errors
- **Simplest Solutions**: Implement only the minimum required; avoid premature abstraction
- **Full Test Suite**: Ensure new tests pass AND all existing tests pass; check no regressions
- **Safe Refactoring**: Improve structure while keeping tests green; remove duplication; maintain consistency
- **Documentation**: Update relevant \*.md files; reference related code for future maintenance
- **Code Review**: Verify test coverage, minimal scope, no unrelated changes, standards compliance
- **Final Validation**: Re-run full test suite; confirm backward compatibility and integration

## Workflow

The execute-task skill orchestrates work through this sequence:

### 1. **Load Task Context** (Understand the Problem)

- If `task_id` provided: Use `mcp-manager/taskmaster/get_task tool` to fetch full task definition (requirements, subtasks, context, links)
- If `spec_file` provided: Read the markdown file to extract requirements, acceptance criteria, and context
- If both: Get task via ID first (authoritative source), then cross-reference with spec file for additional context
- **Read specification carefully** until goal is completely clear
- **Inspect relevant source files and modules** involved in the change
- **Check \*.md documentation** for architectural guidelines and conventions
- **Identify dependencies, side effects, and impacted modules**

### 2. **Plan the Approach** (Define Smallest Deliverable)

- Use `sequentialthinking tool` to reason through requirements, dependencies, and edge cases
- Identify which modules/files are affected; check for existing patterns in the codebase
- **Break the work into the smallest possible vertical slice** — each slice produces a working, testable result
- **Ensure backward compatibility** with existing system flows
- Decompose the task into concrete subtasks (what needs to be built, tested, documented)
- Determine if specialist agents (developer-specialist, database-specialist, cybersecurity-specialist) are needed

### 3. **Create Progress Tracking** (Prepare for Test-First)

- Use `todo tool` to create explicit task breakdown with status tracking
- Mark tasks **in-progress** as you start each step
- Mark **completed** immediately after finishing (do not batch)
- **Reserve space in tracking for: failing tests, implementation, full test suite run, refactoring pass, documentation**
- Use this to maintain context and prevent losing work mid-task

### 4. **Execute with Test-First & Delegation**

#### 4a. Write Tests First (Test First - TDD)

- **Before any implementation**, write failing tests that describe expected behavior
- Cover: happy paths, edge cases, error conditions
- **Reference relevant files** using code references (file#L123-L456)
- Run tests to confirm they fail (proves test validity)

#### 4b. Implement Minimal Solution (Simplest Solution)

- Implement **only the minimum code** required to make tests pass
- Avoid premature abstractions
- Follow existing architectural conventions
- **Run full test suite** — ensure new tests pass AND all existing tests pass; validate no regressions

#### 4c. Refactor Safely (Safe Refactoring)

- Improve code structure while keeping tests green
- Remove duplication
- Improve naming and readability
- Ensure architecture consistency

#### 4d. Delegate When Appropriate

- **For complex refactoring/architecture**: Delegate to `developer-specialist` agent
- **For security concerns**: Escalate to `cybersecurity-specialist`
- **For data/performance**: Escalate to `database-specialist`
- **For patterns/architecture**: Escalate to `design-pattern-specialist`
- Provide agents with clear scope: what they own, what you'll verify
- Integrate their work back into the main execution flow

### 5. **Verify, Document & Final Validation**

- **Update all relevant \*.md documentation** files with architectural guidelines, new endpoints, or public interfaces
- **Reference related files and modules** useful for future maintenance
- After completing each subtask, verify it against acceptance criteria
- Check for regressions, missing edge cases, or incomplete integration
- **Run full test suite again** — confirm new tests pass, all existing tests pass, backward compatibility maintained
- **Confirm feature integrates correctly** with the rest of the system
- Update task status and capture any learnings for future iterations
- Maintain a clear record of what was done and why (for reviews/documentation)

## Good Signals This Skill Should Trigger

- User provides a task ID or task spec file
- Task involves multiple files, modules, or architectural decisions
- Task requires test coverage, refactoring, or performance analysis
- User says "build", "implement", "fix", "refactor", "complete this task"
- Progress needs to be tracked across multiple steps
- Engineering discipline required: TDD, smallest deliverables, test-first approach
- Work needs rigorous verification against acceptance criteria

## Anti-Patterns (Don't Do This)

- **Don't run code without understanding requirements first** — read specs entirely, inspect sources, check docs
- **Don't skip the plan step** — jumping straight to coding creates rework
- **Don't write code before tests** — tests should drive implementation (Test First / TDD)
- **Don't implement complex solutions** — build the simplest code that passes tests
- **Don't skip full test suite validation** — ensure new + existing tests all pass, no regressions
- **Don't mark all tasks complete at the end** — mark them complete as you go (progress visibility)
- **Don't ignore test failures or incomplete acceptance criteria** — these block validation
- **Don't try to do everything yourself** — delegate to specialist agents when their domain expertise applies
- **Don't lose context** — always use task tracking to stay oriented
- **Don't skip refactoring** — improve structure while tests stay green
- **Don't forget documentation** — update \*.md files and reference related code
- **Don't merge code without code review checklist** — verify test coverage, scope, standards
- **Don't drop verification step** — backward compatibility and integration must be confirmed
