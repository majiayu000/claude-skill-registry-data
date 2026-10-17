---
name: ttd-api-and-automation
description: Automate The Trade Desk safely at a publicly supportable level, and know where the public surface ends. Use when the user says "Trade Desk API", "TTD API", "automate The Trade Desk", "TTD raw event data feed", "what is safe to automate on TTD", or asks how to manage campaigns or pull reporting on TTD programmatically. States up front that the full API and its documentation are partner-gated, describes the REST API for campaign management and reporting and the raw event data feed for log-level data, and gives a safe-to-automate matrix with human-in-the-loop gates. No secrets in code.
---

# The Trade Desk API and automation

How to plan automation against The Trade Desk (TTD) without breaking a live account, and where the public surface stops. Read this first: the full TTD API and its reference documentation are partner-gated. You need a TTD account and credentials issued by TTD, and the developer portal sits behind a partner login. Nothing in this skill is a substitute for that reference. This skill maps the surfaces at the publicly supportable level, gives the safe workflows and the guardrails, and draws a hard line around what an agent must never automate and around inventing endpoint detail.

For KPI math and definitions, see the `programmatic-foundations` skill. For what to measure and what the reporting means, see the `ttd-measurement-and-reporting` skill. For building the right report for an objective, see `reporting-by-campaign-goal`, and for multi-touch path thinking see `path-to-conversion-analysis`. This skill is about the mechanics of automation and the guardrails, not about how to read the numbers.

## Read this first: the API is partner-gated

This is the single most important fact for planning a TTD integration. State it plainly to the user before designing anything:

- **You need a TTD partner account and credentials.** API access is not self-serve. Login credentials and any API token are obtained through your TTD account or representative, not issued on public signup.
- **The reference documentation requires a partner login.** The developer and partner portal that holds the endpoint reference, authentication detail, request and response schemas, and rate limits is gated. Public marketing pages confirm the API exists and what it is for; they do not publish the endpoint reference.
- **Therefore: do not invent endpoint paths, field names, feed names, or limits.** When the user needs an exact route, parameter, schema, or rate limit, point them to the partner developer portal and their TTD representative. Describe the workflow and the guardrails, which are stable, rather than a specific path you cannot verify.

If you cannot confirm access or the exact contract for an operation, say so and stop, rather than designing around a capability or a route you have not verified.

## When to use this skill

- Planning a script or integration against TTD for campaign management or reporting.
- Pulling reporting programmatically instead of by hand.
- Moving log-level / raw event data out of TTD for analysis or modeling.
- Deciding whether a given change is safe to automate, and what human gate it needs.

Boundaries with sibling skills:

- What the measurement data means and what to measure (marketplace providers, brand lift, attribution, raw event data as a concept): `ttd-measurement-and-reporting`.
- Report design for a goal (which metrics and dimensions, what good looks like): `reporting-by-campaign-goal`.
- Metric and KPI definitions and formulas: `programmatic-foundations`.
- Cross-DSP path-to-conversion thinking: `path-to-conversion-analysis`.

## The public surface, at a supportable level

TTD publicly positions itself as an API-extensible platform: brands, agencies, and partners can access APIs, custom solutions, and data to build on the platform and integrate it into their own systems. At the publicly supportable level there are two surfaces an automation cares about. Confirm the exact contract for each in the partner developer portal before you build.

| Surface | What it is (public level) | Read / write | Where the detail lives |
| --- | --- | --- | --- |
| **REST API** | Programmatic campaign management and reporting: manage entities and pull reporting data outside the UI. | Read and write | Partner developer portal (gated) |
| **Raw event data feed** | Log-level event data delivered to partners for advanced, custom analysis and modeling in your own environment. | Read (export) | Partner developer portal (gated) |

The REST API is the surface for managing campaigns and pulling reports. The raw event data feed is the surface for log-level data you analyze yourself (the analysis use cases live in `ttd-measurement-and-reporting`). Specific resource paths, parameters, authentication headers, schemas, delivery mechanics, and rate limits are partner-gated. Do not assume a shape from memory.

