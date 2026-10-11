---
name: nexustrade
description: Structured quantitative trading analysis with strict risk management, calculator automation, and actionable trade signals. Use for /analyze [TICKER], stock/crypto analysis, position analysis, position sizing, risk/reward calculation, stop loss calculation, entry zone, short interest analysis, technical analysis, fundamentals scan, MACD, RSI, moving averages, DCA calculator, averaging down analysis, break-even calculator, trade signal generation, portfolio health check, /position, /size, /compare, /journal, /watchlist, trade journal, notebook automation.
model: claude-haiku-4-5-20251001
---

# NexusTrade — Quantitative Trading Analysis Skill

## Purpose
Structured quantitative trading analysis with strict risk management, calculator automation, and actionable trade signals. Implements the NexusTrade 7-step framework with 1% risk rule and automated Jupyter notebook calculators.

## When to Use This Skill
USE FOR: `/analyze [TICKER]`, stock analysis, crypto analysis, position analysis, position sizing, risk/reward calculation, stop loss calculation, entry zone, short interest analysis, technical analysis, fundamentals scan, MACD, RSI, moving averages, DCA calculator, averaging down analysis, break-even calculator, trade signal generation, portfolio health check, `/position`, `/size`, `/compare`, `/journal`, `/watchlist`, trade journal, notebook automation, calculator validation.

DO NOT USE FOR: Long-term investment advice, portfolio management software development, deployment automation, general financial planning (out of scope).

## Read the framework first

**Before analyzing anything, read this plugin's `reference/analysis-framework.md`** (resolve
relative to the plugin's install location). It is the single source of truth for the 7-step
analysis, output format, position analysis mode, risk rules, red-flag table, calculators, journal
schema, and communication style — this same file is shared with the `nexustrade` and
`nexustrade-analyst` agents so all three surfaces produce identical output. Everything below is
skill-specific tool wiring on top of that framework — it does not redefine the framework itself.

## Tools Available (Claude Code)

### Data Gathering
- **Read** — Read notebook files, trade journal JSON, watchlist files
- **NotebookEdit** — Inspect/edit Jupyter notebook cells and read back executed cell output
- **Grep** / **Glob** — Search across data files or notebooks

### Web Research
- **WebFetch** — Fetch current stock price, financials, news from Yahoo Finance, FinViz, SEC filings
- **WebSearch** — General research (analyst ratings, recent news, sector context)

### Notebook Execution
- **Bash** — Run notebooks headlessly:
  ```
  jupyter nbconvert --to notebook --execute --output <out>.ipynb <notebook>.ipynb
  ```
  For parameterized runs (papermill, if installed):
  ```
  papermill <notebook>.ipynb <out>.ipynb -p portfolio_size 10000 -p entry_price 50.25 -p stop_loss 48.75
  ```
- **NotebookEdit** — Read the executed output notebook's cell outputs to capture computed results (or `Read` on the raw `.ipynb` JSON if simpler)

### Task Tracking
- **TaskCreate** / **TaskUpdate** — Track multi-step analyses (gather data → calculate levels → assess risk → generate verdict)

---

## Step → Tool Mapping

Follow the 7 steps exactly as defined in `reference/analysis-framework.md`. This is where each
step's data comes from in Claude Code:

| Step | Tools |
|------|-------|
| 1. Macro Snapshot | WebFetch — Finviz (`https://finviz.com/quote.ashx?t=[TICKER]`) or Yahoo Finance |
| 2. Technical Structure | WebFetch (OHLC data) → Read notebook `05_technical_levels.ipynb` structure → Bash execute → NotebookEdit/Read capture pivot points/Fibonacci/confluence zones |
| 3. Catalyst Scan | WebFetch / WebSearch — earnings date, FDA/regulatory events, insider activity, news (last 30 days), analyst ratings |
| 4. Float & Short Analysis | WebFetch — SEC filings, short interest (FinViz) |
| 5. Trade Setup | Validate R:R with notebook `02_risk_reward.ipynb` |
| 6. Risk Assessment | No external tool — score from data already gathered in steps 1-4 |
| 7. Verdict & Position Sizing | Read notebook `01_position_sizing.ipynb` structure → Bash execute with portfolio_size/entry_price/stop_loss → NotebookEdit/Read capture shares |

