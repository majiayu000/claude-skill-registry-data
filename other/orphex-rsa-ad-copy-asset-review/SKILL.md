---
name: orphex-rsa-ad-copy-asset-review
description: "Review RSA assets and approved claims for keep, replace, pin, or copy-test proposals; preserve overlapping asset metrics."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex RSA Ad Copy & Asset Review

Use this skill to review responsive search ad (RSA) headlines, descriptions, pins, and reported asset performance, or to draft new copy from approved evidence. Work from supplied exports, ads, landing pages, and brand or legal guidance. An authorized read-only source is optional. Produce reviewable recommendations, never publish or edit an ad.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at levels `asset` and `adtext` for headline and description performance. If `playbook.catalog` lists the ad-text variant pruning playbook, run it with `playbook.run`.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Collect the ad and business context

Request campaign/ad-group/ad identifiers, final URL, date range and timezone, currency, conversion action/window, business objective, and approved claims, offers, legal wording, voice, and prohibited language. For each asset, capture ID/text/type, enabled state, pin position, source/“added by” if present, impressions, clicks, cost, conversions/value, and the ad-level totals for the same scope. Include query themes or search terms and landing-page content where available. If only an asset report is supplied, do not infer unprovided campaign goals, approvals, or legal claims.

Use aligned date ranges and comparable asset types. Google reports full performance statistics for RSA assets for dates on or after June 5, 2025; earlier data may use different reporting. The former Performance label is deprecated. Check the current report columns and pinning semantics before interpreting an unfamiliar export. See [Google's RSA asset report guide](https://support.google.com/google-ads/answer/9564897?hl=en) and [RSA guide](https://support.google.com/google-ads/answer/7684791?hl=en).

## Interpret asset rows as directional evidence

RSA combinations vary. Asset-level impressions, clicks, cost, conversions, and value can be attributed per asset instance in a combination; totals across assets are not additive and ratios such as CTR, CPA, or ROAS are directional, not isolated causal effects. Compare an asset's served volume and outcome pattern with other assets of the same type in the same ad, while using ad-level totals for the overall result. A low-volume or never-served asset is “insufficient evidence,” not a loser. Ratings or Ad Strength can guide diversity and relevance checks; they do not prove that an asset caused a performance change.

Look for message themes supported by actual query intent, approved product facts, offer terms, landing-page language, and ad-level outcomes. Describe keep, replace, pin, unpin, or test as proposals. Pin only when a stated placement or legal requirement justifies reduced flexibility; verify current position guarantees and character/format rules in Google Ads before preparing publish-ready copy. Never invent discounts, guarantees, availability, performance claims, product features, or legal assurances. When source facts conflict, flag the conflict and withhold copy that depends on it.

## Draft a low-risk review

For each proposed action, state the asset ID and exact current text, evidence window and volume, status/pin, observed query or approved message theme, proposal, reason, expected uncertainty, and next review. For replacement copy, give the proposed text with the source fact that supports each claim, plus any remaining approval needed. Do not promise a lift or call the comparison a causal test. If the account has no control group or randomized experiment, recommend a measured test using ad-level outcomes and enough time for conversion lag rather than attributing changes to one asset.

Report conversion counts and values with their definitions; do not compare metrics across unlike attribution windows, currencies, or goals. If a denominator is zero or missing, mark the ratio unavailable. Note whether the report excludes paused or privacy-limited rows, and distinguish “not shown” from “underperformed.”

## Output and authorization

Lead with the review scope and data limits. Use a table with ad/ad-group; asset ID/type/text; pin/status; impressions/clicks/cost/conversions/value; source evidence; decision (keep, replace, pin, unpin, test, or hold); draft or change rationale; claim source; risk; confidence; and approver. Include a short set of coherent message themes rather than a pile of disconnected variants.

Fictional example: a 28-day USD RSA export shows headline H-17 “Same-day pickup” with 14,000 asset impressions, while the ad's landing page says pickup is available only in two cities. Keep only for a verified matching campaign or revise the draft to name those cities; do not call H-17 a conversion winner from asset rows alone. The ad-level total remains the outcome reference.

Any ad or asset mutation requires explicit user authorization naming the account, campaign/ad, exact text or pin changes, and timing. The presence of copy in an export or an installed skill grants no permission.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
