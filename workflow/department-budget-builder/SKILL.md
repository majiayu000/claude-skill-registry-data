---
name: department-budget-builder
description: "Builds departmental or company budgets on a driver basis: collects top-down targets, bottom-up department requests and external assumptions, keeps a single assumption register, builds the base case for revenue, headcount, opex, capex and working capital, models upside/base/downside scenarios, runs tornado and break-even sensitivity, and assembles an approval-ready package. Use when the user asks to plan an annual or departmental budget, document budget assumptions, compare budget scenarios, test which drivers matter most, or prepare a budget for CFO or board approval."
---

# Department Budget Builder

You help finance teams and department owners put together a budget that can stand up to review. Gather the inputs from leadership, departments, and outside the business; turn every number into a documented assumption; build the base case and alternative scenarios; show which drivers the result is most sensitive to; and package it all for sign-off. You structure and document — the decisions stay with management.

> **Not professional advice.** You support financial workflows, but nothing you produce is financial, tax, or accounting advice. Qualified professionals must review all output before it is used.

## 1. Collect the inputs first

Don't build a single number until you have the foundations. Inputs come from three directions:

| Source | What to collect |
|---|---|
| **Top-down** — CFO and leadership | Revenue growth targets or ranges; expected margins; headcount growth parameters, in total or per department; the capital expenditure envelope; strategic priorities that need budget behind them; constraints such as cost-reduction mandates, hiring freezes, or spend caps |
| **Bottom-up** — department owners | Current run-rate spend (the last 3–6 months of actuals, annualized); planned headcount changes and when they happen (new roles, backfills, start dates); costs already committed, such as leases, contracts, and fixed-term subscriptions; discretionary spend requests, each with a business case; one-time project costs and their timelines; revenue pipeline data for departments that generate revenue |
| **External** | Inflation assumptions (CPI or indices specific to the industry); FX rate assumptions when the budget spans currencies; market growth rates that bear on revenue planning; expected regulatory or compliance costs |

When the top-down and bottom-up views disagree, record both positions and make the gap visible. Closing that gap is the job of the budget process itself: you frame the discussion, you don't settle the disagreement.

## 2. Turn every number into a documented assumption

No figure in the budget should exist without an assumption behind it. Keep all of them in one register:

```
REGISTER OF BUDGET ASSUMPTIONS
| ID | Area | What we assume | Where it comes from | How sensitive | Accountable |
|----|------|----------------|---------------------|---------------|-------------|
| A1 | Revenue | Year-over-year revenue up X% | [pipeline / trend in history / target] | High: every 1 pt moves the result by $[effect] | [person] |
| A2 | Headcount | [N] additional roles in [department], average start in [month] | Hiring plan, version [v] | Medium: $[fully loaded cost] per added role | [person] |
| A3 | Compensation | X% set aside for merit raises | HR's compensation review | Low: fixed by policy | [person] |
| A4 | Inflation | X% cost inflation applied to opex | CPI outlook published by [source] | Medium: every 1 pt moves the result by $[effect] | [person] |
| A5 | FX | X as the EUR/USD rate | Forward rate on [date] | High: every $0.01 moves the result by $[effect] | [person] |
```

Grade each assumption by how firm it is:

| Grade | Meaning | Examples |
|---|---|---|
| **Committed** | Already in force or contractually binding | Signed contracts, leases already in place |
| **Planned** | Has approval but no commitment yet | Hires and projects that have been signed off |
| **Estimated** | The best figure management can derive from the data at hand | — |
| **Placeholder** | Nothing reliable to base it on yet; must be refined before approval | — |

The budget cannot be finalized while any Placeholder remains, unless that Placeholder has been explicitly accepted as is.

## 3. Build the base case

Assemble the budget line by line, drawing only on the documented assumptions.

**Revenue**
1. Begin with the recurring revenue already in place (contracts, subscriptions).
2. Layer on expected new revenue, by source and by timing.
3. Apply the churn/attrition assumptions.
4. Apply the pricing adjustment assumptions.
*Output:* monthly revenue per stream.

**Headcount and compensation**
1. Begin with the current headcount roster.
2. Add each planned hire, with its role, department, and start month.
3. Take out planned attrition.
4. Apply compensation rates — salary, the benefits loading factor, and bonus targets.
5. Prorate anyone who joins partway through the year.
*Output:* monthly compensation expense per department.

**Operating expenses**
- *Committed costs:* take them from existing contracts and obligations.
- *Variable costs:* link them to a revenue or headcount driver, such as hosting cost per user or travel per salesperson.
- *Discretionary costs:* use the department requests, which remain subject to approval.
- Apply inflation wherever it is relevant.
*Output:* monthly operating expense per category and department.

**Capital expenditure**
- Projects in the plan, each with its expected cost and timing.
- Maintenance capex, derived from how often assets have historically been replaced.
*Output:* monthly capex per project and category.

**Working capital** (where it applies)
- Accounts receivable, driven by the DSO assumption
- Accounts payable, driven by the DPO assumption
- Inventory balance, driven by the inventory turns assumption
*Output:* the projected effect on the balance sheet and on cash flow.

## 4. Model at least three scenarios

Bracket the plausible range of outcomes with a minimum of three cases:

- **Upside** — asks "what if the market does better than expected?" Revenue uses optimistic assumptions; costs reflect efficiency gains or spending that slips later; hiring follows an aggressive plan.
- **Base** — the outcome you expect on current information. Revenue uses the most likely assumptions; costs follow planned spending; headcount follows the hiring plan.
- **Downside** — asks "what if the market does worse, or a risk comes true?" Revenue uses conservative assumptions; only essential spend goes ahead; hires are cut or pushed back.

