---
name: orphex-budget-change-proposal
description: "Quantify a proposed change to campaign or portfolio budget totals, with assumptions and approval scope; use the reallocator when the total must remain fixed."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Budget Change Proposal

Prepare a decision-ready proposal from budgets, performance exports, and planning documents supplied by the user. Orphex MCP may be used when it is already available and the user has authorized that data access; it is optional. A proposal is not permission to change an advertising account.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `scorecards.read` for targets and pace, `controller.catalog` then `controller.fetch` at level `campaign` for spend, budget, outcomes and lost impression share, and `causal.latest_summary` for any measured lift. If `playbook.catalog` lists the lost-impression-share budget playbook, run it with `playbook.run`. Then list guides with `skill_catalog` (kind `guide`, topic `budget`, then `pacing`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Build the proposal

First identify the scope: account or portfolio, campaigns or other budget units, budget type (daily, lifetime, or total), currency, current limits, proposed effective dates, and the user's spend or performance constraint. If a material field is missing, label the assumption or ask for the missing input before presenting a precise change.

Use like-for-like evidence. Check reporting dates and account timezone, attribution window, conversion definition, currency, and whether the input is spend, budget cap, or both. A budget cap is not a spend forecast: delivery may underspend or exceed a daily amount under the platform's pacing rules. Keep revenue and conversion comparisons aligned to the same attribution basis where possible.

Keep configured budget capacity separate from served cost, billed cost, and incremental cost. Multiply a daily budget delta by days only for an explicitly supplied or clearly labeled hypothetical unchanged-budget horizon; call the result a nominal configured-capacity scenario, never a maximum additional spend. Do not reuse conversion lag or a historical reporting window as the proposal's effective horizon. An actual cost ceiling requires applicable enforceable budget/billing rules and timing; an incremental-cost bound also requires justified counterfactual spend or utilization. The difference between configured ceilings alone does not bound incremental cost. When that evidence is absent, state that actual spend and incremental cost are unknown while retaining the exact current, proposed, and delta budget arithmetic.

For each proposed change, show the current value, proposed value, absolute delta, percentage delta, currency or unit, and effective period. Reconcile portfolio totals before and after. Explain whether the proposal reallocates a fixed amount or increases total exposure. Round only to the platform's stated unit and show the rounding.

Support each recommendation with the supplied marginal evidence, such as recent cost per qualified lead, incremental return, volume, or pacing. Do not assume that adding budget will preserve average efficiency. Average CPA or ROAS does not establish marginal CPA or ROAS. Treat small samples, delayed conversions, mixed objectives, missing spend, and unsettled attribution as limits. If the supplied evidence cannot support a numerical forecast, present a directional hypothesis and the data needed to estimate it.

Rank the proposed changes by expected value and risk. Include a stop or review condition that can be measured, an observation window long enough for the stated conversion lag, and a rollback value. Distinguish an operational guardrail from a predicted outcome.

## Keep account changes authorized

Default to preparing a proposal only. Do not change budgets, bids, campaign status, pacing, or account configuration merely because a proposed change appears in the analysis or an MCP tool is available.

If the user separately asks to apply a change, confirm that their instruction clearly covers the exact account, campaign or budget unit, current and new values, currency, effective time, and any requested stop condition. When any of those details are ambiguous, ask before acting. Use a write-capable tool only if it is available in the current environment and its own authorization rules allow the operation. Report the exact requested and completed changes after an authorized mutation; if no such tool is available, provide the proposal without claiming execution.

## Recommended output

Start with the decision requested and the total portfolio impact. Follow with a table of each change, its evidence, and its key uncertainty. Then state the assumptions, risks, monitoring condition, rollback value, and whether the result is proposal-only or was applied under explicit authorization.
## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
