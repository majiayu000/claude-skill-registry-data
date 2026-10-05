---
name: tabler-ui
description: >
  Use when building or reviewing UI with the Tabler admin template (tabler.io) —
  which Tabler components/utilities exist, how to compose them, and (critically)
  the exceptions/workarounds needed to make Tabler and its companion vanilla JS
  behave in the target framework, especially Vue 3. Invoke for ANY Tabler markup
  decision: modals, dropdowns, badges/pills, grid columns, form inputs, icons,
  wizards, empty states, emails — in any Tabler app. Carries the living
  "don't use Tabler's X — use Y instead" exceptions list; consult it BEFORE using
  any Tabler interactive component. Do NOT use for component/state/data-access
  structure or UX flow decisions — that's the frontend skill; do NOT use for
  color/typography/spacing judgment — that's design-guide. This skill owns "which
  Tabler pieces, and do they break in this framework?"
---

# Tabler UI

The user uses Tabler extensively. Goal: build great interfaces from Tabler's component
set, and know the gotchas — Tabler ships Bootstrap-flavored markup + vanilla JS that
often needs adapting for reactive frameworks. The real content lives in the reference
files below; this file routes you to them.

## Step 1 — route to the exceptions/reference file and READ it first

Skipping this step is how known, already-solved bugs get reshipped (clipped dropdowns,
dead carousels, unstyled prod buttons):

| Task involves… | Read first |
| --- | --- |
| Any interactive/JS component (modal, dropdown, carousel, confirm dialog, action menu), z-index/stacking, or a runtime-composed class name | [components-js.md](components-js.md) — the don't-use-X/use-Y list + the PurgeCSS production-stripping trap |
| Form inputs, validation display, filter UIs (operator pickers, chip bars), date display | [forms-filters.md](forms-filters.md) — the generic vuelidate-wired field widgets and their model quirks |
| Grid/column layout, badges/status pills, icons, table empty/error states, hero/eyebrow type | [layout-visuals.md](layout-visuals.md) |
| Email templates or a non-Vue Tabler stack (R/Shiny) | [emails-other-stacks.md](emails-other-stacks.md) |
| Copying markup from the reference bundle, upgrading `@tabler/core`, a Tabler class or `--tblr-*` token that does nothing, or any v1.6 component (datepicker, OTP, sparkline, legend…) | [versions.md](versions.md) — bundle-vs-app version gap, and the v1.6 changes that bite |

`LEARNINGS.md` beside this skill, when your copy keeps one, holds only raw,
not-yet-promoted captures — check it too when working in an area touched recently.

## Step 2 — compose from Tabler's toolbox, matching the app

- **Know the toolbox.** Tabler provides cards, page header/body, steps/wizards, tables,
  forms (form-control/form-select/form-check + validation states), buttons, badges,
  alerts, empty states, input groups/icons, navs/tabs, offcanvas, dropdowns, modals,
  datagrid, status/avatars, and a large utility layer. v1.6 added a datepicker, OTP
  input, password-strength meter, sparklines, legends, signal bars, clipboard buttons
  and confetti (see versions.md before using any of them). Compose these rather than
  hand-rolling; lean on the utility classes for spacing/layout.
- **Check the reference templates for UX shape.** Before designing a screen's layout,
  look at the official Tabler template bundle you downloaded from tabler.io (its admin
  dashboard pages, emails, icons, avatars and illustrations) — they show the intended
  composition, so you don't approximate it from memory. Keep that bundle at one absolute
  path, so it is the same directory from every repo and every worktree, and keep the
  folder names **unversioned**: upgrade the bundle in place and never write a version
  into a path, or every citation of it goes stale on the next upgrade. (This install's
  path and version: `LOCAL.md` beside this skill, when your copy keeps one —
  *Reference templates*.) For a quick look without the bundle, or to point someone who
  doesn't have it at an example, use the public live preview:
  <https://tabler.io/admin-template/preview>. **The bundle and the preview track the
  newest Tabler; the app may not.** Compare versions before copying markup, because a
  class the app's Tabler lacks renders unstyled with no error ([versions.md](versions.md)).
- **Match the existing app.** Read neighboring components and reuse the same Tabler
  patterns/wrappers already in the codebase (your app's modal wrapper, teleported
  dropdown and shared form fields) before introducing new ones — a second pattern for
  the same job is a review reject. (This install's wrapper names: `LOCAL.md` beside this
  skill, when your copy keeps one — *Match the existing app*.)
- **Respect the framework boundary.** Tabler's vanilla JS components (modals, dropdowns,
  carousels, tooltips) fight a reactive framework's lifecycle — the framework re-renders
  DOM the JS thinks it owns. Prefer the framework-native wrapper the project already
  uses; the exceptions list is the authority.

## Step 3 — verify (hard gates)

1. **Light AND dark mode.** Tabler theming (`data-bs-theme`) means dark-mode-only bugs
   are an established class here (the carousel desync was dark-only). Toggle both.
2. **Built output when any class name is composed at runtime.** PurgeCSS strips
   composed classes from prod CSS only — dev and unit tests pass. See components-js.md.
3. **Show inline screenshots** of the rendered UI (both themes) — the user reviews
   visuals, not descriptions of them.

## Common failure modes

- **Reaching for `data-bs-*` (or its v1.6 alias `data-tblr-*`) attributes for anything
  stateful** (modal, dropdown, carousel, datepicker, OTP) — stop; the Vue-native
  replacement or the lifecycle-owned pattern is in components-js.md.
- **Copying bundle markup into an app on an older Tabler** — the new class renders
  unstyled and nothing errors (versions.md).
- **`col-lg-3` on a 3-tile row** — 12-wide grid: the class must be 12 ÷ tile-count, or
  the row leaves a dangling empty slot (layout-visuals.md).
- **Hand-rolling a raw `form-control` input** when the app already ships shared,
  vuelidate-wired field components (forms-filters.md) — loses validation display for free.
- **Importing a workspace types package's enum values in an SFC** (when that package uses
  decorators/reflect-metadata) to build options/badge maps — reflect-metadata boot crash;
  key by string value instead. (This install's names: `LOCAL.md` beside this skill, when
  your copy keeps one — *Common failure modes*.)
- **Trusting a dev-mode render as proof** — the PurgeCSS and hydration bug classes only
  appear in the built output.

## Before you call this done

- [ ] Checked the relevant reference file(s) before using any interactive component.
- [ ] Consulted the downloaded Tabler template bundle when shaping new UX, and checked
      that anything copied from it exists in the app's installed Tabler version.
- [ ] Reused the app's existing wrappers (modal, dropdown, shared form fields).
- [ ] Verified in BOTH light and dark mode, with inline screenshots.
- [ ] If class names are composed dynamically: verified against the BUILT output.

## Capturing learnings (session-handoff protocol)

On handoff / "update skills" / after UI work: record new Tabler patterns that worked,
any component that needed a framework-specific replacement (with the why and the
replacement), stacking/z-index pitfalls, and styling conventions. Append raw captures to
`LEARNINGS.md` beside this skill, when your copy keeps one, tagged by stack; once an entry is validated/mature, move it
into the matching reference file above (keep the "don't use X / use Y instead, because Z"
format) and leave a one-line pointer. Dedupe/merge as you go.
