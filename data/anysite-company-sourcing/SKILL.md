---
name: anysite-company-sourcing
description: The craft of sourcing companies from Anysite's 70M+ LinkedIn company database (search_sql_companies) - turning a fuzzy ICP into per-field DSL filters that return real matches instead of token soup. Fixes the default failure mode where naive keyword queries return companies from the wrong country, wrong industry and stub pages. Use when the user asks to find/source companies, build a company list, complains that company search results are bad or irrelevant, or needs a target-account universe - "найди компании", "плохие результаты поиска компаний", "source accounts". For people at those companies use anysite-people-sourcing; for funding-stage filters use crunchbase; for pushing into a CRM use anysite-crm-prospect.
---

# Company Sourcing

`linkedin/search/search_sql_companies` searches 70M+ companies and is the single
best bulk company tool in the catalog — **and its naive use is the single most
common source of garbage lists.** Measured live, same intent, same day:

- `{keywords: "AI startup San Francisco"}` → **1 relevant of 5**: a Tel-Aviv
  gaming-data firm, a Sydney fintech and a Ho-Chi-Minh beauty e-commerce all
  matched — each had the token "startup" somewhere in its description and
  "San Francisco" among *secondary* office locations.
- The same intent as structured filters (below) → **5 of 5** genuine SF AI
  companies in the right size band.

The difference is the whole skill. Never ship results from a naive query.

## Why naive queries fail (mechanics, not opinion)

1. `keywords` matches whole words across ALL text fields — name, description,
   specialities, hashtags **and the locations array** — so "San Francisco" as a
   keyword still matches a Hanoi company that lists an SF sales office in
   `locations`. (Whole-word matching removed the inner-substring noise, but not
   the wrong-FIELD problem — HQ is a separate field, use it.)
2. **`sort` changes ordering, not the candidate set — a naive keyword query is
   still not an ICP list.** With relevance (the default), "AI startup San
   Francisco" surfaces *Startup Weekend AI*, *Bitcoin AI Startup Lab*, 1-employee
   shops and a Phoenix-HQ company (all measured) — they score high because the
   words sit in their NAME. The fix is per-field decomposition below, not a sort
   flag.
3. Millions of company pages are stubs. Without hygiene filters they dominate.
4. `employee_count_range` can contradict `employee_count` in the same record
   (measured: 305 employees with range "11-50"). Never filter or segment by the
   range string.

## The method: decompose intent into fields

Take the user's ICP sentence apart and map each fragment to its OWN field. No ICP in the
request → take it from the ICP section of `anysite-gtm-profile` when it exists (and say so
in one line), including its exclusions.

| Intent fragment | Field | Notes |
|---|---|---|
| "based in X" | `country_hq: ["US"]` + `headquarter_location: "\"san francisco\""` | token-aware; NEVER the `locations` field — that matches branch offices |
| "present in X" (offices count too) | `country_any` | this is the only right use of the locations array |
| "does AI / fintech / logistics" | `specialities` OR `industry_name` OR `description` together, not specialities alone | `industry` array wants URNs; `industry_name` resolves labels — see the specialities caveat below |
| "in the orbit of company X" | `similar_organizations: "\"fsd_company:<id>\""` | queryable filter, not just an output field — the reverse-graph expander; see below |
| "startup / SMB / enterprise" | `employee_count_min` / `employee_count_max` | integers; ignore `employee_count_range` entirely |
| "founded recently" | `founded_on_min` | year |
| named company lookup | `name` or `alias` DSL + exact verification | never trust first hit; a known domain → `companies/resolve` (anysite-mcp) |
| always, every query | `is_active: true, has_website: true, min_description_length: 100` | the hygiene trio kills stubs and dead pages |
| ranking | `sort` = `relevance` (default) or `last_modified` | relevance for sourcing; `last_modified` for "what's new since last run" (monitoring). Scoring weights a term by field: name 5× > specialities/hashtags 3× > short_description 2× > long description 1×, length-normalized; ties broken by recency. **Caveat:** the score is built only from `keywords`/`name`/`specialities`/`description` — a query filtered ONLY by non-text fields (e.g. just `industry` + `employee_count_min`) has nothing to score, so it falls back to recency order |

Industry labels are often wrong or empty (auto-created LinkedIn pages especially). When
missing a company matters more than extra noise, run a second query with the description
terms and NO industry filter, merge the two (`merge_data` with `dedupe_by: ["urn"]`) and
decide each row with one yes/no question — the wide-net method in `anysite-crm-lookalikes`.

DSL in every text field: whitespace = AND, `|` = OR (no spaces around it),
`"phrase"` = exact phrase / substring, `-token` = NOT. Example:
`specialities: "\"artificial intelligence\"|\"machine learning\" -agency"`.
**IRON RULE: quote every multi-word alternative in an OR chain.** Whitespace
binds tighter than `|` — `name: "Level Infinite|Proxima Beta"` parses as
`(Level) AND (Infinite|Proxima) AND (Beta)` and returns 0 (verified live on the
sibling people endpoint, same parser). Lint before sending: a space inside an
OR alternative without quotes → fix first.

**Matching semantics (changed — this is now the biggest lever):**
- **A bare word matches as a WHOLE WORD, not a substring** (verified live:
  `keywords: "sdr"` returns "SDR Academy", "SDR Foundry", "Vida SDR" — companies
  with the standalone word, and no longer "adviseur"-style inner hits). Case
  doesn't matter.
- **No stemming.** `integration` does NOT find `integrations` — write both:
  `integration|integrations`. Same for singular/plural and verb forms.
