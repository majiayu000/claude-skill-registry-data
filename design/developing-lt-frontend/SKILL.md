---
name: developing-lt-frontend
description: PRIMARY expert for ALL Nuxt and Vue frontend tasks. ALWAYS use this skill when working with Nuxt 4, Vue components, Nuxt UI, frontend pages, or files in app/components/, app/composables/, app/pages/, app/interfaces/ (supports monorepos with projects/app/, packages/app/). Handles modals (useOverlay), forms (Valibot), API integration (types.gen.ts, sdk.gen.ts), authentication (Better Auth), TailwindCSS styling, useFetch, useState, SSR. ALWAYS activate for .vue files, nuxt.config.ts, or frontend development. NOT for NestJS backend (use generating-nest-servers).
---

# lenne.tech Frontend Development

## When to Use This Skill

- Working with Nuxt 4 projects (nuxt.config.ts present)
- Editing files in `app/components/`, `app/composables/`, `app/pages/`, `app/interfaces/`
- Creating or modifying Vue components with Nuxt UI
- Integrating backend APIs via generated types (`types.gen.ts`, `sdk.gen.ts`)
- Building forms with Valibot validation
- Implementing authentication (login, register, 2FA, passkeys)
- Working in monorepos with `projects/app/` or `packages/app/` structure

**NOT for:** NestJS backend development (use `generating-nest-servers` skill instead)

## Development Approach: Real Backend Integration FIRST

**CRITICAL: Always implement with real backend integration immediately!**

```
┌────────────────────────────────────────────────────────────────┐
│  ❌ FORBIDDEN:                                                 │
│  - Placeholder data: const items = ['Item 1', 'Item 2']        │
│  - TODO comments: // TODO: Connect to API later                │
│  - Mock functions: async function fetchData() { return [] }    │
│  - Dummy interfaces: interface Item { name: string }           │
│  - "We'll add the API call later"                              │
│                                                                │
│  ✅ REQUIRED:                                                  │
│  - Real API calls from the start                               │
│  - Generated types (types.gen.ts)                              │
│  - Generated SDK functions (sdk.gen.ts)                        │
│  - Feature-by-feature with full backend integration            │
└────────────────────────────────────────────────────────────────┘
```

**Workflow for each feature:**

1. **Ensure services are running** (API on 3000, App on 3001)
2. **Generate types first** (`npm run generate-types`)
3. **Create composable** with real SDK functions
4. **Build component** using the composable
5. **Test in browser** with real data
6. **Move to next feature** only when current one works

**Example - The RIGHT way:**

```typescript
// ✅ CORRECT: Real integration from the start
import type { ProductDto } from '~/api-client/types.gen'
import { productControllerFindAll } from '~/api-client/sdk.gen'

export function useProducts() {
  const products = ref<ProductDto[]>([])

  async function fetchAll() {
    const response = await productControllerFindAll()
    if (response.data) products.value = response.data
  }

  return { products: readonly(products), fetchAll }
}
```

```typescript
// ❌ WRONG: Placeholder approach
interface Product { name: string }  // Manual interface!
const products = ref<Product[]>([
  { name: 'Placeholder 1' },  // Fake data!
  { name: 'Placeholder 2' }
])
// TODO: Connect to API  // Deferred work!
```

**Why this matters:**
- Placeholders hide integration issues until later
- Manual interfaces drift from backend DTOs
- "Later" often means bugs discovered too late
- Real data reveals edge cases immediately

## Test-Driven Development (TDD)

**For frontend features, follow the TDD approach:**

```
1. Backend API must be complete (API tests pass)
2. Write E2E tests BEFORE implementing frontend
3. Implement components/pages until E2E tests pass
4. Debug with Chrome DevTools MCP
```

**Complete E2E testing guide: [reference/e2e-testing.md](./reference/e2e-testing.md)**

### Quick E2E Test Example

```typescript
// tests/e2e/products.spec.ts
import { test, expect } from '@playwright/test';

test('should create product', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="create"]');
  await page.fill('[data-testid="name"]', `Test-${Date.now()}`);
  await page.click('[data-testid="submit"]');
  await expect(page.locator('text=erfolgreich')).toBeVisible();
});
```

### Test Cleanup (CRITICAL)

**Every E2E test must clean up after itself:**

```typescript
test.afterAll(async ({ request }) => {
  for (const id of createdIds) {
    await request.delete(`/api/products/${id}`);
  }
});
```

