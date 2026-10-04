---
name: project-check
description: 로컬 품질 검증과 실패 원인 분류. AGENTS.md/DESIGN.md 규칙 준수 확인, pnpm 기반 검증, PR 전 점검
---

# 프로젝트 점검

## 원칙

- `pnpm`만 사용
- `npm`, `yarn` 설치/스크립트 실행 금지
- `AGENTS.md` 선행 읽기
- UI/스타일 변경 시 `DESIGN.md` 추가 읽기
- dirty working tree 전제 작업
- 사용자 변경 되돌리기 금지
- 실패는 한 번에 하나씩 분류
- 가장 작은 수정으로 해결

## 실행 순서

### 1. 범위 확인

```bash
git status --short
git diff --name-status --find-renames
git diff --stat
```

변경 파일이 많으면 기능 단위 검증. 스킬, 에이전트, 규칙 파일 변경 시 `.claude`와 `.agents` 동기화 확인.

### 2. 규칙 준수 확인

다음 항목 빠른 확인.

- 파일/디렉터리 이름 kebab-case 여부
- Tailwind class 사용 여부
- inline style 금지 준수 여부
- 조건부 class의 `cn` 사용 여부
- `useMemo`, `useCallback` 추가 여부
- `useEffect`의 return 직전 위치와 JSDoc 설명 여부
- 객체 타입의 `interface` 사용 여부
- 파일 끝 named export 여부
- `../..`보다 깊은 상대 경로의 path alias 처리 여부
- 컴포넌트 디렉터리 `index.ts` 재export 추가 여부

### 3. 로컬 검증

`package.json`에 존재하는 스크립트만 실행. 기본 순서:

```bash
pnpm format:check
pnpm typecheck
pnpm test
pnpm build
```

릴리스/패키징 검증 시 다음 우선:

```bash
pnpm prepublishOnly
```

### 4. 실패 원인 분류

실패 시 다음 순서 처리:

1. 실패 종류를 `format`, `typecheck`, `test`, `build`, `runtime`, `browser` 중 하나로 분류
2. 첫 번째 의미 있는 에러와 관련 파일만 읽기
3. 원인 후보 1-2개로 축소
4. 필요한 최소 수정
5. 실패한 명령 우선 재실행
6. 통과 후 이후 명령 이어서 실행

### 5. 브라우저/수동 UI 확인

직접 테스트, 화면 먹통, UI 회귀, PNG/export 문제 요청 시 `playwright-cli` 스킬 병행.

```bash
pnpm dev
```

브라우저 확인 시 콘솔 에러, 네트워크 실패, 스크린샷, 재현 단계 기록. UI 변경 검증은 `DESIGN.md` 기준.

## 보고 형식

- 실행한 명령과 결과
- 발견한 규칙 위반 또는 실패 원인
- 수정한 파일
- 남은 검증 공백
