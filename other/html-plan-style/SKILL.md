---
name: html-plan-style
description: >
  Use when generating any HTML plan, report, or deliverable document. Apply this
  skill whenever the task involves "create a plan", "write a plan", "make an HTML
  plan", "/pipeline-*" that produces plans, output convention plan files, or any
  structured HTML document intended for review. Provides a locked color palette,
  typography, and layout system so all plan HTML files look consistent and
  professional. Includes the 22px body font rule, rem-based child sizing, CSS
  variable architecture, print stylesheet, and a full component vocabulary
  (headings, callouts, tables, checklists, code blocks, status badges).
  Self-contained — brand values are resolved into literal CSS once at generation
  time, with no runtime dependency on design-system/. Use plan-template.html as
  the base skeleton and style.css (or the embedded style block) as the single CSS
  source of truth. Also for: session digests, agent reports, architecture decision
  records, sprint summaries, onboarding docs, and any structured HTML deliverable
  that will be opened in a browser or exported to PDF. This skill is for
  plans/documents, not slide decks.
scope: global
dept:
  - all
team: "-"
priority: foundation
triggers:
  - create a plan
  - write a plan
  - make an html plan
  - write an html plan
  - generate a plan
  - plan.html
  - output convention
  - pipeline-feature
  - pipeline-bugfix
  - pipeline-content
  - pipeline-audit
  - pipeline-deploy
  - pipeline-seo
  - html report
  - html deliverable
  - architecture decision record
  - session digest
aliases:
  - plan-style
  - html-plan
  - plan-template
last_updated: "2026-05-22"
trust_level: human-authored
author: operator
provenance: manual
quality_gate_passed: true
---

# html-plan-style

Locked style system for all HTML plan and report files. The palette shipped in
`style.css` is a forest/gold/terracotta editorial scheme; any brand registered in
`{agency-root}/design-system/brands/` can be resolved in its place -- see "Brand
Resolution at Generation Time" below. Apply whenever producing a plan.html.

## Quick Start

1. Copy `plan-template.html` from this skill directory as your starting file
2. Replace the placeholder content with your actual plan content
3. Do NOT change the CSS variables in `:root` -- palette changes happen in one place
4. Serve or open in browser to verify; export to PDF via browser print if needed

## Brand Resolution at Generation Time

`plan-template.html` and `style.css` ship with one palette already resolved into
their `:root` block. This skill promises a **self-contained artifact** -- so brand
resolution happens once, into literal values, at generation/authoring time. It is
never a live dependency.

To generate a plan for a different brand (any brand registered in
`{agency-root}/design-system/brands/`, including the shipped `neutral` fallback):

1. Read `{agency-root}/design-system/brands/{brand}.json` to get that brand's 15
   canonical `roles` (bg, surface, ink, primary, secondary, accent, border,
   text-muted, ...) plus its 4 `semantic` roles.
2. Map those roles onto this skill's `--color-*` variable names. The `:root` block
   already in `style.css` is the worked example -- it shows every mapping decision
   made once already.
3. Where this skill needs a tint or shade the brand does not define as one of its
   roles (a pale accent background, a subtle border), derive it with a CSS
   `color-mix()` expression referencing an already-resolved var **declared earlier
   in the same `:root` block** -- e.g.
   `color-mix(in srgb, var(--color-accent) 15%, white)`. Never invent a new hex
   that is not traceable to a brand role.
4. For the four semantic signals (success / warning / danger / info), prefer the
   brand's own `semantic` block. Only if the brand has none, fall back onto
   whichever structural roles read correctly for each meaning -- and check the
   four still resolve to **visibly different** colors. Two semantic signals
   collapsing into one color is the single most common failure of this step;
   `{agency-root}/design-system/verify-semantic-consumers.js` exists to catch it
   and will render this skill's CSS in a real browser to prove it.
5. Paste the fully RESOLVED, literal `:root` block into the OUTPUT file's own
   `<style>` block. **Never** a live `@import` or `<link>` to `design-system/` --
   that would make every future plan permanently depend on that path at render
   time, regressing this skill's self-contained property. The brand JSON is a
   one-time input to the resolution step, not a runtime dependency of the
   deliverable.
6. Keep the 22px body / rem children / print stylesheet rules exactly as
   documented -- they are layout rules, not brand-owned, and are unaffected by
   brand switching.

## Palette Reference (CSS Variables)

