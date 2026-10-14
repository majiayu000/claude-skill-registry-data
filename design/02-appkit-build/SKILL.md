---
name: 02-appkit-build
description: >
  Build full-stack UI and backend features on a Databricks AppKit project from a PRD
  or feature spec. Covers SQL query design, type generation, React frontend with
  AppKit UI components, backend plugin wiring, and distinctive visual design. Use
  when asked to implement a UI, build features from a PRD, create pages or dashboards,
  add components, develop the frontend/backend of an existing AppKit app, build with
  mock data, or use static data for visual prototyping. Triggers on "build UI",
  "implement PRD", "create dashboard", "add page", "build features", "implement
  design", "create components", "build app from PRD", "develop frontend", "mock data",
  "static data", "two-phase data".
license: Apache-2.0
compatibility: Requires an existing AppKit project scaffolded via 01-appkit-scaffold skill, Node.js v22+, Databricks CLI >= 0.295.0
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Building features is **source editing** (`.sql` queries, `server/server.ts`, `client/src/**`) — fully
  client-agnostic; the same files are written on both clients. Deploy is delegated to `03-appkit-deploy`.
  The local toolchain steps are an **IDE convenience**: `npm run typegen`, `npm run dev`, `npx tsc --noEmit`,
  `npm run build`, and the `http://localhost:8000` checks have **no Genie Code equivalent** (no local Node) —
  on Genie Code typegen/tsc/build run **server-side on deploy**; write UI against the SQL schema + the
  appkit-ui docs and verify on the deployed app. `npx @databricks/appkit docs` is IDE-only (WebFetch on
  Genie Code). `databricks apps validate` is skipped on Genie Code (hard-blocked) — rely on `bundle validate`
  + server-side build logs.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: apps
  role: build
  standalone: false
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources: []  # Project-specific PRD-to-UI workflow; see See Also for canonical upstream.
---

# Build Features on Databricks AppKit

Implement full-stack UI and backend features on an already-scaffolded AppKit project, driven by a PRD or feature spec.

## When to Use

- Implementing a PRD or feature spec on an existing AppKit project
- Building pages, dashboards, or components with `@databricks/appkit-ui`
- Adding SQL queries and wiring them to type-safe React hooks
- Creating a visually distinctive, production-grade frontend

**Not for scaffolding.** Use `01-appkit-scaffold` to create a new project first.
**Not for adding plugins.** Use `04-appkit-plugin-add` to register new plugins.

---

## Before You Begin

### Working in Genie Code (client routing)

This skill is **source editing** — designing SQL queries, writing `server/server.ts`, and building React under `client/src/`. All of that is **identical on both clients**; only the local-toolchain gates differ:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `npm run typegen` (generates `client/src/appKitTypes.d.ts`) | no local Node — typegen runs **server-side on deploy**. Write UI against the `.sql` `-- @param` annotations + the appkit-ui docs; the generated types land at deploy/build time |
| `npm run dev` / `http://localhost:8000` checks (Step 6) | no local dev server — verify UI/queries on the **deployed** app (browser, or the OAuth-session test in `03-appkit-deploy`) |
| `npx tsc --noEmit` (Step 4b) / `npm run build` | no local typecheck — `npm`/`npx`/`tsc` cannot resolve `@databricks/appkit-ui` without `node_modules`. The platform builds **server-side** on deploy, but TS errors do **NOT** come back through `databricks apps logs <name>` (OAuth error from compute) — they appear only at `<app-url>/logz` in a browser. The one viable static pre-flight is the **import-specifier regex gate** in the `99-deploy_databricks_app.genie-code.md` fork (Step 2b) — run it before deploy |
| `npx @databricks/appkit docs …` | npx absent (P9) — WebFetch https://databricks.github.io/appkit/ |
| `ls node_modules/@databricks/appkit-ui/…` | no local `node_modules` — consult the appkit-ui docs (WebFetch) instead |
| `databricks apps validate --profile $PROFILE` (checklist) | hard-blocked on Genie Code — skip; rely on `bundle validate` (`runDatabricksCli`, omit `--profile`) + server-side build logs per `03-appkit-deploy` / `07-appkit-chat-history` Step 9 |

Edit files **in your workshop project** — paths are relative to the top-level app dir `$APP_ROOT` (= `<artifact_root>/<app_name>`; on Genie Code, under `/Workspace/Users/<your-email>/vibe-coding-workshop/<app_name>` — your git-cloned workshop project, NOT the `.assistant/skills` copy), never `/tmp`. See `skills/genie-code-environment` for the full manifest.

