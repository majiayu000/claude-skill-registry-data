---
name: google-ads-api-and-bulk-operations
description: Read and change Google Ads at scale with the Google Ads API, Google Ads Editor, Google Ads scripts, and bulk uploads. Use when the user says "Google Ads API", "GAQL", "Google Ads Query Language", "Google Ads scripts", "Google Ads Editor", "bulk edit Google Ads", "bulk upload", "automate Google Ads", "mutate", "developer token", "manager account", "MCC", or asks "what is safe to automate" in Google Ads. Covers the current v24 API, GAQL, mutates, the four bulk-and-automation surfaces, and a safe-to-automate matrix. Google Ads is a separate platform from DV360; for the Display & Video 360 API see the dv360-api-and-sdf-automation skill.
---

# Google Ads API and bulk operations

How to read and change Google Ads programmatically without breaking a live account. Four surfaces matter: the Google Ads API for full programmatic control, Google Ads Editor for offline desktop bulk edits, Google Ads scripts for in-account JavaScript automation, and bulk uploads for spreadsheet-driven changes. This skill maps the resources, picks the right surface for a job, and draws a hard line around what an agent must never automate.

Google Ads is a different platform from Display & Video 360, and the Google Ads API is a separate service from the Display & Video 360 API (different endpoints, different auth, different resource model). For DV360 automation see the `dv360-api-and-sdf-automation` skill. Do not reuse a DV360 token, scope, or resource name here.

For KPI math and definitions (CPC, CPA, ROAS, impression share), see the `programmatic-foundations` skill. For what a report means once you have the rows, and which metrics and segments to request, see the `google-ads-reporting` skill. This skill is about the mechanics of automation and the guardrails, not about how to read the numbers.

## When to use this skill

- Building a script or integration against the Google Ads API (campaigns, ad groups, ads, criteria, assets, conversions, reporting).
- Writing GAQL to pull a report or retrieve entities.
- Doing bulk creates or edits with Google Ads Editor, bulk uploads, or sheets.
- Automating in-account tasks with Google Ads scripts.
- Deciding whether a given change is safe to automate, and what human gate it needs.

Boundaries with sibling skills:

- Account hierarchy, naming, and taxonomy: `google-ads-account-structure`.
- Report design, metrics, segments, and how to read a report: `google-ads-reporting`.
- Bidding strategy logic, budgets, and pacing: `google-ads-bidding` and `google-ads-budgets-and-pacing`.
- Performance Max strategy and asset guidance: `google-ads-performance-max`.
- Diagnosing a delivery problem the automation surfaced: `google-ads-optimization-and-troubleshooting`.

## Quick reference: pick the right surface

| Task | Surface | Notes |
| --- | --- | --- |
| Full programmatic control, integration, or a custom app | Google Ads API (v24) | GAQL to read, mutates to write. Needs a developer token and OAuth. |
| Pull a report or retrieve entities by query | Google Ads API, GAQL | `GoogleAdsService.SearchStream` or `Search`. Read only; GAQL never writes. |
| Offline bulk edits across whole accounts | Google Ads Editor | Free desktop app. Download account, edit offline, post changes back. |
| Scheduled in-account automation tied to account data or an external feed | Google Ads scripts | JavaScript in a browser-based editor, runs on Google's infrastructure, schedulable. |
| One-off large change from a spreadsheet, no code | Bulk uploads | Download a template, edit the sheet, upload. Good for non-developers. |

Rule of thumb: API for systems and integrations, Editor for a human doing heavy manual surgery, scripts for recurring in-account logic, bulk uploads for a one-time sheet-driven change. The API is the only surface an unattended agent should drive directly, and only behind the guardrails below.

## Core process (Google Ads API)

### 1. Get access: developer token, OAuth, and a manager account

Three things gate the API, and you need all three:

- **A Google Ads manager account (MCC).** The developer token lives in the API Center of a manager account, not a regular client account. Put the manager account at the root of the hierarchy to ease the token review.
- **A developer token.** Required on every API call. Tokens start at a restricted access level (Test or Explorer), which can only call test accounts or has capped usage, and move to Basic then Standard access after Google reviews the application. Plan for the review; do not assume day-one Standard access.
- **OAuth 2.0 credentials.** Every call is authorized with OAuth. Two models:
  - **Service account (server-to-server).** Preferred for unattended automation. Create a service account, download its JSON key, and add the service account email as a user on the Google Ads account it will manage. Unlike the DV360 service-account pattern, the Google Ads guide adds the service account directly as a Google Ads user rather than relying on Workspace domain-wide delegation.
  - **User OAuth (installed app or web).** A human grants access once and the app stores the refresh token. Use this for interactive tooling or to manage accounts on behalf of other users.

