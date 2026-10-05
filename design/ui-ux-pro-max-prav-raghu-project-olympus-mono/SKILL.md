---
description: UI/UX design intelligence for building professional frontend interfaces. Covers styles, color palettes, font pairings, UX guidelines, and component patterns across Angular and Ionic Angular. Invoke when designing new pages, creating or refactoring UI components, choosing visual styles, or when UI looks unprofessional and the reason is unclear.
argument-hint: <page or component description, e.g. "admin dashboard with data table and sidebar">
---

# UI/UX Design Intelligence

This skill provides professional design guidance for this monorepo's frontend stack: Angular standalone components (admin-web, customer-web) and Ionic Angular + Capacitor (customer-mobile), all using Tailwind CSS v4.

## How to use

Run a design system search before writing frontend code, if the global `ui-ux-pro-max` CLI is installed:

```bash
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "$ARGUMENTS" --design-system --stack angular
```

If the global skill is not installed, use the design principles in this file directly.

## Installation (run once globally)

```bash
npm install -g ui-ux-pro-max-cli
uipro init --ai claude --global
```

Requires Python 3.x. This skill's own design-token guidance below does not depend on the CLI being installed.

## Project design principles

This project uses Tailwind v4 with CSS variable color tokens. All design decisions must use the existing token system — never hardcode hex colors.

### Token system

```css
:root {
  --background: hsl(...);
  --foreground: hsl(...);
  --primary: hsl(...);
  --primary-foreground: hsl(...);
  --secondary: hsl(...);
  --muted: hsl(...);
  --muted-foreground: hsl(...);
  --card: hsl(...);
  --border: hsl(...);
  --destructive: hsl(...);
  --ring: hsl(...);
}
```

Use `bg-background`, `text-foreground`, `bg-primary`, `text-destructive` etc. — never raw color classes like `bg-blue-500`.

### admin-web design rules

- Persistent left sidenav, top navigation bar, main content area with breadcrumbs
- Tables with pagination, search input, filter controls, action buttons
- Cards use `bg-card border border-border rounded-lg`
- Loading states use skeleton via `bg-muted animate-pulse`
- Danger actions use `text-destructive` / `bg-destructive`
- No pill-shaped primary buttons unless explicitly requested

### customer-web design rules

- Semantic HTML throughout: `<main>`, `<article>`, `<section>`, `<nav>`
- `Title`/`Meta` services set on every page for SEO
- Mobile responsive first
- No placeholder/stock components — production-ready only

### Mobile (Ionic Angular) design rules

- Native feel: `IonCard`, `IonList`, `IonItem` for content lists
- `IonSkeletonText` for loading states
- `IonRefresher` for pull-to-refresh
- Respect safe areas: `ion-padding` for content spacing
- Animations: 150–300ms, transform/opacity only

## UX quality checklist (apply to every page)

- Loading state: skeleton or spinner when data is fetching
- Error state: message + retry button
- Empty state: helpful message + call-to-action
- Every interactive element has a focus ring
- No layout shift when data loads
- Mobile responsive at 375px minimum
- Color contrast minimum 4.5:1 for text
- Tap targets minimum 44×44px on mobile
- Form errors displayed below the field via Angular `Validators`, not in alerts
