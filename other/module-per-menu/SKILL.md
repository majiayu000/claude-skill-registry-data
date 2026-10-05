---
name: module-per-menu
description: Build Laravel projects with one menu or page per module, using small controllers, per-page views, shared layouts/components, and dynamic DB-backed data.
tags:
  - laravel
  - php
---

# Module Per Menu

Use this skill whenever creating, copying, refactoring, or expanding a Laravel web application with multiple menus, pages, dashboards, reports, or admin screens.

Default to a module-per-menu structure unless the existing project already has a stronger convention.

## Standard Pattern

Use this shape for Laravel apps with menus or pages:

```text
Route -> Small Page/Resource Controller -> Action/Service/Query Service when needed -> Eloquent -> View/API Response
```

Organize UI work so one menu or page maps to one clear module:

```text
app/Http/Controllers/<Domain>/
  AuthController.php
  DashboardController.php
  GateInController.php
  GateOutController.php
  CustomerController.php
  ReportController.php

app/Services/<Domain>/
  DashboardReportService.php
  BillingService.php
  DailyReportService.php

resources/views/<domain>/
  layouts/app.blade.php
  pages/dashboard.blade.php
  pages/gate-in/index.blade.php
  pages/gate-in/create.blade.php
  pages/gate-out/index.blade.php
  pages/gate-out/process.blade.php
  components/filters.blade.php
  components/table.blade.php
```

## Controller Rules

- Keep controllers small and readable.
- Create one controller per menu, page group, or resource boundary.
- Let controllers orchestrate HTTP only: receive request, call validation/authorization, call service/action/query, return view/redirect/JSON.
- Move repeated query/report calculations to a Service or query object.
- Move multi-step writes to Actions or Services with explicit transactions when needed.
- Do not put unrelated menus into one controller just because they share a layout.
- Do not use one giant `PageController` or one giant `DepoWebController` for a full admin system.

## View Rules

- Use one Blade view per page or page state.
- Use a shared layout for sidebar, topbar, shell, asset loading, and page header.
- Use Blade components or partials for repeated filters, tables, badges, stats, modals, and form controls.
- Keep page Blade files focused on rendering one menu/page.
- Do not put all menus into one Blade file with large `@if ($active === ...)` blocks.
- Keep display data dynamic from Eloquent/model-backed services. Avoid hardcoded metrics except placeholders explicitly marked as prototype/demo.

## Route Rules

- Keep route files as mappings only.
- Use route groups for middleware, prefixes, and shared names.
- Place static routes before broad parameter routes.
- Prefer invokable controllers for single-page modules and normal controllers for page groups.
- Add route/render tests for every important menu or page.

## Dynamic Data Rules

- Build page metrics, summaries, charts, tables, and select options from database queries or model-backed services.
- Derive counts and totals from Eloquent collections or queries instead of duplicating numbers in Blade.
- Use Services for dashboards, financial reports, daily reports, billing quotes, sync contracts, or other reusable calculations.
- Keep seeded/demo data in seeders and factories, not embedded in views.

## Verification

Before handoff, run the smallest meaningful checks available:

- route list for changed route groups;
- feature tests that open each authenticated menu/page;
- API contract tests for new endpoints;
- `php artisan test`;
- Blade compile check such as `php artisan view:cache` followed by `php artisan view:clear`;
- frontend build when assets changed.

Report any checks that cannot run and why.