## Core process

### 1. Confirm access and authenticate

- **Get credentials from TTD.** Obtain account access and any API credentials through your TTD account or representative. There is no public self-issue flow.
- **Read the current auth contract from the partner portal.** The authentication scheme, token lifetime, and header format are defined there and can change. Do not hardcode an auth flow from memory; confirm it against the gated reference.
- **No secrets in code.** Read credentials from an environment variable at runtime (for example a `TTD_API_TOKEN` or a login/secret pair your code reads from the environment) or from a path the user supplies. Never hardcode a token or password, never paste one into code, logs, error messages, or sample requests, and never commit one.
- **Least privilege.** Request the least access the automation needs. A read-only monitor must not run with write-capable credentials. Most automation should be read-only.

### 2. Manage campaigns with the REST API

The REST API is where you create, read, update, and query campaign entities programmatically. Before writing anything against a live account:

- **Read the current schema from the partner portal.** Resource paths, required fields, and enums are gated and versioned. Build against the live reference, not a remembered shape.
- **Start with reads.** Validate IDs and confirm you are pointed at the right account and entities before any write.
- **Treat every write as a guarded change.** Apply the safe-to-automate matrix below. Gate writes behind a human, cap step size and frequency, and log every change.

### 3. Pull reporting with the REST API

Reporting can be pulled programmatically instead of by hand. The stable shape of the workflow, independent of exact routes:

1. **Define the report** (metrics, dimensions, date range, filters) per the gated reference.
2. **Request or schedule the run** so the report generates on demand or on a cadence.
3. **Retrieve the output** and store it, then page through results as needed.

For which metrics and dimensions to request and how to read attribution, hand off to `ttd-measurement-and-reporting` and `reporting-by-campaign-goal`. This skill covers the mechanics of pulling, not the analysis.

### 4. Move log-level data with the raw event data feed

The raw event data feed exports event-level data for analysis in your own environment (warehouse joins, custom measurement, media mix and attribution modeling). Treat it as a read/export surface:

- **Confirm the feed name, schema, delivery, latency, and retention in the partner portal.** All of these are gated. Do not invent a feed name or a field name.
- **Automate the export as monitoring-grade work.** Pulling the feed on a schedule is safe; what you do with it downstream follows the same data-freshness discipline as everything else.
- **Privacy first.** Log-level data is sensitive. Handle it in a privacy-conscious way, restrict access, and never log raw records into application logs.

## Safe-to-automate matrix

The single most important decision is not how to call the API but what to let the automation do unattended. Default to read and alert. Gate every write. Never automate destruction.

| Action | Verdict | Required control |
| --- | --- | --- |
| Read and monitor (pull entities, pull reports, watch pacing and delivery) | Safe | Log what you read. No write. |
| Export the raw event data feed on a schedule | Safe | Read-only export. Restrict and protect the data. Idempotent retrieval so a retry does not duplicate downstream. |
| Bulk create campaigns or entities from a validated template | Conditional | Create paused, QA the result, then a human activates. Never launch live in one unattended step. |
| Guardrailed small bid or budget change | Conditional | Hard caps on step size and frequency, full logging, and a human approval gate before it applies. |
| Pause an underperformer | Conditional | Alert a human first. Do not auto-resume; resuming is a judgment call. |
| Broad targeting or audience change | Conditional | Human approval. Targeting changes move spend and reach in ways that are hard to reverse cleanly. |
| Cross-campaign budget reallocation | Conditional | Human approval. Moving budget between campaigns has strategy implications a script cannot weigh. |
| Delete or archive | Never automate | Do it by hand. Deletion and archival are destructive and easy to get catastrophically wrong at scale. |

When in doubt, drop a write down a tier: a "conditional" action you are unsure about becomes "monitor and alert" until a human signs off.

## Human-in-the-loop patterns

