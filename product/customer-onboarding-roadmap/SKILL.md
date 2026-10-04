---
name: customer-onboarding-roadmap
description: "Builds a milestone-based onboarding plan that takes a newly signed customer from contract to first realized value, using a 30/60/90-day Foundation, Adoption and Optimization structure with entry and exit criteria, owners on both sides, checkpoint reviews, a communication cadence, risks and a stakeholder map. Use when a customer success manager or implementation lead needs to plan the onboarding of a new customer, turn a sales handoff into a kickoff-ready plan, or adapt the onboarding timeline for SMB, enterprise, usage-based, multi-product or tech-touch accounts."
---

# Customer Onboarding Roadmap

You help the customer success team turn a freshly signed deal into a structured onboarding plan. The plan runs from contract signature to the point where the customer first realizes value, and it is organized around milestones, clear owners on both sides, and formal checkpoints. Everything customer-specific comes from the user, the CRM, or uploaded documents and connected knowledge sources.

## Where the account details live

Use connected tools and sources where they exist:

- **CRM** (HubSpot, Salesforce): the account record, what the contract covers, ARR, the main contacts, and the notes written when the deal closed-won
- **Project tracker** (Asana, Monday, Jira, Notion): the task list, milestone progress, and who is assigned to what

Without any connection, the user can supply the details by hand; the plan stands on its own as a document.

## How to build the plan

Each time you plan an onboarding, work through these five steps in sequence.

### Step 1 — Gather the requirements

Before you draft anything, pin down the inputs below. Point out anything missing, because a plan built on partial requirements ends up being redone.

| Input | Where it usually comes from | What it drives |
|---|---|---|
| **Contract scope** | CRM, sales handoff | What the customer bought and what you are obliged to deliver |
| **Customer business goals** | Sales notes, discovery calls | Lets you tie milestones to results the customer actually cares about |
| **Technical environment** | The technical assessment done during pre-sales | How complex integrations will be, and which technical milestones are needed |
| **Customer team** | Sales handoff, CRM contacts | Who holds a stake, who decides, and who you will deal with day to day |
| **Timeline constraints** | Contract, customer request | Fixed dates (for instance, going live before the fiscal year closes) that the plan has to respect |
| **Known risks** | Sales handoff notes | Concerns raised during the sale, such as thin IT capacity or competing priorities |
| **Success criteria** | Stated by the customer or agreed jointly | What "finished" means from the customer's point of view |

### Step 2 — Lay out the three phases

The default arc is 90 days split into three phases, each with an explicit way in and way out:

| | **Phase 1 — Foundation** (Days 1–30) | **Phase 2 — Adoption** (Days 31–60) | **Phase 3 — Optimization** (Days 61–90) |
|---|---|---|---|
| **Aim** | Technical setup finished, key stakeholders onboarded, first value shown | Wider team adoption, workflows in place, early evidence of ROI | Full deployment, value confirmed, handover to a steady-state CS relationship |
| **Starts when** | The contract is signed and the sales-to-CS handoff is done | Phase 1 exit criteria are met | Phase 2 exit criteria are met |
| **Typical milestones** | Kickoff call; technical setup; training for admins; initial configuration; first use case in production | Training for end users; configuring workflows; an adoption check-in; a usage review | Enabling advanced features; reviewing success metrics; a check-in with the executive sponsor; formally handing the account to ongoing CS |
| **Ends when** | The core platform is configured, admins are trained, and at least one use case is running | The target user activation rate is reached, core workflows are running, and first success metrics are recorded | The success criteria gathered in Step 1 are met, an ongoing cadence is in place, and a success plan has been drafted |

### Step 3 — Give every milestone an owner on both sides

Each milestone needs a named owner on your side and on the customer's. The usual roles:

- **CSM** (your team) — owns the plan overall, manages the relationship, tracks milestones, handles escalation
- **Implementation / Solutions** (your team) — technical setup, configuration, integrations, data migration
- **Trainer** (your team) — delivers admin and end-user training
- **Customer Project Lead** (customer team) — coordinates internally, secures resources, makes decisions
- **Customer IT / Admin** (customer team) — provides technical access, sets up the environment, runs the security review
- **Executive Sponsor** (one on each side) — keeps strategy aligned, clears escalations, validates success

On small accounts one person may cover several of these roles. On enterprise accounts, add roles as the situation demands — a dedicated data migration lead or change management lead, for example.

### Step 4 — Schedule the checkpoints

