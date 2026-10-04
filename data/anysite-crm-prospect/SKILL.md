---
name: anysite-crm-prospect
description: Find net-new leads with anysite (LinkedIn and Crunchbase search, email finding) and push them into the CRM deduplicated - companies first, then contacts with associations. Creating records is gated by the profile's allow_create. Use when the user asks to find new leads/prospects/accounts AND add them to the CRM, build a list in HubSpot, or import prospects. For research without CRM push, use anysite-company-sourcing / anysite-people-sourcing. Requires an active CRM connection and profile.
---

# CRM Prospect

Search → resolve → dedup → create. Order matters: companies before contacts, dedup before
create, dry-run before both.

## Prerequisites

Active CRM connection + profile (`allow_create: true` agreed in profile — if not, stop and
ask). Read Writing rules in `anysite-crm-setup`.

## Flow

### 1. Define the search

Get concrete criteria from the user (persona titles, industry, geography, size, stage).
If the saved GTM profile (`anysite-gtm-profile`, made by `anysite-gtm-onboarding`) exists,
its ICP and Personas sections are the default criteria — confirm them in one line and ask
only for what the request overrides or the profile lacks.
Estimate volume and confirm before running anything large.

**Companies:**
- `execute linkedin/search/search_sql_companies` — main path: `keywords`/`industry_name`
  DSL, `employee_count_min/max`, `country_hq`, up to 1000/call, 1cr-class.
- `execute crunchbase/db/db_search` — when stage/funding filters matter
  (`last_funding_type`, `last_funding_date_after`, `investors`).
- `execute crunchbase/search` — live, adds `hiring: true`, `it_spend_*`, `valuation_*`
  filters (20cr/50 — use for precision, not volume).
- **Let the user pick before you spend on people and emails.** Show the company result
  with `show_entity_table`, or run `review_leads` for a Yes/No pass; only the approved
  selection (a cache_key in the `[anysite-table]` message) goes on to people, emails and the
  CRM push. Funding for the list: batch the Crunchbase database and `merge_data(join_on=
  ["domain","linkedin_url","company_id"], unmatched="drop")` (`anysite-mcp` → Tables, joins
  and lead review).

**People at those companies:**
- Bulk (default): `execute linkedin/search/search_sql_users` — filter by
  `current_company_id`/`current_company_domain` (straight from the company results),
  `seniority_min`/`function` (derived — better recall than title text), country.
  Craft + coverage caveats: `anysite-people-sourcing` skill. >1000 matches → walk
  `bucket_total`/`bucket_index`, not repeated calls.
- Point lookups / disambiguation: `execute linkedin/search/search_users {job_title,
  current_company: [urn] | company_keywords, location, count}` — never bare `keywords`.
- Live-verify the outreach shortlist via `linkedin/user` with a small
  `cache_max_age_days` (e.g. 7) before pushing — the DB is fresh but not realtime, and
  without that parameter the "live" call may return a profile up to 180 days old.

### 2. Emails (cheap-first cascade)

1. `execute linkedin/user/user_email` — batches of ≤10 profiles. Warn the user upfront:
   yield is low, a large share of leads will come back email-less.
2. Remainder → `user_find_email_by_url {url: <vanity profile URL>}` — high yield, 50cr
   each: estimate the cost (50cr × remainder) and confirm before running on large lists.
   Vanity URLs only (`/in/name/`, not `/in/ACoA...`). Its `valid_email`/`email_status`
   fields are the deliverability gate: only validated work addresses go into the push;
   the rest stay "found, unverified". (`emails/find {linkedin_url}` is an alternative
   finder with `email_status` and `is_personal`.)
2b. Step-1 addresses → `emails/verify {email}`: only `status: valid` with `is_personal:
   false` counts as a verified work email; `risky` stays unverified, `invalid` is dropped.
3. Still nothing → **keep the lead in the report**, but know the server requires an email
   to CREATE a contact — email-less leads can only update existing records (matched by
   `linkedin_url`). Report them as "found, pending email"; never silently drop them.

### 3. Dedup against the CRM (before any create)

```
crm_query_records(object_type="companies", search=<domain>)     # or batch by domains
crm_query_records(object_type="contacts", emails=[...])
```
Dedup is reliable by email and domain. By `linkedin_url` it is best-effort only (free-text
`search`) — for a lead with no email whose search comes up empty, do NOT create; put it in
a manual-review bucket and say why. Existing company → reuse its record; existing contact →
update, not create. Report how many were already known — it calibrates the user's trust.

**Launch gates before any create** — decide link / create / review / reject per record:
- **Identity:** a consumer-email domain is never account identity; resolve the company by
  its own domain. Re-run the dedup lookup right before the create, not only at the start.
- **Context:** already a customer, an open deal, a contact touched recently (if the CRM
  exposes it) or a competitor → not a cold prospect; flag it instead of creating.
- **List quality** (show it before the push): verified work emails, duplicate emails,
  people per company (> 3 at one domain → trim), titles that match the personas, company
  fit, name quality (see `anysite-outreach` → Clean names). Grade it A–F, weighting
  verification and fit double; below C → fix the list first, don't push.

### 4. Push — companies first, then contacts

```
crm_upsert_companies(records=[{domain, properties per profile}],
                     allow_create=true, dry_run=true)            → confirm → write
crm_upsert_contacts(records=[{email | linkedin_url,
                              properties per profile,
                              associate_company_domain: <domain>}],
                    allow_create=true, dry_run=true)             → confirm → write
```
Before pushing, split found emails by domain: `user_email` returns a mix of personal and
work addresses (and sometimes an address at a PAST employer), so match each email's domain
to the contact's current company. Personal addresses (gmail/yahoo/outlook and similar) are
NOT work emails — never feed them into a work-email sequence; keep those leads in a
"personal email only" bucket alongside
"pending email", and say so in the report. Server requires email to create a contact;
contacts without email that don't match an existing record will be skipped with a
warning — report them as "found, pending email", don't retry blindly. When associating to companies created in the same run, prefer
`associate_company_id` from the company upsert result. Save `run_id`s.

Note: crm_* tools cannot add records to CRM lists (list_id is read-only in queries). If
the user wants the new leads in a HubSpot list, suggest an active-list filter on a mapped
property (e.g. `lead_source = "anysite"`) — set that property during the upsert instead.

### 5. Report

Created / updated / already-known / pending-email / manual-review. Never call data
"verified" unless a verification step actually ran.

## Boundaries

- Creating records (`allow_create=true`) is permitted here and in `anysite-crm-champions`,
  in both cases only when the profile's `allow_create` agrees. If the user wants research
  without CRM push, stop after step 1 and hand over the table (`anysite-company-sourcing`,
  `anysite-people-sourcing`).
- Don't set owner, lifecycle stage, or any protected field — routing belongs to the CRM's
  own automation.
- ICP scoring of the found leads → `anysite-crm-score`; lookalike seeding →
  `anysite-crm-lookalikes`; writing the first-touch message → `anysite-outreach`
  (it opens on a detail you collected here, not a generic template).
