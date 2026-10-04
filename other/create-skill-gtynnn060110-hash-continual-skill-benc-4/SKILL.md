---
name: create-skill
description: Create a new reusable skill file to capture a calculation method, formula, or tool pattern you've discovered during a task.
allowed-tools: Write Bash
---

# create-skill

When you solve a finance problem and discover a reusable pattern—a formula, a Python snippet, or a workflow—save it as a new skill so future tasks in this session can benefit from it.

## When to Use

- After completing a task, if you used a technique not covered by existing skills
- After receiving positive judge feedback ("Score: 0.8+") — the approach is validated
- When you derive a formula from first principles that will likely recur
- When you find a better implementation than what a skill suggests

## Usage

### Option A: Direct bash (recommended for simple skills)

```bash
SKILL_NAME="bond-ytm-calculator"
SKILL_CONTENT='---
name: bond-ytm-calculator
description: Compute bond YTM using Newton-Raphson iteration from price, face value, coupon, and maturity.
---

# Bond YTM Calculator

## Formula
Price = sum(coupon / (1+ytm)^t for t in 1..n) + face / (1+ytm)^n

## Python Implementation
```python
import numpy as np

def bond_ytm(price, face, coupon_rate, n_periods, freq=1):
    """Newton-Raphson YTM solver."""
    coupon = face * coupon_rate / freq
    ytm = coupon_rate  # initial guess
    for _ in range(100):
        p = sum(coupon / (1 + ytm/freq)**t for t in range(1, n_periods*freq+1))
        p += face / (1 + ytm/freq)**(n_periods*freq)
        dp = sum(-t * coupon / (freq * (1 + ytm/freq)**(t+1)) for t in range(1, n_periods*freq+1))
        dp -= n_periods * face / (1 + ytm/freq)**(n_periods*freq+1)
        ytm -= (p - price) / dp
        if abs(p - price) < 1e-10:
            break
    return ytm
```

## Notes
- coupon_rate and ytm are annual rates; freq=2 for semi-annual
- Converges in <20 iterations for typical bond prices'

# Write to all agent skill directories
for DIR in /root/.claude/skills /root/.terminus/skills /root/.codex/skills /root/.opencode/skill /root/.goose/skills /root/.factory/skills /root/.agents/skills /root/.gemini/skills; do
    mkdir -p "$DIR/$SKILL_NAME"
    printf '%s' "$SKILL_CONTENT" > "$DIR/$SKILL_NAME/SKILL.md"
done
echo "Skill '$SKILL_NAME' created in all agent directories."
```

### Option B: Using the helper script

```bash
python3 /root/create_skill_helper.py \
  --name "portfolio-returns-sharpe" \
  --description "Compute annualized return and Sharpe ratio from price series" \
  --content-file /tmp/skill_draft.md
```

## Skill File Format

```markdown
---
name: skill-name-in-kebab-case
description: One-line description the agent sees when deciding which skill to load.
---

# Skill Title

## What it does
[Brief explanation]

## Python Implementation
```python
# Working code example
```

## Key Parameters / Notes
- [Important gotcha 1]
- [Important gotcha 2]
```

## Naming Conventions

| Domain | Example Skill Names |
|--------|-------------------|
| market | `portfolio-returns-sharpe`, `beta-regression`, `efficient-frontier` |
| fixed-income | `bond-ytm-duration`, `yield-curve-bootstrap`, `convexity-calc` |
| derivatives | `black-scholes-pricer`, `greeks-delta-gamma`, `implied-vol-bisection` |
| corporate | `financial-ratio-calculator`, `dupont-decomposition`, `cashflow-parser` |
| macro | `hp-filter-detrend`, `cpi-deflator`, `gdp-growth-rate` |
| risk | `var-historical`, `cvar-parametric`, `drawdown-analyzer` |
| valuation | `dcf-fcf-model`, `wacc-calculator`, `ev-ebitda-multiples` |

## After Creating a Skill

The skill is immediately available for the current session. You do NOT need to reload it—
it will appear in `available_skills` at the start of the next task.
