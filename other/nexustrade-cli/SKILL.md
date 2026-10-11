---
name: nexustrade-cli
description: Run the NexusTrade monitoring CLI (`nexustrade`) for a stock watchlist - buy-ladder levels and alerts, one-shot price alerts, big-player gainers screen, signal journal, performance ranking, market regime tags, discipline rule check against the live account, MU revenue breakdown, tool inventory. Use for scheduled checks (LADDER ALERT CHECK, PRICE ALERT CHECK, GAINERS CHECK, DAILY LADDER RECOMPUTE, SIGNAL JOURNAL UPDATE), "how did X perform", "what regime are we in" and "am I within my rules" questions. READ-ONLY, never places orders.
---

# nexustrade CLI

Read-only wrapper over the official `webull-cli` binary. It never places, modifies or cancels an order. Do not use any other Webull client.

## Install and run

The package is NOT bundled with this plugin. It lives in the user's own `nexustrade-cli` folder (a Python package named `nexustrade`).

```
pip install -e <path-to>/nexustrade-cli         # once; add [charts] for matplotlib
nexustrade <command>                            # or: python -m nexustrade <command>
```

Environment:
- `NEXUSTRADE_HOME` - folder with `config.json`, `levels.json`, `state.json`, `price_alerts*.json`, `journal.jsonl`. Default `~/.nexustrade`. Point it at an existing scripts folder to share state with legacy scripts.
- `WEBULL_CLI` - path to the webull binary. Default `%USERPROFILE%\.webull\webull-cli.exe`.

Run `nexustrade status` first if unsure what exists.

## Commands

| Command | Use | Writes state |
|---|---|---|
| `ladder check` | LADDER ALERT CHECK. Prints triggered rungs or "NO NEW TRIGGERS" | yes |
| `ladder recompute` | DAILY LADDER RECOMPUTE of ATR rungs into `levels.json` | yes |
| `alerts check` | PRICE ALERT CHECK. Prints new triggers or "NO NEW TRIGGERS" | yes |
| `alerts status` | Show each alert: armed or FIRED | no |
| `alerts reset` | Re-arm alerts. Only when the user asks | yes |
| `gainers` | Large (cap >= $10B), liquid gainers for the current session, with tracked/watch flags | no |
| `journal log TICKER VERDICT REF [--entry --stop --t1 --t2 --src --note --date]` | Log a signal | yes |
| `journal evaluate` | Score logged signals at 5 and 20 days | yes |
| `journal report` | Show journal results | no |
| `rank [TICKERS] [--periods D...] [--benchmarks T...] [--sort D] [--json]` | Trailing performance vs benchmarks | no |
| `regime` | Last 8 days tagged by trend (SMH vs 20/50-day averages), volatility (ATR% rank) and breadth (share of tracked tickers above their 20-day average), plus journaled ladder signals grouped by regime | no |
| `strategy` | Ladder and AMD breakout rule card plus a descriptive reading of the current regime. Informational only, no rule is gated by regime | no |
| `discipline check` | Compare live positions, open orders and balance with `discipline.json`: BREACH (position over max %), REVIEW (loss past invalidation %), VERIFY (sell limit over 15% from price), NOTE (no stop, low cash) | no |
| `discipline rules` | Print the written rules. Creates `discipline.json` with defaults if missing | first run only |
| `revenue [--chart [PATH]]` | Micron revenue by business unit, product and region (stored reported figures, extended by hand each earnings release). `--chart` needs matplotlib | no |
| `status [--only live\|tool\|experimental\|research\|archived]` | Tool inventory from `metadata.json` | no |

## Rules for checks

- Chat-only checks (ladder, price, gainers): no cache file, no git.
- "NO NEW TRIGGERS": reply with one short line.
- Ladder trigger: report ticker, level, price and tranche shares. Remind to cancel the lowest rung if the one above closes broken, and to stop near the final rung.
- Watch-only tickers (for example AMD) are never traded. A breakout counts only on a daily close above the level on higher volume.
- Gainers: after the screen, look up news for the printed tickers, then a short table. SKIP gets one line.
- Regime and strategy output is context, not a trading signal. A 250-day test on MU, ASML and TSM found DOWN or WEAK-breadth days were followed by the best 5-day returns, so never tell the user to pause or skip a ladder rung because of the regime. The per-regime journal table is empty until signals have 5-day outcomes; small samples are a log, not evidence.
- Discipline check: quote the BREACH, REVIEW and VERIFY lines as printed. Never place, change or cancel an order to fix a finding; the user decides.
- Discipline limits live in `discipline.json` (`max_position_pct`, `invalidation_loss_pct`, `min_cash_pct`, `account_id`). Regime constants (benchmark, SMAs, percentiles, breadth cut-offs) are at the top of `regime.py`.
- Never run state-writing commands as "tests" - they alter live alert and ladder state.

## Parsing tips

- Use `--json` where offered (`rank`). Other commands print plain text; quote lines, do not reinterpret numbers.
- webull-cli sometimes returns non-JSON under load; the package retries 3 times. If it still fails, say so instead of guessing prices.
