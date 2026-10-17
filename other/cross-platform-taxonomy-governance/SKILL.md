---
name: cross-platform-taxonomy-governance
description: Govern campaign, ad group, line item, placement, creative, UTM, cost-center, and reporting naming across platforms so operations, billing, and analytics join cleanly. Use when the user asks for naming conventions, taxonomy, UTM governance, campaign codes, reporting keys, dashboard joins, or taxonomy cleanup.
---

# Cross-platform taxonomy governance

Taxonomy is not cosmetic. It is how the desk finds work, joins reports, reconciles billing,
audits launches, and explains campaigns to clients. A naming convention that only looks tidy
but cannot join to spend, tags, creative, and invoices is not a taxonomy.

This skill defines a cross-platform taxonomy operating model. It complements
`dv360-account-setup-and-taxonomy` by making the rule platform-neutral.

## When to use this skill

- A user asks for campaign naming, taxonomy, UTM standards, or reporting keys.
- A launch needs names, labels, cost centers, or codes approved.
- A dashboard, billing file, or reconciliation is failing because names do not join.
- The team needs to clean up old names without breaking live reports.
- A bulk taxonomy change is proposed.

## Core principles

- Names are for operators and humans. IDs and codes are for systems. Use both.
- Every token must have an owner, allowed values, and a reason.
- The taxonomy must work across campaign, ad server, analytics, warehouse, and billing.
- Do not encode values that change daily into the name. Use labels, reports, or metadata.
- Do not rename live entities without checking downstream reports and billing joins.

## Required token model

Use a local codebook, but keep these token groups available across platforms:

| Token group | Examples | Purpose |
| --- | --- | --- |
| Client or advertiser code | `acme` | Join to client and billing |
| Market or region | `us`, `ca`, `emea` | Geo reporting and budget pools |
| Objective | `awareness`, `traffic`, `leads`, `sales` | KPI and optimization logic |
| Funnel stage | `prospecting`, `retargeting`, `crm` | Audience and reporting logic |
| Channel or format | `display`, `video`, `ctv`, `audio`, `native`, `search` | Supply and creative grouping |
| Platform | `dv360`, `ttd`, `amazon`, `meta`, `tiktok`, `msads` | Cross-platform joins |
| Flight or quarter | `2026q3`, `jul2026` | Calendar grouping |
| Campaign code | `cmp00123` | Stable join key |
| Creative or test code | `cr001`, `hook-a` | Asset and test reads |
| Cost center or PO | `po4567` | Billing and finance |

## Naming pattern

Choose one delimiter, usually `_`, and prohibit free-form punctuation.

```text
client_market_objective_funnel_channel_platform_flight_campaigncode
acme_us_sales_retargeting_video_dv360_2026q3_cmp00123
```

Shorten only through the codebook. Do not let teams invent one-off abbreviations inside the
platform.

## UTM pattern

Use lowercase, stable values. Match UTM values to the platform taxonomy where possible.

```text
utm_source=platform
utm_medium=paid_media
utm_campaign=campaigncode
utm_content=creativecode
utm_term=audience_or_keyword_code
```

If the landing-page analytics team has a different source or medium standard, adopt that
standard rather than forcing a media-only convention.

## Core process

1. **Confirm downstream consumers.** Identify who needs the taxonomy: trader, ad ops,
   analytics, billing, client reporting, finance, creative, and data engineering.
2. **Define allowed values.** Create a codebook for each token. Include spelling, allowed
   abbreviations, owner, and examples.
3. **Map platform limits.** Some platforms have name length limits, label limits, or fields
   that do not export cleanly. Use stable IDs or labels where the name cannot carry the token.
4. **Validate before launch.** Every launch QA should check taxonomy fields before go-live.
   Invalid taxonomy is a launch blocker if it breaks reporting, billing, or automation.
5. **Govern changes.** New values require an owner and date. Deprecated values stay in the
   codebook until no active reports depend on them.
6. **Bulk changes safely.** Any live rename or taxonomy backfill runs through
   `bulk-change-governance-and-rollback`.

## Taxonomy acceptance checks

- All required tokens are present and valid.
- Values are lowercase unless the platform requires otherwise.
- No spaces, special punctuation, or one-off abbreviations.
- Campaign code and creative code match the source plan.
- UTM campaign and content join to reporting keys.
- Cost center or PO is present when billing requires it.
- No live rename is made without a downstream impact check.

## Common pitfalls

- Treating taxonomy as a naming style exercise rather than a reporting and billing contract.
- Encoding objective in some platforms and not others, then losing cross-platform reporting.
- Renaming live campaigns to fix cosmetics and breaking dashboard history.
- Letting each client team define `vid`, `video`, and `olv` differently.
- Using free-text creative names as the only asset identifier.

## Related artifacts

- `templates/ops/taxonomy-convention.csv`
- `tools/utm_builder.py`
- `dv360-account-setup-and-taxonomy`
- `marketing-analytics-warehouse-and-dashboards`
- `programmatic-month-end-close`
- `bulk-change-governance-and-rollback`
