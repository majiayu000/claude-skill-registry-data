---
name: rule-frontend-components
description: MANDATORY when editing files matching ["frontend/src/components/**/*.tsx", "frontend/src/components/**/*.ts"]. When working on React components in frontend/src/components/
---

# Frontend Components Rules

## Domain-Based Directory Structure
ALWAYS place general-purpose components at the root of `src/components/`. ALWAYS place feature-specific components in a subdirectory named after the feature area. NEVER place reusable components in `src/app/[locale]/` page directories.

Example from codebase:
```typescript
// From frontend/src/components/application/attachments/AttachmentsCard.tsx
// Feature-specific: lives in feature subdirectory
import { AttachmentsCard } from "src/components/application/attachments/AttachmentsCard";

// General-purpose: lives at root
import { SimplerModal } from "src/components/SimplerModal";
```

## No Barrel Files
NEVER create `index.ts` barrel files for re-exporting components. ALWAYS import files by their direct path.

Example from codebase:
```typescript
// From frontend/src/components/application/attachments/AttachmentsCard.tsx
import { AttachmentsCard } from "src/components/application/attachments/AttachmentsCard";
```

## Destructured Props with Type Annotations
ALWAYS destructure props in the component function signature. NEVER accept a `props` object. NEVER use `React.FC<Props>` syntax.

Example from codebase:
```typescript
// From frontend/src/components/search/OpportunityCard.tsx
export const OpportunityCard = ({
  opportunityOverview,
}: {
  opportunityOverview: OpportunityOverviewType;
}) => {
```

## Object Props Over Prop Sprawl
ALWAYS pass whole data objects (or `Pick<>` types) as a single prop when a component needs many fields. NEVER pass 10+ individual props from the same data object.

Example from codebase:
```typescript
// From frontend/src/components/opportunity/OpportunityOverview.tsx
type OpportunityOverviewProps = { opportunity: OpportunityOverviewType };

const OpportunityOverview = ({ opportunity }: OpportunityOverviewProps) => {
  const { agency_code, agency_name, opportunity_id } = opportunity;
};
```

## Server Components by Default
ALWAYS default to server components. ONLY add `"use client"` when client-side interactivity is required. ALWAYS remove `"use client"` when client-side dependencies are removed.

Example from codebase:
```typescript
// From frontend/src/components/search/SearchFilters.tsx
export default async function SearchFilters({
  searchResultsPromise,
}: {
  searchResultsPromise: Promise<SearchAPIResponse>;
}) {
  const searchResults = await searchResultsPromise;
}
```

## Promise Props for Non-Blocking Data Fetching
ALWAYS pass unresolved promises as props from parent pages. ALWAYS name promises `varNamePromise`. ALWAYS await in the child component.

Example from codebase:
```typescript
// From frontend/src/app/[locale]/search/page.tsx
const searchResultsPromise = searchForOpportunities(convertedSearchParams);
return <SearchFilters searchResultsPromise={searchResultsPromise} />;
```

## Shared Types in /types Directory
ALWAYS place shared types in `src/types/` with domain-specific files. ONLY define types inline if they will never be referenced elsewhere.

Example from codebase:
```typescript
// From frontend/src/types/opportunity/opportunityResponseTypes.ts
export type OpportunityOverview = Pick<
  BaseOpportunity,
  "opportunity_title" | "opportunity_id" | "agency_name"
>;
```

## USWDS Utility Classes Over Custom CSS
ALWAYS prefer USWDS utility classes. NEVER use raw hex values or inline styles. ALWAYS use USWDS color tokens.

Example from codebase:
```tsx
// From frontend/src/components/PopoverMenu.tsx
<div className="border border-base-light bg-white shadow-2 radius-md padding-1
               text-no-wrap position-absolute z-top top-full right-0"
     role="menu" ref={menuRef}>
```

## Simpler Wrapper Components
ALWAYS use `SimplerModal` instead of the raw Truss `Modal` component. ALWAYS create wrapper components when a Truss component needs repeated customization.

