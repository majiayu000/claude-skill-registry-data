---
name: design-harden
description: "Make interfaces bulletproof — error boundaries, loading states, empty states, text overflow, i18n readiness, offline handling, and every edge case that breaks in production. Triggers: 'harden the UI', 'add error states', 'handle edge cases', 'add loading states'."
version: "1.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous UI hardening agent. You scan every component in the codebase, find every missing edge case handler, and add it. You do not ask questions. You infer the appropriate error, loading, and empty state patterns from the existing codebase and fill every gap.

Do NOT ask the user questions. Scan the code, find every missing state, implement it.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific components, pages, or hardening categories (e.g., "error handling only", "dashboard page", "loading states"). If not provided, perform a full hardening pass.

---

## PHASE 1: CODEBASE RECONNAISSANCE

### 1.1 Identify Stack and Patterns
- Read package.json, pubspec.yaml, build.gradle, or equivalent.
- Identify UI framework: React, Vue, Svelte, Angular, Flutter, SwiftUI, Jetpack Compose.
- Identify state management: Redux, Zustand, Riverpod, Provider, Bloc, TCA, MVI.
- Identify data fetching: React Query, SWR, Apollo, Dio, Retrofit, URLSession, custom.
- Identify existing error handling patterns: error boundaries, try/catch wrappers, Result types.

### 1.2 Catalog All Interactive Components
- List every component that:
  - Fetches data from an API or database.
  - Accepts user input (forms, text fields, selectors).
  - Displays dynamic content (lists, grids, tables, charts).
  - Navigates between screens or pages.
  - Performs mutations (create, update, delete).
- For each component, note which states it currently handles: loading, error, empty, success, partial.

### 1.3 Identify Gaps
- Flag components that have data fetching but no loading state.
- Flag components that have data fetching but no error state.
- Flag components that display lists but no empty state.
- Flag forms with no validation or error feedback.
- Flag mutations with no loading indicator or optimistic update.
- Rank gaps by user impact (how likely is a user to encounter this state?).

---

## PHASE 2: ERROR HANDLING

### 2.1 Error Boundaries (React)
- Verify every route/page is wrapped in an error boundary.
- If no error boundaries exist, add a root-level error boundary and per-feature boundaries:
  ```tsx
  // Granular error boundary with recovery
  <ErrorBoundary
    fallback={({ error, resetErrorBoundary }) => (
      <ErrorFallback
        message="Something went wrong loading this section."
        onRetry={resetErrorBoundary}
      />
    )}
  >
    <FeatureComponent />
  </ErrorBoundary>
  ```
- Error fallbacks should include: a human-readable message, a retry button, and optionally a "report issue" link.
- NEVER show raw error messages, stack traces, or internal details to the user.

### 2.2 Async Error Handling
- Every async operation (fetch, mutation, file read) must be wrapped in try/catch.
- Error handling must be specific — catch different error types and show appropriate messages:
  - Network error: "Unable to connect. Check your internet connection and try again."
  - 404: "This content is no longer available."
  - 403: "You don't have permission to view this."
  - 429: "Too many requests. Please wait a moment and try again."
  - 500: "Something went wrong on our end. Please try again later."
  - Timeout: "The request took too long. Please try again."
- Implement retry logic with exponential backoff for transient errors:
  ```typescript
  async function fetchWithRetry(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
    for (let i = 0; i < maxRetries; i++) {
      try { return await fn(); }
      catch (e) {
        if (i === maxRetries - 1 || !isTransient(e)) throw e;
        await sleep(Math.pow(2, i) * 1000);
      }
    }
  }
  ```

### 2.3 Graceful Degradation
- If a non-critical section fails, the rest of the page should still render.
- Sidebar widgets, recommendation sections, and analytics should degrade silently.
- Critical sections (main content, navigation) should show an error with retry.
- Never let one failed API call take down the entire page.

### 2.4 Flutter Error Handling
- Wrap async calls in try/catch with proper error state management.
- Use `ErrorWidget.builder` for custom error widgets in debug and release mode.
- Implement `runZonedGuarded` for catching uncaught async errors.
- Use `Result` or `Either` types for typed error handling in repositories.

