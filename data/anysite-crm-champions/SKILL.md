---
name: anysite-crm-champions
description: Detect job changes among CRM contacts (champion tracking) - find contacts who moved to a new company, flag past champions at new accounts, update the CRM and propose re-engagement plays. Widely considered the highest-converting B2B signal. Use specifically for job-change detection - "who changed jobs", "track champions", "are my contacts still there". For general field updates on contacts use anysite-crm-enrich instead. Requires an active CRM connection and contacts with linkedin_url or email.
---

# CRM Champion Tracking

People move; CRMs rot (typically ~25%/year of contacts change jobs). A past champion at a
new company is warm pipeline. This skill finds the movers and turns them into plays.

## Prerequisites

Active CRM connection. Profile mapping for any writes — the Writing rules in
`anysite-crm-setup` apply, including its create policy: creating records here follows the
profile's `allow_create`, same as in `anysite-crm-prospect`. Contacts need `linkedin_url`
or `email` — run `anysite-crm-enrich` first if coverage is poor.

## Flow

### 1. Pick who to track

Priority order (ask the user which tier, default to the first available):
1. **Key champions** — closed-won contacts, power users, admins (if such a list/field exists),
2. **Open/closed-lost opportunity contacts**,
3. The working list / everyone with a linkedin_url.

Only tier 1 people are **champions** — someone who got real value from the product. A
contact on a lost or open deal who moves is "warm familiarity", a weaker play; label it so.

```
crm_query_records(object_type="contacts", list_id=... | search=...,
                  properties=[record_id, email, linkedin_url, <company field>, jobtitle])
```

Cap a run at ~100 contacts (one profile call each); more → propose batching by tier.

### 1b. Cheap pre-filter on big lists (optional)

For hundreds of contacts, don't live-check everyone: `search_sql_users` with
`urn: [<contact urns>]` (batch) or `past_company_id: [<your CRM company ids>]` +
`months_since_change_max: 6` surfaces LIKELY movers from the 856M DB at DB cost.
It's a pre-filter, not evidence: the DB is fresh but not realtime, so every
flagged mover still goes through the live check below before any CRM write or play.

### 2. Detect moves

Per contact:
- `linkedin_url` → `execute linkedin/user/user {user: <url>, cache_max_age_days: 7}` →
  current experience. Without the small cache window the profile can be up to 180 days
  old — exactly the months in which the move happened.
- email only → `people/by-email {email}` (a stored answer can be a year old — it tells you
  who the person is, not where they are now); then confirm via the CRM's own knowledge:
  email domain → `companies/resolve` → `company:<id>` → `search_users {first_name,
  last_name, current_company: [{"type": "company", "value": "<id>"}]}`. For champion
  tracking a search by the CRM company tells you where they WERE — a zero-result search
  there is itself a move hint; re-search without the company filter, then apply the
  identity guard below before concluding.

Compare the profile's **current company** against the CRM company. Normalize before
comparing (legal suffixes, casing, known rebrands); when unsure, treat as "same" — false
move-alarms erode trust. Also catch **promotions** (same company, new title) — a secondary
but useful signal.

**Identity and move guards** (a false "moved" burns the relationship):
- **Same person, proven.** A name + new company match is never enough: MOVED requires the
  new profile's own `experience[]` to contain the CRM company. No such entry → "possible
  namesake", not a move.
- **Not a move:** advisor, board, investor, fractional or part-time roles; a second job
  while the old one is still current (flag "dual role", keep the old record).
- **Into another existing customer** → internal reshuffle for account management, not a
  new-logo play. **Into a competitor** → log it, no play.
- **Aggregate:** several movers into one company = ONE account signal listing all of them.
  Two or more departures from one account → flag churn risk on the OLD account.
- **Idempotent reruns:** record processed moves (a "move processed" date in the profile
  mapping, or the run report) so a monthly run never re-announces the same move.

**Movers IN, not only out:** new decision-makers at your target accounts are the same play
from the other side — `search_sql_users {current_company_id: [<target ids>],
months_in_role_max: 3, seniority_min: "head"}`, then the live check above (small
`cache_max_age_days`). Widen the title family before widening the window (3 → 6 months,
never past 9). That search result opens as a table in clients that render MCP Apps —
`show_entity_table(cache_key, group_by="company_id")` groups the new people by account.

### 3. Classify and propose plays

- **Moved to an in-ICP company** → hottest: "past champion at new account" play. Propose:
  update old record, create the new-company record and a fresh contact entry.
- **Moved out of ICP** → update CRM only.
- **Promoted** → update title; suggest congratulation touch if they're an active deal contact.
- **Profile gone/private** → report, no change.

### 4. Write back (with explicit user confirmation)

Job-change writes touch the fields most likely to collide with CRM automations, so always
dry-run and show the diff, even for small batches:

- Update the old contact: new title/company per profile mapping (these need `overwrite` in
  the profile — job data is volatile by design).
- New account: `crm_upsert_companies` (match by domain, `allow_create` per profile).
- New email at the new company: `user_email` first (cheap), then
  `user_find_email_by_url {url: <vanity profile URL>}` (50cr, high yield; check
  `valid_email`/`email_status` before trusting). Note that creating a NEW contact record
  requires an email; without one, update the existing record.
- Association: pass `associate_company_domain` (or `associate_company_id` from the company
  upsert result) so the contact links to the new company; the server keeps the old
  association unless `overwrite_associations=true` — set it only if the user confirms the
  contact should be re-linked.

Save `run_id`s; mention `crm_undo`.

### 5. Report

Table: contact → old → new → start date → play. Lead with movers into ICP accounts. Timing:
a new starter is busy in week one — the best window is roughly 2 to 6 weeks after the start
date; past ~3 months the "new role" angle is stale. Include suggested opener anchored on
the shared history ("you used X at <old company>...") — personalization from facts, never
invented familiarity. Hand the mover + the shared-history fact to
`anysite-outreach` to draft the actual re-engagement message.
