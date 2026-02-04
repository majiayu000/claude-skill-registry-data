---
name: phase-validation
description: >
  Phase 0-6 검증 자동화. 각 Phase별 필수 조건 확인.
version: 2.0.0

triggers:
  keywords:
    - "Phase 검증"
    - "validate phase"
    - "Phase 0"
    - "Phase 1"
    - "Phase 2"
  file_patterns: []
  context:
    - "Phase 진행 상태 확인"
    - "다음 Phase 조건 검증"

capabilities:
  - validate_phase
  - auto_advance
  - phase_status

model_preference: haiku

phase: [0, 0.5, 1, 2, 2.5, 3, 4, 5, 6]
auto_trigger: true
token_budget: 1000
---

# Phase Validation

Phase 0-6 검증 자동화 워크플로우입니다.

## Quick Start

```bash
# 전체 Phase 상태 확인
python .claude/skills/phase-validation/scripts/validate_phase.py --status

# 특정 Phase 검증
python scripts/validate_phase.py --phase 2

# 다음 Phase 자동 진행
python scripts/validate_phase.py --auto-advance
```

## Phase 개요

| Phase | 핵심 | Validator |
|-------|------|-----------|
| 0 | PRD 생성 | PRD 문서 존재, 50줄 이상 |
| 0.5 | Task 분해 | Task 파일 존재, 체크리스트 |
| 1 | 구현 + 테스트 | 1:1 테스트 페어링 |
| 2 | 테스트 통과 | pytest 100% 통과 |
| 2.5 | 코드 리뷰 | 린트 + 보안 스캔 |
| 3 | 버전 결정 | Conventional Commits |
| 4 | PR 생성 | gh pr create |
| 5 | E2E + Security | Playwright + audit |
| 6 | 배포 | 사용자 확인 필수 |

## Phase 0: PRD 생성

### 검증 조건

- [ ] `tasks/prds/NNNN-*.md` 파일 존재
- [ ] 최소 50줄 이상
- [ ] 필수 섹션 포함 (Purpose, Features, Timeline)

### 검증 명령

```powershell
.\scripts\validate-phase-0.ps1 <prd-number>
```

## Phase 0.5: Task 분해

### 검증 조건

- [ ] `tasks/PRD-NNNN-tasks.md` 파일 존재
- [ ] 체크리스트 형식 (- [ ])
- [ ] Task 0.0 (브랜치 생성) 포함

### 검증 명령

```powershell
.\scripts\validate-phase-0.5.ps1 <prd-number>
```

## Phase 1: 구현 + 테스트

### 검증 조건

- [ ] 1:1 테스트 페어링 (`src/*.py` → `tests/test_*.py`)
- [ ] 구현 파일 존재
- [ ] 테스트 파일 존재

### 검증 명령

```powershell
.\scripts\validate-phase-1.ps1
```

## Phase 2: 테스트 통과

### 검증 조건

- [ ] `pytest tests/ -v` 100% 통과
- [ ] 커버리지 > 70% (권장)

### 검증 명령

```powershell
.\scripts\validate-phase-2.ps1
```

## Phase 2.5: 코드 리뷰

### 검증 조건

- [ ] ruff check 통과
- [ ] black --check 통과
- [ ] mypy 경고 없음 (권장)

### 검증 명령

```powershell
.\scripts\validate-phase-2.5.ps1
```

또는 `/parallel-review` 실행

## Phase 3: 버전 결정

### 검증 조건

- [ ] Conventional Commits 형식 준수
- [ ] MAJOR/MINOR/PATCH 결정

### 자동 결정 규칙

```
feat!: BREAKING CHANGE → MAJOR
feat:  새 기능        → MINOR
fix:   버그 수정      → PATCH
```

## Phase 4: PR 생성

### 검증 조건

- [ ] PR 생성됨 (`gh pr view`)
- [ ] PR 제목이 Conventional Commit 형식
- [ ] PR 본문에 Summary, Test Plan 포함

### 검증 명령

```powershell
.\scripts\validate-phase-4.ps1
```

## Phase 5: E2E + Security

### 검증 조건

- [ ] Playwright 테스트 통과
- [ ] pip-audit 통과
- [ ] npm audit 통과 (해당 시)
- [ ] Critical 취약점 없음

### 검증 명령

```powershell
.\scripts\validate-phase-5.ps1
```

## Phase 6: 배포

### 검증 조건

- [ ] 모든 이전 Phase 통과
- [ ] **사용자 확인 필수**
- [ ] 배포 체크리스트 완료

### 자동 진행 중지 조건

| 조건 | 중지 |
|------|------|
| MAJOR 버전 | ⏸️ |
| Critical 취약점 | ⏸️ |
| 배포 단계 | ⏸️ |
| 3회 실패 | ⏸️ |

## 자동 진행

```bash
# 현재 Phase 완료 후 다음 Phase로 자동 진행
python scripts/validate_phase.py --auto-advance

# 특정 Phase까지 자동 진행
python scripts/validate_phase.py --advance-to 5
```

## 상태 대시보드

```bash
python scripts/validate_phase.py --status

# 출력 예시:
# Phase 0  ✅ PRD 생성 완료
# Phase 0.5 ✅ Task 분해 완료
# Phase 1  ✅ 구현 완료 (5/5 파일)
# Phase 2  🔄 테스트 진행 중 (3/5 통과)
# Phase 3  ⏳ 대기 중
# ...
```

## 관련 도구

| 도구 | 용도 |
|------|------|
| `scripts/validate_phase.py` | 통합 검증 |
| `scripts/validate-phase-*.ps1` | 개별 Phase 검증 |
| `scripts/phase-status.ps1` | 상태 확인 |

---

> 참조: CLAUDE.md 섹션 4 Phase Pipeline