- **Quotes = substring** (the old behaviour, kept). `"integr"` matches both
  `integration` and `integrations`; `"machine learning"` matches that exact
  sequence. Use quotes deliberately when you WANT a fragment.
- Terms with separators (`b2b-saas`, `S.E.E.D.`, `x.com`) and Cyrillic are
  auto-substring — nothing to change for them.
- `alias` and `website` are untouched — still substring (`alias: "openai"` finds
  `openai-inc`); `hashtags` is exact element match.

Practical consequence: short single-word queries used to be the WORST case (inner
substring noise); they are now precise. If you actually need "a piece of a word",
reach for quotes.

**Specialities caveat:** self-declared tags are the highest-signal field WHEN
present, but hot young startups often leave them blank — measured: 2/10 in a
US/Software slice had empty `specialities[]`, one of them Hebbia ($160M-funded,
empty short_description too). So `specialities` is a widening OR alongside
`industry_name` and `description`, never the sole gate, or you silently drop
exactly the fresh-funded targets a list is built for.

## The loop (never skip step 3)

1. **Build** the per-field query from the decomposition above.
2. **Probe** with `count: 10`.
3. **Validate against the intent, not the filters**: for each of the 10 check
   HQ country/city, what the company actually does (short_description), and
   `employee_count`. Fewer than ~8 on target → the query is wrong, not the data:
   move misused fragments to their proper field, add `-tokens`, tighten
   phrases. On target → widen coverage with `|` synonyms in the same fields
   (`"machine learning"|"computer vision"|"nlp"`), re-probe.
4. **Fetch** the real volume (`count` up to 1000). More than 1000 matches →
   split by size bands / countries / founded ranges into disjoint queries.
5. **Free re-cuts**: `query_cache` on the result for sorting, counting,
   sub-segmenting — don't re-execute.
6. **Show it** (clients that render MCP Apps): `show_entity_table(cache_key,
   title=<intent>)` instead of pasting rows; when the user wants to qualify the
   list one by one, `review_leads(cache_key)` — the approved companies come back
   as a cache_key for people sourcing or CRM push (`anysite-mcp` → Tables, joins
   and lead review).

## Two hard limits to state up front (TAM planning)

Unlike people search, company search has **no `bucket_total`**, and its `dry_run`
count-only mode does not reach you through the MCP (the count travels in a response
header; the call returns an empty list). That means:

- **You cannot ask "how big is my ICP universe" cheaply** — there's no total
  count without pulling rows. Size the split blind, or probe representative
  sub-slices and extrapolate; tell the user the number is an estimate. (Still
  true regardless of `sort`.)
- **Plan the universe from the target backwards** when the user asks for TAM or
  tiers: accounts needed ≈ revenue goal ÷ deal size ÷ the win rate from contacted
  account to closed deal (ask for theirs; say it is an assumption if they have
  none). Then tier what you found — a few dozen 1:1 accounts, a few hundred
  1:few, the rest 1:many — rather than handing over one flat list.
- **A >1000 match returns only the top 1000 by rank**, so full coverage still
  needs splitting by size/country/founded into sub-queries each < 1000. With the
  relevance default the top is at least relevance-ordered rather than a pure
  recency head, but you still don't see rows 1001+. Note card freshness lags
  (`employee_count` drifts from reality on some records). Dedup on band
  boundaries by `urn` (`query_cache uniq`). `last_modified_after` +
  `sort: last_modified` is the right combo for a "new since last run" sweep.

## Read the bonus fields — they're the handoff

Every row carries, at no extra cost (names as in the call's table rows; full records
from `get_page` use `organizational_urn` / `website` / `crunchbase_link`):

- `company_id` → **feeds `anysite-people-sourcing`** (`current_company_id`) and
  `search_jobs` directly;
- `domain` → domain for CRM matching and `current_company_domain` people filters;
- `crunchbase_alias` → free crunchbase alias, skip the live 20cr search;
- `similar_organizations[]` → both an output list AND a **queryable filter** (the
  bigger lever — see below);
- `specialities[]` → the company's own vocabulary, reuse it to widen synonyms.

## similar_organizations as a filter — the reverse-orbit expander

Verified live: `similar_organizations: "\"fsd_company:1441\""` (Salesforce) +
`country_hq:["US"]` + size band returned 8 companies, all 8 carrying Salesforce in
their own similar-orgs graph. This is "who sits in the orbit of company X" — the
right tool for two jobs no keyword query does well:

- **ICP expansion from a seed account** — feed your best customer's `fsd_company`
  id, get its competitive/adjacent set.
- **Competitor-adjacency lists** — the closest this skill gets to "companies like
  my competitor". (It is NOT the competitor's customers — for that,
  `anysite-crm-competitor-intel` via wappalyzer/reviews.)

Noisy — roughly 3/8 were on-target in the test — so always combine with
`industry_name`/`specialities` and run the probe-validate loop. Batch-fetching the
output `similar_organizations[]` by `urn:[...]` (≤12 at a time) is the weaker,
one-hop version; the filter is the scalable one.

## When a different tool is right

- Funding stage / investors / valuation → `crunchbase/db/db_search` (dates as
  unix ts, count ≤100) or live `crunchbase/search` (`hiring`, `it_spend` filters).
- One known company by domain → `companies/resolve` (exact domain; recipe in
  `anysite-mcp` — several candidates can claim one domain, pick the right one).
- Early-stage / launches → `yc/search/search_companies`, `producthunt`, `betalist`.
- People at the sourced companies → `anysite-people-sourcing` with the URNs/domains
  from step "bonus fields". CRM push → `anysite-crm-prospect` (dedup + create rules).
