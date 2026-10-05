---
name: system-patterns
description: Architect composite UI patterns that assemble components into coherent features. Use when building forms, validation, error handling, multi-step flows, navigation, breadcrumbs, active states, deep linking, tables, lists, cards, sorting, filtering, pagination, empty/loading/error states, feedback systems, confirmations, progress, optimistic updates, page layouts, sidebar+main structures, dashboard grids, responsive stacking, or content density. Also triggers for "how should this form validate", "where should errors show", "toast or inline", "how to structure this dashboard", "mobile navigation", workflow coherence, complexity cost, feature accretion, or how components work together. Does NOT cover button labels, command names, feature/product names, or UI terminology (use system-naming), component APIs (use system-components), token architecture (use system-tokens), animation values (use surface-motion), or platform quirks (use surface-details).
---

# Patterns

Composite UI patterns that assemble components into features. system-components builds the atoms. This skill builds the molecules, organisms, and templates.

This is the layer between "I have well-structured components" and "I have a well-structured product." It prevents the common failure mode of correct components wired into incoherent features.

For the shared design philosophy, see `references/design-philosophy.md`.

**Apply this when composing components into larger features or building pages.** For button labels, feature names, product names, and shared terminology, use system-naming. For accessibility across all skills, see `references/accessibility.md`. For multi-skill task sequencing, see `references/composition.md`.

---

## Coherence and Complexity

Good product patterns preserve coherence as features accumulate. Every addition creates new relationships between states, transitions, permissions, errors, empty cases, navigation, and feedback. Treat that complexity as a cost.

Before adding or changing a feature, identify:

- The existing pattern it extends.
- The user task it improves.
- The states and transitions it adds.
- The complexity it removes, hides, or justifies.

If a feature duplicates an existing pattern, contradicts established behaviour, or adds states without a recovery path, stop and simplify the pattern before building more UI.

Prefer removing, merging, or progressively disclosing secondary controls over adding another visible branch to the workflow. A feature that is technically correct but makes the product harder to hold in someone's head is a pattern failure.

---

## 1. Form Patterns

### Validation timing

Three strategies, each suited to different contexts:

**On submit only.** Validate the entire form when the user presses submit. Best for short forms (login, search, simple settings) where inline validation would be more annoying than helpful. Show all errors at once, scroll to the first error, and focus the first invalid field.

**On blur + on submit.** Validate each field when the user leaves it (blur), plus validate everything on submit. Best for medium forms (registration, profile editing) where catching errors early saves time. Never validate on blur before the user has interacted with the field: showing an error on an empty field they haven't touched yet feels aggressive.

**Real-time (on change).** Validate as the user types. Only appropriate for specific fields where immediate feedback is valuable: password strength meters, username availability, character count limits. Never apply to every field: it produces a wall of errors before the user has finished typing.

### Error display

- Errors appear directly below the invalid field, not in a banner at the top of the page.
- The invalid field receives a visible error state (red border, error icon).
- Error text is specific: "Email must include @" not "Invalid input."
- On submit with multiple errors: scroll to the first invalid field and focus it. Show all errors, not just the first.
- Errors clear when the user corrects the input. Never require re-submission to clear an error.

### Field grouping

Related fields are grouped with a visible container or heading. Address fields together. Payment fields together. Account fields together. Groups reduce cognitive load by chunking related decisions.

For long forms (10+ fields), consider breaking into sections with visible progress or a step indicator.

### Multi-step forms

When a form has 7+ fields spanning multiple concerns, split into sequential steps with transitions between them. Each step has a clear title and a manageable number of fields (3-5).

- Show progress: step indicators, progress bar, or "Step 2 of 4."
- Allow backward navigation: the user can return to previous steps without losing data.
- Validate each step on advancement, not only on final submit.
- Preserve entered data: if the user goes back, their previous inputs are still there.
- The final step shows a summary or confirmation before submitting.

### Submit behaviour

- The submit button disables immediately on press to prevent duplicate submissions.
- Show a loading state on the button itself (spinner or label change), not a separate indicator.
- On success: confirm inline (checkmark on button, success message near the form) or navigate to the result. Never only a toast.
- On error: re-enable the button, show the error, and preserve all entered data. Never clear the form on server error.
- In textareas and command-style forms, Enter inserts a newline by default. If quick submit is useful, support `Cmd+Enter` on macOS and `Ctrl+Enter` elsewhere, and expose the shortcut near the submit action.

---

## 2. Navigation Patterns

### Structure

**Top navigation** suits products with 3-7 top-level sections of roughly equal importance. The user can see all options at a glance. Works well when horizontal space is available.

**Sidebar navigation** suits products with many sections, nested hierarchy, or where the navigation needs to persist while the user works. Dashboards, admin panels, documentation. Can collapse to icon-only on smaller viewports.

