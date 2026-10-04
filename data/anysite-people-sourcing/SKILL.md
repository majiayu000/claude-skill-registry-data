---
name: anysite-people-sourcing
description: Source people in bulk from Anysite's LinkedIn profile database (search_sql_users) with ~60 filters - derived seniority/function, company domain/id incl. past employers (alumni), career-shape (new in role, tenure, promotions), education, skills, deterministic territory buckets. Use when the user wants to find people in bulk - persona lists, buyers/candidates by role and company traits, competitor alumni, "new VP hires", recruiting searches - "найди людей", "собери список персон", "кто недавно сменил работу". For company lists first use anysite-company-sourcing; for one known person use linkedin/user; for CRM push use anysite-crm-prospect.
---

# People Sourcing

`linkedin/search/sql/users` (endpoint `search_sql_users`) searches a very large
profile database with filters no live LinkedIn search has: derived seniority and
function, career-shape maths (tenure, promotions, months in role), past-employer
alumni, company domains and deterministic bucketing. It is the bulk people
workhorse; live `search_users` stays the tool for one-off lookups and namesake
disambiguation.

Verified live: filters compose correctly (seniority_min=head + function=sales +
US + 51–500 headcount + new-in-role returned exactly that, role histories fresh
to the current quarter; alumni via `past_company_id` returns people whose role at
that company has an end date, never current staff).

## Two semantics that change how you work

1. **An over-`count` result is an unbiased SAMPLE, and repeating the request
   returns the SAME people** (verified: two identical calls → identical 5
   aliases; and raising `count` only appends — the list is prefix-stable, not
   reshuffled). Calling again is not pagination.
2. **Buckets are disjoint and stable** (verified: `bucket_total:2`, index 0 vs 1
   → zero overlap across 40). Walk them for volume: `bucket_total:N,
   bucket_index:0..N-1`, also the built-in territory splitter. **Ceiling:**
   `bucket_total` max is 100, so the reachable population is ~100×1000 = 100k;
   size `bucket_total` so each bucket is < 1000, otherwise a bucket is itself a
   sample and you silently lose the tail.

## What filters but does NOT come back (read before you "validate")

The derived fields you filter on are **not in the response**: no `seniority`,
`function`, `profile_score`, `months_in_role`, `promotion_count`, `industry`,
`employee_count` (verified on a live record). Consequences:

- "Validate against intent" = read `experience[]` by hand: take roles with
  `end_date == null` (the current ones) and check `.position` / `.company.name`.
  You cannot re-sort or re-segment the result by seniority/function via
  `query_cache` — those columns aren't there.
- The only size field carried per role is `experience[].company.employee_range`,
  and that string is unreliable (see Company filters). There is no trustworthy
  company-size value in a people result to write to a CRM.

## Filter map (grouped; full contract via `discover(linkedin, search)`)

- **Batch identity:** `alias[]`, `urn[]`, `member_id[]`; `last_name[]`
  (diacritics/case/spacing-folded) + `first_initial[]` for "J. Smith".
- **Text DSL** (whitespace=AND, `|`=OR no spaces around it, `"phrase"`, `-not`):
  `name`, `headline`, `summary`, `current_title`, `any_title` (past roles
  included), `skills`, `languages`, `location`, `keywords`, `edu_*`.
  **IRON RULE — quote every multi-word alternative in an OR chain.** Whitespace
  binds tighter than `|`, so an unquoted phrase SHATTERS the chain into
  impossible AND groups: `current_company_name: "Tencent|Tencent Games|Level
  Infinite|Proxima Beta"` parses as `(Tencent|Tencent) AND (Games|Level) AND
  (Infinite|Proxima) AND Beta` → **0 results on Tencent-scale companies**
  (verified live — this exact failure burned a real user session). Correct:
  `"Tencent"|"Tencent Games"|"Level Infinite"|"Proxima Beta"|Krafton`.
  Lint before EVERY send: any token containing a space inside an OR chain
  without quotes → do not send, fix first.