**Use separate test database:** `app-test` instead of `app-dev`

## Related Skills

**Works closely with:**
- `generating-nest-servers` - For NestJS backend development (projects/api/)
- `using-lt-cli` - For Git operations and Fullstack initialization
- `building-stories-with-tdd` - For complete TDD workflow (Backend + Frontend)

**When to use which:**
- .vue files, Nuxt, Vue components? Use **this skill** (developing-lt-frontend)
- NestJS, services, controllers? Use `generating-nest-servers` skill
- Git operations, `lt` commands? Use `using-lt-cli` skill
- Complete TDD workflow (tests first)? Use `building-stories-with-tdd` skill

**In monorepo projects:**
- `projects/app/` or `packages/app/` → **This skill**
- `projects/api/` or `packages/api/` → `generating-nest-servers` skill

## TypeScript Language Server (Recommended)

**Use the LSP tool when available** for better code intelligence in TypeScript/Vue/Nuxt projects:

| Operation | Use Case |
|-----------|----------|
| `goToDefinition` | Find where a type, composable, or component is defined |
| `findReferences` | Find all usages of a symbol across the codebase |
| `hover` | Get type information for props, refs, and computed values |
| `documentSymbol` | List all exports, functions, and types in a file |
| `workspaceSymbol` | Search for composables, interfaces, or components |
| `goToImplementation` | Find implementations of interfaces |

**When to use LSP:**
- Finding where a type from `types.gen.ts` is used → `findReferences`
- Understanding composable structure → `documentSymbol`
- Navigating to type definitions → `goToDefinition`
- Searching for components or composables → `workspaceSymbol`

**Installation (if LSP not available):**
```bash
claude plugins install typescript-lsp --marketplace claude-plugins-official
```

## Service Health Check (MANDATORY)

**Before starting ANY frontend work, check if required services are running:**

```bash
# Check if API is running (Port 3000)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api

# Check if App is running (Port 3001)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3001
```

**Workflow:**

```
┌────────────────────────────────────────────────────────────────┐
│  BEFORE starting frontend work:                                │
│                                                                │
│  1. CHECK API (Port 3000):                                     │
│     curl -s -o /dev/null -w "%{http_code}" localhost:3000/api  │
│     - If NOT 200: Start API in background                      │
│       cd projects/api && npm run start:dev &                   │
│     - Wait until API responds (max 30s)                        │
│                                                                │
│  2. CHECK APP (Port 3001):                                     │
│     curl -s -o /dev/null -w "%{http_code}" localhost:3001      │
│     - If NOT 200: Start App in background                      │
│       cd projects/app && npm run dev &                         │
│     - Wait until App responds (max 30s)                        │
│                                                                │
│  3. ONLY THEN proceed with frontend development                │
└────────────────────────────────────────────────────────────────┘
```

**Starting Services (if not running):**

```bash
# Start API in background (from monorepo root)
cd projects/api && npm run start:dev &

# Start App in background (from monorepo root)
cd projects/app && npm run dev &
```

**Important:**
- Always check BEFORE starting to avoid duplicate processes
- Use `lsof -i :3000` or `lsof -i :3001` to check if port is already in use
- If port is in use but service not responding, investigate before starting another instance

## Browser Testing (Chrome DevTools MCP)

**After implementing each feature, verify it works in the browser!**

**Available Tools:**
| Tool | Use Case |
|------|----------|
| `mcp__chrome-devtools__navigate_page` | Navigate to URL |
| `mcp__chrome-devtools__take_snapshot` | Get page structure with UIDs (preferred) |
| `mcp__chrome-devtools__take_screenshot` | Visual verification |
| `mcp__chrome-devtools__click` / `fill` | Interact with elements |
| `mcp__chrome-devtools__list_console_messages` | Check for JS errors |
| `mcp__chrome-devtools__list_network_requests` | Debug API calls |

**Workflow after each feature:**

```
┌────────────────────────────────────────────────────────────────┐
│  AFTER implementing a feature:                                 │
│                                                                │
│  1. NAVIGATE to the page:                                      │
│     mcp__chrome-devtools__navigate_page(url: "localhost:3001") │
│                                                                │
│  2. TAKE SNAPSHOT (preferred over screenshot):                 │
│     mcp__chrome-devtools__take_snapshot()                      │
│     - Check if on correct page (middleware may redirect)       │
│     - If redirected to /login: Handle authentication first     │
│                                                                │
│  3. CHECK CONSOLE for errors:                                  │
│     mcp__chrome-devtools__list_console_messages(types: error)  │
│     - Fix any JavaScript errors before proceeding              │
│                                                                │
│  4. VERIFY API calls work:                                     │
│     mcp__chrome-devtools__list_network_requests()              │
│     - Check for failed requests (4xx, 5xx)                     │
│                                                                │
│  5. ONLY proceed to next feature when current one works        │
└────────────────────────────────────────────────────────────────┘
```

