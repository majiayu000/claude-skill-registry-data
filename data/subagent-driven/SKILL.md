---
name: subagent-driven
description: Execute implementation plans with structured subagent dispatch and two-stage review (spec compliance, then code quality). Based on obra/superpowers.
version: 1.0.0
category: development
last_updated: 2026-01-19
source: https://github.com/obra/superpowers
related_skills:
  - writing-plans
  - tdd-obra
  - code-reviewer
  - parallel-dispatch
---

# Subagent-Driven Development Skill

## Overview

This skill implements structured plan execution by dispatching independent subagents for each task, followed by mandatory two-stage reviews: specification compliance first, then code quality. Ensures systematic progress with quality gates.

## Quick Start

1. **Prepare plan** - Extract tasks to TodoWrite tracker
2. **For each task:**
   - Dispatch implementer subagent
   - Answer clarification questions
   - Run spec compliance review
   - Run code quality review
3. **Final review** - Comprehensive code review
4. **Complete** - Use finishing-a-development-branch

## When to Use

- Executing implementation plans with mostly independent tasks
- Need to remain in current session
- Quality gates required between tasks
- Context preservation across multiple steps

**Don't use when:**
- Tasks are tightly coupled
- Parallel execution preferred
- Simple, single-file changes

## Process Flow

```
Plan → [Task 1] → Implement → Spec Review → Quality Review → ✓
                                  ↓              ↓
                               Fix & Re-review if needed
       [Task 2] → Implement → Spec Review → Quality Review → ✓
       ...
       Final Review → Complete
```

## Detailed Process

### Step 1: Plan Preparation

Extract all tasks with full context:

```markdown
## Task Extraction

From plan, create TodoWrite entries:
- [ ] Task 1: [Description with full context]
- [ ] Task 2: [Description with full context]
- [ ] Task 3: [Description with full context]
```

**Important:** Provide extracted text to subagents, don't make them read plan files.

### Step 2: Per-Task Execution

For each task:

#### 2a. Dispatch Implementer

```markdown
**Implementer Subagent Prompt:**

Implement the following task:

[Complete task text from plan]

Requirements:
- Follow TDD: write test first, verify failure, implement, verify pass
- Make atomic commits
- Self-review before signaling completion
- Ask clarifying questions if needed

Signal completion with summary of:
- Files changed
- Tests added/modified
- Any deviations from plan
```

#### 2b. Handle Clarifications

If implementer asks questions:
- Answer before implementation begins
- Don't let implementer proceed with assumptions
- Document answers for future reference

#### 2c. Spec Compliance Review

```markdown
**Spec Reviewer Subagent Prompt:**

Review the implementation for specification compliance:

**Original task spec:**
[Task text from plan]

**Changes made:**
[Summary from implementer]

Verify:
- [ ] All requirements from spec implemented
- [ ] No requirements missed
- [ ] No extra features added (YAGNI)
- [ ] Implementation matches described approach

Report: PASS or FAIL with specific issues
```

If FAIL: Fix issues, re-run spec review.

#### 2d. Code Quality Review

Only after spec review passes:

```markdown
**Quality Reviewer Subagent Prompt:**

Review the implementation for code quality:

**Files changed:**
[List of files]

Review for:
- [ ] Code clarity and readability
- [ ] Error handling
- [ ] Test coverage and quality
- [ ] Performance considerations
- [ ] Security implications
- [ ] Adherence to project conventions

Report: PASS or FAIL with specific issues
```

If FAIL: Fix issues, re-run quality review.

#### 2e. Mark Complete

After both reviews pass:
- Mark task as complete in TodoWrite
- Move to next task

### Step 3: Final Review

After all tasks complete:

```markdown
**Final Reviewer Subagent Prompt:**

Conduct comprehensive code review of all changes:

**Tasks completed:**
[List of all tasks]

**Files modified:**
[Complete file list]

Review for:
- [ ] Overall architectural coherence
- [ ] Cross-task consistency
- [ ] Integration correctness
- [ ] Complete test coverage
- [ ] Documentation completeness

Report: PASS or specific issues to address
```

### Step 4: Completion

Use finishing-a-development-branch skill:
- Decide: merge to main or create PR
- Handle cleanup
- Update tracking

## Critical Rules

### Never

- Skip reviews (spec compliance OR code quality)
- Start code quality review before spec compliance passes
- Dispatch multiple implementation subagents in parallel
- Make subagents read plan files directly
- Accept reviews with unresolved issues
- Continue to next task before current passes both reviews

### Always

- Provide extracted text to subagents
- Answer clarifications before implementation
- Fix issues before re-review
- Document deviations from plan
- Run both review stages in order

## Review Order Rationale

```
1. Spec Compliance (Does it do the right thing?)
   ↓
2. Code Quality (Does it do it well?)
```

Spec first because:
- No point polishing wrong code
- Requirements drive design decisions
- Quality review assumes correct functionality

## Best Practices

### Do

1. Extract complete task context
2. Include expected outcomes in implementer prompt
3. Be specific in review criteria
4. Fix issues immediately when found
5. Keep TodoWrite updated
6. Document any plan deviations

### Don't

1. Rush through reviews
2. Batch multiple tasks before review
3. Skip re-review after fixes
4. Let implementer guess at requirements
5. Accept "mostly passing" reviews
6. Proceed with unresolved questions

## Error Handling

| Situation | Action |
|-----------|--------|
| Implementer asks question | Answer fully, then proceed |
| Spec review fails | Fix specific issues, re-review |
| Quality review fails | Fix specific issues, re-review |
| Task blocked by dependency | Complete dependency first |
| Plan needs revision | Update plan, re-extract tasks |

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| First-pass spec compliance | >80% | Tasks passing spec review first time |
| First-pass quality | >70% | Tasks passing quality review first time |
| Re-review cycles | <2 | Average re-reviews per task |
| Task completion rate | 100% | Tasks completed as planned |

## Related Skills

- [writing-plans](../planning/writing-plans/SKILL.md) - Create implementation plans
- [tdd-obra](../tdd-obra/SKILL.md) - Test-first development
- [code-reviewer](../code-reviewer/SKILL.md) - Code quality review
- [parallel-dispatch](../../agents/parallel-dispatch/SKILL.md) - Parallel execution

---

## Version History

- **1.0.0** (2026-01-19): Initial release adapted from obra/superpowers
