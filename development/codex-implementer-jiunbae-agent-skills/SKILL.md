---
name: codex-implementer
description: Codex CLI를 sub-agent로 활용하여 실제 구현 작업을 수행합니다. Claude가 작업을 분석/분해하고, Codex가 코드 작성/수정/리팩토링을 담당합니다. "Codex로 구현", "구현해줘", "코드 작성해줘", "병렬 구현" 요청 시 활성화됩니다.
---

# Codex Implementer (멀티 에이전트 구현)

## Overview

Claude가 오케스트레이터로서 작업을 분석하고, Codex CLI를 sub-agent로 호출하여 실제 구현 작업을 수행하는 스킬입니다.

**핵심 아이디어:**
- Claude: 분석, 설계, 작업 분해, 결과 검토 및 통합
- Codex: 실제 코드 구현, 버그 수정, 리팩토링, 테스트 작성

**지원 구현 패턴:**
- **단일 구현**: 하나의 기능/파일을 Codex가 구현
- **병렬 구현**: 여러 파일/기능을 동시에 여러 Codex가 구현
- **점진적 구현**: 단계별로 Codex가 순차 구현 + Claude 검토
- **리팩토링**: 기존 코드 개선을 Codex에게 위임

**Codex의 강점:**
- full-auto 모드로 자율적 구현 가능
- 로컬 파일 시스템 직접 접근
- 터미널 명령 실행 가능
- 빠른 반복 작업에 적합

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:

**명시적 요청:**
- "Codex로 구현해줘"
- "구현을 Codex에게 맡겨줘"
- "병렬로 구현해줘"
- "Codex 에이전트로 작업해줘"

**권장 상황:**
- 구현할 기능이 명확히 정의되었을 때
- 여러 파일을 동시에 수정해야 할 때
- 반복적인 코드 작성 작업이 있을 때
- 빠른 프로토타이핑이 필요할 때

## Prerequisites

### OpenAI Codex CLI 설치

```bash
# npm으로 설치
npm install -g @openai/codex

# 설치 확인
codex --version
```

### 환경 변수 설정

```bash
# Codex CLI용 OpenAI API 키
export OPENAI_API_KEY="sk-..."
```

### Codex 승인 모드 설정

```bash
# full-auto 모드 권장 (자율 실행)
# suggest-edit: 편집 제안만
# auto-edit: 파일 편집 자동 승인
# full-auto: 모든 작업 자동 승인 (권장)
```

## Workflow

### Mode 1: 단일 구현 (Single Implementation)

하나의 기능을 Codex가 구현합니다.

#### Step 1: 요구사항 분석

Claude가 구현할 기능을 분석합니다:

```
사용자: "사용자 로그인 API 엔드포인트를 만들어줘"

Claude 분석:
- 기능: POST /api/auth/login
- 입력: email, password
- 출력: JWT 토큰
- 필요 파일: routes/auth.ts, services/authService.ts
```

#### Step 2: Codex 호출

분석 결과를 바탕으로 Codex를 호출합니다:

```bash
codex -a full-auto "다음 기능을 구현해주세요:

## 요구사항
- POST /api/auth/login 엔드포인트 생성
- email, password로 인증
- 성공 시 JWT 토큰 반환
- 실패 시 적절한 에러 응답

## 파일 위치
- routes/auth.ts에 라우트 추가
- services/authService.ts에 인증 로직 구현

## 기존 패턴 참고
- routes/users.ts의 라우트 패턴 따르기
- 기존 에러 핸들링 패턴 유지"
```

#### Step 3: 결과 확인

Codex 실행 완료 후 Claude가 결과를 검토합니다:
- 생성/수정된 파일 확인
- 코드 품질 검토
- 테스트 실행 제안

---

### Mode 2: 병렬 구현 (Parallel Implementation)

여러 기능을 동시에 여러 Codex 인스턴스가 구현합니다.

#### Step 1: 작업 분해

Claude가 작업을 독립적인 단위로 분해합니다:

```
사용자: "CRUD API를 만들어줘 (users, posts, comments)"

Claude 작업 분해:
- Task 1: users CRUD (routes/users.ts, services/userService.ts)
- Task 2: posts CRUD (routes/posts.ts, services/postService.ts)
- Task 3: comments CRUD (routes/comments.ts, services/commentService.ts)
```

#### Step 2: 병렬 Codex 호출

각 작업을 별도의 Codex 프로세스로 실행합니다:

```bash
# Terminal 1
codex -a full-auto "users CRUD API를 구현해주세요..."

# Terminal 2 (동시 실행)
codex -a full-auto "posts CRUD API를 구현해주세요..."

# Terminal 3 (동시 실행)
codex -a full-auto "comments CRUD API를 구현해주세요..."
```

**Claude에서 병렬 실행:**
```
Claude가 여러 Bash 명령을 동시에 실행하여 병렬 처리합니다.
각 Codex는 독립적인 파일을 작업하므로 충돌이 없습니다.
```

#### Step 3: 통합 및 검토

