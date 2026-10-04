---
name: lemon-strategy
description: >-
  LEMON v2.0 — The Degen Fader. Identifies historically reckless traders
  (DEGEN activity + CHOPPY consistency) on Hyperliquid, monitors their live
  positions, and counter-trades them when they're bleeding at high leverage.
  If a cluster of degens goes max-leverage long on a coin and starts losing,
  LEMON shorts it — betting on their inevitable liquidation cascade.
  DSL exit managed by plugin runtime via runtime.yaml.
license: MIT
metadata:
  author: jason-goldberg
  version: "2.0"
  platform: senpi
  exchange: hyperliquid
  requires:
    - senpi-trading-runtime
---

# 🍋 LEMON v2.0 — The Degen Fader

Find the worst traders. Wait until they're bleeding. Take the other side.

---

## ⛔ CRITICAL AGENT RULES

### RULE 1: Install path is `/data/workspace/skills/lemon-strategy/`

### RULE 2: THE SCANNER DOES NOT EXIT POSITIONS

When the scanner sees an active position, it outputs NO_REPLY. DSL is the
ONLY exit mechanism. Every Senpi agent that implemented its own exit logic
lost money. The scanner finds entries. DSL manages exits. Period.

### RULE 3: MAX 2 POSITIONS at a time

Check clearinghouse before every entry. If positions >= 2, skip.

### RULE 4: Scanner output is AUTHORITATIVE

Leverage, margin, direction, coin — use exactly what the scanner says.
Do not override from memory or "improve" the parameters.

### RULE 5: Verify runtime is installed on every session start

Run `openclaw senpi runtime list`. Runtime must be listed. The position tracker and DSL exit are handled by the plugin runtime.

### RULE 6: Never retry timed-out position creation

If `create_position` times out, check clearinghouse state. If position exists, the position tracker will pick it up automatically. If not, wait for next scan.

### RULE 7: Never modify parameters

Do not adjust leverage, margin, thresholds, or any other
parameter. Every agent that self-modified made things worse.

### RULE 8: 180-minute per-asset cooldown after any exit

---

## Core Thesis

Most copy-trading strategies follow the best traders. LEMON does the opposite:
it finds the WORST traders and bets against them.

Hyperliquid's `discovery_get_top_traders` API exposes trader quality labels:
- **Activity labels:** DEGEN, SNIPER, AGGRESSIVE, BALANCED, CONSERVATIVE
- **Consistency labels:** CHOPPY, STREAKY, RELIABLE, ELITE

DEGEN + CHOPPY traders are statistically the most likely to:
1. Over-leverage (20x+ on volatile assets)
2. Hold losing positions too long (hope trading)
3. Eventually get liquidated (forced cascade)

When a cluster of these traders is max-leveraged and actively bleeding
(-10%+ ROE), their liquidation is increasingly likely. LEMON enters the
opposite direction — SHORT if they're LONG, LONG if they're SHORT — and
rides the liquidation cascade that follows.

**Why this works:** Liquidation cascades are mechanical. When leveraged
positions get liquidated, the exchange force-sells/buys, pushing price
further against the crowd. This creates a predictable directional move
that LEMON is already positioned for.

---

## Signal Pipeline

### Phase 1: Target Acquisition (every 5 minutes)

Call `discovery_get_top_traders` with filters:
```
time_frame: "WEEKLY"
activity_labels: ["DEGEN"]
consistency: ["CHOPPY"]
limit: 10
```

This returns the top 10 DEGEN/CHOPPY traders by recent activity.

### Phase 2: Vulnerability Scan

For each target trader, call `discovery_get_trader_state` to inspect
their live open positions. Look for the vulnerability trigger:

| Condition | Threshold | Why |
|---|---|---|
| Leverage | >= 10x | Over-leveraged = closer to liquidation |
| ROE | < -10% | Already bleeding = liquidation approaching |
| Position exists | Active, not closed | Still in the trade |

**Both conditions must be true simultaneously.** A degen at 20x leverage
but +5% ROE is winning — don't fade a winner. A trader at 5x and -15%
has room to breathe — liquidation is far away. The sweet spot is high
leverage AND actively losing.

### Phase 3: Conviction Scoring

Not every bleeding degen is worth fading. Score the setup:

| Signal | Points | Description |
|---|---|---|
| Target leverage >= 10x | 2 | Base threshold |
| Target leverage >= 20x | +1 | High leverage = faster cascade |
| Target ROE < -10% | 2 | Base threshold |
| Target ROE < -20% | +1 | Deep in the red = liquidation imminent |
| Multiple degens on same asset/direction | +2 | Cluster = bigger cascade |
| Asset funding rate confirms fade direction | +1 | Structural pressure aligned |
| SM (smart money) aligned with fade direction | +1 | Top traders agree with our side |

**Minimum score: 6 to enter.**

### Phase 4: SM Confirmation Gate

Before entering, check `leaderboard_get_markets` for the fade asset:
- Is smart money positioned in our fade direction?
- Are there 10+ SM traders on the asset?

If SM is actively positioned AGAINST our fade direction (i.e., SM agrees
with the degens), SKIP. Don't fight both degens AND smart money.

### Phase 5: Entry

If score >= 6 and SM gate passes:

```
Asset: [Target's coin]
Direction: OPPOSITE of target's direction
Leverage: 5x (conservative — we're betting on their liquidation, not YOLO-ing ourselves)
Margin: 15% of account value
Order type: FEE_OPTIMIZED_LIMIT
```

**Why 5x leverage:** The fade thesis plays out over minutes to hours. At 5x,
a 3% favorable move = +15% ROE. We don't need 20x — that's what the degens
use, and that's why they blow up.

---

## Exit Management

DSL exit is handled by the plugin runtime via `runtime.yaml`. The `position_tracker` scanner auto-detects position opens/closes on-chain. See `runtime.yaml` for configuration details.

**Monitor positions:**
- `openclaw senpi dsl positions` — list all DSL-tracked positions
- `openclaw senpi dsl inspect <ASSET>` — full position details

---

## Risk Management

| Rule | Value |
|---|---|
| Max positions | 2 |
| Max entries/day | 4 |
| Leverage | 5x (fixed) |
| Margin per trade | 15% of account |
| Per-asset cooldown | 180 min |
| Daily loss limit | 10% |
| Consecutive losses | 3 → 45 min cooldown |
| XYZ assets | Banned |
| Max single trade loss | 3% of account (floor at -15% ROE × 15% margin = 2.25%) |

### Anti-Patterns (Hard-Coded)

1. **NEVER fade a winning degen.** ROE must be < -10% before fading.
2. **NEVER fade when SM agrees with the degen.** If smart money is on the same side as the target, the degen might accidentally be right.
3. **NEVER use more than 5x leverage.** We're the patient predator, not another degen.
4. **NEVER re-enter the same asset within 3 hours.** If the first fade didn't work, the thesis was wrong.
5. **Max 1 fade per trader cluster.** If 3 degens are all long BTC, that's one fade signal, not three.

---

## Runtime Setup

**Step 1:** Set your strategy wallet address in runtime.yaml:
```bash
sed -i 's/${WALLET_ADDRESS}/<STRATEGY_WALLET_ADDRESS>/' /data/workspace/skills/lemon-strategy/runtime.yaml
```
Replace `<STRATEGY_WALLET_ADDRESS>` with the actual wallet address.

**Step 2:** Set telegram chat ID for notifications:
```bash
sed -i 's/${TELEGRAM_CHAT_ID}/<CHAT_ID>/' /data/workspace/skills/lemon-strategy/runtime.yaml
```
Replace `<CHAT_ID>` with the actual Telegram chat ID.

**Step 3:** Install the runtime:
```bash
openclaw senpi runtime create --path /data/workspace/skills/lemon-strategy/runtime.yaml
```

**Step 4:** Verify:
```bash
openclaw senpi runtime list
```

---

## Data Sources

| Data | MCP Tool | Purpose |
|---|---|---|
| Degen traders | `discovery_get_top_traders` | Find DEGEN/CHOPPY targets |
| Trader positions | `discovery_get_trader_state` | Check leverage, ROE, direction |
| SM consensus | `leaderboard_get_markets` | Confirmation gate |
| Asset data | `market_get_asset_data` | Funding rate, price context |
| Account state | `strategy_get_clearinghouse_state` | Position tracking |

---

## State Files

```
state/
  trade-counter.json        # Daily entries, loss tracking, gate
  cooldowns.json            # Per-asset cooldown after exits
  scan-history.json         # Recent degen scans for cluster detection
```

