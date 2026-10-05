---
name: qruiq-review-ux
description: |
  Review-only audit of interaction UX patterns and design principles. Scans for missing
  confirmation dialogs, loading states, toast feedback, form validation, empty states,
  keyboard accessibility, error boundaries, progressive disclosure, navigation patterns,
  responsive touch targets, scroll behavior, state persistence, search UX, file upload UX,
  permission UI, native element usage, and HeroUI design principle violations (semantic
  variants, composition patterns, consistency, type safety, customization). Reports issues
  with severity and recommended fix — does NOT modify any code.
  Use when asked to "review UX", "audit interactions", "check UX", "交互审查",
  "优化交互", "交互细节", "UX best practices", "review UI patterns", "检查界面",
  "UI 审查", "交互优化", "design review", "设计审查", "组件审查", or any request
  involving reviewing or improving the quality of user-facing interaction flows.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# qruiq-review-ux

> **Review-only.** Audit the current project for interaction anti-patterns and produce a
> structured report with recommendations. This skill never edits code.
>
> Tech stack assumption: Next.js + HeroUI + Tailwind CSS + TypeScript

## Parameters

Collect before execution:

| Parameter | Required | Default | Description |
|---|---|---|---|
| `SCOPE` | No | `full` | Audit scope: `full` (entire app) or a specific directory path (e.g. `app/dashboard`) |

## Steps

**Execute all steps directly. Do not list as TODOs.**

### 1. Determine scan scope (incremental vs full)

The skill uses a file-level cache at `.qruiq-review-ux/` in the project root. Each scanned file produces a per-file result stored as `.qruiq-review-ux/<relative-path>.json`.

**Decision logic:**

```
if .qruiq-review-ux/ does NOT exist:
  → Full scan: scan every .tsx/.ts file in SCOPE
else:
  → Incremental scan: only scan files changed since last scan
```

**Step 1a — Check for cache directory:**

```bash
ls .qruiq-review-ux/ 2>/dev/null
```

**Step 1b — If cache exists, get changed files only:**

Use git diff to find files changed since the last scan timestamp stored in `.qruiq-review-ux/_meta.json`:

```bash
# Read last scan commit from meta
cat .qruiq-review-ux/_meta.json   # { "last_commit": "<sha>", "last_scan": "<iso-date>" }

# Get changed .tsx/.ts files since that commit
git diff --name-only <last_commit> HEAD -- '*.tsx' '*.ts'

# Also include untracked new files
git ls-files --others --exclude-standard -- '*.tsx' '*.ts'
```

If the last commit no longer exists (e.g. after a rebase), fall back to full scan.

**Step 1c — If no cache, collect all files:**

```bash
# Use Glob to find all .tsx/.ts files in SCOPE
# Pattern: "**/*.tsx" and "**/*.ts" (exclude node_modules, .next, dist)
```

### 2. Scan files (file-by-file)

For each file in the scan list, **Read the entire file** and audit it against ALL checklist categories (A–S). Do NOT use grep for scanning — read each file fully to understand context.

**For each file, check for:**
- Destructive actions without confirmation (delete, remove, reset, revoke, destroy)
- Buttons/forms triggering async ops without loading/disabled states
- Mutations with no toast/feedback on success or failure
- Toggles/favorites waiting for API before updating UI
- Forms missing client-side validation, required indicators, or error preservation
- Lists/tables with no empty state
- Custom clickable elements (`<div onClick>`) not keyboard-accessible
- Missing error boundaries on routes or dynamic sections
- Instant show/hide with no transitions
- Low-frequency actions (logout, delete account) not behind progressive disclosure
- Navigation missing active state, mobile support, or breadcrumbs
- Touch targets < 44px, hover-only interactions
- Search without debounce, clear button, or empty results state
- File uploads without progress, validation, or preview
- Permission-gated content flashing before redirect
- Tables without sort, loading state, or mobile fallback
- Scroll/state not persisted across navigation
- Native HTML elements (`<button>`, `<input>`, `<select>`, `<table>`, `<dialog>`, `window.confirm()`) used instead of component library equivalents
- Design: visual variant names instead of semantic (`solid`/`flat` → `primary`/`secondary`)
- Design: prop-based composition instead of dot notation compound components
- Design: inconsistent sizes, hardcoded colors, missing className, lost type safety, copy-pasted components instead of wrappers

