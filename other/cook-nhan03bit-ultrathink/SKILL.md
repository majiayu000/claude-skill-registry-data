---
name: cook
description: End-to-end feature builder that orchestrates the full lifecycle from planning through research, scouting, coding, testing, review, and shipping a feature.
layer: orchestrator
category: orchestration
triggers:
  - "/cook"
  - "cook a feature"
  - "build this feature end to end"
  - "implement this feature completely"
  - "full feature build"
inputs:
  - Feature description or user story
  - Optional acceptance criteria
  - Optional target branch or module
  - Optional priority level
outputs:
  - Completed, tested, reviewed feature code
  - Generated tests covering the feature
  - Code review summary with any resolved issues
  - Commit(s) ready to merge or ship
linksTo:
  - plan
  - research
  - scout
  - code-review
  - test
  - fix
  - refactor
  - optimize
  - sequential-thinking
  - git-workflow
  - commit-crafter
  - pr-writer
  - changelog-writer
  - docs-writer
linkedFrom:
  - team
  - kanban
preferredNextSkills:
  - ship
  - pr-writer
  - changelog-writer
fallbackSkills:
  - plan
  - debug
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: always
sideEffects:
  - Creates or modifies source files
  - Creates or modifies test files
  - Creates git commits
  - May create or update documentation
---

# Cook

## Purpose

Cook is the end-to-end feature builder orchestrator. It takes a feature request, user story, or task description and drives it through every stage of development -- from initial planning and research all the way through coding, testing, code review, and preparing to ship. Think of it as the "chef" that coordinates the entire kitchen: it delegates specialized work to hub and utility skills while maintaining the big picture.

Cook ensures that no step is skipped. Features built through Cook always have a plan, are informed by research, follow existing codebase patterns, include tests, pass review, and are commit-ready.

## Workflow

### Phase 1: Understand & Plan
1. **Parse the request** -- Extract the core feature, constraints, acceptance criteria, and scope from the user's input.
2. **Invoke `plan`** -- Generate a structured implementation plan with milestones, dependencies, and risk flags.
3. **Invoke `research`** (if needed) -- Look up library docs, API references, or patterns via Context7 or web search when the feature touches unfamiliar territory.
4. **Invoke `sequential-thinking`** (if complex) -- For multi-step logic or architectural decisions, use structured reasoning to resolve ambiguity before writing code.

### Phase 2: Scout & Prepare
5. **Invoke `scout`** -- Scan the codebase for related files, existing patterns, naming conventions, and integration points. Identify where the new code should live and what it should conform to.
6. **Summarize findings** -- Present a brief to the user: "Here's the plan, here's what I found in the codebase, here's my approach." Wait for confirmation if the task is high-risk or ambiguous.

### Phase 3: Implement
7. **Write the code** -- Implement the feature following the plan, adhering to patterns discovered by `scout`, and respecting all project guidelines (single responsibility, separation of concerns, DRY).
8. **Invoke `refactor`** (if needed) -- If existing code must be restructured to accommodate the feature cleanly, delegate refactoring to the refactor skill.
9. **Invoke `optimize`** (if needed) -- If the implementation has obvious performance concerns, run optimization passes.

### Phase 4: Test
10. **Invoke `test`** -- Generate and run tests for the new feature. This includes unit tests, integration tests if applicable, and edge-case coverage.
11. **Fix failures** -- If tests fail, invoke `fix` or `debug` to resolve issues. Re-run tests until green.

### Phase 5: Review
12. **Invoke `code-review`** -- Run a self-review pass on all changed files. Check for code quality, security issues, adherence to project patterns, and completeness against the original plan.
13. **Address review findings** -- Fix any issues surfaced by review. Re-review if changes were significant.

### Phase 6: Prepare to Ship
14. **Invoke `commit-crafter`** -- Create well-structured commit(s) with meaningful messages.
15. **Invoke `docs-writer`** (if needed) -- Update or create documentation if the feature warrants it.
16. **Report completion** -- Present a summary of what was built, what was tested, and what's ready to ship. Suggest invoking `ship` or `pr-writer` as the next step.

## Decision Points

| Condition | Action |
|-----------|--------|
| Feature touches unknown library | Invoke `research` before coding |
| Feature requires architectural change | Invoke `sequential-thinking` then confirm with user |
| Existing code needs restructuring | Invoke `refactor` before or during implementation |
| Tests fail after implementation | Invoke `fix` or `debug`, then re-test |
| Review surfaces critical issues | Fix and re-review before proceeding |
| Feature is trivial (< 20 lines) | Skip `plan` formal output, still scout and test |

## Usage

Use Cook when you have a well-defined feature or task and want it handled completely. Cook is the default choice for "build this thing" requests.

**Best for:**
- New features with clear requirements
- Bug fixes that need proper test coverage
- Enhancements to existing features
- Tasks where you want the full quality pipeline

**Not ideal for:**
- Pure exploration or research (use `research` or `brainstorm` directly)
- Release management (use `ship`)
- Codebase audits (use `audit`)
- Multi-team coordination (use `team` to orchestrate multiple cooks)

## Examples

### Example 1: Simple feature
```
User: /cook Add a dark mode toggle to the settings page

Cook workflow:
1. plan -> Identify settings page location, toggle component needs, theme system
2. scout -> Find existing theme files, settings page components, CSS variables
3. Implement -> Create toggle component, wire up theme context, add CSS variables
4. test -> Unit test toggle behavior, integration test with settings page
5. code-review -> Check accessibility, contrast ratios, state persistence
6. commit-crafter -> "Add dark mode toggle to settings page"
```

### Example 2: Complex feature
```
User: /cook Implement real-time collaborative editing for document pages

Cook workflow:
1. plan -> Architecture decision (WebSocket vs SSE), conflict resolution strategy
2. research -> Look up CRDT libraries, WebSocket patterns via Context7
3. sequential-thinking -> Resolve operational transform vs CRDT trade-offs
4. scout -> Find document model, existing API routes, auth middleware
5. Implement -> WebSocket server, CRDT integration, cursor presence UI
6. refactor -> Restructure document save flow to support real-time
7. test -> Unit tests for CRDT ops, integration tests for sync
8. code-review -> Security review of WebSocket auth, performance review
9. commit-crafter -> Series of atomic commits for each component
10. docs-writer -> Update API docs with WebSocket endpoints
```

### Example 3: Bug fix
```
User: /cook Fix the login form not validating email addresses properly

Cook workflow:
1. scout -> Find login form component, existing validation logic
2. plan -> Identify the validation gap, plan the fix
3. Implement -> Fix email regex or validation library usage
4. test -> Add test cases for valid/invalid emails, edge cases
5. code-review -> Verify fix doesn't break other validation
6. commit-crafter -> "Fix email validation in login form"
```

## Guardrails

- **Always scout before coding.** Never write code without understanding the codebase context.
- **Always test.** No feature ships from Cook without at least unit-level test coverage.
- **Always review.** Even small changes get a code-review pass.
- **Respect the plan.** If the plan said 3 files, don't touch 12 without re-planning.
- **Ask when uncertain.** If a decision is ambiguous and high-impact, surface it to the user rather than guessing.
