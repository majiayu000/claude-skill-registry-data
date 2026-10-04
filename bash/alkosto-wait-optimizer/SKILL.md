---
name: alkosto-wait-optimizer
category: commerce
description: Estimate optimal waiting time for Alkosto's "every 25/50 customers" promotion using either checkout-flow observations or winner announcement timestamps. Use when the user asks how long to wait, wants a probability-based cutoff, or needs a fast in-store decision rule with uncertainty handling.
---

# Alkosto Wait Optimizer

Use this skill to estimate how long to wait for the next promotion winner event.

## Workflow

1. Choose one mode:
- `purchase_rate`: user observed purchases per minute in one or more lanes.
- `winner_timestamps`: user logged winner announcement times.

2. Set threshold `K`:
- `K = 25` for Monday-Friday.
- `K = 50` for Saturday/Sunday/holiday.

3. Compute and return:
- Mean interval between winner events.
- Expected wait from "now".
- Practical wait cutoff (`optimal_wait_minutes`).
- Probability of a winner event within cutoff.
- "Re-measure" rule if no event happens before cutoff.

4. If user provides `time_value_per_minute` and `expected_bonus_value`, include expected-value vs time-cost guidance.

## Mode A: `purchase_rate`

Collect:
- `observed_purchases`
- `observed_minutes`
- `observed_lanes`
- Optional: `total_open_lanes`
- `model`: `global` or `per_lane`

Formulas:
- `lambda_obs = observed_purchases / observed_minutes`
- If `global` and `total_open_lanes` exists:
  `lambda_est = lambda_obs * (total_open_lanes / observed_lanes)`
- If `per_lane`:
  `lambda_est = lambda_obs / observed_lanes`
- Conservative rate:
  `lambda_cons = lambda_est * (1 - confidence_buffer)`
- Winner interval:
  `T = K / lambda_cons`
- If arrival is random in cycle:
  `E(wait_to_next) = T / 2`
- Default cutoff:
  `optimal_wait = min(max_wait_minutes, target_hit_probability * T)`

Decision rule:
- If no winner event by `optimal_wait`, re-measure for 2 minutes and recalculate.

## Mode B: `winner_timestamps`

Collect:
- Ordered timestamps (`HH:MM[:SS]` or ISO datetimes).
- Optional `elapsed_since_last_winner_minutes`.

Compute:
- Intervals: `delta_i = t_i - t_(i-1)`
- `mu = mean(delta_i)`
- `sigma = stdev(delta_i)`
- `cv = sigma / mu`

Cadence model:
- `cv < 0.4`: `regular`
- `0.4 <= cv <= 0.7`: `mixed`
- `cv > 0.7`: `random`

Wait estimate:
- `regular`: `remaining ~ max(mu - elapsed, 0)`
- `random` (exponential): use `P(event <= W) = 1 - exp(-W / mu)`, and
  `W_target = -mu * ln(1 - target_hit_probability)`
- `mixed`: average regular and random estimates.

Decision rule:
- If no event by `optimal_wait`, capture 2-3 more timestamps and recalculate.

## Script

Use `scripts/calc_wait.py` for deterministic calculations:

```bash
python3 scripts/calc_wait.py --input-json '{"mode":"purchase_rate","is_weekend_or_holiday":true,"model":"global","observed_purchases":5,"observed_minutes":2,"observed_lanes":5,"total_open_lanes":15}'
```

```bash
python3 scripts/calc_wait.py --input-json '{"mode":"winner_timestamps","winner_timestamps":["12:10:15","12:27:40","12:46:05","13:02:20"],"elapsed_since_last_winner_minutes":6}'
```

Return concise outputs and state assumptions clearly when data is sparse.