### 2.5 Form Validation
- Every form field must have validation rules that run on blur and on submit.
- Show inline error messages below the field (not alerts/toasts).
- Error messages must be specific: "Email must include @" not "Invalid input."
- Disable submit button while form has errors or submission is in progress.
- Preserve form state on error — never clear the form after a failed submission.

---

## PHASE 3: LOADING STATES

### 3.1 Skeleton Screens (Not Spinners)
- Replace generic spinners with skeleton screens that mirror the content layout:
  ```tsx
  // Bad: generic spinner
  {isLoading && <Spinner />}

  // Good: content-shaped skeleton
  {isLoading && (
    <div class="card-skeleton">
      <div class="skeleton-image" />
      <div class="skeleton-line w-3/4" />
      <div class="skeleton-line w-1/2" />
    </div>
  )}
  ```
- Skeleton styles should use a shimmer animation:
  ```css
  .skeleton {
    background: linear-gradient(
      90deg,
      oklch(0.92 0 0) 25%,
      oklch(0.96 0 0) 50%,
      oklch(0.92 0 0) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }
  @keyframes shimmer {
    from { background-position: 200% 0; }
    to { background-position: -200% 0; }
  }
  ```

### 3.2 Suspense Boundaries (React)
- Wrap lazy-loaded components in Suspense with appropriate fallbacks.
- Nest Suspense boundaries: page-level loading for route changes, section-level for deferred content.
- Use `startTransition` for non-urgent updates to avoid unnecessary loading states.

### 3.3 Loading Indicators for Mutations
- Every button that triggers a mutation should show a loading state:
  - Disable the button.
  - Replace text with a spinner or "Saving..." text.
  - Prevent double-submission.
- For long-running operations (file upload, batch processing), show a progress indicator.

### 3.4 Optimistic Updates
- For mutations where the outcome is predictable (toggle, like, delete), update UI immediately:
  ```typescript
  // Optimistic: update cache immediately, revert on error
  const previousData = queryClient.getQueryData(key);
  queryClient.setQueryData(key, optimisticData);
  try {
    await mutation(data);
  } catch {
    queryClient.setQueryData(key, previousData);
    showToast("Failed to save. Please try again.");
  }
  ```
- Show a subtle sync indicator for optimistic updates (small icon, not a toast).

### 3.5 Flutter Loading States
- Use `Shimmer` package or custom `AnimatedContainer` for skeleton screens.
- Implement loading state in state management (Riverpod AsyncValue, Bloc states).
- Never use bare `CircularProgressIndicator()` — always wrap in a meaningful layout.
- For lists, show 3-5 skeleton items matching the list item shape.

---

## PHASE 4: EMPTY STATES

### 4.1 Empty State Design
- Every list, grid, table, or collection must handle the empty case.
- Empty states should include:
  - An illustration or icon (not just text).
  - A descriptive message explaining why it is empty.
  - A primary action CTA (create first item, adjust filters, etc.).
  ```tsx
  <EmptyState
    icon={<SearchIcon />}
    title="No results found"
    description="Try adjusting your filters or search terms."
    action={<Button onClick={clearFilters}>Clear filters</Button>}
  />
  ```

### 4.2 Contextual Empty States
- Distinguish between different empty reasons:
  - **First use**: "Welcome! Create your first project to get started." (encouraging, with CTA)
  - **No results**: "No items match your filters." (with clear filters action)
  - **Deleted all**: "All items have been archived." (with undo or view archive action)
  - **Permission**: "You don't have access to this content." (with request access action)

### 4.3 Partial Empty States
- Tables with no data but existing columns should show an empty row message, not a blank table.
- Charts with no data should show axes with a "No data for this period" message.
- Dashboards should show placeholder cards, not collapsed sections.

### 4.4 Flutter Empty States
- Create a reusable `EmptyStateWidget` with icon, title, description, and optional action.
- Use `AnimatedSwitcher` to transition between loading, content, and empty states smoothly.
- Verify `ListView.builder` with `itemCount: 0` shows an empty state, not a blank screen.

---

## PHASE 5: TEXT OVERFLOW AND CONTENT RESILIENCE

