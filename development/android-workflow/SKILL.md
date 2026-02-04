---
name: android-workflow
description: |
  Orchestrates Android development workflows for Kotlin/Compose projects.
  Routes tasks to appropriate workflow: feature, quick-fix, refactor, investigate, hotfix.
  Use when user requests: implementation (구현, 추가, 새 기능, 만들어, 개발, 적용),
  bug fixes (버그, 수정, 오류, 고쳐), refactoring (리팩토링, 개선, 정리),
  debugging (분석, 원인, 왜, 디버깅, 안돼), or hotfix (긴급, 프로덕션, 핫픽스).
  Provides Self-Check Protocol and Quality Gates for implementation tasks.
---

# Android Workflow Orchestrator

Routes Android development tasks to appropriate workflows and manages quality gates.

## Self-Check Protocol (MUST DO)

Before starting implementation tasks, verify:

| # | Question | Action if No |
|---|----------|--------------|
| 1 | Is this an implementation task? | Handle directly |
| 2 | Has the workflow been classified? | Call task-router first |
| 3 | Following the correct sequence? | Re-check workflow |
| 4 | Trying to skip an agent? | Never allowed, follow sequence |

## Quick Classification

### Classification Criteria

| Condition | Workflow |
|-----------|----------|
| Files ≤2, single layer, no UI/API/DB | **quick-fix** |
| New feature, new screen | **feature** |
| Structure change, behavior preserved | **refactor** |
| Unknown bug cause, error analysis | **investigate** |
| Production emergency | **hotfix** |

### Auto-Upgrade Rules

| Trigger | From | To |
|---------|------|-----|
| UI changes detected | quick-fix | feature |
| Files 3+ | quick-fix | feature |
| API/DB changes | quick-fix | feature |
| Build fails 2x | any | investigate |

## Workflow Sequences

Agent execution order for each workflow:

| Workflow | Sequence |
|----------|----------|
| **quick-fix** | code-writer → code-critic |
| **feature** | planner → [ux-engineer] → [ui-builder] → code-writer → test-engineer → code-critic |
| **refactor** | planner → code-writer → test-engineer → code-critic |
| **investigate** | investigator → (route based on findings) |
| **hotfix** | code-writer → test-engineer(smoke) → code-critic |

**Detailed Guides:**
- quick-fix: [workflows/quick-fix.md](workflows/quick-fix.md)
- feature: [workflows/feature.md](workflows/feature.md)
- refactor: [workflows/refactor.md](workflows/refactor.md)
- investigate: [workflows/investigate.md](workflows/investigate.md)
- hotfix: [workflows/hotfix.md](workflows/hotfix.md)

## Quality Gates

| Gate | Checkpoint | Criteria |
|------|------------|----------|
| Gate 0 | task-router | Classification complete |
| Gate 1 | planner | Requirements clear, tasks defined |
| Gate 2 | code-writer | Build succeeds |
| Gate 3 | code-critic | 0 critical, ≤2 major issues |

**Detailed Criteria:** [gates/quality-gates.md](gates/quality-gates.md)

## MCP Tool Requirements

| Workflow | sequential-thinking | context7 | codex-cli |
|----------|---------------------|----------|-----------|
| quick-fix | Skip | Optional | 1 round |
| feature | 3+ steps | Required | 2+ rounds |
| refactor | 3+ steps | Optional | 2+ rounds |
| investigate | 5+ steps | Optional | Optional |
| hotfix | Skip | Optional | 1 round |

## Build Commands

```bash
# Full build
./gradlew build

# Module build
./gradlew :feature:home:build

# Run tests
./gradlew test
./gradlew :feature:home:testDebugUnitTest

# Clean build
./gradlew clean build
```

## Failure Recovery

On build or gate failure:

1. **Record**: Log error messages and environment info
2. **Retry**: Auto-retry once
3. **Escalate**: If still failing, present options
   - A: Manual fix then retry
   - B: Call investigator
   - C: Abort task