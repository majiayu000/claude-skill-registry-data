---
name: dv360-api-and-sdf-automation
description: Automate Display & Video 360 with the API, the Bid Manager reporting API, and Structured Data Files. Use when the user says "DV360 API", "automate DV360", "Structured Data Files", "SDF", "bulk edit", "bulk create line items", "pull a report with the API", "programmatic report", or asks "what is safe to automate" in DV360. Covers v4 resources, OAuth and service-account auth, SDF v10 download-edit-upload, the reports query workflow, and a safe-to-automate matrix with human-in-the-loop gates.
---

# DV360 API and SDF automation

How to read and change Display & Video 360 programmatically without breaking a live account. Three surfaces matter: the Display & Video 360 API for entity management, the Bid Manager API for report pulls, and Structured Data Files (SDF) for bulk CSV create and edit. This skill maps the resources, shows the safe workflows, and draws a hard line around what an agent must never automate.

For KPI math and definitions, see the `programmatic-foundations` skill. For what the reports mean once you have the CSV, see `dv360-reporting`. This skill is about the mechanics of automation and the guardrails, not about how to read the numbers.

## When to use this skill

- Building a script or integration against the DV360 API (entities, targeting, creatives, custom bidding, inventory sources, SDF download tasks).
- Pulling reports programmatically with the Bid Manager API instead of by hand.
- Doing bulk creates or edits with Structured Data Files.
- Deciding whether a given change is safe to automate, and what human gate it needs.

Boundaries with sibling skills:

- Report types, metrics, dimensions, and how to read a report: `dv360-reporting`.
- Bid strategy logic and custom bidding scoring: `dv360-bid-strategy` and `dv360-custom-bidding`.
- Diagnosing a delivery problem the automation surfaced: `dv360-troubleshooting`.

## Quick reference: pick the right surface

| Task | Surface | Notes |
| --- | --- | --- |
| Read or change one entity (line item, insertion order, targeting, creative) | DV360 API v4 | Full CRUD and bulk methods. |
| Bulk create or edit many entities from a spreadsheet | SDF v10 | Download via API or UI, edit CSV locally, upload via UI. |
| Pull a report on a schedule or on demand | Bid Manager API v2 | Create a query, run it, download the CSV from Cloud Storage. |
| Manage YouTube and Demand Gen resources in bulk | SDF v10 | SDF covers YouTube ad groups and ads. |
| Generate an SDF programmatically | DV360 API v4 `sdfdownloadtasks` | Produces the SDF; upload still goes through the UI. |

Three different APIs with three different OAuth scopes. The DV360 API and the Bid Manager API are separate services with separate scopes; do not assume one token works for both.

## Core process

### 1. Authenticate

Two credential models, both OAuth 2.0:

- **Service account (server-to-server).** Preferred for unattended automation. Create a service account, generate a JSON key, and associate the service account email with a DV360 user that has the needed role. The application then runs the server-to-server OAuth flow with that key. No interactive login.
- **User OAuth (installed app).** A human grants access in the browser once and the script stores the refresh token. Use this for local, interactive tooling.

Scopes:

- DV360 API read and write: `https://www.googleapis.com/auth/display-video`.
- DV360 user management: `https://www.googleapis.com/auth/display-video-user-management`.
- Bid Manager (reporting) API: `https://www.googleapis.com/auth/doubleclickbidmanager`.

Never hardcode a key. Read the credential path or contents from an environment variable (for example `GOOGLE_APPLICATION_CREDENTIALS` pointing at the JSON key file), and never commit the key. See `references/api-resources.md` for the auth detail and the official client libraries (.NET, Java, JavaScript, Objective-C, PHP, Python, Go, Node.js, Ruby).

### 2. Manage entities with the DV360 API (v4)

v4 is the current, generally available version (it left beta on March 27, 2025, with ongoing updates through mid-2026). The resource hierarchy is advertiser then campaign then insertion order then line item, with targeting attached to line items (and to higher levels) as assigned targeting options. Creatives, custom bidding algorithms, and inventory sources hang off the advertiser or partner.

The resources you will use most: `advertisers`, `advertisers.campaigns`, `advertisers.insertionOrders`, `advertisers.lineItems`, `advertisers.creatives`, `customBiddingAlgorithms`, `inventorySources`, `guaranteedOrders`, `firstPartyAndPartnerAudiences` and the other audience resources, `targetingTypes.targetingOptions` and the assigned-targeting subresources, and `sdfdownloadtasks`. Line items and insertion orders support bulk methods (for example bulk update and bulk edit of assigned targeting) so you do not have to loop one call per entity. Full resource and method map in `references/api-resources.md`.

