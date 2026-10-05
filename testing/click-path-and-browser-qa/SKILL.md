---
name: click-path-and-browser-qa
description: Inventory and validate user-facing browser workflows with click-path evidence, accessible controls, Playwright coverage, console/network checks, and lifecycle verification. Use for UI work, web regressions, shadcn/ui changes, todo-style create/edit/delete flows, or browser acceptance testing.
---

# Click Path And Browser QA

## Purpose

Make browser-facing behavior testable by mapping important user paths to controls, routes, expected state changes, and verification evidence.

## Inspect First

- app routes, pages, components, forms, buttons, links, dialogs, and Playwright tests
- `docs/development/ui.md`, observability/debugging docs, and existing browser QA reports
- local runtime scripts and healthcheck commands

## Procedure

1. Inventory click paths.
   - Run `scripts/inventory_click_paths.py <repo> --json` when available.
   - Identify routes, forms, buttons, links, and missing accessible names.
   - Prioritize create/edit/delete/filter or equivalent user lifecycles.
   - Add `scripts/click-path-audit` when UI surfaces are part of the repo validation contract.

2. Define browser evidence.
   - Use `assets/templates/click-path-audit.md.tmpl` or `browser-qa-report.md.tmpl`.
   - Map each path to expected state, data persistence, error handling, and validation command.

3. Validate with the right tool.
   - Prefer Playwright for repeatable lifecycle checks.
   - Use `$chrome-devtools-runtime-debugger` for console, network, DOM, performance, or accessibility investigation.
   - Use `$tdd-playwright-workflow` when fixing a bug with a failing browser reproduction first.

4. Record gaps.
   - Missing e2e coverage, inaccessible icon-only controls, untested destructive actions, and console errors should become review findings or follow-up tasks.
   - When trajectory tracing exists, record UI and browser-evidence risk surfaces so `$trajectory-risk-supervisor` can distinguish tested from untested UI work.

## Validation

- Run the narrow Playwright/browser command when available.
- Run `./scripts/click-path-audit` when the wrapper exists.
- Confirm key controls have accessible names.
- Confirm browser findings include route, action, expected result, actual result, and evidence.

## Completion Criteria

- Critical user paths are inventoried and have browser or Playwright evidence.
- UI workflow gaps are documented with concrete follow-up commands.