**Per-file result format** (written to `.qruiq-review-ux/<relative-path>.json`):

```json
{
  "file": "app/dashboard/page.tsx",
  "scanned_at": "2026-04-05T12:00:00Z",
  "commit": "ae68566",
  "issues": [
    {
      "line": 42,
      "category": "A",
      "severity": "P0",
      "summary": "Delete handler calls API without confirmation modal",
      "recommendation": "Wrap in a Modal with confirmation text naming the target"
    }
  ]
}
```

If a file has zero issues, still write the cache entry with an empty `issues` array — this marks it as scanned.

### 3. Update cache metadata

After all files are scanned, write/update `.qruiq-review-ux/_meta.json`:

```json
{
  "last_commit": "<current HEAD sha>",
  "last_scan": "<current ISO timestamp>",
  "total_files_scanned": 42,
  "scan_mode": "full | incremental"
}
```

**Important:** Add `.qruiq-review-ux/` to `.gitignore` if not already present.

### 4. Merge results and output the report

Combine all per-file cache results (not just the ones scanned this run — include cached results from previous runs for unchanged files) into a single report.

### 5. Output the report

Present a structured report in this format:

```markdown
# UX Interaction Audit Report

## Summary
- Total issues found: N
- P0 Critical: N | P1 High: N | P2 Medium: N | P3 Low: N

## Issues

### P0 Critical

#### 1. [File:Line] Short description
- **Category**: (e.g. A. Destructive Actions)
- **Problem**: What's wrong
- **Recommendation**: How to fix it
- **Code snippet**: The offending code (3-5 lines for context)

### P1 High
...

### P2 Medium
...

### P3 Low
...
```

Severity levels:
- **P0 Critical**: Data loss without confirmation, no error handling on mutations, exposed actions without auth guard
- **P1 High**: Missing loading states, no disabled during submit, no toast feedback, flat info hierarchy exposing destructive/sensitive actions at top level, using native HTML elements instead of component library
- **P2 Medium**: Missing empty states, no keyboard support, poor focus management, no search debounce, missing scroll restoration, design principle violations (inconsistent variants, broken hierarchy)
- **P3 Low**: Missing transitions/animations, tooltip hints, micro-interactions, inconsistent icon-only button hints, minor design inconsistencies (size mismatches, missing className customization points)

**Do NOT apply any fixes. Only report.**

---

## Interaction Checklist

### A. Destructive Actions — Confirmation Required

Any action that deletes, removes, resets, or irreversibly changes data MUST have a confirmation step.

**What to check:**
- `onClick` handlers that call delete/remove APIs without a confirmation modal
- Inline delete buttons without a two-step flow (click → confirm → execute)
- Bulk actions (select all → delete) without explicit count in confirmation

**Expected pattern:**
- Use a Modal or Popover confirmation — never `window.confirm()`
- Confirmation text must name the action and the target (e.g. "Delete project 'My App'?")
- Destructive button must use danger styling and be placed on the right
- Cancel button must be the default focus to prevent accidental confirm
- Must support `Escape` key to cancel

### B. Loading & Disabled States

**What to check:**
- Buttons that trigger async operations without a loading indicator
- Forms that can be double-submitted
- Pages that fetch data without a skeleton or spinner

**Expected pattern:**
- Buttons must show a loading spinner and be disabled while the operation is in-flight
- Form submit buttons must be disabled after first click until the response arrives
- Data loading states should use skeleton layouts matching the final content shape
- Full-page loads should never show a blank white screen — always show a skeleton or spinner

### C. Toast / Feedback Notifications

**What to check:**
- Mutations (create, update, delete) that complete silently with no user feedback
- Error responses that are swallowed or only logged to console

**Expected pattern:**
- Every mutation must show a toast on success AND on failure
- Use a toast library (e.g. `sonner`) — configure once in providers, never use `alert()` or `window.alert()`
- Success toasts should be brief and auto-dismiss in ~3 seconds
- Error toasts should persist until dismissed and include a retry action if applicable

### D. Optimistic Updates

**What to check:**
- Toggle switches, like/favorite buttons, or status changes that wait for API response before reflecting in UI
- Lists where adding/removing items causes a full refetch flash

**Expected pattern:**
- UI-only state changes (toggles, favorites) should update immediately and rollback on error
- List mutations should optimistically add/remove the item without a loading flash
- Show a subtle rollback toast if the optimistic update fails

