---
name: cypress-testing
description: "Cypress web testing, custom commands, network stubbing with cy.intercept, and flaky retry policies."
---

# Cypress E2E Testing Protocol

1. Intercept network endpoints with cy.intercept() for deterministic state.
2. Use custom commands (cy.loginByApi) to bypass slow UI setup flows.
3. Assert visible UI changes rather than waiting on timers.
