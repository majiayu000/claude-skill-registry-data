---
name: wolverine-strategy
description: >-
  WOLVERINE v2.0 — HYPE alpha hunter. Entry-only scanner, DSL-exit-only
  architecture. v1.1 lost -22.7% because the scanner's thesis exit chopped
  25/27 trades before DSL could manage them. v2.0 removes thesis exit entirely.
  Scanner decides entries (score 8+, 4H/1H aligned, SM consensus). DSL manages
  all exits (wide Phase 1 for HYPE volatility, trailing tiers starting at +15% ROE).
  Leverage lowered to 7x. Max 4 entries/day. 3-hour cooldown between entries.
  DSL exit managed by plugin runtime via runtime.yaml.
license: MIT
metadata:
  author: jason-goldberg
  version: "3.0"
  platform: senpi
  exchange: hyperliquid
  requires:
    - senpi-trading-runtime
---

# WOLVERINE v2.0 — HYPE Alpha Hunter

Scanner enters. DSL exits. The scanner NEVER re-evaluates open positions.

---

## CRITICAL AGENT RULES

### RULE 1: Install path is `/data/workspace/skills/wolverine-strategy/`

### RULE 2: THE SCANNER DOES NOT EXIT POSITIONS — DSL-ONLY EXITS

This is the single most important rule. When the scanner output contains `"_v2_no_thesis_exit": true` and the note says "DSL manages exit. Scanner does NOT re-evaluate," that means **DO NOT close, modify, or re-evaluate the open position for any reason.** The plugin DSL is the ONLY mechanism that can close positions.

v1.1 lost -22.7% because the scanner kept killing positions via "thesis exit" — 25 of 27 trades were chopped by the scanner before DSL could manage them. On HYPE, which wicks 5-10% ROE routinely, the scanner saw every wick as "thesis invalidation" and cut winners that would have run to +30%.

**If you close a position because "the thesis changed" or "SM flipped" or "the 4H trend broke," you are violating this rule and will bleed exactly like v1.1 did.**

### RULE 3: MAX 1 POSITION at a time

Only one HYPE position at a time. Check clearinghouse before every entry.

### RULE 4: Scanner output is AUTHORITATIVE

Leverage, margin, direction — use exactly what the scanner says.

### RULE 5: Verify runtime is installed on every session start

Run `openclaw senpi runtime list`. Runtime must be listed. The position tracker auto-detects position opens/closes on-chain and DSL exit is handled by the plugin runtime.

### RULE 6: Never modify parameters

### RULE 7: 3-hour cooldown between entries

After any position close (DSL floor, timeout, trailing stop), wait 3 hours before the next entry. This prevents revenge trading after a loss.

---

## What Changed From v1.1

| Setting | v1.1 | v2.0 | Why |
|---|---|---|---|
| Scanner thesis exit | ENABLED (killed 25/27 trades) | **REMOVED** | Was chopping winners |
| DSL authority | Shared with scanner | **DSL-ONLY exits** | One exit mechanism, no conflicts |
| Entry score threshold | ~5 (effectively) | **8** | Fewer, higher conviction entries |
| 4H/1H alignment | Optional | **REQUIRED** | Both timeframes must agree |
| Leverage | 10x | **7x** | More room to breathe on HYPE |
| Max daily entries | Unlimited | **4** | Patience is the edge |
| Cooldown | 120 min | **180 min** | 3 hours, prevent revenge trading |
| Phase 2 trigger | 7% ROE | **15% ROE** | Don't trail until a real move |
| First trailing tier | 7% trigger, 40% lock | **15% trigger, 30% lock** | Wide breathing room |

---

## The Thesis

HYPE moves 2-4% routinely. At 7x leverage, that's 14-28% ROE. The edge is:
1. Enter only when SM consensus + price momentum + contribution acceleration all align (score 8+)
2. Let DSL manage the position through HYPE's normal volatility
3. Wide Phase 1 floor (-20% ROE) survives the wicks that killed v1.1 entries
4. Trailing tiers don't engage until +15% ROE — no premature profit locking
5. When HYPE runs, it runs hard. One +30% ROE trade pays for 3 losing trades at -10%

