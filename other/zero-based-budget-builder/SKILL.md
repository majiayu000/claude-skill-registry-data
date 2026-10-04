---
name: zero-based-budget-builder
description: Builds a zero-based budget for a cost center by requiring every line item to be justified from first principles rather than rolled forward from the prior year.
---

# Zero-Based Budget Builder

## When to use

Use this skill when a cost center or department budget has grown incrementally for several years without scrutiny, when a new cost reduction target has been set and the budget owner needs a structured approach to re-justify spend, or when an incremental budget process is being replaced with zero-based budgeting. ZBB is most powerful for overhead and SG&A cost centers where spend tends to accumulate through inertia rather than need.

## What it does

Produces a zero-based budget template and review guide for one cost center: a structured challenge of every spend category from a zero base, a justification requirement for each line, and a recommended budget amount for each category based on the user's inputs and the ZBB logic applied.

## Method

This skill applies the Zero-Based Budgeting method, which requires each spend line to be justified on its own merits for the coming period rather than being derived as "last year plus X%."

**Step 1: Define the decision unit**
- Confirm the cost center name, the budget owner, the cost center's primary purpose (what service or output it provides), and the cost period (typically 12 months).
- Identify the cost center's internal customers or stakeholders: who depends on this cost center's output and what do they actually need from it?

**Step 2: List all current spend categories**
- From the prior-year actuals or the current budget, list every spend line.
- Group lines into: People (salaries, benefits, contractors), Technology (software, hardware, infrastructure), External services (consulting, legal, audit, outsourced services), Facilities and infrastructure (rent, utilities, maintenance), and Discretionary (training, travel, events, subscriptions, memberships).

**Step 3: Apply the zero-based challenge to each category**
For each category, work through four questions:
1. What output does this spend produce? State the specific deliverable or service it enables.
2. What is the minimum level of this spend required to meet the cost center's core obligations (legal, regulatory, or contractually mandated)?
3. What level of spend optimally meets the cost center's purpose (above minimum, at current performance standard)?
4. What level of spend would be required to enhance the cost center's output (above current standard, for investment scenarios)?

Label each spend line with one of three levels:
- Level 1: Minimum (mandatory/non-discretionary)
- Level 2: Target (recommended baseline for this budget cycle)
- Level 3: Enhancement (optional, to be approved separately)

**Step 4: Challenge Level 2 assumptions**
- For each Level 2 item, verify: Has the need changed since last year? Is the quantity or headcount still justified by current demand? Is the unit cost competitive (benchmarked or recently tendered)? Could the same output be achieved at lower cost (automation, self-service, shared service)?
- Reduce the Level 2 estimate where a cheaper alternative has been identified. Document the basis for each revised figure.

**Step 5: Build the ZBB output**
- Total Level 1: the non-negotiable budget floor.
- Total Level 2: the recommended budget.
- Total Level 3: investment items for separate approval.
- State the saving versus the prior-year budget: (prior-year total) minus (Level 2 total) = identified saving.
- If a specific target saving has been given, flag whether Level 2 meets the target. If not, identify which Level 2 items could be moved to Level 1 and what the service consequence would be.

**Step 6: Prepare the justification package**
- For each Level 2 line, write one sentence: what the spend is, what it enables, and why the stated amount is the right level.
- This is the budget owner's evidence if challenged by Finance or the CFO.

## Inputs

- Prior-year budget or actuals for the cost center, by line item.
- The cost center's primary purpose and key outputs.
- Any mandatory or contractually committed spend items.
- Any saving target (percentage or dollar amount) given by Finance or leadership.
- Budget period.

## Output format

1. Decision unit summary (cost center purpose, owner, prior-year total, period).
2. ZBB line-item review (prose list per category: level classification, challenged amount, prior-year amount, saving or increase, and one-sentence justification).
3. Level 1 / Level 2 / Level 3 summary totals.
4. Saving versus prior year (total, and as a percentage).
5. Target gap analysis (if a saving target was provided: does Level 2 meet the target? If not, what is the gap and what are the options?).
6. Justification sentences for each Level 2 line (one sentence per line, ready for the budget submission).

## Example

**User input:**
"I manage the Corporate Communications cost center. Prior-year budget: $1.1M. Main items: 2 FTEs ($240K), agency retainer ($360K), media monitoring tool ($48K), events ($180K), PR subscriptions and memberships ($72K), travel ($90K), design and production ($110K). My saving target is 20%."

**Claude output (abbreviated):**
> **ZBB review (selected)**
> - Agency retainer $360K: Level 2 challenge. What deliverables does the retainer produce? If it covers day-to-day press inquiries and campaign support, is the full retainer utilized each month? Recommend a utilization audit before the next renewal. If utilization is below 70%, renegotiate to a reduced scope or hourly model. Revised Level 2 estimate pending audit. Flag as amber.
> - Events $180K: Level 3 (enhancement) unless specific events are contractually committed. In a cost-cutting cycle, recommend reclassifying as Level 3 and submitting for leadership approval. Level 1 = $0. If 1 flagship event is considered mandatory, Level 1 = $60K, Level 2 = $120K, Level 3 = $180K.
> - Media monitoring tool $48K: Level 1 (required for crisis management and regulatory monitoring). No reduction recommended.
>
> **Summary**
> Level 1 (minimum): $648K. Level 2 (recommended): $880K. Prior-year: $1.1M. Saving at Level 2: $220K (20%). Target: 20%. Level 2 meets the target exactly. Level 3 (events enhancement above $120K): $60K held separately for leadership approval.