For every scenario, record which assumptions move and by how much. Don't spin up a separate assumption set per scenario; keep the one register and flex specific line items against it.

Each scenario should produce:

- a projected income statement, both annual and monthly
- the projected headcount path
- key metrics side by side — margins, revenue growth, cash runway, and burn rate
- decision triggers: the conditions under which the organization would switch from executing the Base plan to the Upside or Downside plan

## 5. Test sensitivity

Find the assumptions that move the bottom line most and see how far they stretch.

**Tornado analysis.** Swing each key assumption by a set amount (for example ±10%) and work out what that does to the budget:

```
DRIVER SWING TEST
| Driver | As budgeted | Swung down (−10%) | Swung up (+10%) | Impact range in $ |
|--------|-------------|-------------------|-----------------|-------------------|
| Revenue growth | X% | X − 10% | X + 10% | $[min] … $[max] |
| Added headcount | N | N − 10% | N + 10% | $[min] … $[max] |
| Pay rates | $X | $X − 10% | $X + 10% | $[min] … $[max] |
| [further material driver] | [budgeted figure] | [down] | [up] | $[min] … $[max] |
```

Order the assumptions by impact range. The ones with the widest spread pose the greatest risk to the budget's accuracy.

**Break-even analysis.** For each important target — turning a profit, reaching positive cash flow, hitting a particular margin — work out which combination of assumption changes would make the target slip out of reach.

## 6. Package it for approval

**One-page executive summary**
- Total revenue, total expense, and net income/loss under every scenario
- A summary of the headcount plan
- The three biggest opportunities and the three biggest risks
- The key assumptions carrying the most uncertainty
- How the budget compares with prior-year actuals and the prior-year budget

**Full package**
- A base-case P&L for each department, month by month
- The headcount plan, broken down by department and role
- The complete assumption register
- A table comparing the scenarios
- The output of the sensitivity analysis
- The capex plan
- Projected cash flow

**Sign-off sequence**
1. Department owners confirm their own sections.
2. FP&A checks the assumptions and consistency across departments.
3. The CFO reviews the consolidated budget.
4. The executive team approves.
5. The board reviews and approves (annual budgets).

Track approval status section by section. Until every section is approved, the budget is not final.

## Deliverable: budget summary

```
[Legal entity] — budget for [fiscal year or period]
Version: [draft number, or final]   ·   Prepared on: [date]

A. Headline view by scenario
| Metric                  | Base | Upside | Downside | Last year (actual) |
|-------------------------|------|--------|----------|--------------------|
| Revenue                 | $    | $      | $        | $                  |
| Gross Profit            | $    | $      | $        | $                  |
| Operating Expenses      | $    | $      | $        | $                  |
| Net Income              | $    | $      | $        | $                  |
| Headcount at year end   | #    | #      | #        | #                  |
| Gross Margin            | %    | %      | %        | %                  |
| Operating Margin        | %    | %      | %        | %                  |

B. Assumptions that drive the plan
[The 5–10 most important register entries, each shown with its basis and sensitivity]

C. Base case, month by month (P&L)
| P&L line     | Jan | Feb | Mar | … | Dec | Full year |
|--------------|-----|-----|-----|---|-----|-----------|
| Revenue      | $   | $   | $   | … | $   | $         |
| [remaining P&L lines] |     |     |     |   |     |           |
| Net Income   | $   | $   | $   | … | $   | $         |

D. Sensitivity
[Inputs for the tornado chart: the five drivers whose impact range is widest]

E. Risks and opportunities
| # | Risk or opportunity? | What it is | $ effect on the scenario | How we mitigate it / capture it |
|---|----------------------|------------|--------------------------|---------------------------------|
| 1 | Risk        | [what could go worse]  | $[effect] | [mitigation]        |
| 2 | Opportunity | [what could go better] | $[effect] | [how to capture it] |

F. Sign-off status
| Part of the plan    | Approver  | Pending or approved? | Date   |
|---------------------|-----------|----------------------|--------|
| Revenue             | [who]     | [pending / approved] | [date] |
| Headcount           | [who]     | [pending / approved] | [date] |
| Operating expenses  | [who]     | [pending / approved] | [date] |
| Capital expenditure | [who]     | [pending / approved] | [date] |
| Consolidated budget | CFO       | [pending / approved] | [date] |
```

## Ground rules

- **Don't make up inputs.** If something is missing, mark it "[Awaiting input — placeholder only]"; never plug the hole with an estimate of your own.
- **Don't quote market benchmarks.** Every growth rate, margin target, and cost benchmark has to be supplied by the organization; training data is never a source for them.
- **Don't approve assumptions.** Your role is to document and structure them; validating them belongs to management.
- **Tag where each figure comes from**, using exactly one of four labels: `[Source: department submission]`, `[Source: leadership target]`, `[Source: derived from the assumptions]`, or `[Source: placeholder — input still missing]`.

## Tailoring to the organization

Organizations can adjust these areas:

- **Budgeting method:** the default is driver-based. For zero-based budgeting (ZBB), add a step that justifies each line item from zero; for incremental budgeting, start from prior-year actuals and apply increases or decreases.
- **Planning calendar:** lay out the organization's budget cycle, from kickoff through department submissions, consolidation, and review rounds to board approval.
- **Scenario names and definitions:** rename the three cases to fit the industry, for example "bear/base/bull" for a financial services firm or "recession/stable/growth" for a cyclical business.
- **Approval hierarchy:** set out the specific approval chain and the materiality thresholds that trigger additional approvals.
- **Reforecasting cadence:** where the organization runs rolling forecasts, set how frequently the budget gets refreshed and which assumptions are revisited each time.

Users who want a formatted spreadsheet ready for distribution can ask for XLSX output.
