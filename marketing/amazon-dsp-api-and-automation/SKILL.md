---
name: amazon-dsp-api-and-automation
description: Automate Amazon DSP through the Amazon Ads API. Use when the user says "Amazon Ads API", "Amazon DSP API", "automate Amazon DSP", "AMC API", "Amazon DSP reporting API", "Login with Amazon", "Amazon Ads profile", "Amazon DSP audiences API", or asks "what is safe to automate on Amazon". Covers Login with Amazon auth, the profile and advertiser account model, the developer access and allowlisting requirement, the DSP campaign management, reporting, audiences, and AMC API areas, what is self-service automatable versus managed-service only, and a safe-to-automate matrix with human gates. Amazon DSP is distinct from Amazon Ads sponsored ads; both ride the same Amazon Ads API.
---

# Amazon DSP API and automation

How to read and change Amazon DSP programmatically without breaking a live account. There is no separate "DSP API" product. Amazon DSP is one of several solutions served by the single Amazon Ads API, alongside sponsored ads, streaming TV, Amazon Marketing Cloud (AMC), and Amazon Marketing Stream. This skill maps the API areas that matter for DSP, the auth and account model that gates all of them, what is automatable for a self-service account versus what stays managed-service only, and a hard line around what an agent must never automate.

Amazon DSP is not the same thing as Amazon Ads sponsored ads. Sponsored Products, Sponsored Brands, and Sponsored Display are keyword-and-product-driven ads inside Amazon's own surfaces. Amazon DSP is programmatic display, video, and audio buying that reaches audiences on and off Amazon. Both are served by the Amazon Ads API, but they are different solutions with different resources, different access requirements, and different reporting. Do not assume a sponsored-ads integration covers DSP.

For KPI math and definitions (CPM, CPC, ROAS, reach, frequency), see the `programmatic-foundations` skill. For DSP report design, the metrics and dimensions to request, and how to read the numbers once you have them, see the `amazon-dsp-measurement-and-reporting` skill. This skill is about the mechanics of automation and the guardrails, not about how to read the numbers.

## When to use this skill

- Building a script or integration against the Amazon Ads API to touch Amazon DSP (campaigns, ad groups, targets, creatives, audiences, reports).
- Pulling DSP reports programmatically instead of by hand.
- Working with the AMC API for clean-room reporting and audience creation tied to DSP.
- Deciding whether a given DSP change is safe to automate, and what human gate it needs.
- Figuring out whether your account can write to DSP through the API at all, or whether it is managed-service only.

Boundaries with sibling skills:

- DSP report metrics, dimensions, and how to read a report: `amazon-dsp-measurement-and-reporting`.
- Audience strategy and segment selection: `amazon-dsp-audiences`.
- Bidding and optimization logic: `amazon-dsp-bidding-and-optimization`.
- Account, advertiser, and seat structure: `amazon-dsp-account-structure`.
- KPI definitions and shared math: `programmatic-foundations`.

## Quick reference: API areas for DSP

| Goal | API area | Access reality |
| --- | --- | --- |
| Read and change DSP campaigns, ad groups, targets, creatives | DSP campaign management | Self-service DSP advertisers and their authorized partners. Not available to managed-service-only accounts. |
| Pull DSP performance reports | Reporting API (DSP reports) | Available to accounts with DSP access. Asynchronous: request, poll, download. |
| Discover and manage audiences for DSP | Audiences API | Available to accounts with DSP access. Discovery plus DSP audience resources. |
| Build audiences and run clean-room analytics from signals | Amazon Marketing Cloud (AMC) API | Requires an AMC instance. Reporting, audiences, and signal management. |
| Receive near-real-time campaign and event data | Amazon Marketing Stream | Push delivery to your own AWS resources, separate setup. |

One API, one auth model, many solutions. A token that works for sponsored ads does not automatically grant DSP scope or DSP account access. Access is granted per solution and per account, so confirm DSP access explicitly before assuming a write path exists.

## Core process

### 1. Get access: developer registration and allowlisting

The Amazon Ads API is not open. Three things gate it, and you need all three before any DSP call:

