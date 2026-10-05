---
name: value-investing-research
description: Use this skill whenever the user asks about public-stock or listed-company investment analysis, intrinsic value, margin of safety, valuation model selection, reverse DCF, implied market expectations, data freshness, source checks, orphan numbers, data provenance, earnings reviews, thesis updates, relevant company/industry news, risk reviews, or buy/add/hold/trim/sell price zones. It routes company type, gathers public data when possible, runs executable valuation models, audits assumptions and sources, and produces decision-oriented value-investing reports.
---

# Value Investing Core Skill 

## Purpose

Analyze public stocks and listed companies through a value-investing lens. The skill is designed to judge business quality, estimate intrinsic value, check margin of safety, audit data reliability, summarize material company or industry news when it affects the thesis, and translate the conclusion into conditional buy, add, hold, trim, or sell price zones.

The purpose is not to predict near-term price moves. It converts public evidence and structured assumptions into auditable value judgments and action ranges.

This file is the compact entrypoint. Detailed rules live in `references/`, workflows in `workflows/`, and deterministic calculations in `scripts/`.

## Trigger Conditions

Use this skill when the user asks to:

- analyze a public stock, listed company, peer group, industry, or equity investment opportunity
- estimate intrinsic value or margin of safety
- run reverse DCF, DCF, SOTP, EPV, NAV, DDM, residual-income, rNPV, REIT, insurance, cyclical, fintech, or scenario valuation
- build, audit, or explain a valuation model
- generate an investment memo, earnings review, thesis update, risk review, or price/action framework
- summarize material company, sector, regulatory, litigation, product, management, or capital-allocation news when it may change the thesis, catalyst path, risk rating, valuation assumptions, or data freshness
- compare companies or check whether a company type is supported

Do not use this as the primary skill for:

- short-term price prediction, chart patterns, day trading, or technical-analysis-only requests
- options strategy, leverage design, tax planning, legal advice, or broad personal financial planning
- private-company diligence unless the user provides enough source data to support the analysis
- generic macro forecasting unless it directly supports a valuation assumption
- pure news summarization with no connection to a stock thesis, risk review, catalyst, earnings update, or investment decision

If the request is mainly news-oriented, keep the output focused on investment relevance: what happened, why it matters to the thesis, which assumptions or risks changed, and what evidence would confirm or refute the change.

## Progressive Loading Rule

Do not load all references, formulas, workflows, master files, or source materials by default.

Default context pattern:

```text
Request -> Context Manifest -> Router -> One Primary Workflow -> Needed Policies -> Scripts -> Fixed Renderer
```

Read `references/context_policy/token_budget_policy.md` and `references/context_policy/context_manifest.md` first for normal analysis. Use the context manifest as the navigation index.

## L0 / L1 Quick Path

For short checks, sell-zone questions, reverse DCF requests, data-source audits, or thesis updates, do not run the full memo flow unless the user asks for it.

1. Identify the ticker / company, user question, and whether the request is current.
2. Load only the relevant workflow or sub-skill plus the needed policy.
3. Use public data when current price, latest filing, or material news affects the answer.
4. Execute the selected model / audit, or explicitly block it with missing inputs.
5. Return the compact output required by the fixed renderer or the selected sub-skill.

## Non-Overridable Investment Principles

Every stock/company analysis must obey: business quality before valuation; cash-flow reality over accounting appearance; model-company fit; required margin of safety; evidence-backed conclusions; explicit bear case; internal calculation traces by default; data confidence gating action; separate judgment of good business and good price; missing/stale data flagged or blocked; relative valuation considered for public, peer-comparable competitive industries; evidence-based moat assessment for L1+ stock analysis where data is available.

Load for the core philosophy and quality gate:

- `references/core/investment_philosophy_layer.md`
- `references/core/investment_quality_gate.md`
- `references/core/modular_workflow_architecture.md`

## Standard Workflow

For L1/L2 current company analysis:

1. Infer output language from the user's latest request unless explicitly overridden.
2. Classify task depth: L0 quick check, L1 standard report, L2 full memo, L3 committee pack, L4 audit package.
3. Identify target, ticker, market, industry, lifecycle, and likely business type.
4. Use `scripts/context/context_router.py` and `references/context_policy/context_manifest.md` to select the smallest useful context packet.
5. Route to one primary workflow and no more than two auxiliary workflows for L0/L1.
6. Classify the company by evidence, not name alone: base business type plus shareholder-return, technology-optionality, and cyclicality / risk overlays.
7. Route primary, cross-check, downside, implied-expectation / reverse DCF, and material overlay valuation models.
8. Proactively fetch or verify public data that does not require user credentials or files.
9. Convert important inputs into structured assumptions with evidence, confidence, and sensitivity.
10. Bind model inputs to source metadata where possible with `schemas/valuation_input_packet.schema.json`.
11. Run Python valuation scripts instead of expanding formulas in the prompt. Prefer `scripts/valuation/valuation_executor.py` when a routed model execution is possible.
12. Audit assumptions, formulas, data lineage, freshness, and sensitivity internally.
13. Render through the fixed report contract. Workflows must not directly create custom final reports.
14. End the report with optional user-provided data suggestions that would improve assumption quality.

## Public Data Default

For normal L1/L2 analysis, do not wait for user-provided data before doing the public-data version unless the analysis is blocked.

Proactively use or check:

- official filings, annual reports, 10-K / 10-Q, exchange filings, earnings releases, IR pages, presentations, and management guidance
- current price, market capitalization, shares, rates, and FX where material
- public peer, customer, supplier, capex, industry, regulatory, litigation, and news sources where material to the thesis
- public market data helpers such as yfinance / OpenBB only if the runtime has a working connector; otherwise use verifiable web or official sources

Use public-data connectors when possible: `scripts/connectors/public_data_packet_builder.py`, `sec_edgar_connector.py`, `yfinance_connector.py`, `ir_release_parser.py`, and `openbb_provider_config.py`.

Before retrieving financial statements, route the ticker through `scripts/markets/registry.py`. US tickers may use SEC EDGAR companyfacts. A-share tickers such as `000858.SZ` or `600519.SH` must use the CN_A adapter path; if CN_A filing data is unavailable, block current valuation instead of substituting SEC companyfacts or generic WebSearch snippets.

If `yfinance` is missing in the sandbox/runtime, attempt a local sandbox-target install before using Yahoo endpoint fallbacks. Do not replace this with WebSearch prices.

Reflect `sources_used`, `missing_data`, and `errors` in data provenance and optional-data suggestions.

For current valuation, current price must have a same-day market timestamp. If the quote timestamp is missing or from a prior date, block current margin of safety, reverse DCF, and price-zone conclusions until same-day market data is available.

Do not use generic WebSearch snippets, search-result cards, or webpage snapshots as current-price sources unless they include an explicit same-day market timestamp. Undated or timestamp-free page prices are invalid for current valuation and must be marked blocked.

Do not bypass paywalls, store credentials in git, commit paid exports, reproduce long paid-report excerpts, or treat institutional target prices as intrinsic value.

If institutional views are provided, load `skills/institutional-view-ingestion/SKILL.md`, `references/data_source_policy/institutional_view_policy.md`, `schemas/institutional_view.schema.json`, and `scripts/connectors/institutional_view_parser.py`.

## Routing Files

Use these routers and policies when a current stock/company analysis needs classification or valuation model selection:

Core routing files: `workflows/00_router.md`, `skills/valuation-router/SKILL.md`, `references/valuation_rules/company_classification_routing_policy.md`, `token_efficient_routing_policy_v17.md`, `structured_assumption_policy.md`, and `scripts/routing/select_valuation_models.py`.

Use `company_type_coverage_matrix_v17.md` when coverage is uncertain, and `specialized_company_routes_v17.md` only for specialist company types.

Primary workflows: `01_quality_company`, `02_dividend_compounder`, `03_tech_platform`, `04_ai_semiconductor`, `05_healthcare_managed_care`, `06_holding_company`, `07_reit_infrastructure`, `08_cyclical_commodity`, `09_watchlist_compare`, and `10_fintech_brokerage`.

Default L0/L1 route cap:

- one base route
- one primary workflow
- no more than two auxiliary workflows
- one primary model
- one or two cross-check models
- one downside model
- one implied-expectation model
- defer non-material modules instead of expanding them

