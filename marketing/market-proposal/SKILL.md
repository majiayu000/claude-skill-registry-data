---
name: market-proposal
description: Client proposal generator for marketing services with anchored pricing, tiered options, and ROI projections.
---

# Client Proposal Generator for Marketing Services

## Skill Purpose

Generate a professional, client-ready marketing services proposal. This skill produces a complete proposal document that positions the agency/consultant as the clear choice, frames pricing with anchoring and tiered options, and includes ROI projections to justify the investment.

## When to Use

- User wants to create a proposal for a prospective marketing client.
- User has completed a discovery call and needs to formalize the engagement.
- User wants a template for their marketing agency's proposals.
- Triggered by `/market proposal` or `/market proposal <client name>`.

## Reference map

| When | Read |
|---|---|
| Running the discovery call (Step 2) | [`references/discovery-questions.md`](references/discovery-questions.md) |
| Writing the 11 proposal sections (Step 3) | [`references/proposal-sections.md`](references/proposal-sections.md) |
| Design & formatting rules (Step 4) | [`references/design-and-formatting.md`](references/design-and-formatting.md) |
| Follow-up email sequence after sending (Step 5) | [`references/follow-up-sequence.md`](references/follow-up-sequence.md) |
| Objection-handling responses (Step 6) | [`references/objection-handling.md`](references/objection-handling.md) |

## Pricing, scope, and risk rules

- **Anchored pricing.** Present **three tiers** (Growth / Accelerate / Dominate) with the highest tier first so the middle tier feels reasonable. Use aspirational labels, not Bronze/Silver/Gold. Mark the middle tier "Most Popular" or "Recommended". Most clients pick the middle.
- **Pricing model fit.** Match engagement model to the client's risk preference and scope clarity:

  | Model | When to use | Typical range |
  |---|---|---|
  | Monthly retainer | Ongoing, relationship-based | $2,000–$25,000/month |
  | Project-based | Defined scope, one-time | $5,000–$100,000 per project |
  | Performance-based | Client wants risk-sharing + you're confident | Base + % revenue/leads |
  | Hybrid | Complex engagements | Base retainer + performance bonus |
  | Hourly | Consulting, advisory, ad-hoc | $150–$500/hour |

- **Conservative ROI projection.** Under-promise, over-deliver. Use **ranges, not specific numbers**. Always add disclaimers that results depend on multiple factors. Past performance ≠ guaranteed future results.
- **Scope discipline.** Every deliverable explicit (counts + word ranges + cadences). Explicit exclusions to prevent scope creep. Client responsibilities listed (feedback SLAs, access, ad budget separate from management fees).
- **No fabricated case studies.** Use only real client results. Anonymize as needed. Don't promise outcomes you can't back with evidence.
- **No fabricated reviews, testimonials, or partner logos.** All social proof must be real, attributable, and used with consent.
- **Validity window.** Every proposal has a 30-day expiration. State the date explicitly on the cover and in Next Steps.

## How to Execute

### Step 1: Gather proposal inputs

Collect from the user (ask if not provided):