**Optional upstream checks** (skip if latency-constrained or the `last_verified` date above is < 30 days old):

1. **Databricks Apps skill (source of truth for AppKit workflow):**
   Fetch the latest from https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps
   If accessible, check the "Breaking Changes" and "New Patterns" sections.

2. **Anthropic frontend-design skill (inspiration for design quality):**
   Fetch the latest from https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
   Skim for new aesthetic examples. Skip if latency-constrained.

**Additional live docs (always prefer over bundled references):**

```bash
npx @databricks/appkit docs              # documentation index
npx @databricks/appkit docs "<query>"    # specific topic
```

Key upstream doc pages:
- LLM guardrails: https://databricks.github.io/appkit/docs/development/llm-guide
- Type generation: https://databricks.github.io/appkit/docs/development/type-generation
- UI components: https://databricks.github.io/appkit/docs/api/appkit-ui/
- Configuration: https://databricks.github.io/appkit/docs/configuration
- Architecture: https://databricks.github.io/appkit/docs/architecture

The bundled references below are fallbacks when live docs cannot be reached.

> **Workshop Mode (blank app):** If you are following the AppKit+Lakebase workshop (**Scaffold, Build & Test** step) and scaffolded a blank app without plugins, skip Step 2 (SQL Queries) and the `analytics()` plugin references in Step 4. Use static mock data arrays instead of `useAnalyticsQuery`. The backend only needs `server()` — no `analytics()` plugin. All SQL/typegen sections are not applicable until the Lakebase plugin is added in the **Wire Lakebase Backend** step.

---

## Architecture Overview

AppKit is a TypeScript full-stack framework with two packages:

- **`@databricks/appkit`** — backend: Express server, plugin system, SQL query execution, caching, telemetry
- **`@databricks/appkit-ui`** — frontend: React hooks (`useAnalyticsQuery`), UI primitives (Shadcn/Radix), data visualization (ECharts)

```
client/src/App.tsx  →  useAnalyticsQuery("key", params)  →  server/server.ts  →  config/queries/key.sql  →  SQL Warehouse
```

---

## Step 1: Read the PRD

Before writing any code, thoroughly understand:

- **User personas** and their needs
- **Key user journeys** (focus on Happy Path first)
- **Core features** and requirements
- **Data requirements** — what tables/queries will the UI need?

---

## Step 2: Plan and Create SQL Queries

Create `.sql` files in `config/queries/`. Each file becomes a query key.

```sql
-- config/queries/active_users.sql
-- @param startDate DATE
-- @param endDate DATE
SELECT user_id, email, last_login
FROM catalog.schema.users
WHERE last_login BETWEEN :startDate AND :endDate
ORDER BY last_login DESC
```

**Rules:**
- Use `:paramName` placeholders — NEVER construct SQL strings dynamically
- Annotate params with `-- @param name TYPE` (types: `STRING`, `NUMERIC`, `BOOLEAN`, `DATE`, `TIMESTAMP`)
- `:workspaceId` is auto-injected by the server — do NOT annotate it
- `queryKey.sql` runs as service principal; `queryKey.obo.sql` runs as user

Then generate types:

```bash
npm run typegen
```

**Do NOT write UI code until types are generated.** Read `client/src/appKitTypes.d.ts` to see available query types.

---

## Step 3: Design the UI

Before coding components, commit to a design direction. READ [references/design-quality.md](references/design-quality.md) for detailed guidelines.

Key principles:
- Choose a **bold aesthetic direction** — not generic AI aesthetics
- Use AppKit UI primitives (`@databricks/appkit-ui`) as the foundation, then layer distinctive styling on top
- Plan the page layout, component hierarchy, and navigation flow
- Pay special attention to the "CSS Variables → Components" section — it prevents the most common styling anti-pattern

---

## Step 4: Build the Backend

**First action:** Open `server/server.ts`. The scaffold may generate `createApp({...}).catch(console.error)` — this must be replaced. **Replace the file contents** with:

```typescript
import { createApp, server, analytics } from "@databricks/appkit";

await createApp({
  plugins: [server(), analytics()],
});
```

Verify the file uses `await createApp()` before proceeding. Do not leave `.catch(console.error)`.

For non-query APIs (writes, ML endpoints, custom logic), extend the server:

```typescript
const appkit = await createApp({
  plugins: [server({ autoStart: false }), analytics()],
});

appkit.server.extend((app) => {
  app.post("/api/custom-action", (req, res) => { /* ... */ });
});

await appkit.server.start();
```

**NEVER use tRPC or custom routes for SELECT queries** — always use SQL files in `config/queries/`.

---

