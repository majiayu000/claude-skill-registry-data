---
name: odin-component-architecture
description: Project conventions for reusable UI components, file placement, naming, and deduplication in Odin Reporters App. Use when adding or editing screens, components, hooks, API clients, interceptors, server-state caching, client state, stores, forms, persistence, storage, security, API authoring, performance, ANRs, crashes, startup, Fast Refresh, feature completion, shared logic, or reviewing the app's architecture.
---

# Odin component architecture

Apply these conventions to new and touched code in this existing app. Do not reorganize unrelated files as part of a feature. This skill supplies project-specific rules alongside `expo-ui`, `expo-design-system`, and `expo-router`; `expo-project-structure` supplies a new-project skeleton, not a migration requirement.

## Inspect and reuse first

Before adding a file, search `src/components`, `src/hooks`, `src/lib`, and the relevant screen for an existing implementation and its callers. Read the closest match. Extend its supported variants or compose it before creating an overlapping implementation. Reuse existing `ThemedText`, `ThemedView`, `ExternalLink`, and other suitable components at their current paths.

## Components before screens

- Screens compose app-owned UI components. Implement a new app control (button, input, select, toggle, sheet, row, badge, or similar reusable visual element) in a component file first, then use it in the screen. Do not recreate its styling and interaction inline at each call site.
- New generic app controls belong in `src/components/ui/`, including thin adapters over native controls when they provide a stable app API, shared defaults, accessibility, or styling. Establish these controls from their first real use; do not wait for a second screen to copy them.
- Read `../expo-ui/SKILL.md` before selecting the underlying native control. Prefer the suitable native implementation behind the app component. Preserve its accessibility, native behavior, and platform requirements; do not reimplement the widget just to own its API.
- Basic layout primitives such as `View`, `ScrollView`, and virtualized list containers may remain directly in screens. Router layouts, headers, links, and providers may also use framework APIs directly. A wrapper that adds no app policy or useful boundary is unnecessary.
- Feature-specific compositions stay with their screen until another screen needs the same concept. Extract meaningful sections into named components; do not turn every layout node into a separate file.
- Fix shared appearance or behavior in the owning component so all consumers benefit. Use typed variants for supported differences, not copied components or caller-specific color overrides.

## File placement

Use these locations as responsibilities, creating a directory only when it has real content:

| Location | Responsibility |
| --- | --- |
| `src/app/` | Expo Router routes, layouts, and framework special files only. Route files handle route parameters/navigation and compose screen components. |
| `src/screens/<screen-name>/` | Screen body and private components/hooks/helpers when a screen needs extraction. Use `<screen-name>-screen.tsx` and `components/` for private UI. |
| `src/components/ui/` | New domain-independent app UI controls and primitives. |
| `src/components/` | Components shared across screens, including existing primitives at their current paths. |
| `src/hooks/` | Hooks reused across screens; screen-specific hooks remain colocated. |
| `src/lib/` | Shared non-UI helpers and integrations; name files by purpose, following the existing `cn.ts` convention. |
| `src/constants/` | Shared static app values and the existing `theme.ts`. |
| `src/global.css` | Existing Tailwind/Uniwind global styles and CSS tokens. |

Keep tests, types, and utilities out of `src/app/`. Keep component props beside their component; extract a shared type only when multiple consumers need it. Do not introduce parallel `common/`, `shared/`, `helpers/`, or `utils/` buckets for responsibilities already owned by these folders. Preserve existing component paths unless a requested refactor requires moving them, and update all callers when moving.

## Naming and imports

- Files and ordinary folders use descriptive kebab-case: `report-card.tsx`, `report-details/`, `use-report-filters.ts`. Preserve Expo Router's required names such as `_layout.tsx`, `index.tsx`, `[id].tsx`, and route groups.
- Components and types use PascalCase (`ReportCard`, `ReportCardProps`); hooks use `use` plus camelCase (`useReportFilters`); functions and variables use camelCase.
- Prefer named exports for reusable components. Keep default exports where Expo Router requires them.
- Prefer descriptive files over generic `helpers.ts`, `data.ts`, `common.tsx`, or numbered alternatives such as `button-v2.tsx`.
- Use `@/` imports across folders, following `tsconfig.json`; short relative imports within a component or screen are fine. Avoid a global barrel exporting every component or library module, which can hide cycles and platform imports.
- Use `.ios.tsx`, `.android.tsx`, or `.web.tsx` when platform implementations differ materially. Keep their public props compatible and provide the appropriate default implementation.

## Component boundaries and shared logic

- Generic UI receives data and callbacks through typed props. It must not fetch feature data, import screens/routes, or depend on feature-specific stores. Screens or their hooks own orchestration.
- Dependencies flow from routes to screens to shared components/hooks/helpers. Shared modules must not import route or screen modules; avoid circular imports.
- Prefer composition for optional content and small intent-based variants for appearance. Avoid many boolean flags or a universal component that understands unrelated screens.
- Preserve labels, disabled/loading behavior, focus/ref needs, and accessibility props supported by the underlying control. A shared wrapper must not swallow them.
- Centralize repeated business rules, formatting, and data access at the narrowest shared owner. Similar-looking JSX with different meaning does not automatically need one abstraction.
- Extend the current styling system: `src/constants/theme.ts`, `src/global.css`, and existing theme hooks. Do not add a competing `src/theme/` system or manually duplicate the same token in TS and CSS. If a value must cross systems, define an explicit source and derive/read it through the existing styling integration.
- Keep styles beside the component and use existing tokens/utilities. Shared control identity belongs inside the control; callers may adjust surrounding layout.

## API clients and server state

For network requests, authentication, interceptors, query/mutation hooks, or caching, read [API and server-state conventions](references/api-and-server-state.md) and `../expo-data-fetching/SKILL.md`. Route requests through one shared client, keep endpoints separate from UI, and follow the installed fetching/cache library's version-specific best practices.

## State management and forms

For local/shared state, stores, providers, persisted preferences/drafts, or forms, read [State ownership and forms](references/state-and-forms.md). Keep state at its narrowest owner; separate server cache, client state, navigation parameters, and editable drafts.

## Storage and security

For AsyncStorage, MMKV, SecureStore, SQLite, persisted stores/caches, credentials, offline files, or security-sensitive work, read [Storage and security](references/storage-and-security.md). Choose storage by sensitivity and access pattern, centralize adapters, and apply the relevant session and security boundaries.

## Feature quality

When implementing or reviewing a feature, read [Feature completion and adjacent concerns](references/feature-quality.md) and load only the domain skills relevant to that feature. It covers error recovery, permissions/media lifecycle, accessibility, dependency choices, and meaningful verification.

## API authoring and performance

For server endpoints or API contract changes, read [API authoring](references/api-authoring.md); for client calls, use the API client reference above. For optimization work, read [Performance](references/performance.md): establish a baseline, fix the measured bottleneck, and verify the result.

## Reliability and lifecycle

For ANRs, crashes, freezes, cold/warm/hot startup, app resume, process restoration, Fast Refresh, or release-health work, read [Reliability and lifecycle](references/reliability-and-lifecycle.md). Separate development reload behavior from production lifecycle, diagnose with appropriate traces, and verify representative builds.

## Completion checks

For code changes, inspect the diff for duplicate controls, copied business rules, misplaced route helpers, cycles, and inconsistent names. Check every affected consumer after changing a shared API. Run the project's relevant lint/type checks and, for behavior changes, focused tests or device checks covering affected states/platforms. Documentation-only edits need link and skill validation, not an app build.

Do not bulk-refactor the app just because this skill was loaded. Apply it incrementally within the user's requested work.
