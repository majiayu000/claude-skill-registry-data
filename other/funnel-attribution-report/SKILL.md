---
name: funnel-attribution-report
description: Reconcile cross-system marketing and sales attribution from traffic/ad/search/social sources through website events, calls, Vapi, bookings, CRM, completed jobs, and revenue. Use when the user asks where leads or revenue came from, whether tracking is trustworthy, why platform conversions disagree, how many leads are lost between systems, or wants an attribution/data-integrity audit across GSC, Meta CAPI, GA/website, phone, CRM, and business outcomes.
triggers: attribution, where leads came from, where revenue came from, tracking trustworthy, meta leads vs crm, trace calls to revenue, dropping out, conversion funnel, ad sources, website events, bookings
---

# Funnel Attribution Report

Audit both the customer funnel and the measurement system used to describe it.

## Workflow

1. Define the business funnel and exact reporting period before comparing counts.
2. Inventory systems and identifiers.
   - traffic/source identifiers
   - click IDs/UTMs when present
   - session or lead IDs
   - event_id or server/browser identifiers
   - phone/call IDs
   - appointment/CRM/customer IDs
   - invoice/job/order IDs
3. Map each stage and its source of truth:
   - exposure/visit -> intent event -> lead/contact -> qualified lead -> booking/order -> arrival/completion -> revenue -> repeat/review.
4. Reconcile counts between adjacent stages. Explain legitimate differences such as attribution windows, timezones, repeat interactions, modeled conversions, spam, cancellations, offline completion, and deduplication.
5. Find measurement defects:
   - double-counted events
   - missing server/browser events
   - overwritten UTMs
   - lost click IDs
   - calls without source mapping
   - booking/CRM records with no originating lead
   - platform conversions without backend receipts
   - revenue records that cannot be joined back to acquisition
6. Find operational leakage separately from tracking leakage. A missing booking can be a sales/process problem even when attribution is perfect.
7. Quantify uncertainty. Use ranges or unresolved counts rather than false precision.
8. Read `references/report-contract.md` and follow its output structure.

## Rules

- Never force a single-source attribution story when the evidence supports multi-touch or unknown origin.
- Never reconcile by changing definitions silently.
- Preserve source-system counts and show derived reconciliations separately.
- Prefer deterministic joins; label probabilistic or heuristic matching.
- Protect customer-level data in outputs.

## Useful triggers

Examples: "audit our attribution", "why does Meta say 80 leads but CRM says 42?", "trace calls to revenue", "where are customers dropping out?", "can we trust our conversion numbers?"
