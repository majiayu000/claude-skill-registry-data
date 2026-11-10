---
name: app-table
zh_name: "数据表格"
en_name: "App Table"
emoji: "📋"
description: "A list or table of records with search, filters, sort, selection, bulk actions and pagination, plus its empty, loading and no-results states, inside the app shell."
en_description: "A list or table of records with search, filters, sort, selection, bulk actions and pagination, plus its empty, loading and no-results states, inside the app shell."
category: app
scenario: design
tags: ["table", "data table", "list", "records", "crm", "admin", "filters", "列表", "表格"]
triggers:
  - "table"
  - "data table"
  - "list of"
  - "records list"
  - "admin list"
  - "crm list"
  - "orders list"
  - "users list"
od:
  mode: prototype
  craft:
    requires:
      - product-ui
      - state-coverage
      - action-states
      - ux-writing
  surface: web
  platform: desktop
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
  example_prompt: "The Customers table of a CRM: name, company, status, owner, last contact and value, with search, a status filter, bulk email and pagination."
---

<!-- Kit skill (openspec add-app-screens). -->
# App Table

Produce one screen whose job is a list of records: find one, act on several, open one.

## Workflow

1. **Columns.** Name first (strongest weight), then status as a badge with a word, then two to four key fields, then row actions at the end. Five to seven columns on desktop.
2. **Rows.** At least eight realistic rows from the brief's domain, varied: long and short names, every status at least once, an empty optional field, a large and a small number.
3. **Toolbar above the table:** search, one or two filters as menus or chips showing their current value, the primary create action on the right.
4. **Selection:** a checkbox column; selecting rows shows a bulk bar ("3 selected · Email · Export · Delete").
5. **Sort:** one column sorted, shown with an arrow and `aria-sort` on its header.
6. **Pagination** under the table counting the rows actually shown, with rows-per-page.
7. **Narrow screens:** each row becomes a record card (name, status, one key field, chevron), or the table scrolls sideways inside its own box. The page never scrolls sideways.

## States

- `default`: populated.
- `empty`: no records yet: what will be here, why it's empty, the create action.
- `loading`: skeleton rows the shape of real rows, header and toolbar in place.
- `long-content` (optional): the same table with very long names and huge numbers, to show truncation with the full value in a `title`.
Also design a no-results variant inside `empty` or as a note: echo the query and offer to clear filters.

## Self-check

- Numbers right-aligned with tabular figures.
- The search, filter and pagination numbers agree with the rows on screen.
- A sorted, filterable, selectable header is a real `<button>` or has the right ARIA, so it can be checked.

## Markup contract (shared by every app screen)

- **States.** Each state of the screen is a sibling `<section data-od-state="…">`: `default` (populated), and the ones this pattern lists below from `empty`, `loading`, `error`, `success`, `no-access`, `long-content`. Only `default` is visible; the others carry `hidden`. The kit's check renders every state, and the preview shows them side by side.
- **Slots.** Keep the seed's `data-od-slot` names (`nav`, `toolbar`, `content`, `empty`, `loading`) so states, links and comments line up.
- **Links between screens.** When this screen is part of a planned flow, link to another screen with its entry path in `href` and its screen id in `data-od-goto`, and use the shared navigation the brief gives instead of drawing your own.
- **The app's own components.** When the brief lists the app's components, build each part from one of them and mark it `data-od-component="<Name>"`; mark a part with no match `data-od-component="new:<Name>"`.
- **Sample data.** Records come from the data file the brief describes, never typed into the markup row by row: one template row or card with `data-od-repeat="<list>"` and `data-od-bind=".<field>"` inside it, single values with `data-od-bind="<list>[n].<field>"`, and `data-od-format` for money, dates and numbers. Every screen that shows the same record binds to the same one.
- **Tokens only.** Every colour, size, radius and shadow comes from the design system's `:root` variables. No raw hex outside `:root`.
- **Platform.** Web app: the shell as given. iPhone, Android, tablet or desktop app: put `data-od-device` on `<body>` (`iphone`, `android`, `tablet` with `data-od-orientation`, or `desktop-app` with `data-od-window="mac"` or `"windows"`); the kit draws the device frame, status bar and home indicator around the screen, so never draw them yourself. iPhone or Android: a single column 390 px (iPhone) or 412 px (Android) wide, with a bottom tab bar instead of the side nav, a top bar with the title and a back button on inner screens, and 44 px (iPhone) or 48 px (Android) touch targets. Android screens use Material patterns (top app bar, floating action button where there is one main create action). Tablet: the sidebar collapses to an icon rail with labels in a tooltip, content in two columns where the pattern has a detail pane.
- **Density.** Use the density the brief gives (compact, medium or airy) with the numbers from the product UI craft rules.

## Seed

Start from this shell (one HTML file, inline CSS). Replace the comments; keep the structure.

<!-- od:app-shell:start -->
```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Screen title · Product</title>
<style>
/* Paste the active design system's :root block here, then use only var(--…). */
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:var(--text-base)/var(--leading-body) var(--font-body)}
.app{display:grid;grid-template-columns:1fr;min-height:100dvh}
.app-nav{display:flex;gap:var(--space-1);padding:var(--space-2) var(--space-4);border-bottom:1px solid var(--border);overflow-x:auto}
.app-nav a{display:flex;align-items:center;gap:var(--space-2);min-height:44px;padding:0 var(--space-3);border-radius:var(--radius-md);color:var(--muted);text-decoration:none;white-space:nowrap}
.app-nav a[aria-current="page"]{background:var(--surface);color:var(--fg);box-shadow:var(--elev-ring)}
.app-main{min-width:0;padding:var(--space-4)}
.app-toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:var(--space-3);margin-bottom:var(--space-4)}
.app-toolbar h1{margin:0 auto 0 0;font:600 var(--text-xl)/var(--leading-tight) var(--font-display)}
[data-od-state][hidden]{display:none}
@media (min-width:64rem){
  .app{grid-template-columns:260px 1fr}
  .app-nav{flex-direction:column;border-bottom:0;border-right:1px solid var(--border);padding:var(--space-4)}
  .app-main{padding:var(--space-6) var(--space-8)}
}
</style>
</head>
<body>
<div class="app">
  <nav class="app-nav" aria-label="Main" data-od-slot="nav">
    <a href="#" aria-current="page">Current place</a>
    <a href="#">Another place</a>
  </nav>
  <main class="app-main">
    <header class="app-toolbar" data-od-slot="toolbar">
      <h1>Screen title</h1>
    </header>
    <section data-od-state="default" data-od-slot="content"><!-- the populated screen --></section>
    <section data-od-state="empty" data-od-slot="empty" hidden><!-- what will be here, why it is empty, the first action --></section>
    <section data-od-state="loading" data-od-slot="loading" hidden aria-busy="true"><!-- a skeleton shaped like the content --></section>
  </main>
</div>
</body>
</html>
```
<!-- od:app-shell:end -->