### 5.1 Text Overflow Handling
- Every text element that displays dynamic content must handle overflow:
  ```css
  /* Single line truncation */
  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Multi-line clamp */
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  ```
- Headings in cards and list items should truncate, not wrap infinitely.
- User-generated content must have max-width constraints.

### 5.2 Long Content Stress Test
- Mentally test every text field with:
  - A single character ("A").
  - A very long string with no spaces ("Aaaaaaaaaaaaaaaaaa...").
  - A very long string with spaces (full paragraph).
  - Unicode characters, emoji, RTL text.
  - HTML entities (should be escaped, not rendered).
- Fix any layout that breaks under these conditions.

### 5.3 Word Break Handling
- For user-generated content areas, add word-break handling:
  ```css
  .user-content {
    overflow-wrap: break-word;
    word-break: break-word;
    hyphens: auto;
  }
  ```
- URLs and file paths should break with `word-break: break-all` in constrained containers.

### 5.4 Number and Date Formatting
- Large numbers should use locale-aware formatting (1,234,567 not 1234567).
- Dates should use relative time for recent ("2 hours ago") and formatted for older.
- Currency should always show the correct number of decimal places.
- Verify number formatting does not break layout (e.g., "$1,234,567.89" in a narrow column).

### 5.5 Flutter Text Resilience
- Use `maxLines` and `overflow: TextOverflow.ellipsis` on all dynamic text.
- Verify `Text` widgets inside `Row` are wrapped in `Expanded` or `Flexible` to prevent overflow.
- Use `FittedBox` sparingly for headings that must fit a constrained width.

---

## PHASE 6: I18N READINESS

### 6.1 String Externalization
- Scan for hardcoded user-facing strings in component files.
- Flag strings that should be in a localization file (l10n, i18n, intl, arb).
- Do NOT move all strings — flag them and create a task list for future extraction.
- Ensure string templates use parameterized interpolation, not concatenation:
  ```typescript
  // Bad: "Welcome " + userName + "!"
  // Good: t("welcome", { name: userName })
  ```

### 6.2 RTL Support Readiness
- Check for directional CSS properties that should use logical properties:
  ```css
  /* Physical (breaks RTL) */
  margin-left: 16px;
  padding-right: 8px;
  text-align: left;

  /* Logical (RTL-safe) */
  margin-inline-start: 16px;
  padding-inline-end: 8px;
  text-align: start;
  ```
- Flag all physical direction properties for future RTL conversion.
- Verify icons with directional meaning (arrows, chevrons) can be mirrored.

### 6.3 Pluralization and Gender
- Check for naive pluralization ("1 items", "item(s)").
- Verify date/time formatting uses Intl API or equivalent.
- Check number formatting uses locale-aware separators.

### 6.4 Text Expansion
- Verify layouts can handle text expansion (German is ~30% longer than English).
- Buttons with text should not have fixed widths.
- Navigation labels should accommodate longer translations.

---

## PHASE 7: OFFLINE AND CONNECTIVITY

### 7.1 Offline Detection
- Verify the app detects connectivity changes.
- Web: `navigator.onLine` + `online`/`offline` events.
- Mobile: platform connectivity APIs (connectivity_plus for Flutter).
- Show a non-intrusive banner when offline, not a blocking modal.

### 7.2 Offline-First Patterns
- If the app uses any local caching (service worker, Hive, SQLite, AsyncStorage):
  - Verify cached data is shown when offline instead of an error.
  - Show a "Last updated X ago" indicator when serving stale data.
  - Queue mutations for sync when connectivity returns.
- If no caching exists, flag it as an improvement opportunity.

### 7.3 Low Bandwidth Handling
- Verify images have loading="lazy" (web) or equivalent lazy loading.
- Check for unnecessary auto-playing videos or large asset downloads.
- Verify API calls are not duplicated (no fetching the same data twice on page load).

### 7.4 Service Worker (Web)
- If a service worker exists, verify it caches critical assets (HTML, CSS, JS, fonts).
- Verify stale-while-revalidate strategy for API responses.
- If no service worker exists and the app would benefit from offline support, flag it.

---

## PHASE 8: ACCESSIBILITY HARDENING

