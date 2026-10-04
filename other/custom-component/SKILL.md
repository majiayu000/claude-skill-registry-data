---
name: custom-component
description: 비대한 React 컴포넌트를 스코프별 서브 컴포넌트로 분리, 시맨틱 HTML 적용, 전용 서브디렉토리 구조화
triggers:
  - custom-component
  - 컴포넌트 분리
  - 컴포넌트화
  - split component
argument-hint: "<component-file-path>"
quality: high
---

# Custom Component

비대한 React 컴포넌트의 스코프별 서브 컴포넌트 분리, 시맨틱 HTML 적용, 전용 서브디렉토리 구조화.

## When to Activate

- 단일 컴포넌트가 100줄 이상이고 여러 시각적/논리적 영역을 포함할 때
- 컴포넌트 내부에 조건부 렌더링이 복잡하게 얽혀 있을 때
- `$ARGUMENTS`로 대상 컴포넌트 파일 경로가 주어질 때

## Workflow

### 1단계: 분석

1. 대상 컴포넌트 파일 읽기
2. 해당 컴포넌트의 사용처와 의존성 Grep 파악
3. 프로젝트 내 기존 컴포넌트 분리 패턴 탐색 (예: `tier-card/` 패턴)

### 2단계: 분리 설계

1. 시각적/논리적 영역별 분리 지점 식별
2. 각 영역에 적합한 시맨틱 HTML 태그 매핑:
   - 페이지 섹션 → `<section>`
   - 도입부/제목 → `<header>`
   - 보조/장식 콘텐츠 → `<aside>`
   - 이름-값 쌍 → `<dl>/<dt>/<dd>`
   - 동적 알림 → `role="alert"`
3. 각 서브 컴포넌트의 책임과 props interface 정의

### 3단계: 서브 컴포넌트 생성

1. 의존성 없는 서브 컴포넌트부터 생성 (leaf → root 순서)
2. 레이아웃 컴포넌트는 `children: ReactNode` 기반 composition 패턴 사용
3. prop pass-through 발생 시 children composition 대체

### 4단계: 오케스트레이터 리팩터

1. 오케스트레이터 JSX는 HTML 태그 없이 컴포넌트만 조합:
   ```tsx
   <Layout>
     <Content>
       <ChildA ... />
       <ChildB />
     </Content>
     <Sidebar />
   </Layout>
   ```
2. 오케스트레이터 로직(상태, 이펙트, 핸들러, API 호출)은 전용 훅으로 분리 (`/custom-hook` 참조)
3. 서브 컴포넌트로 이동한 import 정리

### 5단계: 디렉토리 구조화

1. 오케스트레이터 전용 서브 모듈은 동명 서브디렉토리 안의 `_components/`, `_hooks/`로 분류:
   ```
   component.tsx
   component/
     _components/
       sub-a.tsx
       sub-b.tsx
     _hooks/
       use-sub-action.ts
   ```
2. 서브 컴포넌트 전용 훅은 `_hooks/` 하위 배치, 전용 서브 훅은 훅 동명 서브디렉토리에 배치:
   ```
   component/
     _hooks/
       use-sub-action.ts
       use-sub-action/
         use-state.ts
         use-auth.ts
   ```
3. 다른 곳에서도 사용되는 독립 컴포넌트/훅은 상위 디렉토리에 유지
4. import 경로 업데이트

### 6단계: 검증

1. `pnpm build` 성공 확인
2. `pnpm lint` 통과 확인
3. 시각적 변경 없음 확인 (Tailwind preflight가 시맨틱 태그 기본 스타일 초기화)

## Constraints

- 오케스트레이터 JSX의 HTML 태그 금지 — 컴포넌트만 조합
- prop pass-through 대신 children composition 패턴 우선
- 프로젝트 코드 규칙 준수 (CLAUDE.md 참조): arrow function, named export, Tailwind only 등
- 기존 프로젝트 분리 패턴(tier-card/ 등) 기준 일관성 유지

## Success Criteria

- 오케스트레이터 return문의 HTML 태그 없음
- 각 서브 컴포넌트의 단일 책임
- 전용 서브 컴포넌트의 하위 디렉토리 격리
- 빌드/린트 통과
- 시각적 변경 없음
