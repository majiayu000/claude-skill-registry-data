---
name: observability-harness
description: Add local-first observability for coding agents. Use when a repo needs logging conventions, request or correlation IDs, diagnostics, scripts/logs, scripts/diagnose, debugging docs, metrics/tracing guidance, or smoke-test diagnostics.
---

# Observability Harness

## Purpose

Make runtime behavior inspectable through local logs, diagnostics, and documented debugging paths before adding heavy external platforms.

Use `chrome-devtools-runtime-debugger` for browser console, network, DOM, accessibility, Lighthouse, responsive, or performance investigation.
Use `sprint-contract-observability` for process observability: sprint contracts, evaluator rubrics, and task traces.

## Inspect First

- logging utilities, request middleware, error handling, health checks, dev scripts, local runtime docs, tests, and production monitoring notes

## Procedure

1. Define observability basics.
   - Structured logs where appropriate.
   - Request or correlation IDs for request-based systems.
   - Standard error shape and debugging fields.

2. Add local diagnostics.
   - Create or update `scripts/logs`.
   - Create or update `scripts/diagnose` when repeatable diagnostics exist.
   - Link diagnostics from `scripts/healthcheck` when helpful.
   - Link browser runtime debugging to `docs/observability/browser-debugging.md` when Chrome DevTools MCP is relevant.

3. Document behavior.
   - `docs/observability/logging.md`
   - `docs/observability/debugging.md`
   - Metrics/tracing notes only when the repo uses them.
   - Link sprint contract and evaluator rubric docs when process observability is configured.

4. Keep it boring.
   - Prefer grep-able local logs before introducing external services.
   - Do not add observability vendors without explicit need.

## Validation

- Run log and diagnostic scripts when feasible.
- Confirm docs include expected log fields and local commands.
- Confirm failures produce actionable diagnostics.

## Completion Criteria

- Agents can inspect local runtime behavior and trace a failing request or workflow.
