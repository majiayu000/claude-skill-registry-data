---
name: joint-success-plan
description: "Drafts a joint customer success plan with the customer: discovers their business goals, turns each goal into measurable KPIs with baselines and targets, maps milestones with dependencies and a critical path, assigns one accountable owner per milestone on each side, and sets a review cadence with update triggers. Use when a customer success manager wants to write or refresh a success plan, agree KPIs and milestones with a customer, prepare a post-onboarding, enterprise, renewal-recovery, expansion or tech-touch plan, or needs discovery questions to uncover customer goals."
---

# Joint Success Plan

You help a customer success manager build a success plan together with the customer: business goals the customer owns, KPIs both sides accept, milestones with named owners, and a rhythm for reviewing progress. Treat it as a shared commitment, not a vendor deliverable. Customer-specific facts come from the user, from connected tools and sources, or from uploaded documents.

## Where the account facts come from

- **CRM** (HubSpot, Salesforce): the account record, what the contract covers, stakeholder contacts, past expansions

If no CRM is connected, the user can supply the same details by hand and the method is unchanged.

## How to build the plan

Do every step with the customer, not for them. A plan the vendor writes alone and hands over is a vendor document; it only becomes a partnership artifact when the customer has shaped it.

### Step 1 — Uncover what the business is trying to achieve

Start from the customer's business outcomes. Ask what their business needs to accomplish, and leave aside for now what they would like your product to do. Cover these areas in discovery:

- **Strategic priorities** — learn the organization's top-level objectives. *"Which three priorities matter most to your team or department this year?"*
- **Success definition** — find out how success is judged internally. *"How will your leadership decide whether this initiative worked?"*
- **Current challenges** — surface the pain points your product could relieve. *"What stands most in the way of reaching [priority]?"*
- **Stakeholder expectations** — capture what each group needs from the partnership. *"What would a good outcome look like for [the executive sponsor / end users / IT]?"*
- **Timeline pressures** — expose outside deadlines and dependencies. *"Is a fixed date or business event setting the pace here?"*
- **Previous experience** — draw lessons from earlier vendor relationships. *"In past partnerships, what went well and what didn't?"*

Hold firm on one rule: the goals belong to the customer and must not be lifted from your feature list. "Get more users onto our AI assistant" is a vendor goal. "Cut average first-response time on support tickets by 40%" is a customer goal.

### Step 2 — Turn each goal into KPIs

For every business goal, agree measurable KPIs that both parties accept as proof of success. Each KPI has seven parts:

| Part | What it captures | Worked example |
|---|---|---|
| **Metric name** | The thing being measured | First-response time on support tickets |
| **Baseline** | Where it stands today — measured, never assumed | 9.5 hours on average |
| **Target** | The value both sides have agreed to reach | 5.7 hours on average |
| **Measurement method** | How it will be tracked | Report from the customer's helpdesk system, pulled monthly |
| **Data owner** | Who supplies the numbers | The customer's support operations team |
| **Review frequency** | How often it is looked at | Monthly at the CSM check-in; quarterly at the QBR |
| **Timeline** | When the target should be hit | Within 6 months of full deployment |

Test every KPI against four questions before it goes in:

- **Can we influence it?** It must sit within what the customer and your team can jointly affect — skip metrics that neither side controls.
- **Can we measure it?** The available tools must be able to track it reliably — skip anything you cannot track.
- **Does their leadership care?** The customer's leaders must see it as meaningful — skip metrics only the CSM values.
- **Is the target set right?** Aim high but reachable. Unrealistic targets sap motivation; soft targets prove nothing about value.

### Step 3 — Map the milestones

Split each goal into milestones that have clear dependencies and owners. Capture for each one:

- **Milestone name** — a descriptive label for what will be achieved
- **Description** — what "done" means for this milestone
- **Dependencies** — what has to be in place before work on it can begin
- **Owner** — the responsible person on each side (your team and the customer's)
- **Target date** — when it should be finished
- **Success indicator** — how you will know it has actually been achieved, not merely ticked off; make it measurable wherever you can
- **Risk factors** — known risks that could push it back

Arrange the milestones under their goals, order them by dependency, and mark the critical path: the milestones whose slippage would knock on to other milestones or to the overall timeline.

### Step 4 — Assign owners

Each piece of the plan has to have a named owner on the customer's side and on yours. The standard roles:

| Role | What they are responsible for |
|---|---|
| **Executive sponsors** (one per side) | Keeping strategy aligned, clearing escalations, taking part in quarterly reviews |
| **CSM** | Owning the plan, tracking progress, coordinating milestones, reporting |
| **Customer project lead** | Coordinating inside the customer, allocating resources, delivering the customer's milestones |
| **Subject matter experts** (both sides) | Configuration, integration work, training, and the technical delivery itself |

Remember that when everyone owns something, no one does. Give each milestone exactly one primary owner — the single person accountable for getting it done — however many people contribute.

### Step 5 — Agree how the plan will be reviewed

Settle when and how the plan gets reviewed and updated:

| Review | How often | Who takes part | What it looks at |
|---|---|---|---|
| **Progress check** | Every two weeks or monthly | CSM and customer project lead | Where milestones stand, blockers, adjustments |
| **Quarterly review** | Once a quarter, lined up with the QBR | CSM, customer project lead, executive sponsors | Progress toward goals, KPI assessment, how the plan should evolve |
| **Plan refresh** | Twice a year or at renewal | The full stakeholder group | Whether the goals still matter, new priorities, planning the next phase |

Also reopen the plan between scheduled reviews whenever:

- a business goal shifts or a new priority appears
- a milestone is badly delayed or blocked
- the customer's organization changes — M&A, new leadership, a restructuring
- a major product release opens up new opportunities
- the account's health score moves significantly

## The plan document

```markdown
# Success plan: [account name]

| Role                             | Name   |
| -------------------------------- | ------ |
| CSM (owns the plan)              | [name] |
| Customer lead                    | [name] |
| Executive sponsor, our side      | [name] |
| Executive sponsor, customer side | [name] |

Runs from [start date] to [end date] · First drafted [date] · Last revised [date]

## The customer's situation
- Sector: [industry]
- What matters most to them: [their two or three top strategic priorities]
- Problems this plan tackles: [the key challenges]

## Goal 1: [business goal, worded the way the customer words it]
Payoff if we get there: [the business impact]

**How we will measure it**
| KPI      | Starting point  | Measured on | Target       | Tracking (method · who · how often) |
| -------- | --------------- | ----------- | ------------ | ----------------------------------- |
| [metric] | [current value] | [date]      | [goal value] | [method] · [person] · [frequency]   |

**Milestones**
| ID   | Milestone | Done means             | Our owner | Their owner | Due    | Depends on         | Status |
| ---- | --------- | ---------------------- | --------- | ----------- | ------ | ------------------ | ------ |
| M1.1 | [name]    | [the finished state]   | [name]    | [name]      | [date] | [items, or "none"] | [Not started / In progress / Complete / At risk] |
| M1.2 | [name]    | ...                    |           |             |        |                    |        |

## Goal 2: [business goal]
[same layout as Goal 1]

## Goal 3: [business goal]
[same layout as Goal 1]

## Risks and how we will handle them
| #   | Risk   | Mitigation   | Owner  |
| --- | ------ | ------------ | ------ |
| 1   | [risk] | [mitigation] | [name] |
| 2   | ...    |              |        |

## Review rhythm
| Review           | How often   | Next one |
| ---------------- | ----------- | -------- |
| Progress check   | [frequency] | [date]   |
| Quarterly review | quarterly   | [date]   |
| Plan refresh     | [twice yearly or at renewal] | [date] |

## Staying in touch
- Routine updates: [channel, and how often]
- Escalations: [the route for raising a problem]

## Sign-off
| Signatory                     | Name    | Date   |
| ----------------------------- | ------- | ------ |
| CSM                           | [name]  | [date] |
| Customer lead                 | [name]  | [date] |
| Executive sponsors (optional) | [names] |        |
```

If the user wants a file to circulate, offer to produce the plan as a formatted Word (DOCX) document.

## Variations by situation

- **After onboarding** — build the plan around time-to-value measures and adoption targets, with shorter milestone horizons of 30/60/90 days.
- **Strategic enterprise account** — plan over several years and refresh goals annually; build in organizational change management and a cadence for executive engagement.
- **Renewal recovery** — concentrate on rebuilding evidence of value and resolving the customer's specific concerns; tighten the review rhythm to weekly check-ins until the account has stabilized.
- **Expansion focus** — add a "future state" section that links expansion opportunities to the business goals.
- **Tech-touch or scaled CS** — reduce the plan to one or two goals with automated milestone tracking, and use in-app progress indicators and automated alerts in place of CSM check-ins.

## Ground rules

- Never invent the customer's business goals, priorities, or challenges. They must come from the customer or from recorded discovery conversations; where they are missing, mark the field `[ASK IN DISCOVERY]`.
- Never produce baseline figures or KPI targets without customer data. Label anything unknown "Not yet measured" rather than estimating it.
- Never present the plan as final until the customer has agreed to it. Point out every section the customer has not yet validated.
- Mark the origin of each element with one of four tags: `(account record)`, `(plan methodology)`, `(customer's own words)`, or `(CSM suggestion)`.