**About the client:**
1. Client name and company.
2. Industry and business model.
3. Current marketing situation (what they're doing now).
4. Primary pain points or challenges.
5. Goals (revenue, growth, leads, brand awareness).
6. Budget range (if known).
7. Decision timeline.
8. Key stakeholders and decision-makers.

**About the services:**
1. What services are you proposing? (SEO, paid ads, content, social, email, full-stack)
2. Engagement model (retainer, project, performance-based).
3. Proposed timeline.
4. Your relevant case studies or results.

**If audit data exists:** check for previous `/market audit` results. If found, automatically incorporate findings into the Situation Analysis for a data-backed proposal.

### Step 2: Discovery call question framework

If the discovery call hasn't happened, provide the **10 essential questions** plus bonus questions across four categories:

- **Business understanding** — business model, ideal customer, sales process.
- **Current marketing** — what's working/not, monthly spend + ROI, tools.
- **Goals and expectations** — 6/12-month success picture, specific numbers, customer LTV.
- **Decision and process** — other stakeholders, timeline for choosing a partner.

Full prompts + bonus questions ("biggest frustration", "previous agency experience", "what would make you say no"): [`references/discovery-questions.md`](references/discovery-questions.md).

### Step 3: Build the proposal document

Eleven sections, in order. Full per-section templates, writing guidance, pricing tier table, and ROI calculation framework in [`references/proposal-sections.md`](references/proposal-sections.md).

| # | Section | Length | Job |
|---|---------|--------|-----|
| 1 | **Cover page** | 1 page | Title, prepared-for/by, date, valid-until (date + 30 days), CONFIDENTIAL stamp. |
| 2 | **Executive summary** | 1 page max | Acknowledge situation + state problem + preview approach + hint at outcome + create urgency. |
| 3 | **Situation analysis** | 2–3 pages | Current state, opportunities, competitive landscape, key challenges, market context. **Frame as opportunities, not failures** (use `/market audit` data if available). |
| 4 | **Strategy & approach** | 2–3 pages | Framework + Phase 1 Foundation (months 1–2) + Phase 2 Growth (months 3–4) + Phase 3 Scale (months 5–6) + Ongoing Optimize. Specific enough to show expertise; not so detailed they execute without you. |
| 5 | **Scope of work** | 1–2 pages | Explicit deliverables with quantities, meeting cadence, response-time SLAs, tools, reporting; **explicit exclusions** to prevent scope creep; **client responsibilities** (feedback SLA, access, designated POC, ad budget separate). |
| 6 | **Timeline** | 1 page | 6-month visual timeline with phase labels + key milestones (week-2 audit done, week-4 first campaigns live, month-2 first report, etc.). |
| 7 | **Investment** | 1–2 pages | **Three-tier table** (Growth / Accelerate / Dominate) with anchored pricing; pricing-psychology tips applied; pricing-models reference for engagement-model fit. |
| 8 | **ROI projection** | — | Current state → projected state (6 months) → projected ROI. **Use ranges, be conservative, add disclaimers.** |
| 9 | **Team** | 0.5–1 page | Per team member: name + title + relevant experience + role on engagement + 2–3-sentence bio. |
| 10 | **Case studies** | 1–2 pages | 2–3 relevant. Format: Client (anonymized as needed) / Challenge / Solution / Results (3 specific metrics). **Real results only.** |
| 11 | **Next steps** | 0.5 page | Sign → kickoff call within 48h → onboarding questionnaire → Foundation phase begins. Reduce friction. State validity window. |

### Step 4: Proposal design and formatting

Keep total under 15 pages excluding appendix. Consistent headers/fonts/colors. Client logo on cover. Charts/visuals over dense text. Bold key numbers and outcomes. Whitespace generous. Page numbers + TOC. Save as PDF for delivery. Full Markdown rendering rules and design checklist: [`references/design-and-formatting.md`](references/design-and-formatting.md).

### Step 5: Follow-up sequence after sending

Seven touchpoints over 21 days: Day 0 (send), Day 2 (confirm receipt), Day 5 (value-add), Day 7 (direct ask), Day 14 (final check-in), Day 21 (breakup). Full subject lines + body templates: [`references/follow-up-sequence.md`](references/follow-up-sequence.md).

### Step 6: Objection handling

Prepare responses for **8 common pushbacks**: "too expensive", "we can do this in-house", "we tried this before", "need to think about it", "can you guarantee results", "we're talking to other agencies", "timeline is too long", "we don't have the budget". Full response frameworks: [`references/objection-handling.md`](references/objection-handling.md).

### Step 7: Terms and conditions essentials

Include in the proposal appendix or as a separate document:

1. **Payment terms** — Net 15 or Net 30, payment methods, late-payment penalties.
2. **Contract duration** — minimum commitment period, auto-renewal terms.
3. **Cancellation policy** — required notice period (typically 30 days), exit process.
4. **Scope changes** — process for handling changes and additional costs.
5. **Intellectual property** — who owns the work product, license terms.
6. **Confidentiality** — NDA terms, how client data is handled.
7. **Liability limitations** — caps on liability, force majeure.
8. **Reporting and communication** — agreed cadence and format.
9. **Third-party costs** — client responsibility for ad spend, software, stock images.
10. **Results disclaimer** — marketing results are not guaranteed, past performance context.

## Cross-skill integration

- **`/market audit`** — if `MARKETING-AUDIT.md` exists, incorporate findings into Section 3 (Situation Analysis).
- **`/market competitors`** — if `COMPETITOR-REPORT.md` exists, use it for the competitive-landscape paragraph in Section 3.
- **`/market funnel`** — if `FUNNEL-ANALYSIS.md` exists, reference funnel metrics in Section 4 (Strategy) and Section 8 (ROI projection baseline).
- **`/market brand`** — if `BRAND-VOICE.md` exists, write the proposal in the client's voice (or in your own brand voice if their voice doesn't match the moment).

Data-backed proposals close at 2–3× the rate of generic proposals — use prior skill outputs aggressively.

## Output Format

Generate a file called `CLIENT-PROPOSAL.md` with:

```markdown
# Marketing Services Proposal

## Prepared for: [Client Name]
## Prepared by: [Agency Name]
## Date: [Date]

---

## Table of Contents
1. Executive Summary
2. Situation Analysis
3. Strategy & Approach
4. Scope of Work
5. Timeline
6. Investment
7. ROI Projection
8. Our Team
9. Case Studies
10. Next Steps

---

[Full proposal content with all sections populated based on client details]

---

## Appendix
- Terms & Conditions
- Detailed Deliverable Descriptions
- Tool Stack
```

## Key Principles

- The proposal is a **sales document**, not a statement of work. It should SELL, not just describe.
- Lead with the client's problems and goals, not your services. Make them feel understood before presenting solutions.
- Every price should be **anchored to the ROI** it will generate. Never present cost without context.
- Use the client's own language from the discovery call. Mirror their words back to them.
- If audit data is available from previous skills, use it extensively — data-backed proposals close at 2–3× the rate of generic proposals.
- Keep it concise. Executives skim. Use bold, headers, and tables to make key information scannable.
- Always include a specific, **time-bound next step**. Ambiguity kills deals.