### E. Form Validation & Error Handling

**What to check:**
- Forms with no client-side validation (relying only on server errors)
- Required fields without visual indicators
- Error messages that appear far from the invalid field
- Forms that clear all input on submission error

**Expected pattern:**
- Required fields must have a visual indicator (asterisk or label text)
- Validate on blur for individual fields, validate all on submit
- Error messages must appear directly below the invalid field
- Form state must be preserved on submission failure — never clear user inputs on error

### F. Empty States

**What to check:**
- Lists or tables that show nothing when data is empty
- Search results with no matches showing a blank area
- Dashboard widgets with no data

**Expected pattern:**
- Every list/table must have an empty state with: illustrative icon + message + primary action button
- Search empty states should suggest clearing filters or broadening the query
- Use a centered layout with muted text

### G. Keyboard Accessibility

**What to check:**
- Custom clickable elements (`<div onClick>`) that are not focusable
- Modals or dropdowns that don't trap focus
- Missing `aria-label` on icon-only buttons

**Expected pattern:**
- All interactive elements must be focusable — use semantic elements (`<button>`, `<a>`) or add `tabIndex={0}` + `role`
- Custom clickable divs must handle `onKeyDown` for Enter and Space
- Modals must trap focus and return focus to the trigger element on close
- Icon-only buttons must have `aria-label`

### H. Error Boundaries

**What to check:**
- Pages or sections that crash the entire app on render error
- Missing error boundaries around dynamic content (user-generated, API-driven)

**Expected pattern:**
- Each route should have a framework-level error boundary (e.g. `error.tsx` in Next.js)
- Critical sections (charts, user content, third-party embeds) should have local error boundaries
- Error UI must offer a "Try again" action and never expose stack traces in production

### I. Transitions & Micro-interactions

**What to check:**
- Elements that appear/disappear instantly (modals, dropdowns, accordions)
- Page transitions that feel jarring
- State changes with no visual continuity

**Expected pattern:**
- Modals and drawers should animate in/out (HeroUI handles this natively)
- List item add/remove should use layout animations for smooth reflows
- Skeleton-to-content transitions should crossfade
- Button state changes (idle → loading → success) should transition smoothly

### J. Progressive Disclosure & Information Hierarchy

Low-frequency or sensitive actions must not sit at the same visual level as primary actions. They should be nested behind an intentional interaction so the interface remains clean and safe.

**What to check:**
- Sign Out / Logout exposed as a top-level button in the header instead of nested inside a user avatar dropdown menu
- "Delete Account" or danger zone settings visible on page load without a collapsed section
- Admin-only actions displayed at the same visual level as regular user actions
- Settings pages that dump all options in a flat list without grouping or collapsible sections
- Edit/Delete actions on cards permanently visible instead of revealed on hover or via a "⋮" overflow menu
- Toolbars with too many visible buttons — low-frequency actions should collapse into a "More" menu

**Expected pattern:**
- Account actions (Sign Out, Profile, Settings) belong inside a Dropdown triggered by the user's avatar — the avatar is the natural affordance for "things about me"
- Destructive settings should be behind a collapsible "Danger Zone" section or placed at the very bottom of the page
- Card action menus: use a three-dot icon button that opens a dropdown; only the primary action (e.g. "Open") should be directly visible on the card surface
- Toolbars with more than 4–5 actions should group lower-priority items into a "More" dropdown
- Inline editing: show read-only content by default; reveal edit controls on hover or via an explicit "Edit" trigger

### K. Navigation & Menu Patterns

**What to check:**
- No visual indicator for the current active route in the sidebar or navbar
- Mobile navigation missing entirely (no hamburger menu, bottom tabs, or drawer)
- Breadcrumbs absent on deeply nested pages (3+ levels deep)
- Logo or app name not linking back to home/dashboard
- Navigation items using plain `<div>` or `<span>` instead of proper link elements

**Expected pattern:**
- Active route must be visually distinct (background highlight, bold text, left border, or underline)
- Mobile screens (< 768px) should collapse navigation into a hamburger/drawer or switch to bottom tabs
- Pages 3+ levels deep should show breadcrumbs for orientation
- The app logo must always link to the root route
- Navigation items must be semantic links for right-click/open-in-new-tab support and accessibility

### L. Responsive & Touch UX

