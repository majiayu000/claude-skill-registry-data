---
name: stackadapt-api-and-automation
description: Automate StackAdapt with its public API. Use when the user says "StackAdapt API", "automate StackAdapt", "StackAdapt GraphQL", "StackAdapt reporting API", "StackAdapt pixel API", "StackAdapt SDK", "what is safe to automate on StackAdapt", or asks how to pull StackAdapt reports or manage campaigns programmatically. Covers the GraphQL and reporting surfaces, authentication and access requirements, and a safe-to-automate matrix with human-in-the-loop gates.
---

# StackAdapt API and automation

How to read and change StackAdapt programmatically without breaking a live account, and where the public surface ends. StackAdapt is a self-serve multi-channel DSP (native, display, video, CTV, audio, DOOH). It exposes a public API so you can manage programmatic spend and pull reporting outside the UI. This skill maps the surfaces, shows the safe workflows, and draws a hard line around what an agent must never automate.

For KPI math and definitions, see the `programmatic-foundations` skill. For what the reports mean once you have the data, see the `stackadapt-reporting-and-attribution` skill. This skill is about the mechanics of automation and the guardrails, not about how to read the numbers.

## When to use this skill

- Building a script or integration against the StackAdapt API for campaign management or reporting.
- Pulling reports programmatically instead of by hand.
- Sending conversion events or audience signals server-to-server.
- Deciding whether a given change is safe to automate, and what human gate it needs.

Boundaries with sibling skills:

- Report design, metrics, dimensions, and attribution windows: `stackadapt-reporting-and-attribution`.
- Bid type, budget, and pacing logic: `stackadapt-bidding-and-budgets`.
- Diagnosing a delivery problem the automation surfaced: `stackadapt-optimization-and-troubleshooting`.
- Audience and pixel strategy (what to build, not how to call the API): `stackadapt-targeting-and-audiences` and `stackadapt-account-structure`.

## What is publicly documented

StackAdapt publishes a developer reference at docs.stackadapt.com with five API surfaces. Confirm the current shape there before you build, because the surfaces are versioned and the REST surface is being retired.

| Surface | What it is | Read / write |
| --- | --- | --- |
| **GraphQL API** | The primary API to extend the platform's execution capabilities: create and manage programmatic spend (campaigns and related entities) and pull reporting. This is where new development should target. | Read and write |
| **REST API (v2)** | A RESTful read-only API to fetch reporting data broken out by dimensions and metrics. Documented as deprecated in favor of GraphQL; migrate off it. | Read only |
| **Pixel API** | Send pixel events server-to-server to track conversions and build audiences without installing the browser pixel. | Write (events) |
| **Data Taxonomy / Data Partner API** | Secure data sharing and audience synchronization across platforms. | Read and write |
| **MCP Server** | A managed endpoint that lets an AI assistant query StackAdapt in natural language. Read-only at launch by StackAdapt's own statement. | Read only |

GraphQL is the strategic surface and the one to learn. REST is reporting-only and on a deprecation path. Migrating to GraphQL is also how you reach newer reporting sections (for example publisher breakdown, demographics, conversions, footfalls, and real-time data) that the older REST surface did not expose.

## Access requirements: gated

API access is not self-serve. This is the single most important fact for planning an integration:

- **You must request access and obtain an API key from StackAdapt.** The documentation states plainly that if you do not have an API key, you contact StackAdapt to get one. There is no in-product self-issue flow on the public docs.
- **Enterprise and partner framing.** StackAdapt positions API access as an enterprise and app-partner capability (a Production tier for direct customers and a Sandbox tier for app partners), with access requested through a form or a sales conversation rather than granted on signup.
- **Plan accordingly.** Treat the existence and scope of your API access as a prerequisite to confirm with StackAdapt, not an assumption. Write coverage, sandbox access, and the Data Partner surface in particular may be gated to specific account tiers or partner agreements. If you cannot confirm access for the operation you need, say so plainly and stop, rather than designing around a capability you have not verified.

