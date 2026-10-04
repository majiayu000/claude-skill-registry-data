---
name: new-client-onboarding
description: >
  Post-deal new client onboarding workflow. Creates client profile,
  runs baseline technical audit, generates project plan, sets up
  communication templates, and updates CRM.
tags: [onboarding, client, post-sale, playbook]
---

# New Client Onboarding

Post-deal setup workflow for new clients. Takes a signed deal and produces everything needed to kick off the engagement: client profile, baseline audit, project timeline, communication templates, and CRM updates. Run this immediately after a deal closes to maintain momentum and professionalism.

## Prerequisites

- `agency.config.json` fully populated with services and team info
- CRM initialized with the lead record for this client
- Deal closed and contract signed

## Composites & Capabilities Used

1. `company-researcher` -- gather company details if not already in CRM
2. `cro-auditor` -- baseline technical and CRO audit
3. `crm-writer` -- update lead stage, record contract details

## Phase 0: Intake

Read `agency.config.json` for agency info and services catalog.

Accept the following inputs:
- **Client name**: the company name
- **Website**: their primary website URL
- **Contact person**: primary point of contact (name, email, title)
- **Services purchased**: which services from the agency catalog were sold
- **Start date**: engagement start date
- **Contract value**: monthly retainer or project fee
- **Contract duration**: number of months or project timeline

Validate that the client exists in CRM. If not, create a new lead record first.

## Phase 1: Client Profile

Create a client profile document containing:

```
CLIENT PROFILE: [Client Name]
===
Created: [Date]
Account Owner: [From agency.config.json]

COMPANY DETAILS:
- Name: [Client Name]
- Website: [URL]
- Industry: [from company-researcher or intake]
- Platform: [Shopify plan, theme, apps]
- Team size: [if known]
- Social: [Instagram, LinkedIn URLs]

KEY STAKEHOLDERS:
- [Name] -- [Title] -- [Email] -- [Role in engagement]
  Decision maker / Day-to-day contact / Technical contact / Billing contact

ENGAGEMENT DETAILS:
- Services: [list of services purchased]
- Monthly retainer: [amount]
- Contract duration: [months]
- Start date: [date]
- End date: [date]
- Payment terms: [from contract]

COMMUNICATION PREFERENCES:
- Primary channel: [Slack / Email / WhatsApp]
- Meeting cadence: [Weekly / Bi-weekly]
- Preferred meeting day/time: [TBD -- confirm at kickoff]
- Reporting format: [Email summary / Shared doc / Dashboard]

ACCESS NEEDED:
[ ] Shopify admin (collaborator account)
[ ] Google Analytics
[ ] Google Search Console
[ ] Ad accounts (Meta, Google Ads)
[ ] Email marketing platform
[ ] Social media accounts
[ ] Brand assets (logos, fonts, guidelines)
```

## Phase 2: Technical Audit

Run a full technical and CRO audit on the client's current state to establish baselines.

Execute `cro-auditor` with depth: "deep":
- Full audit across homepage, product pages, collection pages, mobile, cart, checkout
- Document current Core Web Vitals scores
- Capture current conversion rate benchmarks (if analytics access is available)
- Screenshot key pages for before/after comparison later

Compile baseline metrics:

```
BASELINE METRICS: [Client Name]
===
Captured: [Date]

SITE PERFORMANCE:
- PageSpeed (Mobile): N/100
- PageSpeed (Desktop): N/100
- LCP: Ns
- FID: Nms
- CLS: N

CRO SCORES:
- Homepage: N/10
- Product pages: N/10
- Collection pages: N/10
- Mobile experience: N/10
- Cart/Checkout: N/10
- Overall: N/10

QUICK WINS IDENTIFIED:
1. [Issue] -- Impact: [High/Med/Low] -- Effort: [Low]
2. [Issue] -- Impact: [High/Med/Low] -- Effort: [Low]
3. [Issue] -- Impact: [High/Med/Low] -- Effort: [Low]
```

Quick wins are defined as: high or medium impact, low effort, deliverable within the first 2 weeks.

## Phase 3: Project Setup

Generate a phased project plan based on the services purchased:

```
PROJECT PLAN: [Client Name]
===

WEEK 1-2: QUICK WINS & SETUP
---
[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [access needed]
    Definition of done: [specific criteria]

[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [none]
    Definition of done: [specific criteria]

[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [brand assets]
    Definition of done: [specific criteria]

WEEK 3-4: CORE DELIVERABLES
---
[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [quick wins complete]
    Definition of done: [specific criteria]

[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [none]
    Definition of done: [specific criteria]

WEEK 5-8: OPTIMIZATION & MEASUREMENT
---
[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [core deliverables complete]
    Definition of done: [specific criteria]

[ ] [Task] -- Owner: [name] -- Due: [date]
    Dependencies: [analytics data accumulated]
    Definition of done: [specific criteria]

MONTHLY ONGOING:
---
[ ] Performance review and reporting
[ ] Conversion rate monitoring
[ ] A/B test planning and execution
[ ] Content and catalog updates
[ ] Monthly strategy call with client
```

Tailor tasks to the specific services purchased. If CRO only, focus on audit fixes and testing. If full management, include catalog, marketing, and analytics tasks.

## Phase 4: Communication Setup

Generate the following templates:

**Kickoff Meeting Agenda:**
```
KICKOFF MEETING AGENDA -- [Client Name]
Date: [Date]
Duration: 60 minutes
Attendees: [List]

1. Introductions (5 min)
2. Engagement overview: scope, timeline, deliverables (10 min)
3. Access and setup: confirm all logins and permissions (10 min)
4. Current state review: share baseline audit findings (15 min)
5. Quick wins: present and prioritize (10 min)
6. Communication cadence: agree on meeting times and channels (5 min)
7. Next steps and action items (5 min)
```

**Weekly Status Report Template:**
```
WEEKLY STATUS -- [Client Name] -- Week of [Date]
===

COMPLETED THIS WEEK:
- [Task]: [outcome/result]

IN PROGRESS:
- [Task]: [status, % complete, blockers]

PLANNED NEXT WEEK:
- [Task]: [owner, expected completion]

METRICS UPDATE:
- [Key metric]: [current value] (vs baseline: [value])

BLOCKERS / NEEDS FROM CLIENT:
- [Item]: [what's needed, by when]
```

**Monthly Review Template:**
```
MONTHLY REVIEW -- [Client Name] -- [Month Year]
===

EXECUTIVE SUMMARY:
[2-3 sentences on progress and impact]

KEY METRICS:
| Metric | Baseline | Last Month | This Month | Delta |
|--------|----------|------------|------------|-------|
| [metric] | [val] | [val] | [val] | [+/-] |

COMPLETED THIS MONTH:
- [Deliverable]: [impact]

NEXT MONTH PRIORITIES:
1. [Priority]
2. [Priority]
3. [Priority]

RECOMMENDATIONS:
- [Recommendation based on data]
```

**Escalation Process:**
```
ESCALATION PROCESS:
---
Level 1 (Day-to-day): Contact [name] via [channel]
- Response time: within 4 business hours

Level 2 (Urgent): Contact [name] via [channel]
- Response time: within 2 business hours

Level 3 (Critical/Outage): Contact [name] via phone
- Response time: within 30 minutes
```

## Phase 5: CRM Update

Write to CRM using `crm-writer`:
- Update lead stage from DEMO_BOOKED or NEGOTIATION to WON
- Record contract value, start date, end date, services
- Add client profile link to CRM notes
- Create any recurring tasks or reminders for the engagement

## Phase 6: Checklist Output

Final output, a comprehensive onboarding checklist:

```
NEW CLIENT ONBOARDING -- [Client Name]
===

PRE-KICKOFF:
[ ] Client profile created
[ ] Access requested (Shopify admin, Analytics, Ad accounts)
[ ] Technical audit completed
[ ] Baseline metrics documented
[ ] Project timeline drafted
[ ] Kickoff meeting scheduled
[ ] CRM updated to WON

WEEK 1:
[ ] Kickoff meeting conducted
[ ] Quick wins identified and prioritized
[ ] Communication cadence agreed
[ ] All access confirmed and working
[ ] First deliverable in progress

WEEK 2:
[ ] Quick wins delivered
[ ] First progress report sent
[ ] Core project work started
[ ] Client feedback on quick wins collected

ONGOING:
[ ] Weekly status calls
[ ] Weekly status reports sent
[ ] Monthly reviews conducted
[ ] Quarterly business review scheduled
[ ] Metrics tracked against baseline
```

## Example Usage

**Trigger phrases:**
- "Onboard [client name]"
- "New client setup for [company]"
- "Run onboarding for the new deal"
- "Set up [client] after contract signing"