- **An approved Amazon Ads API application.** You request access and Amazon reviews the application before granting it. The path varies by organization type: a third party building tools for others, an advertising solution provider, an agency with engineering resources, or an advertiser running a significant volume directly. Plan for the review. Do not assume day-one access.
- **A Login with Amazon (LWA) security profile.** This is the OAuth client. You create it in the Amazon developer console and then associate API access with it. It produces the client ID and client secret.
- **DSP access on the account, and consent.** DSP campaign management is allowlisted to self-service DSP advertisers and the partners they authorize. If you are a partner acting for an advertiser, you obtain that advertiser's consent to access their DSP account before you can manage it. An approved API application alone does not grant DSP write access; the account itself must have self-service DSP and must consent.

If the account is managed-service only (Amazon's team runs the buying), DSP campaign management through the API is not available to you. You can still pull reports and, depending on setup, work with audiences and AMC, but you cannot programmatically create or edit the campaigns. Say this plainly to the user rather than promising a write path that does not exist.

### 2. Authenticate with Login with Amazon

Every call is authorized with OAuth 2.0 through Login with Amazon. The flow:

1. **Authorize once.** A user with access to the Amazon Ads account grants your LWA application consent in the browser. You receive an authorization grant.
2. **Exchange for tokens.** Trade the grant for an access token and a long-lived refresh token by POSTing to the LWA token endpoint with your client ID and client secret.
3. **Call the API.** Send the access token plus your client ID on each request. Set the profile header to scope the call to the right account (see step 3).
4. **Refresh before expiry.** Access tokens are short-lived (about one hour). Refresh on a margin (around the 55-minute mark) so an in-flight request never fails on an expired token. Refresh tokens persist; store them securely.

Never hardcode the client secret, refresh token, or access token. Read them from environment variables or a path the user supplies at runtime, and never commit them. Treat the refresh token like a password; it is the long-lived credential.

### 3. Understand the profile and advertiser account model

The Amazon Ads API scopes almost every request to a profile. A profile represents an advertiser's account in a specific marketplace (country). You list the profiles your authorization can see, pick the right one, and pass its identifier in the profile header so the API knows which account and marketplace the request applies to.

For DSP, the profile selects the advertiser context, and DSP resources (campaigns, ad groups, audiences) live under the advertiser the profile maps to. The same LWA authorization can see multiple profiles across multiple accounts and marketplaces, so selecting the wrong profile is a real way to act on the wrong account. Resolve the profile deliberately and log which profile every write used. OAuth separates three things and you should keep them separate in your head and your code: application identity (client ID and secret), user authorization (access and refresh tokens), and account scope (the profile).

### 4. Manage DSP entities (campaign management API)

Where DSP campaign management is available to you, it exposes the buy structure as resources: campaigns, ad groups, targets, creatives, and creative associations. You can read them with batch reads to mirror the account locally, and create, read, and update them to run campaigns inside your own workflow. The intended use is exactly the automation pattern this skill guards: pull performance, then adjust ad group and targeting settings against it, experiment with new audiences, and remove audiences that underperform.

Confirm which operations your account and allowlist actually permit before building against them. Feature availability moves (some surfaces ship in beta first), and a given account may have read access without write. When a feature is in beta, gated, or not publicly documented for your account type, treat it as unavailable until you confirm it, and tell the user it is gated rather than assuming it works.

### 5. Pull DSP reports (reporting API)

DSP reporting is asynchronous. The shape is always the same:

1. **Request a report.** Define the report type, metrics, dimensions, and date range, and submit the request. The API returns a report identifier.
2. **Poll for completion.** Check status until the report is ready. Large reports take time; do not block on a tight loop, back off between polls.
3. **Download the output.** When ready, the API returns a download location. Fetch the file from there.

DSP reporting exposes campaign-level performance, audience and other breakdowns, and conversion data including new-to-brand metrics. It does not give user-level rows or full per-user attribution paths; that kind of analysis lives in AMC. For which report type, metrics, and dimensions to request and how to read them, hand off to `amazon-dsp-measurement-and-reporting`.

### 6. Work with audiences (audiences API and AMC)

Two layers matter for DSP audiences:

- **Audiences API.** Discover available audiences and work with DSP audience resources so a script can attach, swap, or retire audiences on ad groups as performance dictates. Discovery lets you find segments programmatically rather than by hand.
- **Amazon Marketing Cloud (AMC) API.** AMC is a privacy-safe clean room. You query pseudonymized signals (Amazon Ads signals plus your own inputs) with SQL-style workflows, build custom audiences from the results, and activate them for DSP. The AMC API now uses the same Login with Amazon authorization and endpoint conventions as the rest of the Amazon Ads API and supports reporting, audiences, and signal management. AMC requires an AMC instance to exist for the advertiser; without one, the AMC paths do not apply.

For audience strategy and which segments to use, see the `amazon-dsp-audiences` skill. This skill covers the API mechanics, not the targeting decisions.

## Safe-to-automate matrix

The single most important decision is not how to call the API but what to let the automation do unattended. Default to read and alert. Gate every write. Never automate destruction.

| Action | Verdict | Required control |
| --- | --- | --- |
| Read and monitor (pull entities, pull reports, watch pacing, spend, and delivery) | Safe | Log what you read. No write. |
| Run AMC queries and pull results for analysis | Safe | Read-only analytics. Log the query and the instance. |
| Bulk create from a validated template | Conditional | Create in a non-serving state where the API allows it, QA the result, then a human activates. Confirm your account has DSP write access first. |
| Guardrailed bid or budget change | Conditional | Hard caps on step size and frequency, full logging, and an approval gate before it applies. A runaway budget script spends real money fast. |
| Pause an underperformer | Conditional | Alert a human first. Do not auto-resume. Pausing is reversible but resuming is a judgment call. |
| Add, swap, or retire audiences or targets | Conditional | Human approval. Targeting changes move spend and reach in ways that are hard to reverse cleanly. |
| Activate an AMC-built audience into DSP | Conditional | Human approval. An activated audience starts shaping delivery and spend. |
| Cross-campaign or cross-advertiser budget reallocation | Conditional | Human approval. Moving budget has strategy implications a script cannot weigh. |
| Delete or archive anything | Never automate | Do it by hand. Deletion and archival are destructive and easy to get catastrophically wrong at scale. |

## Human-in-the-loop patterns

Four patterns cover almost everything.

- **Monitor and alert.** The agent reads on a schedule (entities, reports, pacing) and raises an alert when a threshold trips. It never writes. This is the safe default and where most DSP automation should live.
- **Guardrailed change with an approval gate.** The agent proposes a bounded change (within hard step and frequency limits), logs it, and waits for a human approval before applying. Good for small bid or budget nudges.
- **Bulk with a QA gate.** The agent prepares a bulk create or edit, validates it, and stages it so a human reviews the diff before it serves. Confirm DSP write access exists before relying on this pattern.
- **Staged rollout.** Roll a new change (a new audience, a bid logic change) to a small slice first, watch it against a control, and only widen after it proves out. Never flip an account-wide change in one step.

## Data-freshness caveats

Automation that decides on stale data is worse than no automation.

- Do not auto-optimize on conversion data that is only a few hours old. View-through, new-to-brand, and offline conversions lag, so a fresh "no conversions" reading is usually incomplete, not real. Wait for the data to mature.
- Reporting has latency, and very recent windows settle later. Build alerts and changes around matured windows, not the last hour.
- When in doubt, widen the lookback and require the signal to persist across more than one read before acting.

## Security

- No secrets in code. Read the LWA client secret, refresh token, and access token from environment variables or a path the user supplies at runtime.
- Never commit a client secret, refresh token, or access token. Keep credential files out of the repository. The refresh token is the long-lived credential; protect it like a password.
- Scope every call to the right profile. Resolve the profile deliberately and confirm it is the intended advertiser and marketplace before any write.
- Grant the authorizing user the least Amazon Ads and DSP access role the automation needs. A read-only monitor does not need write access.
- Log every write the automation performs, with the profile and the run, so a change is always traceable.

## What is gated or unavailable publicly

State these plainly to the user rather than inventing a workaround:

- **DSP campaign management write access is allowlisted.** It is for self-service DSP advertisers and the partners they authorize, not for managed-service-only accounts. If the account does not have self-service DSP, there is no API write path to its campaigns.
- **Partner access needs consent.** A partner managing an advertiser's DSP account obtains that advertiser's consent before accessing it; an approved API application is not sufficient on its own.
- **Some surfaces ship in beta or are not publicly documented for every account type.** Feature availability moves. Confirm an operation is available to your account and allowlist before building against it; do not assume undocumented or beta endpoints exist.
- **AMC requires an instance.** AMC API paths only apply where the advertiser has an AMC instance provisioned.
- **Exact endpoint paths and field-level schemas change across versions** and the official reference is a JavaScript-rendered site, so confirm current paths and fields against the live reference before coding rather than hardcoding from memory.

## Reference material

This skill ships no helper scripts. The flows above (OAuth with Login with Amazon, profile selection, asynchronous report pull) are standard request-poll-download and token-refresh patterns; build them against the current reference. If you add a script later, read credentials from the environment, never hardcode them, and have it print usage with no arguments.

## Common pitfalls

- **Assuming sponsored ads access covers DSP.** It does not. DSP is a separate solution with separate access; confirm DSP access on the account explicitly.
- **Promising a write path for a managed-service account.** If the account is managed-service only, you cannot create or edit DSP campaigns through the API. Say so.
- **Acting on the wrong profile.** One authorization can see many profiles across accounts and marketplaces. Resolve and log the profile on every write.
- **Polling a report in a tight loop.** DSP reports are asynchronous and can take time. Back off between status checks.
- **Optimizing on immature conversion data.** Amazon conversions lag. A fresh zero is usually incomplete, not real.
- **Hardcoding endpoint paths from memory.** The reference is versioned and JavaScript-rendered. Confirm current paths and fields against the live docs before coding.

## Sources

- Amazon Ads API overview (what the API covers, including Amazon DSP, sponsored ads, streaming TV, AMC, Amazon Marketing Stream): https://advertising.amazon.com/about-api (as of June 2026)
- Amazon Ads API onboarding overview: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/overview (as of June 2026)
- Apply for Amazon Ads API access: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/apply-for-access (as of June 2026)
- Obtain consent to access an Amazon DSP user's account: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/dsp-obtain-consent (as of June 2026)
- Amazon Ads API authorization overview (Login with Amazon): https://advertising.amazon.com/API/docs/en-us/guides/account-management/authorization/overview (as of June 2026)
- Authorization grants (Amazon Ads API): https://advertising.amazon.com/API/docs/en-us/guides/account-management/authorization/authorization-grants (as of June 2026)
- Generate access and refresh tokens: https://advertising.amazon.com/API/docs/en-us/guides/get-started/retrieve-access-token (as of June 2026)
- Profiles (account and marketplace scope): https://advertising.amazon.com/API/docs/en-us/guides/account-management/authorization/profiles (as of June 2026)
- Amazon DSP API overview: https://advertising.amazon.com/API/docs/en-us/dsp/overview (as of June 2026)
- Amazon DSP campaign management APIs overview: https://advertising.amazon.com/API/docs/en-us/reference/dsp/dsp-campaign-management-overview (as of June 2026)
- Amazon DSP APIs developer guide: https://advertising.amazon.com/API/docs/en-us/guides/dsp/developer-guide (as of June 2026)
- DSP reporting overview: https://advertising.amazon.com/API/docs/en-us/guides/reporting/dsp/overview (as of June 2026)
- Pulling Amazon DSP reports via API (creating reports): https://advertising.amazon.com/API/docs/en-us/guides/reporting/dsp/creating-reports (as of June 2026)
- Reporting API v3 overview: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/overview (as of June 2026)
- Amazon Marketing Cloud (AMC) overview: https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-cloud/overview (as of June 2026)
- Get started with Amazon Marketing Cloud: https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-cloud/get-started/get-started (as of June 2026)
