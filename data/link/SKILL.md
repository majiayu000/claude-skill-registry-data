---
name: link
description: |
  Full-stack monorepo expert for wellness-link project. Handles features spanning
  packages/web (React 19 + Tailwind v4) and packages/api (Bun + Elysia). Use for
  full-stack features, cross-package types, monorepo workflows, workspace commands.
  Keywords: fullstack, monorepo, wellness-link, cross-package, workspace, bun.
---

# Wellness Link - Full-Stack Monorepo Expert

Expert for the wellness-link monorepo. Combines frontend (React 19 + Tailwind v4 + shadcn/ui) and backend (Bun + Elysia + Drizzle) development with monorepo-specific workflows.

## Available Documentation

### Patterns
- **[Full-Stack Workflow](patterns/fullstack-workflow.md)** - Complete guide for implementing features across packages
- **[Monorepo Commands](patterns/monorepo-commands.md)** - Bun workspace commands, development, and troubleshooting

### Agent References
- **[Web Agent](reference/web-agent.md)** - Quick reference to `.claude/agent/web.md`
- **[API Agent](reference/api-agent.md)** - Quick reference to `.claude/agent/api.md`

## Monorepo Structure

```
wellness-link/
├── packages/
│   ├── web/          # React 19 + Vite (port 5176)
│   └── api/          # Bun + Elysia (port 5300)
├── bunfig.toml       # Bun workspaces
└── package.json      # Root workspace
```

## Critical Cross-Package Rules

### 1. Type Sharing
```typescript
// API defines types, web imports via edenTreaty
// packages/api/src/index.ts
export const app = new Elysia()...

// packages/web/src/lib/api.ts
import type { App } from "@wellness-link/api"
export const api = edenTreaty<App>("http://localhost:5300")
```

### 2. Language & Theme
- **User-facing text**: Spanish (buttons, forms, messages)
- **Technical docs**: English (code, comments, README)
- **Theme**: Always use CSS variables (`bg-background`, `text-foreground`)

### 3. Workspace Commands
```bash
# Run from root
bun --filter @wellness-link/web dev    # Frontend only
bun --filter @wellness-link/api dev    # Backend only

# Development (both in parallel)
bun run dev                             # Runs both packages
```

## Web Package (packages/web)

### Stack
- React 19 + React Router 7 (file-based)
- Tailwind CSS v4 + shadcn/ui
- TanStack Query (server state)
- React Hook Form + Zod (forms)

### Critical Rules
```typescript
// ALWAYS use @/ alias
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

// ALWAYS use cn() for classes
<div className={cn("flex", className, isActive && "bg-primary")} />

// ALWAYS Spanish UI text
<Button>Guardar Cambios</Button>
toast.success("Perfil actualizado")
```

### Data Fetching
```typescript
const { data, isLoading } = useQuery({
  queryKey: ["profiles"],
  queryFn: async () => {
    const { data, error } = await api.api.profiles.get()
    if (error) throw error
    return data
  },
})
```

## API Package (packages/api)

### Stack
- Bun (runtime)
- Elysia (framework)
- Drizzle ORM (PostgreSQL)
- Better Auth (authentication)

### Critical Rules
```typescript
// Table names are SINGULAR
import { profile, asset, socialLink } from "../../db/schema"

// ALWAYS register services in plugins/services.ts
export const servicesPlugin = new Elysia({ name: "services" }).derive(
  { as: "global" },
  async () => {
    const featureRepo = new FeatureRepository();
    const featureService = new FeatureService(featureRepo);
    return { services: { featureRepo, featureService } };
  },
);

// Access relations via name
const platform = click.socialLink.platform; // ✅
const platform = click.platform;            // ❌
```

### Route Pattern
```typescript
export const featureRoutes = new Elysia({ prefix: "/feature" })
  .use(errorMiddleware)
  .use(servicesPlugin)
  .use(authGuard)
  .get("/", ({ ctx, services }) => services.featureService.getAll(ctx!))
  .post("/", ({ body, ctx, services, set }) => {
    set.status = 201;
    return services.featureService.create(ctx!, body);
  }, { body: t.Object({ name: t.String() }) });
```

## Full-Stack Feature Workflow

### 1. Define API Contract
```typescript
// packages/api/src/api/routes/feature.ts
export const featureRoutes = new Elysia({ prefix: "/feature" })
  .get("/", () => [...])
  .post("/", ({ body }) => body, {
    body: t.Object({
      name: t.String(),
      description: t.String(),
    })
  });
```

### 2. Add Route to App
```typescript
// packages/api/src/index.ts
import { featureRoutes } from "./api/routes/feature"

export const app = new Elysia()
  .use(featureRoutes)
  ...
```

### 3. Frontend Integration
```typescript
// packages/web/src/hooks/use-features.ts
export function useFeatures() {
  return useQuery({
    queryKey: ["features"],
    queryFn: async () => {
      const { data, error } = await api.api.feature.get()
      if (error) throw error
      return data
    },
  })
}

// packages/web/src/components/FeatureForm.tsx
const mutation = useMutation({
  mutationFn: async (values: { name: string; description: string }) => {
    const { data, error } = await api.api.feature.post(values)
    if (error) throw error
    return data
  },
})
```

## Common Patterns

### Authentication Flow
```typescript
// API: Better Auth automatic
// packages/api/src/lib/auth.ts
export const auth = betterAuth({ ... })

// Web: Use auth client
// packages/web/src/hooks/use-auth.ts
const { data: session } = useSession()
```

### File Upload (Full-Stack)
```typescript
// API: Asset service
const asset = await services.assetService.create(ctx, {
  file: request.file,
  type: "avatar",
})

// Web: Form with file input
const { mutate } = useMutation({
  mutationFn: async (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    const { data } = await api.api.assets.post(formData)
    return data
  },
})
```

### Error Handling
```typescript
// API: HTTP exceptions
throw new NotFoundException("Profile not found")     // 404
throw new ConflictException("Username exists")       // 409

// Web: React Query + toast
onError: (error) => {
  toast.error(error.message || "Error al guardar")
}
```

## Monorepo Best Practices

### 1. Development Setup
```bash
# Install all dependencies
bun install

# Start both packages
bun run dev

# Type check entire monorepo
bun run typecheck
```

### 2. Database Migrations
```bash
# Generate migration
cd packages/api && bun run db:generate

# Apply migration
bun run db:migrate

# Seed data
bun run db:seed
```

### 3. Cross-Package Changes
**Order**: API first, then Web
1. Add DB schema/migration
2. Create repository + service
3. Add API route
4. Create frontend hook
5. Build UI component

### 4. Type Safety
```typescript
// API exports App type
export type App = typeof app

// Web imports and uses it
import type { App } from "@wellness-link/api"
export const api = edenTreaty<App>("http://localhost:5300")
```

## Key Tables

- **user**: Better Auth authentication
- **profile**: Wellness professional info
- **socialLink**: Orderable social media links
- **healthSurvey**: Visitor survey responses
- **analytics**: Views and clicks tracking
- **asset**: File uploads (avatars, images)

## Quick Commands

```bash
# Web development
cd packages/web
bun run dev          # Port 5176
bun run build
bun run lint

# API development
cd packages/api
bun run dev          # Port 5300
bun run db:seed
bun run db:reset
bun run lint

# Monorepo (from root)
bun run dev          # Both packages
bun install          # All dependencies
```

## When to Use This Skill

- Implementing features that span both web and api
- Setting up new API endpoints with frontend integration
- Working with shared types across packages
- Monorepo workflow questions
- Cross-package refactoring
- Full-stack feature development
