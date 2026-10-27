---
name: blazor-interactive-ssr-adhoc-testing-playwright-cli
description: Specialized for ad-hoc testing Blazor web apps in interactive server render mode with SignalR using playwright-cli. Use when performing quick tests on Blazor components, real-time updates, forms, and UI interactions in server-rendered applications.
version: 2.0.0
---

# Blazor Interactive SSR Ad-Hoc Testing

Extends the `playwright-cli` skill for exploratory, in-development testing of Blazor apps running in interactive server render mode (interactive SSR) with SignalR. Focus is on quick, manual validation — not CI/CD automation.

## Scope

**Covers**: ad-hoc E2E workflows, component interaction, SignalR-driven UI updates, form/validation testing, basic visual and performance checks.

**Does not cover**: automated test suites (use Playwright Test Framework), unit/component testing (xUnit/bUnit), load/security/accessibility testing, or production E2E.

## Key Considerations for Blazor Server Mode

- **SignalR**: Always wait for the WebSocket connection before testing interactions. Check `window.Blazor._internal.dotNetObject !== undefined`.
- **Async rendering**: Elements update asynchronously; use `eval` to assert DOM state after actions rather than relying on timing.
- **Component lifecycle**: Test mounting, updates, and disposal; watch for circuit disconnection errors.
- **Console monitoring**: Use `playwright-cli console` to catch Blazor-specific errors (circuit disconnections, rendering exceptions).

## Testing Strategies

Seven strategies cover the common Blazor ad-hoc testing scenarios. Detailed workflows with bash examples are in [references/strategies.md](references/strategies.md).

| # | Strategy | When to use |
|---|----------|-------------|
| 1 | **Connection and Initial Load** | Verify SignalR connects and components render |
| 2 | **Component Interaction and State** | Test clicks, server state changes, and UI updates |
| 3 | **Real-Time Data Sync** | Validate SignalR-pushed data updates in UI |
| 4 | **Form Submission and Validation** | Test form fill, submit, success/error handling |
| 5 | **Error Scenarios and Recovery** | Test circuit disconnection and reconnection |
| 6 | **Visual Regression Verification** | Snapshot/DOM checks for unintended visual changes |
| 7 | **Basic Performance Assessment** | Tracing and responsiveness checks |

Read [references/strategies.md](references/strategies.md) for the workflow commands for any strategy above.

## Quick Examples

```bash
# Verify Blazor and SignalR loaded
playwright-cli open https://localhost:5001
playwright-cli eval "window.Blazor !== undefined"
playwright-cli network

# Click + assert state change
playwright-cli click e5
playwright-cli eval "document.querySelector('.counter-value').textContent.includes('1')"
playwright-cli snapshot

# Form fill and submit
playwright-cli fill e2 "user@example.com"
playwright-cli click e3
playwright-cli eval "document.querySelector('.success-message') !== null"
```

## Best Practices

- Read [references/strategies.md](references/strategies.md) before starting — pick the strategy that matches your goal.
- Use `eval` assertions immediately after interactions to avoid race conditions with SignalR updates.
- Always run `playwright-cli console` and `playwright-cli network` when debugging connection issues.
- For repeated validations (>3 runs), convert to a proper Playwright test script.
- Reference the `playwright-cli` skill for the full command reference and session management.
