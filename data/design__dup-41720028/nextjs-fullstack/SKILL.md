---
name: nextjs-fullstack
description: Next.js fullstack development guidelines for React 19 and Next.js 15+. Use when building Next.js applications with Feature-Sliced Design, TailwindCSS v4, ShadCN, Jotai, React Query, and Supabase integration. Covers file naming, component architecture, testing with Vitest/Playwright, UI/UX design patterns, and Toss frontend principles.
---

# Next.js Fullstack Development

## Quick Reference

- **Next.js Convention**: See [nextjs-convention.md](references/nextjs-convention.md) for FSD structure and package conventions
- **UI/UX Design**: See [design-rules.md](references/design-rules.md) for design patterns and accessibility
- **Playwright Testing**: See [playwright-test-guide.md](references/playwright-test-guide.md) for E2E tests
- **Toss Principles**: See [toss-frontend.md](references/toss-frontend.md) for readability, predictability, cohesion

## Core Conventions

### Package Manager
Use `pnpm` instead of `npm`, `bunx` instead of `npx`.

### File Naming
- All files: `kebab-case` (e.g., `user-profile.tsx`, `auth-form.tsx`)
- Components: `PascalCase` for component names, `kebab-case` for files
- Functions/Variables: `camelCase`

### Directory Structure (Feature-Sliced Design)
```
├── app/                     # Next.js App Router (routing only)
│   ├── (routes)/example/page.tsx  # Re-export from FSD pages
│   └── api/                 # API Route Handlers
└── src/
    ├── pages/               # FSD Pages Layer
    ├── widgets/             # Header, Sidebar, Footer
    ├── features/            # User scenarios (auth, checkout)
    ├── entities/            # Business entities (user, product)
    └── shared/              # Shared resources
        ├── ui/              # ShadCN components
        ├── lib/             # Utilities
        └── api/             # Supabase clients
```

### Layer Import Rules
Upper layers can only import from lower layers:
`app` → `pages` → `widgets` → `features` → `entities` → `shared`

```typescript
// Import through public API only
import { UserCard } from '@/entities/user';     // Correct
import { UserCard } from '@/entities/user/ui/user-card'; // Wrong
```

## Tech Stack

| Category | Technology |
|----------|------------|
| UI Components | ShadCN (`pnpm dlx shadcn@latest add [name]`) |
| Icons | lucide-react |
| State Management | Jotai |
| Data Fetching | React Query |
| Styling | TailwindCSS v4 (globals.css only) |
| Testing | Vitest + Playwright |
| Database | Supabase |

## React 19 / Next.js 15 Patterns

### Server vs Client Components
```typescript
// Default: Server Component (no directive needed)
export function ServerPage() {
  return <div>Server rendered</div>;
}

// Client Component: explicit directive
'use client';
export function InteractiveButton() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Async APIs
```typescript
const cookieStore = await cookies();
const headersList = await headers();
const params = await props.params;
const searchParams = await props.searchParams;
```

### Server Actions
```typescript
// src/features/auth/api/actions.ts
'use server';

export async function signIn(formData: FormData) {
  // Server action logic
}
```

## Code Quality Principles

### Naming Magic Numbers
```typescript
const ANIMATION_DELAY_MS = 300;
await delay(ANIMATION_DELAY_MS);
```

### Separate Conditional Components
```typescript
function SubmitButton() {
  const isViewer = useRole() === 'viewer';
  return isViewer ? <ViewerSubmitButton /> : <AdminSubmitButton />;
}
```

### Consistent Return Types
```typescript
type ValidationResult = { ok: true } | { ok: false; reason: string };

function checkIsNameValid(name: string): ValidationResult {
  if (name.length === 0) return { ok: false, reason: 'Name cannot be empty.' };
  return { ok: true };
}
```

## Testing

### Vitest Setup
```typescript
// vitest.config.mts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: { environment: 'jsdom' },
});
```

### Playwright Locator Priority
```typescript
// 1. Role and accessibility (preferred)
page.getByRole('button', { name: 'Login' });
page.getByLabel('Email');

// 2. Text
page.getByText('Create account');

// 3. Test ID (last resort)
page.getByTestId('submit-button');
```
