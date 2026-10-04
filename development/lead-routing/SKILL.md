---
name: lead-routing
description: Design a lead routing and SLA model someone can actually implement. The assignment rules, the round-robin or account-based logic, the SLA timers, and the fallbacks when a rep is out or a lead has no owner. Built for B2B RevOps teams, customizable to your CRM and your team shape. Trigger on "design lead routing", "who should get this lead", "build our SLA", "round robin rules", "leads are falling through", or any routing diagnostic.
---

# Lead Routing

## What this does
Takes your team shape and your rules and produces a routing and SLA model written to be built. It lays out how a lead gets matched to an owner, whether by round-robin, territory, or account ownership, sets the SLA clock for first touch, and defines the fallbacks for the cases that quietly break every routing setup: the rep who is out, the lead that matches nobody, the account already owned. The output is a spec, not a suggestion.

## What you'll need
You do not need to connect anything to get value today. Bring your team list and rules and the skill runs now. Connect the tools below and it reads your live ownership and territories automatically and tests the rules against real leads.

- Works today with: a list of your reps and territories, your segment or ICP definition, and a sample of recent inbound leads with the fields you would route on.
- More powerful connected to a CRM: it reads live account ownership, rep capacity, and territory fields automatically, so routing respects who already owns what.
- Sharper with an enrichment tool: fills the firmographic fields (size, industry, geo) that routing depends on before assignment, so fewer leads fall to fallback.
- Sharper with an activity tool: measures real first-touch times so the SLA is set against reality, not hope.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the rules you give it today and gets more powerful as you connect tools. It never assigns a lead on a field it cannot see. A missing routing field is a fallback path, not a guess.

- **Bring your data**: paste your team, territories, and a lead sample. The skill designs the full model today against your real shape. No connection required.
- **Connect your tools**: the same skill reads live ownership and capacity and tests the rules against real inbound, so you find the leaks before you ship. Same output, less effort, safer.
- **Just exploring**: no data yet? Get the framework, the rule structure, the SLA and fallback patterns, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to enrich or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org routing inbound to a segmented sales team. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | a CRM (Salesforce, HubSpot, Pipedrive) |
| ROUTING model | how leads match to owners | round-robin, territory, account-based, hybrid |
| ROUTING fields | the fields assignment reads | segment, geo, company size, existing owner |
| SEGMENTS | the buckets you route into | SMB, Mid-Market, Enterprise |
| SLA timers | first-touch clock per segment | 5 min for hot inbound, 1 business day otherwise |
| CAPACITY rule | how load is balanced | equal round-robin, weighted by ramp |
| FALLBACKS | what happens when no rule matches | queue owner, manager, holding pool |

Pin the account-ownership rule first. The fastest way to poison a routing model is to hand a rep a lead at a company another rep already runs.

## The method

### Match logic
Define the order rules are evaluated in, because order is the model. Typically: existing account owner wins first, then territory or segment match, then round-robin within the matched pool. Print the precedence so there is no ambiguity about which rule fires when two could.

### Round-robin and capacity
Within a pool, assign in rotation, and state how capacity is handled: flat rotation, or weighted so a ramping rep gets fewer. Define what "available" means so leads never route to someone out of office. Capacity without an availability rule just routes leads into a void.

### SLA timers
Set a first-touch clock per segment and state the business-hours rule. Define the escalation: what happens at the SLA breach, who gets notified, and whether the lead re-routes. An SLA with no breach action is a wish.

### Fallback paths
Name the destination for every lead that matches nothing: no territory, no enrichment, no available rep. A holding queue with a named owner beats a lead sitting unassigned. Every path in the model must terminate at a human.

### Implementation spec
Output the rules as an ordered, buildable list: field checks, pool definitions, rotation logic, timers, and escalations. Written so whoever configures the CRM can build it without guessing what you meant.

## Quality gates
- Every routing path terminates at a named owner or queue. No lead can fall through.
- Rule precedence is explicit. No two rules can fire ambiguously.
- Every SLA has a breach action, not just a timer.
- Account ownership is checked before any new assignment. No poaching by routing.

## Output (example)
```
LEAD ROUTING MODEL · 3 segments · 14 reps
Precedence:
  1. Existing account owner -> that owner (skip all below)
  2. Enterprise (size >= 1000) -> Ent pool, round-robin, weighted by ramp
  3. Mid-Market -> MM pool, flat round-robin
  4. SMB -> SMB pool, flat round-robin
  5. No match / missing fields -> holding queue (owner: RevOps lead)

SLA:
  Hot inbound (demo request): 5 min first touch, breach -> notify rep + manager, re-route at 15 min
  Standard inbound: 1 business day, breach -> notify manager

Fallbacks:
  Rep out of office -> skip in rotation, do not queue to them
  No enrichment -> route to holding queue, flag for enrichment, not to a rep
```
Illustrative structure. Your run reflects your real team and rules.

## Where the numbers come from
The SLA timers (5 minutes hot, 1 business day standard) and the size cutoffs are defaults, not laws. They suited a mid-market SaaS inbound motion. If your buyers move slower or your segments split elsewhere, change them. The precedence logic holds. The thresholds are yours.

## Example chat
Here is the skill running on a real team, start to finish.

**You:** Leads are falling through. Design the routing model for our 3-segment team.

**Claude:** Here's the precedence, SLA, and fallback spec.
```
Precedence:
  1. Existing account owner -> that owner (skip all below)
  2. Enterprise -> Ent pool, round-robin, weighted by ramp
  3. No match / missing fields -> holding queue (owner: RevOps lead)

SLA: Hot inbound 5 min first touch, breach -> notify rep + manager
```
The catch worth naming: rule 5, the fallback, is the line that actually stops leads from disappearing. Most routing models define the happy path and leave "no match" undefined, which is exactly where leads go quiet. Every path here terminates at a named human. One sharpener: connect your CRM so "existing account owner" checks live ownership instead of the sample list you pasted.

## Go further
The spec is step one. Here is where an operator takes it once the manual version proves out.

- **Build it, don't just spec it.** Hand the ordered rule list to whoever configures Salesforce or HubSpot routing (native rules or a tool like LeanData), so the spec becomes the live config, not a doc that sits next to it.
- **Watch the SLA clock in real time.** Wire a scheduled Claude task to check first-touch time against the timer and post a breach alert to Slack the moment a lead crosses it.
- **Audit the fallback queue weekly.** Pull everything that landed in the holding queue from the CRM and report why (missing field, no territory match), so the enrichment gaps causing fallbacks actually get fixed.

You built the model once, now the leaks get caught as they happen.


## Make it yours
Fork it. Change the routing model, the pools, the timers, the fallbacks. The point is not to run someone else's routing. It is to run yours, written clearly enough that it gets built and no lead falls through. Built by an operator. Customize it, break it, make it better.