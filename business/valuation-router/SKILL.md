---
name: valuation-router
description: Use this skill to classify a public company by economic characteristics and select primary, cross-check, downside, implied-expectation, and overlay valuation models. Trigger for stock analysis, intrinsic value estimates, model selection, company-type routing, peer comparisons, or questions like which valuation method fits this business.
---

# Valuation Router Skill 

## Purpose

Select primary, cross-check, downside, implied-expectation, and overlay-specific valuation models by classifying the company through economic characteristics, not by company name alone.

## Trigger Examples

- "Which valuation model should I use for UNH / NVDA / AAPL?"
- "Classify this company before running valuation."
- "Compare AAPL, GOOGL, and AMZN as quality compounders."
- "Is this a bank, compounder, managed care company, platform, REIT, or cyclical?"

## Inputs

- Target company / ticker
- Market
- Industry
- Business segments
- Revenue / earnings / cash-flow profile
- ROE / ROIC and capital intensity
- Dividend, buyback, share cancellation, and debt reduction history
- Segment disclosure for technology-related businesses
- Cyclicality exposures
- Available data and freshness status
- Structured assumptions and evidence for material forecast, normalization, multiple, discount, probability, or recovery inputs
- User requested depth
- Prior assumptions, if any

## Required Inputs

Minimum usable routing requires target name or ticker plus at least one of: industry, business description, segment profile, revenue / earnings / cash-flow profile, or explicit user-provided classification clues.

If the request is current and valuation/action guidance will follow, current price, latest filing period, and freshness status should be supplied or marked missing.

## Outputs

- Base Business Type
- Overlay Tags
- Structured valuation model stack
- Missing data / blocked models
- Assumption confidence and blocked / low-confidence assumption items
- Confidence level
- Next required action

## Blocking Behavior

Do not invent company type from ticker alone when evidence is missing. If classification evidence is insufficient, return:

```text
Valuation Routing Blocked:
- Missing company / industry evidence:
- Models that cannot be selected:
- Minimum data needed:
```

If only partial classification is possible, return a low-confidence route and defer non-material overlays.

## Script Mapping

- Routing implementation: `scripts/routing/select_valuation_models.py`
- Unified execution handoff: `scripts/valuation/valuation_executor.py`
- Structured assumption policy: `references/valuation_rules/structured_assumption_policy.md`
- Specialist routes: `references/valuation_rules/specialized_company_routes_v17.md`

## Company Classification Flow

### Step 1: Base Type

Classify as **Mature Quality Compounder** if the company has mature operations, stable earnings, durable FCF conversion, above-industry ROE / ROIC, and a defensible competitive position.

Default models:

- Primary: Owner Earnings DCF / FCFE DCF
- Cross-check: EPV / Quality-adjusted P/E / Normalized P/E
- Downside: No-growth EPV
- Implied: Reverse DCF

### Step 2: Dividend / Shareholder Return Overlay

Add this overlay when the company has meaningful dividends, buybacks, share cancellation, or debt reduction that are supported by owner earnings / FCFE and balance-sheet strength.

Additional models / checks:

- Two-stage DDM
- Gordon Growth terminal check
- Dividend Yield Band
- Dividend Yield + Net Buyback Yield + Debt Reduction Yield
- Dividend Safety / payout stress test
- Implied Dividend Growth

If dividend coverage is weak, do not use DDM as valuation support; treat it as a risk flag.

### Step 3: Technology Optionality Overlay

Add this overlay when technology-related businesses are financially visible, commercially monetized, and potentially material.

Technology treatment:

- Efficiency-only technology: reflect in margin, ROIC, FCF conversion, and moat quality.
- Separable monetized segment: use SOTP or scenario-weighted optionality.
- Narrative-only technology: no separate valuation premium.

### Step 4: Light Cyclical Manufacturing Overlay

Add this overlay when the company is exposed to real estate, consumer cycle, raw material prices, exports, FX, channel inventory, or manufacturing capex cycles.

Additional models / checks:

- Mid-cycle earnings
- Normalized margin
- Stress-case FCF
- No-growth EPV