## Master Lenses

Use `references/masters/multi_master_framework.md` as the index. Load individual files under `references/masters/` only when materially relevant to the selected workflow or explicitly requested.

Default lens mapping: quality / dividend / holding company -> Buffett-Munger, Graham, Greenwald; tech platform -> Buffett-Munger, Fisher, Mauboussin-Rappaport, Damodaran; AI semiconductor -> Fisher, Mauboussin-Rappaport, Howard Marks, Damodaran; cyclical / commodity -> Howard Marks, Graham, Greenwald; action / position overlay -> Jin Jiancheng.

Include a compact `Master Lens Used` section only for lenses that materially affect the analysis.

## Output Contract

Every standard stock/company report must obey:

- `references/output_policy/mandatory_output_contract.md`
- `references/output_policy/workflow_payload_contract.md`
- `references/output_policy/fixed_report_renderer.md`
- `references/output_policy/output_validation_rules.md`

The final report must preserve valuation range, current price, margin of safety, selected models, key assumptions, sensitivity, risks, data provenance, execution gates, and investor action zones when relevant and available.

Preserve moat assessment where material and peer comparison / relative valuation verdict where peer-comparable.

If valuation or market data is missing, keep the affected sections, mark them `Blocked`, explain missing inputs, and provide non-price-based next steps.

Do not show formulas, spreadsheet-style steps, internal scorecards, detailed DCF schedules, or debug traces unless explicitly requested.

## Deterministic Valuation Rule

Assumptions may differ across analysts or model runs, but Python valuation calculations must be deterministic: identical inputs to the same valuation script must produce identical outputs.

Numerical valuation outputs must come from executable Python valuation scripts. If a routed model cannot be executed through scripts, mark it `Blocked` or `Low-confidence`, or clearly label any number as a rough manual estimate that must not drive the final conclusion.

Valuation algorithms must be documented by formula/policy and covered by unit or golden tests. If a formula is not implemented, tested, and suitable for the company type, do not present it as a reliable valuation result.

For formula provenance and confidence status, use `references/valuation_rules/formula_source_registry.json`. Treat `heuristic_helper` entries as supporting calculations only, not standalone high-confidence valuation models.

## Execution Gates

Important modules must be executed or explicitly blocked. If a selected valuation model, reverse DCF, data audit, risk check, or report module cannot run, state:

```text
[Module] Blocked: [missing/stale input and impact]
```

Load when needed:

`references/execution_policy/execution_gate_policy.md`, `references/valuation_rules/reverse_dcf_execution_policy.md`, `skills/execution-gate-auditor/SKILL.md`, and `scripts/audit/execution_gate_audit.py`.

## Data Rules

Every material number must be sourced, derived from sourced inputs, user-provided, or labeled as an assumption. Unsourced numbers must not drive the final conclusion.

Load when needed:

`references/data_source_policy/data_source_policy.md`, `data_freshness_policy.md`, `data_provenance_policy.md`, `scripts/data/check_data_freshness.py`, and `scripts/audit/data_provenance_audit.py`.

For current analysis, state analysis date, market data date, latest financial period, and important missing data. Detailed data-source rules live in the data source policies.

## Investor Action

When the user asks for buy/add/hold/trim/sell guidance, or when a standard stock report is produced, include valuation-based and position-aware action guidance.

Load:

`skills/investor-action-framework/SKILL.md`, `references/action_policy/investor_action_framework.md`, and `scripts/scoring/investor_action_framework.py`.

Use conditional language: consider, wait for, monitor, add only if, trim if, reassess if. Do not give absolute personalized financial advice.

## Optional Presentation Layers

Default final presentation is pyramid-principle structured output through the fixed renderer.

Load `skills/pyramid-summary`, `skills/mindmap-summary`, presentation policies, and presentation scripts only when requested.

## Hard Rules

Always state assumptions, flag missing data, separate good business from good price, include margin of safety and downside risk for valuation work, avoid single-multiple conclusions, avoid loading all sub-skills or master source materials by default, and do not let optional paid/private data block normal public-data L1/L2 analysis.
