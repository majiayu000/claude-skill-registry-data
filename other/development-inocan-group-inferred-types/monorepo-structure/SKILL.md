---
name: monorepo-structure
description: Use when determining where to place files, understanding project organization, or working across multiple packages. Provides comprehensive knowledge of the Hounii monorepo structure and workspace configuration.
---

# Monorepo Structure Skill

Use this skill when you need to understand where files should go, how packages are organized, or how the monorepo workspace is configured.

## Overview

Hounii is a **pnpm + Turborepo monorepo** with three apps and multiple shared packages.

```
hounii-monorepo/
├── apps/                    # Application layer
│   ├── mobile/             # React Native + Expo (SDK 53)
│   ├── web/                # Next.js 15 (App Router)
│   └── admin/              # Next.js 15 (Admin portal)
├── packages/               # Shared packages
│   ├── ui/                 # Tamagui design system
│   ├── lib/                # Shared utilities & business logic
│   ├── i18n/               # Internationalization
│   ├── api/                # Supabase client & types
│   └── config/             # Shared configurations
├── supabase/               # Database & backend
│   ├── migrations/         # SQL migrations
│   └── functions/          # Edge functions
└── [root configs]          # Turborepo, pnpm, ESLint, TypeScript
```

## Where Things Go

### 🎯 Quick Reference

| What | Where | Why |
|------|-------|-----|
| Mobile screens/features | `apps/mobile/features/` | Feature-driven structure |
| Web pages | `apps/web/app/` | Next.js App Router |
| Admin pages | `apps/admin/app/` | Next.js App Router |
| UI components (atoms) | `packages/ui/src/` | Shared Tamagui primitives |
| Business logic | `packages/lib/src/` | Reusable across apps |
| Translations | `packages/i18n/translations/` | Multi-language support |
| Database schema | `supabase/migrations/` | Version-controlled migrations |
| API types | `packages/api/src/types/` | Generated from Supabase |
| Config files | `packages/config/` | Shared ESLint, TS configs |

## Apps Directory (apps/)

### Mobile App (apps/mobile/)

**Tech**: React Native + Expo SDK 53 + Expo Router

```
apps/mobile/
├── app/                    # Expo Router routes
│   ├── (auth)/            # Auth-protected routes
│   ├── (tabs)/            # Tab navigation
│   └── _layout.tsx        # Root layout
├── features/              # Feature-driven modules
│   ├── auth/
│   │   ├── screens/       # Auth screens
│   │   ├── components/    # Auth-specific components
│   │   ├── hooks/         # Auth hooks
│   │   └── index.ts       # Public exports
│   ├── profile/
│   ├── pets/
│   └── map/
├── components/            # Shared mobile components
├── hooks/                 # Shared hooks
├── utils/                 # Mobile-specific utilities
├── assets/                # Images, fonts, etc.
└── package.json           # Mobile dependencies
```

**When to use:**
- React Native screens and navigation
- Mobile-specific features (camera, location, notifications)
- Native module integrations
- Platform-specific code (iOS/Android)

**Dependencies:**
```json
{
  "dependencies": {
    "@hounii/ui": "workspace:*",
    "@hounii/lib": "workspace:*",
    "@hounii/i18n": "workspace:*",
    "@hounii/api": "workspace:*"
  }
}
```

### Web App (apps/web/)

**Tech**: Next.js 15 + App Router + Server Components

```
apps/web/
├── app/                   # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── (auth)/           # Auth routes
│   ├── profile/          # Profile pages
│   └── api/              # API routes
├── components/           # Web-specific components
├── lib/                  # Web utilities
├── public/               # Static assets
└── package.json          # Web dependencies
```

**When to use:**
- Public-facing web pages
- SEO-optimized content
- Server-side rendering
- Web-specific features (PWA, web push)

### Admin App (apps/admin/)

**Tech**: Next.js 15 + App Router

```
apps/admin/
├── app/
│   ├── dashboard/        # Admin dashboard
│   ├── users/            # User management
│   ├── pets/             # Pet moderation
│   └── analytics/        # Analytics views
├── components/           # Admin-specific components
└── package.json          # Admin dependencies
```

**When to use:**
- Internal admin tools
- Moderation interfaces
- Analytics dashboards
- User management

## Packages Directory (packages/)

### UI Package (packages/ui/)

**Purpose**: Tamagui design system - atoms and primitives ONLY

```
packages/ui/
├── src/
│   ├── components/       # Tamagui primitives
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── index.ts
│   ├── theme/           # Design tokens
│   │   ├── tokens.ts    # Colors, spacing, typography
│   │   └── themes.ts    # Light/dark themes
│   └── index.ts         # Public exports
└── package.json
```

