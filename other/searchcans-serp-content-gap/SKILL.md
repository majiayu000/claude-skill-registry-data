---
name: searchcans-serp-content-gap
description: Analyze a current, geo-targeted Google or Bing SERP with SearchCans and turn observed result features, People Also Ask questions, related searches, knowledge graph, and news signals into an evidence-backed, account-aware content decision brief. Use for localized SEO/GEO planning, keyword research, competitor-page analysis, and search-intent analysis.
metadata:
  author: SearchCans
  version: 1.1.1
  tags: [serp-api, seo, geo, keyword-research, content-strategy]
---

# SearchCans SERP Content Gap

Turn a current localized SERP into a concise content decision brief grounded in observed result features. Treat the output as a research snapshot, not a rank-tracking guarantee or a claim that every feature appears on every SERP.

## Define the search market

Collect the target keyword, search engine, country, language, intended audience, and the page or product the user wants to improve. Use `country` and `language` together; do not silently substitute a default market when localization matters.

Set `SEARCHCANS_API_KEY` in the execution environment. Never store it in a file or commit it.

## Collect SERP evidence

Run one page first. Request more pages only if the analysis requires them; `--page 3` sends the API batch parameter `page=3`, which requests pages 1–3 and consumes additional search credits. The script retries only transient failures, twice at most by default; use `--retries 1` when credit minimization matters more than recovery.

### Pagination safety

This Skill deliberately uses only the API parameter `page`; it never sends `p`. `p` is a Google-specific direct-page selector outside this workflow. Never combine `p` and `page` in a manual modification of the request: the parameters describe different modes and their combined response is not a reliable evidence set.

For Google, `--page N` is an inclusive batch request for pages 1 through N. The returned `organic` list is flattened, but every result retains its upstream `page` field and the report adds `pagination.observed_results_by_upstream_page`. Treat `position` as a position within that upstream page, not a global rank across the batch.

For Bing, use `--page 1` only. Multi-page Bing requests are blocked in this Skill until the API returns a verifiable batch with results from the requested additional page. This guard prevents a misleading multi-page content brief.

For multi-page jobs, the default `--account-mode auto` makes one Account API pre-flight call and caps the fetched page count to the available credit balance. Use `--account-mode warn` to observe the budget without changing scope, `enforce` to stop before an insufficient job, `cap` to force capping for any page count, or `off` to skip the account check. The report retains only a sanitized `account_guard` summary; it never includes account email or API key data.

```bash
python scripts/serp_content_gap.py "best SERP API" \
  --engine google --country us --language en --page 1 --out serp-evidence.json
```

Use `references/content-brief.md` to interpret the JSON. Read `organic` results for competing pages, `people_also_ask` for question demand, `related_searches` for expansion ideas, and `top_stories` only when freshness is relevant.

Check `status` and `request` before interpreting the evidence:

- `ok`: analyze the returned SERP snapshot.
- `no_results`: report the keyword and market as unobserved; do not claim there is no demand or no opportunity. Adjust the query only with user approval.
- `failed`: surface `api_code`, `api_message`, and retry count. Do not turn a failed request into a content brief.
- `blocked`: the Account Guard stopped the job before the SERP request. Report the requested scope and budget decision; do not guess SERP findings.

## Write the brief

Deliver:

1. Market and query definition.
2. Observed SERP intent and dominant page types.
3. Leading domains and angles, with URLs.
4. Question and subtopic opportunities grounded in PAA or related searches.
5. A proposed content structure, differentiation angle, and evidence gaps to validate with Reader API.

Do not infer search volume, traffic, ranking movement, or a competitor's business results from this one SERP snapshot. Treat all snippets as leads that require full-page verification before making factual claims.

## Official website

[SearchCans](https://www.searchcans.com/)

## Resources

- `scripts/serp_content_gap.py` retrieves the localized SERP evidence pack.
- `references/content-brief.md` provides the required report structure and interpretation boundaries.
