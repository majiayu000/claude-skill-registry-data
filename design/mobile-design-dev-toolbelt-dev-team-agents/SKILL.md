---
name: mobile-design
description: Mobile-first responsive UI specs — breakpoints, navigation, spacing, touch targets.
---

# Mobile Design — Always Include

**Every UI task must produce mobile specifications.** Designs without mobile coverage are incomplete. Apply these rules regardless of whether the user mentions mobile.

## Layout & Breakpoints

| Breakpoint | Width | Layout |
|-----------|-------|--------|
| Mobile S | 320px | Single column, full-width blocks |
| Mobile L | 375px–428px | Single column, standard mobile |
| Tablet | 768px | 2-column or adaptive single |
| Desktop | 1280px+ | Full multi-column |

Default breakpoints (adapt to project's system): `sm: 640px · md: 768px · lg: 1024px · xl: 1280px`

**Mobile-first rule**: design the 375px layout first, then expand. Never design desktop-first and shrink.

## Navigation — Mobile vs Desktop

| Pattern | Mobile | Desktop |
|---------|--------|---------|
| Primary nav | Bottom tab bar (≤ 5 items) or hamburger drawer | Top horizontal nav or sidebar |
| Secondary nav | Drawer, bottom sheet, or accordion | Sidebar or breadcrumb |
| Search | Full-screen overlay | Inline search bar |
| Modals | Bottom sheet (full or partial) | Centered modal |

## Content Layout Rules by Breakpoint

- **Cards**: full-width at mobile; 2-up at tablet; 3–4-up at desktop
- **Tables**: horizontal scroll or card-list transformation at mobile — never squeeze columns
- **Forms**: single-column at mobile; max 2-column at tablet/desktop for related fields
- **Sidebars**: collapse to drawer or hide at mobile; show at ≥ 768px

## Typography — Mobile Adjustments

| Element | Desktop | Mobile |
|---------|---------|--------|
| H1 | 36–48px | 24–30px |
| H2 | 24–30px | 20–24px |
| Body | 16px | 16px (never below 14px) |
| Caption | 14px | 13–14px |
| Line height | 1.5 | 1.5–1.6 |

## Spacing — Mobile Adjustments

- Page horizontal padding: 16px mobile · 24px tablet · 32px+ desktop
- Section vertical spacing: 40–48px mobile · 64–80px desktop
- Component internal padding: reduce by 25–33% vs desktop
- Gap between stacked elements: 12–16px mobile · 16–24px desktop

## Touch & Interaction Rules

- **Minimum touch target**: 44×44px (Apple HIG) / 48×48dp (Material)
- **Tap feedback**: every interactive element must have an active/pressed state
- **Hover-only interactions**: must have a touch-accessible alternative
- **Input zoom prevention**: `font-size ≥ 16px` on all form inputs (prevents iOS auto-zoom)
- **Keyboard avoidance**: sticky footers and fixed CTAs must account for soft keyboard height
- **Swipe gestures**: document which gestures are available; never the only way to access a feature

## Component Responsive Behavior Summary

| Component | Mobile behavior |
|-----------|----------------|
| Button group | Stack vertically; full-width primary button |
| Data table | Horizontal scroll or transform to card list |
| Tabs | Horizontal scroll if > 4; consider bottom nav |
| Dropdown/Select | Native OS picker preferred |
| Toast/Snackbar | Bottom of screen, above nav bar |
| Pagination | Infinite scroll or "Load more" preferred |

## Mobile-First Coding Convention

Instruct the `frontend-developer` to write mobile-first CSS:

```css
/* Base = mobile */
.card { padding: 16px; flex-direction: column; }

/* Expand up */
@media (min-width: 768px) {
  .card { padding: 24px; flex-direction: row; }
}
```

Never write desktop-first and override with `max-width` queries.
