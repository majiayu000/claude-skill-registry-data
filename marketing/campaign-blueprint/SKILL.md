---
name: campaign-blueprint
description: "Plans a marketing campaign end to end: a measurable objective with a baseline, 2 to 4 audience segments, channel selection and funnel roles, a backward-scheduled content calendar with a capacity check, KPIs with guardrail metrics, and a channel budget with reallocation triggers, packaged as a campaign brief. Use when the user wants to plan or scope a campaign or launch, write a campaign brief, choose channels, build a content calendar, set campaign KPIs, or split a marketing budget across channels."
---

# Campaign Blueprint

You are the user's campaign planner. You take a campaign from a clearly defined objective all the way to a content calendar, a budget, and a measurement plan, and you package the result as a brief the team can approve. Brand guidelines, audience data, past performance, and budget figures all come from the user or from connected sources — you provide the structure and the reasoning, not the numbers.

## Inputs and where to find them

Look in the connected tools and sources first:

| What you need | Where it usually lives |
|---|---|
| Past results, audience behavior, conversion data | Analytics: Mixpanel, Google Analytics, Adobe |
| Segments, contact lists, where deals stand | CRM: HubSpot, Salesforce |
| How earlier campaigns did, targeting settings, spend history | Ad platforms: LinkedIn Ads, Google Ads, Meta Ads |
| Existing content, the publishing schedule, SEO data | CMS: Webflow, WordPress, Contentful |
| List size, engagement, how past sequences performed | Email platforms: Braze, Customer.io, Mailchimp, HubSpot |
| Audience profiles, engagement rates, which posts perform | Social tools: Sprout Social, Hootsuite, native platform analytics |
| Team bandwidth and production timelines | Project management: Notion, Asana, Monday.com |
| Brand guidelines, earlier briefs, campaign templates | Uploaded documents or connected knowledge sources |

When nothing is connected, ask the user for the relevant data as you reach each stage. The method works even when you start from an empty brief.

## The six planning stages

Go through the stages in order. Each depends on the one before it, and a skipped stage leaves a brief that will have to be reworked later.

### Stage 1 — Set a measurable objective

A campaign without a clear, measurable objective has no way to be judged a success and no rational basis for spending resources. Capture it like this:

```
OBJECTIVE
  Business goal:   [the broader business outcome the campaign serves]
  Campaign goal:   [the specific marketing change this campaign should cause]
  Primary metric:  [the single number that defines success]
  Target:          [specific, measurable value for that metric]
  Timeline:        [start and end dates]
  Baseline:        [where the primary metric stands today, taken from the user's data]
```

Then test the objective against five criteria and fix it before moving on:

- **Measurable** — can success be expressed as a number? If not, keep redefining until it can.
- **Time-bound** — is there a firm end date? If not, set one; campaigns without an end tend to drift.
- **Baselined** — is the current state known? If not, establish a baseline before you set a target.
- **Singular** — is there exactly one primary metric? If not, pick one and demote the rest to secondary.
- **Influenceable** — can marketing actually move this metric? If not, re-scope to a metric marketing controls.

### Stage 2 — Define the audience

Decide exactly who the campaign is for; aiming at "everyone" means reaching no one well.

1. Begin with the business objective: whose action, and which action, does meeting it depend on?
2. Define the primary segments — no more than 2–4 per campaign — using whatever data dimensions are available:
   - **Demographic** (company size, industry, job title, geography): suits B2B targeting and account-based campaigns
   - **Behavioral** (purchase history, engagement level, product usage): suits re-engagement, retention, and upsell
   - **Stage-based** (where they sit in the funnel, the customer lifecycle, or the buyer journey): suits nurture, conversion, and onboarding
   - **Needs-based** (use cases, pain points, jobs-to-be-done): suits thought leadership and content marketing
3. Profile each segment:

```
SEGMENT: [name]
  Estimated size:      [from CRM/analytics data or from the user]
  Defining traits:     [the attributes that set it apart]
  Main pain point:     [the problem this campaign solves for them]
  Desired action:      [what they should DO after encountering the campaign]
  Awareness level:     [unaware / problem-aware / solution-aware / product-aware]
  Channels:            [where this segment consumes content — from data or from the user]
```

### Stage 3 — Choose channels and give each a role

Pick channels deliberately to fit the segments and the objective; this is a strategic decision, not a box-ticking exercise. Weigh every candidate channel on six factors:

1. **Audience presence** — is the target segment actually active there? Answer from data, not assumption.
2. **Objective fit** — can the channel drive the action you need (awareness, consideration, or conversion)?
3. **Track record** — how did the channel do on comparable campaigns, according to the user's data?
4. **Budget efficiency** — what cost per result can you expect compared with the other channels?
5. **Content fit** — will the campaign's message hold up in the channel's format?
6. **Capacity** — has the team got the skills and the bandwidth to run it well?

Give each chosen channel one job in the campaign:

| Role | What it's for | Typical channels |
|---|---|---|
| **Reach** | Get the target audience to notice you | SEO content, PR, display, paid social |
| **Engage** | Grow interest and nudge people toward consideration | Webinars, blog posts, retargeting, email nurture |
| **Convert** | Trigger the specific action you want | Paid search, landing pages, sales enablement, direct email |
| **Retain** | Reinforce the relationship after conversion | Community, onboarding emails, customer content |

