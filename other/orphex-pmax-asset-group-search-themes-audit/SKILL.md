---
name: orphex-pmax-asset-group-search-themes-audit
description: "Review PMax asset groups, destinations, themes, and Search overlap; distinguish optimization signals from targeting and causal evidence."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex PMax Asset Group & Search Themes Audit

Use this skill to review whether Performance Max asset groups and search themes reflect the supplied offer and observed search demand, or to investigate possible overlap with Search campaigns. Work from exports and documents the user provides; an authorized read-only data source is optional. Return an audit and proposals only.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at level `asset` for asset-group assets and at level `search_term` for Search overlap. If `playbook.catalog` lists the PMax asset-group coverage playbook, run it with `playbook.run`.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Inputs and limits

Request campaign and asset-group IDs/names, reporting dates/timezone, currency, campaign-level spend and conversion/value outcomes, conversion action/window, goals, asset IDs/types/text/status, final URLs and URL expansion setting, search themes, audience signals, and brand exclusions/negative keywords. Add search-term or insights rows with any “source” dimension, related Search keyword/campaign inventory, and approved product/brand facts where available. Ask whether the current period has matured for conversion lag. Without campaign-level outcomes or definitions, summarize structure and coverage without ranking business performance. Without Search controls, label overlap “not assessable.”

Search theme and search-term insights may represent grouped, privacy-limited demand, and asset or theme reports may not expose all serving contexts. Record the exact source and grain. Keep each campaign's objective and dates separate. Google describes Search themes as broader AI signals that provide context, not traditional keyword targets; [read the current Search themes guide](https://support.google.com/google-ads/answer/16669486?hl=en) and [PMax search controls](https://support.google.com/google-ads/answer/16672776?hl=en) when available fields or controls are unclear.

## Audit theme and asset alignment

Treat an asset group as a coherent bundle of creative, URL, and related audience context. Check whether the text, images/video, final URL, and stated theme match a real product, audience need, language/region, and approved promise. Identify empty, duplicated, generic, or mismatched groups only when the supplied rows show it. Compare themes with the landing page and observed searches to find useful missing context; lexical novelty alone is not incremental demand. Recommend broader or more specific themes only as candidates supported by the advertiser's product knowledge or visible query evidence. Do not treat audience signals as proof of who saw an ad or as hard targeting restrictions; check [Google's current audience signals guidance](https://support.google.com/google-ads/answer/14530785?hl=en-CA) before interpreting an unfamiliar field.

Search overlap is a hypothesis, not automatic cannibalization. Compare matched queries, brand/nonbrand definition, campaign type, eligibility, Search exact-match coverage, location/language, negatives and exclusions, dates, and conversion definitions. Search and PMax may have different inventory and attribution behavior. A shared query or conversion does not show which campaign caused incremental business. State missing control evidence and avoid assigning blame from a cross-campaign table alone.

## Read performance at the right level

Use campaign-level totals to describe campaign outcomes, consistent with [Google's PMax asset-group reporting guidance](https://support.google.com/google-ads/answer/13872527?hl=en_us_us). Asset impressions, clicks, conversions, or value can be attributed to multiple assets used together and should not be summed to reconstruct campaign totals. Treat per-asset rates as directional diagnostics; asset group rows are context for a theme or URL, not proof that a single asset caused a result. Compare like campaign objectives, dates, currencies, goals, and attribution windows. Show counts and denominators; mark missing, zero, and lagged data distinctly.

Do not hardcode theme, asset, or character limits because platform capabilities change. Check the current Google Ads UI/help before recommending a numeric limit or a control. Where the export lacks field-level status or serving coverage, mark it unverified rather than interpreting absence as inactive.

## Deliver the audit

Provide scope, objective, date window, currency, conversion definition, lag status, and sources. Use one row per campaign/asset group with group theme and ID; asset/URL coverage; search themes and signal context; observed query themes and source; possible Search overlap evidence; campaign-level outcomes; gaps or risks; proposed review; confidence; and missing checks. Separate facts, hypotheses, and proposals. Give each claim a source file, row, or report segment and preserve campaign-level totals.

Fictional example: one 45-day PMax campaign has separate “starter kit” and “replacement parts” groups, but both point to the same generic landing page; its search insights show “replacement filter refill” attributed to Search. Flag a URL/theme alignment review and compare Search eligibility and brand settings. This does not establish Search cannibalization or that changing the theme will produce additional conversions.

Changing themes, assets, exclusions, URLs, or campaign settings requires explicit user authorization for the named account and exact edits. This audit never applies changes.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.