모든 Codex 완료 후:
- 생성된 코드 간 일관성 확인
- 공통 로직 추출 여부 검토
- 통합 테스트 실행

---

### Mode 3: 점진적 구현 (Incremental Implementation)

복잡한 기능을 단계별로 구현하며 Claude가 각 단계를 검토합니다.

#### Step 1: 단계 정의

```
Phase 1: 기본 구조 생성
Phase 2: 핵심 로직 구현
Phase 3: 에러 처리 추가
Phase 4: 테스트 작성
```

#### Step 2: 단계별 실행

```bash
# Phase 1
codex -a full-auto "Phase 1: 기본 파일 구조와 스켈레톤 코드를 생성해주세요..."

# Claude 검토 후...

# Phase 2
codex -a full-auto "Phase 2: 핵심 비즈니스 로직을 구현해주세요.
기존 파일: [Phase 1에서 생성된 파일 목록]..."

# 반복...
```

#### Step 3: 최종 검토

모든 단계 완료 후 전체 코드 리뷰 및 테스트

---

### Mode 4: 리팩토링 위임 (Refactoring Delegation)

기존 코드 개선을 Codex에게 위임합니다.

#### Step 1: 리팩토링 범위 정의

```
사용자: "이 파일의 중복 코드를 제거해줘"

Claude 분석:
- 대상 파일: services/userService.ts
- 문제점: validateUser, validateAdmin에 중복 로직
- 해결: 공통 validate 함수 추출
```

#### Step 2: Codex 리팩토링 실행

```bash
codex -a full-auto "다음 리팩토링을 수행해주세요:

## 대상 파일
services/userService.ts

## 리팩토링 목표
1. validateUser와 validateAdmin의 공통 로직을 baseValidate로 추출
2. 각 함수에서 baseValidate 호출하도록 수정
3. 기존 테스트가 통과하는지 확인

## 제약 조건
- 외부 인터페이스(함수 시그니처) 유지
- 기존 동작 변경 없음"
```

## Examples

### 예시 1: 단일 기능 구현

```
사용자: Codex로 비밀번호 재설정 기능을 구현해줘

Claude: 비밀번호 재설정 기능을 분석하고 Codex에게 구현을 위임합니다.

## 기능 분석
- 이메일로 재설정 링크 발송
- 토큰 기반 인증
- 새 비밀번호 설정

Codex를 호출합니다...

[Codex 실행]
codex -a full-auto "비밀번호 재설정 기능을 구현해주세요:
1. POST /api/auth/forgot-password - 재설정 이메일 발송
2. POST /api/auth/reset-password - 새 비밀번호 설정
기존 auth 라우트 패턴을 따라주세요."

[실행 완료]

## Codex 구현 결과
- routes/auth.ts: 2개 엔드포인트 추가
- services/authService.ts: resetPassword 로직 추가
- utils/email.ts: sendResetEmail 함수 추가

## 검토 사항
✅ 기존 패턴과 일관성 유지
✅ 토큰 만료 처리 포함
⚠️ 테스트 추가 권장

테스트를 작성할까요?
```

### 예시 2: 병렬 구현

```
사용자: 3개의 Codex 에이전트로 dashboard, settings, profile 페이지를 동시에 만들어줘

Claude: 3개의 Codex 에이전트를 병렬로 실행하여 각 페이지를 구현합니다.

## 작업 분배
- Agent 1: Dashboard 페이지 (pages/dashboard/*)
- Agent 2: Settings 페이지 (pages/settings/*)
- Agent 3: Profile 페이지 (pages/profile/*)

## 병렬 실행 중...

[Agent 1 - Dashboard] 실행 중...
[Agent 2 - Settings] 실행 중...
[Agent 3 - Profile] 실행 중...

✓ Agent 1 완료 (45초)
✓ Agent 3 완료 (52초)
✓ Agent 2 완료 (58초)

## 구현 결과 요약

### Dashboard (Agent 1)
- pages/dashboard/index.tsx
- pages/dashboard/components/StatsCard.tsx
- pages/dashboard/hooks/useDashboardData.ts

### Settings (Agent 2)
- pages/settings/index.tsx
- pages/settings/components/SettingsForm.tsx
- pages/settings/hooks/useSettings.ts

### Profile (Agent 3)
- pages/profile/index.tsx
- pages/profile/components/ProfileCard.tsx
- pages/profile/hooks/useProfile.ts

## 통합 검토
✅ 컴포넌트 네이밍 일관성
✅ 공통 레이아웃 사용
✅ 라우팅 설정 완료

빌드 및 테스트를 실행할까요?
```

### 예시 3: 버그 수정 위임

