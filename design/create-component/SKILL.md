---
name: create-component
description: Creates React components for SideDish. Use when adding new UI components, modals, forms, or interactive elements. Includes TypeScript interfaces, styling patterns, and security considerations.
---

# Create Component Skill

## Instructions

1. Create in `src/components/ComponentName.tsx`
2. Add `'use client'` for interactive components
3. Define props interface above component
4. Use `React.FC<Props>` pattern
5. Export as default

## Component Template

```tsx
'use client'

import { useState } from 'react'

interface ComponentNameProps {
  title: string
  onClick?: () => void
  children?: React.ReactNode
}

const ComponentName: React.FC<ComponentNameProps> = ({ title, onClick, children }) => {
  const [isLoading, setIsLoading] = useState(false)

  return (
    <div className="bg-white rounded-xl p-6 shadow-lg">
      <h2 className="text-lg font-bold text-slate-900">{title}</h2>
      {children}
    </div>
  )
}

export default ComponentName
```

## Korean Text
- Buttons: 등록하기, 저장하기, 취소, 삭제
- Labels: 제목, 설명, 태그
- Errors: 오류가 발생했습니다

## Security
```tsx
import SafeMarkdown from '@/components/SafeMarkdown'
<SafeMarkdown>{userContent}</SafeMarkdown>
```

For form components, modal template, and complete patterns, see [reference.md](reference.md).
