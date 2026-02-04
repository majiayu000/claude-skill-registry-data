---
name: codebase-structure
description: Provides a high-level overview of the Next.js application's file structure and directory organization. Use when deciding where to place new files, components, server actions, database schemas, or when understanding the overall architecture of the codebase. Essential for maintaining consistent file organization and knowing where different types of code belong.
---

# Codebase Structure

## Overview

Understand the file structure and directory organization to maintain consistency when adding new features, components, or functionality.

## Directory Structure

```txt
create-reodor-app/
├── app/                    # Next.js App Router - Pages and routes
├── components/             # React components
├── docs/                   # Project documentation
├── hooks/                  # Custom React hooks
├── lib/                    # External service configurations and utilities
├── providers/              # React context providers
├── public/                 # Static assets (images, logos, manifests)
├── schemas/                # Generated Zod schemas (auto-generated)
├── scripts/                # Utility scripts (deployment, setup)
├── seed/                   # Database seeding configuration
├── server/                 # Server actions for data mutations
├── stores/                 # Zustand state management stores
├── supabase/               # Supabase configuration and database
├── transactional/          # React Email templates
├── types/                  # TypeScript type definitions
└── middleware.ts           # Next.js middleware (auth, route protection)
```

## Where to Place New Code

### Pages & Routes (`app/`)

**Structure**: Next.js App Router with file-based routing

**Place here**:

- Page components (`page.tsx`)
- Layouts (`layout.tsx`)
- Error boundaries (`error.tsx`, `global-error.tsx`)
- Not found pages (`not-found.tsx`)
- API routes (`api/*/route.ts`)
- Route-specific loading states (`loading.tsx`)
- SEO metadata (`robots.ts`, `sitemap.ts`, `opengraph-image.png`)
- Favicons and app icons

**Examples**:

- `app/oppgaver/page.tsx` - Todos feature page
- `app/auth/sign-in/page.tsx` - Sign in page
- `app/api/cron/*/route.ts` - Cron job endpoints
- `app/layout.tsx` - Root layout with providers

### Components (`components/`)

**Structure**: Feature-based organization + shared components

**Place here**:

- **Feature directories** (`components/[feature]/`) - Feature-specific components
  - Example: `components/todos/`, `components/auth/`, `components/admin/`
- **Shared components** - Components used across features
  - Example: `navbar.tsx`, `footer.tsx`, `error-boundary.tsx`
- **UI library** (`components/ui/`) - shadcn/ui components
- **Specialized UI** (`components/kibo-ui/`) - Kibo UI components
- **Magic UI** (`components/magicui/`) - Magic UI components

**Naming**: Use kebab-case for directories, PascalCase for component files

**Examples**:

- `components/todos/todo-form.tsx` - Todo form component
- `components/todos/todo-dialog.tsx` - Todo dialog wrapper
- `components/auth/auth-form.tsx` - Authentication form
- `components/ui/button.tsx` - shadcn/ui button component

### Server Actions (`server/`)

**Purpose**: Type-safe server-side data operations with authentication

**Place here**:

- Database CRUD operations
- Authenticated data mutations
- Server-side business logic

**Naming**: `[feature].actions.ts`

**Examples**:

- `server/todo.actions.ts` - Todo CRUD operations
- `server/profile.actions.ts` - Profile management
- `server/admin.actions.ts` - Admin operations

**Pattern**: Individual exported async functions, not default exports

### Custom Hooks (`hooks/`)

**Purpose**: Reusable React hooks for client-side logic

**Place here**:

- Data fetching hooks (TanStack Query)
- File upload hooks
- Authentication hooks
- Form state management hooks
- UI state hooks (media queries, scroll position, etc.)

**Naming**: `use-[hook-name].ts`

**Examples**:

- `hooks/use-auth.ts` - Authentication state
- `hooks/use-upload-todo-attachments.ts` - File upload logic
- `hooks/use-media-query.ts` - Responsive breakpoint detection

### State Management (`stores/`)

**Purpose**: Global state with Zustand

**Place here**:

- Application-wide state
- Persisted state (localStorage, sessionStorage)
- Shared UI state

**Naming**: `[feature]-store.ts` or `use-[feature]-store.ts`

**Examples**:

- `stores/setup-steps-store.ts` - Setup wizard state

### Database (`supabase/`)

**Structure**:

```
supabase/
├── schemas/        # Declarative SQL schemas (source of truth)
├── migrations/     # Generated SQL migrations (auto-generated)
└── functions/      # Edge functions (Deno runtime)
```

**Place here**:

- **schemas/** - Declarative database schemas, RLS policies, triggers
  - `01-schema.sql` - Tables, enums, indexes
  - `02-policies.sql` - Row Level Security policies
  - `03-triggers.sql` - Database triggers
- **migrations/** - Generated from schemas (DO NOT edit manually)
- **functions/** - Supabase Edge Functions for serverless operations

**Workflow**:

1. Edit schema in `schemas/`
2. Run `bun db:diff <name>` to generate migration
3. Review generated migration in `migrations/`
4. Run `bun migrate:up` to apply

### Type Definitions (`types/`)

**Purpose**: TypeScript types and interfaces

**Place here**:

- **database.types.ts** - Generated from Supabase (auto-generated, DO NOT edit)
- **index.ts** - Custom types, shared filter types, runtime-agnostic types
- Feature-specific type definitions

**Examples**:

- `types/database.types.ts` - Auto-generated Supabase types
- `types/index.ts` - Custom types like `BookingFilters`, `ServiceFilters`

### Schemas (`schemas/`)

**Purpose**: Auto-generated Zod validation schemas

**Content**:

- `database.schema.ts` - Generated from Supabase types (DO NOT edit manually)

**Usage**: Import schemas for validation in server actions and forms

**Generation**: Run `bun gen:types` to regenerate

### External Services (`lib/`)

**Purpose**: Service configurations and utilities

**Place here**:

- **Service clients** (`resend.ts`, `lib/supabase/client.ts`)
- **Service utilities** (`resend-utils.ts`, `lib/supabase/storage.ts`)
- **Configuration** (`brand.ts`, `navigation.ts`, `permissions.ts`)
- **Helper functions** (`utils.ts` - cn(), formatting, etc.)

**Structure**:

```
lib/
├── supabase/           # Supabase configuration
│   ├── client.ts       # Browser client
│   ├── server.ts       # Server client
│   └── storage.ts      # Storage utilities
├── brand.ts            # Brand configuration
├── navigation.ts       # Navigation structure
├── utils.ts            # Shared utilities
└── [service].ts        # External service configs
```

### React Providers (`providers/`)

**Purpose**: React Context providers for app-wide state

**Place here**:

- TanStack Query provider
- Theme providers
- Authentication providers
- Any context providers

**Examples**:

- `providers/tanstack-query-provider.tsx`

### Email Templates (`transactional/emails`)

**Purpose**: React Email templates for transactional emails

**Place here**:

- Email components built with React Email
- Email-specific utilities

**Examples**:

- `transactional/emails/welcome.tsx`
- `transactional/emails/password-reset.tsx`

### Documentation (`docs/`)

**Structure**:

```
docs/
├── business/       # Business features and workflows
└── technical/      # Technical implementation details
```

**Place here**:

- **business/** - Feature docs, user workflows, business logic
- **technical/** - Architecture, API docs, deployment guides

**Examples**:

- `docs/technical/google-auth-setup.md`
- `docs/technical/railway-deployment.md`

### Static Assets (`public/`)

**Purpose**: Static files served at root path

**Place here**:

- Logos and brand assets
- Web app manifest images
- Static images referenced by absolute paths
- Files that need specific public URLs

**Structure**:

```
public/
├── logos/                          # Logo variations
├── web-app-manifest-192x192.png   # PWA icons
└── web-app-manifest-512x512.png
```

**Note**: Favicons and app icons go in `app/` directory, not `public/`

### Utility Scripts (`scripts/`)

**Purpose**: Development and deployment automation

**Place here**:

- Deployment scripts
- Setup scripts
- Database utilities
- Build automation

**Examples**:

- `scripts/railway-setup.sh`
- `scripts/ensure-transactional-deps-installed.sh`

### Database Seeding (`seed/`)

**Purpose**: Snaplet configuration for database seeding

**Place here**:

- Snaplet configuration
- Seed data scripts

## Root-Level Files

- **middleware.ts** - Next.js middleware for auth and route protection
- **next.config.ts** - Next.js configuration
- **tailwind.config.ts** - Tailwind CSS configuration
- **seed.config.ts** - Database seeding configuration
- **next-env.d.ts** - Next.js TypeScript declarations (auto-generated)

## Key Principles

1. **Feature-based organization** - Group related files by feature (e.g., `components/todos/`, `server/todo.actions.ts`)
2. **Separation of concerns** - Keep server logic (`server/`) separate from client components (`components/`)
3. **Generated files** - Never edit auto-generated files (`types/database.types.ts`, `schemas/database.schema.ts`, `migrations/`)
4. **Naming conventions** - Use kebab-case for files, PascalCase for components, camelCase for functions

## Common Workflows

### Adding a New Feature

1. **Database**: Update `supabase/schemas/01-schema.sql` with new database schema state. Refer to `skills/database-schema-extension/SKILL.md` for guidance.
2. **Server Actions**: Create `server/[feature].actions.ts`
3. **Components**: Create `components/[feature]/` directory
4. **Hooks**: Add custom hooks to `hooks/use-[feature].ts` if needed.
5. **Page**: Create `app/[path-to-feature]/page.tsx`. It can be nested as needed.
6. **Types**: Custom types go in `types/index.ts`

### Adding a New UI Component

1. **Shared component**: `components/[name].tsx`
2. **Feature component**: `components/[feature]/[name].tsx`
3. **shadcn/ui**: Run `bunx --bun shadcn@latest add [component]` (auto-adds to `components/ui/`)

### Adding Authentication

1. **Server action**: Add to `server/auth.actions.ts`
2. **Middleware**: Update route protection in `middleware.ts`
3. **Components**: Add to `components/auth/`
4. **Hooks**: Update `hooks/use-auth.ts`

## Quick Reference

| Type            | Location                                   | Example                           |
| --------------- | ------------------------------------------ | --------------------------------- |
| Page            | `app/[route]/page.tsx`                     | `app/oppgaver/page.tsx`           |
| Server Action   | `server/[feature].actions.ts`              | `server/todo.actions.ts`          |
| Component       | `components/[feature]/[name].tsx`          | `components/todos/todo-form.tsx`  |
| Hook            | `hooks/use-[name].ts`                      | `hooks/use-auth.ts`               |
| Store           | `stores/[name]-store.ts`                   | `stores/setup-steps-store.ts`     |
| Database Schema | `supabase/schemas/01-schema.sql`           | Table definitions                 |
| Email Template  | `transactional/[name]-email.tsx`           | `transactional/welcome-email.tsx` |
| Util Function   | `lib/utils.ts` or `lib/[service]-utils.ts` | `lib/resend-utils.ts`             |
| Type            | `types/index.ts`                           | Custom types                      |
| API Route       | `app/api/[route]/route.ts`                 | `app/api/cron/demo/route.ts`      |
