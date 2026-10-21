---
name: dev-workflow
description: Valid workflow state transitions for TDD feature/defect development. Use when determining which building block to invoke next in a development workflow.
---

## TDD Development State Machine

### From context-collector
- ✅ Next: planner
- ❌ Invalid: Any other building block (context must be collected first)

### From planner
- ✅ Next: reviewer (plan review mode)
- ❌ Invalid: test-writer, implementor (plan must be reviewed first)

### From reviewer (plan review)
- ✅ Next: test-writer Phase 1 (if approved)
- ✅ Next: planner (if changes needed)
- ❌ Invalid: implementor (tests must exist first — TDD)

### From test-writer Phase 1
- ✅ Next: test-writer Phase 2 (after user approves strategy)
- ❌ Invalid: Any other building block (strategy must be approved first)

### From test-writer Phase 2
- ✅ Next: test-runner (red phase — verify tests fail)
- ❌ Invalid: implementor (must verify tests fail first)

### From test-runner (red phase)
- ✅ Next: implementor (if tests fail as expected — missing implementation)
- ✅ Next: test-writer (if tests fail unexpectedly — syntax/setup errors)
- ❌ Invalid: reviewer (implementation not done yet)

### From implementor
- ✅ Next: test-runner (green phase — verify tests pass)
- ❌ Invalid: pr-creator (must verify tests pass first)

### From test-runner (green phase)
- ✅ Next: reviewer (code review mode)
- ✅ Next: implementor (if tests still failing)
- ❌ Invalid: pr-creator (must have code review first)

### From reviewer (code review)
- ✅ Next: pr-creator (if approved)
- ✅ Next: implementor (for code issues)
- ✅ Next: test-writer (for test issues)

### From pr-creator
- ✅ Next: none (workflow complete)

## Invalid Transitions
- Never skip context-collector
- Never implement before tests exist (TDD violation)
- Never go to pr-creator without reviewer approval