**Bottom tab navigation** is the mobile standard for 3-5 primary destinations. Thumb-reachable, always visible. Each tab is a top-level section, not a nested page.

### Mobile adaptation

Sidebar navigation on desktop should not become a hamburger menu on mobile if the content is critical. Options:

- Collapse sidebar to icon-only (most common, preserves one-tap access).
- Move top-level items to bottom tabs, keep secondary items in a drawer.
- Full hamburger only for truly secondary navigation.

If using a hamburger: the menu slides in from the edge (not centre fade), is dismissible via swipe or backdrop tap, and shows an obvious close affordance.

### Active states

The currently active navigation item must be visually distinct at all times. Use a combination of colour, weight, and an indicator (left border for sidebar, bottom border for top nav, filled icon for tabs). Colour alone is insufficient (surface-colour rule: colour never the sole indicator).

### Breadcrumbs

Use breadcrumbs when the hierarchy is 3+ levels deep and the user needs to orient themselves or navigate back to intermediate levels. Each breadcrumb is a link except the current page. Use a separator (/ or >) between levels. Truncate long breadcrumb chains with an ellipsis that expands on click.

### Deep linking

Every view that a user might want to return to or share should have a unique URL. Modal states, filter configurations, tab selections, and pagination should be reflected in the URL. Use URL search params for transient state (filters, page) and path segments for persistent state (resource IDs, section).

---

## 3. Data Display Patterns

### Tables

Tables are for comparing structured data across multiple attributes. Use tables when the user needs to scan, sort, compare, or act on rows of similar items.

**Columns:** Keep the most important identifier (name, title, ID) in the first column. Left-align text, right-align numbers (for decimal alignment). Use `tabular-nums` for numeric columns (surface-typography). Column headers must be sortable where the data supports it.

**Sorting:** Single-column sort with a visible indicator (arrow) on the active column. Clicking the same column toggles ascending/descending. Clicking a different column sorts by it in ascending order.

**Filtering:** Filters sit above the table. Active filters are visible as tags or chips that can be individually cleared. A "clear all" option resets all filters. Show the result count: "Showing 12 of 148 results."

**Pagination:** Show at the table footer. Include: previous/next buttons, current page indicator, total count. For large datasets, offer page size control (10, 25, 50 items). Consider infinite scroll or "load more" for feeds where position in the list doesn't matter.

**Row selection:** Checkbox on the left. A floating action bar appears when rows are selected, showing the count and available bulk actions. "Select all" selects the current page. Offer "select all X results" for cross-page selection.

**Responsive:** Tables are inherently difficult on small screens. Strategies: horizontal scroll with sticky first column, card layout transformation (each row becomes a card), or priority columns (hide less important columns progressively).

**States:** Empty table prompts creation. Loading shows skeleton rows matching the column structure. Error shows retry. Partial shows pagination or "load more."

### Lists

Lists are for sequential items where comparison across attributes isn't the primary task. Use lists for feeds, search results, notifications, message threads.

Each list item should have a consistent structure: primary content (title, description), secondary metadata (date, status), and optionally an action (chevron, menu).

### Cards

Cards are for items with rich mixed content (image, title, description, metadata, actions). Use cards when items are browsed rather than compared, or when each item has visually distinct content.

Cards should have consistent height in a grid, or use a masonry layout if heights genuinely vary. Avoid mixing cards of different structures in the same grid.

---

## 4. Feedback Patterns

### Choosing the right feedback type

| Situation | Feedback type | Example |
|---|---|---|
| Background success (non-critical) | **Toast** | "Settings saved" |
| Inline success (action just taken) | **Inline indicator** | Checkmark on copy button |
| Error on specific field | **Field-level inline** | Red border + error text below input |
| System-wide error | **Banner** | "Service unavailable. Retrying..." |
| Destructive action confirmation | **Dialog** | "Delete this project? This cannot be undone." |
| Long-running process | **Progress indicator** | Upload progress bar with percentage |

### Toast rules

Toasts are for low-priority background confirmation only. They auto-dismiss after 4-5 seconds. They stack from the bottom (or top) without blocking interaction. They never contain actions the user needs to take. Important outcomes (success, error, completion) are inline, not toasts.

### Confirmation dialogs

Use only for destructive or irreversible actions. The dialog states what will happen ("This will permanently delete 12 files"), names the action on the confirm button ("Delete files", not "OK"), and gives a clear cancel path. The destructive action button uses the destructive variant.

Never use confirmations for reversible actions. If the user can undo, let them act and show an undo toast instead.

### Progress

For actions under 1 second, show no indicator (the result appears fast enough). For 1-4 seconds, show a spinner or loading state on the trigger element. For 4+ seconds, show a progress bar or percentage.

