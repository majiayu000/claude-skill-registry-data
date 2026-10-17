---
name: dv360-account-setup-and-taxonomy
description: Stand up and govern a Display & Video 360 account structure the right way. Use when the user asks how to set up a partner or advertiser, what lives at the partner versus the advertiser, user roles and permissions, least privilege, a naming convention or taxonomy, account governance, shared brand-safety exclusion lists, default targeting, audience naming, change management, or archiving.
---

# DV360 account setup and taxonomy

Set up the account hierarchy, access model, and naming discipline that everything else depends on. Get this right once and reporting rolls up cleanly, automation by structured data file works, and access stays least privilege. Get it wrong and you pay for it on every campaign.

For definitions of partner, advertiser, insertion order, line item, and the bid math, see the `programmatic-foundations` skill. This skill is the operational playbook for standing the structure up and governing it.

## When to use this skill

Use this skill when the task is account architecture or governance:

- Creating or organizing a partner or advertiser, or deciding what belongs where.
- Granting access, choosing a role, or auditing who can do what.
- Defining or enforcing a naming convention across campaigns, insertion orders, line items, creatives, and audiences.
- Setting up shared brand-safety exclusions, default targeting, creative approval, or audience naming.
- Change management and archiving policy.

Boundaries with sibling skills:
- How to lay out campaigns, insertion orders, and line items for a specific brief: see `dv360-campaign-architecture`.
- Configuring brand suitability and frequency on live campaigns: see `dv360-frequency-and-brand-safety`.
- The pre-launch checklist that enforces this taxonomy at go-live: see `dv360-launch-qa`.
- Running bulk edits and the API or structured data file workflow: see `dv360-api-and-sdf-automation`.

## Quick reference: what lives where

| Concern | Partner level | Advertiser level |
| --- | --- | --- |
| Billing profiles, currency, timezone, partner costs | Yes | Inherits |
| Partner-wide default targeting (copied into new campaigns, IOs, line items) | Yes | Can override |
| Users with partner scope (see all advertisers below) | Yes | Narrower scope here |
| Shared deals and central deal management | Yes | Consumes |
| Floodlight and the Campaign Manager 360 link | No | Yes (the advertiser is the link point) |
| Brand controls and brand-safety exclusions | Inherited defaults | Yes (apply across all line items) |
| Creatives, conversion pixels, content channels, targeting templates | No | Yes |
| First-party audiences | Auto-shared down to advertisers | Created and consumed here |

Partner properties (name, timezone, currency, billing profiles, and partner-wide default targeting) are inherited by every advertiser under the partner. Conversion measurement attaches at the advertiser: in most setups the Floodlight configuration is parented in Campaign Manager 360 and the DV360 advertiser links to it.

## Core process

1. **Decide the partner and advertiser map before creating anything.** One partner per billing and trading entity (an agency, a trading desk, or a large direct advertiser). One advertiser per real-world business or brand that needs its own Floodlight, creatives, and brand controls. Do not split one brand across advertisers for convenience, because audiences, brand controls, and conversion data do not move freely across advertisers and you will fragment measurement.
2. **Set partner-level controls once.** Billing profiles, currency, timezone, partner costs, and partner-wide default targeting. These cascade, so set conservative defaults (for example, a default brand-safety posture) that every new advertiser inherits.
3. **Create each advertiser and wire measurement.** Link the Campaign Manager 360 advertiser or Floodlight configuration so conversions and creatives resolve. Confirm the timezone and currency match the billing intent before any spend.
4. **Build the access model on least privilege.** Map who needs what, assign the narrowest role at the narrowest scope that lets each person do their job, and prefer advertiser-scoped roles over partner-scoped admin. See `references/roles_and_permissions.md` for the full role matrix.
5. **Adopt one documented naming convention** across campaign, insertion order, line item, creative, and audience before the first campaign is built. Pick a delimiter, an ordered set of fields, and a controlled vocabulary for each field. See `references/taxonomy_template.md` and emit it as the team standard.
6. **Set governance defaults at the advertiser:** brand-safety exclusion lists, default targeting, creative approval expectations, and audience naming rules. Document a change-management and archiving policy so the structure stays clean over time.
7. **Audit on a cadence.** Quarterly, review users and roles for least privilege, confirm naming compliance on recent entities, and archive finished campaigns so active views stay readable.

## Decision rules and thresholds

- **One partner per billing entity, one advertiser per brand.** If two teams bill separately, they are two partners. If one brand needs a wall between two markets but shares billing, prefer two advertisers under one partner, not two partners.
- **Default to read-only or reporting-only.** Grant a role that can edit live spend (Standard or Admin) only to people who traffic or manage campaigns. Stakeholders and analysts get Reporting only.
- **Partner-level Admin is rare.** It can edit every advertiser and manage users. Keep the count low and named. Day-to-day traders get advertiser-scoped Standard.
- **Only Admin, Standard, and Read only have API access.** If a person or service account drives the API or structured data files, it needs one of those three roles. Scope a service account to the single advertiser it automates, not the whole partner.
- **Brand-safety exclusions live at the advertiser and apply to all line items.** Set the floor centrally rather than re-entering exclusions per line item, which drifts. Use a structured data file to apply or audit them in bulk.
- **Default targeting cascades, so set it deliberately.** A partner-wide default is copied into every new campaign, insertion order, and line item. A wrong default silently mis-targets new builds.
- **Name before you build.** A new entity that does not match the convention is corrected at creation, not after, because renaming after reporting has accrued breaks historical filters and dashboards.
- **Archive, do not delete, finished work.** Archiving pauses and hides an entity while keeping its data for reporting. Use it to keep active views clean.

