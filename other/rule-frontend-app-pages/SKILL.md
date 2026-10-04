---
name: rule-frontend-app-pages
description: MANDATORY when editing files matching ["frontend/src/app/**/*.tsx", "frontend/src/app/**/*.ts"]. When working on Next.js App Router pages and layouts in frontend/src/app/
---

# Frontend App Router Pages Rules

## Server Components by Default

ALWAYS use server components at the page level. NEVER add `"use client"` to page.tsx or layout.tsx unless the page itself requires client-side interactivity (not just its children). Delegate client interactivity to child components.

## Metadata Generation

ALWAYS use async `generateMetadata()` for page-specific metadata. ALWAYS integrate with `next-intl` for translated titles and descriptions. NEVER hardcode English strings in metadata.

Example from codebase:
```tsx
// From frontend/src/app/[locale]/(base)/opportunities/page.tsx
import { getTranslations } from "next-intl/server";

export async function generateMetadata({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale });
  return {
    title: t("opportunities.title"),
    description: t("opportunities.description"),
  };
}
```

## Async Params

ALWAYS type page params as `Promise<{...}>` and await them. This is the Next.js App Router async params pattern.

Example from codebase:
```tsx
// From frontend/src/app/[locale]/(base)/opportunity/[id]/page.tsx
type Props = {
  params: Promise<{ id: string; locale: string }>;
};

export default async function OpportunityPage({ params }: Props) {
  const { id, locale } = await params;
  ...
}
```

## ISR and Dynamic Classification

ALWAYS set `export const revalidate = 600` (10-minute ISR) for pages with data that updates periodically. ALWAYS set `export const dynamic = "force-dynamic"` for pages requiring fresh data on every request (user-specific, real-time). NEVER leave pages without an explicit caching strategy when they fetch data.

Example from codebase:
```tsx
// Static with ISR (default for data pages)
export const revalidate = 600;

// Fully dynamic (user-specific pages like dashboard, settings)
export const dynamic = "force-dynamic";
```

## Layout Hierarchy

ALWAYS define shared metadata at the layout level. ALWAYS use `generateMetadata()` in page.tsx to override layout-level metadata with page-specific values. NEVER duplicate metadata between layout and page.

Example from codebase:
```tsx
// From frontend/src/app/[locale]/(base)/layout.tsx
export async function generateMetadata({ params }: LayoutProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale });
  return {
    title: { template: "%s | simpler.grants.gov", default: t("site.title") },
  };
}
```

## Locale Routing

ALWAYS use the `[locale]/(base)/` route group structure for localized pages. ALWAYS use `[locale]/(print)/` for print-optimized layouts. NEVER create routes outside the `[locale]` dynamic segment.

## API Routes

ALWAYS use the `respondWithTraceAndLogs()` middleware wrapper for API route handlers in `frontend/src/app/api/`. ALWAYS return typed JSON responses. NEVER expose internal implementation details in API route responses.

Example from codebase:
```tsx
// From frontend/src/app/api/ pattern
import { respondWithTraceAndLogs } from "src/utils/apiUtils";

export async function GET(request: NextRequest) {
  return respondWithTraceAndLogs(request, async () => {
    const data = await fetchData();
    return NextResponse.json(data);
  });
}
```

## Error and Loading Boundaries

ALWAYS provide `error.tsx` for error boundaries on routes that fetch data. ALWAYS provide `loading.tsx` for routes with significant data loading. NEVER show raw error messages to users — use translated error strings.

## Page Structure

NEVER place business logic in page.tsx files. ALWAYS delegate to components (for rendering) and services (for data fetching). Pages should be thin orchestrators that compose components with data.

Example from codebase:
```tsx
// Correct: thin page composing components
export default async function SearchPage({ params, searchParams }: Props) {
  const { locale } = await params;
  const resolvedSearchParams = await searchParams;
  return <SearchResults locale={locale} searchParams={resolvedSearchParams} />;
}
```

## Not Found Handling

ALWAYS use the `[...not-found]/` catch-all route for 404 pages. ALWAYS provide a localized 404 page with navigation back to the homepage.

---

## Context Enrichment

When generating significant page code (new route, new layout, new API route), enrich your context:
- Call `get_architecture_section("frontend")` from the `simpler-grants-context` MCP server to understand frontend architecture
- Call `get_rule_detail("frontend-components")` for component patterns used in pages
- Call `get_rule_detail("frontend-services")` for data fetching patterns
- Call `get_rule_detail("frontend-i18n")` for translation integration
- Consult **Compound Knowledge** for indexed documentation on page patterns

## Related Rules

When working on App Router pages, also consult these related rules:
- **`frontend-components.mdc`** — component patterns composed in pages
- **`frontend-services.mdc`** — data fetching and API service patterns
- **`frontend-i18n.mdc`** — translation key naming and usage
- **`frontend-hooks.mdc`** — client-side hooks used in interactive pages
- **`accessibility.mdc`** — WCAG 2.1 AA compliance for all user-facing pages
- **`cross-domain.mdc`** — structured logging, feature flags

## Specialist Validation

When generating or significantly modifying page code:

**For simple changes (< 20 lines, metadata update, layout adjustment):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new page route, new API route):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new route group, new layout hierarchy, new middleware):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate page structure and data flow
- `performance-oracle` — check ISR/dynamic classification and rendering strategy
- `kieran-typescript-reviewer` — TypeScript-specific quality review
- `accessibility-auditor` — verify page accessibility compliance