If the duration is unknown, use an indeterminate spinner. If the duration is known (file upload, data export), use a determinate progress bar.

### Optimistic updates

Update the UI immediately on action. Show the new state as if the server has already confirmed. If the server returns an error, roll back to the previous state and show an error message. Never show a loading spinner for actions that succeed 99% of the time. Per surface-details, this is the implementation pattern: system-patterns is the decision about when to use it.

Use optimistic updates for: toggles, likes, saves, preference changes, simple edits.
Do not use for: financial transactions, destructive actions, operations with complex server validation.

---

## 5. Layout Patterns

### Sidebar + main

The most common application layout. Sidebar holds navigation and context; main holds the primary content.

- Sidebar width: 240-280px on desktop. Collapsible to 64px (icon-only) or fully hidden.
- The sidebar does not shift when the main content scrolls. Use `position: sticky` or `position: fixed`.
- On mobile: sidebar becomes a drawer (slides from left edge) or collapses into bottom tabs.
- The main area fills the remaining width. Content within it has a max-width (typically 768px-1024px for text, wider for dashboards).

### Dashboard grids

Dashboards display multiple data widgets simultaneously. Use CSS Grid with a responsive column system.

- Define a minimum card width (300-400px) and let the grid auto-fill: `grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))`.
- All cards in a row share the same height (implicit with grid).
- Important metrics go top-left (the first thing scanned in LTR layouts).
- Group related widgets visually with proximity or a shared heading.

### Content density

Different contexts demand different density levels:

**Compact:** Dense data displays. Dashboards, admin tables, code editors. Smaller text, tighter spacing (--space-2 to --space-3 gaps), more information visible at once.

**Default:** Standard application UI. Forms, settings, content pages. Body text size, standard spacing (--space-4 to --space-6 gaps).

**Comfortable:** Marketing, reading-focused, onboarding. Larger text, generous spacing (--space-8 to --space-12 gaps), breathing room.

Use system-tokens spacing tokens to implement density variants. Consider offering user-controlled density preferences in data-heavy tools.

### Responsive strategies

**Reflow:** Items stack vertically as the viewport narrows. A 3-column grid becomes 2, then 1. The simplest and most common approach.

**Collapse:** Complex layouts simplify. A sidebar collapses to icons. A data table becomes cards. Filters move behind a "Filters" button.

**Adapt:** The layout fundamentally changes. Desktop sidebar + main becomes mobile bottom tabs + full-screen views. This is the most work but the best mobile experience.

### Max-width

Content should not span the full width of a large screen. Text is unreadable beyond 80 characters per line. Set `max-width` on content containers:

- Prose/text content: 65ch-75ch (about 650-750px)
- Forms: 480-640px
- Dashboards and data: full width minus sidebar, but individual widgets capped at ~600px
- Marketing hero sections: 1200-1400px

Centre the max-width container with `margin: 0 auto`.

---

## 6. Search Patterns

Search is one of the most common composite patterns. It involves an input, a results area, filtering, keyboard navigation, and multiple states.

### Input behaviour

The search input should be focusable via a keyboard shortcut (typically `⌘K` or `/`). On focus, show recent searches or suggested queries if available. Debounce the query (200-300ms) to avoid firing a request on every keystroke.

Clear the input with a visible "x" button that appears when text is present. Pressing Escape clears the input first; pressing Escape again closes the search if it's in an overlay.

### Results

Results appear as the user types (after debounce). Highlight the matching portion of each result to show why it matched. Support `↑`/`↓` arrow key navigation through results with a visible highlight. Pressing Enter selects the highlighted result.

If no results match, show a clear empty state: "No results for [query]" with suggestions (check spelling, try different terms) rather than a blank area.

### Loading and error

Show a subtle loading indicator within the search area (not a full-page spinner) while results are being fetched. If the search fails, show an inline error with retry. Never show stale results from a previous query without indicating they're outdated.

### Filtering

If the search supports filters (type, date, status), place them above the results. Active filters are visible as removable chips. Filters should update the URL so the search is shareable and bookmarkable.

---

## 7. Modal and Dialog Patterns

Modals interrupt the user's flow. They should be used sparingly and only when the task requires focused attention separate from the underlying page.

### When to use a modal vs inline/page

**Use a modal** for: confirmation of destructive actions, focused creation flows (compose, new item), content preview that returns to the same context, and settings that affect the current view.

**Use a page/route** for: complex forms with many fields, content that the user may want to bookmark or share, flows longer than 2-3 steps, and anything that benefits from the full viewport.

**Use a sheet/drawer** for: secondary actions on mobile (filters, sort, share), quick edits that don't warrant a full modal, and progressive disclosure of options.

### Focus management

When a modal opens, focus moves to the first focusable element inside it (or the modal container itself). Focus is trapped: tabbing past the last element wraps to the first. When the modal closes, focus returns to the element that triggered it.