## Naming convention and taxonomy governance

A naming convention is not cosmetic. Names are the join keys for reporting, the filters analysts pivot on, and the values that structured data file automation reads and writes. One inconsistent field breaks a dashboard or a bulk edit.

A workable convention has three parts:
- **A single delimiter** used everywhere (for example, a pipe `|` or underscore `_`), chosen so it never appears inside a field value.
- **An ordered set of fields**, the same order on every entity type, most-stable field first (advertiser or brand) to most-specific last (tactic or creative variant).
- **A controlled vocabulary** per field: a fixed, documented list of allowed values and abbreviations, so "Q3" never competes with "Q03" or "Quarter3".

Apply the same field order across campaign, insertion order, line item, creative, and audience so a name read at any level tells you the brand, market, objective, funnel stage, channel, and flight at a glance. Put the full template, the field list, the controlled values, and a worked example name in `references/taxonomy_template.md` and emit it as the team standard.

## Governance

- **Shared brand-safety exclusion lists.** Maintain the exclusion floor (digital content labels, sensitive categories, blocked URLs and apps, keyword exclusions, authorized-seller posture) at the advertiser so it applies across all line items. Keep one source-of-truth list per advertiser and apply or audit it in bulk with a structured data file. Tune brand suitability per campaign in `dv360-frequency-and-brand-safety`.
- **Default targeting.** Decide what cascades from the partner and what each advertiser overrides, and document it so a trader knows what is inherited versus set.
- **Creative approval.** Creatives are reviewed automatically against policy on create or edit and cannot serve until the status is Servable or Approved. Build approval lead time into every launch and assign creatives to line items early so review starts.
- **Audience naming.** Audiences auto-share from the partner down to advertisers, so a vague audience name pollutes every advertiser. Hold audiences to the same controlled vocabulary as everything else.
- **Change management.** Require that structural changes (new advertisers, role grants, default-targeting edits, exclusion-list edits) follow the documented convention and are logged. Pair this with the `dv360-launch-qa` sign-off so changes are reviewed before they affect spend.
- **Archiving.** Archive campaigns, insertion orders, and line items when a flight ends. They are paused and filtered from view but their data stays available for reporting.

## Reference material

- `references/roles_and_permissions.md` - read when granting access or auditing users. Full role-by-capability matrix, partner versus advertiser scope, least-privilege patterns, and which roles have API access.
- `references/taxonomy_template.md` - read when defining or enforcing names. The delimiter, the ordered fields, a controlled vocabulary with example values, and a worked example name for each entity type.

## Templates and examples

Worked advertiser-scoped naming (pipe delimiter, fields: Brand | Market | Objective | FunnelStage | Channel | Flight):

```
Campaign        ACME | US | Sales | Full | AllChannels | 2026Q3
Insertion order ACME | US | Sales | Prospecting | Display | 2026Q3
Line item       ACME | US | Sales | Prospecting | Display | PMP | 2026Q3 | 728x90
Creative        ACME | US | Sales | Prospecting | Display | 728x90 | SummerSale_v2
Audience        ACME | US | 1P | CartAbandoners_30d
```

The full field list and the controlled vocabulary that backs these values are in `references/taxonomy_template.md`.

## Common pitfalls

- **Splitting one brand across advertisers.** Audiences, brand controls, and conversion data do not move freely across advertisers, so this fragments measurement permanently. One brand, one advertiser.
- **Handing out partner Admin to move fast.** It grants edit on every advertiser and user management. Scope traders to advertiser-level Standard instead.
- **Naming after launch.** Renaming once reporting has accrued breaks historical filters and saved dashboards. Enforce the convention at creation.
- **Re-entering brand-safety exclusions per line item.** It drifts and you cannot audit it. Set the floor at the advertiser and manage it as one list.
- **Forgetting the cascade.** A wrong partner-wide default targeting silently mis-targets every new build. Verify defaults before a new advertiser goes live.
- **Vague audience names.** They auto-share down to every advertiser. Apply the controlled vocabulary to audiences too.

## Sources

- [Partners in Display & Video 360](https://support.google.com/displayvideo/answer/7622449) (as of June 2026)
- [Advertisers in Display & Video 360](https://support.google.com/displayvideo/answer/2696883) (as of June 2026)
- [Manage users in Display & Video 360](https://support.google.com/displayvideo/answer/2723011) (as of June 2026)
- [View and edit brand controls for your advertiser](https://support.google.com/displayvideo/answer/9179543) (as of June 2026)
- [Brand suitability](https://support.google.com/displayvideo/answer/3032915) (as of June 2026)
- [About Floodlight and Floodlight activities](https://support.google.com/displayvideo/answer/3027419) (as of June 2026)
- [Connect a Campaign Manager 360 advertiser to Display & Video 360](https://support.google.com/displayvideo/answer/3155819) (as of June 2026)
- [Link Display & Video 360 accounts to share audience lists](https://support.google.com/displayvideo/answer/9134175) (as of June 2026)
- [Create or edit entities with Structured Data Files](https://support.google.com/displayvideo/answer/6301070) (as of June 2026)
- [About the creative review process](https://support.google.com/displayvideo/answer/6063030) (as of June 2026)
- [Archive campaigns, insertion orders, and line items](https://support.google.com/displayvideo/answer/6342906) (as of June 2026)
