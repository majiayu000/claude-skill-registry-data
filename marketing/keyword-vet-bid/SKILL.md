---
name: keyword-vet-bid
description: Validate Pleasur.ai Stage 01 blog-keyword candidates with the Business potential, Intent, and Difficulty method using current Ahrefs evidence. Use before AIO vetting and prioritization to reject poor business fits, mismatched search intent, and SERPs the brand cannot realistically win.
---

# Keyword Vet — BID

Evaluate every candidate independently. Do not manufacture a winner or silently discard a failure. Read [references/bid-policy.md](references/bid-policy.md) before scoring.

## Required inputs

Require the Stage 01 run packet to contain:

- candidate keyword, target country, discovery source, volume, KD, traffic potential, parent topic, and Ahrefs intent labels;
- an approved, versioned Pleasur.ai brand/product snapshot with audience, pain points, live products, use cases, monetization model, and brand domain;
- current Pleasur.ai Domain Rating and its retrieval provenance;
- current top-ten organic SERP evidence for intent and difficulty;
- the current content inventory needed to identify existing strong coverage.

Use `needs_data` when a required input is absent, stale under the run's approved freshness policy, contradictory, or country-mismatched. Never convert missing values to zero.

## Evidence contract

- Use the configured Ahrefs integration as the only external SEO data source.
- Inspect the live tool/report schema before requesting fields; do not rely on legacy tool names or field shapes.
- Record provider, report/tool, exact query, country, selected fields, filters, retrieval time, provider freshness/reference, status, and error for every request.
- Reuse evidence only when its query, country, scope, and freshness satisfy the current run contract.
- Apply bounded retries from the workflow run packet. After the retry bound, return `needs_data`; do not substitute a provider, legacy cache, guessed value, or bare KD cutoff.
- Never expose credentials or mutate external systems.

## Process

### 1. Resolve brand authority

Use current Ahrefs evidence for Pleasur.ai DR. Brand DR is mandatory because Difficulty is relative to the site's authority. If it is unavailable, stop BID evaluation with `needs_data` and reason `brand_dr_unavailable`.

Treat KD as supporting evidence only. Never decide Difficulty from a universal cutoff such as `KD <= 70`.

### 2. Apply Business potential

Score `brand_fit` and `product_fit` from the approved brand snapshot, following the reference policy.

- Reject when `brand_fit < 4`.
- Reject when live products exist and `product_fit < 3`.
- Reject vanity-rank queries with no credible path to Pleasur.ai users or revenue.
- Set `business_value` from genuine product usefulness. Do not reward `best`, `review`, `pricing`, or other salesy phrasing by itself.
- Treat `business_value` as a prioritization signal, not an additional BID pass/fail threshold. A value of `1` may pass when the fit gates and credible-path check pass; downstream prioritization must preserve and penalize the weak path.
- Flag free-seeker terms such as free, unlimited, no-account, or without paying. Do not reject solely for this signal; prioritization applies the conversion penalty.
- When the approved snapshot explicitly has no products, skip the product gate, set `product_fit_applicable=false`, and record why.
- Return `needs_data` when `business_value` contradicts the fit evidence, such as `business_value=0` alongside a passing product-fit score and claimed credible business path.

### 3. Apply Intent

Use current Ahrefs keyword intent classification as the primary signal:

- pass informational intent;
- pass commercial-investigation intent suitable for a useful blog article;
- reject dominant transactional intent with `serp_is_transactional`;
- reject navigational-only intent with `serp_is_navigational`;
- inspect the current top ten when intent is empty, evenly mixed, or inconsistent with the observed SERP.

For the fallback, classify result page types and titles as informational, commercial investigation, transactional, or hybrid. Pass informational, commercial-investigation, and blog-suitable hybrid SERPs; reject transactional SERPs.

Run tool-led detection independently of Ahrefs intent labels. When at least three of the top five organic results are tools, calculators, or generators, set `serp_intent=tool-led` and route the candidate to tool opportunities rather than the blog queue. This is a routing result, not an Ahrefs intent value.

### 4. Apply Difficulty

Use ten usable current organic results when available. For each result, record URL, title, position, domain, DR or comparable Ahrefs authority evidence, link-strength evidence when available, page type, and intent match.

Calculate median top-ten DR. Count a weak link only when the packet names the URL and a concrete displacement reason such as:

- result DR strictly below `brand_dr + 5`;
- poor match to the dominant intent;
- thin or materially incomplete coverage;
- a forum, UGC, orphaned, or otherwise displaceable page type whose ranking is not explained by strong page-level evidence.

The numeric DR condition is required for `weak_link_count`; the qualitative evidence supplies the displacement rationale and must not increase the count on its own.

Pass Difficulty when either:

- `median_top10_dr <= brand_dr + 15`; or
- `weak_link_count >= 2`.

Do not call a result weak merely because its DR is lower than the median. If fewer than ten usable results exist, record the reduced sample; use `needs_data` if the sample cannot support a defensible decision.

### 5. Determine the verdict

- `PASS`: all three gates pass with complete evidence.
- `FAIL`: complete evidence exists and at least one gate fails.
- `needs_data`: a required gate cannot be evaluated reliably.

Preserve every candidate, including failures, in the immutable Stage 01 validated-research packet. A failed candidate must not proceed to AIO vetting or keyword prioritization.

## Output schema

For every candidate, persist:

- `keyword`, `country`, `bid_verdict`, and `bid_reason_codes`;
- `brand_fit`, `brand_fit_reason`, `product_fit`, `product_fit_reason`, `product_fit_applicable`, `business_value`, and `free_seeker`;
- `ahrefs_intents`, `observed_serp_intent`, `intent_match`, `intent_reason`, and `tool_led`;
- `brand_dr`, `median_top10_dr`, `weak_link_count`, named weak URLs, displacement rationales, `difficulty_match`, and `difficulty_reason`;
- all evidence provenance, uncertainties, freshness decisions, retry outcomes, and the policy version used.

## Quality checks

- Every candidate has a terminal BID result and specific reason.
- Every numeric score has evidence and rationale; scores are not flat-filled.
- Every PASS meets both fit thresholds and the credible-business-path check, has blog-suitable intent, and passes the DR-relative Difficulty gate.
- `business_value` is preserved for prioritization and is not applied as a second, conflicting Business threshold.
- Every weak link is named and justified.
- Tool-led results are routed, not treated as blog candidates.
- Missing evidence produces `needs_data`, never a guessed PASS or FAIL.
- No CSV, cache, repository, CMS, workflow, or production system was written or triggered.
