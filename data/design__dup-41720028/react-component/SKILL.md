---
name: react-component
description: React 컴포넌트 생성, shadcn/ui 통합 작업 시 사용. component, 컴포넌트, UI, shadcn 키워드에 자동 활성화.
allowed-tools: Read, Write, Glob
---

# React Component Helper

## 컴포넌트 구조

- 위치: `src/components/`
- 네이밍: PascalCase
- 파일: `.tsx` 확장자

### 디렉토리 구조

```
src/components/
├── ui/           # shadcn/ui 컴포넌트
├── shared/       # 공통 컴포넌트
├── layout/       # 레이아웃 컴포넌트
├── forms/        # 폼 관련 컴포넌트
└── features/     # 기능별 컴포넌트
```

## shadcn/ui 통합

- 설치: `npx shadcn@latest add [component]`
- 위치: `src/components/ui/`
- 커스터마이징: Tailwind CSS

### 자주 사용하는 컴포넌트

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add table
```

## 컴포넌트 템플릿

```tsx
import { cn } from "@/lib/utils"

interface ComponentProps {
  className?: string
  children?: React.ReactNode
}

export function Component({ className, children }: ComponentProps) {
  return (
    <div className={cn("base-styles", className)}>
      {children}
    </div>
  )
}
```

## 패턴

- Compound Components: 복합 컴포넌트 패턴
- Render Props: 필요시 사용
- Custom Hooks: 로직 분리 (`src/hooks/`)
- forwardRef: DOM 참조 필요시
