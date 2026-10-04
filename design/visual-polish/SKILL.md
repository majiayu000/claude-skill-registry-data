---
name: visual-polish
description: Use after features are built and before shipping, when the UI needs a quality pass, when the product needs to look premium instead of functional, or when preparing for a demo or investor meeting.
---

# Visual Polish

## Overview

Run the systematic quality pass that turns "it works" into "this feels professional." Output is `.forge/polish-checklist.md` — pass/fail per item, with `file:line` for every failure. Reads `design-system`, `component-library`, `page-composition` (all optional, but each makes the pass sharper). Sits between `/build` and `/ship` in the pipeline.

## When to Use

- Features are built, tests pass, and the UI is about to be shown to anyone outside the team
- A demo or investor meeting is scheduled within the week
- The product "works" but the team feels something is off and can't name it
- A redesign was promised and the team needs to confirm the redesign actually landed
- Before promoting a beta to general availability

## When NOT to Use

- Features aren't built yet — polish is the last 10%, not the first 90%
- A backend-only service
- Polish was done this sprint and nothing visual changed since

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "It works, that's enough" | Working is table stakes. Users judge quality in the first 3 seconds. Polish is the difference between "this works" and "this feels professional." |
| "We'll polish before launch" | Launch is always tomorrow. If polish isn't in the process, it never happens. |
| "Users don't notice these details" | Users can't articulate what they notice. They feel "janky" or "solid." Polish is what they're feeling. |
| "It's just a demo" | Demos are the highest-stakes UI moment. Every missing hover state says "prototype." |
| "We'll fix it after the demo" | After the demo means after the impression. The first impression is the only impression. |

## Red Flags

- Browser default focus rings (`outline: auto`)
- Empty state that says only "No data" with no context or CTA
- Error message that says "Something went wrong" with no next step
- Layout shift on content load (CLS > 0.1)
- Missing favicon — the tab is generic
- Page title that says `localhost:3000` or `Vite App`
- Horizontal scroll appearing at 320px or 1440px

## Core Process

### Step 1: Read available UI artifacts

Load whichever of these exist: `.forge/design-system.md`, `.forge/component-library.md`, `.forge/page-composition.md`, `.forge/brand-identity.md`, `.forge/interaction-patterns.md`, `references/motion-system.md`. Use them as the rubric — polish is "the runtime matches the system."

### Step 2: Micro-interaction audit

For every interactive element:
- Every button has `hover` + `active` + `focus-visible` states
- Every toggle/switch transitions smoothly (not instant swap; per `references/motion-system.md`)
- Every link has a hover state (underline or color shift)
- Focus rings are visible and consistent (not browser defaults; not `outline: none` without replacement)
- Form inputs have `focus` + `error` + `disabled` styling

### Step 3: Empty state audit

For every list, table, chart, dashboard panel, sidebar group:
- An empty state exists with helpful headline + description + CTA
- No blank areas; no "No data" without context
- Empty-state voice matches `brand-identity` voice rules

### Step 4: Error state audit

- Every form has inline validation with **specific** messages (not just a red border)
- Every network call has error handling with retry where applicable
- A 404 page exists and matches the product's visual language
- Toast notifications for async errors are styled (not `alert()`)
- Error messages name *what happened* and *what to do next*

### Step 5: Loading audit

- Every async content area has a skeleton screen (not a spinner; per `interaction-patterns`)
- Skeletons match the shape of real content (same dimensions, same approximate density)
- Zero layout shift when content loads (skeleton → content occupies identical box)
- Spinners only inside buttons (`spinner-in-button` + disabled state)

### Step 6: Responsive edge case audit

Test at the extremes:
- **320px** — smallest common phone; no horizontal scroll, no text overflow without ellipsis
- **1440px+** — large desktop; content respects the max-width cap from `page-composition`
- Touch targets ≥ 44pt on mobile
- Long content (multi-word labels, 100-character strings, pasted URLs) tested in every container

### Step 7: Meta audit

- Favicon exists and matches `brand-identity`
- Apple touch icon for iOS home-screen save
- OG meta tags: `og:title`, `og:description`, `og:image` — image is 1200×630 and matches brand
- `<title>` is descriptive per route (not the same string everywhere)
- `<meta name="theme-color">` set for mobile browser chrome

### Step 8: Dark mode audit (if applicable)

- Every screen rendered in dark mode
- All text/background pairings pass WCAG AA (4.5:1 for body, 3:1 for large text)
- Images and illustrations have dark-mode variants or transparent backgrounds
- No hardcoded `#FFFFFF` leaking through (grep for raw hex in component files)
- Inline SVGs use `currentColor` where appropriate

### Step 9: Write `.forge/polish-checklist.md`

For every audit, list each item as pass/fail. Every failure includes:
- The audit it belongs to
- A `file:line` (or route + selector) pointer
- The smallest specific fix

Prepend a `forge:meta` header (`generated_by: visual-polish`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [<each UI artifact that existed at run time>]` — paths only, never hashes, `generated_from: {<each upstream path>: <its content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`).

After writing, report a summary: total items checked, total failed, the three highest-impact failures.

## Verification

- [ ] Every interactive element has `default / hover / active / focus-visible / disabled` states (loading + error where relevant)
- [ ] Every list/table/chart has an empty state with CTA
- [ ] Every async area has a skeleton, not a spinner on the content
- [ ] No layout shift on content load (CLS ≈ 0)
- [ ] Favicon, Apple touch icon, OG tags, and route-specific `<title>` all present
- [ ] No horizontal scroll at 320px or 1440px+
- [ ] Touch targets ≥ 44pt on mobile
- [ ] Dark mode parity (if shipped) — all pairings pass WCAG AA
- [ ] `.forge/polish-checklist.md` written with `file:line` pointers for every failure
- [ ] Summary reported with the three highest-impact failures called out