**What belongs here:**
- ✅ Reusable UI primitives (Button, Input, Card)
- ✅ Design tokens (colors, spacing, typography)
- ✅ Theme configuration (light/dark modes)
- ✅ Icon components

**What does NOT belong:**
- ❌ Business logic
- ❌ API calls
- ❌ Feature-specific components
- ❌ State management

**Example:**
```tsx
// ✅ BELONGS in packages/ui/
export function Button({ children, onPress, variant = 'primary' }: ButtonProps) {
  return (
    <Tamagui.Button
      backgroundColor={variant === 'primary' ? '$primary' : '$secondary'}
      onPress={onPress}
    >
      {children}
    </Tamagui.Button>
  );
}

// ❌ DOES NOT BELONG in packages/ui/
export function LoginButton() {
  const { signIn } = useAuth(); // ❌ Business logic
  return <Button onPress={signIn}>Login</Button>;
}
```

### Lib Package (packages/lib/)

**Purpose**: Shared utilities and business logic

```
packages/lib/
├── src/
│   ├── stores/          # Zustand stores
│   │   ├── userStore.ts
│   │   └── authStore.ts
│   ├── hooks/           # Shared hooks
│   │   ├── useAuth.ts
│   │   └── useLocation.ts
│   ├── utils/           # Utilities
│   │   ├── date.ts
│   │   ├── validation.ts
│   │   └── format.ts
│   ├── types/           # Shared types
│   └── constants/       # App constants
└── package.json
```

**What belongs here:**
- ✅ Zustand stores
- ✅ Shared hooks (auth, data fetching)
- ✅ Utility functions (date formatting, validation)
- ✅ Shared types and interfaces
- ✅ Constants and enums

**Example:**
```typescript
// ✅ BELONGS in packages/lib/
export const useAuth = () => {
  const user = useUserStore((state) => state.user);
  const signIn = async (email: string, password: string) => {
    // Auth logic
  };
  return { user, signIn };
};
```

### i18n Package (packages/i18n/)

**Purpose**: Internationalization for all apps

```
packages/i18n/
├── translations/
│   ├── en/
│   │   ├── common.json
│   │   ├── mobile.json
│   │   └── web.json
│   ├── fr/
│   ├── de/
│   └── ar/
├── src/
│   ├── config.ts        # i18next configuration
│   └── index.ts
└── package.json
```

**Supported languages:**
- `en` - English
- `fr` - French
- `de` - German
- `ar` - Arabic (RTL)

**Structure:**
```json
// translations/en/mobile.json
{
  "auth": {
    "login": "Log In",
    "signup": "Sign Up"
  },
  "profile": {
    "title": "Profile",
    "edit": "Edit Profile"
  }
}
```

**Usage:**
```typescript
import { useTranslation } from '@hounii/i18n';

const { t } = useTranslation('mobile');
console.log(t('auth.login')); // "Log In"
```

### API Package (packages/api/)

**Purpose**: Supabase client and generated types

```
packages/api/
├── src/
│   ├── client.ts        # Supabase client factory
│   ├── types/
│   │   └── database.ts  # Generated from Supabase
│   └── index.ts
└── package.json
```

**What belongs here:**
- ✅ Supabase client configuration
- ✅ Database types (auto-generated)
- ✅ API helpers

**Example:**
```typescript
// ✅ BELONGS in packages/api/
export const createSupabaseClient = (anonKey: string) => {
  return createClient<Database>(SUPABASE_URL, anonKey);
};
```

### Config Package (packages/config/)

**Purpose**: Shared ESLint, TypeScript, and other configs

```
packages/config/
├── eslint-preset.js
├── typescript/
│   ├── base.json
│   ├── react.json
│   └── nextjs.json
└── package.json
```

**Usage:**
```json
// apps/mobile/tsconfig.json
{
  "extends": "@hounii/config/typescript/react.json"
}
```

## Supabase Directory (supabase/)

### Migrations (supabase/migrations/)

```
supabase/migrations/
├── 20240101000000_initial_schema.sql
├── 20240102000000_add_profiles.sql
└── 20240103000000_enable_rls.sql
```

**Naming**: `YYYYMMDDHHMMSS_description.sql`

### Edge Functions (supabase/functions/)

```
supabase/functions/
├── user-profile-update/
│   └── index.ts
└── send-notification/
    └── index.ts
```

## Workspace Configuration

### pnpm Workspace (pnpm-workspace.yaml)

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

All packages use `workspace:*` protocol:

