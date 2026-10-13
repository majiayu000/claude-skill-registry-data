---
name: orphex-conversion-tracking-health-check
description: "Audit supplied conversion configuration and safe diagnostics; separate transport acceptance, deduplication, and actual counted outcomes."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Conversion Tracking Health Check

Use this skill to check whether business events are configured, fired, transported, and counted as intended across tags, pixels, server APIs, imports, and analytics. It assesses tracking health; it does not expect attribution reports to match. Optional Orphex MCP reads may be used within the user's authorized scope.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `workspace.config_read` for connected pixels, analytics and store connections with their auth health, and `insights.read` for standing tracking findings. Then list guides with `skill_catalog` (kind `guide`, topic `measurement`, then `account_health`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Define the expected event path

Define the event's business meaning, exact name, primary/secondary role, bidding inclusion, source, value/currency rules, and expected user path. Record platform, account/property, site/app, dates, timezone, refresh time, attribution basis, and recent changes. Minimum evidence is the event definition plus a safe diagnostic, configuration view, or reproducible test. Redacted traces, retry behavior, counts, consent, and redirects help. Without a diagnostic or sample, report `unknown`. Use `not tested` only when the test is known not to have run and its required source and safe method are available; missing results alone do not establish that. A report total alone cannot prove health.

Use these finding statuses consistently:

- **Pass:** direct evidence confirms the expected event fired through the tested path with the required fields.
- **Fail:** a diagnostic or repeatable test shows a material setup defect, missing signal, duplicate, wrong value, or broken path.
- **Not tested:** a test has not yet been run, although the required source and method are available.
- **Unknown:** evidence, access, or definitions are missing or inconclusive.

An unavailable tag view is not a pass. Platform labels are not interchangeable: preserve the exact status and diagnostic text, then explain what it establishes and what it does not.

## Check implementation and integrity

Test the user path in a debug context. Check event name, page/app state, event time, currency, value, and source. Verify redirects preserve documented click IDs and UTMs where needed; the landing URL cannot prove later events retained them. Check consent behavior. Never bypass consent or call an intentionally suppressed event a defect.

For browser/server setups, compare documented deduplication fields and event names without exposing identifiers. Test retries for duplicate events; a repeated request is not automatically idempotent. Use a test purchase or redacted synthetic trace and verify the unique order reference is handled consistently. Keep customer data, click IDs, tokenized URLs, and order identifiers out of reports; state what was redacted and how to repeat the test safely.

Distinguish primary bidding events from secondary observation. Check value and currency consistency. Compare counts only when event, event-time basis, denominator, deduplication, timezone, and window align. Platforms may differ in attribution, interaction dates, modeling, consent, or processing delays; unequal totals alone do not prove a broken tag. Fractional attributed conversion credits do not establish duplicated business events. Use platform diagnostics and latency guidance before classifying a discrepancy.

## Findings and boundaries

For each finding, report status, severity, event/scope, evidence path and time, expected versus observed behavior, privacy-safe proof, confidence, next test, and owner. Base severity on impact to primary outcomes and path breadth, not a universal count threshold. Separate configuration evidence from report symptoms. Apply a correction only when a current or prior instruction authorizes the exact property/event change and the write path allows it. A test request does not authorize a production purchase or customer-data replay.

Fictional failure case: a synthetic checkout test shows one browser `Purchase` event and two server sends after a retry, with no shared deduplication reference in the redacted trace. Mark the tested path `fail`, confidence high for a duplicate-risk finding, and request the implementation owner to inspect retry and dedup logic. Do not change the server integration or replay a real order. If the only evidence were different Analytics and Ads totals, the result would be `unknown` pending aligned event definitions and platform diagnostics.

## Official references

- [Google Tag Assistant troubleshooting](https://support.google.com/tagassistant/answer/10039345?hl=en)
- [Google Ads conversion tracking status](https://support.google.com/google-ads/answer/12674892?hl=en)
- [Meta Conversions API: deduplicate Pixel and server events](https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events/)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.