**v1.1 proof:** Trade #6 hit +29.92% ROE (+$112) when the scanner accidentally let it run. That single trade was worth more than all other 13 winners combined.

---

## Exit Management

DSL exit is handled by the plugin runtime via `runtime.yaml`. The `position_tracker` scanner auto-detects position opens/closes on-chain. See `runtime.yaml` for configuration details.

**Monitor positions:**
- `openclaw senpi dsl positions` — list all DSL-tracked positions
- `openclaw senpi dsl inspect <ASSET>` — full position details

---

## Runtime Setup

**Step 1:** Set your strategy wallet address in runtime.yaml:
```bash
sed -i 's/${WALLET_ADDRESS}/<STRATEGY_WALLET_ADDRESS>/' /data/workspace/skills/wolverine-strategy/runtime.yaml
```
Replace `<STRATEGY_WALLET_ADDRESS>` with the actual wallet address.

**Step 2:** Set telegram chat ID for notifications:
```bash
sed -i 's/${TELEGRAM_CHAT_ID}/<CHAT_ID>/' /data/workspace/skills/wolverine-strategy/runtime.yaml
```
Replace `<CHAT_ID>` with the actual Telegram chat ID.

**Step 3:** Install the runtime:
```bash
openclaw senpi runtime create --path /data/workspace/skills/wolverine-strategy/runtime.yaml
```

**Step 4:** Verify:
```bash
openclaw senpi runtime list
```

---

## Bootstrap Gate

On EVERY session start, check `config/bootstrap-complete.json`. If missing:
1. Read the senpi-trading-runtime skill: `cat /data/workspace/skills/senpi-trading-runtime/SKILL.md` — this provides all CLI commands for runtime management and DSL position inspection.
2. Verify Senpi MCP
3. Set wallet in runtime.yaml: `sed -i 's/${WALLET_ADDRESS}/ACTUAL_ADDRESS/' /data/workspace/skills/wolverine-strategy/runtime.yaml`
4. Set Telegram in runtime.yaml: `sed -i 's/${TELEGRAM_CHAT_ID}/CHAT_ID/' /data/workspace/skills/wolverine-strategy/runtime.yaml`
5. Install runtime: `openclaw senpi runtime create --path /data/workspace/skills/wolverine-strategy/runtime.yaml`
6. Verify runtime installed: `openclaw senpi runtime list`
7. Remove old DSL cron (if upgrading): run `openclaw crons list`, delete any cron containing `dsl-v5.py` via `openclaw crons delete <id>`
8. Create scanner cron (3 min, main)
9. Write `config/bootstrap-complete.json`
10. Send: "WOLVERINE v2.0 online. HYPE hunter. Entry-only scanner. Plugin DSL manages all exits. Waiting for score 8+ setup."

If bootstrap exists, still verify runtime and scanner cron on every session start.

---

## Notification Policy

**ONLY alert:** Position OPENED (direction, score, reasons, leverage), Position CLOSED BY DSL (P&L, close reason, duration), critical error.

**NEVER alert:** Scanner found no signal, scanner sees open position and is not re-evaluating, any reasoning about whether to exit an open position.

---

## Expected Behavior

| Metric | Expected |
|---|---|
| Entries/day | 0-3 (some zero-trade days) |
| Position duration | 30 min to 12+ hours |
| Win rate | ~35-40% |
| Avg winner | +15% to +30% ROE |
| Avg loser | -10% to -20% ROE (Phase 1 cuts) |

**Long periods of silence are expected.** HYPE must have SM consensus, 4H/1H alignment, contribution acceleration, AND score 8+ to enter. That's rare. The patience IS the edge.

---

## Files

| File | Purpose |
|---|---|
| `scripts/wolverine-scanner.py` | Entry-only scanner. NO thesis exit. |
| `scripts/wolverine_config.py` | Config helper |
| `config/wolverine-config.json` | All parameters |
| `runtime.yaml` | Runtime config for plugin (DSL exit + position tracker) |

---

## License

MIT — Built by Senpi (https://senpi.ai).