When you call on behalf of a client account under a manager, set the `login-customer-id` header to the manager account ID so the request is authorized through the hierarchy. Never hardcode the developer token, client secret, or refresh token. Read them from environment variables or a user-supplied path, and never commit them. See `references/api-resources.md` for the auth detail and the official client libraries.

### 2. Read with GAQL

The Google Ads Query Language (GAQL) is the read interface. It is SQL-like and read only: it retrieves resources, attributes, segments, metrics, and metadata, and it never mutates anything. Clauses: `SELECT` and `FROM` are required; `WHERE`, `ORDER BY`, `LIMIT`, and `PARAMETERS` are optional. You query one resource per `FROM`, and that resource determines which fields, segments, and metrics are joinable.

Two methods run a query, both on `GoogleAdsService`:

- `SearchStream` streams all rows in one response. Prefer it for large pulls.
- `Search` returns paginated rows. Use it when you need page-by-page control.

Reporting and entity retrieval use the same GAQL surface; a "report" is just a query that selects metrics and segments. For which metrics and segments to ask for, and how to read them, hand off to `google-ads-reporting`.

### 3. Change with mutates

Writes go through mutate operations, never through GAQL. Two shapes:

- **Service-level mutates.** Each resource has a service, for example `CampaignService.MutateCampaigns` or `AdGroupCriterionService.MutateAdGroupCriteria`. One resource type per call.
- **`GoogleAdsService.Mutate`.** A single endpoint that groups operations across multiple resource services in one atomic request, succeeding or failing as a unit. It supports temporary resource IDs so you can create a campaign and its children in one call.

Two safety properties of the API support careful automation. Mutates are atomic, so a partially applied bulk change does not leave half-built state. And cross-account mutating is blocked by default: an account cannot mutate objects it did not create unless it manages the account that created them, which contains the blast radius of a misconfigured credential.

Core resources you will use most: `customer`, `campaign`, `ad_group`, `ad_group_ad`, `ad_group_criterion`, `asset`, `asset_group`, and `conversion_action`. Performance Max replaces ad groups, ads, and keywords with `asset_group` (and listing groups for retail), so its structure and its mutates differ from Search and Display. Full resource and method map in `references/api-resources.md`.

### 4. Bulk and automation without the API

Three non-API surfaces cover bulk work for people who are not building an integration:

- **Google Ads Editor.** A free desktop application. Download one or more accounts, make changes offline in bulk (multi-select edits, find and replace, copy and paste across campaigns), then post the changes back. Best when a human is doing heavy manual restructuring and wants to review everything before it goes live.
- **Google Ads scripts.** JavaScript entered in a browser-based editor that runs on Google's infrastructure (not on your machine and not as local account code). Scripts read and change the account through search and mutate calls, can pull in external data (for example a conversion or inventory feed), and can be scheduled to run once, daily, weekly, or monthly. Best for recurring in-account logic that does not need a full external system.
- **Bulk uploads (sheets).** Download a spreadsheet template, edit it offline, and upload it to apply many changes at once. Best for a one-time, large, sheet-driven change by someone who does not write code.

Detail and the decision logic for picking among these are in `references/bulk-and-automation.md`.

## Safe-to-automate matrix

The single most important decision is not how to call the API but what to let the automation do unattended. Default to read and alert. Gate every write. Never automate destruction.

| Action | Verdict | Required control |
| --- | --- | --- |
| Read and monitor (run GAQL, pull reports, watch spend, pacing, and disapprovals) | Safe | Log what you read. No write. |
| Bulk create from a validated template | Safe | Create paused, QA the entities, then a human enables them. |
| Guardrailed bid change (manual CPC nudge or a target adjustment) | Conditional | Hard caps on step size and frequency, full logging, and an approval gate before it applies. |
| Guardrailed budget change | Conditional | Hard caps and an approval gate. A runaway budget script spends real money fast. |
| Pause an underperformer | Conditional | Alert a human first. Do not auto-resume. Pausing is reversible but resuming is a judgment call. |
| Add or change keywords, audiences, or other criteria | Conditional | Human approval. Targeting changes move spend and reach in ways that are hard to reverse cleanly. |
| Performance Max asset or asset-group change | Conditional | Extra care and human approval. Asset edits reset learning and reshape where spend goes across channels. |
| Cross-account or cross-campaign budget reallocation | Conditional | Human approval. Moving budget has strategy implications a script cannot weigh. |
| Remove or permanently delete anything | Never automate | Do it by hand. Removal is destructive and easy to get catastrophically wrong at scale. |

Full rationale and edge cases in `references/safe-to-automate.md`.

## Human-in-the-loop patterns

Four patterns cover almost everything. Detail and pseudo-flows in `references/safe-to-automate.md`.