## Step 4b: TypeScript Validation Gate

**You MUST run `npx tsc --noEmit` and fix all errors before proceeding to Step 5.** TypeScript errors in the backend will cascade to the frontend build and cause deploy failures. Fix them now while the scope is small.

---

## Step 5: Build the Frontend

Implement components in `client/src/`. Start with `App.tsx`.

### Two-Phase Data Pattern

Build the UI in two phases so you get immediate visual feedback before SQL queries are wired up.

**Scaffold step — Static data for immediate visual feedback:**

Use the `data` prop on AppKit data components (charts, tables) with representative sample data. This lets you build and iterate on the UI visually before wiring up live query-driven data.

```tsx
<BarChart
  data={[
    { month: "Jan", revenue: 4200 },
    { month: "Feb", revenue: 5100 },
    { month: "Mar", revenue: 3800 },
  ]}
  xKey="month"
  yKey="revenue"
/>
```

**Even with static data, add loading/error/empty branches** so components are ready for the query-driven swap:

```tsx
const properties = MOCK_PROPERTIES; // Will become API response
const loading = false;              // Will become true during fetch
const error: string | null = null;  // Will capture API errors

if (loading) return <Skeleton className="h-64 w-full" />;
if (error) return <div className="text-destructive">{error}</div>;
if (!properties.length) return <EmptyState />;
```

**Later — Swap to query-driven data (final state):**

Once SQL files exist in `config/queries/` and `npm run typegen` has generated types, replace static `data` with `queryKey` + `params`:

```tsx
import { useAnalyticsQuery } from "@databricks/appkit-ui/react";
import { sql } from "@databricks/appkit-ui/js";

function RevenueChart() {
  const params = useMemo(() => ({
    year: sql.number(2025),
  }), []);

  const { data, loading, error } = useAnalyticsQuery("monthly_revenue", params);

  if (loading) return <Skeleton className="h-32 w-full" />;
  if (error) return <div className="text-destructive">{error}</div>;
  if (!data?.length) return <div className="text-muted-foreground">No data</div>;

  return <BarChart data={data} xKey="month" yKey="revenue" />;
}
```

All static demo data must be replaced with query-driven data before declaring the build complete.

### Hard Rules

**GATE:** Read [references/llm-guardrails.md](references/llm-guardrails.md) before writing any code in this step. Violations of these rules cause runtime bugs and deployment failures. Key rules (not a substitute for reading the file):

- **SQL results return strings** — `useAnalyticsQuery` may return all values as strings at runtime, even for numeric columns. Always coerce with `Number()` before arithmetic to avoid string concatenation bugs
- **Always `useMemo`** on query parameters — prevents infinite refetch loops. For parameterless queries (`Record<string, never>`), pass `useMemo(() => ({}), [])`
- **Always handle loading/error/empty states** — use `Skeleton` for loading
- **Always use `sql.*` helpers** for parameters (`sql.date()`, `sql.string()`, `sql.number()`)
- **Use `import type`** for type-only imports when `verbatimModuleSyntax` is enabled
- **Never invent APIs** — only use documented exports from `@databricks/appkit` and `@databricks/appkit-ui`
- **Never build SQL strings dynamically** — use parameterized queries
- **`createApp()` is async** — always `await` it
- **Wrap root with `<TooltipProvider>`** — many AppKit components use tooltips internally; add this to `App.tsx` by default (imported from `@databricks/appkit-ui/react`, per the specifier rule below)
- **AppKit import specifiers are exact:**
  - Components/hooks: `import { … } from "@databricks/appkit-ui/react"` — **never** the bare `@databricks/appkit-ui` (the bare path has no React export and the build cannot resolve it).
  - Global stylesheet: `@import "@databricks/appkit-ui/styles.css";` in `client/src/index.css` — **never** the extension-less `@import "@databricks/appkit-ui/styles";` (the package only exports the `.css` path; the extension-less form is unresolvable). These two are the exact paths the scaffold ships.
