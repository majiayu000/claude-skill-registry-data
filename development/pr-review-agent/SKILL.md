---
name: pr-review-agent
description: >
  PR 코드 리뷰, 개선 제안, 자동 머지 에이전트.
  코드 품질, 테스트, 보안 검사 통합.
version: 2.0.0

triggers:
  keywords:
    - "PR review"
    - "PR 리뷰"
    - "코드 리뷰"
    - "auto merge"
  file_patterns: []
  context:
    - "Pull Request 검토"
    - "코드 리뷰 요청"

capabilities:
  - parallel_code_check
  - review_checklist
  - auto_merge

model_preference: sonnet

auto_trigger: false
---

# PR Review Agent

PR 리뷰 후 개선 제안, 문제없으면 자동 머지하는 전문 에이전트입니다.

## Quick Start

```bash
# 커맨드로 호출
/pr review #42       # PR 리뷰
/pr auto #42         # 리뷰 + 자동 머지

# 직접 호출
Task(
    subagent_type="general-purpose",
    prompt="PR #42 리뷰 및 머지 검토",
    description="PR 리뷰"
)
```

## 핵심 기능

### 1. 병렬 코드 검사

```python
# 3개 에이전트 병렬 실행
Task(subagent_type="Explore", prompt="코드 품질 검사: lint, type, complexity")
Task(subagent_type="Explore", prompt="테스트 검증: coverage, new tests")
Task(subagent_type="Explore", prompt="보안 검사: secrets, vulnerabilities")
```

### 2. 리뷰 체크리스트

| 카테고리 | 검사 항목 | 심각도 | 블로커 |
|----------|----------|--------|--------|
| **코드 품질** | Lint 오류 | High | ✅ |
| | Type 오류 | High | ✅ |
| | 복잡도 >10 | Medium | ❌ |
| **테스트** | 테스트 실패 | High | ✅ |
| | 커버리지 <80% | Medium | ❌ |
| **보안** | 시크릿 노출 | Critical | ✅ |
| | 취약 의존성 | High | ✅ |
| **스타일** | 포맷팅 | Low | ❌ |

### 3. 머지 조건 검증

```bash
# 필수 조건
gh pr checks #42 --watch          # CI 상태
gh pr view #42 --json mergeable   # 충돌 여부

# 권장 조건
gh pr view #42 --json baseRefName # 브랜치 최신 여부
```

## 리뷰 워크플로우

```
PR 리뷰 시작
    │
    ├─ Step 1: PR 정보 수집 ─────────────────────┐
    │      │                                      │
    │      ├─ gh pr view #N --json ...            │
    │      ├─ gh pr diff #N                       │
    │      └─ 변경 파일 목록                      │
    │                                        ─────┘
    │
    ├─ Step 2: 병렬 검사 ───────────────────────┐
    │      │                                     │
    │      ├─ [Agent 1] 코드 품질               │
    │      │     ├─ ruff check                  │
    │      │     ├─ mypy (Python)               │ 병렬
    │      │     └─ eslint (JS/TS)              │
    │      │                                     │
    │      ├─ [Agent 2] 테스트                  │
    │      │     ├─ pytest --cov                │
    │      │     └─ 신규 코드 테스트 존재 확인  │
    │      │                                     │
    │      └─ [Agent 3] 보안                    │
    │            ├─ grep -r "password\|secret"  │
    │            └─ pip-audit / npm audit       │
    │                                      ─────┘
    │
    ├─ Step 3: 결과 분석
    │      │
    │      ├─ Critical/High → 블로커 (머지 차단)
    │      │     └─ 구체적 수정 방법 제시
    │      │
    │      ├─ Medium → 개선 제안
    │      │     └─ 코드 예시와 함께 제안
    │      │
    │      └─ Low → 참고 사항
    │
    ├─ Step 4: 리뷰 코멘트 작성
    │      │
    │      └─ gh pr comment #N --body "리뷰 결과..."
    │
    └─ Step 5: 머지 결정
           │
           ├─ 블로커 있음 → 종료 (수정 대기)
           │
           └─ 블로커 없음 → 머지 진행
                  │
                  └─ gh pr merge #N --squash --delete-branch
```

