---
name: ui-design-lord
description: Lord skill for UI/UX design mastery — HTML, CSS, Tailwind v4.3, Filament v5 UI components, responsive design, RTL/Arabic, accessibility, and design systems. Do not use for frontend ui expert tasks — use `frontend-ui-expert` instead. Do not use for python ui lord tasks — use `python-ui-lord` instead.
triggers:
  - ui design lord
  - ui design
  - css design
  - html design
  - tailwind design
  - filament ui
  - responsive design
  - rtl design
  - arabic ui
  - تصميم UI
  - واجهة مستخدم
  - تصميم واجهات
personas:
  - DEV
tech_stack:
  - tailwind-4-3
  - filament-5
  - laravel-13
  - php-8-5
lord: true

---

# UI Design Lord

[OBJ] Mastery of UI/UX design for web applications — HTML, CSS, Tailwind v4.3, Filament v5 components, responsive design, RTL/Arabic support, accessibility (a11y), and design systems.

[RULES]
1. [CMD] Query Context7 for Tailwind CSS v4.3 and Filament v5 UI docs. Use `/tailwindlabs/tailwindcss` and `/filament/filament` library IDs.
2. [REQ] Tailwind v4.3: Use `@theme` in CSS (NOT `tailwind.config.js`). Oxide engine (Rust). `@container` for container queries. `@starting-style` for entry animations. `motion-reduce:` mandatory for a11y.
3. [REQ] Design Tokens: Define colors, spacing, typography in `@theme` block. Use new palettes (mauve, olive, mist, taupe). Logical properties (`ms-*`, `me-*`, `ps-*`, `pe-*`) for direction-aware layouts.
4. [REQ] Filament v5 UI: `Filament\Schemas\Components` (unified composition). `Schema::make()->components([...])`. `->deferLoading()` for heavy UI. `SlideOver::make()->position('left')` for RTL.
5. [REQ] Responsive: Mobile-first approach. `@container-size` for size-based container queries (not just width). `zoom-*` for CSS zoom. Test on real devices, not just browser DevTools.
6. [REQ] RTL/Arabic: `dir="rtl"` on `<html>`. Tailwind logical properties auto-flip. Filament `->position('left')` for SlideOver. Store translations in `lang/ar/`. Use `backed enum locale` for Filament enum labels.
7. [REQ] Accessibility (a11y): `motion-reduce:` for animations. `aria-*` attributes on interactive elements. `focus-visible:` for keyboard nav. Color contrast WCAG AA minimum (4.5:1). `sr-only` for screen reader text. NEVER rely on color alone for state.
8. [REQ] Component Architecture: Filament plugins for reusable features. `ComponentManager::resolve()->configureUsing()` for global defaults. `EvaluatesClosures` for DI in closures (`fn(Get $get, Set $set) => ...`).
9. [REQ] Empty States: `->emptyStateHeading()`, `->emptyStateDescription()`, `->emptyStateActions()` on stats/widgets. NEVER show raw "No data" — provide actionable empty states with CTAs.
10. [REQ] Loading States: `->deferLoading()` with skeleton placeholders. Loading indicator refactor (v5.8). NEVER show blank content during async loads — use skeletons or spinners.
11. [REQ] Design Slop Prevention: Use `DesignSlopVerifier` (aiZee runtime) to detect AI-generated UI slop. Check for: generic gradients, placeholder text, inconsistent spacing, non-matching brand colors.
12. [REQ] Brand Consistency: Use `DesignLibrary` (aiZee runtime) for 58 brand design systems. Match brand colors, typography, spacing. NEVER invent colors outside the design token system.
13. [REQ] Performance: Lazy-load images (`loading="lazy"`). `loadedOnRequest()` for Filament JS assets. Vite for production builds. NEVER inline large CSS/JS in Blade templates.
14. [REQ] Dark Mode: `dark:` variant. `@variant dark` in CSS. Filament theme switcher with CSP-safe Alpine. Test both light and dark in every UI review.

[WORKFLOWS]
1. Design a Filament Page: Define design tokens in `@theme` → create Schema components → add responsive variants → test RTL → verify a11y → check empty states → add loading skeletons → verify dark mode → run DesignSlopVerifier.
2. Responsive Layout: Mobile-first CSS → `@container` breakpoints → test on 375px/768px/1024px/1440px → add `motion-reduce:` → verify touch targets >= 44px → test keyboard navigation.
3. RTL Setup: `dir="rtl"` on `<html>` → use logical properties → translate Filament labels in `lang/ar/` → `->position('left')` for SlideOver → test with Arabic content → verify text alignment → check icon direction.
