---
name: ui-agent-browser
description: Build and refine Laravel UI/UX/frontends with stack-aware implementation, backend contract alignment, Playwright handoff, and agent-browser inspection.
tags:
  - laravel
  - php
  - ui
  - ux
  - frontend
---

# UI Agent Browser

Use this skill when a Laravel task asks to build, redesign, implement, inspect, or judge frontend/UI/UX quality before the final responsive audit.

Treat the browser as the design surface and the backend contract as the source of truth. A UI is not done because the code compiles; it is done when the page communicates its purpose quickly, supports the real workflow, is wired to real routes or API contracts, and survives visual inspection in meaningful states.

## Workflow

1. Detect the target stack: Blade, Livewire, Inertia, Filament, Nova, Flux, Alpine, React, Vue, Tailwind, Bootstrap, component library, icon library, build tool, route structure, and test runner.
2. Inspect the existing frontend in a browser before designing: current route, layout shell, navigation, component language, visual density, interaction pattern, console errors, and rendered DOM or accessibility tree.
3. Read the backend surface that the UI must connect to: routes, controllers, Form Requests, policies, API Resources, DTOs, Inertia props, Livewire public state/actions, model relationships, events, files, and pagination.
4. Define the UI contract before styling: data needed, user actions, request payloads, validation errors, authorization-dependent controls, loading states, empty states, success states, and failure states.
5. Design to the detected stack, browser baseline, and project conventions. Reuse existing layouts, tokens, components, tables, forms, modals, navigation, and icons before introducing a new visual language.
6. Implement the UI in the target stack, wired to real backend routes, Livewire actions, Inertia props, or API clients. Avoid static-only screens unless the requested artifact is explicitly a mockup.
7. Inspect the result in a real browser with realistic data, screenshots, console output, interaction states, and at least mobile and desktop viewports.
8. Iterate on hierarchy, spacing, alignment, text fit, color, controls, and backend state mapping until the interface feels intentional and works through the real workflow.
9. Use `responsive-ui-testing` for the final viewport matrix when responsiveness, overflow, clipping, modals, tables, or visual regression matters.

## Browser Tool Strategy

Combine `agent-browser` and Playwright deliberately:

- Use the official `vercel-labs/agent-browser` repository as the source for current command behavior when agent-browser details matter: https://github.com/vercel-labs/agent-browser. Prefer its README or bundled `skills/agent-browser` guidance over remembered flags.
- Use the official `microsoft/playwright` repository as the source for current Playwright behavior when test, locator, browser, trace, CLI, or MCP details matter: https://github.com/microsoft/playwright. Prefer its README, docs, and API reference over remembered APIs.
- Use `agent-browser` for low-token exploration, quick interaction, screenshots, accessibility-tree snapshots, annotated screenshots, visual inspection, and short browser loops.
- Use Playwright for durable cross-browser tests, web-first assertions, resilient locators, auth setup, deterministic seeds, traces, screenshots in CI, regression coverage, and repeated workflows.
- Use `agent-browser read` on the active tab when rendered text/DOM is enough, then escalate to `snapshot` or screenshots only when structure or visual quality needs it.
- Prefer `agent-browser snapshot -i -c -d 5 --json` or a scoped selector snapshot for planning interactions; ask for full snapshots only when structure is genuinely unclear.
- Use annotated screenshots when visual layout, unlabeled icon buttons, canvas content, or spacing cannot be understood from the accessibility tree alone.
- Use `agent-browser batch --bail` for multi-step navigation, wait, snapshot, screenshot, and interaction flows to reduce command overhead.
- Use the default `agent-browser mcp` or `--tools core` profile when available; expand to `network`, `debug`, `react`, or `mobile` only when the task needs that surface.
- Fall back to Playwright when `agent-browser` is unavailable, when the project already has Playwright helpers, or when the result must become a committed test.

Use this division of labor:

- agent-browser discovers the current UI, explores states, captures compact evidence, and helps decide what to build.
- Playwright codifies the accepted workflow as repeatable browser coverage with `@playwright/test`, user-facing locators, isolation, deterministic data, traces, and screenshots.
- Convert agent-browser observations into Playwright assertions only after the UI/BE contract and visual behavior have stabilized.

## Backend Contract Alignment

Before implementing visible UI:

- Map every user action to a route, Livewire method, Inertia visit, form submit, API request, job trigger, file upload, or modal-only local action.
- Confirm required fields, validation rules, authorization rules, response shape, pagination metadata, filters, sort keys, and error format.
- Keep templates focused on rendering and interaction. Put queries, authorization, validation, side effects, and provider calls in Laravel boundaries.
- Use model-backed factories, seeders, fakes, or local API fixtures to make the browser state realistic without hardcoding fake UI-only data.
- Show backend states honestly: forbidden actions hidden or disabled, validation errors near fields, failed requests recoverable, queued/background work visible, and empty states useful.

## Design Rules

- Make the primary entity or task obvious in the first viewport.
- Prefer quiet, work-focused density for admin, CRM, ERP, SaaS, and operational pages.
- Use cards only for repeated items, modals, or genuinely framed tools. Do not nest cards inside cards.
- Keep section layouts full-width or unframed with constrained inner content.
- Use familiar controls: icon buttons for tool actions, tabs for view switching, segmented controls for modes, checkboxes or toggles for binary settings, menus for option sets, and inputs or sliders for numbers.
- Use the existing icon library when available. Prefer named icons over hand-drawn SVG controls.
- Keep border radii restrained unless the project design system says otherwise.
- Avoid one-note color palettes. Combine neutral surfaces with purposeful accent colors, semantic states, and enough contrast.
- Avoid decorative blobs, generic gradients, and stock-like visuals that do not clarify the product, place, object, or workflow.
- Do not add visible instructional copy that explains obvious UI mechanics. Let labels, affordances, grouping, and state do the work.

## Laravel UI Boundaries

- Use `blade-components-and-layouts` when the work touches reusable Blade layout or component structure.
- Use `livewire-development` when state, uploads, pagination, modals, filters, or dynamic interactions are Livewire-driven.
- Use `module-per-menu` when a multi-page admin app needs one page per module instead of conditional menu blocks in one Blade file.
- Use `e2e-playwright` when the browser workflow should become a durable test.
- Keep database queries, authorization, validation, and side effects out of templates.
- Build summaries, metrics, filters, tables, and select options from real model-backed data when the page is not a static mockup.
- Keep client names, private branding, internal URLs, sample customer data, phone numbers, and credentials out of reusable UI standards and screenshots intended for handoff.

## Browser Inspection Loop

When changing visible UI:

1. Start the project through its documented runner.
2. Visit the affected routes as the intended user role.
3. Capture screenshots for at least a narrow mobile viewport and a desktop viewport.
4. Check console errors, failed assets, missing fonts, broken images, hydration issues, and Livewire or Alpine errors.
5. Interact with primary controls, navigation, filters, forms, dropdowns, modals, pagination, and destructive confirmations.
6. Inspect the data contract while interacting: submitted payloads, response status, validation messages, optimistic updates, redirects, flash messages, and refreshed table or form data.
7. Re-check layout after loading, empty, validation-error, long-content, and success states when those states can be reached locally.

Do not rely only on static code review for visual quality.

## State Checklist

Cover the states that matter for the page:

- default data
- empty data
- long names, long translated strings, and large numbers
- loading or disabled controls
- validation errors
- success or flash messages
- unauthorized or hidden actions
- destructive confirmation
- filter or search results
- dark mode when supported

## Token Budget Rules

- Start with stack and contract discovery using `rg`, route lists, component names, and scoped browser snapshots.
- Prefer targeted file reads over loading whole frontend trees.
- Capture the existing frontend baseline with `agent-browser read`, scoped snapshots, or one screenshot before proposing broad UI changes.
- Prefer compact browser snapshots before screenshots; use screenshots when visual judgment matters.
- Keep browser evidence small: route, viewport, screenshot path, key console errors, and the exact failing or changed component.
- Convert repeated manual browser checks into Playwright only after the workflow stabilizes.

## Completion Gate

Do not call the UI finished unless:

- the page matches the existing project design language or intentionally introduces a coherent new one;
- the main workflow is visible and usable without reading explanatory text;
- frontend behavior is wired to the intended backend route, Livewire action, Inertia prop, or API contract;
- spacing, alignment, typography, icon use, and color look deliberate;
- text fits its containers on mobile and desktop;
- interactive states have been exercised in the browser;
- backend-driven states such as validation, authorization, loading, empty data, success, and failure are represented;
- screenshots or browser observations support the handoff;
- high-value or regression-prone browser flows are handed off to `e2e-playwright` when the project supports it;
- remaining visual risks are named explicitly.
