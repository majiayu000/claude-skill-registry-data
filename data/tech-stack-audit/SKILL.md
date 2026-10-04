---
name: tech-stack-audit
description: Audit your GTM tech stack for overlap, gaps, and wasted spend. What each tool actually does, where two tools do the same job, what nobody uses, and a consolidation plan with the renewal calendar attached. Built for B2B RevOps teams, customizable to your stack and your budget. Trigger on "audit my tech stack", "what tools overlap", "what are we not using", "cut our GTM spend", "what should we consolidate", or any tooling diagnostic.
---

# Tech-Stack Audit

## What this does
Reads your list of GTM tools and returns a straight read on the stack: what each one is for, where two tools quietly do the same job, what is paid for and barely touched, and where a real capability is missing. Then it lays out a consolidation plan ordered by savings and risk, with renewal dates attached so the plan lands before the auto-renew does.

## What you'll need
You do not need to connect anything to get value today. Bring your tool list and the skill runs now. Connect the tools below and it reads usage and spend automatically and grounds the "nobody uses this" call in real data.

- Works today with: a list of your GTM tools with annual cost, renewal date, owner, and what each is meant to do. A spreadsheet or paste is enough.
- More powerful connected to a CRM or admin export: it reads seat counts and last-login data automatically, so unused is a fact, not a hunch.
- Sharper with a data warehouse or billing export: reconciles real spend against contracts and catches the tools nobody remembers paying for.
- Sharper with usage exports from the tools themselves: separates "licensed" from "actually used" seat by seat.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the list you give it today and gets more powerful as you connect tools. It never calls a tool unused on a guess. Missing usage data is a question to answer, not an assumption to make.

- **Bring your data**: paste your tool list with costs and renewals. The skill runs the full audit today on your real stack. No connection required.
- **Connect your tools**: the same skill pulls seat and login data and reconciles spend automatically, so unused and overlapping are proven, not asserted. Same output, less effort, defensible.
- **Just exploring**: no data yet? Get the framework, the capability map, the overlap and consolidation logic, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a usage export to pull or a contract to dig up.

## Customize this for yourself
This was built for a B2B SaaS org auditing a mid-size GTM stack. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| INVENTORY source | where the tool list lives | a spreadsheet, a spend/billing export |
| CAPABILITY map | the jobs a GTM stack must cover | CRM, enrichment, sequencing, routing, analytics, CS |
| USAGE source | how you measure real use | seat counts, last-login, admin export |
| SPEND basis | the cost figure you audit | annual contract value per tool |
| RENEWAL field | when each contract comes up | renewal date and notice window |
| OWNER field | who owns each tool | the team or person accountable |
| KEEP criteria | what earns a tool its seat | used, unique job, positive ROI |

Define your capability map first. Overlap only means something against the list of jobs the stack is supposed to do. Two tools sharing a job is waste. Two tools doing different jobs that sound similar is not.

## The method

### Capability mapping
Place every tool on the map of jobs a GTM stack has to cover. A tool that maps to no job is a candidate to cut. A job with no tool is a gap. This is the frame everything else reads against.

### Overlap detection
Find the jobs covered by more than one tool and show the pair, the cost of each, and which one carries the usage. Two tools doing the same job is the most common and most defensible cut. Name the redundant one and the savings.

### Unused and underused
Flag tools with low or zero real usage against seats paid for. State the basis (last-login, seat activation) so nobody argues the call. An unused tool at renewal is the easiest dollar in the stack to save.

### Gap check
Name the capabilities with no tool or a tool too weak to count. A gap is as much a finding as an overlap. The plan is not only what to cut, it is what the cuts should fund.

### Consolidation plan
Order the moves by net savings and switching risk, and attach each to its renewal date. Cutting a redundant tool the month before it auto-renews is a clean win. Ripping out a load-bearing tool mid-contract is not. The renewal calendar sequences the plan.

## Quality gates
- No tool called unused without stating the usage basis behind the call.
- Overlap always names both tools, both costs, and which one keeps the job.
- Every recommended cut carries its renewal date and notice window.
- Gaps are reported alongside cuts. The audit is not just a cost-cutting list.

## Output (example)
```
TECH-STACK AUDIT · 18 tools · $412K annual
Job                 Tools                    Finding
Enrichment          Tool A ($60K), Tool B ($28K)   OVERLAP, B carries 12% of usage
Sequencing          Tool C ($75K)            KEEP, core, high usage
Sales analytics     Tool D ($40K)            UNDERUSED, 6 of 40 seats active in 90d
Lead routing        none                     GAP, routed by hand today

Consolidation plan (by savings, sequenced to renewals):
  1. Drop Tool B at its renewal next month. Saves $28K. Usage already on Tool A.
  2. Right-size Tool D to 10 seats at renewal in Q3. Saves ~$30K.
  3. Fill the routing gap. Fund it partly from the two cuts above.
```
Illustrative figures. Your run reports your real stack and spend.

## Where the numbers come from
The usage window (90-day last-login) and the keep criteria are defaults, not laws. They suited a mid-market SaaS stack review. If your tools are seasonal or your teams smaller, adjust the window. The capability map and the keep bar are yours.

## Example chat

**You:** Here's our GTM tool list with costs and renewal dates, can you audit it?

**Claude:** Mapped it to your capability list first.
```
Job              Tools                          Finding
Enrichment       Tool A ($60K), Tool B ($28K)   OVERLAP, B carries 12% of usage
Sales analytics  Tool D ($40K)                  UNDERUSED, 6 of 40 seats active
Lead routing     none                           GAP, routed by hand today
```
Key insight: the gap matters as much as the cuts. The routing gap is probably costing more in leaked leads than either overlap saves, so the plan should fund the gap from the cuts, not just bank the savings. One sharpener: connect the CRM's login export so "12% of usage" is a real number instead of an estimate.

## Go further
The audit runs once, by hand. Here is where an operator takes it once the manual version proves out.

- **Reconcile spend automatically.** Point the audit at a billing export (via a data warehouse like Snowflake) so contract cost and actual usage stay in sync without a quarterly manual pull.
- **Catch the renewal before it auto-fires.** A scheduled Claude task checks the renewal calendar monthly and flags any tool inside its notice window that is still marked underused.
- **Prove usage seat by seat.** Pull last-login data straight from each tool's admin API instead of asking IT for an export, so the "unused" call is defensible in the room.

The audit finds the waste once; the calendar is what stops it from creeping back.


## Make it yours
Fork it. Change the capability map, the usage basis, the keep criteria, the way the plan is sequenced. The point is not to run someone else's stack review. It is to run yours, so the cuts are defensible and the renewals never catch you. Built by an operator. Customize it, break it, make it better.