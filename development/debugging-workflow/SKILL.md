---
name: debugging-workflow
description: >
  디버깅 실패 시 자동 트리거되는 체계적 문제 해결 워크플로우.
  DEBUGGING_STRATEGY.md 기반 Phase 0-3 디버깅 프로세스 자동화.
version: 2.0.0

# 2025 Schema: 자동 트리거 조건
triggers:
  keywords:
    - "로그 분석"
    - "debug"
    - "실패"
    - "오류"
    - "버그"
    - "3회 실패"
    - "error"
    - "exception"
  file_patterns:
    - "logs/**/*.log"
    - "**/*.error"
    - "**/debug.log"
  context:
    - "테스트 실패 분석"
    - "에러 로그 확인"
    - "버그 원인 파악"

# 2025 Schema: 스킬 기능 선언
capabilities:
  - analyze_logs
  - add_debug_logs
  - classify_problem_area
  - verify_hypothesis
  - manage_debug_state      # Phase D0-D4 상태 관리
  - enforce_phase_gate      # 수정 전 가설 검증 강제

# 2025 Schema: 모델 선호도
model_preference: sonnet

# 기존 필드 유지
phase: [1, 2, 5]
auto_trigger: true
dependencies:
  - debugger
token_budget: 2500
---

# Debugging Workflow

문제 해결 실패 시 체계적인 디버깅 워크플로우입니다.

## Quick Start

```bash
# 로그 분석 실행
python .claude/skills/debugging-workflow/scripts/analyze_logs.py <log_file>

# 디버그 로그 자동 삽입
python .claude/skills/debugging-workflow/scripts/add_debug_logs.py <source_file>
```

## 핵심 원칙

1. **로그 없이 수정 금지**: 추측 기반 수정은 새 버그 유발
2. **문제 파악 > 해결**: 문제를 정확히 알면 해결은 쉬움
3. **예측 검증 필수**: "내 예측이 로그로 확인되었는가?"

## Phase 0: 디버그 로그 추가

### 로그 패턴

```python
logger.debug(f"[ENTRY] input: {input}")
logger.debug(f"[STATE] current: {state}")
logger.debug(f"[RESULT] output: {result}")
```

### 분석 체크리스트

- [ ] 예상 입력 = 실제 입력?
- [ ] 중간 상태가 예상과 일치?
- [ ] 출력 불일치 지점 확인?
- [ ] **내 예측이 로그로 검증됨?**

> 예측 불일치 시 → Phase 0 재시작

## Phase 1: 문제 영역 분류

```
Q: 이 코드는 언제 작성되었는가?

A) 이번 작업에서 새로 작성 → Phase 2 (신규 기능)
B) 기존에 있던 로직       → Phase 3 (기존 로직)
```

```bash
# Git blame으로 확인
git blame <file_path> | grep "<line_number>"
```

## Phase 2: 신규 기능 문제

**PRD 검토**:
- [ ] 요구사항 모호한 부분?
- [ ] Edge case 정의됨?
- [ ] 에러 처리 명시됨?

**리팩토링 판단** (2개 이상 해당 시):
- [ ] 동일 버그 3회+ 반복
- [ ] 수정 시 Side effect 발생
- [ ] 테스트 커버리지 < 50%
- [ ] "이해하기 어렵다"

## Phase 3: 기존 로직 문제

### 예측 검증 템플릿

```markdown
**가설**: [원인 추정]
**검증 방법**: [확인 방법]
**예상 결과**: [가설 맞으면 기대값]
**실제 결과**: [실험 결과]
**결론**: ✅ 일치 → 해결 / ❌ 불일치 → 새 가설
```

### 해결 전 체크리스트

- [ ] 문제를 한 문장으로 설명 가능?
- [ ] 문제를 재현 가능?
- [ ] 발생 조건 파악?
- [ ] 비발생 조건 파악?
- [ ] 예측이 검증됨?

> **모든 항목 체크 후** 해결 진행

## 실패 시 워크플로우

```
실패 → Phase 0 (로그) → Phase 1 (분류)
         ↓
    ┌────┴────┐
    ↓         ↓
 Phase 2   Phase 3
 (신규)    (기존)
    ↓         ↓
 PRD 검토  예측 검증
    ↓         ↓
 리팩토링? 가설 실험
    ↓
 3회 실패 → /issue-failed
```

## Anti-Patterns

| 금지 | 이유 |
|------|------|
| ❌ 로그 없이 수정 | 추측 = 새 버그 |
| ❌ 문제 파악 전 해결 | 시간 낭비 |
| ❌ 여러 곳 동시 수정 | 원인 파악 불가 |
| ❌ "아마 이거겠지" | 반드시 검증 |

---

## Known Issues 문서화 (Phase 4)

