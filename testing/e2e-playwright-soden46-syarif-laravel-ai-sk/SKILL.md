---
name: e2e-playwright
description: Laravel E2E testing with official Playwright patterns for locators, auth state, seeds, traces, screenshots, CI, and cross-browser workflows.
tags:
  - laravel
  - php
---

# E2E Playwright

Use this skill when a Laravel task involves Playwright E2E tests, browser workflow coverage, regression tests, screenshots, traces, auth setup, or converting manual browser findings into durable tests.

Use the official `microsoft/playwright` repository as the source for current Playwright behavior when APIs, CLI, MCP, browser support, locators, traces, or configuration details matter: https://github.com/microsoft/playwright. Prefer the linked Playwright docs and API reference over remembered APIs.

## Workflow

1. Detect how the project runs Laravel, assets, queues, database, and browser tests: host, Sail, Docker, package manager, Vite, Playwright config, existing test helpers, and CI commands.
2. Reuse project-local Playwright patterns first: auth helpers, seed scripts, storage state, route helpers, page objects, fixtures, test IDs, screenshots, and trace settings.
3. Seed deterministic data through Laravel factories, seeders, HTTP setup routes, API helpers, or existing test bootstrap. Avoid fragile production-like data dependencies.
4. Write tests with user-facing locators first: `getByRole`, `getByLabel`, `getByText`, `getByPlaceholder`, and `getByTestId` only when semantic locators are not stable enough.
5. Prefer Playwright web-first assertions such as `toBeVisible`, `toHaveText`, `toHaveURL`, `toHaveValue`, and `toHaveScreenshot` over fixed sleeps.
6. Cover the high-value user workflow, not every implementation detail. Include success, validation failure, authorization-dependent UI, empty state, loading or queued state, and destructive confirmation when relevant.
7. Capture traces, screenshots, videos, or console/network evidence only when they help debug failures or support handoff.
8. Run the smallest meaningful Playwright command locally and report skipped browsers, missing services, or environment blockers explicitly.

## Laravel Setup Rules

- Authenticate through existing Laravel test helpers when available. If the project uses storage state, create it from a safe test user and never commit real cookies, tokens, or session files.
- Keep `.env`, credentials, tokens, private URLs, raw customer data, and real auth state out of tests, screenshots, traces, and fixtures.
- Use Laravel fakes for mail, notifications, queues, files, events, and HTTP integrations when the browser flow does not need the real external system.
- Wait for app-specific readiness: Vite assets loaded, Livewire requests settled, Inertia navigation finished, queued job state visible, fonts ready, and network idle only when it is meaningful.
- Add stable `data-testid` attributes only when accessible locators are not reliable and the project accepts test IDs.

## Playwright And Agent Browser

Use `ui-agent-browser` when UI/UX design or implementation is still being explored. Use `agent-browser` for low-token browser inspection, then convert the accepted workflow into Playwright when it should become a repeatable regression test.

## Completion Gate

Do not call Playwright coverage complete unless:

- the tested workflow is tied to real Laravel routes, Livewire actions, Inertia pages, or API contracts;
- deterministic setup and teardown exist or the dependency on local state is explicit;
- locators are resilient and user-facing where possible;
- assertions prove behavior and state, not only that the page loads;
- auth, validation, authorization, loading, empty, and success states are covered when relevant;
- screenshots/traces are enabled or captured where failure diagnosis needs them;
- the exact command run and any skipped checks are reported.

## Related Skills

- `using-laravel-standards`
- `ui-agent-browser`
- `responsive-ui-testing`
- `testing`
- `runner-selection`
