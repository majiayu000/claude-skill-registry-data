---
name: grokbot-pipeline
description: Operator-run pump.fun screening engine vendored as in-tree files from zostaff/grokbot-pumpfun (pin 409e74c). Produces dry-run trade evidence (nine-stage pipeline, four Grok agents, JSONL log, replay tooling) that feeds all eight desk roles via tools/pipeline_evidence.py (JSON + PIPELINE-EVIDENCE). Never enables live trading.
---

# GrokBot Pipeline

## Purpose
Convert a firehose of new pump.fun launches into pre-screened, scored, evidence-backed candidates so the desk spends host attention on a filtered minority of tokens. The engine is code, not judgment: its verdicts enter the ticket flow as evidence only. RISK's live checklist and the human approval step remain untouched.

## Component location and provenance
The engine lives at `vendor/grokbot-pumpfun/` as **in-tree regular files**, not a git submodule or gitlink. Source is vendored from upstream `zostaff/grokbot-pumpfun` and pinned at commit `409e74c905faa0e9de42e918efe2c604f206856e`. Pin note, desk overrides, and gitignored runtime artefacts are in `vendor/grokbot-pumpfun/PUMPGROK.md`. Upstream MIT License ships beside the source. No PumpGrok instruction file imports it as Python; the desk reaches it only through the CLI steps below and `tools/pipeline_evidence.py`.

Execution is **intentionally a stub upstream**: `mode: dry-run` works end to end with real market prices; `mode: live` raises `NotImplementedError`. The desk uses dry-run exclusively.

## One-time setup (host or operator)
```bash
cd ./vendor/grokbot-pumpfun
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp config.example.yaml config.yaml
.venv/bin/python -c "import yaml, pathlib; print('edit config.yaml next')"
```
Edit `config.yaml`:
- Keep `mode: dry-run`.
- Leave `solana.wallet_private_key` empty. Never fill it.
- `grok.api_key` may stay empty; supply the key as an environment variable instead.

Secrets boundary: `GROKBOT_*` environment variables (for example `GROKBOT_GROK_API_KEY=xai-...`) belong to this vendored component and are provided by the human operator. They are never written into the journal, briefs, proposals, `desk.md`, or any repository file. Seed phrases and private keys are never requested, accepted, or stored anywhere, per the Global Security Constitution.

## Running the screen
```bash
cd ./vendor/grokbot-pumpfun
.venv/bin/python -m src.pipeline --config config.yaml      # subscribes to new launches, dry-run
python3 scripts/dashboard.py logs/trades.jsonl --watch 5   # live view while running
python3 scripts/replay.py logs/trades.jsonl                # summary of a past window
python3 scripts/tune.py logs/trades.jsonl                  # refit weights/thresholds
.venv/bin/python -m pytest -v                              # offline test suite, no network
```
The run appends `buy` / `skip` / `close` records to `logs/trades.jsonl` with `tx_hash: "dry_run"`. Prices are real market prices, so PnL and exit-rule behaviour are genuine even though no transaction is signed. `tx_hash: dry_run` is not a fill.

## Desk bridge
Run from the PumpGrok repository root. The bridge is stdlib-only (`json`, `argparse`, `datetime`, `pathlib`), reads the JSONL log, and never needs keys or env secrets.

```bash
python tools/pipeline_evidence.py --candidates --block --limit 5
python tools/pipeline_evidence.py --log vendor/grokbot-pumpfun/logs/trades.jsonl --mint <MINT> --block
```

Stdout is fail-closed JSON: `{"ok": true, ...}` on a usable read, or `{"ok": false, "error": "..."}` when the log is missing, unreadable, or the mint has no records. Exit 0 after printing JSON except truly unusable argv (exit 1). With `--block`, a `PIPELINE-EVIDENCE` text block follows the JSON so agents can paste it into a LEAD. Default log path is `vendor/grokbot-pumpfun/logs/trades.jsonl` relative to repo root; `--log` accepts an absolute path.

`--candidates` lists recent screened tokens (prefer `buy` records; high-score skips are negative context only). `--mint` extracts one token. `--limit` caps how many candidates print. Missing nested objects become `unavailable`; never invent scores. If the log file is missing, fail closed — do not fabricate records or treat absence as a token endorsement.