## 검사 명령어

### Python 프로젝트

```bash
# 코드 품질
ruff check src/ --output-format=json
mypy src/ --json-output

# 테스트
pytest tests/ -v --cov=src --cov-report=json

# 보안
pip-audit --format=json
bandit -r src/ -f json
```

### JavaScript/TypeScript 프로젝트

```bash
# 코드 품질
npx eslint src/ --format=json
npx tsc --noEmit

# 테스트
npm test -- --coverage --json

# 보안
npm audit --json
```

## 개선 제안 형식

### 코드 블로커

```markdown
### ❌ 블로커: 시크릿 노출

**파일**: `src/config.py:12`

**현재 코드**:
```python
API_KEY = "sk-1234567890abcdef"
```

**문제**: API 키가 소스 코드에 하드코딩되어 있습니다.

**해결 방법**:
```python
import os
API_KEY = os.getenv("API_KEY")
```

**추가 작업**:
1. `.env` 파일에 `API_KEY=sk-...` 추가
2. `.gitignore`에 `.env` 확인
```

### 개선 제안

```markdown
### ⚠️ 개선 제안: 함수 복잡도

**파일**: `src/auth.py:45-78`
**복잡도**: 12 (권장: 10)

**현재 코드**:
```python
def authenticate(user, password, token, ...):
    # 33줄의 복잡한 로직
```

**제안**:
```python
def authenticate(user, password, token, ...):
    if not _validate_input(user, password):
        raise ValueError("Invalid input")

    token = _generate_token(user)
    return _create_session(user, token)

def _validate_input(user, password):
    # 입력 검증 로직 분리
    ...

def _generate_token(user):
    # 토큰 생성 로직 분리
    ...
```
```

## 머지 설정

```yaml
# .claude/config/pr-merge.yaml 참조

merge:
  method: squash          # squash (기본), merge, rebase
  delete_branch: true     # 머지 후 브랜치 삭제

review:
  strict_mode: false      # true: Medium도 블로커
  auto_fix:
    - lint               # 자동 수정 대상
    - format

thresholds:
  complexity: 10          # 함수 복잡도 한계
  coverage: 80            # 최소 테스트 커버리지 (%)

labels:
  auto_merge:             # 자동 머지 허용
    - "auto-merge"
    - "trivial"
  block_merge:            # 머지 차단
    - "wip"
    - "do-not-merge"
```

## 자동 수정 기능

### Lint/Format 자동 수정

```bash
# Python
ruff check src/ --fix
black src/

# JavaScript/TypeScript
npx eslint src/ --fix
npx prettier --write src/
```

### 자동 수정 후 커밋

```bash
git add -A
git commit -m "style: auto-fix lint and format issues

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
git push
```

## Anti-Patterns

| 금지 | 이유 | 대안 |
|------|------|------|
| 블로커 무시 머지 | 품질 저하 | 수정 후 재리뷰 |
| 테스트 없이 머지 | 회귀 위험 | 최소 테스트 추가 |
| 리뷰 없이 머지 | 버그 유입 | `/pr review` 필수 |
| force push 후 머지 | 이력 손실 | 일반 push |

## 연동

| 커맨드/스킬 | 연동 시점 |
|-------------|----------|
| `/create pr` | PR 생성 후 → `/pr review` |
| `/check` | 리뷰 전 로컬 검사 |
| `tdd-workflow` | 테스트 커버리지 확인 |
| `debugging-workflow` | 테스트 실패 시 |

## 트러블슈팅

### CI 실패

```bash
# 1. CI 로그 확인
gh run list --limit 5
gh run view <run-id> --log-failed

# 2. 로컬에서 재현
pytest tests/ -v
npm test
```

### 충돌 발생

```bash
# 1. 베이스 브랜치 최신화
git fetch origin main
git rebase origin/main

# 2. 충돌 해결 후 force push
git push --force-with-lease
```

### 머지 권한 없음

```bash
# 권한 확인
gh api repos/{owner}/{repo}/collaborators/{username}/permission

# 관리자에게 요청 또는
gh pr merge #42 --admin  # admin 권한 필요
```
