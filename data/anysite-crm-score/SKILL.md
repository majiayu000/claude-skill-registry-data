---
name: anysite-crm-score
description: Score CRM companies or contacts against the user's ICP using anysite data (firmographics, funding stage, hiring, tech signals) and write the score into the single mapped score field. Use when the user asks to score leads, rank accounts, prioritize the pipeline, or apply ICP criteria to CRM records. Requires an active CRM connection and a profile with a score field marked overwrite.
---

# CRM Score

Deterministic-ish prioritization: explicit rubric, evidence per company, score written to
exactly one mapped field.

## Prerequisites

Active CRM connection. Profile must map a score target field with `mode: overwrite`
(scores are re-computed by design). Not mapped → offer to store nothing and just report,
or send the user to re-run `/anysite-crm-setup`. The Writing rules in `anysite-crm-setup`
apply to every write. Cap a scoring run at ~50 companies and state the credit estimate
(evidence calls × price) before fetching; more → propose tiers or a narrower list.

## Flow

### 1. Fix the rubric BEFORE fetching data

Get ICP criteria from the user, or derive them with `anysite-crm-lookalikes` logic from
closed-won records. The saved GTM profile (`anysite-gtm-profile`), when present, is the
starting draft of the rubric — its ICP section gives the criteria, its disqualifiers the
zero-score rules. Turn them into a written rubric with weights, e.g.:

```
industry match (0-3), size band (0-2), geo (0-1), funding stage (0-2),
hiring in buyer function (0-1), tech/context signal (0-1)  → 0-10
```

Split hard from soft criteria. Hard = a disqualifier ("if a company matches everything
except this, do we still reach out?" — no): excluded industry, unserviceable region,
competitor, existing customer. A hard miss makes the score 0 with the reason, whatever the
rest adds up to. Buying signals are never hard criteria — they belong to
`anysite-crm-signals`.

Show the rubric, get a nod. The rubric goes into the report verbatim — scores must be
explainable and reproducible.

### 2. Fetch evidence (cheap-first)

```
crm_query_records(object_type="companies", ...) → record_id, name, domain, existing fields
```
- Base firmographics: `companies/resolve {website, count: 3}` per domain (exact domain;
  pick the right candidate — `anysite-mcp` → Domain → company), then one batch
  `search_sql_companies {urn: ["fsd_company:<id>", ...]}` for industry, size, locations and
  `crunchbase_alias`. Unresolved domain = no evidence, criteria "unknown"; a domain with no
  candidate is resolved via `webparser/parse` on the site itself, per the same recipe.
- Stage/funding (only if the rubric needs it): take `crunchbase_alias` from the row above —
  free, no lookup. Only when it is empty and the
  company is plausibly venture-backed, fall back to the live `crunchbase/search` (20cr, fuzzy
  — verify name+domain) → `crunchbase/company`. Skip entirely for obviously non-venture
  companies. Note `leadership_hires[]` is unusable as an ICP criterion for SMB/startup targets
  — measured empty on 6 of 6 live accounts, including a 281-person one.
- Hiring probe (only if in rubric): the numeric id from the resolve (`company:<id>` /
  `company_id`) → `search_jobs {company: [{"type": "company", "value": "<id>"}],
  count: 20}`. No resolve → `search_companies {keywords: name, count: 5}` +
  verify by name/industry (its `urn` is already the `{type, value}` object).
- Team-shape evidence (great for "engineering-led vs sales-led" criteria):
  `linkedin/company/company_employee_stats` (1cr, needs company URN) — absolute headcounts
  by function (verified: Engineering 26 / Sales 14 on a 79-person company). Don't sum its
  `locations` array (nested buckets: US ⊃ state ⊃ metro); cross-check totals against
  `employee_count`.

Company size in the rubric: use `employee_count`, never `employee_count_range` — the two
can contradict each other in one record (verified: 1465 vs "201-500"), and the range would
misfile the size band silently. Range only as fallback when the count is empty, noted.

Skip any evidence source whose rubric weight is zero. State per-company data gaps —
a company with missing data gets a confidence note, not a silently low score.

### 3. Score

Apply the rubric in-session. For every company keep one line of evidence per criterion.
No evidence → that criterion is "unknown", never a guessed value — and it is left OUT of
the scale rather than counted as 0: score = points earned ÷ maximum points of the criteria
that had data × 10, with "scored on 7 of 10 points of evidence" next to it. A company with
data on less than half of the rubric gets "insufficient data" instead of a score. This keeps
a thinly covered company from looking like a poor fit.

### 4. Write and report

```
crm_upsert_companies(records=[{domain: "<domain>", properties:{<score field>: <value>}}],
                     allow_create=false, overwrite_properties=[<score field>],
                     dry_run=true)  → confirm → write → run_id
```
Company upserts match ONLY by domain — pull `domain` when querying records; companies
without one get a score in the report but no write. Write ONLY the score field (plus
`scored_at` if mapped). Report: top-N with evidence lines,
distribution summary, gaps. Contacts scoring (persona fit) works the same way against
contact records with `linkedin/user` evidence — same rubric-first discipline.

## Boundaries

- Score ≠ routing: never touch owner/stage/status based on a score.
- Re-scoring overwrites by design — that's why the profile must explicitly mark the field.
- Intent-level signals (fresh funding, exec hires) belong to `anysite-crm-signals`; this
  skill measures fit. The two compose into a 2×2: high fit + signal score ≥ 100 = work now;
  high fit, no signal = nurture / watch; low fit + strong signal = "do not pursue" (say so
  explicitly — a loud trigger does not fix a bad fit); low fit, no signal = drop.
