---
description: Model best, base, and worst-case financial scenarios
---

# Scenario

Model financial scenarios for "$ARGUMENTS". Build structured best/base/worst-case projections to understand the range of possible outcomes and prepare contingency plans.

## Prerequisites

None — utility skill, run anytime. Works best when financial data exists in `.metapowers/finance/$ARGUMENTS/`.

## Process

1. **Gather context:**
   - If prior phase artifacts exist, read them for baseline data
   - Ask the user what decision or question the scenarios should inform
   - Determine the time horizon for the scenarios

2. **Define scenario parameters:**
   - Identify the 5-8 key variables that drive outcomes (revenue growth, churn, ARPU, hiring pace, etc.)
   - For each variable, define best/base/worst values with rationale
   - Reference `financial-model-template.md` for scenario table structure

3. **Build three scenarios:**
   - **Best case:** optimistic but plausible assumptions
   - **Base case:** most likely outcome based on current trajectory
   - **Worst case:** pessimistic but survivable assumptions
   - For each: project revenue, expenses, cash flow, and runway

4. **Analyze implications:**
   - What decisions change between scenarios?
   - At what point does the worst case become dangerous?
   - What early warning signals distinguish which scenario is unfolding?
   - What contingency actions should be prepared?

5. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/scenario.md` with sections:
   - **Scenario Question** — what decision this analysis informs
   - **Variable Assumptions** — table of inputs per scenario
   - **Scenario Projections** — financial outcomes per scenario
   - **Decision Triggers** — signals that indicate which scenario is playing out
   - **Contingency Plans** — actions to take in each scenario

## Output

The scenario analysis written to `.metapowers/finance/$ARGUMENTS/scenario.md`. Present a summary highlighting:
- Range of outcomes (worst to best)
- Key differentiating variables
- Decision triggers and contingency plans