**해결된 이슈를 체계적으로 문서화하여 재발 방지 및 지식 공유.**

### 문서화 시점

- 디버깅 완료 후
- 동일 이슈 2회+ 발생 시
- 복잡한 원인 분석이 필요했던 경우

### 문서화 템플릿

```markdown
### Issue #{N}: {제목}

**증상**: {사용자/시스템이 관찰한 문제}

**원인**: {분석 결과 밝혀진 근본 원인}

**해결**: {적용한 수정사항}

**파일**: `{수정된 파일 경로}:{라인 번호}`

**재발 방지**: {방지 조치 또는 테스트 추가 여부}
```

### 예시

```markdown
### Issue #3: 폴더-카테고리 매칭 실패

**증상**: GGMillions, HCL 등 일부 폴더가 진행률 트리에서 매칭되지 않음

**원인**:
1. DB 카테고리 누락 (Google Sheets 동기화 문제)
2. 복합 단어 매칭 한계 (`folder_lower in category_words` 규칙)

**해결**:
- `folder_prefix` 전략 추가 (점수 0.85)
- `reverse_word` 전략 추가 (점수 0.75)

**파일**: `backend/app/services/progress_service.py:230`

**재발 방지**: 매칭 전략 단위 테스트 추가
```

### 문서 위치

| 프로젝트 유형 | 권장 위치 |
|---------------|-----------|
| 단일 프로젝트 | `docs/KNOWN_ISSUES.md` |
| 모노레포 | `{component}/docs/KNOWN_ISSUES.md` |
| 도메인 에이전트 | `.claude/agents/{domain}-domain.md` 내 섹션 |

### 워크플로우 통합

```
문제 해결 완료
    ↓
Known Issue 해당 여부 판단
    │
    ├─ 단순/일회성 → 스킵
    │
    └─ 복잡/재발 가능 → 문서화
        ↓
    KNOWN_ISSUES.md 또는
    Domain Agent에 기록
```

---

## 관련 도구

| 도구 | 용도 |
|------|------|
| `scripts/analyze_logs.py` | 로그 파일 분석 |
| `scripts/add_debug_logs.py` | 디버그 로그 삽입 |
| `references/log-patterns.md` | 로그 패턴 사전 |
| `/issue-failed` | 3회 실패 시 호출 |

---

> 상세 전략: `docs/DEBUGGING_STRATEGY.md`

---

## Phase D0-D4: 가설-검증 강제 디버깅

**수정 전 가설 검증을 강제하여 무의미한 수정-실행 반복 방지**

### Phase Gate 모델

```
문제 발생
    ↓
[D0: 이슈 등록] ─── 이슈 설명 필수
    ↓
[D1: 원인 분석] ─── 가설 작성 필수 (최소 20자)
    ↓
[D2: 검증 설계] ─── 검증 방법 기록 필수
    ↓
[D3: 가설 검증] ─── 결과 기록 필수
    │
    ├─ 기각 → D1로 복귀 (3회 시 /issue failed)
    │
    └─ 확인 → [D4: 수정 허용]
```

### 상태 기반 Phase 전환

| Phase | 진입 조건 | Gate 조건 |
|-------|----------|----------|
| D0 | /debug start | 이슈 설명 작성 |
| D1 | D0 완료 | 가설 작성 (min 20자) |
| D2 | 가설 존재 | 검증 계획 작성 |
| D3 | 검증 계획 존재 | 결과 기록 (confirmed/rejected) |
| D4 | hypothesis_confirmed=true | - |

### 가설 반복 제한

- 동일 이슈에서 **3회 가설 실패** 시 `/issue failed` 강제 호출
- 각 가설은 `.debug/hypotheses/NNN-*.md`에 기록됨
- 검증 증거는 `.debug/evidence/NNN-*.txt`에 기록됨

### 반자동 실행 모드

`/debug` 커맨드 호출 시:
1. D0 → 이슈 설명 요청
2. D1 → 가설 요청 (자동 진행)
3. D2 → 검증 계획 요청 (자동 진행)
4. D3 → 검증 결과 요청 (자동 진행)
5. D4 → 수정 허용 (가설 확인 시)

Gate 미충족 시만 멈추고 사용자 입력 요청

### 상태 관리 스크립트

```python
from debug_state import DebugState

state = DebugState(project_root)
state.start("이슈 설명")
state.set_hypothesis("가설 (min 20자)")
state.set_verification_plan("검증 방법")
state.set_verification_result("confirmed", "증거")
state.advance_to_fix()
```

### 통합 워크플로우

```
/work E2E 실패 → /debug 자동 트리거
/issue fix → confidence < 80% → /debug 자동 트리거
```

### 관련 커맨드

- `/debug` - 가설-검증 디버깅 시작
- `/debug status` - 현재 상태 확인
- `/debug abort` - 세션 취소
