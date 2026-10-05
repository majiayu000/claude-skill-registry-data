---
name: tdd-playwright-workflow
description: Drive changes through TDD with unit tests and Playwright e2e tests. Use when a bug fix or feature should start with a failing reproduction, when browser workflows need e2e coverage, or when Playwright setup/test wrappers are needed.
---

# TDD Playwright Workflow

## Purpose

Make implementation evidence-driven: reproduce the behavior first, make the smallest fix, then prove the user workflow works through unit and e2e tests where appropriate.

## Inspect First

- existing test runners, Playwright config, browser test directories, fixtures, package scripts, CI, and user workflow docs
- changed behavior, bug reports, and product acceptance criteria

## Procedure

1. Choose the reproduction layer.
   - Unit test for pure logic, validation, formatting, reducers, and domain behavior.
   - Integration test for API, database, service collaboration, or contract behavior.
   - Playwright e2e for complete browser workflows such as create, edit, delete, checkout, login, or publish.

2. Write the failing test first.
   - For bug fixes, add the failing reproduction before changing production code unless impossible.
   - If impossible, document why in PR/final validation notes.
   - Use `assets/templates/tdd-bug-reproduction.md.tmpl` for notes.

3. Implement minimally.
   - Make the reproduction pass.
   - Avoid unrelated refactors during red/green.
   - Use `typescript-monorepo-clean-code` if cleanup is needed after behavior is green.

4. Add or verify Playwright.
   - Use existing Playwright setup when present.
   - Add Playwright only when the task accepts browser e2e tooling.
   - Use `assets/templates/playwright-e2e.spec.ts.tmpl` as a starting point.
   - Ensure `scripts/test-e2e` exists when e2e tests are part of the repo contract.
   - Keep unit and e2e discovery separate. In Bun repos, do not let `bun test` discover Playwright `*.spec.ts` files; narrow `scripts/test` to unit/integration paths or place Playwright files under an ignored e2e pattern.
   - Ignore Playwright output directories such as `test-results` and `playwright-report` in repo linters/formatters.
   - Use `$click-path-and-browser-qa` to inventory routes, controls, accessible names, and missing lifecycle coverage before broad UI test work.

5. Validate the loop.
   - Run the narrow failing test, then relevant broader tests.
   - Use `chrome-devtools-runtime-debugger` for runtime-only console, network, layout, or performance investigation.
   - Record completion evidence through `termination-gatekeeper` and feature evidence through `feature-state-machine` when present.

## Validation

- Show red/green evidence when feasible.
- Run unit and/or Playwright commands that cover the change.
- Run `./scripts/test` and `./scripts/validate` when the change is broad.
- After running Playwright, rerun `./scripts/test` or `./scripts/validate` to confirm e2e output and file globs did not break baseline validation.

## Completion Criteria

- Feature or bug behavior is covered at the narrowest useful layer.
- Browser lifecycle changes have Playwright or a documented reason e2e is not feasible.
- Validation evidence names exact commands and outcomes.
