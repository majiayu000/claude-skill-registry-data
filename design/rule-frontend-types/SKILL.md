---
name: rule-frontend-types
description: MANDATORY when editing files matching ["frontend/src/**/*.ts", "frontend/src/**/*.tsx", "frontend/src/types/**/*"]. TypeScript type organization for the Simpler Grants frontend — when to share vs inline types, naming for API response vs UI state types, generics, and discriminated unions. Grounded in frontend/src/types/ conventions.
---

# Frontend Types Rules

## Where Types Live

- **Shared types** → `frontend/src/types/`. Use a domain subfolder (`application/`, `opportunity/`, `search/`, `attachment/`, `grantor/`) when the slice has multiple related files; otherwise a flat `<feature>Types.ts` file at the root of `types/`.
- **Component-local types** (props, internal state used by exactly one component) → inline in the component file or a sibling `Component.types.ts`. NEVER pollute `src/types/` with single-use prop types.
- **Ambient/global declarations** → `*.d.ts` (e.g., `i18n.d.ts`).

> Decision rule: if a type is imported by 2+ files, or crosses a feature boundary, promote it to `src/types/`.

## File Naming

- `camelCase` ending in `Types.ts` for shared modules: `opportunityTypes.ts`, `apiResponseTypes.ts`.
- `*ResponseTypes.ts` specifically for API response shapes: `applicationResponseTypes.ts`, `competitionsResponseTypes.ts`, `formResponseTypes.ts`.
- `*.d.ts` for ambient declarations only.
- AVOID `index.ts` barrels unless a domain folder genuinely needs one.

## Type Identifier Naming

ALWAYS use **PascalCase** for `type` and `interface` (`QueryParamData`, `PaginationInfo`, `APIResponse`).

Suffix conventions:
- `*Response` — raw API response envelopes (`OpportunityResponse`)
- `*Request` / `*Params` — outbound request payloads or query params (`QueryParamData`)
- `*Props` — React component props (`ErrorProps`)
- `*State` — reducer/store/local state shapes
- `*Dto` is **not** used in this codebase — do NOT introduce it.

NEVER prefix interfaces with `I`. NEVER prefix type aliases with `T`. Booleans use `is*`, `has*`, `should*`.

## Property Naming — Wire Format vs Internal

- **API response/request types mirror the backend exactly using `snake_case`** (`page_offset`, `pagination_info`, `status_code`). Do NOT camelCase API contract types — it breaks the wire mapping.
- **All other types use `camelCase`** properties.
- When mapping API data into UI state, do the snake→camel conversion at the boundary (fetcher/service layer) and define a separate UI type — NEVER reuse the response type as the UI type.

```ts
// Wire (snake_case) — mirrors backend
export interface PaginationInfo {
  page_offset: number;
  page_size: number;
  total_pages: number;
  sort_direction: "asc" | "desc";
}

// UI (camelCase) — converted at the service boundary
export interface Pagination {
  pageOffset: number;
  pageSize: number;
  totalPages: number;
  sortDirection: SortDirection;
}
```

## `type` vs `interface`

- DEFAULT to `interface` for object shapes that may be extended (props, response envelopes — matches existing usage like `interface APIResponse`, `interface ErrorProps`).
- USE `type` for unions, intersections, mapped/conditional types, tuples, and function signatures.
- NEVER mix both for the same concept.

## Generics

PREFER a properly generic API envelope for new code:

```ts
export interface APIResponse<TData = unknown> {
  data: TData;
  pagination_info?: PaginationInfo;
  warnings?: ApiMessage[];
  errors?: ApiMessage[];
  status_code: number;
}
```

> Today's `APIResponse` uses `data: unknown[] | object`. New code should pass an explicit `TData`, and existing call sites should be tightened opportunistically.

- Single-letter generics only when meaning is obvious (`T`, `K`, `V`). Otherwise use descriptive names: `TData`, `TParams`, `TError`.
- CONSTRAIN generics (`<T extends object>`) rather than leaving them open when shape matters.
- DO NOT reach for generics when a plain type works — avoid generic gymnastics.

## Discriminated Unions

PREFER explicit discriminants over optional-field flag soup:

```ts
type FetchResult<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: FrontendErrorDetails }
  | { status: "loading" };

function render<T>(result: FetchResult<T>) {
  switch (result.status) {
    case "success": return renderData(result.data);
    case "error":   return renderError(result.error);
    case "loading": return renderSpinner();
    default: {
      const _exhaustive: never = result;
      return _exhaustive;
    }
  }
}
```

- Use a `kind` or `status` literal string as the discriminant.
- Exhaustively `switch` with a `never` default for safety.
- NEVER overload one interface with mutually exclusive optional fields when a union expresses intent more clearly.

## Enums vs Union Literals

- Existing code uses `enum Breakpoints` for fixed design-token sets — fine when values are referenced by name across many files.
- For most other finite sets (status, sort direction), PREFER **string literal unions**: `type SortDirection = "asc" | "desc"`. They tree-shake and serialize naturally.
- NEVER introduce numeric enums.

## Imports & Re-exports

- Import shared types via the `src/types/...` path (match the alias configured in `tsconfig.json` — verify before writing examples).
- USE `import type { … }` for type-only imports to keep runtime bundles clean.
- AVOID deep barrel files; import directly from the specific module.

```ts
import type { APIResponse, PaginationInfo } from "src/types/apiResponseTypes";
import type { ErrorProps } from "src/types/uiTypes";
```

## Ambient & Third-Party Augmentation

Module augmentation (e.g., extending `next-intl`, `NewRelic`, `next/server`) belongs in a `*.d.ts` at `src/types/` — see `intl.ts`, `newRelic.ts`, `i18n.d.ts` for the established pattern. ALWAYS include a top-of-file comment explaining what is being augmented and why.

## Anti-Patterns

- NO `any` — use `unknown` and narrow.
- NO `as` casts to bypass type errors; fix the type or use a type guard.
- NO duplicating an API response type as a UI type — define both and map at the boundary.
- NO single-use prop types in `src/types/`.
- NO `I`-prefixed interfaces, no `T`-prefixed type aliases.
- NO camelCasing API contract fields.
- NO numeric enums.
- NO giant union of optional fields where a discriminated union belongs.

---

## Related Rules

- **`frontend-services.mdc`** — service-layer boundary where snake→camel mapping happens
- **`frontend-components.mdc`** — where `*Props` types are declared and consumed
- **`api-routes.mdc`** — backend wire format that response types must mirror

## Specialist Validation

**Simple changes (add a field, new union literal):** No specialist needed.

**Moderate changes (new shared type module, new response envelope):** Invoke `codebase-conventions-reviewer`.

**Complex changes (new generic API envelope, refactoring discriminated unions, ambient module augmentation):** Invoke in parallel:
- `kieran-typescript-reviewer` — TypeScript-specific quality review
- `architecture-strategist` — validate type boundaries and module placement
