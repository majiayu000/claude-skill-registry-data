---
name: anysite-crm-lookalikes
description: Derive the actual ICP from the CRM's closed-won/best customers and find lookalike companies with anysite bulk search (LinkedIn company DB, Crunchbase filters), scored and deduplicated against the CRM. Use when the user asks to find companies like their best customers, expand the target list, derive their real ICP from data, or seed a prospecting campaign. Requires an active CRM connection with some won/customer records.
---

# CRM Lookalikes

Your real ICP is written in your closed-won list, not in your pitch deck. Extract the
pattern, then search 70M+ companies for more of it.

For PEOPLE lookalikes see `anysite-people-sourcing` → Lookalike: `similar_to` /
`also_viewed` are experimental — stated by a minority of profiles, so they miss most
matches and must be verified every time. Filters derived from the seeds' titles, seniority
and companies are the reliable path.

## Flow

### 1. Collect the seed set

```
crm_query_records(object_type="companies", list_id=<customers list> | search=...,
                  properties=[record_id, name, domain, industry, <size/stage if mapped>])
```
Need the user's help to identify "best": a customers list, a lifecycle/status field, or an
explicit pick of 10–30 names. The "Best customers" line of `anysite-gtm-profile` is a ready
pick when it exists. Fewer than ~8 seeds → warn that the pattern will be weak.

### 2. Profile the seeds

Resolve each seed to structured firmographics with the exact resolve (`anysite-mcp` →
Domain → company) — a wrong seed poisons the whole ICP pattern downstream:
```
execute companies/resolve {website: "seed1.com", count: 3}          # per seed; pick the
                                                                    # right candidate
execute linkedin/search/search_sql_companies {urn: ["fsd_company:<id>", ...], count: N}
```
A seed with no candidate is NOT dropped yet — resolve it via the site itself
(`webparser/parse {url, extract_minimal: true}` → own linkedin.com/company URL in `links[]`
→ `linkedin/company`), or via crunchbase → `contacts.linkedin_url`. Only a seed that
survives neither is excluded from profiling, and say which ones.

**Contrast, not only resemblance.** If the CRM also has weak customers (churned, smallest,
lowest usage) or closed-lost accounts, profile them too and keep only the dimensions where
the best and the worst DIFFER — a trait every customer shares says nothing. State the
counter-pattern ("under 10 employees churns"). At most 5 criteria. Fewer than ~10 seeds →
say the pattern is a hypothesis.
Plus `crunchbase/company` for stage/funding on a subset (venture-relevant seeds only).
Derive the pattern in-session and SHOW it:

```
Industries: X (60%), Y (25%) · Size: 11-200 dominant · Geo: US+UK 80%
Stage: seed-B · Common traits: has API docs page, hiring in data roles, ...
```

Build the size band from `employee_count`, never from `employee_count_range` — the two can
contradict each other in one record (verified: `employee_count: 1465` with
`employee_count_range: "201-500"`), and a wrong band here propagates into every search
below. Bucket the exact counts yourself.

The user confirms/edits the pattern — it's their ICP, the data only proposes it.

### 3. Search for lookalikes

**Wide net, then judge each row.** LinkedIn industry labels are often wrong or empty
(auto-created pages especially), so a search on the seeds' dominant industry silently
misses real lookalikes:
- Search with EVERY industry that at least one seed carries, plus a keywords/description
  query with no industry filter at all (catches the blank- and mislabelled ones).
- Decide membership with ONE yes/no question per row, the edge cases settled inside the
  question ("Does this company sell B2B software to finance teams? Payment processors: no.
  Consultancies: no."), answered from the row's description — not with a weighted score.
- **Canary first:** run the question on 50–100 rows, show the user the yes/no split with a
  few examples of each, fix the question, then run the rest.

- `execute linkedin/search/search_sql_companies` — industry_name/keywords DSL from the
  pattern, employee_count band, country filter, count up to 1000.
- `execute crunchbase/db/db_search` — when stage matters (`last_funding_type`,
  `last_funding_date_after`); `crunchbase/search` live for `hiring: true` or
  `shares_investors_with: [<seed investors>]` (a strong hidden-similarity filter).
- Niche supplements per pattern: `yc/search/search_companies` (early-stage), `builtin`
  (US tech hubs), `producthunt` (product-led).

Search wide, profile narrow: the searches themselves are cheap even at count 1000, but do
NOT enrich every candidate — score on the fields the search already returned, and fetch
extra evidence (crunchbase lookups etc.) only for the top ~50. State the credit estimate
before any per-candidate enrichment.

### 4. Score and dedup

Rank the rows that passed the yes/no question against the confirmed pattern (same rubric
discipline as `anysite-crm-score` — evidence per company, no guessed values, a missing
value is "unknown", not a low score). Every row carries its reason in one line.
Dedup against the CRM by domain (`crm_query_records`) — existing accounts drop out or get
flagged "already in CRM, unworked".

### 5. Hand off

Output: top-N table (name, domain, why-it-matches, score) + the confirmed ICP pattern for
reuse. In clients that render MCP Apps, open the candidates with `show_entity_table` and
offer `review_leads` for a Yes/No pass — the approved selection is what goes to the CRM. Pushing to CRM → `anysite-crm-prospect` (its dedup/create/working-list rules apply);
finding people at these companies → same skill. This skill itself writes nothing.
