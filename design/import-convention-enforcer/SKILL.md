---
name: nextjs-import-enforcer
description: Automatically enforce consistent import patterns using Next.js path aliases and proper organization. Use when writing imports, creating new files, or organizing code structure.
---

# Import Convention Enforcer (Next.js/React)

Auto-enforces consistent import patterns using Next.js path aliases for clean, maintainable code.

## Activation Triggers

This skill activates when:
- Writing or modifying TypeScript/JavaScript files
- Creating new components, hooks, utilities
- Importing from other files
- Organizing project structure
- Mentioning "import", "add", "create"

## Required Import Pattern (MANDATORY)

Use path aliases for internal imports:

```tsx
// ✅ CORRECT - Path aliases
import { Button } from '@/components/ui'
import { useAuth } from '@/hooks'
import { formatDate } from '@/lib/utils'
import { User } from '@/types'

// ❌ WRONG - Relative paths
import { Button } from '../../components/ui/Button'
import { useAuth } from '../../../hooks/useAuth'
```

## Path Alias Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"],
      "@/app/*": ["./src/app/*"]
    }
  }
}
```

## Auto-Fix Process

### Step 1: Detect Relative Imports

```tsx
// ❌ User writes
import { Button } from '../../../components/ui/Button'
import { Card } from '../../components/ui/Card'
import { useUser } from '../hooks/useUser'
```

### Step 2: Convert to Path Aliases

```tsx
// ✅ Auto-fixed to
import { Button } from '@/components/ui'
import { Card } from '@/components/ui'
import { useUser } from '@/hooks'
```

### Step 3: Organize Imports

```tsx
// ✅ Final organized imports
// 1. React/Next.js
import { useState } from 'react'
import Link from 'next/link'

// 2. Third-party libraries
import { z } from 'zod'
import { useForm } from 'react-hook-form'

// 3. Internal - path aliases
import { Button, Card } from '@/components/ui'
import { useUser } from '@/hooks'
import { formatDate } from '@/lib/utils'
import type { User } from '@/types'
```

## Import Organization Rules

### 1. Import Order (Top to Bottom)

```tsx
// 1. React/Next.js core
import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'

// 2. Third-party libraries
import { z } from 'zod'
import clsx from 'clsx'

// 3. Internal modules (using @/ aliases)
import { Button } from '@/components/ui'
import { useAuth } from '@/hooks'
import { api } from '@/lib/api'

// 4. Types (separate or with type keyword)
import type { User, Post } from '@/types'

// 5. Styles (if needed)
import styles from './Component.module.css'
```

### 2. Named Imports (Alphabetical)

```tsx
// ✅ CORRECT - Alphabetical
import { Button, Card, Dialog, Input } from '@/components/ui'

// ❌ WRONG - Random order
import { Dialog, Input, Button, Card } from '@/components/ui'
```

### 3. Type-Only Imports

```tsx
// ✅ CORRECT - Explicit type imports
import type { User } from '@/types'
import type { ButtonProps } from '@/components/ui'

// ✅ CORRECT - Inline type keyword
import { type User, type Post } from '@/types'
```

## Path Alias Patterns by Directory

### Components

```tsx
// UI components
import { Button, Card, Input } from '@/components/ui'

// Feature components
import { UserProfile } from '@/components/features'

// Layout components
import { Header, Footer } from '@/components/layout'
```

### Hooks

```tsx
// Custom hooks
import { useAuth, useUser, useLocalStorage } from '@/hooks'

// Or specific hook files
import { useAuth } from '@/hooks/useAuth'
```

### Utilities/Lib

```tsx
// Utilities
import { cn, formatDate, truncate } from '@/lib/utils'

// API client
import { api } from '@/lib/api'

// Constants
import { ROUTES, API_URL } from '@/lib/constants'
```

### Types

```tsx
// All types from types directory
import type { User, Post, Comment } from '@/types'

// Or specific type files
import type { ApiResponse } from '@/types/api'
```

### App Router (Next.js 13+)

```tsx
// Route components/utilities
import { generateMetadata } from '@/app/utils'
import { PageProps } from '@/app/types'
```

## Barrel Exports (index.ts)

Encourage barrel exports for cleaner imports:

```tsx
// components/ui/index.ts
export { Button } from './Button'
export { Card } from './Card'
export { Input } from './Input'
export { Dialog } from './Dialog'