### 8.1 Interactive Element Hardening
- Every interactive element must be keyboard accessible.
- Custom interactive elements must have appropriate ARIA roles.
- Modals must trap focus and return focus on close.
- Dropdown menus must support arrow key navigation.

### 8.2 Screen Reader Hardening
- Images must have meaningful alt text (not "image" or "photo").
- Icon-only buttons must have `aria-label`.
- Dynamic content updates must use `aria-live` regions.
- Form errors must be associated with fields via `aria-describedby`.

### 8.3 Motion Sensitivity
- Verify `prefers-reduced-motion` is respected for all animations.
- Auto-playing carousels must have pause controls.
- Parallax effects must have reduced-motion alternatives.

### 8.4 Touch Target Sizing
- All interactive elements must be at least 44x44px (48x48px preferred).
- Spacing between touch targets must be at least 8px.
- Small interactive elements (close buttons, checkboxes) must have expanded hit areas:
  ```css
  .small-button::before {
    content: '';
    position: absolute;
    inset: -8px;
  }
  ```

---

## PHASE 9: APPLY HARDENING

### 9.1 Execution Strategy
- Prioritize fixes by user impact:
  1. Missing error handling on data fetching (crashes in production).
  2. Missing loading states (confusing blank screens).
  3. Text overflow issues (broken layouts).
  4. Missing empty states (confusing blank sections).
  5. Accessibility gaps (exclusion of users).
  6. i18n and offline (future readiness).
- For each fix, follow existing patterns in the codebase. Do not introduce new libraries or paradigms.
- If the codebase has no existing pattern for a state (e.g., no error handling anywhere), create a minimal, reusable pattern and apply it consistently.

### 9.2 Create Reusable Utilities
When adding multiple instances of the same pattern, create a shared utility:
- `ErrorFallback` component for error states.
- `Skeleton` component for loading states.
- `EmptyState` component for empty states.
- `withRetry` or `fetchWithRetry` utility for retry logic.
Then use these utilities across all instances.

---

## PHASE 10: SELF-HEALING VALIDATION

### 10.1 Build Verification
- Run the project build command.
- If build fails, revert the last change and re-run.
- Run linter and fix any new warnings.

### 10.2 Type Safety Check
- If TypeScript/Dart/Kotlin, verify no new type errors were introduced.
- Verify error types are properly typed (not `catch(e: any)`).
- Verify loading/error state types are exhaustive in switch/match statements.

### 10.3 Test Verification
- Run existing tests. Fix any that break due to hardening changes.
- If tests exist for components that were modified, verify they still pass.
- Do not remove or weaken existing test assertions.

### 10.4 State Coverage Check
- For every component modified, verify it now handles: loading, error, empty, and success states.
- List any components that still have gaps (with justification for why they were skipped).

---

## PHASE 11: TELEMETRY AND REPORT

### 11.1 Hardening Summary
Output a summary table:

```
## Hardening Summary

| Category          | Gaps Found | Fixed | Deferred |
|-------------------|-----------|-------|----------|
| Error Boundaries  |           |       |          |
| Async Errors      |           |       |          |
| Loading States    |           |       |          |
| Empty States      |           |       |          |
| Text Overflow     |           |       |          |
| Form Validation   |           |       |          |
| i18n Readiness    |           |       |          |
| Offline           |           |       |          |
| Accessibility     |           |       |          |
| **Total**         |           |       |          |
```

### 11.2 State Coverage Matrix
For each major component, show its state coverage:

```
| Component     | Loading | Error | Empty | Offline | a11y |
|---------------|---------|-------|-------|---------|------|
| UserList      | [x]     | [x]   | [x]   | [ ]     | [x]  |
| Dashboard     | [x]     | [x]   | [x]   | [ ]     | [x]  |
```

### 11.3 Reusable Utilities Created
List any shared components or utilities created during hardening.

### 11.4 Deferred Items
List items not addressed with reasons and recommended follow-up actions.

### 11.5 Self-Evolution Notes
- Which categories had the most gaps? (Focus future hardening here.)
- Were there systematic patterns? (e.g., "No component has error handling" suggests missing conventions.)
- What infrastructure improvements would prevent these gaps? (error boundary wrapper in layout, global error handler, etc.)
- Recommend running `/design-polish` after hardening to ensure new states match the design language.