- **Preserve the scaffold — do NOT regenerate from memory.** Edit `client/src/App.tsx` and `client/src/index.css` **incrementally**; never overwrite them with hand-authored versions. Regenerating these from memory is how the wrong (shorter) import specifiers get reintroduced. Likewise, **keep the scaffold's `client/src/ErrorBoundary.tsx`** — it is the only thing that surfaces a client-side runtime crash in the browser (a crash that otherwise deploys "green").
- **Images: external CDN primary, deterministic `onError` fallback (mandatory).** A generated mock has no realistic photo library to bundle, so external CDN hotlinks (Unsplash / Pexels) are the practical default `src` for realistic, use-case-varied imagery. But those requests are made by the **user's browser** and are routinely blocked by corporate/network egress — and the block is invisible at build time. So **every `<img>` must carry a runtime `onError` handler** that swaps `src` to an **inline data-URI SVG** placeholder (zero-network, embedded bytes — nothing to fetch or block), so a blocked CDN degrades to a clean placeholder instead of a blank/broken image: `<img src={cdnUrl} onError={(e) => { e.currentTarget.src = DATA_URI_SVG_PLACEHOLDER; }} alt="…" />`. When you actually have real images to ship, bundle them with the app (`client/public/…` or a Vite `import`) — served same-origin behind the OAuth gate, they render anywhere with no egress.
- **No decorative controls that silently no-op.** Every visible interactive control (filter, tab, date/guest picker, search box) must either function against the mock data OR be visibly marked as a later-phase placeholder (disabled, or a "coming soon" affordance). A control that looks live but does nothing reads as a broken app.

### UI Components

AppKit UI components are Shadcn/Radix-based. Data charts are ECharts-based — use props (`xKey`, `yKey`, `colors`), NOT Recharts children.

Check the live docs for the latest component list:

```bash
npx @databricks/appkit docs "appkit-ui API reference"
```

**Note:** The `docs` search matches section headings only. Searching for a component name like `"DataTable"` may fail. Use the full doc path for specific components:

```bash
npx @databricks/appkit docs "./docs/api/appkit-ui/data/DataTable.md"
```

### Chart Components Quick Reference

Available chart components from `@databricks/appkit-ui`:

| Component | Key Props | Use Case |
|-----------|-----------|----------|
| `BarChart` | `xKey`, `yKey`, `colors`, `height`, `title` | Categorical comparison |
| `LineChart` | `xKey`, `yKey`, `colors`, `height` | Trends over time |
| `AreaChart` | `xKey`, `yKey`, `colors`, `height` | Volume trends |
| `PieChart` | `nameKey`, `valueKey`, `colors` | Part-of-whole |
| `DonutChart` | `nameKey`, `valueKey`, `colors` | Part-of-whole (with center) |
| `ScatterChart` | `xKey`, `yKey`, `colors` | Correlation |

All accept either `data` (static array) for the scaffold step or `queryKey` + `parameters` for query-driven mode.

For the full list with all props, inspect the type definitions:

```bash
ls node_modules/@databricks/appkit-ui/dist/charts/
```

### Routing

The scaffold generates react-router v7 with `createBrowserRouter`. For multi-page apps, set up routing in `App.tsx`:

- **`createBrowserRouter`** — define routes with path and element
- **`<Outlet />`** — render child routes inside a layout component
- **`<NavLink>`** — navigation links with active state styling
- **`useParams()`** — read URL parameters (e.g. `/orders/:id`)
- **`useNavigate()`** — programmatic navigation

```tsx
import { createBrowserRouter, RouterProvider, NavLink, Outlet } from "react-router";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: "orders", element: <Orders /> },
      { path: "orders/:id", element: <OrderDetail /> },
    ],
  },
]);

function Layout() {
  return (
    <div>
      <nav>
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/orders">Orders</NavLink>
      </nav>
      <Outlet />
    </div>
  );
}
```

---

## Step 6: Test Locally

```bash
npm run dev
```

Verify at `http://localhost:8000`:
- UI loads without console errors
- Navigation works across pages
- Data queries return results (loading → data flow)
- All interactive elements respond

### Smoke Test Selectors

Update `tests/smoke.spec.ts` to use `data-testid` selectors instead of text/role selectors. Add `data-testid` attributes to the primary heading and at least one content element per page:

```tsx
<h1 data-testid="hero-heading">Find your perfect stay</h1>
```

```typescript
await expect(page.getByTestId('hero-heading')).toBeVisible();
```

Text and role selectors break when the UI adds duplicate content (e.g., a second heading with the same text). `data-testid` selectors are immune to copy changes and ARIA ambiguity.

---

## Known Gotchas

Common runtime surprises that cause bugs or confusion:

