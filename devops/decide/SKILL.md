---
name: decide
description: Decision helper — coin flip, dice roll, pick from options, Magic 8-Ball.
homepage: https://github.com/timkrase/clawdis-skills
metadata: {"clawdis":{"emoji":"🎲","requires":{"bins":["node"]}}}
---

# Decide Skill 🎲

When you can't decide, let fate decide for you!

## Quick Start

```bash
# Coin flip
{baseDir}/scripts/decide.js flip

# Roll dice (default: d6)
{baseDir}/scripts/decide.js roll
{baseDir}/scripts/decide.js roll d20
{baseDir}/scripts/decide.js roll 3d6

# Pick from options
{baseDir}/scripts/decide.js pick "Pizza" "Burger" "Sushi"

# Magic 8-Ball
{baseDir}/scripts/decide.js 8ball "Should I go to the gym?"

# Yes or No
{baseDir}/scripts/decide.js yesno

# Random number (1-100 default, or specify range)
{baseDir}/scripts/decide.js number
{baseDir}/scripts/decide.js number 1 10
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `flip` | Coin flip (Heads/Tails) | `decide.js flip` |
| `roll` | Dice roll (NdX format) | `decide.js roll 2d20` |
| `pick` | Random pick from options | `decide.js pick A B C` |
| `8ball` | Magic 8-Ball wisdom | `decide.js 8ball "Will it work?"` |
| `yesno` | Simple yes/no | `decide.js yesno` |
| `number` | Random number | `decide.js number 1 100` |

## Usage in Chat

When Tim can't decide:
- "Pizza oder Burger?" → `pick "Pizza" "Burger"`
- "Soll ich Sport machen?" → `8ball` or `yesno`
- "Gib mir eine Zahl zwischen 1 und 10" → `number 1 10`
- "Würfel mal" → `roll`

Add dramatic flair to your responses! 🎭

## Output Format

Returns JSON for easy parsing:
```json
{
  "type": "flip",
  "result": "Heads",
  "emoji": "🪙"
}
```

Use `--raw` for plain text output (just the result).
