---
name: rl
version: 1.0.0
description: >
  Manage Reinforcement Learning (A/B testing) experiments via Drush CLI.
  Thompson Sampling multi-armed bandit experiments: create, analyze,
  configure, and optimize content variants.
triggers:
  - /rl
  - experiment
  - a/b test
  - ab test
  - bandit
  - thompson sampling
  - conversion rate
  - variant
---

# RL — Reinforcement Learning Experiments

You are managing A/B testing experiments powered by Thompson Sampling.
The RL module tracks impressions (turns) and conversions (rewards) across
content variants and automatically optimizes traffic distribution.

## Preamble — Auto-discover Current State

```bash
# List all active experiments
drush rl:list --format=yaml

# Get current module configuration
drush rl:config:list

# If experiments exist, get status of the most active one
# drush rl:status <experiment_id> --format=yaml
```

## Commands Reference

### Discovery & Analysis (read-only)

| Command | Alias | Purpose |
|---|---|---|
| `rl:list` | `rll` | List all experiments with summary stats |
| `rl:status <id>` | `rlst` | Detailed status: phase, confidence, traffic distribution |
| `rl:performance <id>` | `rlp` | Arm-level performance with human-readable labels |
| `rl:trends <id>` | `rlt` | Historical trends with period aggregation |
| `rl:export <id>` | `rle` | Export complete experiment data |
| `rl:analyze <id>` | `rla` | Full analysis with actionable recommendations |

### Experiment Lifecycle

| Command | Alias | Purpose |
|---|---|---|
| `rl:experiment:create <id>` | `rl-ec` | Create experiment (`--module`, `--name`, `--dry-run`) |
| `rl:experiment:update <id>` | `rl-eu` | Update name/module (`--module`, `--name`, `--dry-run`) |
| `rl:experiment:delete <id>` | `rl-ed` | Delete experiment + all data (`--dry-run`) |

### Configuration

| Command | Alias | Purpose |
|---|---|---|
| `rl:config:get [key]` | `rl-cg` | Get one or all settings |
| `rl:config:set <key> <value>` | `rl-cs` | Set a setting with validation (`--dry-run`) |
| `rl:config:list` | `rl-cl` | List all settings with current values |
| `rl:config:reset` | `rl-cr` | Reset all settings to defaults (`--dry-run`) |
| `rl:event-log:clear` | `rl-elc` | Clear all snapshots (`--dry-run`) |

### Setup

| Command | Alias | Purpose |
|---|---|---|
| `rl:setup-ai` | `rl-sa` | Install AI skill files (`--host`, `--check`) |

## Configuration Keys

| Key | Type | Default | Description |
|---|---|---|---|
| `debug_mode` | boolean | false | Log Thompson Sampling scores |
| `enable_event_log` | boolean | true | Record snapshots for historical charts |
| `event_log_max_rows` | integer | 100000 | Max snapshot rows (1000–10000000) |
| `chart_line_threshold` | integer | 9 | Max variants for 2D line chart (2–50) |

## Workflow Examples

### Create and monitor a new A/B test
```bash
# Create experiment
drush rl:experiment:create hero_cta_test \
  --module=my_module \
  --name="Hero CTA Button Color Test"

# Check status after data collection
drush rl:status hero_cta_test

# Get detailed performance breakdown
drush rl:performance hero_cta_test --format=yaml

# Full analysis with recommendations
drush rl:analyze hero_cta_test
```

### Configure the module
```bash
# Enable debug logging temporarily
drush rl:config:set debug_mode true

# Increase snapshot storage
drush rl:config:set event_log_max_rows 500000

# Check all settings
drush rl:config:list
```

## Key Concepts

- **Experiment**: A multi-armed bandit test comparing content variants
- **Arm**: A single variant (identified by arm_id, often a node ID)
- **Turn/Impression**: One display of a variant to a visitor
- **Reward/Conversion**: A successful outcome (click, form submit, etc.)
- **Thompson Sampling**: Bayesian algorithm that balances
  exploration vs exploitation
- **Phase**: exploration, learning, exploitation, conclusive
- **Confidence**: Statistical confidence that the top
  performer is truly best

## Notes

- Experiments are tracked in custom database tables,
  not Drupal config entities
- The `rl.php` endpoint provides high-performance
  tracking with minimal Drupal bootstrap
- Arms are typically node IDs; the analyzer resolves
  them to node titles automatically
- Views management is handled by `drush_webmaster`
  (`wm:view:*` commands) — do not duplicate
