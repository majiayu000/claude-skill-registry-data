---
name: jwc-convex-backend-changes
description: Convex 기반 백엔드(@jwc/backend)에서 schema/쿼리/뮤테이션/액션을 안전하게 변경하고 codegen/dev로 검증합니다. Node 전용 액션("use node")과 비밀값 로그 금지 규칙을 포함합니다.
---

# Convex Backend Changes (@jwc/backend)

## 언제 사용하나요?

- `packages/backend/convex/*`에 기능을 추가/수정할 때
- schema 변경, 인덱스 추가, http 라우팅 변경, cron/workpool 변경
- SMS/Google Sheets 등 외부 연동 액션 수정

## 빠른 경로(가장 흔한 작업)

### 1) Node 버전/환경

- Node 버전은 루트 `.nvmrc` 기준:
  - `nvm use`

### 2) 변경 → 검증 루프

1. 타입체크:
- `pnpm -C packages/backend typecheck`

2. 린트:
- `pnpm -C packages/backend lint`

3. Convex 코드젠(필요 시):
- `pnpm -C packages/backend convex:codegen`

4. 로컬 dev(필요 시):
- `pnpm -C packages/backend convex:dev`

## 작업별 체크리스트

### A) schema.ts 수정

- 새 테이블/필드 추가 시:
  - 인덱스/서치 인덱스 영향 범위를 먼저 확인
  - codegen으로 타입 갱신

### B) 액션/뮤테이션/쿼리 추가

- args validator를 명확히 정의
- 에러 메시지는 구체적으로(민감정보는 포함 금지)
- 전화번호/키/토큰 등 개인정보/비밀값은 로그에 출력하지 않음

### C) Node 전용 코드

- Node 런타임 전용이면 파일 상단에 `"use node"` 유지

## 참고(레포 규칙)

- 상세 규칙: [packages/backend/AGENTS.md](packages/backend/AGENTS.md)
- 공통 규칙: [AGENTS.md](AGENTS.md)