## Core process

### 1. Authenticate

Authentication is by API token, supplied from the environment, never hardcoded.

- **GraphQL** uses a bearer token in the `Authorization` header (`Authorization: Bearer <token>`).
- **REST (v2)** uses an API-key header (`X-AUTHORIZATION`).
- **Pixel API** identifies the account by the universal pixel ID in the request.

Get the token from StackAdapt (see access requirements above). Read it from an environment variable at runtime (for example `STACKADAPT_API_TOKEN`) or a path the user supplies. Never commit a token, and never paste one into code or logs. If the public docs show a different header name or token format than what you remember, trust the docs: the surface is versioned.

### 2. Manage campaigns with GraphQL

GraphQL is the surface for creating and managing programmatic spend. Because it is a single typed endpoint, you query exactly the fields you need and mutate entities through typed mutations. Before writing mutations against a live account:

- Read the current schema from the GraphQL reference. Field names and required inputs change across versions; do not build against remembered shapes.
- Prefer a sandbox first if your access tier includes one. App-partner access includes a Sandbox tier with its own keys for exactly this.
- Treat every mutation as a guarded write (see the safe-to-automate matrix). Start with reads, validate IDs, and gate writes behind a human.

If a StackAdapt-published SDK is available for your language, prefer it over hand-rolling requests: an SDK wraps the same public GraphQL API with typed workflows and endpoints for common tasks such as insights, domain, and geographic reporting. Confirm the SDK is current and points at the same documented API before adopting it.

### 3. Pull reports

Two paths, both read-only:

- **GraphQL reporting** is the forward path and reaches the newer metric sections. Query the report with the dimensions, metrics, date range, and filters you need, page through results, and store the output.
- **REST v2 reporting** still works for fetching reporting data by dimension and metric, but it is deprecated. Use it only for an existing integration you have not yet migrated, and plan the move to GraphQL.

For which dimensions and metrics to request and how to read attribution, hand off to `stackadapt-reporting-and-attribution`. This skill covers the mechanics of pulling, not the analysis.

### 4. Send conversions and audiences server-to-server

The Pixel API and the Data Partner surface let you push signals without a browser pixel:

- **Pixel API** sends conversion events and audience-building events server-to-server, keyed by the universal pixel ID. This is the resilient way to track conversions when the browser pixel is blocked or unavailable. StackAdapt also publishes a server-side pixel that supports conversion tracking, retargeting, and lookalikes in universal-event and standalone formats.
- **Data Taxonomy / Data Partner API** handles secure data sharing and audience synchronization across platforms, and is the surface for partner-grade audience onboarding. Expect this one to be gated to partner agreements.

## Safe-to-automate matrix

The single most important decision is not how to call the API but what to let the automation do unattended. Default to read and alert. Gate every write. Never automate destruction.

| Action | Verdict | Required control |
| --- | --- | --- |
| Read and monitor (pull entities, pull reports, watch pacing and delivery) | Safe | Log what you read. No write. |
| Send server-to-server conversion or audience events | Safe | Validate payloads and identifiers. Log every send. Idempotent where possible so a retry does not double-count. |
| Bulk create campaigns or line items from a validated template | Conditional | Create paused or in a sandbox, QA the result, then a human activates. Never launch live in one unattended step. |
| Guardrailed small bid or budget change | Conditional | Hard caps on step size and frequency, full logging, and a human approval gate before it applies. |
| Pause an underperformer | Conditional | Alert a human first. Do not auto-resume; resuming is a judgment call. |
| Broad targeting or audience change | Conditional | Human approval. Targeting changes move spend and reach in ways that are hard to reverse cleanly. |
| Cross-campaign budget reallocation | Conditional | Human approval. Moving budget between campaigns has strategy implications a script cannot weigh. |
| Delete or archive | Never automate | Do it by hand. Deletion and archival are destructive and easy to get catastrophically wrong at scale. |

