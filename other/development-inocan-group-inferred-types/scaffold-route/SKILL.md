---
name: scaffold-route
description: Scaffold a new Next.js route with tRPC router, Zod validation, and proper file structure
---

# Scaffold Route

Create a complete vertical slice for a new feature: page, API, and validation.

## What gets created

```
app/[feature]/
├── page.tsx           # Server component
├── loading.tsx        # Skeleton loader
├── error.tsx          # Error boundary
└── components/
    └── index.ts       # Barrel export

server/api/routers/[feature]/
└── index.ts           # tRPC router with CRUD procedures

validations/
└── [feature].ts       # Zod schemas + inferred types
```

## What gets updated

- `server/api/root.ts` - import and add router to appRouter
- `validations/index.ts` - add barrel export

## Instructions

1. Ask for the feature name (singular, lowercase, e.g., "project", "booking", "invoice")
2. Ask which CRUD operations are needed: list, get, create, update, delete
3. Generate files following the patterns below
4. Update barrel exports and root router

## Patterns

### page.tsx (Server Component)

```tsx
import { Suspense } from 'react'
import { FeatureList } from './components'
import { FeatureSkeleton } from '@/components/skeletons'

export default function FeaturePage() {
  return (
    <main className="container py-8">
      <h1 className="text-2xl font-bold mb-6">Features</h1>
      <Suspense fallback={<FeatureSkeleton />}>
        <FeatureList />
      </Suspense>
    </main>
  )
}
```

### loading.tsx

```tsx
import { FeatureSkeleton } from '@/components/skeletons'

export default function Loading() {
  return <FeatureSkeleton />
}
```

### error.tsx

```tsx
'use client'

interface Props {
  error: Error & { digest?: string }
  reset: () => void
}

export default function Error({ error, reset }: Props) {
  return (
    <main className="container py-8">
      <h1 className="text-2xl font-bold mb-4">Something went wrong</h1>
      <p className="text-muted-foreground mb-4">{error.message}</p>
      <button onClick={reset} className="text-primary underline">
        Try again
      </button>
    </main>
  )
}
```

### validations/[feature].ts

```tsx
import { z } from 'zod'

export const createFeatureSchema = z.object({
  name: z.string().min(1, 'Name is required'),
})

export const updateFeatureSchema = createFeatureSchema.partial()

export type CreateFeatureInput = z.infer<typeof createFeatureSchema>
export type UpdateFeatureInput = z.infer<typeof updateFeatureSchema>
```

### server/api/routers/[feature]/index.ts

```tsx
import { z } from 'zod'
import { router, publicProcedure } from '@/server/api/trpc'
import { createFeatureSchema, updateFeatureSchema } from '@/validations'
import { prisma } from '@/prisma/prisma'

export const featureRouter = router({
  list: publicProcedure.query(async () => {
    return prisma.feature.findMany({
      select: { id: true, name: true, createdAt: true },
      orderBy: { createdAt: 'desc' },
    })
  }),

  get: publicProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ input }) => {
      return prisma.feature.findUniqueOrThrow({
        where: { id: input.id },
        select: { id: true, name: true, createdAt: true },
      })
    }),

  create: publicProcedure
    .input(createFeatureSchema)
    .mutation(async ({ input }) => {
      return prisma.feature.create({
        data: input,
        select: { id: true },
      })
    }),

  update: publicProcedure
    .input(z.object({ id: z.string(), data: updateFeatureSchema }))
    .mutation(async ({ input }) => {
      return prisma.feature.update({
        where: { id: input.id },
        data: input.data,
        select: { id: true },
      })
    }),

  delete: publicProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ input }) => {
      return prisma.feature.delete({
        where: { id: input.id },
        select: { id: true },
      })
    }),
})
```

### Updating root.ts

```tsx
import { featureRouter } from './routers/feature'

export const appRouter = router({
  // existing routers...
  feature: featureRouter,
})
```

---

> **Note:** Prisma model scaffolding is currently under review. For now, create models manually in `prisma/schema.prisma` and run migrations before using this skill.

## Checklist

- [ ] Feature name is singular and lowercase
- [ ] All files use `@/` imports
- [ ] Barrel exports updated
- [ ] Root router updated
- [ ] Skeleton component exists or created
- [ ] No `any` types
- [ ] No semicolons