Hold a formal checkpoint at the start, whenever one phase gives way to the next, and on day 90:

| Checkpoint | When | What it covers | Who attends |
|---|---|---|---|
| **Kickoff** | Day 1–5 | Introductions, walkthrough of the plan, confirming goals, agreeing the timeline | Every stakeholder |
| **30-day review** | Day 28–32 | Phase 1 milestones, resolving issues, readiness for Phase 2 | CSM, customer project lead, and sponsors if they wish |
| **60-day review** | Day 58–62 | Adoption metrics, how well workflows are working, planning Phase 3 | CSM and customer project lead |
| **90-day review** | Day 88–92 | Whether success criteria were met, value summary, move to the ongoing cadence | CSM, customer project lead, and executive sponsors |

Every checkpoint must leave a written record of four things: milestones completed, milestones that slipped (with their new dates), issues still open, and next steps everyone agreed on.

### Step 5 — Set the communication rhythm

Decide up front how and how often you will keep in touch during onboarding:

- **Status update** — weekly, by email or in a shared document, owned by the CSM
- **Working sessions** — whenever milestones call for them, over video, owned by the implementation lead
- **Escalation** — whenever needed, by direct message plus email, owned by the CSM or the customer project lead
- **Checkpoint review** — at each phase boundary, on a video call with an agenda, owned by the CSM

Fit the rhythm to the customer. Some want asynchronous updates, others want a weekly sync — ask which at kickoff.

## The plan document

The risks section carries forward the known risks from Step 1, each paired with a mitigation and an owner.

```
CUSTOMER ONBOARDING PLAN
Account: [name]
CSM: [name]
Start date: [date]
Target completion: [date — usually 90 days after start]
Contract scope: [short summary of what was bought]
Success criteria: [the customer's own definition of success]

PHASE 1 — FOUNDATION (Days 1–30)
Goal: [tailored to this customer]
  Milestone 1: [description]
    Owner: [name/role] | Due: [date] | Status: [Not started / In progress / Complete]
  Milestone 2: [description]
    Owner: [name/role] | Due: [date] | Status: [...]
  ...
  Exit criteria: [what has to be true before Phase 2 starts]
  30-day checkpoint: [date]

PHASE 2 — ADOPTION (Days 31–60)
Goal: [tailored to this customer]
  Milestone 1: [description]
    Owner: [name/role] | Due: [date] | Status: [...]
  ...
  Exit criteria: [what has to be true before Phase 3 starts]
  60-day checkpoint: [date]

PHASE 3 — OPTIMIZATION (Days 61–90)
Goal: [tailored to this customer]
  Milestone 1: [description]
    Owner: [name/role] | Due: [date] | Status: [...]
  ...
  Exit criteria: [what has to be true for onboarding to count as complete]
  90-day checkpoint: [date]

RISKS & MITIGATIONS:
  1. [risk] → [how it will be mitigated] → Owner: [name]
  2. ...

COMMUNICATION CADENCE:
  [as agreed in Step 5]

STAKEHOLDER MAP:
  Your team:     [name — role, name — role, ...]
  Customer team: [name — role, name — role, ...]
```

## Adapting the timeline

The 30/60/90 structure is only the default. Reshape it to the product and the customer:

- **Simple product, SMB customer** — shrink it to 14/30/45 days, with fewer milestones and lighter checkpoints.
- **Complex platform, enterprise customer** — stretch it to 30/60/90/120 days, adding a Phase 0 for pre-kickoff preparation and a Phase 4 for advanced enablement.
- **Usage-based product** — swap the calendar gates for usage triggers; for example, Phase 2 begins once the customer hits X active users rather than on day 31.
- **Multi-product deployment** — run a parallel track for each product on one shared timeline, with combined checkpoints.
- **High-touch vs. tech-touch** — when onboarding is pooled or tech-touch, swap person-by-person milestones for automated triggers such as a sequence of welcome emails, guides inside the app, and self-serve training, and add group check-ins on a schedule.

## Ground rules

- Never make up customer requirements, technical environments, or business goals. Every customer-specific detail must come from the user or from connected data; where something is missing, insert a placeholder field that is plainly marked as such.
- Never presume how the customer's team is structured or how much capacity they have. Ask rather than infer.
- Never put specific adoption metrics or usage targets in the plan unless customer data supports them.
- Label each element with where it came from — `[From account data]`, `[From onboarding framework]`, or `[CSM input needed]`.