**What to check:**
- Tap targets smaller than 44×44px on interactive elements
- Hover-only interactions with no touch alternative (e.g. tooltip content, hover-reveal menus)
- Content overflow or horizontal scroll on mobile viewports
- Fixed-position elements (modals, floating buttons) that overlap or become unreachable on small screens
- Text inputs that cause layout shifts when the mobile keyboard opens

**Expected pattern:**
- All tappable elements must meet minimum 44×44px (Apple HIG) / 48×48dp (Material) — if the visual element is smaller, add padding to expand the hit area
- Hover-triggered content must also be accessible via tap/click or long-press
- Test layouts at 320px, 375px, and 768px breakpoints — no horizontal overflow
- Modals on mobile should use full-screen or bottom-sheet presentation
- Use `dvh` (dynamic viewport height) units instead of `vh` to account for mobile browser chrome

### M. Search UX

**What to check:**
- Search input that fires a request on every keystroke with no debounce
- No loading indicator while search results are being fetched
- No empty state for "no results found"
- Search input that cannot be cleared with a single action (missing ✕ button)
- No keyboard shortcut to focus search (e.g. `/` or `Cmd+K`)

**Expected pattern:**
- Debounce search input by at least 300ms before triggering a request
- Show a spinner inside or adjacent to the search input while loading
- Empty result state should say "No results for '[query]'" and suggest broadening the search
- Include a clear button (✕) inside the input when it has a value
- Consider supporting `Cmd+K` / `Ctrl+K` or `/` to focus the search field

### N. File Upload UX

**What to check:**
- File input with no drag-and-drop support
- No progress indicator during upload
- No file type or size validation before upload starts
- No preview for image uploads
- No way to remove a selected file before submitting

**Expected pattern:**
- Provide a drop zone with visual feedback (border highlight on drag-over)
- Show upload progress (percentage bar or spinner)
- Validate file type and size client-side before uploading; show an inline error immediately if invalid
- For image files, show a thumbnail preview after selection
- Allow removing or replacing a selected file before final submission

### O. Permission & Authorization UI

**What to check:**
- Pages that flash restricted content before redirecting unauthorized users
- No visible feedback when a user attempts an action they lack permission for
- Admin-only buttons rendered but non-functional for regular users (silent failures)
- Middleware redirects with no explanation — user sees a sudden jump with no context

**Expected pattern:**
- Unauthorized users should never see restricted content flash — use server-side checks or a loading gate
- If a user lacks permission, show a clear message (e.g. "You don't have access. Contact your admin.")
- Actions the user cannot perform should either be hidden entirely or shown as disabled with a tooltip explaining why
- On redirect for authorization failure, land the user on a meaningful page (e.g. a 403 page with next steps), not the homepage with no explanation

### P. Data Table UX

**What to check:**
- Tables with no sorting on columns that are naturally sortable
- No loading state during data refetch (e.g. when changing sort or filter)
- Table content that overflows on mobile without horizontal scroll or responsive fallback
- Bulk selection (checkbox column) without a "Select All" / "Deselect All" toggle
- Pagination controls that don't indicate total count or current position

**Expected pattern:**
- Sortable columns should show a sort indicator (arrow icon) and toggle asc/desc on click
- Wrap table refetch in a loading state — dim the table body or show a subtle overlay spinner
- On mobile, either allow horizontal scroll with a visible scrollbar hint, or switch to a card-based layout
- Bulk selection should include "Select all on this page" and optionally "Select all N items"
- Pagination must show: current page, total pages or total items, and per-page size selector

### Q. Scroll & State Persistence

**What to check:**
- Scroll position lost when navigating back (e.g. list → detail → back resets to top)
- Tab selection, filter values, or sort order that reset on page navigation
- Infinite scroll with no "Back to top" affordance
- Infinite scroll that loses position on page refresh

**Expected pattern:**
- Preserve scroll position on back navigation — verify that the routing approach supports this
- Persist filter, sort, and tab state in URL search params so it survives refresh and is shareable
- Infinite scroll pages should show a floating "Back to top" button after scrolling 2+ viewport heights
- Consider URL-based pagination (e.g. `?page=3`) even in infinite scroll as a fallback anchor

### R. Native Element Avoidance — Use Component Library

Projects using a component library (e.g. HeroUI, Ant Design, MUI, shadcn/ui) must NOT use native HTML elements for interactive UI. Native elements have inconsistent styling across browsers, lack built-in dark mode support, and break visual consistency.

