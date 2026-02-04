---
name: jwc-ui-shadcn-workflow
description: packages/ui의 shadcn/ui + Tailwind v4 컴포넌트를 추가/수정할 때 기존 컴포넌트 재사용, cn()/cva 패턴, exports 영향, lint/typecheck 절차를 따릅니다.
---

# UI (shadcn + Tailwind v4) Workflow

## 언제 사용하나요?

- `packages/ui/src/components/shadcn/*` 컴포넌트를 추가/수정할 때
- className 병합, variants(cva), Radix 컴포넌트 조합을 해야 할 때
- exports 경로가 깨지지 않게 안전하게 변경하고 싶을 때

## 작업 원칙(요약)

- 새 컴포넌트 전에 **기존 컴포넌트 재사용**부터 검토
- className 조합은 `cn()` 사용
- Tailwind class 정렬 경고가 있을 수 있으니 `useSortedClasses`를 염두
- 아이콘은 `lucide-react`만 사용(이모지 금지)

## 변경 절차

1) 변경 범위 최소화
- 먼저 해당 파일/컴포넌트만 수정

2) 스크립트로 shadcn 추가가 필요한 경우(선택)
- `pnpm -C packages/ui ui-add`

3) 패키지 검증
- `pnpm -C packages/ui lint`
- `pnpm -C packages/ui typecheck`

## exports 영향 체크

- `packages/ui/package.json#exports`에 경로가 고정되어 있습니다.
- 파일 이동/이름 변경은 소비측 import를 깨뜨릴 수 있으니, 변경 전후로 영향 범위를 확인합니다.

## 참고

- UI 상세 규칙: [packages/ui/AGENTS.md](packages/ui/AGENTS.md)
- 공통 규칙: [AGENTS.md](AGENTS.md)
