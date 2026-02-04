---
name: sdd-workflow
description: >
  SDD(Spec Driven Development) 자동화 워크플로우를 실행합니다.
  사용자가 "다음 작업 진행해줘", "구현 시작해줘", "SDD 워크플로우 실행" 등을 요청할 때 활성화됩니다.
  작업 분할, 계획서 작성, 구현, CI 검증까지 자동으로 진행합니다.
---

# SDD Workflow Skill

이 스킬은 Spec Driven Development 워크플로우를 자동으로 실행합니다.

## 워크플로우 개요

```
1. 분석 → 2. 계획 → 3. 구현 → 4. Push → 5. CI 확인 → 6. 수정(필요시)
```

---

## 환경 요구사항

이 워크플로우는 **사용자 개입 없이** 자동으로 실행됩니다.

### GitHub CLI (gh) 자동 설정

CI 상태 확인을 위해 GitHub CLI가 필요합니다. 스크립트가 자동으로 처리합니다:

1. **자동 설치**: `gh` 명령어가 없으면 자동으로 설치
   - Linux: apt, yum, pacman 또는 바이너리 직접 설치
   - macOS: brew 또는 바이너리 직접 설치

2. **자동 인증**: 다음 환경변수 중 하나를 사용
   - `GITHUB_TOKEN`: GitHub Personal Access Token
   - `GH_TOKEN`: gh CLI 기본 환경변수

### 필수 환경변수

```bash
# 다음 중 하나 설정 (repo, workflow 권한 필요)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
# 또는
export GH_TOKEN="ghp_xxxxxxxxxxxx"
```

### 권한 요구사항

토큰에 필요한 권한:
- `repo`: 저장소 접근
- `workflow`: 워크플로우 실행 조회

---

## Phase 1: 분석 (Analyze)

### 1.1 추적성 매트릭스 분석

`specs/TRACEABILITY.md` 파일을 읽어서 현재 상태를 파악합니다:

1. **우선순위 확인**: 구현 우선순위 섹션에서 다음 작업 식별
2. **상태 확인**: 각 명세의 상태를 확인
   - `⏳ 대기`: 구현 대기 중 (작업 대상)
   - `🚧 진행중`: 이미 작업 중
   - `✅ 완료`: 완료됨
3. **의존성 확인**: 의존성 그래프에서 선행 조건 확인

### 1.2 다음 작업 선택 기준

1. 의존성이 해결된 명세 중 가장 높은 우선순위
2. `⏳ 대기` 상태인 명세
3. Phase 순서 준수 (Phase 1 → Phase 2 → Phase 3)

---

## Phase 2: 계획 (Plan)

### 2.1 계획서 작성

선택한 명세에 대해 `specs/plans/PLAN-XXX.md` 파일을 생성합니다.

**계획서 ID 규칙:**
- 관련 명세 ID를 기반으로 생성
- 예: FEAT-001 구현 → PLAN-001

**계획서 포함 내용:**
1. 목표 정의
2. 작업을 적절한 크기로 분할 (각 단계는 1-2시간 분량)
3. 예상 변경 파일 목록
4. 검증 방법
5. 롤백 계획

### 2.2 작업 분할 원칙

- **단일 책임**: 각 단계는 하나의 명확한 목표
- **테스트 가능**: 각 단계 완료 후 검증 가능
- **되돌림 가능**: 문제 시 이전 단계로 롤백 가능
- **적정 크기**: 너무 크지도, 너무 작지도 않게

---

## Phase 3: 구현 (Implement)

### 3.1 구현 순서

1. 계획서의 각 단계를 순서대로 실행
2. 각 단계 완료 시 체크박스 업데이트
3. 관련 테스트가 있다면 함께 작성
4. 추적성 매트릭스 상태 업데이트 (`⏳ 대기` → `🚧 진행중`)

### 3.2 코드 작성 규칙

- 명세 ID를 주석으로 포함: `@spec FEAT-001`
- 기존 패턴과 일관성 유지
- 에러 처리 포함
- 필요한 경우 타입 정의 추가

### 3.3 추적성 매트릭스 업데이트

구현 완료 후 `specs/TRACEABILITY.md` 업데이트:
- 구현 파일 경로 추가
- 테스트 파일 경로 추가
- 상태를 `🧪 테스트중` 또는 `✅ 완료`로 변경

---

## Phase 4: Push 및 CI 확인

### 4.1 Git 커밋

```bash
git add .
git commit -m "feat(SPEC-ID): 구현 설명"
```

**커밋 메시지 형식:**
- `feat(FEAT-001): Add user authentication`
- `fix(API-002): Fix response format`
- `docs(PLAN-001): Add implementation plan`

### 4.2 Push

```bash
git push -u origin <current-branch>
```

### 4.3 CI 상태 확인

Push 후 GitHub Actions CI 완료를 자동으로 대기합니다.

**자동화 스크립트 사용:**

```bash
# 스크립트가 gh CLI 설치/인증/모니터링을 모두 처리
.claude/skills/sdd-workflow/scripts/check-ci.sh
```

**스크립트 동작:**
1. gh CLI 설치 확인 (없으면 자동 설치)
2. GITHUB_TOKEN/GH_TOKEN으로 자동 인증
3. Push 후 10초 대기 (워크플로우 시작 대기)
4. 30초 간격으로 상태 확인 (최대 10분)
5. 완료 시 결과 반환

**수동 확인 (필요시):**

```bash
# CI 실행 상태 확인
gh run list --limit 1

# CI 완료 대기
gh run watch
```

---

## Phase 5: CI 실패 시 수정

### 5.1 실패 분석

```bash
# 실패한 run의 로그 확인
gh run view <run-id> --log-failed
```

### 5.2 수정 및 재시도

1. 실패 원인 분석
2. 코드 수정
3. 재커밋 및 push
4. CI 재확인

**최대 재시도 횟수: 3회**

3회 실패 시:
- 현재까지의 시도 내용 요약
- 사용자에게 도움 요청
- 추적성 매트릭스 상태를 `❌ 실패`로 변경

---

## Phase 6: 완료

### 6.1 최종 확인

- [ ] CI 통과
- [ ] 추적성 매트릭스 업데이트
- [ ] 계획서 체크박스 모두 완료

### 6.2 다음 작업 안내

현재 작업 완료 후:
1. 완료된 작업 요약 출력
2. 다음 우선순위 작업 안내
3. 사용자에게 계속 진행할지 확인

---

## 실행 예시

사용자가 "다음 작업 진행해줘"라고 요청하면:

1. `specs/TRACEABILITY.md` 분석
2. 다음 작업 식별 (예: FEAT-001)
3. `specs/features/FEAT-001.md` 명세 읽기
4. `specs/plans/PLAN-001.md` 계획서 작성
5. 계획대로 구현
6. 추적성 매트릭스 업데이트
7. Git commit & push
8. CI 완료 대기
9. 결과 보고

---

## 주의사항

- **명세 없이 구현 금지**: 항상 명세가 먼저
- **매트릭스 동기화**: 모든 변경은 즉시 매트릭스에 반영
- **점진적 진행**: 한 번에 하나의 명세만 구현
- **실패 시 중단**: 3회 실패 시 사용자 개입 요청

---

## 참고 파일

- 계획서 템플릿: `.claude/skills/sdd-workflow/plan-template.md`
- 추적성 매트릭스: `specs/TRACEABILITY.md`
- CI 워크플로우: `.github/workflows/ci.yml`
- CI 상태 확인 스크립트: `.claude/skills/sdd-workflow/scripts/check-ci.sh`