// Usage - clean!
import { Button, Card, Input } from '@/components/ui'
```

## Dynamic Imports

```tsx
// ✅ CORRECT - Dynamic import with path alias
const Chart = dynamic(() => import('@/components/Chart'), {
  loading: () => <Skeleton />,
  ssr: false,
})

// ❌ WRONG - Relative path
const Chart = dynamic(() => import('../../components/Chart'))
```

## Server/Client Component Imports

```tsx
// Server Component
import { db } from '@/lib/database'  // Server-only
import { ServerComponent } from '@/components/server'

// Client Component
'use client'
import { useState } from 'react'
import { Button } from '@/components/ui'  // Client component
```

## CSS/Style Imports

```tsx
// ✅ CORRECT - At the end
import { Button } from '@/components/ui'
import styles from './Component.module.css'

// ✅ CORRECT - Global styles in _app or layout
import '@/styles/globals.css'
```

## Image Imports

```tsx
// ✅ CORRECT - Next.js Image with path alias
import Image from 'next/image'
import logo from '@/public/logo.png'

// ✅ CORRECT - Public path
<Image src="/logo.png" alt="Logo" width={200} height={50} />
```

## Common Violations

### Violation 1: Deep Relative Paths

```tsx
// ❌ WRONG
import { Button } from '../../../components/ui/Button'

// ✅ CORRECT
import { Button } from '@/components/ui'
```

### Violation 2: Missing Barrel Export

```tsx
// ❌ WRONG - Importing from specific files
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

// ✅ CORRECT - Import from barrel
import { Button, Card } from '@/components/ui'
```

### Violation 3: Mixing Import Styles

```tsx
// ❌ WRONG - Inconsistent
import { Button } from '@/components/ui'
import { useAuth } from '../../hooks/useAuth'  // Relative!

// ✅ CORRECT - All use aliases
import { Button } from '@/components/ui'
import { useAuth } from '@/hooks'
```

### Violation 4: Type Import Without Keyword

```tsx
// ❌ WRONG - Importing type as value
import { User } from '@/types'  // Adds to bundle

// ✅ CORRECT - Explicit type import
import type { User } from '@/types'  // No runtime cost
```

## Project Structure Best Practices

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/
│   ├── (dashboard)/
│   └── api/
├── components/
│   ├── ui/                # Shadcn components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── index.ts       # Barrel export
│   ├── features/          # Feature components
│   └── layout/            # Layout components
├── hooks/
│   ├── useAuth.ts
│   ├── useUser.ts
│   └── index.ts           # Barrel export
├── lib/
│   ├── api.ts
│   ├── utils.ts
│   └── constants.ts
├── types/
│   ├── api.ts
│   ├── models.ts
│   └── index.ts           # Barrel export
└── styles/
    └── globals.css
```

## ESLint Integration

Suggest ESLint rules:

```json
{
  "rules": {
    "import/order": [
      "error",
      {
        "groups": [
          "builtin",
          "external",
          "internal",
          "parent",
          "sibling",
          "index"
        ],
        "pathGroups": [
          {
            "pattern": "@/**",
            "group": "internal",
            "position": "after"
          }
        ],
        "alphabetize": {
          "order": "asc"
        }
      }
    ],
    "import/no-relative-packages": "error"
  }
}
```

## Success Criteria

✅ ALL internal imports use path aliases
✅ NO deep relative paths (../..)
✅ Barrel exports for component directories
✅ Imports organized by category
✅ Type imports use `type` keyword
✅ Consistent import style across project

## Behavior

**Proactive enforcement:**
- Detect relative imports automatically
- Convert to path aliases immediately
- Organize import order
- Suggest barrel exports
- Explain import patterns

**Never:**
- Require explicit "fix imports" request
- Allow deep relative paths
- Wait for linter errors

**Always:**
- Use `@/` path aliases
- Organize imports by category
- Add barrel exports where beneficial
- Add type keyword for type imports

This ensures clean, maintainable import structure from day one.