| Gotcha | Fix |
|--------|-----|
| SQL results return strings even for numeric columns | Coerce with `Number()` before arithmetic |
| `useAnalyticsQuery` params must be wrapped in `useMemo` | Unwrapped objects trigger infinite refetch loops |
| Parameterless queries generate `Record<string, never>` | Pass `useMemo(() => ({}), [])` |
| Charts are ECharts-based, not Recharts | Use props (`xKey`, `yKey`, `colors`) — not children (`<XAxis>`, `<Bar>`) |
| `import type` required with `verbatimModuleSyntax` | Separate type-only imports or build fails |
| Chart components accept both `data` (static) and `queryKey` (query-driven) props | Use `data` for scaffold-step static data, `queryKey` + `params` for query-driven mode |
| `npx @databricks/appkit docs` search matches section headings only | Use full doc path for specific component lookups |
| `npm run dev` triggers typegen via `predev` hook | `TABLE_OR_VIEW_NOT_FOUND` errors are expected if custom queries reference tables that don't exist yet. Not blocking. |
| `getByText`/`getByRole` matches multiple elements (Playwright strict mode) | Use `data-testid` selectors; add `data-testid` attributes to key elements during page creation |
| Escaped quotes in JSX attributes (`placeholder='I\'m...'`) crash Vite/rolldown parser | Use double-quoted attributes or JSX expressions: `placeholder={"I'm..."}` |
| AppKit AST-grep linter blocks `as any` and `as unknown as T` | Avoid type assertions; use proper type imports or leave parameters untyped for inference. `databricks apps validate` runs these rules but `npm run build` does not |
| Radix `<Select.Item>`/`<SelectItem>` throws at runtime if `value` is an empty string | **Never** use `value=""` for an "all/any" option (it crashes the component when the menu opens). Use a non-empty sentinel and filter explicitly: `<SelectItem value="all">` + `if (filter !== "all") { … }`. |
| `<Card onClick={...}>` without keyboard handlers | Wrap navigable cards in `<Link>` or add `role="link"`, `tabIndex={0}`, `onKeyDown`. Required for WCAG 2.1 AA. |
| A needed build tool (`vite`, `typescript`, `@vitejs/plugin-react`, …) absent from BOTH `dependencies` and `devDependencies` | The server-side build fails with the tool "missing". `devDependencies` is the scaffold-correct home — the platform build installs devDeps (the pristine v4 scaffold ships every build tool there and deploys), so do NOT move build tools to `dependencies`; only a tool missing from both is the defect. |
| `@tailwind`/`@layer` (or the AppKit stylesheet) without a complete toolchain | Toolchain-aware: **v3** needs `tailwind.config.*` **and** `postcss.config.*` present plus `tailwindcss`/`postcss`/`autoprefixer` in `dependencies`; **v4** needs `@tailwindcss/vite` in `dependencies` and wired into the vite `plugins`. The build-breaker is a **v3 PostCSS setup that also `@import`s `@databricks/appkit-ui/styles.css`** (a v4 stylesheet) — pick one generation. |
| Client bundle not in a `server()`-auto-detected dir | `server()` serves the client only from `dist`, `client/dist`, `build`, `public`, or `out` (project-root-relative — `build/` is **NOT** reserved, verified in Phase 0). The trap is `dist/client` from a **root-level `vite.config` with `root: "client"` + `outDir: "../dist/client"`** → deploys GREEN but returns `Cannot GET /`. Use the scaffold's `client/vite.config.ts` (outDir → `client/dist`) or pass `server({ staticPath })`. |

---

## Pre-Finalization Checklist

Before declaring the build complete:

- [ ] SQL files exist in `config/queries/` for every data need
- [ ] `npm run typegen` has been run after all SQL files are finalized
- [ ] All query parameters wrapped in `useMemo`
- [ ] Loading/error/empty states on every data component
- [ ] `tests/smoke.spec.ts` uses `data-testid` selectors (not text/role); key elements have `data-testid` attributes
- [ ] Static demo data renders correctly (swap to live data happens in the **Wire Lakebase Backend** step)
- [ ] `npx tsc --noEmit` passes with zero TypeScript errors (catches unused imports, missing types that block deployment)
- [ ] `npm run dev` runs cleanly at `http://localhost:8000`
- [ ] `databricks apps validate --profile $PROFILE` passes (catches strict-mode TS errors and smoke test regressions that `npm run build` alone misses)

---

## What's Next: Deploying

Once local testing passes, deploy to Databricks Apps using the `03-appkit-deploy` skill at `@apps_lakebase/skills/03-appkit-deploy/SKILL.md`. The calling prompt (`02-deploy.md` or `05-e2e-test.md`) will set variables and invoke the skill.

See the [AppKit App Management docs](https://databricks.github.io/appkit/docs/app-management) for advanced deploy options.

---

## See Also

- Authoritative upstream: [databricks-agent-skills / `databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) — canonical Apps platform patterns this skill builds on.
- Frontend design reference: [Anthropic frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- AppKit docs hub: [databricks.github.io/appkit](https://databricks.github.io/appkit/)

