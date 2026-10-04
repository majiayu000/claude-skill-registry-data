---
name: page-composition
description: Use when defining how pages are assembled from components, when establishing layout grids, when deciding responsive collapse strategies, or when multiple routes have inconsistent layouts.
---

# Page Composition

## Overview

Decide how pages are assembled from components: layout grid, page templates, responsive collapse strategy, navigation transformation per breakpoint, and content priority rules. Output is `.forge/page-composition.md`. Reads `component-library` (available pieces), `design-system` (breakpoints + spacing), and `interaction-patterns` (scroll, sticky, overlay behavior).

## When to Use

- A product is about to start building pages and there's no named template vocabulary
- Routes have drifted into one-off layouts with no shared structure
- The sidebar collapses inconsistently on mobile (or doesn't collapse at all)
- A new responsive breakpoint is being added and nobody knows what should change
- A second product is joining the design system and needs to inherit layout conventions

## When NOT to Use

- A single one-off marketing page — that's content, not composition
- Backend-only services with no UI
- A trivial layout fix inside one route — `incremental-implementation`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Every page is different" | Every page feels different, but most follow 3–4 templates. Name them and variation becomes predictable. |
| "We'll figure out responsive as we go" | "As we go" means the first 5 pages are desktop-only and mobile is retrofitted on day 10 under deadline pressure. |
| "Just make it responsive with Tailwind" | Tailwind handles the mechanics (`sm:`, `md:`, `lg:`). It doesn't decide *what* to do at each breakpoint. That's a design decision. |
| "Mobile can wait" | If field users open the product on phones, mobile IS the product. Desktop is the secondary experience. |
| "Sticky elements just work" | A sticky header that covers content on mobile is a bug. Sticky needs a rule. |

## Red Flags

- A route with no defined template (a one-off layout)
- A sidebar that doesn't collapse on mobile (or hides instead of relocating)
- Content that disappears on small screens rather than relocating to a secondary tab/accordion
- Inconsistent grid usage across routes (12-col on one, free-flow on another)
- Scroll behavior differing between similar pages (infinite on one list, paginated on the next)
- Sticky element that covers content on mobile (header overlapping first row of a list)

## Core Process

### Step 1: Read upstream artifacts

Read `.forge/component-library.md` (available components), `.forge/design-system.md` (breakpoints + spacing scale + max content width), `.forge/interaction-patterns.md` (scroll, sticky, overlay rules). Confirm the breakpoint set before defining templates against it.

### Step 2: Layout system

Define the grid that every template inherits:

- **Grid:** 12-column, 8-column, or flexbox-based. Pick one product-wide.
- **Gutter:** from the `design-system` spacing scale (e.g., `16px` mobile, `24px` desktop).
- **Max content width:** the cap beyond which content doesn't grow on ultra-wide screens (e.g., `1280px` for dashboards, `1440px` for tables, `640px` for forms).
- **Edge padding per breakpoint:** how much breathing room from the viewport edge at each size.

### Step 3: Name page templates

List the recurring page shapes the product uses. Common templates (include only what's needed):

- **Dashboard:** metrics row → charts grid → activity feed. Sidebar on desktop, bottom nav on mobile.
- **Detail:** hero/header → key metrics → content tabs → action footer. Full-width on mobile.
- **List:** filter bar → sortable table or card list → pagination. Cards on mobile, table on desktop.
- **Form:** section groups → inputs → sticky action bar. Single column always.
- **Settings:** sidebar nav → content panel. Tabs on mobile.
- **Empty:** illustration + headline + description + CTA. Centered always.

### Step 4: Define each template

For every template, document:

- **Section hierarchy** — what comes first, second, third
- **Information density per breakpoint** — desktop shows 3 columns of cards, tablet 2, mobile 1
- **Sticky elements** — header, action bar, sidebar; offsets so they don't cover content
- **Scroll behavior** — infinite scroll vs pagination vs load-more, per template (not per page)
- **Responsive collapse strategy** — what happens to the sidebar, what happens to the grid, what gets hidden vs stacked vs tabified

### Step 5: Responsive philosophy (per product)

Decide once, product-wide:

- **Mobile-first** (field reps, consumer apps): design at 380px first, enhance for desktop. Mobile is THE product.
- **Desktop-first** (SaaS managers, admin tools): design at 1280px first, adapt for mobile. Desktop is THE product.

This is a per-*product* decision, not a per-page decision. State it explicitly in the artifact.

### Step 6: Navigation transformation

Document how navigation changes across breakpoints:

| Breakpoint | Primary nav | Secondary nav |
|---|---|---|
| Desktop (`lg+`) | Sidebar (expanded) + topbar | Inline in topbar |
| Tablet (`md`) | Sidebar (collapsed to icons) + topbar | Inline in topbar |
| Mobile (`sm`) | Bottom tabs (3–5 items) | Hamburger overflow menu |

Define each breakpoint transition explicitly. No implicit "the sidebar will figure it out."

### Step 7: Content priority rules

On mobile, content does **not disappear** — it relocates. Document the rules:

- Primary content stays in the main flow
- Secondary content collapses into an expandable section or moves to a separate tab
- Tertiary content moves to a "More" overflow menu
- Decorative content (avatars in tables, illustrations) shrinks or hides — explicitly mark which

The principle: every piece of information has a home at every breakpoint. Nothing vanishes.

### Step 8: Write `.forge/page-composition.md`

Sections in this order: upstream-read confirmation, layout system, template catalog, per-template specs, responsive philosophy, navigation transformation, content priority rules. Prepend a `forge:meta` header (`generated_by: page-composition`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/component-library.md, .forge/design-system.md, .forge/interaction-patterns.md]` — paths only, never hashes, `generated_from: {.forge/component-library.md: <hash>, .forge/design-system.md: <hash>, .forge/interaction-patterns.md: <hash>}` — each upstream's content_hash AT generation time, `content_hash: <sha256 first 8 of THIS file's body>`).

## Verification

- [ ] Every route in the product maps to a named template (or is documented as one-off with reason)
- [ ] Every template has responsive behavior at all `design-system` breakpoints
- [ ] Navigation transformation is documented per breakpoint
- [ ] Content priority rules exist — nothing disappears, it relocates
- [ ] Mobile-first vs desktop-first decided once, product-wide
- [ ] Layout grid, gutter, max content width, and edge padding documented
- [ ] Sticky elements have offsets that don't cover content on the smallest breakpoint
- [ ] Scroll behavior is template-level, not per-page
- [ ] `.forge/page-composition.md` written with `forge:meta` header
