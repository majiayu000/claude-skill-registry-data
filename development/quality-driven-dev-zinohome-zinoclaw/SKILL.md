---
slug: quality-driven-dev
version: 1.1.1
displayName: 质量驱动开发（Quality Driven Dev）
summary: 通过自动选择TDD/DDD方法和TRUST 5质量框架，实现高质量开发，适用于构建功能、重构代码、修复错误等任务。
tags: clawhub
---

# Quality-Driven Development

Structured development methodology inspired by MoAI-ADK's TRUST 5 framework. Automatically selects TDD or DDD based on project state, enforces quality gates, and produces tested, documented code.

## Core Philosophy

> "바이브 코딩의 목적은 빠른 생산성이 아니라 코드 품질이다."

## Logging Strategy

All code must include meaningful logs. Logs are the first line of defense for debugging production issues.

### Log Levels

| Level | Purpose | Examples | 운영(PRD) | 개발(DEV) |
|-------|---------|----------|:---------:|:---------:|
| **ERROR** | 예외, 실패, 복구 불가 상황 | catch 블록, DB 연결 실패, 필수값 누락 | ✅ | ✅ |
| **WARN** | 예상 밖 상황, 복구 가능 | fallback 사용, 재시도, deprecated 호출 | ✅ | ✅ |
| **INFO** | 핵심 흐름만 간결하게 | API 호출/응답, 상태 변경, 트랜잭션 시작/완료 | ✅ | ✅ |
| **DEBUG** | 상세 디버깅, 자유롭게 | 함수 진입/종료, 변수값, 조건 분기, 쿼리 파라미터 | ❌ | ✅ |

### Log Placement Rules

**반드시 로그를 넣어야 하는 곳:**
- API 엔드포인트 진입 (INFO: 요청 파라미터 요약)
- 외부 서비스 호출 전/후 (INFO: 호출 대상, 응답 상태)
- 에러/예외 catch 블록 (ERROR: 에러 메시지 + 컨텍스트)
- 비즈니스 로직 분기점 (DEBUG: 어떤 분기로 갔는지)
- 상태 변경 (INFO: before → after)
- 배치/스케줄러 시작/완료 (INFO: 처리 건수, 소요 시간)

**로그 작성 원칙:**
- 운영에서 INFO만으로 흐름 추적이 가능해야 한다
- DEBUG는 부담 없이 자유롭게 — 운영에선 출력 안 됨
- 민감 정보(비밀번호, 토큰, 개인정보) 절대 로그에 포함 금지
- 로그 메시지에 컨텍스트 포함 (ID, 파라미터 등) — `"처리 실패"` ❌ → `"주문 처리 실패 [orderId=123, reason=재고부족]"` ✅

## Workflow

### Phase 0: Project Analysis

Before any coding, analyze the project:

1. Check if test framework exists (`jest`, `vitest`, `pytest`, `go test`, etc.)
2. Measure current test coverage (run coverage command if available)
3. Detect language, framework, and project structure
4. **Identify logging framework** (`slf4j`, `winston`, `pino`, `logback`, `print/console.log` etc.) — if none exists, recommend and set up one
5. Select methodology automatically:

```
Coverage >= 10% OR new project → TDD (default)
Coverage < 10% AND existing project → DDD
```

Report the analysis result and selected methodology to the user before proceeding.

### Phase 1: SPEC Document

Create a SPEC document before implementation:

```markdown
# SPEC-{ID}: {Title}

## Goal
One sentence describing what this change achieves.

## Acceptance Criteria
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

## Scope
- **In scope:** What will be changed
- **Out of scope:** What will NOT be changed

## Technical Approach
Brief description of implementation strategy.

## Log Points
Key locations where logs will be added (level + message summary).

## TRUST 5 Checklist
- [ ] **Tested:** All acceptance criteria have corresponding tests
- [ ] **Readable:** Code is self-documenting with clear naming
- [ ] **Unified:** Follows existing project conventions
- [ ] **Secured:** No new vulnerabilities introduced
- [ ] **Trackable:** Changes are documented and linked to this SPEC
```

### Phase 2A: TDD Execution (New Projects / Coverage >= 10%)

Follow RED → GREEN → REFACTOR strictly:

**RED — Write failing tests first**
1. Write test for first acceptance criterion
2. Run test — confirm it FAILS
3. Report: "🔴 RED: Test written and failing as expected"

