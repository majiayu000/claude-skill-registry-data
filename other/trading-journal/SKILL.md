---
name: trading-journal
description: Use when writing desk notes, monitor logs, morning plans/scans, powerhour preps, or X/Twitter buzz reports for Jason's live trading — covers naming conventions and where notes go now (Obsidian first).
---

## Where notes go now — Obsidian first

As of 2026-08-22, write new trading/desk notes into the Obsidian vault at
`C:\Users\bottl\Documents\Obsidian Vault\Trading\` (an `obsidian` MCP server is connected, filesystem-
scoped to that vault — or use Read/Write/Edit with the absolute path). See the `reference-obsidian-vault`
memory for the vault's existing structure (`Trading journal.md`, `Positions.md`, `Research.md`,
`FinancialDevelopment Journal.md`). Do not write new notes into `FinancialDevelopment/trading_journal/`
unless the user asks for the repo copy specifically — that folder was copied into the vault once as a
one-time archive and is not kept in sync.

The repo's `trading_journal/scripts/` (`rh_monitor.py`, `powerhour_prep.py`, `morning_outlook.py`,
`xcom_buzz_scan.py`, etc.) still run and still produce output on their existing cadence — this only
changes *where a note written by hand or by you* ends up, not the scripts themselves.

## Naming conventions (from the archived repo history — same names should be used in the vault)

- **Alerts**: `alerts/ALERT_HHMM_YYYYMMDD.md` — one file per ~10-minute intraday check during market
  hours (e.g. `ALERT_0850_20260818.md`).
- **Daily desk notes**: `YYYY-MM-DD.md` at the journal root, or `desk_note_YYYYMMDD*.md` — free-form
  narrative of what happened and why.
- **Monitors**: `*_monitor*` / `rh_monitor` baselines — position/order state snapshots, not narrative.
- **Morning routine**: `morning_plan_YYYYMMDD.md`, `morning_scan_YYYY-MM-DD.md`,
  `morning_outlook_*.md` — pre-market plan and scan output, one set per trading day.
- **Powerhour**: `powerhour_prep_YYYYMMDD.md`, `powerhour_plan_*`, `powerhour_cron_verify_*` — last-hour
  prep and the cron-verification log for the automation that generates it.
- **X/Twitter buzz**: `x_buzz/LATEST*.md` (always-current per cadence: morning/mid-day/power-hour) plus
  dated snapshots `x_buzz/YYYY-MM-DD_<cadence>.md` — contested-narrative sentiment scans.
- **One-off research**: `<ticker_or_topic>_research_YYYYMMDD.md`, `*_deep_dive_YYYYMMDD.md` — ad hoc
  investigation notes, not part of a recurring cadence.

## Relation to other skills

- [[robinhood]] — monitors/fills notes summarize what `mcp__robinhood__*` calls show; don't duplicate
  raw API output into a note, summarize the decision-relevant parts.
- [[trading-mode]] — an active trade-hunt session; its output (trade ideas, sizing) is a natural desk-note
  candidate once acted on.
