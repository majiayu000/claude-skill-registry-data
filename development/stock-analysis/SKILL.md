---
name: stock-analysis
description: Generate A-share individual stock fundamental and industrial-chain research reports from a stock code using the reviewed stock-analysis source tree. Use when the user explicitly asks for A-share stock code analysis, 个股分析, 股票基本面分析, 股票研究报告, A股研报, HTML stock report generation, or A股产业链卡脖子/龙头买入逻辑. Do not use for global non-mainland-A-share leader screens.
license: MIT
source: https://github.com/mingli30119/stock-analysis
source_path: ~/.hermes/external-repos/stock-analysis
security_review: medium
---

# Stock Analysis

Use this skill to generate an A-share individual stock fundamental analysis report from a stock code. When the prompt asks for 产业链, 卡脖子, 龙头, 买入逻辑, or AI-era suppliers, include the chokepoint lens below instead of producing a generic valuation-only report. If the user asks for 全球股/全球产业链 and says to exclude mainland A-shares, route away from this skill.

## Scope

- Source root: `~/.hermes/external-repos/stock-analysis`.
- Runtime data collector: `stock_full_report.py`.
- Data source: AkShare public market/financial endpoints.
- Output convention: write results under the current project's `output/` directory unless the user names another destination.
- The report is for research only and is not investment advice.

## Safety Rules

- Do not install Python dependencies globally unless the user explicitly asks. Prefer a project-local virtual environment.
- Do not create or edit MCP configs or store API keys unless the user explicitly asks.
- Treat live market/news/financial fetches as external network calls; run them only when the user asks for an actual report.
- If the user only asks for routing or install, do not fetch stock data.

## Workflow

1. Confirm the stock code is a six-digit A-share code or infer it only when the name is unambiguous.
2. From a project/work directory, prepare dependencies if needed:

```bash
. ~/.hermes/skills/data-science/stock-analysis/.venv/bin/activate
```

3. Run Phase 1 data collection:

```bash
~/.hermes/skills/data-science/stock-analysis/.venv/bin/python ~/.hermes/external-repos/stock-analysis/stock_full_report.py <股票代码>
```

4. Read `output/data_<股票代码>.json`.
5. Draft the Markdown report with the Step 0-8 framework from the upstream skill.
6. If HTML is requested, use the upstream `shared/` assets and `examples/个股研究-中国长城.html` as visual reference; write the final HTML under `output/`.

## Chokepoint / 产业链 Mode

Use this mode when the user asks from demand waves, AI产业链, 卡脖子, 龙头, 买入逻辑, 前瞻TAM, qualification cycle, 垄断, 功能性独占, or 价值链向上爬.

Output contract:
- First line: only the A-share leader ticker/name when the user explicitly asks for A-share leaders.
- Do not mix mainland A-share leaders into a global-stock leader answer unless the user explicitly asks for A-shares.
- Put all reasoning, caveats, valuation, and buy logic after the first line.

Frame the thesis from demand backward:
- Demand wave: what secular demand shock is forcing a new architecture or capacity bottleneck?
- Architecture bottleneck: which physical/process/material function becomes scarce?
- Cannot be designed away: why customers cannot easily bypass it through redesign, second source, software substitution, or vertical integration.
- Material revenue: how the company can convert the bottleneck into revenue large enough to matter.
- Qualification cycle: evidence from certification, customer qualification, platform inclusion, long-term orders, capacity reservation, or process/tool approval.
- Early/small preference: prefer smaller or earlier-stage names only after the chokepoint filter passes.

Use this scoring formula as the ranking spine:

```text
excess return =
  major demand trend
  × insufficient supply elasticity
  × low market recognition
  × catalyst
  - valuation / liquidity / dilution / geopolitical risk
```

Do not let current-period financials dominate when the user's thesis is explicitly qualification-cycle / forward-TAM based. Still name thesis-break conditions: design-out evidence, failed qualification, revenue not scaling after the expected cycle, dilution, customer loss, or policy/geopolitical block.

## IBKR/TWS API fallback for US/global watchlists

When the user explicitly requires IBKR/TWS API data (for example port `4002`) and the Python `ibapi`/`ib_insync` packages are unavailable, use the raw TWS socket protocol rather than silently switching providers:

- Connect to `127.0.0.1:<port>` and send the v100 handshake.
- Send `START_API` (`71`) before any request.
- Use `reqMatchingSymbols` (`81`) to resolve symbols to IBKR contracts/conIds.
- Use delayed market data when subscriptions block live data: `REQ_MARKET_DATA_TYPE` (`59`) with type `3`.
- Use `REQ_MKT_DATA` (`1`) with message version `11` for stock quotes.
- Treat `10167 Requested market data is not subscribed. Displaying delayed market data...` as a valid delayed-data status, not a hard failure.

Reference: `references/ibkr-tws-raw-api.md`.
Reusable probe: `scripts/ibkr_tws_raw_probe.py`.

## First Probe

```bash
~/.hermes/skills/data-science/stock-analysis/.venv/bin/python ~/.hermes/external-repos/stock-analysis/stock_full_report.py 000001 --max-kline-years 1
```