```json
{
  "dependencies": {
    "@hounii/ui": "workspace:*",
    "@hounii/lib": "workspace:*"
  }
}
```

### Turborepo (turbo.json)

Defines task dependencies and caching:

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "lint": {},
    "type-check": {}
  }
}
```

**Run from root:**
```bash
pnpm build        # Builds all packages in dependency order
pnpm lint         # Lints entire workspace
pnpm type-check   # Type checks all packages
```

**Run specific package:**
```bash
pnpm --filter @hounii/mobile build
pnpm --filter @hounii/web dev
```

## Decision Tree: Where Should This Go?

### Is it a UI primitive?
- ✅ → `packages/ui/src/components/`

### Is it business logic or a utility?
- ✅ → `packages/lib/src/`

### Is it a translation string?
- ✅ → `packages/i18n/translations/`

### Is it a mobile screen or feature?
- ✅ → `apps/mobile/features/[feature-name]/`

### Is it a web page?
- ✅ → `apps/web/app/[route]/`

### Is it an admin feature?
- ✅ → `apps/admin/app/[section]/`

### Is it a database change?
- ✅ → `supabase/migrations/[timestamp]_[name].sql`

### Is it a backend function?
- ✅ → `supabase/functions/[function-name]/`

### Is it a shared config?
- ✅ → `packages/config/`

## Common Scenarios

### Adding a New Mobile Screen

1. **Create feature directory**: `apps/mobile/features/[feature-name]/`
2. **Add screen**: `apps/mobile/features/[feature-name]/screens/MainScreen.tsx`
3. **Create route**: `apps/mobile/app/[route].tsx`
4. **Add translations**: `packages/i18n/translations/en/mobile.json`
5. **Use UI components**: Import from `@hounii/ui`

### Adding Shared Business Logic

1. **Create utility**: `packages/lib/src/utils/myUtil.ts`
2. **Export from index**: `packages/lib/src/index.ts`
3. **Import in apps**: `import { myUtil } from '@hounii/lib'`

### Adding a New UI Component

1. **Create component**: `packages/ui/src/components/MyComponent.tsx`
2. **Export from index**: `packages/ui/src/index.ts`
3. **Use in apps**: `import { MyComponent } from '@hounii/ui'`

### Adding Database Table

1. **Create migration**: `supabase/migrations/[timestamp]_add_my_table.sql`
2. **Apply migration**: Use `mcp__supabase__apply_migration`
3. **Generate types**: `mcp__supabase__generate_typescript_types`
4. **Update API package**: Types auto-update in `packages/api/src/types/`

## Package Dependencies

### Dependency Flow

```
apps/mobile
  ↓ depends on
packages/ui, packages/lib, packages/i18n, packages/api
  ↓ depends on
External packages (react, tamagui, zustand, etc.)
```

**Rules:**
- Apps can depend on packages
- Packages can depend on other packages (carefully)
- Packages cannot depend on apps
- Use `workspace:*` for internal dependencies

### Circular Dependencies

**❌ AVOID:**
```
packages/ui → packages/lib → packages/ui  (CIRCULAR!)
```

**✅ PREFER:**
```
packages/ui → standalone
packages/lib → packages/ui (one direction only)
```

## File Naming Conventions

- **Components**: PascalCase (`Button.tsx`, `UserProfile.tsx`)
- **Utilities**: camelCase (`formatDate.ts`, `validation.ts`)
- **Hooks**: camelCase with `use` prefix (`useAuth.ts`, `useLocation.ts`)
- **Stores**: camelCase with `Store` suffix (`userStore.ts`, `authStore.ts`)
- **Pages (Next.js)**: lowercase (`page.tsx`, `layout.tsx`, `[id]`, `(group)`)
- **Screens (RN)**: PascalCase with `Screen` suffix (`HomeScreen.tsx`)

## Import Aliases

Configured in each app's `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],              // apps/mobile: relative imports
      "@/components/*": ["./components/*"],
      "@/features/*": ["./features/*"]
    }
  }
}
```

**Usage:**
```typescript
// ✅ Package imports
import { Button } from '@hounii/ui';
import { useAuth } from '@hounii/lib';

// ✅ Local imports with alias
import { HomeScreen } from '@/features/home';

// ✅ Relative imports (when close)
import { UserCard } from './components/UserCard';
```

## References

- Main config: [CLAUDE.md](../../../CLAUDE.md)
- Workspace config: [pnpm-workspace.yaml](../../../pnpm-workspace.yaml)
- Build pipeline: [turbo.json](../../../turbo.json)
- Package manager: pnpm v10.18.2
- Build system: Turborepo v2.5.8
