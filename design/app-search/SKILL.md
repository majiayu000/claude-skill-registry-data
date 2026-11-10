---
name: app-search
zh_name: "搜索页"
en_name: "App Search"
emoji: "🔍"
description: "A search screen: query field, filters, grouped results with highlights, recent searches, and its no-results and loading states, inside the app shell."
en_description: "A search screen: query field, filters, grouped results with highlights, recent searches, and its no-results and loading states, inside the app shell."
category: app
scenario: design
tags: ["search", "results", "filters", "find", "command palette", "搜索"]
triggers:
  - "search page"
  - "search screen"
  - "search results"
  - "results page"
  - "command palette"
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
  example_prompt: "Search across a knowledge base app: query box, filters by type and author, results grouped into Articles and People, and a no-results state."
---

<!-- Kit skill (openspec add-app-screens). -->
# App Search

Produce the screen where users look something up and pick a result.

## Workflow

1. **Query field** at the top, wide, with the query echoed in it and a clear button. Keyboard hint if there is one ("⌘K").
2. **Filters** as chips or a short side panel showing their current values and the count of each, from the results actually shown.
3. **Results** grouped by type when there are several (Articles, People, Files), each result with its title (query terms highlighted), its type, one line of context and where it lives.
4. **Before a query:** recent searches and suggested starting points, not a blank page.

## States

- `default`: results for a realistic query.
- `empty`: no results: echo the query, suggest a spelling or a broader filter, and offer a way to create or ask.
- `loading`: result-shaped skeletons below the query.

## Self-check

- Result counts, filter counts and the results on screen agree.
- The highlighted terms are the ones in the query field.

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