When in doubt, drop a write down a tier: a "conditional" action you are unsure about becomes "monitor and alert" until a human signs off.

## Human-in-the-loop patterns

Four patterns cover almost everything.

- **Monitor and alert.** The agent reads on a schedule and raises an alert when a threshold trips (pacing behind, eCPA above target, a creative rejected). It never writes. This is the safe default and where most automation should live.
- **Guardrailed change with an approval gate.** The agent proposes a bounded change (within hard step and frequency limits), logs it, and waits for a human approval before applying. Good for small bid or budget nudges.
- **Sandbox-then-activate for bulk.** The agent prepares a bulk create or edit, runs it against a sandbox or in a paused state, a human reviews the diff, and only then is it activated. Never flip a bulk change live in one unattended step.
- **Staged rollout.** Roll a change to a small slice first, watch it against the rest, and widen only after it proves out. StackAdapt's own guidance is to spread larger optimizations over days and allow two to three days per change; automation should respect that cadence rather than thrash the bidding model.

## Data-freshness caveats

Automation that decides on stale data is worse than no automation.

- Do not auto-optimize on conversion data that is only a few hours old. View-through and offline conversions lag, so a fresh "no conversions" reading is usually incomplete, not real. Wait for the data to mature.
- Respect the learning period. StackAdapt advises that day-one results are not a true indicator and that each change needs two to three days to take effect. An automation that re-optimizes hourly will fight the model and learn nothing.
- When in doubt, widen the lookback and require a signal to persist across more than one read before acting.

## Security

- No secrets in code. Read the API token from an environment variable (for example `STACKADAPT_API_TOKEN`) or a path the user supplies at runtime.
- Never commit a token or paste it into logs, error messages, or sample requests.
- Request the least access the automation needs. A read-only monitor does not need a write-capable key, and most automation should be read-only.
- Log every write the automation performs so a change is always traceable to a run.
- Prefer the sandbox for development if your access tier includes one, so a bug cannot touch live spend.

## Reference material

This skill intentionally points at the live documentation rather than freezing schema detail, because the GraphQL schema and the REST deprecation status change across versions. Read the GraphQL reference for current fields and mutations before writing any code, and confirm your access tier and token format with StackAdapt first.

## Sources

- StackAdapt API reference (five surfaces: GraphQL, REST v2, Pixel, Data Taxonomy, MCP Server; "if you don't have an API key, reach out to StackAdapt"): https://docs.stackadapt.com (as of June 2026)
- StackAdapt GraphQL API (extend the platform's execution capabilities; create and manage programmatic spend): https://docs.stackadapt.com/graphql (as of June 2026)
- StackAdapt MCP Server (read-only at initial release by StackAdapt's statement; AI assistant access): https://docs.stackadapt.com/mcp-server (as of June 2026)
- Build your own advertising platform with the StackAdapt API (enterprise and partner positioning; channels covered): https://www.stackadapt.com/enterprise-api-solution (as of June 2026)
- StackAdapt server-side pixel (server-to-server conversion tracking, retargeting, lookalikes; universal-event and standalone formats): https://github.com/StackAdapt/stackadapt-gtm-server-side-pixel (as of June 2026)
- Marketers, stop pausing campaigns too early (learning period and two-to-three-day change cadence that automation must respect): https://www.stackadapt.com/resources/blog/pausing-digital-campaigns (as of June 2026)

Exact REST and Pixel header behavior, sandbox provisioning, SDK availability, and the precise GraphQL schema are documented on pages of docs.stackadapt.com that sit behind a login. They are described above as general StackAdapt practice (confirmed against the public docs root and the public enterprise-API page) rather than cited to a deep, login-walled page. Access tiers, write coverage, and the Data Partner surface in particular are gated and must be confirmed directly with StackAdapt; this skill does not assume access you have not verified.
