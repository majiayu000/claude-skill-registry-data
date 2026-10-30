---
name: token-roi
description: Token budget analytics and ROI scoring for AI agent actions. Track token cost per fix, detect wasteful loops, auto-route to fast tier when burn rate is too high. Integrates with token-budget-guard.sh hook. Triggered by /cost-report, "how much did that cost", "token usage", "am I wasting tokens".
origin: yamtam-original — Financial Guardrails layer
license: MIT
version: 1.0.0
compatibility: Claude Code, Anthropic API
---

# token-roi

## When to Use

- After a long session to review token spend vs value delivered
- When `autonomous-patching-loop` has been running for multiple attempts
- Before deciding whether to continue a costly repair or escalate to human
- Triggered by: `/cost-report`, "how much did that cost", "token usage", "token budget", "am I wasting tokens", "ROI", "cost per fix"

## Do NOT use for

- Real-time per-token billing (use Anthropic console for exact billing)
- Replacing a proper cost alert system in production
- See `prompt-caching-strategy` for reducing token cost via cache_control

---

## Cost Tiers (Anthropic Sonnet 4.x pricing reference)

```
Tier       Model               Input $/1M    Output $/1M   Use when
──────────────────────────────────────────────────────────────────────
Power      claude-opus-4-7     $15.00        $75.00        Architecture, deep reasoning
Balanced   claude-sonnet-4-6   $3.00         $15.00        Default for most tasks
Fast       claude-haiku-4-5    $0.80         $4.00         Simple fixes, boilerplate
──────────────────────────────────────────────────────────────────────
Cached     any + cache_control 90% discount  standard      Static context blocks
```

---

## /cost-report Command

```bash
#!/usr/bin/env bash
# Generate token ROI report for current session
BUDGET_FILE="core/memory/L2_session/token-budget.json"

if [[ ! -f "$BUDGET_FILE" ]]; then
  echo "No token budget data for this session."
  exit 0
fi

python3 - <<PYEOF
import json

with open("$BUDGET_FILE") as f:
    d = json.load(f)

total = d.get('total_tokens_used', 0)
actions = d.get('actions', [])
loops = d.get('loop_attempts', {})
fast_triggered = d.get('fast_tier_triggered', False)

# Cost estimate (Sonnet 4.6 balanced tier)
cost_usd = (total / 1_000_000) * 9  # avg input+output blended

print("=" * 50)
print(" YAMTAM Token ROI Report")
print("=" * 50)
print(f" Session start : {d.get('session_start', 'unknown')}")
print(f" Total tokens  : {total:,}")
print(f" Est. cost     : \${cost_usd:.4f} USD (Sonnet 4.6 blended)")
print(f" Fast tier     : {'TRIGGERED' if fast_triggered else 'not triggered'}")
print("")
print(" Loop attempts by tool:")
for tool, count in sorted(loops.items(), key=lambda x: -x[1]):
    flag = " ⚠ LOOP" if count >= 3 else ""
    print(f"   {tool:<30} {count} calls{flag}")
print("")

# ROI assessment
if cost_usd > 0.50:
    print(" ROI Assessment: HIGH COST — review if value delivered matches spend")
elif fast_triggered:
    print(" ROI Assessment: LOOP DETECTED — strategy switch recommended")
else:
    print(" ROI Assessment: Within normal budget")
print("=" * 50)
PYEOF
```

---

## Fast-Tier Auto-Routing

When `token-budget-guard.sh` triggers fast tier, agents MUST:

```
1. STOP current loop immediately
2. Assess: is this a simple fix that Haiku can handle?
   YES → switch model to claude-haiku-4-5, retry with minimal prompt
   NO  → escalate to human with cost summary

3. Fast-tier prompt template (minimal tokens):
   "Fix: [one-line error description]
    File: [path]:[line]
    Error: [exact error message]
    Fix in ≤ 20 lines."
```

---

## Token ROI Scoring Formula

```python
def roi_score(tokens_used: int, bugs_fixed: int, tests_passed: int) -> float:
    """
    Score 0.0–10.0. Higher = better ROI.
    Penalize high token use, reward concrete outcomes.
    """
    if tokens_used == 0:
        return 0.0

    # Value: each fixed bug = 10k tokens of "worth", each test = 2k tokens
    value = (bugs_fixed * 10_000) + (tests_passed * 2_000)
    efficiency = value / tokens_used

    # Normalize to 0–10 scale (efficiency 1.0 = score 5)
    score = min(efficiency * 5, 10.0)
    return round(score, 1)

# Examples:
# roi_score(5000, 1, 3)  → 8.0  ← good (1 bug fixed, 3 tests added, low tokens)
# roi_score(50000, 0, 0) → 0.0  ← bad (50k tokens, nothing fixed)
# roi_score(20000, 2, 5) → 5.5  ← acceptable
```

---

## Session Budget Defaults

```bash
# Override via environment variables
export YAMTAM_MAX_LOOP_TOKENS=50000   # ~$0.15 at Sonnet — warn threshold
export YAMTAM_MAX_FIX_ATTEMPTS=5      # tool call loop limit before fast-tier
export YAMTAM_TOKEN_BUDGET=core/memory/L2_session/token-budget.json
```

---

## Integration with autonomous-patching-loop

```
autonomous-patching-loop attempt 1  →  token-budget-guard checks loop count
                      attempt 2  →  guard checks (count=2)
                      attempt 3  →  guard WARNS (count=3)
                      attempt 4  →  guard checks (count=4)
                      attempt 5  →  guard TRIGGERS FAST TIER
                                    loop stops, escalates or switches model
```

---

## Anti-Fake-Pass Checklist

- [ ] Budget file exists at `core/memory/L2_session/token-budget.json` before session ends
- [ ] Loop count tracked per tool name — not total session calls
- [ ] Fast tier triggered when loop count ≥ MAX_ATTEMPTS (default: 5)
- [ ] Cost estimate calculated and shown in /cost-report
- [ ] ROI score computed when both token count and outcomes are known
- [ ] Fast-tier mode uses shorter prompt template (not full context dump)
- [ ] Budget state written to L2 — expires at session end, not promoted to L1 unless anomaly