- **Derived seniority/function — start here for recall.** `seniority` /
  `seniority_min` (entry→ic→senior_ic→manager→head→vp→founder→cxo), `function` /
  `any_function` (sales, marketing, engineering, product, data, finance, hr, ops,
  legal, support, exec, …). Catch titles a text search can't (CRO, CCO, "VP
  Business Development" all matched a `function:sales`+`seniority_min:vp` query —
  none would survive a `"vp of sales"` DSL). Two traps, both measured:
  - **`seniority_min:"head"` includes `founder`** → pulls solo owners of 2-person
    shops. For enterprise buyers list the levels explicitly:
    `seniority:["head","vp","cxo"]`, and always add `employee_count_min`.
  - Token false-positives: "CEO Office" (staff, not the CEO) scored ≥head;
    "…President's Club 2020…" (an award on a rank-and-file AE) scored ≥vp.
    Precision on a vp+sales slice was 9/10 — good, not perfect; verify the
    shortlist against `experience[]`.
- **Company — a ladder, pick the rung deliberately:**
  1. `current_company_name` DSL with QUOTED brand variants — the default. A bare
     token like `Tencent` also matches subsidiaries ("Tencent Korea", "Fintech at
     Tencent") — a feature for brand families, a bug if you need one legal entity.
  2. `current_company_id[]` (numeric LinkedIn page ids, resolve via company
     search first) — when strictness matters: separating Level Infinite from the
     rest of Tencent, excluding brand-name lookalikes.
  3. `current_company_domain[]` (bare domains) — when domains are what you have
     (e.g. a CRM list).
  4. `keywords` — LAST resort, only WITH ≥1 selective filter (company/title/
     seniority/country) and never as the employer filter itself: it's full-text
     across all fields, and an unselective keywords query is a DB scan
     (measured: 140s → HTTP 500).
  Also: `any_company_id/domain` (ever worked);
  **`past_company_id[]` (worked and LEFT — alumni)**; `employee_count_min/max` of
  the current company. **Do NOT use `employee_range[]`** — the band string
  contradicts the true headcount often (measured ~35%: a 104-person company
  banded "11-50", a 58-person one "501-1000"); filter size only with the numeric
  `employee_count_min/max`.
- **Industry:** `industry[]` / `any_industry[]` take **exact LinkedIn-taxonomy
  labels** (e.g. "Software Development" works), NOT market words — `["fintech"]`
  returns 0 (measured). Resolve labels via `search_industries`; for "fintech",
  "SaaS" and the like, filter on the company side (`anysite-company-sourcing`
  specialities) or on `headline`/`skills` DSL instead.
- **Geo:** `country[]` ISO2 (reliable); `location` DSL for cities/metros.
  **"Responsible for a market" ≠ "located in it."** When the user wants people
  FOCUSED on a region (CIS/MENA/emerging markets), do NOT filter `country` by
  that region — BD/publishing teams of global companies sit in HQ (KR/CN/US/NL/
  SG). Search the market mention in the profile instead:
  `headline`/`summary`: `CIS|Russia|Kazakhstan|MENA|"emerging markets"|"Middle
  East"`. Measured on a live case: `country:[RU,KZ,UZ,AE,SA,…]` → 2 profiles;
  the headline variant → 84. Use `country` only when the person must physically
  BE in the region — and warn the user the pool will be narrow.
- **Education:** `edu_slug[]`, `edu_institution`, `edu_field`,
  `edu_ended_year_min/max` (graduation cohort ≈ age proxy).
- **Career shape:** `months_in_role_max` (new in role), `months_in_role_min`,
  `months_since_change_max` (started OR ended a role recently — job-change
  radar), `experience_years_min`, `n_roles_*`, `n_companies_*` (stability vs
  hopping), `promotion_count_min` (promoted without changing employer),
  `avg_tenure_months_*`.
- **Quality & coverage:** `profile_score_min` (0–8) — do NOT set it by default:
  it silently drops sparse-but-on-target profiles (a real user's default of 5
  cut exactly the people they were hunting). Add it only when the user asks for
  "complete/outreach-grade profiles" (then 5+), or as a tie-breaker on an
  over-1000 pool. Plus the `has_*` family (`has_current_role`, `has_role_dates`,
  `has_education`, `has_company_size`, `has_engagement`…).
- **Badges/engagement:** `open_to_work`, `hiring`, `verified`, `is_premium`,
  `is_top_voice`, `follower_count_min`, `connection_count_min`. (`is_creator` /
  `is_influencer` filter but are NOT returned — you can't confirm them.)
- **Lookalike (EXPERIMENTAL — verify every time):** `similar_to` / `also_viewed`
  by alias. Measured unreliable: two seeds returned namesakes (same name,
  different people) or nothing — NOT semantic lookalikes. Do not use it as a
  "people like our champion" shortcut; if you try it, probe `count:5` and confirm
  the surnames differ from the seed's before trusting a single row. For real
  lookalikes, replicate the champion's attributes as explicit filters instead.
- **Freshness:** `fetched_after` (unix ts) — only recently refreshed profiles.

## Coverage honesty

Not every profile states a current employer, industry, company size or dated
roles — those filters answer **only for people who do**. The API's own numbers:
current title, seniority and function resolve for about a third of people;
`current_company_id`, `current_company_domain` and `employee_range` for about one
person in five. So a company-id or domain rung returns roughly a fifth of the
people who really work there — say so, and for coverage run the
`current_company_name` rung alongside it. Set the matching `has_*` flag
deliberately and tell the user the trade-off ("filtering by company size skips
people whose company doesn't state one"). `open_to_work: false` = "no badge
observed", not "not looking". Follower/connection counts exist on a small share —
gate with `has_engagement`.

Two data-shape facts to expect: some profiles carry **multiple concurrent open
roles** (measured: 4/10 in one slice; one person had ~19 — advisory boards,
visiting posts). "Current company" is then ambiguous, and a
`current_company_domain`/`employee_count` filter may match on a quarter-time
advisory role, not the day job — so verify the target company is an *operational*
current role before anchoring an opener on it. And `urn` is occasionally `null`
even when `alias` is present — the vanity URL still enables `user_find_email_by_url`
and `user_posts` (it accepts the alias/URL and resolves it at the cost of one extra
lookup).

## The loop

1. **Start from the most selective structural filters** (seniority/function/
   company/country) — never bare `keywords` (it only helps for distinctive words
   and must ride a selective filter). No persona in the request → use the titles,
   seniority and function from the Personas section of `anysite-gtm-profile` when
   it exists.
2. **Probe `count:10`, validate against INTENT via `experience[]`** (structural
   filters aren't semantic: "Director of Sales, 51–200, US" returned a coffee
   wholesaler). Precision comes from `current_company_domain[]` (a list from
   `anysite-company-sourcing`), taxonomy `industry[]`, or headline/skills DSL.
3. **Tighten/widen, re-probe, fetch;** >1000 → size `bucket_total` so each bucket
   < 1000 and walk it.
4. **Free re-cuts** with `query_cache` (only on returned fields); export with
   `export_data`. In clients that render MCP Apps, show the result with
   `show_entity_table(cache_key, group_by="company_id")` so people are grouped by
   account; people at approved accounts from `review_leads` start from that
   selection's company ids.

**Zero results — debug in this order, don't flail:**
1. Re-read your own DSL for unquoted multi-word phrases in OR chains (the #1
   cause by far — see the IRON RULE).
2. Loosen ONE filter per step (drop `profile_score_min`, widen `seniority`,
   drop `industry`) — never jump straight to a bare `keywords` full-text.
3. Sanity check: 0 results for a Tencent-scale employer is almost certainly a
   query bug, not missing data — go back to step 1, don't report "not found".

**500/408 on a broad query:** don't retry as-is — narrow it (add a selective
filter) or raise `timeout` (≤1500). An unselective query is a scan; retrying a
scan just times out again.

## Recipes

- *"VPs of Sales at US SaaS 50–500"*: `seniority:["vp","cxo"], function:["sales"],
  country:["US"], employee_count_min:50, employee_count_max:500,
  industry:["Software Development"]`. (SaaS ≠ a taxonomy label — narrow via the
  company-side list or headline DSL. `profile_score_min` only if asked.)
- *"BD/partnerships across a brand family"* (verified live, 99 profiles):
  `current_company_name: "\"Tencent\"|\"Tencent Games\"|\"Level Infinite\"|
  \"Proxima Beta\"|Krafton", current_title: "\"business development\"|bizdev|
  partnership|partnerships|licensing|monetization|payments|commercial",
  seniority:["manager","head","vp","cxo"], has_current_role:true` — every
  multi-word alternative quoted; regional focus goes in `headline`, not
  `country` (see Geo).
- *"New decision-makers"* (best-converting timing): add `months_in_role_max:3`
  (default 90 days). Too few → widen the title family first, then relax size or
  geography, and only then the window (6 months; 9 is the ceiling).
- *"Buying committee at one account"*: `anysite-buying-committee`.
- *"Warm paths"*: people who used to work at your customers —
  `past_company_id:[<customer ids>]` + your persona filters; name the shared
  employer in the message only if the user confirms it may be mentioned.
- *"Grew up inside the company"* (internal champion / stable ABM contact):
  `promotion_count_min:2` + `avg_tenure_months_min:24`.
- *"Competitor alumni"*: `past_company_id:[<ids>]` (+ function/seniority) — people
  who LEFT. Note: this is ex-employees, NOT the competitor's customers; for
  customers use `anysite-crm-competitor-intel` (wappalyzer + reviews).
- *EMEA localized sequences*: `languages:"german", country:["DE","AT","CH"]`.
- *School alumni warm-intro*: `edu_slug:[...]` + `edu_ended_year_min/max`.
- *Recruiting*: `skills`/`edu_field` DSL + `avg_tenure_months_min` (stability) +
  `n_companies_max` (not a hopper) + `open_to_work:true` as a bonus tier only.
- *Territory split*: same query, `bucket_total:<reps>, bucket_index:<rep #>`.

## Handoffs and hygiene

- Company lists IN (`current_company_id`/`domain`) come from
  **`anysite-company-sourcing`**; people OUT go to **`anysite-crm-prospect`**
  (dedup + CRM push).
- For "up to N contacts across a few companies", 2–3 focused queries (base +
  regional + function-specific) deduped by `alias` beat one mega-query — each
  stays selective and each angle surfaces people the others rank low.
- **Emails have a real cost and yield — don't hand-wave it.** The result's
  `alias` is the vanity URL, ready for the email cascade (`anysite-mcp` →
  Email finding): `user_email` first (cheap, ~half personal addresses, low
  yield), then `user_find_email_by_url` (~75% yield but 50cr each — estimate
  `50cr × N` and confirm before a big run) with its `valid_email`/`email_status`
  as the deliverability gate. Personal/unverified addresses never go into a work
  sequence. For bounce-critical sends, run the address through `emails/verify`
  (`status` valid / invalid / risky, `is_personal`); it may answer from a verdict
  stored up to a year ago (`resolved_by` says which).
- **Live-verify the outreach shortlist** via `linkedin/user` with a small
  `cache_max_age_days` (e.g. 7) — without it the call may return a profile up to
  180 days old, which defeats the check; it also yields the vanity URL. Job-change detection on CRM
  contacts belongs to `anysite-crm-champions` (this DB's `months_since_change_max`
  is its cheap pre-filter, not its evidence).
- Sourcing individuals is personal-data processing: search to the stated business
  need, don't hoard.
