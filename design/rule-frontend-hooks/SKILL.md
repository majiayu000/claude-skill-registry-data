---
name: rule-frontend-hooks
description: MANDATORY when editing files matching ["frontend/src/hooks/**/*.ts"]. When working on custom React hooks in frontend/src/hooks/
---

# Frontend Hooks Rules

## Standalone vs. Service-Coupled Hook Placement
ALWAYS place standalone custom hooks in `src/hooks/` as individual `use{PascalCaseName}.ts` files. If a hook is part of a larger service, it MUST live in that service's directory (e.g., `src/services/auth/useUser.tsx`).

Example from codebase:
```typescript
// Standalone hooks in src/hooks/
// src/hooks/useClientFetch.ts
// src/hooks/useSearchParamUpdater.ts
// src/hooks/useRouteChange.ts

// Service-coupled hook in service directory
// src/services/auth/useUser.tsx
```

## useClientFetch as Standard Client-Side Fetch Hook
ALWAYS use `useClientFetch<T>` for client-side API requests. NEVER create standalone client fetcher files.

Example from codebase:
```typescript
// From frontend/src/hooks/useClientFetch.ts usage
const { clientFetch } = useClientFetch<Response>(
  "Error deleting saved search",
  { jsonResponse: false, authGatedRequest: true },
);

clientFetch("/api/user/saved-searches", {
  method: "DELETE",
  body: JSON.stringify({ searchId: savedSearchId }),
});
```

## useClientFetch Must Not Be in Dependency Arrays
NEVER include `clientFetch` in React `useEffect` dependency arrays. ALWAYS add an `eslint-disable-next-line react-hooks/exhaustive-deps` comment instead.

Example from codebase:
```typescript
// From frontend/src/components/ExportSearchResultsButton.tsx
useEffect(() => {
  // ... uses clientFetch
}, [searchParams]);
// eslint-disable-next-line react-hooks/exhaustive-deps
```

## useSearchParamUpdater for URL Query Parameters
ALWAYS use `useSearchParamUpdater` for URL query parameter manipulation. NEVER use `router.push` directly with query string construction.

Example from codebase:
```typescript
// From frontend/src/components/search/SearchFilterSection.tsx
import { useSearchParamUpdater } from "src/hooks/useSearchParamUpdater";

const { setQueryParam } = useSearchParamUpdater();
const clearAllOptions = () => {
  const clearedSelections = defaultEmptySelection?.size
    ? Array.from(defaultEmptySelection).join(",")
    : "";
  setQueryParam(queryParamKey, clearedSelections);
};
```

## useRouteChange with Suspense Boundary
ALWAYS wrap components that use `useSearchParams` in a `<Suspense>` boundary. ALWAYS use `useRouteChange` via a dedicated wrapper component.

Example from codebase:
```typescript
// From frontend/src/components/Header.tsx
export const RouteChangeWatcher = () => {
  const { refreshIfExpired } = useUser();
  useRouteChange(async () => {
    await refreshIfExpired();
  });
  return <></>;
};

// In parent:
<Suspense>
  <RouteChangeWatcher />
</Suspense>
```

## UserProvider as Central Auth State Manager
ALWAYS manage auth state through `UserProvider` and consume via the `useUser` hook. NEVER implement auth state management in individual components.

Example from codebase:
```typescript
// From frontend/src/services/auth/useUser.tsx
const value = useMemo(
  () => ({
    user: localUser,
    error: userFetchError,
    isLoading,
    refreshUser: getUserSession,
    hasBeenLoggedOut,
    logoutLocalUser,
  }),
  [localUser, userFetchError, isLoading, getUserSession, hasBeenLoggedOut],
);
```

## Early Return for Missing Auth Token
ALWAYS check for `user?.token` before making authenticated API requests. ALWAYS return early if the token is missing.

Example from codebase:
```typescript
// From frontend/src/components/search/SaveSearchModal.tsx
const handleSubmit = useCallback(() => {
  if (!user?.token) {
    return;
  }
  clientFetch("/api/user/saved-searches", {
    method: "POST",
    body: JSON.stringify({ ...savedSearchParams, name: savedSearchName }),
  });
}, [user?.token]);
```

## Auth Timing Constants
ALWAYS define auth timing values in `src/constants/auth.ts`. NEVER hardcode timing values in hooks or components.

Example from codebase:
```typescript
// From frontend/src/constants/auth.ts
export const clientTokenRefreshInterval = 10 * 60 * 1000; // 10 minutes
export const clientTokenExpirationInterval = 15 * 60 * 1000; // 15 minutes
```

## Token Expiration as Milliseconds
ALWAYS store token expiration as a `number` (milliseconds since epoch). NEVER store as a `Date` type. ALWAYS convert JWT `exp` (seconds) by multiplying by 1000.

Example from codebase:
```typescript
// From frontend/src/services/auth/session.ts
export interface UserProfile {
  email?: string;
  token: string;
  expiresAt?: number; // milliseconds since epoch
  user_id: string;
}

// Conversion: expiresAt: exp ? exp * 1000 : undefined
```

## Simplify Conditional Expressions
ALWAYS prefer direct boolean expressions over ternary operators when setting boolean state.

Example from codebase:
```typescript
// From frontend/src/components/OpportunitySaveUserControl.tsx
setSaved(data.type === "save");
```

## Avoid Single-Function Utility Files
NEVER create utility files that contain only a single function. ALWAYS merge into a related utility file.

Example from codebase:
```typescript
// From frontend/src/utils/search/searchUtils.ts
import { convertSearchParamsToProperTypes } from "src/utils/search/searchUtils";
```

---

## Context Enrichment

When generating significant hook code (new custom hook, complex state management), enrich your context:
- Call `get_architecture_section("frontend")` from the `simpler-grants-context` MCP server to understand frontend architectural principles
- Call `get_rule_detail("frontend-services")` for service integration patterns that hooks may consume
- Consult **Compound Knowledge** for indexed documentation on hook patterns and state management conventions

## Related Rules

When working on custom hooks, also consult these related rules:
- **`frontend-services.mdc`** — `useClientFetch`, server-side fetching patterns, auth token handling
- **`frontend-components.mdc`** — how components consume hooks, context guard pattern
- **`cross-domain.mdc`** — boolean naming, general conventions
- **Refactor agent** (`.cursor/agents/refactor.md`) — invoke with `/refactor` for hook extraction, splitting complex hooks, or consolidating duplicated hook logic

## Specialist Validation

When generating or significantly modifying hook code:

**For simple changes (< 20 lines, single hook modification):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new custom hook, refactoring hook logic):**
Invoke `codebase-conventions-reviewer` to validate against hook conventions.

**For complex changes (hooks with async logic, race conditions, complex state):**
Invoke the following specialists (run in parallel where possible):
- `julik-frontend-races-reviewer` — validate async/race condition handling in hook logic
- `code-simplicity-reviewer` — check for unnecessary complexity
- `kieran-typescript-reviewer` — TypeScript-specific quality review