Three v4 changes to code against:

- **Audience resource renamed.** The old `FirstAndThirdPartyAudience` resource is now `firstPartyAndPartnerAudiences`. Update any code that referenced the old name.
- **`optimizationObjective` is required on insertion orders.** In v4 the `optimizationObjective` field on an insertion order is required, so a create call that omitted it under an earlier version will fail. Set it explicitly.
- **Campaign and insertion-order assigned-targeting read methods were removed.** The `listAssignedTargetingOptions` methods on `advertisers.campaigns` and `advertisers.insertionOrders` (and the campaign `targetingTypes.assignedTargetingOptions` get and list methods) were sunset in v4. Read assigned targeting at the line-item level instead. Check the current reference before assuming a targeting read method exists on a higher-level entity.

A safety default of the API supports careful automation: a created line item starts in draft (`ENTITY_STATUS_DRAFT`), so a bulk create does not go live until you explicitly activate it. Use that as your built-in QA gate.

### 3. Pull reports with the Bid Manager API (v2)

The reporting surface is a separate service. The workflow is always the same three steps:

1. **Create a query.** Define the report (metrics, dimensions, date range, filters) and optionally a schedule. The query is a reusable definition.
2. **Run the query.** Running generates the report as a CSV stored automatically in Google Cloud Storage. Scheduled queries run on their own cadence.
3. **Download the CSV.** List the query's reports, take the most recent, and download it from the `googleCloudStoragePath` in the report metadata. Direct bucket access is not granted; you download through the path the API returns.

The helper script `scripts/dv360_report_puller.py` is a runnable skeleton of this flow. For report design (which metrics and dimensions to request), hand off to `dv360-reporting`.

### 4. Bulk create and edit with SDF (v10)

Structured Data Files are CSVs with one file per resource type. v10 is the current version. The workflow:

1. **Download** the current SDF, either through the UI or programmatically with the DV360 API `sdfdownloadtasks` resource.
2. **Edit the CSV locally.** Change existing rows to update resources, add rows to create resources, and remove rows you are not touching so the upload is small and fast. Partial SDF Upload lets you upload a subset of columns for the Line Items file, which keeps uploads small and fast; when you include a column you must include its whole column group or the upload fails, so check the format reference for the group each column belongs to.
3. **Upload through the UI.** SDF upload is UI-only. The API can download SDFs but cannot upload them. This is a deliberate guardrail: the bulk write always passes through a human in the UI.
4. **Process and review the result file.** After upload, read the result file to confirm which rows succeeded and which failed, and why.

SDF resource files cover Campaigns, Insertion Orders, Inventory Sources, Line Items, Media Products, YouTube Ad Groups, and YouTube Ads, with QA-format variants for Line Items and YouTube Ad Groups. SDF is the right tool for bulk create and edit and for YouTube and Demand Gen resources. The helper script `scripts/sdf_template.py` emits a minimal v10 Line Items header plus one example row to start from. Field-level detail and the workflow in full are in `references/sdf-workflow.md`.

## Safe-to-automate matrix

The single most important decision is not how to call the API but what to let the automation do unattended. Default to read and alert. Gate every write. Never automate destruction.

| Action | Verdict | Required control |
| --- | --- | --- |
| Read and monitor (pull entities, pull reports, watch pacing and delivery) | Safe | Log what you read. No write. |
| Bulk create from a validated template | Safe | Create in draft, QA the draft, then a human activates. |
| Guardrailed small bid change | Conditional | Hard caps on step size and frequency, full logging, and an approval gate before it applies. |
| Pause an underperformer | Conditional | Alert a human first. Do not auto-resume. Pausing is reversible but resuming is a judgment call. |
| Broad targeting change | Conditional | Human approval. Targeting changes move spend and reach in ways that are hard to reverse cleanly. |
| Cross-campaign budget reallocation | Conditional | Human approval. Moving budget between campaigns has strategy implications a script cannot weigh. |
| Delete or archive | Never automate | Do it by hand. Deletion and archival are destructive and easy to get catastrophically wrong at scale. |

Full rationale and edge cases in `references/safe-to-automate.md`.

## Human-in-the-loop patterns

Four patterns cover almost everything. Detail and pseudo-flows in `references/safe-to-automate.md`.