### Dismiss behaviour

Modals close via: the close button, pressing Escape, and clicking the backdrop (unless the modal contains unsaved data, in which case backdrop click should warn). Sheets and drawers also close via swipe gesture.

### Scroll lock

When a modal is open, the underlying page must not scroll. Use `overflow: hidden` on the body, but preserve the scroll position and compensate for the scrollbar width to prevent layout shift.

### Mobile adaptation

On small screens, full-width or full-height modals often work better than centred floating dialogs. Bottom sheets are particularly effective on mobile: they start at a partial height and can be dragged to full-screen, matching native interaction patterns.

### Stacking

Avoid stacking modals (a modal opening another modal). If a confirmation is needed within a modal, use an inline confirmation within the same modal rather than opening a second one. If stacking is truly unavoidable, only the topmost modal should trap focus, and each layer should dim progressively.

### Deep linking

If a modal represents a distinct piece of content (a preview, an item detail), reflect its open state in the URL so the user can share or bookmark the modal view directly.

---

## Anti-Patterns

1. **Feature accretion without a pattern.** Adding a new branch that does not extend an existing workflow or replace a worse one.
2. **Unpriced complexity.** Adding states, permissions, or transitions without deciding what complexity is removed, hidden, or justified.
3. **Validate on blur before interaction.** Showing an error on a field the user hasn't touched yet.
4. **Clear form on server error.** The user loses all entered data and has to start over.
5. **Toast for important outcomes.** Success, error, and completion feedback must be inline.
6. **Confirmation for reversible actions.** If it can be undone, let the user act and offer undo.
7. **Hamburger for primary navigation.** Hiding critical navigation behind a menu on mobile when bottom tabs or icon sidebar would work.
8. **Colour-only active state.** Navigation active state using only colour. Must include weight, indicator, or icon change.
9. **Unresponsive tables.** A wide table that overflows on mobile with no scroll, card transformation, or column prioritisation.
10. **Generic spinner for loading data.** Use skeleton screens that mirror the actual content structure.
11. **Full-width text on large screens.** Prose that spans 1400px is unreadable. Max-width your content.
12. **Optimistic update on destructive actions.** Delete and financial operations should wait for server confirmation.
13. **Modal for complex multi-step flows.** If it needs more than 2-3 steps or the full viewport, it should be a page.
14. **Stacked modals.** A modal opening another modal. Use inline confirmation instead.
15. **Search without keyboard navigation.** Arrow keys must navigate results. Enter must select.

---

## Checklist

### Coherence
- New feature extends or replaces an existing pattern
- User task improved by the change is explicit
- Added states, transitions, permissions, errors, and empty cases are known
- Complexity is removed, hidden, or justified
- Existing behaviour is not contradicted without a migration path

### Forms
- Validation timing is intentional (on submit, on blur, or real-time per field)
- Errors appear inline below the invalid field
- Error text is specific, not generic
- On submit error: scroll to first invalid field and focus it
- Multi-step forms show progress and allow backward navigation
- Submit button disables on press and shows loading state
- Server error preserves entered data

### Navigation
- Structure matches the product's hierarchy and section count
- Active state is visually distinct (not colour-only)
- Mobile adaptation preserves access to primary sections
- Deep linkable: views have unique URLs
- Breadcrumbs present for 3+ level hierarchies

### Data Display
- Tables sort on column header click with visible indicator
- Filters are above the table with visible active state and clear option
- Pagination shows count, current page, and page size control
- Empty, loading, error, and partial states are all handled
- Responsive strategy exists for small screens

### Feedback
- Toast used only for background confirmation
- Important outcomes are inline
- Destructive actions have confirmation dialogs
- Reversible actions use undo, not confirmation
- Progress indicators match expected duration
- Optimistic updates used for low-risk actions only

### Layout
- Sidebar is sticky/fixed, not scrolling with content
- Content has max-width appropriate to its type
- Dashboard uses auto-fill grid with minimum card width
- Responsive strategy is defined (reflow, collapse, or adapt)
- Density matches the context (compact, default, comfortable)

### Search
- Keyboard shortcut to focus search (⌘K or /)
- Input debounced (200-300ms)
- Arrow key navigation through results
- Empty state shows helpful message, not blank area
- Active filters reflected in URL

### Modal / Dialog
- Focus trapped inside open modal
- Focus returns to trigger on close
- Escape closes the modal
- Scroll locked on underlying page (with scrollbar compensation)
- Modal state reflected in URL if content is shareable
- No stacked modals (use inline confirmation instead)
- Mobile: full-width or sheet instead of centred floating dialog

---

## Learning from Usage

After completing a feature or page layout task, review the output against the checklist. Append findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new task.