Four patterns cover almost everything.

- **Monitor and alert.** The agent reads on a schedule and raises an alert when a threshold trips (pacing behind, eCPA above target, a creative rejected, a feed delivery missing). It never writes. This is the safe default and where most automation should live.
- **Guardrailed change with an approval gate.** The agent proposes a bounded change (within hard step and frequency limits), logs it, and waits for a human approval before applying. Good for small bid or budget nudges.
- **Paused-then-activate for bulk.** The agent prepares a bulk create or edit, runs it in a paused state, a human reviews the diff, and only then is it activated. Never flip a bulk change live in one unattended step.
- **Staged rollout.** Roll a change to a small slice first, watch it against the rest, and widen only after it proves out. Never flip an account-wide change in one step; give the optimization model time to settle rather than thrashing it.

## Data-freshness caveats

Automation that decides on stale data is worse than no automation.

- Do not auto-optimize on conversion data that is only a few hours old. View-through and offline conversions lag, so a fresh "no conversions" reading is usually incomplete, not real. Wait for the data to mature.
- Reporting and feed delivery have latency. Build alerts and changes around matured data windows, not the last hour, and confirm the feed's actual latency in the partner docs rather than assuming.
- When in doubt, widen the lookback and require a signal to persist across more than one read before acting.

## Security

- No secrets in code. Read credentials from an environment variable (for example `TTD_API_TOKEN`, or a login and secret your code reads from the environment) or a path the user supplies at runtime.
- Never commit a token or password, and never paste one into logs, error messages, or sample requests.
- Request the least access the automation needs. A read-only monitor does not need write-capable credentials, and most automation should be read-only.
- Log every write the automation performs so a change is always traceable to a run.
- Treat raw event data as sensitive: restrict access, handle it in a privacy-conscious way, and keep raw records out of application logs.

## Reference material

This skill intentionally points at the live partner documentation rather than freezing endpoint detail, because the API reference is gated, versioned, and changes over time. Read the partner developer portal for current resource paths, authentication, request and response schemas, reporting workflow, raw-event-feed schema and delivery, and rate limits before writing any code, and confirm your account access and credentials with TTD first. If you cannot confirm the exact contract for an operation, say so and stop rather than guessing a route or field.

## Sources

- The Trade Desk, Our Platform overview (API-extensible platform; access APIs, custom solutions, and data; developer documentation referenced; identity, measurement, audiences, AI decisioning, OpenPath): https://www.thetradedesk.com/us/our-platform (as of June 2026)
- The Trade Desk, Measurement and Optimization (programmatic reporting and outcome measurement the API and feed support; first-party conversion data; multi-touch attribution and media mix modeling; marketplace of independent measurement providers): https://www.thetradedesk.com/our-demand-side-platform/advertising-campaign-performance-measurement (as of June 2026)
- The Trade Desk launches Kokai (Partner Portal with standard adapters for integrations, including measurement, retail onboarding, and third-party audience data; partners building on the platform), June 2023: https://www.thetradedesk.com/press-room/the-trade-desk-launches-kokai-a-new-media-buying-platform-that-brings-the-full-power-of-ai-to-digital-marketing (as of June 2026)
- The Trade Desk, OpenPath (direct buyer-to-seller supply path; part of the platform an integration may touch): https://www.thetradedesk.com/us/our-platform/openpath (as of June 2026)
- The Trade Desk press room (public newsroom index): https://www.thetradedesk.com/press-room (as of June 2026)

The full TTD API and its reference documentation (endpoint paths, authentication scheme, request and response schemas, the raw event data feed's name and schema and delivery, and rate limits) are hosted on the TTD partner developer portal and require a TTD partner account and login. They are described above only at the publicly supportable level confirmed against TTD's public product pages and newsroom. This skill deliberately does not state or invent endpoint paths, field names, feed names, or numeric limits; those require TTD partner and API access and must be confirmed in the partner developer portal and with the TTD representative.