**What to check:**
- `<button>` instead of the library's `<Button>`
- `<input>` / `<textarea>` instead of `<Input>` / `<Textarea>`
- `<select>` instead of `<Select>` or `<Dropdown>`
- `<table>` / `<tr>` / `<td>` instead of `<Table>` / `<TableRow>` / `<TableCell>`
- `<dialog>` instead of `<Modal>`
- `<details>` / `<summary>` instead of `<Accordion>`
- `<progress>` / `<meter>` instead of `<Progress>` / `<CircularProgress>`
- `<input type="checkbox">` / `<input type="radio">` instead of `<Checkbox>` / `<Radio>`
- `<input type="file">` without a styled wrapper or drop zone component
- `window.confirm()` / `window.alert()` / `window.prompt()` instead of Modal or Toast

**Expected pattern:**
- Always use the project's component library equivalent — this ensures consistent theming, dark mode, accessibility, and responsive behavior out of the box
- If no library equivalent exists for a specific element, wrap the native element in a styled component that matches the design system
- The only acceptable native elements are non-interactive structural tags (`<div>`, `<span>`, `<p>`, `<h1>`–`<h6>`, `<ul>`, `<li>`, `<form>`, `<label>`, `<img>`, `<a>`, etc.)

### S. Design Principles Audit (HeroUI)

Audit component usage against HeroUI's 9 core design principles. Reference: https://www.heroui.com/docs/native/getting-started/design-principles

#### S1. Semantic Intent Over Visual Style

**What to check:**
- Variants using visual names (`solid`, `flat`, `bordered`, `ghost`, `faded`, `light`, `shadow`) instead of semantic names (`primary`, `secondary`, `tertiary`, `danger`)
- Button groups or action sets where the visual hierarchy is unclear — reader cannot tell at a glance which is the main action

**Expected pattern:**
- Use semantic variant names that communicate hierarchy: `primary` (main action, 1 per context), `secondary` (alternative actions), `tertiary` (dismissive: cancel, skip), `danger` (destructive)
- Bad: `<Button variant="solid">Save</Button> <Button variant="flat">Cancel</Button>`
- Good: `<Button variant="primary">Save</Button> <Button variant="tertiary">Cancel</Button>`

#### S2. Accessibility as Foundation

**What to check:**
- Interactive components missing accessibility labels (`aria-label`, `accessibilityLabel`)
- Custom components that don't pass accessibility props through to the underlying HeroUI component
- Focus order that doesn't match visual reading order
- Touch targets without proper hit area sizing

**Expected pattern:**
- All interactive components must have accessibility labels — HeroUI components include built-in support, but custom wrappers must forward these props
- Screen reader announcements should describe the action, not the visual appearance (e.g. "Delete item" not "Red button")
- Tab order must follow logical reading order (left-to-right, top-to-bottom)

#### S3. Composition Over Configuration

**What to check:**
- Using monolithic prop-based patterns (`startContent`, `endContent`, `leftIcon`, `rightIcon`, `label` as props) instead of HeroUI's compound component (dot notation) pattern
- Components that pass complex JSX through props instead of composing with child components
- Deeply nested prop objects for styling individual parts

**Expected pattern:**
- Use compound components with dot notation for composability:
  - Bad: `<Button label="Submit" leftIcon={<Icon />} />`
  - Good: `<Button><Icon /><Button.Label>Submit</Button.Label></Button>`
- Each sub-component should be independently arrangeable, customizable, or omittable
- If a component supports dot notation (`.Trigger`, `.Content`, `.Label`, `.Indicator`), use it

#### S4. Progressive Disclosure in Component Usage

**What to check:**
- Components overloaded with too many props when a minimal version would suffice
- Complex configurations used where simple defaults work
- All available options exposed at once instead of layered complexity

**Expected pattern:**
- Start with minimal props; add complexity only when the use case demands it:
  - Level 1 (minimal): `<Button>Click me</Button>`
  - Level 2 (enhanced): `<Button variant="primary" size="lg"><Icon /><Button.Label>Submit</Button.Label></Button>`
  - Level 3 (advanced): Add `isDisabled`, `isLoading`, conditional children
- If a component works without a prop, don't add the prop

#### S5. Predictable Behavior & Consistency

**What to check:**
- Inconsistent `size` values across components in the same view (e.g. `size="sm"` button next to `size="lg"` chip with no reason)
- Different variant naming or patterns for similar components
- Components that don't accept `className` for customization
- Hardcoded pixel values instead of using the size system (`sm`, `md`, `lg`)