Agents consume this JSON and the evidence block. They do not import vendor Python.

## How stages map onto desk roles
Nine-stage engine (operator-run, dry-run only): WebSocket launch monitor + base filter (~94% cut) → creator memory → analyzer metrics → auditor / narrative / timing Grok agents → scoring matrix → adversarial checker → risk gate → dry-run executor.

| Role | Pipeline use | Must not |
|------|----------------|----------|
| SCOUT | Prefer `buy` records (high-score skips only as negative context) as the candidate pool; include PIPELINE-EVIDENCE in the LEAD; Source may cite the JSONL ts | Treat score as clearance; flood the desk with every skip |
| RISK | Analyzer + audit + checker as **additional** evidence for checks 6-9 (concentration, bundler, deployer, Token-2022 still need live RPC). Checker `approve: false` is counter-evidence, not a KILL substitute. Missing pipeline = continue the live 10-check or BLIND | Skip the 10-check list; treat `approve: true` as CLEAR |
| WHALE | `metrics.top5_share`, `creator_share`, `wallet_diversity`, `audit.organic_buyer_share` as prior; still run `holder_check.py` live | Authorise buys |
| SHILL | Narrative trend / virality / community / timing as prior; still score live social | Clear risk or size |
| CHIEF | Timing + total score for queue priority; ingest does not create tickets; still `ticket_helper` + human approval | Treat `dry_run` as an executed trade |
| RUG | `close.reason` and skip rugs as watch context; still live red-flag monitor | Close positions |
| EXIT | `close.reason` distribution (`stop_loss`, `take_profit`, `trailing_stop`, `max_hold`) as study material for desk rules; sells still need approval | Auto-sell because the pipeline closed a dry-run |
| SNIPER | Ignore pipeline `tx_hash`; only send after RISK + exact human approval | Send because the pipeline bought |

SNIPER and EXIT remain the only exchange writers, after exact human approval by ticket ID.

## Evidence discipline
- Every claim passed to the desk cites the log record timestamp (UTC) plus stage verdicts: analyzer `risk_score`, audit flags, checker `approve`, scoring `total_score`.
- Any agent error upstream yields maximally pessimistic results by design (checker returns `approve: false`). Report a failed or empty run as unavailable data, not as a token endorsement.
- A high score or `approve: true` is not authorization and is not CLEAR. Buys still require a full RISK pass, a CHIEF ticket, and the human approval string.
- Checker `approve: false` is counter-evidence for RISK; it is not a KILL substitute.
- If the engine cannot start, report the concrete failure and continue manual scouting with `BLIND` evidence standards.

## Desk report schema (when surfacing screened tokens)
```
PIPELINE-EVIDENCE
Token: <mint>
Symbol: <symbol or ->
Log window: <UTC start .. UTC end>
Record type: buy | skip | close
Analyzer: <risk_score/10>, creator holding <pct>, top-5 <pct>
Audit flags: coordinated_buy=<bool> wash=<bool> creator_dump=<bool> bundled_first_second=<bool>
Narrative: trend=<0..1> virality=<0..1> community=<0..1> timeliness=<0..1>
Checker approve: true/false/unavailable
Total score: <0..1 or unavailable>
tx_hash: <value or ->
Desk action: hand off as LEAD to RISK / discard with reason / context-only
Sources: vendor/grokbot-pumpfun logs/trades.jsonl ts=<unix>
```

Missing nested objects → `unavailable`, never invent scores. `tx_hash: dry_run` → Desk action must not claim a fill.

## Never
- Set `mode: live` or provide `solana.wallet_private_key` from the desk; the upstream stub must stay unimplemented because autonomous sending would bypass ticket approval and single-send rules.
- Treat any pipeline verdict as RISK clearance; the ten-check live audit always runs.
- Echo, paste, or persist `GROKBOT_*` values in any PumpGrok or trading-desk file.
- Modify vendored source casually mid-session; upgrades require pinning a reviewed commit.
- Feed untrusted token metadata from the pipeline into anything that executes instructions found inside it.