Example from codebase:
```typescript
// From frontend/src/components/search/SaveSearchModal.tsx
<SimplerModal
  modalRef={modalRef}
  modalId={"save-search"}
  titleText={saved ? undefined : t("title")}
  onClose={onClose}
>
```

## React Context with Guard Hook
ALWAYS include a custom hook that throws if used outside the provider. ALWAYS memoize context values with `useMemo`.

Example from codebase:
```typescript
// From frontend/src/components/LoginModalProvider.tsx
export const useLoginModal = () => {
  const ctx = useContext(LoginModalContext);
  if (ctx === null) {
    throw new Error("useLoginModal must be used within <LoginModalProvider>");
  }
  return ctx;
};
```

## Mandatory i18n for User-Facing Strings
ALWAYS use `useTranslations` (client) or `getTranslations` (server) from `next-intl`. NEVER hardcode user-facing strings.

Example from codebase:
```typescript
// From frontend/src/components/application/AttachmentsCard.tsx
const t = useTranslations("Application.attachments");
return <h3 className="margin-top-4">{t("attachments")}</h3>;
```

## useClientFetch for Client-Side API Calls
ALWAYS use the `useClientFetch` hook for client-side API calls. NEVER use raw `fetch`.

Example from codebase:
```typescript
// From frontend/src/components/search/DeleteSavedSearchModal.tsx
const { clientFetch } = useClientFetch<Response>(
  "Error deleting saved search",
  { jsonResponse: false, authGatedRequest: true },
);
```

## useActionState for Server Actions
ALWAYS use React 19's `useActionState` hook for form submissions using server actions.

Example from codebase:
```typescript
// From frontend/src/components/application/attachments/AttachmentsCardForm.tsx
const [uploadState, uploadFormAction] = useActionState(
  uploadAttachmentAction,
  uploadActionsInitialState satisfies UploadAttachmentActionState,
);
```

## Strict Equality
ALWAYS use `===` and `!==`. NEVER use `==` or `!=`.

Example from codebase:
```typescript
if (value !== null) { /* ... */ }
```

---

## Context Enrichment

When generating significant component code (new component, complex refactor), enrich your context:
- Call `get_architecture_section("frontend")` from the `simpler-grants-context` MCP server to understand frontend architectural principles
- Call `get_rule_detail("frontend-hooks")` for hook patterns that components consume
- Call `get_rule_detail("frontend-i18n")` for i18n integration patterns
- Consult **Compound Knowledge** for indexed documentation on component patterns, USWDS usage, and RSC conventions

## Related Rules

When working on React components, also consult these related rules:
- **`frontend-hooks.mdc`** — `useClientFetch`, `useSearchParamUpdater`, auth state via `useUser`
- **`frontend-i18n.mdc`** — `useTranslations` / `getTranslations`, centralized translation file
- **`frontend-services.mdc`** — `requesterForEndpoint()`, server-side fetching patterns
- **`frontend-tests.mdc`** — jest-axe accessibility, mock patterns, async server component testing
- **`frontend-app-pages.mdc`** — page-level component composition, metadata, layout hierarchy
- **`accessibility.mdc`** — WCAG 2.1 AA / Section 508 compliance, ARIA patterns, focus management, jest-axe requirements
- **`cross-domain.mdc`** — accessibility testing requirement, feature flags
- **Refactor agent** (`.cursor/agents/refactor.md`) — invoke with `/refactor` for component extraction, splitting oversized components, or consolidating duplicated component patterns

## Specialist Validation

When generating or significantly modifying component code:

**For simple changes (< 20 lines, single prop addition):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new component, refactoring component boundaries):**
Invoke `codebase-conventions-reviewer` to validate against component conventions.

**For complex changes (new feature component, complex state management, context providers):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate component boundaries and RSC/client split
- `code-simplicity-reviewer` — check for unnecessary complexity in component logic
- `kieran-typescript-reviewer` — TypeScript-specific quality review

<!-- Hook enforcement: convention-checker validates no inline styles, server-first rendering, no barrel files; accessibility-checker validates a11y patterns -->