---

## Bootstrap Gate

On EVERY session start, check `config/bootstrap-complete.json`. If missing:
1. Read the senpi-trading-runtime skill: `cat /data/workspace/skills/senpi-trading-runtime/SKILL.md` — this provides all CLI commands for runtime management and DSL position inspection.
2. Verify Senpi MCP
3. Set wallet in runtime.yaml: `sed -i 's/${WALLET_ADDRESS}/ACTUAL_ADDRESS/' /data/workspace/skills/lemon-strategy/runtime.yaml`
4. Set Telegram in runtime.yaml: `sed -i 's/${TELEGRAM_CHAT_ID}/CHAT_ID/' /data/workspace/skills/lemon-strategy/runtime.yaml`
5. Install runtime: `openclaw senpi runtime create --path /data/workspace/skills/lemon-strategy/runtime.yaml`
6. Verify runtime installed: `openclaw senpi runtime list`
7. Remove old DSL cron (if upgrading): run `openclaw crons list`, delete any cron containing `dsl-v5.py` via `openclaw crons delete <id>`
8. Create scanner cron (5 min, main)
9. Write `config/bootstrap-complete.json`
10. Send: "🍋 LEMON v2.0 online. Degen Fader scanning for bleeding high-leverage traders. DSL managed by plugin runtime. Silence = no vulnerable degens."

---

## Notification Policy

**ONLY alert:** Position OPENED (target trader, their leverage/ROE, our
fade direction, score), Position CLOSED (P&L, close reason, duration),
risk gate triggered, critical error.

**NEVER alert:** Scanner found no vulnerable degens, target trader still alive (not yet triggered), any reasoning about whether
to exit.

---

## Expected Behavior

| Metric | Expected |
|---|---|
| Entries/day | 0-3 (many zero-trade days) |
| Win rate | ~45-55% |
| Avg winner | 2-3x avg loser (cascade runs > small losses) |
| Position duration | 10 min to 2+ hours |
| Hold time on winners | Longer (cascades compound) |

**Most days will have zero trades.** DEGEN/CHOPPY traders at 20x+ leverage
AND -10%+ ROE is a specific, uncommon setup. That's the point — high
conviction entries only.

---

## Why "LEMON"

Because we're squeezing the lemons. 🍋

---

## Package Contents

The complete skill is in `lemon-v1.0.tar.gz`. Extract to `/data/workspace/skills/lemon-strategy/`.

| File | Purpose |
|---|---|
| `SKILL.md` | This document — all rules, architecture, and configuration |
| `README.md` | Short overview |
| `scripts/lemon-scanner.py` | Degen finder + vulnerability scan + conviction scoring + entry signal |
| `scripts/lemon_config.py` | Config helper (MCP calls, state I/O, cooldowns, trade counter) |
| `config/lemon-config.json` | Wallet, strategy ID, configurable thresholds (agent fills in wallet/strategyId) |
| `runtime.yaml` | Runtime config for plugin (DSL exit + position tracker) |

---

## Installation

1. Extract `lemon-v1.0.tar.gz` to `/data/workspace/skills/lemon-strategy/`
2. Create a strategy vault and fund it with $1,000
3. Update `config/lemon-config.json` with the wallet address and strategy ID
4. Set wallet in runtime.yaml: `sed -i 's/${WALLET_ADDRESS}/ACTUAL_ADDRESS/' /data/workspace/skills/lemon-strategy/runtime.yaml`
5. Set Telegram in runtime.yaml: `sed -i 's/${TELEGRAM_CHAT_ID}/CHAT_ID/' /data/workspace/skills/lemon-strategy/runtime.yaml`
6. Install runtime: `openclaw senpi runtime create --path /data/workspace/skills/lemon-strategy/runtime.yaml`
7. Verify runtime: `openclaw senpi runtime list`
8. Create scanner cron (5 min, main): `python3 /data/workspace/skills/lemon-strategy/scripts/lemon-scanner.py`
9. Verify scanner cron running with `openclaw crons list`
10. After first position opens, verify DSL is tracking via `openclaw senpi dsl positions`

---

## License

MIT — Built by Senpi (https://senpi.ai).
Source: https://github.com/Senpi-ai/senpi-skills