**Expected pattern:**
- Use consistent `size` across related components in the same context
- All components should follow the same API patterns: `size`, `variant`, `className`, `color`
- Prefer the size tokens (`sm`, `md`, `lg`) over hardcoded values
- If one button in a group is `size="md"`, all buttons in that group should be `size="md"` unless intentionally differentiated

#### S6. Type Safety

**What to check:**
- Using string literals for variants/sizes without TypeScript checking (e.g. `variant={"custom"}` that isn't in the type union)
- Custom component wrappers that lose type information (`any` types, missing generics)
- Event handlers without proper typing (e.g. `onPress={(e: any) => ...}`)

**Expected pattern:**
- Extend component types properly: `interface CustomButtonProps extends Omit<ButtonRootProps, 'variant'> { ... }`
- Never use `any` for component props — leverage HeroUI's exported types
- Custom variants should be typed as string unions

#### S7. Customization Patterns

**What to check:**
- Inline styles (`style={{...}}`) used for theming instead of `className` or CSS variables
- Overriding component internals with `!important` or deep CSS selectors
- Colors hardcoded as hex/rgb instead of using theme tokens (`--accent`, `--background`)
- No dark mode consideration — colors that only work in one theme

**Expected pattern:**
- Use `className` for component customization, not inline styles
- Use Tailwind Variants (`tv()`) for custom variant definitions
- Colors must reference theme tokens or CSS variables — never hardcode `#fff` or `rgb(0,0,0)`
- All custom styles must work in both light and dark mode
- For extensive customization, create a wrapper component with `tv()` rather than ad-hoc className strings

#### S8. Component Extension Patterns

**What to check:**
- Copy-pasted HeroUI component source code instead of wrapping/extending
- Components that re-implement functionality already provided by HeroUI (custom modal, custom dropdown)
- Custom components that don't forward refs or spread remaining props

**Expected pattern:**
- Wrap, don't fork: create custom wrappers using HeroUI base components
- Custom wrappers must spread `...props` to the underlying component for extensibility
- Use `tailwind-variants` (`tv()`) for custom variant maps when the built-in variants aren't enough
- Example:
  ```tsx
  const CTAButton = ({ intent = 'primary-cta', children, ...props }) => {
    const variantMap = { 'primary-cta': 'primary', 'secondary-cta': 'secondary' };
    return <Button variant={variantMap[intent]} {...props}><Button.Label>{children}</Button.Label></Button>;
  };
  ```

---

## Confirmation Patterns by Action Type

Use this table to verify the correct confirmation pattern is used:

| Action Type | Expected Pattern | Example |
|---|---|---|
| Delete single item | Modal with item name | "Delete user 'John Doe'?" |
| Delete multiple items | Modal with count | "Delete 3 selected projects?" |
| Irreversible action | Modal + type-to-confirm | "Type 'DELETE' to confirm" |
| Logout / disconnect | Dropdown menu item (not top-level button) | Avatar → Menu → "Sign Out" |
| Discard unsaved changes | Modal on navigation | "You have unsaved changes. Discard?" |
| Bulk operation | Modal with summary | "Archive 12 messages?" |
| Payment / charge | Modal with amount | "Charge $49.99 to card ending 4242?" |
| Toggle dangerous setting | Inline confirm with undo window | Switch flips → "Undo" toast for 5s |

---

## Composability

This skill layers on top of existing projects as a review step:

```
qruiq-create-app          → Project skeleton
    + qruiq-review-ux      → Review interaction patterns (report only)
    + qruiq-google-auth    → Google OAuth login
    + qruiq-github-ci      → CI/CD pipeline
```

## Rules

- **NEVER edit source code files** — this is a review-only skill. The only files written are inside `.qruiq-review-ux/`
- **Write** and **Bash** tools are ONLY for managing `.qruiq-review-ux/` and `.gitignore` — never for modifying project source
- Output a structured report with file paths, line numbers, and severity
- If no issues are found for a category, skip it in the report
- Be specific: cite exact file + line, not vague "some buttons lack loading states"
- On incremental scans, merge cached results from unchanged files with fresh results from changed files
- If a previously cached file has been deleted, remove its cache entry
- Always ensure `.qruiq-review-ux/` is in `.gitignore`