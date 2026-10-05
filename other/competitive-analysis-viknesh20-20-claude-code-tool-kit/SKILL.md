---
name: competitive-analysis
description: "Research how 2–4 mature competitors solve a specific business problem (billing, RBAC, search, onboarding, multi-tenancy, etc.) and produce a side-by-side comparison so the team can pick the right approach for their context. Uses web search + scraping; cites every source."
argument-hint: "<feature or problem to research>"
---

# /competitive-analysis

Before designing a feature in a well-trodden domain, look at how 2–4 mature companies handle it. Faster than inventing. More robust than guessing. Cite every source — never copy product copy or terms-of-service language.

## When to use

- Designing billing, dunning, refunds, plan changes, trials, onboarding.
- Designing RBAC, workspace management, team invitations.
- Designing notifications, digests, preferences.
- Designing API rate limits, pagination, idempotency, error formats.
- Designing search, filters, saved views.
- Designing data export, deletion, retention.
- Stuck on UX for a non-obvious flow (account merging, plan downgrade, account recovery).

## When NOT to use

- The user's domain is unique enough that competitor patterns won't transfer (specialized B2B verticals, regulated industries with custom workflows).
- The user has already decided. Don't second-guess; just ship.
- Style and copy decisions — those are taste, not pattern.

## Operating method

### 1. Confirm the question

Ask the user, in one round:

- **What's the specific problem?** Not "how does Stripe work" but "how should we handle a failed-payment retry schedule and the user-facing dunning emails?"
- **What's our context?** B2C / B2B / SMB / enterprise / specific vertical. Self-serve vs sales-led. Plan structure.
- **What constraints are non-negotiable?** Compliance, no-third-party-data, must-self-host, etc.
- **Which competitors should I look at?** If unsure, suggest 3–4 mature ones in the relevant space.

Don't research without these answers. Researching the wrong question wastes a few minutes; *acting* on the wrong research costs a quarter.

### 2. Pick competitors deliberately

Mature comparison sets by domain (suggest these as defaults; adjust per user):

| Domain | Suggested competitors |
|---|---|
| **SaaS billing & dunning** | Stripe, Recurly, Chargebee, Paddle |
| **B2B SaaS workspace + RBAC** | Linear, Notion, Slack, Asana |
| **CRM** | Salesforce, HubSpot, Pipedrive, Close |
| **E-commerce checkout** | Shopify, Stripe Checkout, BigCommerce, WooCommerce |
| **Marketplace fees + payouts** | Stripe Connect, Airbnb, Etsy, Uber |
| **Customer support** | Intercom, Zendesk, HelpScout, Front |
| **Project management** | Linear, Jira, Asana, Monday |
| **ERP financials** | NetSuite, SAP, Odoo, Microsoft Dynamics |
| **Inventory** | Shopify, NetSuite, Cin7, Brightpearl |
| **Auth / SSO** | Auth0, Clerk, WorkOS, Okta |
| **Notifications / engagement** | Customer.io, Braze, Iterable, Knock |
| **Webhooks / events** | Stripe, GitHub, Segment |
| **Analytics** | Mixpanel, Amplitude, PostHog, Segment |
| **Search** | Algolia, Elasticsearch, Typesense, Meilisearch |
| **Status / incidents** | StatusPage, Statuspal, Better Uptime |

### 3. Research each competitor

For each:
1. **Read their public docs** for the specific feature. Use `firecrawl-scrape` MCP if available. Quote with attribution.
2. **Find dev-blog posts, conference talks, engineering decisions.** These reveal *why* not just *what*.
3. **Read 1–2 critical reviews** (G2, ProductHunt, Reddit, HN) to find the friction points.
4. **Note the version / date.** Patterns evolve; a 2019 blog post may not reflect 2026 behavior.

### 4. Extract the dimensions that matter

Don't write narrative comparisons. Build a table where each row is a *decision point* and each column is a competitor.

For billing failure-recovery:

| Dimension | Stripe Smart Retries | Recurly | Chargebee | Paddle |
|---|---|---|---|---|
| Retry count | 4 (default) | configurable 1–5 | configurable 1–10 | 3 |
| Retry window | 15 days | 21 days | configurable | 14 days |
| Retry timing | ML-optimized | fixed cadence | fixed/custom | fixed |
| Email cadence | day 1, 3, 7 | day 1, 5, 10, 15 | per template | day 1, 7 |
| Grace period | bills marked past_due | suspend after final retry | configurable | suspend |
| Customer self-rescue | `customer_portal` | hosted page | hosted page | hosted page |
| Card update prompt | yes, in-product | yes, hosted | yes | yes |
| 3DS / SCA handling | re-auth at retry | re-auth at retry | re-auth at retry | re-auth |

### 5. Recommend with reasoning

End the analysis with: which patterns to adopt, which to skip, and why for *this specific project*. Cite the dimensions that drove the call.

```
## Recommendation for <project>

Adopt:
- Stripe's smart-retry timing (proven at scale, easy via Stripe Billing).
- Recurly-style dunning email cadence (more touchpoints than Stripe; better for our SMB churn profile).

Skip:
- Customer portal self-rescue (we'll wait for v2 — not enough users to justify yet).

Open question for the user:
- Grace period: do we want past_due → readonly access (Stripe default) or past_due → fully-featured for 7 days then suspend? Affects our retention math.
```

### 6. Save the research

Write the result to `.claude/memory/reference/competitive-analysis-<topic>-<date>.md` so future sessions don't re-research the same thing. Add to `MEMORY.md`.

## Output format

```
## Question
<the user's actual question, refined>

## Context
- Business type:
- Constraints:
- Competitors compared:

## Comparison

[Table — one row per dimension, one column per competitor]

## Patterns worth borrowing
- <pattern A> — used by: <competitors>. Why: <reason>.
- <pattern B> — used by: <competitors>. Why: <reason>.

## Patterns to skip
- <pattern> — used by: <competitor>. Why we don't: <reason>.

## Recommended approach
[2–4 paragraphs. What you'd build, citing competitor patterns by name where you adopted them.]

## Open questions for the user
1. …
2. …

## Sources
- [Stripe docs — Smart Retries](https://...)
- [Recurly engineering blog — Dunning](https://...)
- [HN discussion: SaaS dunning best practices](https://...)
```

## Boundaries

- **Cite every source.** No "I read somewhere that …"
- **Never copy product copy, terms-of-service text, or trademarked material.** Learn from the *approach*, write your own copy.
- **Note the date** of every source. Stripe-2019 ≠ Stripe-2026.
- **Don't recommend the most popular pattern** — recommend the pattern that fits the project's constraints.
- **Don't research private information.** Public docs, blog posts, talks, public reviews only.
- **Ask first** if the user already has strong preferences; this skill is for when they want input, not when they've decided.