**GREEN — Minimal implementation**
1. Write minimum code to pass the test
2. **Add appropriate logs** at key points (API calls, error handling, state changes)
3. Run test — confirm it PASSES
4. Report: "🟢 GREEN: Test passing"

**REFACTOR — Clean up**
1. Improve code quality while keeping tests green
2. **Review log quality** — ensure levels are correct, messages are clear with context
3. Run all tests — confirm everything still passes
4. Report: "♻️ REFACTOR: Code cleaned, all tests green"

Repeat for each acceptance criterion.

### Phase 2B: DDD Execution (Existing Projects / Coverage < 10%)

Follow ANALYZE → PRESERVE → IMPROVE:

**ANALYZE — Understand existing code**
1. Read existing code and identify dependencies
2. Map domain boundaries and side effects
3. **Check existing logging** — identify gaps where logs are missing
4. Report: "🔍 ANALYZE: Current behavior documented"

**PRESERVE — Capture current behavior**
1. Write characterization tests for existing behavior
2. Run tests — confirm they pass against current code
3. Report: "🛡️ PRESERVE: Characterization tests in place"

**IMPROVE — Change under test protection**
1. Make changes incrementally
2. **Add/improve logs** at changed code paths
3. Run tests after each change
4. Report: "📈 IMPROVE: Changes verified by tests"

### Phase 3: TRUST 5 Quality Gate

Before declaring work complete, verify all 5 principles:

| Principle | Check | Action |
|-----------|-------|--------|
| **Tested** | Run full test suite | All tests pass, coverage maintained or improved |
| **Readable** | Review naming, comments, **log messages** | Fix unclear names, ensure log messages have context |
| **Unified** | Check style consistency, **log format consistency** | Match existing patterns (indent, naming, log format) |
| **Secured** | Security review, **log content review** | No hardcoded secrets, no sensitive data in logs |
| **Trackable** | Documentation, **log coverage** | Changes described, key paths have appropriate logs |

Only proceed to completion when ALL 5 checks pass.

### Phase 4: Completion Report

```markdown
## ✅ SPEC-{ID} Complete

### Methodology: {TDD|DDD}
### Changes:
- {file1}: {what changed}
- {file2}: {what changed}

### Log Points Added:
- {file1:line}: {level} - {description}
- {file2:line}: {level} - {description}

### Test Results:
- Tests: {passed}/{total}
- Coverage: {before}% → {after}%

### TRUST 5:
- ✅ Tested | ✅ Readable | ✅ Unified | ✅ Secured | ✅ Trackable
```

## Agent Roles

When working on complex tasks, delegate to specialized perspectives:

| Role | Focus | When to Activate |
|------|-------|-----------------|
| **Architect** | System design, API contracts | New feature, structural change |
| **Backend** | API, DB, business logic | Server-side work |
| **Frontend** | UI, UX, components | Client-side work |
| **Security** | Vulnerabilities, auth, input validation | Auth features, data handling |
| **Tester** | Test strategy, edge cases, coverage | Always (TRUST 5 - Tested) |
| **Performance** | Optimization, profiling | Load-sensitive features |

For each task, identify which roles are relevant and apply their perspective during review.

## Reference Guides

| Topic | Reference | Load When |
|-------|-----------|-----------|
| TDD Patterns | `references/tdd-patterns.md` | TDD methodology selected |
| DDD Patterns | `references/ddd-patterns.md` | DDD methodology selected |
| TRUST 5 Detail | `references/trust5-checklist.md` | Quality gate phase |
| Language-specific | `references/lang-{language}.md` | Language-specific patterns needed |

## Constraints

**MUST DO:**
- Always analyze project before choosing methodology
- Always create SPEC before coding
- Always write tests (TDD: before code, DDD: before changes)
- Always run TRUST 5 gate before completion
- Report progress at each phase transition
- Always add meaningful logs with appropriate levels at key code points
- Always ensure tests are actually executed (not just written) — run the test suite and confirm results before proceeding

**MUST NOT:**
- Skip test writing for any reason
- Write implementation before tests (TDD mode)
- Modify untested code without characterization tests first (DDD mode)
- Declare complete without all 5 TRUST checks passing
- Change code outside the SPEC scope
- Log sensitive data (passwords, tokens, personal info)
- Skip logging at error/catch blocks