| Variable | Value | Use |
|---|---|---|
| `--color-bg` | `#f0f5f3` | Page background (forest-50) |
| `--color-surface` | `#ffffff` | Cards, panels |
| `--color-surface-alt` | `#fdf6f3` | Alternate section bg (terracotta-50) |
| `--color-border` | `#d4e9e2` | Card borders (forest-100) |
| `--color-border-subtle` | `#e7e5e4` | Subtle dividers (stone-200) |
| `--color-primary` | `#1E3A2F` | Forest-800 -- primary headings, CTAs |
| `--color-primary-dark` | `#1a3028` | Forest-900 -- hero bg, dark sections |
| `--color-primary-light` | `#3d7a62` | Forest-500 -- links, accents |
| `--color-accent` | `#D4A853` | Gold-500 -- highlights, badges |
| `--color-accent-dark` | `#b8922e` | Gold-600 -- hover states |
| `--color-secondary` | `#C4785A` | Terracotta-500 -- warnings, secondary |
| `--color-secondary-light` | `#f5d5c8` | Terracotta-200 -- warning backgrounds |
| `--color-text` | `#292524` | Stone-800 -- body text |
| `--color-text-muted` | `#78716c` | Stone-500 -- captions, metadata |
| `--color-text-on-primary` | `#ffffff` | Text on dark/forest bg |
| `--color-success` | `#3d7a62` | Forest-500 -- success states |
| `--color-success-bg` | `#f0f5f3` | Forest-50 -- success bg |

## Typography

- Body: `Plus Jakarta Sans`, `DM Sans`, `system-ui`, sans-serif
- Display/headings: `Playfair Display`, `Georgia`, serif
- Mono: `JetBrains Mono`, `ui-monospace`, monospace
- Base size: **22px** (per CLAUDE.md rule) -- all children in `rem`
- H1: 2.5rem | H2: 1.8rem | H3: 1.3rem | H4: 1.1rem

## Component Vocabulary

### Page Skeleton (REQUIRED -- read before anything else here)

Every other component below assumes this wrapper. `.plan-container` is what
carries `max-width`, `margin: 0 auto`, and the horizontal padding;
`.plan-section` carries the vertical rhythm between sections. A bare `<main>` /
`<section>` inherits none of it, so the page renders full-bleed with zero left
padding and no centering -- and the header still looks correct (it is styled by
`.plan-header`), which is what makes the bug easy to miss on a quick glance.

```html
<body>
  <header class="plan-header">
    <div class="plan-header-inner"> ... </div>
  </header>

  <main class="plan-container">
    <section class="plan-section"> ... </section>
    <section class="plan-section"> ... </section>
  </main>
</body>
```

Both class names are mandatory on every occurrence. Verify after generating:

```bash
grep -c 'class="plan-section"' out.html   # must equal your <section> count
grep -c '<section>' out.html              # must be 0
```

### Section Label (gold, uppercase)
```html
<span class="section-label">Phase 1</span>
```

### Callout Types
```html
<div class="callout callout-info">Informational note</div>
<div class="callout callout-warning">Warning or blocker</div>
<div class="callout callout-success">Completed or approved</div>
<div class="callout callout-decision">Decision locked</div>
```

### Status Badge
```html
<span class="badge badge-done">Done</span>
<span class="badge badge-in-progress">In Progress</span>
<span class="badge badge-blocked">Blocked</span>
<span class="badge badge-pending">Pending</span>
```

### Checklist
```html
<ul class="checklist">
  <li class="done">Completed item</li>
  <li class="in-progress">Active item</li>
  <li>Pending item</li>
</ul>
```

### Card
```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content</p>
</div>
```

### Table
Use standard `<table>` -- the stylesheet handles striping and borders automatically.

### Code Block
Use standard `<pre><code>` -- styled with mono font and forest-50 background.

### Hero / Title Block
```html
<header class="plan-header">
  <span class="section-label">Project Name</span>
  <h1>Plan Title</h1>
  <p class="subtitle">One-line description of this plan</p>
  <div class="header-meta">
    <span>Date: 2026-05-22</span>
    <span>Author: System-Improvement PD</span>
    <span class="badge badge-in-progress">In Progress</span>
  </div>
</header>
```

## Invocation Rules

- Always load `plan-template.html` as the base. If you copy only its `<style>`
  block instead of the whole file, you must also reproduce the Page Skeleton above
  by hand -- the stylesheet alone does nothing without `.plan-container` /
  `.plan-section`, and this is exactly how a shipped plan rendered full-bleed with
  no one noticing until it was opened for review
- Never override CSS variables outside `:root`
- Never use inline `color:` or `background:` -- use CSS variable references only
- Body font stays 22px; child elements use rem (e.g. `1rem` = 22px, `0.9rem` = ~20px)
- Print stylesheet is included -- do not remove the `@media print` block
- No emojis in plan content unless the plan content specifically calls for them

## Design Quality Principles

Before producing any HTML plan output, read `~/.claude/agents/design/memory/design-quality-principles.md` and apply its visual standards to layout, color usage, and typography choices.

## Files in This Skill

- `SKILL.md` -- this file (invocation guide + component vocabulary)
- `plan-template.html` -- full skeleton ready to fill in
- `style.css` -- standalone CSS (same as the embedded style in plan-template.html)
