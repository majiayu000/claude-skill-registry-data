---
name: outcome-vs-output
description: >
  Audit a roadmap or backlog to distinguish outcomes from outputs. Use when the user says
  "outcome vs output", "escaping the build trap", "are we building the right things",
  "roadmap review", "feature factory", "output-driven team", "we keep shipping but nothing changes",
  or wants to shift focus from shipping features to delivering value
  - even if they don't explicitly say "outcome vs output".
---

## Overview

Based on **Escaping the Build Trap** by Melissa Perri. The "build trap" is when teams measure success by features shipped instead of value delivered. Feature factories build a lot - and move metrics very little. Perri's framework: every item in your backlog should trace to a measurable outcome. If it can't, question whether it should be built at all.

The output/outcome distinction:
- **Output** - something you ship ("we launched a dashboard")
- **Outcome** - a change in user or business behavior ("users now self-serve 40% of support queries")

Outputs are inputs to outcomes. Shipping outputs that don't move outcomes is waste.

## Workflow

### Step 1: List the current roadmap or backlog items
Work from the actual list. Don't audit hypothetically.

### Step 2: Classify each item
For each item, ask: "Is this an output or an outcome?"
- **Output:** a feature, a page, a report, an integration, a tool
- **Outcome:** a change in what users do or what the business achieves

Mark each: O (output) or OC (outcome).

### Step 3: Link outputs to outcomes
For every output, complete this sentence:
"If we build [output], we expect [user behavior change], which will result in [business metric change]."

If you can't complete the sentence, the output is not yet justified. Put it on hold.

### Step 4: Identify orphaned outputs
Outputs with no traceable outcome are "orphaned." These are the build trap. Common sources:
- Stakeholder requests with no user research behind them
- "We should have this" features with no metric attached
- Copy-what-competitors-have items

List all orphaned outputs. For each, decide: find the outcome it serves, reframe it, or remove it.

### Step 5: Check outcome ownership
For each outcome on the roadmap: does a specific team own it? Outcomes without owners don't get achieved.

### Step 6: Rewrite the roadmap in outcome language
Replace output-based roadmap items with outcome-based ones.

Before: "Q1: Launch user dashboard, Add CSV export, Rebuild notifications"
After: "Q1: Users can self-serve progress tracking (currently requires support ticket)"

### Step 7: Set a ratio target
Perri's guidance: a healthy team should spend 70%+ of capacity on outcome-driven work. Calculate the current ratio. If it's below 50%, the team is in the build trap.

## Anti-Patterns

**1. Relabeling outputs as outcomes**
Bad: "Our outcome is to launch the dashboard."
Good: Launching is never an outcome. "Users track their own progress without contacting support" is an outcome.

**2. Outcomes without baselines**
Bad: "Increase engagement."
Good: "Increase weekly active usage from 2.1 to 3.5 sessions per user."
Outcomes without baselines can't be measured, so they can never be achieved.

**3. Too many outcomes**
Bad: 12 outcomes for a quarter across one team.
Good: 1-3 outcomes per team. More than that means none will be achieved.

**4. Measuring outputs as proof of outcomes**
Bad: "We shipped 14 features this quarter - great execution."
Good: "We shipped 14 features. Did any of them move the metrics we cared about?"

## Quality Checklist

- [ ] Every roadmap item classified as output or outcome
- [ ] Every output linked to an outcome via "if we build X, we expect Y"
- [ ] Orphaned outputs identified and decision made (justify, reframe, or remove)
- [ ] Every outcome has an owner
- [ ] Roadmap rewritten in outcome language
- [ ] Output-to-outcome ratio calculated and above 50%