**Authentication Handling:**
- Most pages require login
- If redirected to `/login` or `/auth/login`: Ask user for credentials
- Use `fill` and `click` tools to authenticate
- Then navigate back to intended page

## Nuxt UI MCP (Component Documentation)

**Use the Nuxt UI MCP tools for component documentation:**

| Tool | Use Case |
|------|----------|
| `mcp__nuxt-ui-remote__list-components` | List all available components |
| `mcp__nuxt-ui-remote__get-component` | Get component documentation |
| `mcp__nuxt-ui-remote__get-component-metadata` | Get props, slots, events |
| `mcp__nuxt-ui-remote__search-components-by-category` | Find components by category |
| `mcp__nuxt-ui-remote__list-composables` | List available composables |

**When to use:**
- Before using a Nuxt UI component you haven't used before
- When unsure about available props or slots
- When looking for the right component for a use case

## Error Recovery

**For detailed troubleshooting workflows, see [reference/troubleshooting.md](./reference/troubleshooting.md)**

**Quick fixes:**
- Type generation fails → Check if API is running on port 3000
- API won't start → Check `lsof -i :3000`, kill stale processes
- Build fails → Run `npm run generate-types`, check imports
- Console errors → Use `mcp__chrome-devtools__list_console_messages`

## Nuxt 4 Directory Structure

```
app/                  # Application code (srcDir)
├── components/       # Auto-imported components
├── composables/      # Auto-imported composables
├── interfaces/       # TypeScript interfaces
├── lib/              # Utility libraries (auth-client, etc.)
├── pages/            # File-based routing
├── layouts/          # Layout components
├── utils/            # Auto-imported utilities
└── api-client/       # Generated types & SDK
server/               # Nitro server routes
public/               # Static assets
nuxt.config.ts
```

## Type Rules

**CRITICAL: Never create custom interfaces for backend DTOs!**

| Priority | Source | Use For |
|----------|--------|---------|
| 1. | `~/api-client/types.gen.ts` | All backend DTOs (REQUIRED) |
| 2. | `~/api-client/sdk.gen.ts` | All API calls (REQUIRED) |
| 3. | Nuxt UI types | Component props (auto-imported) |
| 4. | `app/interfaces/*.interface.ts` | Frontend-only types (UI state, forms) |

### Missing Generated Types