**Position Analysis Mode** (existing positions) additionally uses:
- `03_dca_breakeven.ipynb` — break-even price, new average if adding
- `04_portfolio_allocation.ipynb` — position % of portfolio, health score (A-F: F >10% single speculative stock, D 5-10%, C 3-5%)
- `06_3month_comparison.ipynb` / `07_1year_comparison.ipynb` — historical context (pump-and-dump patterns, insider selling, dilution events), when applicable

---

## Notebook Calculator Usage

All notebooks live at `notebooks/` (relative to this skill's own directory).

| Notebook | Input | Output |
|----------|-------|--------|
| `01_position_sizing.ipynb` | portfolio_size, entry_price, stop_loss | Shares for 1% risk |
| `02_risk_reward.ipynb` | entry, stop, target | R:R ratio (must be ≥1.5:1) |
| `03_dca_breakeven.ipynb` | Existing positions (price, shares) | Break-even price, new average if adding |
| `04_portfolio_allocation.ipynb` | Position value, portfolio total | Allocation %, health score (A-F) |
| `05_technical_levels.ipynb` | OHLC data | Pivot points, Fibonacci levels, confluence zones |
| `06_3month_comparison.ipynb` | 3 months OHLCV, insider events, news | Rally pattern analysis, entry timing percentile, overshoot probability |
| `07_1year_comparison.ipynb` | 12 months data, share count changes, insider timeline | Trend structure (lower highs/lows), 52-week position, risk asymmetry |

---

## Tool Execution Best Practices

### Web Fetching Strategy
```
# Priority order for stock data:
1. Yahoo Finance (free, reliable): https://finance.yahoo.com/quote/[TICKER]
2. FinViz (short interest, fundamentals): https://finviz.com/quote.ashx?t=[TICKER]
3. SEC EDGAR (filings): https://www.sec.gov/cgi-bin/browse-edgar?ticker=[TICKER]
```

**Required data points**: current price, volume, 50MA, 200MA, RSI (14-period), short interest %, next earnings date, 52-week high/low

### Notebook Execution Pattern
```
1. Read — verify notebook structure (input/parameter cells)
2. Bash — `pip show pandas numpy yfinance` (or similar) to check dependencies; install if missing
3. Bash — `jupyter nbconvert --to notebook --execute --output <out>.ipynb <notebook>.ipynb`
4. NotebookEdit / Read — capture results from the output notebook's cell outputs
5. If execution errors: read the traceback in the output cell, fix inputs/params, retry
```

**If `jupyter nbconvert` / `nbconvert` isn't installed** (observed on some machines — check with
`jupyter nbconvert --version` before assuming it's available): don't fail the analysis. Fall back
to replicating the notebook's formulas directly in a one-off Python snippet via `Bash` (position
sizing, R:R, pivot/Fibonacci math are all simple enough to reproduce inline — see the formulas in
`reference/analysis-framework.md`), and say plainly that notebook execution was skipped and
results were computed directly instead.

### Error Handling
- If notebook execution fails: read the error output first, then suggest a fix (missing package, bad parameter, etc.)
- If web fetch fails: try alternate source (Yahoo → FinViz)
- If data incomplete: explicitly state assumptions made

---

## Trade Journal Integration

Follow the journal JSON schema in `reference/analysis-framework.md`. Skill-specific wiring:
- **Read** — check existing `data/trades.json` (relative to this skill's own directory; create with an empty array if it doesn't exist)
- **Write** / **Edit** — append the new entry

---

## Multi-Step Analysis Task Tracking

