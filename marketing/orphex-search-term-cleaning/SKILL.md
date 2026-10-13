---
name: orphex-search-term-cleaning
description: "Review supplied Search terms to separate irrelevant spend from relevant demand and prepare scoped, risk-aware negative keyword proposals."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Search Term Cleaning

Use this skill when someone asks which Search queries should be excluded, whether paid-search spend is being wasted on irrelevant demand, or how to draft a negative-keyword review. Work from user-supplied exports and documents; an already-authorized read-only data source is optional. Return a proposal, never an account edit.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at level `search_term` for queries, cost and outcomes. If `playbook.catalog` lists the negative keyword hygiene or brand search playbook, run it with `playbook.run`. Then list guides with `skill_catalog` (kind `guide`, topic `search_terms`, then `brand`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Establish what the rows mean

Ask for or extract the reporting window, account timezone, currency, campaign and ad-group IDs or names, search term, matched keyword, reported match type, impressions, clicks, cost, conversions, and conversion value if available. Also request the business definition of brand terms, protected products or services, target customer, conversion action, attribution window, current negative keywords and their scopes. Preserve the export's date and segment grain. If scope, currency, or brand rules are missing, label those fields unknown and do not widen a proposal to account level.

Check whether the period is complete for conversion lag and whether the report includes only visible query rows. Search term reports omit low-activity queries for privacy; an empty or short report does not prove that no other queries served. The report's match-type column describes the query's relation to the triggering keyword and can differ from that keyword's configured match type. Keep those fields separate. Use [Google's Search terms report guide](https://support.google.com/google-ads/answer/2472708?hl=en) for current column semantics.

## Classify before proposing exclusions

For each query, classify it as clearly irrelevant, relevant/protected, or uncertain using supplied product, audience, brand, and conversion evidence. Distinguish branded from nonbrand only with the provided brand dictionary or explicit user confirmation; mark ambiguous brand variants for review. Protect any query with a conversion, meaningful value, or an explicit business protection. A zero-conversion row is not proof of irrelevance, especially with few clicks, delayed outcomes, or an incomplete attribution window.

Calculate historical exposure from the selected rows only: sum cost, clicks, and conversions over the stated period. Show the query count and period beside the total. Call this “observed spend exposure,” not recoverable savings. A negative may reduce future cost, delivery, and conversions; it cannot guarantee savings or preserve every useful variant. Do not invent a universal click, spend, or conversion threshold.

## Choose match type and scope cautiously

Propose the narrowest negative that addresses the evidence. For Search negatives, broad excludes when all terms appear in any order, phrase excludes the same ordered phrase with possible surrounding words, and negative exact requires the same ordered terms with no added words, under Google's documented case/misspelling handling. These behave differently from positive keyword matching. Negatives do not use positive-keyword close-variant expansion. Google documents automatic casing and misspelling handling; separately review singular/plural, synonym, and other intended exclusions if needed. See [Google's negative keyword guide](https://support.google.com/google-ads/answer/2453972?hl=en).

Name a campaign or ad group only when the export proves that scope. Before suggesting a shared list or account-level exclusion, inspect every supplied campaign and protected/converting query it could affect. Check existing negatives, overlapping campaigns, brand/nonbrand intent, and product names that also appear in the proposed phrase. If those checks are unavailable, label the scope “unverified” and ask for review rather than recommending a wider block.

## Deliver an auditable proposal

Lead with the period, currency, campaign scope, data completeness, and any brand-definition gaps. Give one row per proposed term with: search term; class and rationale; proposed negative text and match type; proposed scope; impressions, clicks, cost, conversions/value; observed spend exposure; relevant or protected overlaps checked; blocking risks; confidence; and reviewer decision. Add a separate “keep” or “investigate” list for converting and ambiguous terms. Confidence describes evidence quality, not certainty of future impact. Tie every row to its source file, row identifier, or query and date.

Fictional example: a 30-day USD export shows “free repair manual” with $42 cost and no conversions, while “repair manual subscription” has two conversions. Propose reviewing the exact negative `[free repair manual]` at the demonstrated campaign scope; preserve the converting query. The $42 is past exposure, not a savings forecast, and unreported low-volume queries remain unknown.

Any later account mutation requires explicit user authorization naming the account, campaign/list scope, exact terms and match types, and action. This skill and an installed copy do not authorize changes.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
