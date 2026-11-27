---
name: test-strategy
description: "Generate a risk-based test matrix for domain, EF integration, ASP.NET APIs, Blazor UI, MAUI and delivery."
---

# Build testing strategy
1. Extract acceptance criteria and all business invariants; list irreversible outcomes and data risks.
2. Write test matrix: unit/feature/API/DB/message/contract/UI/E2E/load/security/architecture by scenario and priority.
3. Prefer unit tests for pure rules, Testcontainers/real provider for EF, HTTP host for routes/security, device tests for MAUI.
4. Explicit cases: null/invalid, boundaries, permissions, cross-tenant, concurrency conflict, cancellation, retry/duplicate message, restore/backfill.
5. Define fixtures and test isolation; avoid time-dependent flakiness or production infrastructure.
6. Implement tests only if requested; otherwise return runnable test plan, commands and pass criteria.
7. After running, report executed test count and failed/skipped without pretending missing environments passed.
