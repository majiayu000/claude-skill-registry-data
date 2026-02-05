---
name: custom-hook
description: Creates custom React hooks for SideDish. Use when the user asks to create a new hook, extract shared logic into a hook, or refactor component logic into reusable hooks. Includes TypeScript interfaces, memoization patterns, and index.ts export.
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Custom Hook Skill

## When to Use
- Creating a new reusable hook (e.g., "create a hook for X")
- Extracting repeated logic from components
- Building hooks for form state, API calls, or UI interactions

## Quick Start

### 1. File Location & Naming
```
src/hooks/useHookName.ts    # 파일명: use + PascalCase
```

### 2. Required Structure

```typescript
/**
 * [훅 이름] 훅
 *
 * [목적 설명]
 * [사용 위치 설명]
 */

import { useState, useCallback } from 'react'
import { toast } from 'sonner'

// 1. Options 인터페이스 (선택적 설정)
export interface UseHookNameOptions {
  initialValue?: string
  onError?: (error: string) => void
  onChange?: (value: string) => void
}

// 2. Return 인터페이스 (JSDoc 주석 권장)
export interface UseHookNameReturn {
  /** 현재 값 */
  value: string
  /** 값 변경 핸들러 */
  setValue: (value: string) => void
  /** 상태 초기화 */
  reset: () => void
  /** 유효성 여부 */
  isValid: boolean
}

// 3. 훅 구현 (named export)
export function useHookName(options: UseHookNameOptions = {}): UseHookNameReturn {
  const { initialValue = '', onError, onChange } = options

  const [value, setValueInternal] = useState(initialValue)

  // useCallback으로 메모이제이션
  const handleError = useCallback((message: string) => {
    onError ? onError(message) : toast.error(message)
  }, [onError])

  const setValue = useCallback((newValue: string) => {
    setValueInternal(newValue)
    onChange?.(newValue)
  }, [onChange])

  const reset = useCallback(() => {
    setValueInternal(initialValue)
  }, [initialValue])

  return {
    value,
    setValue,
    reset,
    isValid: value.length > 0,
  }
}

// 4. default export
export default useHookName
```

### 3. Update index.ts

```typescript
// src/hooks/index.ts에 추가
export { useHookName } from './useHookName'
export type { UseHookNameOptions, UseHookNameReturn } from './useHookName'
```

## Checklist

- [ ] 파일명이 `use` + PascalCase 형식인가?
- [ ] JSDoc 주석이 상단에 있는가?
- [ ] `Options`와 `Return` 인터페이스가 export 되었는가?
- [ ] 콜백 함수들이 `useCallback`으로 감싸져 있는가?
- [ ] 에러 처리가 `toast.error` 또는 `onError` 콜백을 사용하는가?
- [ ] `index.ts`에 export가 추가되었는가?

## Project Integration

```typescript
// form-constants.ts 사용 시
import { PROJECT_CONSTRAINTS, FORM_ERROR_MESSAGES } from '@/lib/form-constants'

// API 클라이언트 사용 시
import { ApiError } from '@/lib/api-client'
```

For advanced patterns (API hooks, form integration, compound hooks), see [reference.md](reference.md).