- **Monitor and alert.** The agent runs GAQL on a schedule and raises an alert when a threshold trips (spend pace off, conversions stalled, ads disapproved). It never writes. This is the safe default and where most automation should live.
- **Guardrailed change with an approval gate.** The agent proposes a bounded change (within hard step and frequency limits), logs it, and waits for a human approval before sending the mutate. Good for small bid or budget nudges.
- **Bulk with a QA gate.** The agent prepares a bulk create or edit, validates it, and creates entities paused so a human reviews before enabling. The paused-on-create default is your built-in QA gate.
- **Staged rollout.** Roll a new automated change to a small slice first (one campaign, one ad group), watch it against the rest, and only widen after it proves out. Never flip an account-wide bidding or budget change in one step.

## Data-freshness caveats

Automation that decides on stale data is worse than no automation.

- Do not auto-optimize on conversion data that is only a few hours old. Some conversions import on a delay and attribution windows can be long, so a fresh "no conversions" reading is usually incomplete, not real. Wait for the data to mature.
- Reporting and stats have latency, and very recent windows are estimates that settle later. Build alerts and changes around matured windows, not the last hour.
- When in doubt, widen the lookback and require the signal to persist across more than one read before acting.

## Security

- No secrets in code. Read the developer token, OAuth client secret, and refresh token (or service-account key path) from environment variables or a path the user supplies at runtime.
- Never commit a developer token, client secret, refresh token, or service-account key. Keep credential files out of the repository.
- Grant the OAuth user or service account the least Google Ads access role the automation needs. A read-only monitor does not need admin or standard write access.
- Scope the work to the right accounts. Set `login-customer-id` deliberately, and rely on the API's cross-account mutate block as a backstop, not as your only guard.
- Log every mutate the automation sends so a change is always traceable to a run.

## Scripts

- `scripts/gaql_report_puller.py`: documented skeleton that builds a GAQL query and runs it through `GoogleAdsService.SearchStream` to pull a report. Reads credentials from environment variables and takes a customer ID, an optional login customer ID, and a date range as flags. Prints usage with no arguments. Network and client-library calls are guarded so importing it or running it with no arguments does not require live credentials or the client library installed.

The script is an optional helper. The playbook above stands on its own even if the script is never run. Validate any query and any change against the current reference before running it on a live account.

## Reference material

- `references/api-resources.md`: Google Ads API v24 core resources, GAQL read methods, mutate write methods, auth (developer token, OAuth, manager account, `login-customer-id`), scopes, and client libraries. Read this when writing API code.
- `references/bulk-and-automation.md`: Google Ads Editor, Google Ads scripts, and bulk uploads, with the decision logic for picking among them and what each can and cannot do. Read this before a bulk create or edit.
- `references/safe-to-automate.md`: the full safe-to-automate rationale and the four human-in-the-loop patterns. Read this before letting any automation write to a live account.

## Sources

- Google Ads API release notes (v24 current; v24.1 latest as of 2026-05-13): https://developers.google.com/google-ads/api/docs/release-notes (as of June 2026)
- Get started with the Google Ads API: https://developers.google.com/google-ads/api/docs/start (as of June 2026)
- Google Ads API concepts overview: https://developers.google.com/google-ads/api/docs/concepts/overview (as of June 2026)
- Obtain a developer token: https://developers.google.com/google-ads/api/docs/get-started/dev-token (as of June 2026)
- OAuth 2.0 overview (Google Ads API): https://developers.google.com/google-ads/api/docs/oauth/overview (as of June 2026)
- Use a service account (Google Ads API): https://developers.google.com/google-ads/api/docs/oauth/service-accounts (as of June 2026)
- Account management overview (manager accounts, login-customer-id): https://developers.google.com/google-ads/api/docs/account-management/overview (as of June 2026)
- Google Ads Query Language overview: https://developers.google.com/google-ads/api/docs/query/overview (as of June 2026)
- GAQL grammar: https://developers.google.com/google-ads/api/docs/query/grammar (as of June 2026)
- Reporting overview (SearchStream and Search): https://developers.google.com/google-ads/api/docs/reporting/overview (as of June 2026)
- Reporting reference, queryable resources (v24): https://developers.google.com/google-ads/api/fields/v24/overview (as of June 2026)
- Mutating resources overview: https://developers.google.com/google-ads/api/docs/mutating/overview (as of June 2026)
- Performance Max overview (API): https://developers.google.com/google-ads/api/docs/performance-max/overview (as of June 2026)
- Rate limits: https://developers.google.com/google-ads/api/docs/best-practices/rate-limits (as of June 2026)
- Client libraries: https://developers.google.com/google-ads/api/docs/client-libs (as of June 2026)
- Google Ads scripts (developer docs): https://developers.google.com/google-ads/scripts (as of June 2026)
- About Google Ads Editor: https://support.google.com/google-ads/editor/answer/2484521 (as of June 2026)
- Using scripts to make automated changes: https://support.google.com/google-ads/answer/188712 (as of June 2026)
- Bulk edits (definition and tools): https://support.google.com/google-ads/answer/144560 (as of June 2026)
