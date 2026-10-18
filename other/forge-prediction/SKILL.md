---
name: forge-prediction
description: "Forge: prediction, sports-data, and betting analysis (incl. Telegram tips): forecast, odds, value bet, backtest, confidence label — NO real-money betting."
---

# Forge playbook — Prediction / sports-data

## Hard rules
- **Never claim certainty.** Every output carries a confidence/risk label.
- **No automatic real-money betting / no auto-stake code path.**
- Backtest before trusting any model; show sample size.
- Verify data-source quality; track all assumptions.
- Telegram token in env only; one message format, tested.

## Team (conditional)
Lead: `mle-reviewer` + `planner`. Specialists: `mle-reviewer`, `python-reviewer`, `silent-failure-hunter` (data gaps look like clean zeros), `database-reviewer` (data store).

## Skills / commands / MCP
`systematic-debugging`, `/test-coverage`. For delivery, defer to `forge-n8n` or a Telegram layer (Telegram bots fold in here).

## Fan-out & flow
L3.
**Parallel:** data ingestion ∥ model/stat logic ∥ delivery formatting.
**Serial:** ingest → backtest → value/odds calc → uncertainty labeling → delivery.

## Domain gates
Data sources + quality verified; statistical logic reviewed; backtesting done; odds/value checked; confidence/risk labels on every output; assumptions documented; data freshness check.

## Ship-readiness (unique)
Backtest results shown with sample size; every output labeled with confidence/risk; assumptions + data-quality notes attached; **no auto-bet path**; Telegram message format tested. The `ship-readiness` prediction + Telegram checklists are advisory; optionally run `codex-reviewer` (Codex) on important code — not a blocker.
