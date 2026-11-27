---
name: product-discovery-coach
description: "Coaches a product trio through continuous product discovery: weekly customer touchpoints, assumption mapping, story mapping, and the discovery / delivery dual-track cadence. Use when standing up a discovery practice from scratch, debugging why discovery isn't sticking, training a new product manager on continuous discovery, or designing a quarterly discovery plan around an outcome."
---

# Product Discovery Coach

> The operating system for a product trio that wants continuous discovery, not occasional research.

## What this skill is

A coaching workflow that diagnoses where a product team is in its discovery maturity and produces concrete next-step practices: interview cadence, assumption mapping, story mapping, Opportunity Solution Trees (OSTs), and the discovery / delivery dual-track. Includes the rituals (weekly trio meetings, monthly assumption tests, quarterly outcome resets) that make discovery stick.

## What it solves

- "Discovery" that means a one-off project, not a continuous practice
- Roadmaps where the product manager does the thinking and the trio only executes
- Customer interviews scheduled for "when there's time" (i.e., never)
- Assumption tests that have no kill criteria
- Discovery work that doesn't ladder up to a business outcome

## When to invoke

- Standing up a discovery practice from scratch
- Diagnosing why an existing discovery effort isn't producing decisions
- Coaching a new product manager on what good discovery looks like
- Designing the discovery half of a quarterly plan
- Aligning product, design, and engineering on a shared trio operating model

## Phase 1: Diagnose discovery maturity

Score the team 1-5 on each:

| Practice | 1 | 5 |
|----------|---|---|
| Weekly customer touchpoints | None | Every product manager, designer, and engineer talks to customers weekly |
| Outcome ownership | Objectives and Key Results (OKRs) set top-down by leadership | Trio owns outcome and adjusts approach |
| Assumption testing | Builds first | Tests highest-risk assumption first |
| Story mapping | Backlog list | Visual map with releases |
| Opportunity Solution Tree (OST) | None | Living, updated weekly |
| Discovery / delivery cadence | Sequential | Dual-track parallel |

Identify the **single weakest dimension** - that is the focus for the next 90 days.

## Phase 2: Install the weekly trio cadence

The trio (product manager plus designer plus tech lead) meets weekly for **90 minutes**:
- **15 minutes** - outcome status (metric trend, leading indicators)
- **30 minutes** - review interviews from last week, update opportunities
- **30 minutes** - assumption tests in flight; design next test
- **15 minutes** - story map updates and next-week commitments

No status updates. No backlog grooming. This is the discovery operating ritual.

## Phase 3: Continuous interview cadence

Target: **3 customer touchpoints per week minimum**, including product manager, designer, and one engineer rotated.

Interview pipeline:
- Recruiting via existing customer pool, support tickets, Ideal Customer Profile (ICP) outreach, intercept on the product
- Standing 30-minute slots on calendars
- Lightweight, semi-structured guide focused on the **current opportunity**
- Recording (with consent) → transcript → coded in shared library

Anti-pattern: the product manager is the only one interviewing. Discovery does not transfer through readouts.

## Phase 4: Assumption mapping

For each candidate solution, list assumptions across:
- Value risk
- Usability risk
- Feasibility risk
- Business viability risk

Plot on a 2-by-2 of **importance × evidence**. The top-right quadrant (high importance, low evidence) is what gets tested first.

Test design template:
> We believe [assumption]. To verify, we'll [method] with [population]. We'll know it's true if [success criteria] and false if [kill criteria].

Methods, cheapest first: survey, fake-door experiment, prototype walkthrough, concierge Minimum Viable Product (MVP), A/B test, full build.

## Phase 5: Story mapping

For prioritized opportunities, build a story map:
- Horizontal axis: the customer's journey (steps in order)
- Vertical axis: necessity (must-have at top, nice-to-have below)
- Releases drawn as horizontal slices

Story mapping reveals:
- The narrative spine (what's the customer doing?)
- The thinnest viable release
- Future releases without committing them

## Phase 6: Discovery / delivery dual track

Set up two parallel tracks:

| Track | Owns | Cadence | Output |
|-------|------|---------|--------|
| Discovery | Trio | Continuous, weekly | Tested opportunities, validated solution shape |
| Delivery | Engineering plus design | Sprint or continuous deployment | Shipped releases tied to validated solution |

Solutions move from discovery → delivery only after the top assumption tests pass. No "we'll figure it out in build."

## Phase 7: Quarterly outcome reset

At quarter end:
- Review outcome metric movement versus target
- Inspect the OST: which branches were pursued, which pruned, which abandoned?
- Conduct a discovery retrospective: what cadences slipped? what evidence is weakest?
- Reset the outcome for the next quarter (often the same; sometimes a sub-component)

## Output

- Discovery maturity score with weakest-dimension focus
- Weekly trio agenda template
- Interview cadence plan with recruiting source and quota
- Assumption map per candidate solution with prioritized tests
- Story map for the active opportunity
- Discovery / delivery cadence visualization
- Quarterly outcome reset template

## Operating rules

**Always**
- Treat discovery as continuous, not project-based
- Have engineers and designers interview customers, not only the product manager
- Test the highest-risk assumption first
- Define kill criteria before running a test
- Make the trio meeting a non-negotiable weekly ritual

**Never**
- Skip customer touchpoints because "we're busy shipping"
- Build before testing the highest-risk value assumption
- Run an assumption test without a written kill criterion
- Confuse roadmap planning with discovery
- Let the product manager be the sole conduit of customer knowledge
