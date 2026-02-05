---
name: jwc-workspace-validation
description: pnpm+turbo 모노레포에서 Node 버전(.nvmrc)과 터보 task 의존성을 고려해 lint/typecheck/build를 안전하게 실행하고, 실패 시 패키지 단위로 범위를 좁혀 원인을 찾습니다.
---

# JWC Workspace Validation

## 언제 사용하나요?

- 변경 후 `lint`/`typecheck`/`build`가 깨졌을 때
- CI에서 `turbo` 파이프라인이 실패했는데 원인 추적이 필요할 때
- “워크스페이스 전체”가 아니라 **특정 패키지**만 빠르게 검증하고 싶을 때

## 핵심 사실(이 레포의 터보 구성)

- 루트의 `pnpm -w lint`는 `turbo run lint`를 실행합니다.
- 이 레포의 `lint`/`typecheck`는 터보에서 `^build`에 의존합니다.
  - 즉, **lint/typecheck가 build를 선행 실행**할 수 있습니다.
  - 전체 lint가 실패하면, 먼저 “어느 패키지의 build가 터졌는지”를 확인해야 합니다.

## 표준 워크플로우

### 1) Node / pnpm 정합성

1. Node 버전 맞추기(권장):
   - `nvm use` (루트 `.nvmrc` 사용)
2. pnpm 버전 확인:
   - 루트 `package.json#packageManager`가 기준입니다.

### 2) 변경 범위에 맞춰 ‘좁게’ 검증(권장)

- 한 패키지 변경이면, 먼저 패키지 단위로:
  - `pnpm -C packages/<pkg> lint`
  - `pnpm -C packages/<pkg> typecheck`
  - 필요 시 `pnpm -C packages/<pkg> build`

이 방식은 터보의 `^build` 전파 때문에 “연쇄 build 실패”로 디버깅이 어려워지는 것을 줄입니다.

### 3) 워크스페이스 전체 검증(마지막 단계)

- 전체 lint + 워크스페이스 검증:
  - `pnpm -w lint`
- 전체 타입체크:
  - `pnpm -w typecheck`
- 전체 빌드:
  - `pnpm -w build`

## 실패 시 빠른 분기

### A) `pnpm -w lint`가 build 단계에서 실패할 때

- 터보 출력에서 실패한 task를 먼저 찾습니다(예: `@jwc/schema#build`).
- 해당 패키지로 내려가서 단독 재현:
  - `pnpm -C packages/schema build`

### B) Node 버전 관련 오류가 의심될 때

- 이 레포는 `.nvmrc`로 Node를 고정합니다.
- `node -v`가 다르면 `nvm use`로 맞추고 다시 시도합니다.

### C) 의존성/워크스페이스 규칙 위반(manypky check 등)

- 루트 lint에는 `manypkg check`가 포함됩니다.
- 패키지 `package.json` 변경 후라면, 루트에서 재검증:
  - `pnpm -w lint`

## 보안

- `.env` 및 비밀값은 커밋/로그에 남기지 않습니다.
- 실패 로그를 공유할 때는 키/토큰/전화번호 등 민감정보를 마스킹합니다.
