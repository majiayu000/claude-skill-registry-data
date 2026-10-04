---
name: project-structure
description: This skill should be used when working with the JKKN COE Next.js project folder structure, including understanding where to place files, creating new modules, navigating the codebase, or following architectural patterns. Automatically triggers when user mentions 'project structure', 'folder structure', 'where should I put', 'create module', or asks about file organization.
---

# Project Structure Guide

This skill provides comprehensive guidance for navigating and working with the JKKN COE project folder structure.

## When to Use This Skill

Use this skill when:
- Understanding the overall project organization
- Determining where to place new files (components, services, pages, types, etc.)
- Creating new CRUD modules or features
- Following established architectural patterns
- Navigating the Next.js 15 App Router structure
- Understanding the 5-layer architecture (Types → Services → Hooks → Components → Pages)

## Project Architecture Overview

The JKKN COE application follows a **modular, layered architecture** using Next.js 15 App Router with TypeScript, Supabase backend, and Shadcn UI components.

### Core Architectural Principles

1. **App Router Structure**: Uses Next.js 15 App Router with route groups for organization
2. **5-Layer Architecture**: Types → Services → Hooks → Components → Pages
3. **Role-Based Access Control (RBAC)**: Permission-based routing and component rendering
4. **Server-Side First**: Default to Server Components, use Client Components only when needed
5. **Modular Design**: Each entity (courses, degrees, students, etc.) follows consistent patterns

## Project Folder Structure

### Root Level Organization

```
jkkncoe/
├── .claude/                    # Claude Code configuration and skills
│   └── skills/                 # Custom skills for development acceleration
├── .cursor/                    # Cursor IDE configuration
│   └── rules/                  # Development standards and conventions
├── app/                        # Next.js 15 App Router (main application code)
│   ├── coe/        # Route group for protected pages
│   ├── api/                    # API route handlers
│   ├── auth/                   # Authentication pages (login, callback)
│   └── layout.tsx              # Root layout
├── components/                 # Reusable UI components
│   ├── common/                 # Shared components across modules
│   ├── layout/                 # Layout components (header, sidebar, footer)
│   ├── ui/                     # Shadcn UI primitives
│   └── users/                  # User-specific components
├── context/                    # React Context providers
├── hooks/                      # Custom React hooks
├── lib/                        # Utilities, configurations, and helpers
│   ├── constants/              # Application constants
│   └── utils/                  # Utility functions
├── services/                   # Business logic and data access layer
├── store/                      # State management (Redux if needed)
├── styles/                     # Global styles and Tailwind CSS
├── supabase/                   # Supabase configuration
│   └── migrations/             # Database migration files
├── types/                      # TypeScript type definitions
└── public/                     # Static assets
```

### Detailed Directory Structure

For comprehensive folder structure details, file naming conventions, and usage examples, refer to:
- [references/folder-structure.md](references/folder-structure.md)

## Where to Place Files

### 1. Pages and Routes (`app/`)

**Structure:**
```
app/
├── coe/           # Protected routes
│   ├── courses/               # Entity module
│   │   └── page.tsx           # Main page component
│   ├── degrees/
│   ├── students/
│   └── layout.tsx             # Authenticated layout wrapper
├── api/                       # API routes
│   ├── courses/
│   │   ├── route.ts           # GET, POST endpoints
│   │   └── [id]/
│   │       └── route.ts       # PUT, DELETE endpoints
└── login/                     # Public routes
    └── page.tsx
```

**When to create new files:**
- **New entity page**: `app/coe/[entity-name]/page.tsx`
- **Nested route**: `app/coe/[entity]/[sub-route]/page.tsx`
- **API endpoint**: `app/api/[entity]/route.ts`
- **Dynamic API route**: `app/api/[entity]/[id]/route.ts`

**Naming Convention:**
- Use `kebab-case` for directory names
- Always `page.tsx` for route pages
- Always `route.ts` for API handlers
- Always `layout.tsx` for layout components

### 2. Components (`components/`)

