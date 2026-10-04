---
name: notepad-new-frontend-page
description: "Reference doc: New Frontend Page Checklist"
---

# New Frontend Page Checklist

Use this notepad when creating a new page in the simpler-grants-gov Next.js frontend.

## Files to Create/Modify

| # | File | Purpose |
|---|------|---------|
| 1 | `frontend/src/app/<route>/page.tsx` | Page component (RSC by default) |
| 2 | `frontend/src/components/<domain>/` | Domain-specific components |
| 3 | `frontend/src/i18n/messages/en/index.ts` | Add translations |
| 4 | `frontend/src/services/fetch/` | API fetcher (if new endpoint) |
| 5 | `frontend/tests/components/<domain>/` | Component tests |
| 6 | `frontend/e2e/` | Playwright E2E test (if user-facing flow) |

## Page Component (Server Component by default)

```tsx
import { useTranslations } from "next-intl";
import { Metadata } from "next";

export function generateMetadata(): Metadata {
  return { title: "Page Title | Simpler.Grants.gov" };
}

export default function MyPage() {
  const t = useTranslations("MyPage");
  return (
    <div>
      <h1>{t("header")}</h1>
    </div>
  );
}
```

## Data Fetching (Server-Side)

```tsx
import { requesterForEndpoint } from "src/services/fetch";

const fetchData = requesterForEndpoint({
  method: "GET",
  basePath: process.env.API_URL,
  endpointPath: "/v1/my-endpoint",
});

export default async function MyPage() {
  const data = await fetchData();
  return <MyComponent data={data} />;
}
```

## Promise-as-Props Pattern (non-blocking)

```tsx
// Parent passes unresolved promise
export default function MyPage() {
  const dataPromise = fetchData();
  return <ChildComponent dataPromise={dataPromise} />;
}

// Child awaits it
async function ChildComponent({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = await dataPromise;
  return <div>{data.name}</div>;
}
```

## Client Components (only when needed)

```tsx
"use client";
import { useTranslations } from "next-intl";
import { useClientFetch } from "src/hooks/useClientFetch";

export function InteractiveComponent() {
  const t = useTranslations("MyFeature");
  const { data, error, loading } = useClientFetch("/v1/endpoint");
  // Event handlers, state, etc.
}
```

## Translations

Add to `frontend/src/i18n/messages/en/index.ts`:

```typescript
MyPage: {
  pageTitle: "My Page | Simpler.Grants.gov",
  header: "My Page Header",
  description: "Description text goes here.",
},
```

## Component Organization

- Domain-based directories: `components/search/`, `components/workspace/`
- NO barrel files (`index.ts` re-exports)
- NO type-based directories (`buttons/`, `modals/`)
- Shared utilities go to `frontend/src/utils/`

## USWDS Components

Import from `@trussworks/react-uswds`. Wrap in project-specific components for SSR safety when needed.

## Don't Forget

- [ ] Server component by default (`"use client"` only if needed)
- [ ] All text in translation file (no hardcoded strings in JSX)
- [ ] jest-axe accessibility scan in every component test
- [ ] USWDS components preferred over custom HTML
- [ ] No barrel files
