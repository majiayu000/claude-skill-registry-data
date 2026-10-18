---
name: app-skill
description: T-MAX H5-demo project workflow for the React 19 + Vite + Tailwind + Zustand mobile web app. Use when working in ~/Documents/ane/code/git/T-MAX/H5-demo, including route/page changes, Figma-to-code implementation, shadcn-style UI components, Zustand stores, real login flow, cost pages, mobile layout QA, dependency/version updates, dev-server setup, lint/build validation, or keeping the scaffold generic and free of QT-APP business demo code.
---

# App Skill

## Project Facts

- Work in `~/Documents/ane/code/git/T-MAX/H5-demo`.
- Use React 19, Vite, TypeScript, Tailwind CSS, Zustand, React Router, Axios, Radix/shadcn-style components, and lucide-react icons.
- Always switch Node with:

```bash
eval "$(fnm env --use-on-cd)" && fnm use 22
```

- Run from `H5-demo`:

```bash
npm run dev -- --host 0.0.0.0 --port 7802
npm run lint
npm run build
```

- Default local URL is `http://localhost:7802`.

## Orientation

Before editing, inspect the relevant files instead of relying on memory:

- Routes: `src/app/routes.tsx`, `src/app/router.tsx`
- Shell/navigation: `src/components/layout/AppShell.tsx`, `BottomNav.tsx`
- UI primitives: `src/components/ui/*`
- Cost UI primitives: `src/components/cost/CostPage.tsx`
- Login: `src/pages/Login.tsx`, `src/services/authService.ts`
- Request wrapper: `src/services/request.ts`
- Stores: `src/stores/*`
- Styles and tokens: `src/styles/globals.css`, `tailwind.config.*`, `components.json`
- Project design contract: `DESIGN.md`

Use `rg` first for symbols and text. Treat `dist/` and `node_modules/` as generated/vendor output.

## Page-Level Design Contract

Before creating or restyling a page or shadcn/Radix component, inspect `DESIGN.md`, `tailwind.config.*`, and `src/styles/globals.css`.

`DESIGN.md` is the project source of truth for page-level UI rules. It must define and keep current:

- Spacing scale: page gutters, section padding, panel padding, vertical gaps, control heights, table row/header density, bottom safe-area spacing.
- Radius scale: page sections, cards/panels, buttons, inputs, pills/tags, sheets/dialogs, icon controls.
- Font scale: route content titles, section titles, card/list titles, body text, table text, helper text, numeric text, and font-weight rules.
- Color tokens: semantic colors and Arco scale usage for page, surface, ink, secondary, muted, line, soft, brand, success, warning, danger, chart series, status tags, disabled states, and overlays.

Rules:

- Do not invent local spacing, radius, font, or color decisions in a page. Pick the closest rule from `DESIGN.md`.
- Do not write raw hex/rgb/rgba colors in `src/pages` or `src/components`. Use Tailwind semantic tokens, Arco scale tokens, or CSS variables already documented in `DESIGN.md`.
- If the requirement needs a token that does not exist, update `DESIGN.md`, `tailwind.config.*`, and `src/styles/globals.css` first, then use that token.
- Preserve existing prototype hierarchy. Token unification must not redesign the page, add dashboard cards, change table rhythm, or alter information architecture unless the user explicitly asks.
- For UI tasks, run a quick scan such as `rg -n "#[0-9A-Fa-f]{3,8}|rgba?\(" src/pages src/components -S` before handoff when feasible.

## Figma-To-Implementation Flow

For Figma-driven page, component, or UI changes, follow this order and do not start coding until the extraction steps are complete:

1. Figma extraction: fetch the exact node design context and a screenshot. Extract colors, typography, spacing, radius, layout dimensions, component variants, and visible states such as default, active, disabled, loading, error, empty, and selected when present.
2. Token mapping: map the extracted values to `DESIGN.md`, `tailwind.config.*`, and `src/styles/globals.css`. Prefer existing semantic tokens and scale values. If a required value is missing, update the design contract and token files before using it.
3. UX check with ui-ux-pro-max: review accessibility, target size, focus visibility, contrast, interaction states, loading/empty/error states, responsive behavior, information hierarchy, and business usability. Fix usability gaps before visual polish.
4. Visual direction with frontend-design: define the page's purpose, target user, restrained H5 business tone, one memorable visual or interaction detail, font use, color role, and motion policy. For this app, preserve prototype fidelity and operational density over decorative redesign.
5. shadcn/Radix implementation: implement with existing `src/components/ui/*` primitives or install/copy shadcn components only when needed. Immediately adapt copied components to this project's token and variant system.
6. Figma validation: run the app in a mobile viewport, compare against the Figma screenshot, and check page-level overflow, key spacing, font sizes, colors, radius, component states, and interactive paths.

Required implementation rule:

- Card, Button, Form/Input/Select, Table, Dialog/Sheet, Tabs, Tag/Badge, and icon-button styling must share the same spacing, radius, type scale, and color token system. Put shared behavior in `src/components/ui/*` via `className`, `cva`, and variants; put workflow-specific composition in `src/components/<domain>`. Do not duplicate arbitrary shadcn overrides in pages.

## shadcn/Radix UI Rules

shadcn/ui components are owned source code in this project. Treat `src/components/ui/*` as design-system primitives, not one-off visual snippets.

- New or changed shadcn-style components must route styling through `className`, `cva`, and project tokens from `DESIGN.md`.
- Component variants and sizes must encode the page-level spacing/radius/font/color scale. Do not scatter ad hoc `px-*`, `py-*`, `rounded-*`, `text-*`, or color choices across consuming pages when they belong in a shared primitive.
- Page code may pass `className` for layout context, but should not redefine a primitive's base spacing, radius, font scale, or semantic color unless the component exposes an intentional variant/size for that case.
- Keep Radix accessibility behavior intact: ARIA attributes, focus management, keyboard behavior, disabled states, and focus-visible rings must survive visual customization.
- When installing a shadcn component, adapt the copied file immediately to the H5-demo token system before using it in pages.
- For repeated page patterns, create a domain wrapper under `src/components/<domain>` instead of duplicating shadcn overrides in multiple pages.

## Coding Rules

- Keep the scaffold generic. Do not add QT-APP business copy, sample data, or reference-repo business code unless the user explicitly asks.
- Prefer existing local patterns over new abstractions.
- Add routes only in `src/app/routes.tsx`; keep route elements imported at the top.
- Use `@/` imports according to `tsconfig.json`.
- Put reusable UI in `src/components/ui` or domain-specific UI in `src/components/<domain>`.
- Put cross-page state in Zustand stores under `src/stores`; keep local state in the page when it is not shared.
- Use shadcn/Radix-style component composition already present in the repo, following the shadcn/Radix UI Rules above. Use lucide icons inside icon buttons and action buttons.
- Keep H5/mobile sizing stable: safe-area padding, no body horizontal overflow, fixed toolbar/control dimensions, text that fits inside buttons.
- Keep cards at the radius defined in `DESIGN.md` unless an existing component/page already uses a documented intentional style.
- Do not create nested cards or landing-page marketing sections for app workflows.

## Login Guardrails

Login is a real integration path, not a mock demo.

- Do not replace the real login flow with simulated success.
- Before changing login, read `src/services/authService.ts` and `src/pages/Login.tsx`.
- Preserve the actual API chain: `login`, optional image captcha ticket/image/check flow, token persistence, and navigation.
- Treat request headers and base URL as high-risk. If the user specifies `x-auth-id`, `x-refurl`, `X-AUTH`, app id, or proxy/base path, apply that exact current request and verify it in browser/network behavior when feasible.
- If login breaks after a UI change, inspect request payload/headers first before changing visual code.

## Cost Module Rules

Cost pages are an H5 workflow, not a dashboard landing page.

- Main page: `src/pages/CostView.tsx`
- Filter pages: `CostFilter.tsx`, `CostMonthSelect.tsx`, `CostYearSelect.tsx`
- Template pages: `CostTemplateList.tsx`, `CostTemplateEdit.tsx`
- Filter state: `src/stores/costFilterStore.ts`
- Template state: `src/stores/costTemplateStore.ts`

Preserve these behaviors unless the user changes the requirements:

- Month cycle defaults to recent 12 months.
- Year cycle defaults to recent 3 years.
- Switching to year cycle closes three-year compare but does not clear saved month conditions.
- Three-year compare exists only for month cycle.
- Year report and three-year compare use the year/month matrix table with `成本指标 / 年份 / 01..12`.
- Template selection filters visible indicators; parent rows stay visible when selected descendants exist.
- Template edit supports checked, unchecked, and indeterminate tree states; template names are capped at 20 characters.
- Hide bottom nav for cost filter/template subpages when the existing shell does so.

## UI And QA

For UI work:

- Match the current H5 app style first: restrained operational UI, dense but readable spacing, white/soft gray surfaces, blue as action color.
- Apply the page-level design contract before visual embellishment. In this H5 business app, `frontend-design` means disciplined production polish and prototype fidelity, not a new decorative theme.
- Use screenshots from the user as source of truth for layout and interaction details.
- Avoid visible in-app explanatory text about how features work unless the screenshot/PRD requires it.

For verification:

- Run `npm run lint` and `npm run build` after code changes when feasible.
- For visual or interaction changes, start the dev server and verify in the in-app browser at a mobile viewport such as `430x932`.
- Check key text, selected states, click paths, and `document.documentElement.scrollWidth <= clientWidth` for whole-page overflow. Internal table horizontal scroll is acceptable when the design requires it.

## Handoff

End with:

- Changed files.
- Validation commands and results.
- Browser checks performed, if any.
- Any unverified items and why.
