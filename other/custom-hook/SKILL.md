---
name: custom-hook
description: 비대한 커스텀 훅을 스코프별 서브 훅으로 분리, composer 패턴 적용, 전용 서브디렉토리 구조화
triggers:
  - custom-hook
  - 훅 분리
  - 커스텀훅 분리
  - split hook
argument-hint: "<hook-file-path>"
quality: high
---

# Custom Hook

비대한 커스텀 훅 로직의 스코프별 서브 훅 분리와 composer 훅 조합 구조 리팩터.

## When to Activate

- 단일 커스텀 훅이 여러 관심사(상태 머신, API 호출, 이펙트, 인증 등)를 포함할 때
- 훅 내부에 독립적으로 테스트/재사용 가능한 로직 덩어리가 보일 때
- `$ARGUMENTS`로 대상 훅 파일 경로가 주어질 때

## Workflow

### 1단계: 분석

1. 대상 훅 파일 읽기
2. 해당 훅의 사용처 Grep 파악
3. 내부 로직의 관심사 식별:
   - 상태 머신 (useState + 전이 함수)
   - API 호출 (fetch 함수 + 결과 처리)
   - 사이드 이펙트 (useEffect)
   - 외부 훅 래핑 (인증, 라우터 등)

### 2단계: 분리 설계

1. 각 관심사를 독립된 서브 훅으로 매핑:
   - 상태 머신 → `use-[name]-state.ts`
   - 인증/외부 서비스 래핑 → `use-[name]-auth.ts` 등
   - 사이드 이펙트 → `use-[name]-callback.ts` 등
2. 여러 관심사를 동시에 건드리는 글루 함수는 composer에 유지
3. 단순 `useState(false)` 수준 상태 분리 금지 — 의미 있는 스코프만 추출

### 3단계: 서브 훅 생성

1. 의존성 없는 서브 훅부터 생성 (leaf → root 순서)
2. 서브 훅 단일 책임:
   - 상태 훅: 상태 + 전이 함수만 반환
   - 이펙트 훅: 콜백 파라미터로 외부 의존성 주입, 반환값 없음
   - 래핑 훅: 외부 훅 + 관련 핸들러 묶어서 반환
3. 순수 async 함수(API 호출 등)는 일반 함수로 유지, composer 파일에 co-locate

### 4단계: Composer 훅 리팩터

1. composer 훅은 서브 훅 조합과 글루 로직만 포함:
   ```ts
   const useComposer = (params) => {
     const state = useSubState(params);
     const auth = useSubAuth();
     useSubCallback({ onSuccess: ... });

     // 글루 로직: 여러 스코프를 연결하는 함수
     const handleResult = (result) => { ... };

     return { ...state, ...auth, handleResult };
   };
   ```
2. 서브 훅으로 이동한 import 정리
3. 타입/인터페이스는 사용 파일에 co-locate

### 5단계: 디렉토리 구조화

1. 컴포넌트 서브디렉토리 내부 훅은 `_hooks/` 폴더에 배치:
   ```
   component/
     _hooks/
       use-action.ts
   ```
2. composer 훅 전용 서브 훅은 동명 서브디렉토리로 이동:
   ```
   _hooks/
     use-hero-action.ts
     use-hero-action/
       use-card-state.ts
       use-hero-auth.ts
       use-rso-callback.ts
   ```
3. 다른 곳에서도 사용되는 범용 훅은 `@/hooks/`에 유지
4. import 경로 업데이트

### 6단계: 검증

1. `pnpm build` 성공 확인
2. `pnpm lint` 통과 확인
3. 기존 동작 변경 없음 확인

## Constraints

- `useMemo`, `useCallback` 사용 금지 (React Compiler 환경)
- 프로젝트 코드 규칙 준수 (CLAUDE.md 참조): arrow function, named export, async/await 등
- 이펙트 훅의 JSDoc 설명 필수
- 글루 함수(여러 스코프를 건드리는 함수)는 composer에 유지 — 억지 분리 금지
- 단순 boolean 토글 등 trivial 상태의 별도 훅 분리 금지

## Success Criteria

- composer 훅의 서브 훅 호출 + 글루 로직만 포함
- 각 서브 훅의 단일 책임
- 전용 서브 훅의 하위 디렉토리 격리
- 빌드/린트 통과
- 기존 동작 변경 없음