**Structure:**
```
components/
├── common/                    # Shared across modules
│   ├── data-table.tsx         # Reusable table component
│   ├── file-upload.tsx        # Upload component
│   └── protected-route.tsx    # Auth guard
├── layout/                    # App-wide layout
│   ├── app-header.tsx
│   ├── app-sidebar.tsx
│   └── app-footer.tsx
├── ui/                        # Shadcn UI primitives
│   ├── button.tsx
│   ├── input.tsx
│   └── sheet.tsx
└── [entity]/                  # Entity-specific components
    ├── [entity]-form.tsx
    └── [entity]-table.tsx
```

**When to create new files:**
- **Reusable component**: `components/common/[component-name].tsx`
- **Entity-specific component**: `components/[entity]/[component-name].tsx`
- **UI primitive**: Import from Shadcn, don't create manually

**Component Guidelines:**
- Default to Server Components
- Add `"use client"` only when using:
  - Event handlers (onClick, onChange)
  - Browser APIs (localStorage, window)
  - State (useState, useReducer, useContext)
  - Effects (useEffect)
  - Client-only libraries

### 3. Services (`services/`)

**Structure:**
```
services/
├── courses-service.ts         # Course data access
├── degrees-service.ts         # Degree data access
├── students-service.ts        # Student data access
└── auth-service.ts            # Authentication service
```

**When to create new files:**
- **New entity service**: `services/[entity]-service.ts`
- **Shared utility service**: `services/[utility]-service.ts`

**Service Responsibilities:**
- Database queries using Supabase client
- Data transformation and validation
- Business logic execution
- Error handling and logging

### 4. Types (`types/`)

**Structure:**
```
types/
├── courses.ts                 # Course type definitions
├── degrees.ts                 # Degree type definitions
├── students.ts                # Student type definitions
├── auth.ts                    # Authentication types
└── index.ts                   # Re-export all types
```

**When to create new files:**
- **New entity types**: `types/[entity].ts`
- **Shared types**: `types/[domain].ts`

**Type Naming Convention:**
- Use PascalCase for type/interface names
- Prefix with entity name for clarity
- Example: `CourseFormData`, `DegreeCreatePayload`

### 5. Hooks (`hooks/`)

**Structure:**
```
hooks/
├── use-auth.ts                # Authentication hook
├── use-toast.ts               # Toast notification hook
├── use-courses.ts             # Course data fetching hook
└── use-form-validation.ts     # Form validation hook
```

**When to create new files:**
- **New custom hook**: `hooks/use-[functionality].ts`
- Always prefix with `use-` (React convention)

**Hook Responsibilities:**
- Encapsulate reusable stateful logic
- Handle data fetching with loading/error states
- Manage form state and validation
- Integrate with context providers

### 6. Utilities (`lib/`)

**Structure:**
```
lib/
├── supabase-server.ts         # Server-side Supabase client
├── utils.ts                   # General utilities
├── constants/
│   ├── routes.ts              # Route constants
│   └── permissions.ts         # Permission constants
└── utils/
    ├── format.ts              # Formatting utilities
    └── validation.ts          # Validation helpers
```

**When to create new files:**
- **New utility module**: `lib/utils/[utility-name].ts`
- **New constants**: `lib/constants/[constant-group].ts`

### 7. Context Providers (`context/`)

**Structure:**
```
context/
├── auth-context.tsx           # Authentication context
├── theme-context.tsx          # Theme provider
└── permissions-context.tsx    # Permissions context
```

**When to create new files:**
- **New context**: `context/[context-name]-context.tsx`
- Only create when state needs to be shared across multiple components

### 8. Database Migrations (`supabase/migrations/`)

**Structure:**
```
supabase/
└── migrations/
    ├── 20240101120000_create_users.sql
    ├── 20240102130000_create_courses.sql
    └── 20240103140000_add_rbac_tables.sql
```

**When to create new files:**
- **Schema changes**: Always create a new migration file
- **Naming**: `[timestamp]_[description].sql`
- Generate timestamp: `date +%Y%m%d%H%M%S`

## Creating New Modules (5-Layer Architecture)

When creating a new entity module (e.g., "courses", "students"), follow this order:

### Layer 1: Types (`types/[entity].ts`)
```typescript
export interface Course {
  id: string
  course_code: string
  course_title: string
  credits: number
  // ... other fields
}

export interface CourseFormData {
  course_code: string
  course_title: string
  credits: string
  // ... form fields
}
```

### Layer 2: Services (`services/[entity]-service.ts`)
```typescript
import { getSupabaseServer } from '@/lib/supabase-server'
import type { Course } from '@/types/courses'

export async function getCourses() {
  const supabase = getSupabaseServer()
  const { data, error } = await supabase
    .from('courses')
    .select('*')

  if (error) throw error
  return data as Course[]
}
```

### Layer 3: Hooks (`hooks/use-[entity].ts`)
```typescript
'use client'

import { useState, useEffect } from 'react'
import type { Course } from '@/types/courses'

export function useCourses() {
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch courses
  }, [])

  return { courses, loading }
}
```

### Layer 4: Components (`app/coe/[entity]/page.tsx`)
```typescript
'use client'

import { useState } from 'react'
import { Sheet, SheetContent } from '@/components/ui/sheet'
// ... other imports

export default function CoursesPage() {
  // Component implementation
}
```

### Layer 5: API Routes (`app/api/[entity]/route.ts`)
```typescript
import { NextRequest, NextResponse } from 'next/server'
import { getSupabaseServer } from '@/lib/supabase-server'

export async function GET() {
  // GET handler
}

export async function POST(req: NextRequest) {
  // POST handler
}
```

## Navigation and File Discovery

### Finding Files by Purpose

**Authentication:**
- Auth context: `context/auth-context.tsx`
- Login page: `app/login/page.tsx`
- Auth callback: `app/auth/callback/route.ts`
- Middleware: `middleware.ts` (root level)

**RBAC System:**
- Permission checks: `components/common/protected-route.tsx`
- Role management page: `app/coe/roles/page.tsx`
- User roles API: `app/api/user-roles/route.ts`

**Entity CRUD:**
- Page: `app/coe/[entity]/page.tsx`
- API: `app/api/[entity]/route.ts`
- Types: `types/[entity].ts`
- Service: `services/[entity]-service.ts`

**UI Components:**
- Shadcn primitives: `components/ui/`
- Layout components: `components/layout/`
- Shared components: `components/common/`

### Search Patterns

Use these patterns to quickly find files:

```bash
# Find all entity pages
**/coe/*/page.tsx

# Find all API routes
**/api/*/route.ts

# Find all type definitions
types/*.ts

# Find all services
services/*-service.ts

# Find specific component
components/**/*-[name].tsx
```

## Best Practices

1. **Consistent Naming**: Follow `kebab-case` for directories, `PascalCase` for components/types
2. **Colocation**: Keep related files close (e.g., entity-specific components with entity)
3. **Single Responsibility**: Each file should have one clear purpose
4. **Import Paths**: Use `@/` alias for absolute imports from root
5. **Server/Client Split**: Default to Server Components, add `"use client"` only when needed
6. **Type Safety**: Always define types in `types/` directory before implementing
7. **API Structure**: Use RESTful conventions (GET/POST in route.ts, PUT/DELETE in [id]/route.ts)

## Common Tasks

### Creating a New Entity CRUD Page

1. **Define types**: `types/[entity].ts`
2. **Create API routes**: `app/api/[entity]/route.ts` and `app/api/[entity]/[id]/route.ts`
3. **Create page**: `app/coe/[entity]/page.tsx`
4. **Add to sidebar**: Update `components/layout/app-sidebar.tsx`
5. **Test and verify**: Check RBAC, validation, error handling

### Adding a New Utility Function

1. **Create file**: `lib/utils/[utility-name].ts`
2. **Export from**: `lib/utils.ts` (if general purpose)
3. **Import using**: `@/lib/utils/[utility-name]`

### Adding a New Component

1. **Determine scope**: Common, layout, entity-specific, or UI primitive?
2. **Create file**: `components/[category]/[component-name].tsx`
3. **Use PascalCase**: For component function name
4. **Add `"use client"`**: Only if needed

## Additional Resources

For detailed folder structure visualization and comprehensive file listings, see:
- [references/folder-structure.md](references/folder-structure.md) - Complete directory tree and file descriptions
