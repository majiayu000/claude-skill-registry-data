---
name: mlflow-python
description: >
  Log experiment metrics, parameters, and artifacts using MLflow Python API.
  Query and analyze runs with DataFrame operations. Use when user mentions
  "log backtest", "MLflow metrics", "experiment tracking", "log parameters",
  "search runs", "MLflow query", or needs to record strategy performance.
allowed-tools: Read, Bash, Grep, Glob
---

# MLflow Python Skill

Unified read/write MLflow operations via Python API with QuantStats integration for comprehensive trading metrics.

**ADR**: [2025-12-12-mlflow-python-skill](/docs/adr/2025-12-12-mlflow-python-skill.md)

## When to Use This Skill

**CAN Do**:

- Log backtest metrics (Sharpe, max_drawdown, total_return, etc.)
- Log experiment parameters (strategy config, timeframes)
- Create and manage experiments
- Query runs with SQL-like filtering
- Calculate 70+ trading metrics via QuantStats
- Retrieve metric history (time-series data)

**CANNOT Do**:

- Direct database access to MLflow backend
- Artifact storage management (S3/GCS configuration)
- MLflow server administration

## Prerequisites

### Authentication Setup

MLflow uses separate environment variables for credentials (NOT embedded in URI):

```bash
# Option 1: mise + .env.local (recommended)
# Create .env.local in skill directory with:
MLFLOW_TRACKING_URI=http://mlflow.eonlabs.com:5000
MLFLOW_TRACKING_USERNAME=eonlabs
MLFLOW_TRACKING_PASSWORD=<password>

# Option 2: Direct environment variables
export MLFLOW_TRACKING_URI="http://mlflow.eonlabs.com:5000"
export MLFLOW_TRACKING_USERNAME="eonlabs"
export MLFLOW_TRACKING_PASSWORD="<password>"
```

### Verify Connection

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
cd ${CLAUDE_PLUGIN_ROOT}/skills/mlflow-python
uv run scripts/query_experiments.py experiments
SKILL_SCRIPT_EOF
```

## Quick Start Workflows

### A. Log Backtest Results (Primary Use Case)

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF_2'
cd ${CLAUDE_PLUGIN_ROOT}/skills/mlflow-python
uv run scripts/log_backtest.py \
  --experiment "crypto-backtests" \
  --run-name "btc_momentum_v2" \
  --returns path/to/returns.csv \
  --params '{"strategy": "momentum", "timeframe": "1h"}'
SKILL_SCRIPT_EOF_2
```

### B. Search Experiments

```bash
uv run scripts/query_experiments.py experiments
```

### C. Query Runs with Filter

```bash
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "metrics.sharpe_ratio > 1.5" \
  --order-by "metrics.sharpe_ratio DESC"
```

### D. Create New Experiment

```bash
uv run scripts/create_experiment.py \
  --name "crypto-backtests-2025" \
  --description "Q1 2025 cryptocurrency trading strategy backtests"
```

### E. Get Metric History

```bash
uv run scripts/get_metric_history.py \
  --run-id abc123 \
  --metrics sharpe_ratio,cumulative_return
```

## QuantStats Metrics Available

The `log_backtest.py` script calculates 70+ metrics via QuantStats, including:

| Category     | Metrics                                                           |
| ------------ | ----------------------------------------------------------------- |
| **Ratios**   | sharpe, sortino, calmar, omega, treynor                           |
| **Returns**  | cagr, total_return, avg_return, best, worst                       |
| **Drawdown** | max_drawdown, avg_drawdown, drawdown_days                         |
| **Trade**    | win_rate, profit_factor, payoff_ratio, consecutive_wins/losses    |
| **Risk**     | volatility, var, cvar, ulcer_index, serenity_index                |
| **Advanced** | kelly_criterion, recovery_factor, risk_of_ruin, information_ratio |

See [quantstats-metrics.md](./references/quantstats-metrics.md) for full list.

## Bundled Scripts

| Script                  | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `log_backtest.py`       | Log backtest returns with QuantStats metrics |
| `query_experiments.py`  | Search experiments and runs (replaces CLI)   |
| `create_experiment.py`  | Create new experiment with metadata          |
| `get_metric_history.py` | Retrieve metric time-series data             |

## Configuration

The skill uses mise `[env]` pattern for configuration. See `.mise.toml` for defaults.

Create `.env.local` (gitignored) for credentials:

```bash
MLFLOW_TRACKING_URI=http://mlflow.eonlabs.com:5000
MLFLOW_TRACKING_USERNAME=eonlabs
MLFLOW_TRACKING_PASSWORD=<password>
```

## Reference Documentation

- [Authentication Patterns](./references/authentication.md) - Idiomatic MLflow auth
- [QuantStats Metrics](./references/quantstats-metrics.md) - Full list of 70+ metrics
- [Query Patterns](./references/query-patterns.md) - DataFrame operations
- [Migration from CLI](./references/migration-from-cli.md) - CLI to Python API mapping

## Migration from mlflow-query

This skill replaces the CLI-based `mlflow-query` skill. Key differences:

| Feature        | mlflow-query (old) | mlflow-python (new)    |
| -------------- | ------------------ | ---------------------- |
| Log metrics    | Not supported      | `mlflow.log_metrics()` |
| Log params     | Not supported      | `mlflow.log_params()`  |
| Query runs     | CLI text parsing   | DataFrame output       |
| Metric history | Workaround only    | Native support         |
| Auth pattern   | Embedded in URI    | Separate env vars      |

See [migration-from-cli.md](./references/migration-from-cli.md) for detailed mapping.
