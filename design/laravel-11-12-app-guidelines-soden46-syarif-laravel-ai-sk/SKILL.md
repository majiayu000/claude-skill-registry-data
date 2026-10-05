---
name: laravel-11-12-app-guidelines
description: Work in Laravel 11 or 12 apps with stack detection, Boost-aware docs lookup, frontend conventions, tests, and Pint formatting.
tags:
  - laravel
  - php
---

# Laravel 11/12 App Guidelines

Use this skill when implementing, fixing, or reviewing Laravel 11 or Laravel 12 applications.

## Start Here

1. Read repository instructions and local docs before making architectural decisions.
2. Confirm Laravel and PHP versions from `composer.json`, `composer.lock`, or `php artisan about` when available.
3. Detect whether commands should run through Sail, Docker Compose, Herd, Valet, or host PHP.
4. Detect app mode: API-only, Blade, Livewire, Inertia, Vue, React, or a mixed legacy stack.
5. Reuse existing conventions for naming, language, layout, components, testing, and error responses.

## Laravel 11/12 Conventions

- Configure middleware, exception handling, and routing in `bootstrap/app.php` when the app follows the modern skeleton.
- Register service providers through `bootstrap/providers.php` when that file exists.
- Place scheduled commands in `routes/console.php` unless the project has an explicit scheduler abstraction.
- Prefer named routes and `route()` generation for internal links and redirects.
- Use Form Requests for non-trivial HTTP validation and request-bound authorization.
- Use API Resources for public JSON response shape when the repo already follows resource patterns.
- Ask before destructive database commands such as `migrate:fresh`, `db:wipe`, reset, rollback, or seed operations that overwrite data.

## Stack-Specific Notes

- API-only apps: work in `routes/api.php`, follow the existing auth stack, and avoid frontend build assumptions.
- Inertia apps: use existing page/component locations and server-side route conventions; prefer the project's form helper pattern.
- Livewire apps: pair this with `livewire-development`.
- Blade apps: keep templates presentational and move reusable decisions out of views.
- Tailwind v4 apps: follow the existing token and import pattern; avoid deprecated utility names when editing nearby UI.
- Wayfinder apps: follow existing generated route import patterns and regenerate route artifacts when the project requires it.

## Laravel Boost

When Laravel Boost MCP tools are available, use them to reduce guessing:

- search Laravel ecosystem docs before changing framework-specific behavior;
- list Artisan commands before assuming command options;
- inspect routes before adding overlapping routes;
- use read-only database inspection for debugging query shape;
- inspect browser logs for frontend failures.

If Boost is unavailable, fall back to local project files and official Laravel documentation.

## Verification

Run targeted tests first, then formatting or static checks that match the touched area. Prefer `vendor/bin/pint --dirty` for changed PHP files when available.
