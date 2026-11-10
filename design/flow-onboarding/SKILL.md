---
name: flow-onboarding
zh_name: "新手引导流程"
en_name: "Onboarding Flow"
emoji: "👋"
description: "A linked first-run flow: welcome, goals, permissions with the reason before the system prompt, and an optional paywall, as one collection."
en_description: "A linked first-run flow: welcome, goals, permissions with the reason before the system prompt, and an optional paywall, as one collection."
category: app
scenario: design
tags: ["onboarding", "first run", "welcome", "permissions", "goals", "引导"]
triggers:
  - "onboarding flow"
  - "first run flow"
  - "welcome flow"
  - "app onboarding"
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
  example_prompt: "The first-run flow of a habit tracker on Android: welcome, pick your goals, allow notifications with the reason, then a Pro trial offer the user can skip."
---

<!-- Kit skill (openspec add-app-screens). -->
# Onboarding Flow

A flow pack: one collection of linked screens, each with its branches, made in one ask. Build every screen from the app screen patterns' shell and rules (below), one artifact per screen.

## Screens

| Screen id | Title | What it holds |
|---|---|---|
| `welcome` | Welcome | what the app does for this user in one sentence; one primary action; sign-in link for returning users |
| `goals` | Your goals | two to six choices that change the app; a skip option |
| `permissions` | Allow notifications | why, in the user's terms, before the system dialog; "Not now" as a real choice |
| `paywall` | Try Pro | optional: see the paywall pack's rules; a visible way to continue free |
| `home` | Home | the first real screen, already shaped by the goals; ends the flow |

Main path: `welcome` → `goals` → `permissions` → `paywall` → `home`. Add the branches each screen lists as its own `data-od-state` frames or, when a branch is a whole screen, as a screen.

## Workflow

1. **Ask once, at most three questions, together:** which branches to include, which platform (web app, iPhone, Android), and the product name if the brief doesn't give it. Accept "you pick". Never more than eight screens.
2. **Plan the flow before the first screen.** Pass `flow` to `prepare_open_design_brief` on every screen: the screens above (trimmed to the user's choice), the links between them (from, trigger label, to) and the shared navigation if the flow has one. Use the same `collectionId` and the screen id as `screenRole`.
3. **Build each screen** with its own `prepare_open_design_brief` call, then register it with the same `collectionId`, `screenRole` and `flow`.
4. **Check the collection** with `check_open_design_artifact` and `collectionId`, fix flow findings (broken links, dead ends, unfilled screens, navigation drift, store rules), then show the flow map.

## Rules for this flow

- Every step has a progress indicator and a way back, except the welcome screen.
- Never ask for a permission before showing why; the system prompt comes only after the user taps the primary button on the permissions screen.
- Mark the end screen with `data-od-end`.

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