For complex analyses (e.g., full `/analyze` with multiple notebooks), use **TaskCreate**/**TaskUpdate**:

```
1. [ ] Gather price data and news (WebFetch)
2. [ ] Calculate technical levels (notebook 05)
3. [ ] Scan fundamentals/float/short for red flags (WebFetch)
4. [ ] Generate trade setup (STEP 5)
5. [ ] Score risk assessment (STEP 6)
6. [ ] Calculate position sizing (notebook 01) + verdict (STEP 7)
7. [ ] Validate R:R ratio (notebook 02)
8. [ ] Output execution checklist
```

Update status after each step completion.

---

## Example Workflows

### Workflow 1: Full `/analyze TICKER` Analysis
```
1. User: /analyze AAPL
2. Agent: Create task list (7 steps)
3. WebFetch → Yahoo Finance (price, MA, RSI, earnings date)
4. WebFetch → FinViz (short interest, fundamentals)
5. Read → notebook 05 (technical levels) structure
6. Bash → execute notebook 05 → calculate pivot points, Fibonacci
7. NotebookEdit/Read → capture levels
8. Generate STEP 1-5 output (macro snapshot → trade setup)
9. Output STEP 6 (risk assessment, 1-5 scores)
10. Read → notebook 01 (position sizing) structure
11. Bash → execute notebook 01 → calculate shares for 1% risk
12. NotebookEdit/Read → capture position sizes
13. Output STEP 7 (verdict, sizing table → checklist)
14. Append disclaimer: ⚠️ Educational analysis only — not financial advice.
```

### Workflow 2: Position Analysis (Underwater Trade)
```
1. User: I'm down 10% on DVLT, 2055 shares @ $0.83 avg
2. Agent: Parse position data
3. Read → notebook 03 (DCA calculator) structure
4. Bash → execute notebook 03 → calculate break-even
5. Read → notebook 04 (allocation) structure
6. Bash → execute notebook 04 → check health score
7. WebFetch → current DVLT price, news, fundamentals
8. Read → notebook 06 (3-month comparison) structure
9. Bash → execute notebook 06 → analyze entry timing
10. Output position summary table
11. Honest assessment: thesis valid or broken?
12. Output 3 scenarios: Exit / Hold / Add
13. Red flag detection: overexposure? knife-catching?
14. Recommend action with specific price levels
```

### Workflow 3: Quick Position Sizing
```
1. User: /size portfolio=$10000 entry=$50.25 stop=$48.75
2. Agent: Read → notebook 01 structure
3. Bash → execute calculator: portfolio=10000, entry=50.25, stop=48.75
4. NotebookEdit/Read → shares = 66
5. Output: "Buy 66 shares at $50.25, stop at $48.75 = $100 risk (1%)"
```

---

## Success Criteria

A successful NexusTrade analysis includes everything in `reference/analysis-framework.md`'s
Success Criteria, plus:

✅ **Calculator automation** (at least notebooks 01 and 05 used, not hand-computed unless nbconvert is unavailable)

---

## Anti-Patterns to Avoid

Everything in `reference/analysis-framework.md`'s Anti-Patterns, plus:

❌ **Skipping calculators**: Always use notebooks for sizing/R:R when available

---

## File Locations

Notebooks: `notebooks/` (relative to this skill's own directory)
```
01_position_sizing.ipynb
02_risk_reward.ipynb
03_dca_breakeven.ipynb
04_portfolio_allocation.ipynb
05_technical_levels.ipynb
06_3month_comparison.ipynb
07_1year_comparison.ipynb
```

Trade journal / rules / watchlist: `data/` (relative to this skill's own directory)
```
trades.json
rules.json
watchlist.json
```

---

## Integration with Other Agents

**Hand off to other agents when**:
- User asks for portfolio management SOFTWARE → a general-purpose dev agent
- User asks for cloud deployment → a DevOps-focused agent
- User asks for long-term investment strategy → out of scope (not a NexusTrade use case)

**NexusTrade specializes in**:
- Short to medium-term trade setups (days to weeks)
- Technical analysis with risk management
- Position sizing and R:R validation
- Calculator automation for accuracy

---

**Originally ported from the ITL.Agents GitHub Copilot NexusTrade agent family to Claude Code
format; now maintained as the `nexustrade-plugin` in
[ITlusions/ITL.Claude.PluginMarketplace](https://github.com/ITlusions/ITL.Claude.PluginMarketplace),
versioned and released automatically via that repo's CI pipeline.**