- **Monitor and alert.** The agent reads on a schedule and raises an alert when a threshold trips. It never writes. This is the safe default and where most automation should live.
- **Guardrailed change with an approval gate.** The agent proposes a bounded change (within hard step and frequency limits), logs it, and waits for a human approval before applying. Good for small bid nudges.
- **SDF bulk with a QA gate.** The agent prepares the SDF and validates it, a human reviews the diff, and the upload happens in the UI. The UI-only upload rule enforces this gate by design.
- **Staged custom-bidding rollout.** Roll a new custom bidding algorithm or score to a small slice first, watch it against a control, and only widen after it proves out. Never flip an account-wide bidding change in one step. Scoring logic lives in `dv360-custom-bidding`.

## Data-freshness caveats

Automation that decides on stale data is worse than no automation.

- Do not auto-optimize on conversion data that is only a few hours old. View-through and offline conversions lag, so a fresh "no conversions" reading is usually incomplete, not real. Wait for the data to mature.
- Reporting has latency. Build alerts and changes around matured data windows, not the last hour.
- When in doubt, widen the lookback and require the signal to persist across more than one read before acting.

## Security

- No secrets in code. Read the credential path or contents from an environment variable (for example `GOOGLE_APPLICATION_CREDENTIALS`) or a path the user supplies at runtime.
- Never commit a service-account key or refresh token. Keep key files out of the repository.
- Grant the service account the least DV360 role that the automation needs. A read-only monitor does not need write access.
- Log every write the automation performs so a change is always traceable to a run.

## Scripts

- `scripts/dv360_report_puller.py`: documented skeleton that creates and runs a Bid Manager report query and downloads the CSV. Reads credentials from an environment variable and takes partner or advertiser IDs and a date range as flags. Prints usage with no arguments. Network calls are guarded so importing it or running it with no arguments does not require live credentials.
- `scripts/sdf_template.py`: generates a minimal SDF v10 Line Items header plus one example row, to stdout or a path argument. Pure standard library. Prints usage with no arguments. Validate the output against the current SDF format reference before uploading.

## Reference material

- `references/api-resources.md`: DV360 API v4 resource and method map, auth detail, scopes, and client libraries. Read this when writing entity-management code.
- `references/sdf-workflow.md`: SDF v10 resource files, the download-edit-upload-review workflow, and what is API-able versus UI-only. Read this before a bulk create or edit.
- `references/safe-to-automate.md`: the full safe-to-automate rationale and the four human-in-the-loop patterns. Read this before letting any automation write to a live account.

## Sources

- DV360 API release notes (v4 GA March 27, 2025; SDF v10; campaign and insertion-order assigned-targeting read methods sunset): https://developers.google.com/display-video/api/release-notes (as of July 2026)
- DV360 API v4 REST reference (resource list): https://developers.google.com/display-video/api/reference/rest (as of July 2026)
- DV360 API v4 advertisers.lineItems: https://developers.google.com/display-video/api/reference/rest/v4/advertisers.lineItems (as of June 2026)
- DV360 API v4 advertisers.insertionOrders (optimizationObjective required): https://developers.google.com/display-video/api/reference/rest/v4/advertisers.insertionOrders (as of July 2026)
- DV360 API v4 firstPartyAndPartnerAudiences (renamed from FirstAndThirdPartyAudience): https://developers.google.com/display-video/api/reference/rest/v4/firstPartyAndPartnerAudiences (as of July 2026)
- DV360 API v4 sdfdownloadtasks: https://developers.google.com/display-video/api/reference/rest/v4/sdfdownloadtasks (as of June 2026)
- Use a service account (DV360 API): https://developers.google.com/display-video/api/guides/concepts/general/service-accounts (as of June 2026)
- Authorize requests (DV360 API): https://developers.google.com/display-video/api/guides/how-tos/authorizing (as of June 2026)
- Install client libraries (DV360 API): https://developers.google.com/display-video/api/guides/getting-started/libraries (as of June 2026)
- Structured Data Files overview: https://developers.google.com/display-video/api/guides/concepts/structured-data-files/overview (as of June 2026)
- Structured Data Files format (v10; Partial SDF Upload for Line Items): https://developers.google.com/display-video/api/structured-data-file/format (as of July 2026)
- Bid Manager API scheduled reports overview: https://developers.google.com/bid-manager/guides/scheduled-reports/overview (as of June 2026)
- Bid Manager API getting started: https://developers.google.com/bid-manager/guides/getting-started-api (as of June 2026)
- Bid Manager API v2 queries.create: https://developers.google.com/bid-manager/reference/rest/v2/queries/create (as of June 2026)
- Bid Manager API v2 queries.reports.list: https://developers.google.com/bid-manager/reference/rest/v2/queries.reports/list (as of June 2026)
