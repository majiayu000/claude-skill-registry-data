---
name: schoolos-redesign
description: Plan and rules for redesigning the SchoolOS frontend into a structured, premium "engineered" look based on the TailAdmin design language, with real images. Use whenever the user asks to redesign, restyle, modernise, polish, or add images to any SchoolOS screen, dashboard, sidebar, header, table, card, form, or role portal (principal, teacher, bursar, secretary, student, parent, super-admin), or asks about the SchoolOS design system. Use together with premium-ui-design-stack (process) and schoolos-guard (safety).
---

# SchoolOS Redesign

Goal: replace the ad-hoc burgundy/glassmorphism look with a clean, consistent, premium admin design (the TailAdmin visual language: calm neutrals, one brand colour, clear cards, tidy tables) and add real imagery. This is a **presentation-only** change.

Use `premium-ui-design-stack` for the design process and `schoolos-guard` before calling anything done.

## Hard rules

1. **Presentation only.** Do not change queries, RLS, auth, payments, routes or data shapes while restyling. If a screen needs a data change, stop and ask.
2. **Keep the stack.** Next.js + CSS Modules. Do not add Tailwind or copy the TailAdmin app in. Port its tokens and patterns into `assets/tokens.css` and shared components. (The template is MIT licensed but a separate Tailwind v4 app, and merging it would risk the production build.)
3. **One brand colour per school**, applied through `--school-brand`. No rainbow or per-button colours. Semantic colours (success, warning, error) only for status.
4. **Minimal copy.** One short sentence per helper text; remove explainer paragraphs.
5. **Mobile first.** Check 375px width first; keep the existing bottom navigation per role on phones, sidebar on desktop.
6. **Small, reviewable steps.** One phase or one role per branch and pull request. The owner approves the Vercel preview before merging. Never push redesign work straight to the production branch.

## Phases

1. **Foundations.** Add `assets/tokens.css` to the global styles. Load the Outfit font with `next/font`. Build shared primitives in `src/components/ui/` as CSS Modules: `Button`, `Card`, `StatCard`, `Badge`, `Avatar`, `Table`, `Modal`, `EmptyState`, `PageHeader`. No page changes yet.
2. **Shell.** Redesign the shared layout: sidebar (desktop), top header, breadcrumbs, mobile bottom nav, light and dark theme.
3. **Pilot: super-admin.** One user (the owner) and already has a shared shell, so it is the safest place to prove the system.
4. **Role portals, one per PR:** principal, bursar, secretary, teacher, parent, student, then the smaller roles (vice-principal, counselor, nurse, librarian, ict, examination, hostel, coach).
5. **Public pages:** landing, register-school, login.

For each screen: read the existing component, keep its data code untouched, swap markup and styles to the primitives, then run the review checklist in `premium-ui-design-stack`.

## Taste skills: which one for which screens

Optional. Only if installed from https://github.com/Leonxlnx/taste-skill (`npx skills add ...`). Where they conflict with the hard rules above, **the hard rules and `assets/tokens.css` win**. Review their scripts before enabling them.

| Screens | Use | Do not use |
|---|---|---|
| Public pages: landing, register-school, login | `design-taste-frontend` (art direction, look-and-fix loop on screenshots) | |
| Logged-in dashboards and all role portals | `redesign-existing-projects`, as an audit and polish pass using this skill's tokens as the design system | `design-taste-frontend`: its own description says it is not for dashboards or app screens |
| Any large file or full-screen rewrite | `full-output-enforcement`, to stop truncated or placeholder code | |

Notes:
- `redesign-existing-projects` suggests varying navigation and doubling whitespace. For SchoolOS keep the shared sidebar and bottom nav and the token spacing; dashboards are dense on purpose. Its advice to design composed empty states is good; follow it.
- For public-page photos, use `design-taste-frontend`'s asset script, which finds freely licensed images and records each licence. Keep credits. For dashboards, use the school's own uploads (see `references/imagery.md`).

## Where things are

- `assets/tokens.css`: colours, type scale, shadows, radii, spacing.
- `references/tailadmin-patterns.md`: the card, stat card, sidebar item, button, table and form patterns to copy.
- `references/imagery.md`: how to add images safely.