**If `types.gen.ts` or `sdk.gen.ts` are missing/outdated:** See [reference/troubleshooting.md](./reference/troubleshooting.md#missing-generated-types)

**Key rules:**
- ❌ NEVER create manual interfaces as workaround
- ✅ Always run `npm run generate-types` with API running

### Generating Types

**Prerequisites:** Backend API must be running!

```bash
# Start API first (in monorepo)
cd projects/api && npm run start:dev

# Wait for API to be ready (check http://localhost:3000/api)

# Then generate types (from frontend directory)
npm run generate-types
```

## Core Patterns

### API Calls (via generated SDK)

```typescript
import type { SeasonDto } from '~/api-client/types.gen'
import { seasonControllerGet } from '~/api-client/sdk.gen'

const response = await seasonControllerGet()
const seasons: SeasonDto[] = response.data ?? []
```

### Composables (one per controller)

```typescript
export function useSeasons() {
  const seasons = ref<SeasonDto[]>([])
  const loading = ref<boolean>(false)

  async function fetchSeasons(): Promise<void> {
    loading.value = true
    try {
      const response = await seasonControllerGet()
      if (response.data) seasons.value = response.data
    } finally {
      loading.value = false
    }
  }

  return { seasons: readonly(seasons), loading: readonly(loading), fetchSeasons }
}
```

### Shared State (useState)

```typescript
// For state shared across components (SSR-safe)
export function useSettings() {
  const theme = useState<'light' | 'dark'>('app-theme', () => 'light')
  return { theme }
}
```

### Authentication (Better Auth)

```typescript
// app/composables/use-better-auth.ts (pre-configured in nuxt-base-starter)
import { authClient } from '~/lib/auth-client'

export function useBetterAuth() {
  const session = authClient.useSession(useFetch)

  const user = computed(() => session.data.value?.user ?? null)
  const isAuthenticated = computed<boolean>(() => !!session.data.value?.session)
  const isAdmin = computed<boolean>(() => user.value?.role === 'admin')

  return {
    user, isAuthenticated, isAdmin,
    signIn: authClient.signIn,   // Password auto-hashed (SHA256)
    signUp: authClient.signUp,   // Password auto-hashed (SHA256)
    signOut: authClient.signOut,
    twoFactor: authClient.twoFactor,
    passkey: authClient.passkey,
  }
}
```

**Preferred auth methods:** Passkey (WebAuthn) or Email/Password + 2FA (TOTP)
**Base path:** `/iam` (must match nest-server config)

### Programmatic Modals

```typescript
const overlay = useOverlay()

overlay.open(ModalCreate, {
  props: { title: 'Neu' },
  onClose: (result) => { if (result) refreshData() }
})
```

### Valibot Forms (not Zod)

```typescript
import { object, pipe, string, minLength } from 'valibot'
import type { InferOutput } from 'valibot'

const schema = object({
  title: pipe(string(), minLength(3, 'Mindestens 3 Zeichen'))
})
type Schema = InferOutput<typeof schema>
const state = reactive<Schema>({ title: '' })
```

## Standards

| Rule | Value |
|------|-------|
| UI Labels | German (`Speichern`, `Abbrechen`) |
| Code/Comments | English |
| Styling | TailwindCSS only, no `<style>` |
| Colors | Semantic only (`primary`, `error`, `success`), no hardcoded |
| Types | Explicit, no implicit `any` |
| Backend Types | **Generated only** (`types.gen.ts`) |
| Custom Interfaces | Frontend-only (`app/interfaces/*.interface.ts`) |
| Composables | `app/composables/use*.ts` |
| Shared State | `useState()` for SSR-safe state |
| Local State | `ref()` / `reactive()` |

## Reference Files

| Topic | File |
|-------|------|
| TypeScript | [reference/typescript.md](./reference/typescript.md) |
| Components | [reference/components.md](./reference/components.md) |
| Composables | [reference/composables.md](./reference/composables.md) |
| Forms | [reference/forms.md](./reference/forms.md) |
| Modals | [reference/modals.md](./reference/modals.md) |
| API | [reference/api.md](./reference/api.md) |
| Colors | [reference/colors.md](./reference/colors.md) |
| Nuxt Patterns | [reference/nuxt.md](./reference/nuxt.md) |
| Authentication | [reference/authentication.md](./reference/authentication.md) |
| **E2E Testing** | [reference/e2e-testing.md](./reference/e2e-testing.md) |
| Troubleshooting | [reference/troubleshooting.md](./reference/troubleshooting.md) |
| **Security** | [reference/security.md](./reference/security.md) |

## Pre-Commit

**Backend Integration (CRITICAL):**
- [ ] **No placeholder data** (no fake arrays, no dummy objects)
- [ ] **No TODO comments for API integration** (integrate immediately)
- [ ] **No manual interfaces for backend DTOs** (use `types.gen.ts`)
- [ ] All API calls via `sdk.gen.ts`
- [ ] Types regenerated after backend changes (`npm run generate-types`)
- [ ] Each feature fully integrated before starting next

**Code Quality:**
- [ ] Logic in composables
- [ ] Modals use `useOverlay`
- [ ] Forms use Valibot
- [ ] TailwindCSS only
- [ ] **Semantic colors only** (`primary`, `error`, `success`), no hardcoded colors
- [ ] German UI, English code
- [ ] No implicit `any`
- [ ] ESLint passes

**Authentication:**
- [ ] Auth uses `useBetterAuth()` composable (pre-configured)
- [ ] Protected routes use `middleware: 'auth'`
- [ ] Auth base path is `/iam` (nest-server default)

**Security (OWASP):**
- [ ] **No v-html with user content** (see [security.md](./reference/security.md))
- [ ] **Tokens stored securely** (not in localStorage)
- [ ] Input validation with Valibot schemas

**Browser Verification:**
- [ ] Feature tested in browser (Chrome DevTools MCP)
- [ ] No console errors (`list_console_messages`)
- [ ] API calls successful (`list_network_requests`)
- [ ] Page renders correctly (snapshot or screenshot)