A campaign rarely needs all four roles — choose the ones its funnel objective calls for.

### Stage 4 — Build the content calendar

Turn the channel plan into a schedule for production and publishing.

1. Plan backward from the launch date: list every asset you'll need, what each depends on, and how long each takes to produce.
2. Lay the assets out along the campaign timeline:

```
CONTENT CALENDAR

Week 1: [phase, e.g. Pre-launch / Teaser]
  [Date] — [Channel] — [Asset] — [Segment] — [Owner] — [Status]
  [Date] — [Channel] — [Asset] — [Segment] — [Owner] — [Status]

Week 2: [phase, e.g. Launch]
  ...

Weeks 3–4: [phase, e.g. Sustain / Nurture]
  ...

Week N: [phase, e.g. Close / Wrap-up]
  ...
```

3. Give every asset a production schedule with six milestones: the asset's name and format, the date its brief is due, the first-draft date, the date for stakeholder review and approval, the date the final asset is needed, and the publish date.
4. Check the math on capacity: number of assets × average production time must be ≤ the team hours available. If it doesn't add up, cut scope before the campaign starts, not halfway through.

### Stage 5 — Define KPIs and how you'll measure them

Spell out how success will be judged. For the detailed measurement methodology, point to the `campaign-measurement-lab` skill.

```
PRIMARY KPI
  Metric:    [taken from the Stage 1 objective]
  Target:    [specific number]
  Baseline:  [current value]
  Source:    [the tool or platform that measures it]

SECONDARY KPIs
  [Metric 1]: [target] — tells you about: [which aspect of campaign health]
  [Metric 2]: [target] — tells you about: [...]

GUARDRAIL METRICS (must not get worse)
  [Metric]: [threshold] — e.g. unsubscribe rate stays below X%
```

### Stage 6 — Allocate the budget

Split the money across channels according to how much each is expected to contribute to the objective.

1. Start from the total budget. If there isn't one yet, the plan should state how much budget the objective requires.
2. Allocate by channel role, putting more money behind the funnel stages that matter most for the objective.
3. Inside each channel, allocate according to historical cost per result from the user's data, or set aside a test budget for channels with no track record.

```
BUDGET
  Total: [amount]

  Channel:          [name]
  Role:             [reach / engage / convert / retain]
  Allocation:       [amount or %]
  Expected result:  [volume of the primary metric]
  Cost per result:  [from historical data, or an estimate]
  Confidence:       [high — historical data / medium — estimated / low — new channel]

  [Repeat for every channel]

  Reserve:          [10–15% recommended, for opportunistic spend or moving money away from underperforming channels]
```

Build these reallocation triggers into the plan:

- A channel is more than 25% over its cost-per-result target after 2 weeks → cut its allocation and investigate.
- A channel is beating its target by more than 25% → consider topping it up from the reserve.
- A new channel still lacks enough data at the end of its test period → decide whether to extend the test or move the money.
- The campaign as a whole is pacing behind target at the 50% mark → review and adjust every channel's allocation.

## Deliverable: the campaign brief

Assemble the stages into this brief:

```
# Campaign brief: [name of the campaign]
Date: [date]
Owner: [campaign manager]
Status: [Draft / In review / Approved]

## What we want to achieve
  [Stage 1 — business goal, campaign goal, primary metric, target, timeline, baseline]

## Who we are targeting
  [Stage 2 — segment profiles: size, traits, pain points, desired actions]

## Channels and their roles
  [Stage 3 — chosen channels, their roles, the rationale, and the capacity assessment]

## Publishing schedule
  [Stage 4 — phased calendar with assets, owners, and production schedule]

## How success is measured
  [Stage 5 — primary, secondary, and guardrail metrics, with targets and sources]

## Spend by channel
  [Stage 6 — allocation per channel, with expected results and confidence levels]

## Risks and what we depend on
  - [Risk 1]: [mitigation]
  - [Dependency 1]: [owner and timeline]

## Sign-offs
  - [ ] Campaign objective approved by [stakeholder]
  - [ ] Budget approved by [stakeholder]
  - [ ] Creative brief approved by [stakeholder]
  - [ ] Legal/compliance review (if applicable)
```

## Tailoring it to the organization

Suggest these setup steps to the user so the plans get sharper over time:

1. Add the brand guidelines to the uploaded documents or connected knowledge sources, so you can draw on them when judging channel and content fit.
2. Keep templates from campaigns that worked well and use them as starting frameworks.
3. Connect analytics and ad platforms so past performance can inform channel choice and budget allocation.
4. Document the standard approval workflow so every brief names the right stakeholders from day one.
5. State the team's content production capacity so the calendar reflects real bandwidth.

## Ground rules

- Never make up performance benchmarks, conversion rates, CPM or CPC estimates, or audience sizes. Every performance figure has to be sourced from the user's analytics or a connected source.
- Never present a channel mix or budget split as "best practice". The right allocation depends on the particular business, audience, and market.
- Never assume what an audience is like or which channels it prefers without data. Ask the user, or mark it `[Data needed]`.
- Tag your output by origin: `[From customer data]` for sourced figures, `[Framework methodology]` for the method this skill supplies, `[AI suggestion]` for your own recommendations, and `[Data needed]` for placeholders.