```
사용자: 이 버그를 Codex로 수정해줘: "장바구니에서 수량 변경 시 총액이 업데이트되지 않음"

Claude: 버그를 분석하고 Codex에게 수정을 위임합니다.

## 버그 분석
- 증상: 수량 변경 후 totalPrice가 갱신되지 않음
- 관련 파일: components/Cart.tsx, hooks/useCart.ts
- 원인 추정: useEffect 의존성 배열 누락

Codex를 호출합니다...

[Codex 실행]
codex -a full-auto "다음 버그를 수정해주세요:

## 버그 설명
장바구니에서 상품 수량 변경 시 총액(totalPrice)이 업데이트되지 않음

## 관련 파일
- components/Cart.tsx
- hooks/useCart.ts

## 수정 후 확인 사항
- 수량 변경 시 총액 즉시 반영
- 기존 테스트 통과
- 새로운 테스트 케이스 추가"

[실행 완료]

## 수정 결과
- hooks/useCart.ts: useEffect 의존성 배열에 items 추가
- components/Cart.tsx: 불필요한 로컬 상태 제거
- tests/Cart.test.tsx: 수량 변경 테스트 추가

✅ 테스트 통과
✅ 버그 수정 완료
```

## Configuration

### Codex 실행 옵션

```yaml
# 권장 설정
codex_options:
  approval_mode: "full-auto"  # 자율 실행 (권장)
  model: "o4-mini"            # 또는 "gpt-4o"
  timeout: 300                # 5분 타임아웃

# 모드별 설정
modes:
  single:
    max_files: 5
    timeout: 180

  parallel:
    max_agents: 5
    timeout: 300

  incremental:
    phases: 4
    review_between_phases: true
```

### 병렬 실행 설정

```yaml
parallel:
  max_concurrent: 3      # 동시 실행 Codex 수
  wait_strategy: "all"   # all: 전체 완료 대기, any: 하나라도 완료 시
  conflict_check: true   # 파일 충돌 사전 검사
```

## Best Practices

**DO:**
- 구현 전 Claude에게 충분한 컨텍스트 제공
- 병렬 구현 시 작업 간 파일 충돌 없도록 분리
- Codex 실행 후 Claude 검토 단계 포함
- 점진적 구현으로 복잡한 기능 분해
- 기존 코드 패턴을 프롬프트에 명시

**DON'T:**
- 모호한 요구사항으로 Codex 호출
- 동일 파일을 여러 Codex가 동시 수정
- Codex 결과를 검토 없이 사용
- 너무 많은 병렬 에이전트 (5개 이상)
- 전체 프로젝트 리팩토링을 한 번에 위임

## Codex CLI Quick Reference

```bash
# 기본 실행 (대화형)
codex "프롬프트"

# 승인 모드 지정
codex -a full-auto "프롬프트"
codex -a auto-edit "프롬프트"
codex -a suggest-edit "프롬프트"

# 비대화형 실행 (exec 서브커맨드)
codex exec "프롬프트"

# 조합 예시 (대화형)
codex -a full-auto "구현 프롬프트"

# 조합 예시 (비대화형 - 스크립트에서 사용)
codex exec -a full-auto "구현 프롬프트"
```

## Troubleshooting

### Codex CLI 오류

```bash
# 설치 확인
codex --version

# API 키 확인
echo $OPENAI_API_KEY

# 직접 테스트 (비대화형)
codex exec "Hello, world를 출력하는 Python 코드를 작성해"
```

### 병렬 실행 시 파일 충돌

- 작업 분해 시 파일 의존성 확인
- 동일 파일을 여러 Codex가 수정하지 않도록 분리
- 공통 파일은 마지막에 별도 Codex로 통합

### 타임아웃 발생

- 작업 범위 축소
- 단계별 구현으로 전환
- 모델을 더 빠른 것으로 변경 (o4-mini)

### Codex가 잘못된 파일 수정

- 프롬프트에 파일 경로 명시
- 기존 파일 구조 설명 추가
- working directory 지정

## Integration with Claude

### Claude의 역할

1. **분석**: 요구사항 분석, 작업 분해
2. **오케스트레이션**: Codex 호출 시점/방법 결정
3. **검토**: Codex 결과 품질 검토
4. **통합**: 여러 Codex 결과 통합
5. **커뮤니케이션**: 사용자에게 진행 상황 보고

### Codex의 역할

1. **구현**: 실제 코드 작성
2. **수정**: 기존 코드 변경
3. **실행**: 테스트, 빌드 등 명령 실행
4. **탐색**: 코드베이스 탐색 (필요시)

### 협업 흐름

```
사용자 요청
    ↓
Claude 분석 (요구사항 파악)
    ↓
Claude 설계 (작업 분해)
    ↓
Codex 구현 (병렬/순차)
    ↓
Claude 검토 (품질 확인)
    ↓
결과 보고 + 추가 작업 제안
```

## Resources

- `./templates/implementation_prompt.md`: Codex 호출용 프롬프트 템플릿
- `./references/parallel_patterns.md`: 병렬 구현 패턴 가이드
- `./scripts/orchestrator.sh`: 병렬 Codex 실행 오케스트레이터
- `./config/settings.yaml`: 기본 설정 파일
- [OpenAI Codex CLI](https://github.com/openai/openai-codex): Codex CLI 공식 저장소
