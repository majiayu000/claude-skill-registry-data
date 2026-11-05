---
name: shop-retention-report
description: Analyze auto-repair shop CRM, customer, invoice, and service history for retention, repeat visits, customer cohorts, recency/frequency, average repair order or revenue per visit, declined-work recovery, service mix, tire-to-service cross-sell, dormant customers, review capture, and retention leakage. Use when the user asks for a customer retention report, CRM report, repeat-customer audit, shop economics review, declined-work analysis, or uploads Autolaborexperts/CRM/invoice/customer exports.
triggers: retention, repeat visits, customer cohorts, recency frequency, average repair order, revenue per visit, declined work, service mix, tire-to-service cross-sell, dormant customers, customers come back, crm invoices
---

# Shop Retention Report

Find where existing customers create durable value and where the shop is quietly losing repeat business.

## Workflow

1. Establish exact reporting period, history window, customer deduplication rules, invoice status definitions, and available fields.
2. Clean identity carefully before cohort analysis. Account for duplicate customer records, multiple vehicles, shared households, changed phone/email, and canceled/voided invoices.
3. Build core cohorts where data supports them:
   - new vs returning customers
   - one-and-done customers
   - 2+ visit repeat customers
   - dormant/lapsed customers by recency bands
   - tire-only vs service-only vs mixed customers
   - declined-work cohorts
4. Analyze economics:
   - completed visits/jobs
   - revenue and average revenue/repair order where valid
   - visits per customer
   - time to second visit
   - repeat revenue share
   - service/tire category mix
5. Analyze retention behavior over comparable cohorts rather than raw repeat-customer counts alone. Recent cohorts may not have had enough time to return.
6. Audit declined work and follow-up when available: value declined, age of opportunity, eventual recovery, and categories most likely to convert later.
7. Look for operational leakage: duplicate CRM records, missing contactability, poor follow-up, capacity delays, inconsistent recommendations, or review-request gaps.
8. Tie actions to measurable outcomes such as second-visit rate, reactivation rate, recovered declined work, visit frequency, ARO/revenue per customer, and review conversion.
9. Read `references/report-contract.md` and follow its output structure.

## Rules

- Do not call a new customer "lost" before a reasonable return window has elapsed for the service category.
- Do not use revenue alone as retention proof; mix and price changes can move revenue without better retention.
- Separate customer-level, vehicle-level, and invoice-level metrics.
- Never expose unnecessary customer PII in the report.
- State deduplication assumptions because duplicate CRM records can materially distort retention.

## Useful triggers

Examples: "run retention", "how many customers come back?", "audit declined work", "which customers are going dormant?", "is tire traffic turning into service customers?"
