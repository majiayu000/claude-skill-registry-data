---
name: issue-resolution
description: >
  GitHub 이슈 해결 워크플로우. 분석 → 구현 → 검증 자동화.
version: 2.0.0

triggers:
  keywords:
    - "이슈 해결"
    - "fix issue"
    - "이슈 분석"
    - "GitHub issue"
    - "버그 수정"
  file_patterns: []
  context:
    - "GitHub 이슈 처리"
    - "버그 리포트 분석"

capabilities:
  - analyze_issue
  - resolve_issue
  - handle_failed

model_preference: sonnet

phase: [1, 2]
auto_trigger: true
dependencies:
  - debugging-workflow
  - tdd-workflow
token_budget: 1500
---

# Issue Resolution

GitHub 이슈 분석 및 해결 워크플로우입니다.

## Quick Start

```bash
# 이슈 분석
python .claude/skills/issue-resolution/scripts/analyze_issue.py 123

# 이슈 해결 워크플로우
python scripts/resolve_issue.py 123 --auto-fix

# 실패 이슈 처리
python scripts/handle_failed.py 123 --create-sub-issue
```

## 워크플로우

```
GitHub Issue
    ↓
┌─────────────────────────────────────────────┐
│ 1. 분석 (Analyze)                           │
│    - 이슈 타입 분류 (bug/feature/docs)      │
│    - 관련 파일 탐색                          │
│    - 영향 범위 파악                          │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ 2. 계획 (Plan)                              │
│    - 수정 전략 결정                          │
│    - 테스트 계획                             │
│    - 브랜치 생성: fix/issue-123-desc        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ 3. 구현 (Implement)                         │
│    - TDD 사이클 (Red → Green → Refactor)    │
│    - 코드 수정                               │
│    - 테스트 추가/수정                        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ 4. 검증 (Verify)                            │
│    - 테스트 통과 확인                        │
│    - 린트/포맷 검사                          │
│    - PR 생성                                 │
└─────────────────────────────────────────────┘
```

## 이슈 타입별 처리

| 타입 | 라벨 | 워크플로우 |
|------|------|-----------|
| Bug | `bug` | 분석 → 재현 → 수정 → 테스트 |
| Feature | `enhancement` | PRD → Task → 구현 → 테스트 |
| Docs | `documentation` | 직접 수정 → 커밋 |
| Refactor | `refactor` | 분석 → 계획 → 리팩토링 |

## 분석 단계

### 이슈 정보 수집

```bash
# 이슈 상세 조회
gh issue view 123 --json title,body,labels,assignees

# 관련 PR 확인
gh pr list --search "123"
```

### 관련 파일 탐색

```python
# 이슈 본문에서 파일 패턴 추출
# - 스택 트레이스에서 파일 경로
# - 코드 블록에서 모듈 이름
# - 에러 메시지에서 함수명
```

## 실패 처리

### 3회 실패 시

```bash
# 1. 실패 이슈 생성
python scripts/handle_failed.py 123 --create-sub-issue

# 2. 분석 레포트 생성
python scripts/handle_failed.py 123 --report

# 3. 수동 개입 요청
# → /issue-failed 커맨드 실행
```

### 실패 분석 레포트

```markdown
## 실패 분석: Issue #123

### 시도 내역
1. 시도 1: [접근 방법] - [실패 이유]
2. 시도 2: [접근 방법] - [실패 이유]
3. 시도 3: [접근 방법] - [실패 이유]

### 권장 조치
- [ ] 추가 정보 필요: [상세]
- [ ] 설계 변경 필요: [상세]
- [ ] 외부 의존성 문제: [상세]
```

## 자동화 옵션

```bash
# 분석만
python scripts/resolve_issue.py 123 --analyze-only

# 자동 수정 (3회 시도)
python scripts/resolve_issue.py 123 --auto-fix

# PR까지 생성
python scripts/resolve_issue.py 123 --auto-fix --create-pr

# 강제 모드 (확인 없이 진행)
python scripts/resolve_issue.py 123 --auto-fix --force
```

## 관련 커맨드

| 커맨드 | 용도 |
|--------|------|
| `/fix-issue` | 이슈 분석 및 수정 |
| `/issue-failed` | 실패 분석 및 새 솔루션 |
| `/create-pr` | PR 생성 |

## 연동 Skills

| Skill | 연동 시점 |
|-------|----------|
| `debugging-workflow` | 버그 분석 시 |
| `tdd-workflow` | 구현 단계 |
| `code-quality-checker` | 검증 단계 |

---

> 참조: CLAUDE.md 섹션 6 Commands