## Scoring Rubric

The router may use internal 0 / 1 / 2 scoring.

### Mature Quality Compounder Score

- Stable revenue and earnings
- Strong ROE / ROIC
- Durable FCF conversion
- Competitive advantage
- Mature but positive growth

If score >= 7, classify as Mature Quality Compounder.

### Dividend / Shareholder Return Score

- Stable dividend history
- Reasonable payout ratio
- Dividend covered by FCF / FCFE
- Buyback, share cancellation, or debt reduction
- Balance sheet supports payout

If score >= 6, add Dividend / Shareholder Return Overlay.

### Technology Optionality Score

- Technology-related segment exists
- Segment revenue is disclosed
- Segment growth is above core business
- Segment has profit or credible margin path
- Technology can improve ROIC, margin, or TAM

If score >= 6, add Technology Optionality Overlay.

If score <= 3, treat technology as narrative-only and do not assign separate valuation premium.

### Cyclicality Score

- Real estate / consumption cycle exposure
- Raw material exposure
- FX / export exposure
- Inventory or manufacturing cycle exposure

If score >= 4, add Light Cyclical Manufacturing Overlay.

## Reverse DCF Execution Gate

When Reverse DCF is selected as the implied-expectation model, the downstream workflow must call `skills/reverse-dcf/SKILL.md`.

The final report must include either:

1. A Reverse DCF result, or
2. A Reverse DCF blocked section.

It is not valid to only mention Reverse DCF as a suggested next step.

## User-facing Output Rules

Default output should show:

- Company classification result
- Overlay tags
- Selected valuation model stack
- Missing data / blocked models
- Confidence level
- Investment implication

Default output must not show:

- Internal score-by-score details
- Full formulas
- Spreadsheet-style valuation calculations
- Discounting schedules
- Derived metric tables

Calculation detail is allowed only when the user explicitly requests audit, debug, appendix, formulas, or workbook-style detail.

## General Rules

- State assumptions explicitly.
- Convert material assumptions into structured, evidence-constrained inputs before relying on valuation output.
- Flag missing or low-confidence data.
- Prefer conservative assumptions.
- Keep output auditable.
- Never use a single valuation multiple as the full valuation conclusion.


## v17 Token-Efficient Specialist Route Expansion

The valuation router supports specialist company routes but must lazy-load them.

Default procedure:

1. Run compact classification.
2. Select exactly one base route.
3. Add at most two overlays for L0/L1.
4. Load only the selected route section from `references/valuation_rules/specialized_company_routes_v17.md` when needed.
5. Defer non-material routes and list them briefly.
6. Do not expose internal scorecards or step-by-step valuation calculations by default.

Specialist routes include AI / semiconductor, digital platform, cloud platform, managed care, insurance-float holding company, financial institutions, SaaS, pharma, commodity cyclicals, REIT/infrastructure, and auto/EV platforms.


## v17.1 Modular Workflow Quality Gate

The router now selects workflows as well as valuation models. Default behavior:

1. Select one primary workflow.
2. Add at most two auxiliary workflows for L0/L1.
3. Load `references/core/investment_philosophy_layer.md` and `references/core/investment_quality_gate.md` before final output.
4. Keep domain-specific workflow details out of the main prompt unless selected.
5. Do not expose internal scorecards, workflow internals, quality-gate internals, or valuation calculation traces unless explicitly requested.

Final output must include business quality, valuation attractiveness, margin of safety, data confidence, and action.


##  Fixed Output Contract

The router must return routing and model-selection fields to the renderer. It must not write a custom final report.

Default output must include these user-facing valuation/action fields through the fixed renderer:

- selected valuation model stack
- Bear / Base / Bull intrinsic value range, or blocked status
- current price, or blocked status
- margin of safety, or blocked status
- price zones
- position-aware suggestions for empty, half, full, and overweight investors
- tranche plan
- add / hold / trim / exit conditions

If valuation range is unavailable, report the valuation and price/action framework as blocked with missing data. Do not drop these sections.
