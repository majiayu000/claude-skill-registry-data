---
name: meta-capi-health-report
description: Audit Meta Conversions API (CAPI) and browser/server event tracking for signal quality, event coverage, deduplication, event match quality, freshness, diagnostics, parameter completeness, attribution readiness, and broken or duplicate events. Use when the user asks for a CAPI report, Meta Events Manager audit, Pixel/CAPI health check, tracking diagnosis, conversion-event review, or provides Meta diagnostics/screenshots/exports/logs for analysis.
triggers: meta conversions api, capi, pixel, event tracking, deduplication, event match quality, events manager, duplicate events, browser and server events, signal quality, attribution readiness, diagnostics
---

# Meta CAPI Health Report

Determine whether Meta is receiving trustworthy conversion signals and whether those signals represent real business outcomes.

## Workflow

1. Establish account/pixel/dataset, domain/app, exact date range, environment, and current event inventory.
2. Use current Events Manager/API/log evidence when authorized. Otherwise analyze exports, screenshots, payload samples, server logs, or test-event receipts.
3. Inspect current schema and diagnostics instead of assuming fixed Meta labels or thresholds.
4. Build an event inventory.
   - Event name and business meaning.
   - Browser, server, or both.
   - Volume and trend.
   - Event source URL/context where available.
   - Parameters and customer-information fields present.
   - Downstream business receipt if one exists.
5. Audit signal integrity:
   - browser/server coverage
   - deduplication and event_id consistency
   - duplicate or inflated conversions
   - event freshness/delay
   - match-quality indicators when supplied by Meta
   - malformed or rejected events
   - missing required/recommended parameters
   - test/staging contamination
   - event names that do not correspond to meaningful business actions
6. Reconcile funnel logic. A Lead, Schedule, Purchase, or custom event must have an explicit trigger definition and ideally a source-of-truth receipt.
7. Compare event counts across browser, server, site/backend, call/booking systems, CRM, and invoices when available. Explain expected differences before calling a mismatch a defect.
8. Distinguish delivery health from advertising performance. Good CAPI does not prove good ads; weak CAPI can make ad optimization and measurement less reliable.
9. Read `references/report-contract.md` and follow its output structure.

## Rules

- Never display access tokens, hashed identifiers, phone numbers, emails, IP addresses, or other unnecessary user-level data.
- Do not recommend sending data to Meta that the business is not permitted to send.
- Do not claim a high match-quality score proves accurate conversion semantics.
- Verify current Meta documentation when platform-specific requirements, diagnostics, or recommended fields materially affect the conclusion.

## Useful triggers

Examples: "audit CAPI", "is Pixel + CAPI working?", "why are Meta conversions duplicated?", "check our Events Manager diagnostics", "compare browser and server events".
