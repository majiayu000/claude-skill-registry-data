---
name: orphex-merchant-feed-health-check
description: "Review destination-specific Merchant Center diagnostics and supplied feed-versus-site evidence to prioritize eligibility, price, stock, and data-quality repairs."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Merchant Feed Health Check

Review the supplied Merchant Center product data, destination-specific issues and matching website/checkout evidence. Eligibility issues and economic performance are different analyses.

## Establish product identity and freshness

Record merchant scope, target country/language, destination, stable item/variant ID, feed source/update, diagnostic/crawl timestamp, and site/checkout observation time. An item can have different status across destinations; keep unique item-destination rows and their denominators explicit. Do not call a partial export a complete catalog audit. Preserve account-level versus item-level issues and statuses exactly as supplied.

Check mismatches in price/currency/tax convention, availability, variant, link, required identifiers and attributes, images, and source precedence only when supporting evidence is present. Conditional identifier/variant/shipping requirements depend on product, country and destination; check current official requirements rather than inventing blanket GTIN, image-size or title rules. Do not invent identifiers or change in-stock/out-of-stock to gain eligibility.

A site observation and an eligible status can conflict because timestamps or definitions differ. Verify the exact variant, checkout and data source before calling a live regression or failed correction. Actual source errors, unsupported observations, and pending verification should be distinct. Do not fetch or modify private merchant data without the requested access scope.

Approval is a recorded destination-specific status, not evidence of actual impressions, clicks, or active delivery. Do not describe an approved item as serving unavailable inventory without matched delivery evidence. Preserve a supplied stock or price mismatch as a repair finding while keeping exposure and business impact unknown when delivery rows are absent.

A common snapshot capture time does not establish when the feed was updated, the site was crawled, or eligibility diagnostics were processed. Do not exclude update, crawl, or processing lag merely because observations were captured together. Request the relevant state timestamps and item/destination identity, and distinguish the confirmed value mismatch from its unresolved synchronization mechanism. Recheck the processed source and diagnostics after repair before claiming closure.

## Prioritize a repair queue

Rank actual disapprovals/limited eligibility, scope, business-provided importance, freshness and repair dependencies. Historical spend/revenue may describe exposure when correctly joined; it does not predict lost or recoverable sales. Feed coverage alone cannot explain a ROAS decline or prove incremental demand.

For each issue show item/destination, evidence, source of truth to inspect, proposed repair, owner if supplied, and recheck condition after update/crawl/diagnostics. Correct the upstream source rather than recommending conflicting manual edits blindly. Appeals, feed uploads, item exclusions and price/stock changes require explicit action scope. Finish with coverage limits and untested destinations.

## Official references

- [Merchant Center product data requirements](https://support.google.com/merchants/answer/7052112?hl=en)
- [Google product diagnostics](https://support.google.com/google-ads/answer/12097493?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.
