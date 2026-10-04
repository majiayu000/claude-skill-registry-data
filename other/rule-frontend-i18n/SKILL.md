---
name: rule-frontend-i18n
description: MANDATORY when editing files matching ["frontend/src/i18n/**/*"]. When working on internationalization in frontend/src/i18n/
---

# Frontend i18n Rules

## Single Centralized Translation File
ALWAYS add all user-facing text to `frontend/src/i18n/messages/en/index.ts`. NEVER create separate translation files per page or feature.

Example from codebase:
```typescript
// From frontend/src/i18n/messages/en/index.ts
export const messages = {
  Events: {
    pageTitle: "Events | Simpler.Grants.gov",
    header: "Events",
    upcoming: {
      title: "Upcoming Events",
      header: "Spring 2025 Collaborative Coding Challenge",
    },
  },
};
```

## English-Only Single Locale
ALWAYS add translations only to `messages/en/index.ts`. NEVER add non-English translation files unless the project formally adopts multi-language support.

## Content Directly in Translation Values
ALWAYS store long-form content directly as translation string values. NEVER use separate content files, Markdown files, or a CMS.

Example from codebase:
```typescript
// From frontend/src/i18n/messages/en/index.ts
codingChallenge: {
  title: "Collaborative Coding Challenge",
  descriptionP1:
    "The Simpler.Grants.gov Collaborative Coding Challenge is an entirely virtual interactive event.",
  link: "Read about the Spring 2025 Coding Challenge",
},
```

## camelCase Translation Keys
ALWAYS use camelCase for translation key names. NEVER use snake_case. The sole exception is keys that must match API enum values (e.g., `application_created`).

Example from codebase:
```typescript
// From frontend/src/i18n/messages/en/index.ts
ErrorPages: {
  pageNotFound: {
    title: "Page not found",
  },
},
```

## PascalCase Top-Level Namespace Keys
ALWAYS use PascalCase for top-level namespace keys. ALWAYS use camelCase for all nested keys below the top level.

Example from codebase:
```typescript
// From frontend/src/i18n/messages/en/index.ts
Header: {
  navLinks: {
    home: "Home",
    roadmap: "Roadmap",
    search: "Search",
    login: "Sign in",
  },
  title: "Simpler.Grants.gov",
},
```

## Page Title Format
ALWAYS format page titles as `<Page Name> | Simpler.Grants.gov` under a `pageTitle` key. ALWAYS set via `generateMetadata` using `getTranslations`.

Example from codebase:
```typescript
// From frontend/src/app/[locale]/settings/page.tsx
export async function generateMetadata({ params }: LocalizedPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale });
  const meta: Metadata = {
    title: t("Settings.pageTitle"),
    description: t("Index.metaDescription"),
  };
  return meta;
}
```

## Namespaced Translation Hook with Narrow Scoping
ALWAYS scope `useTranslations` as narrowly as practical. ALWAYS use `getTranslations` for async server components.

Example from codebase:
```typescript
// From frontend/src/components/events/EventsCoding.tsx
export default function EventsCoding() {
  const t = useTranslations("Events.codingChallenge");
  return (
    <h2>{t("title")}</h2>
  );
}
```

## Rich Text via t.rich()
ALWAYS use `t.rich()` when a translation string contains inline HTML elements. NEVER split sentences across multiple translation keys.

Example from codebase:
```tsx
// From frontend/src/components/BookmarkBanner.tsx
{t.rich("technicalSupportMessage", {
  mailToGrants: (content) => (
    <a href="mailto:simpler@grants.gov">{content}</a>
  ),
})}
```

## useMessages() for Dynamic Key Iteration
ALWAYS use `useMessages()` to iterate over structured lists of translated items. ALWAYS update `intlMocks.ts` to mirror the structure when adding new usage.

Example from codebase:
```tsx
// From frontend/src/components/roadmap/RoadmapTimeline.tsx
const t = useTranslations("Roadmap.sections.timeline");
const messages = useMessages() as unknown as IntlMessages;
const { contentItems = {} } = messages.Roadmap.sections.timeline;

{Object.keys(contentItems).map((key) => (
  <h3>{t(`contentItems.${key}.date`)}</h3>
))}
```

## Atomic Translation Key Restructuring
ALWAYS update the translation namespace and all references in one atomic PR when renaming or restructuring. NEVER split namespace renames across multiple PRs.

## No Numbered Key Suffixes
NEVER use numbered suffixes (`title_1`, `paragraph_2`). ALWAYS use semantically meaningful names.

## No defaultValue in Translation Calls
NEVER pass `defaultValue` to `t()` calls. ALWAYS ensure the key exists in `messages/en/index.ts`.

## Import from next-intl Only
ALWAYS import `useTranslations` from `next-intl`. NEVER import from `use-intl` directly.

---

## Context Enrichment

When generating significant i18n changes (new namespace, restructuring keys), enrich your context:
- Call `get_rule_detail("frontend-components")` from the `simpler-grants-context` MCP server to understand how components consume translations
- Consult **Compound Knowledge** for indexed documentation on i18n key naming precedents and translation structure patterns

## Related Rules

When working on internationalization, also consult these related rules:
- **`frontend-components.mdc`** — `useTranslations` in client components, `getTranslations` in server components
- **`cross-domain.mdc`** — general naming conventions

## Specialist Validation

When generating or significantly modifying i18n code:

**For simple changes (adding a few translation keys):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new namespace, restructuring keys):**
Invoke `pattern-recognition-specialist` to check for key naming consistency and duplication.

**For complex changes (namespace migration, atomic key restructuring across components):**
Invoke the following specialists (run in parallel where possible):
- `pattern-recognition-specialist` — validate key naming consistency, detect duplicate translations
- `codebase-conventions-reviewer` — validate PascalCase/camelCase conventions
- `kieran-typescript-reviewer` — TypeScript-specific quality review
