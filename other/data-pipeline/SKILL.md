---
name: data-pipeline
description: "Builds automated sports analytics pipelines -- daily data pulls, scheduled prediction generation, model versioning, prediction tracking, and drift alerting. Use when user asks how to automate their model, how to run predictions every morning, how to set up a cron job for sports data, how to track model performance over time, or how to version their model. Do not use for one-time data pulls -- use game-lookup or puckapi-tool directly. Do not use for building the model itself -- see model-building. Do not use for backtesting historical performance -- see backtesting."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Data Pipeline

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Pipeline automation calls the same MCP endpoints used interactively. Daily NHL data pull: `get_games` (5) + `get_odds` (10/game) = ~125 credits per run (avg 12 games). Full season backfill: ~12,300 credits for odds.
> For building the prediction model that runs in the pipeline, see `model-building` first.

You are an expert in sports analytics automation. Your goal is to bridge the gap between "I built a model" and "my model runs every morning and I check results over coffee." This is where a school project becomes a system.

## When to Use

- "How do I automate my daily NHL picks?"
- "I want my model to run at 6 AM every morning"
- "How do I set up a GitHub Action for sports data?"
- "How do I track which model version made which prediction?"
- "When should I retrain my model?"
- "How do I detect if my model is drifting?"
- "I want to chain play-by-play + odds + injury data in one pipeline"

## When NOT to Use

- One-time data pulls -- use `puckapi-tool` or `game-lookup` directly
- Building the prediction model itself -- see `model-building`
- Validating a model's historical performance -- see `backtesting`
- Generating a one-time picks card -- see `daily-card`

## Commands Available

This skill does not call data tools directly. It generates pipeline code and configuration.

| Output Type | What It Produces |
|------------|-----------------|
| GitHub Actions YAML | Daily cron job for data pull and prediction generation |
| Python script | Data fetch + prediction generation skeleton |
| SQLite schema | Prediction tracking and actuals logging |
| Drift alert script | Detects accuracy drop or edge compression |
| Retrain trigger | Condition-based model refresh logic |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `schedule_pipeline` | Use GitHub Actions cron or system cron via the YAML below |
| `auto_retrain` | Implement retrain trigger logic manually (see Retrain Triggers section) |
| `get_injuries` | Injury data not available via `puckapi-tool`; integrate a separate source |
| `stream_live_data` | MCP is pull-only; schedule frequent polls instead of streaming |

## Initial Assessment

Before building the pipeline, understand:

1. **What does the pipeline need to produce?** Predictions only, or predictions + picks + reports?
2. **How often does it run?** Daily (most common), before each game window, or event-driven?
3. **Where do predictions get stored?** SQLite (local), Postgres, Google Sheets, or Notion?
4. **Does the model already exist?** If not, build it first via `model-building`.

## How It Works

### Step 1: Define the pipeline shape

The standard sports analytics pipeline has four stages:

```
[Schedule] -> [Data Pull] -> [Prediction] -> [Storage + Alert]
      |              |              |                |
   Cron job    puckapi-   Your model      SQLite /
   6 AM daily   tool API       .predict()      Sheets / API
```

### Step 2: Set up the GitHub Actions cron

The daily NHL pipeline:

```yaml
# .github/workflows/daily-nhl-pipeline.yml
name: Daily NHL Pipeline

on:
  schedule:
    - cron: '0 11 * * *'  # 6 AM ET = 11:00 UTC
  workflow_dispatch:       # Manual trigger for testing

jobs:
  run-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Pull today's games
        env:
          PUCKAPI_API_KEY: ${{ secrets.PUCKAPI_API_KEY }}
        run: python scripts/pull_games.py --date today

      - name: Pull odds
        env:
          PUCKAPI_API_KEY: ${{ secrets.PUCKAPI_API_KEY }}
        run: python scripts/pull_odds.py --date today

      - name: Generate predictions
        run: python scripts/generate_predictions.py --date today

      - name: Log predictions to SQLite
        run: python scripts/log_predictions.py --date today

      - name: Check for drift alert
        run: python scripts/drift_check.py --window 14

      - name: Commit results
        run: |
          git config --global user.email "pipeline@yourdomain.com"
          git config --global user.name "Pipeline Bot"
          git add data/ predictions/
          git commit -m "Daily pipeline: $(date +%Y-%m-%d)" || echo "Nothing to commit"
          git push
```

**Time to schedule:** NHL games are typically announced by noon ET. Run at 6 AM ET to catch morning lines, then again at noon to refresh odds before evening games if needed.

### Step 3: Data pull script skeleton

```python
# scripts/pull_games.py
#
# Data pulls use the PuckAPI MCP server, NOT a REST API.
# The MCP server must be connected to Claude via:
#   claude mcp add puckapi -- npx -y @anthropic-ai/sdk puckapi
# (or however the MCP server is configured in your project's .mcp.json)
#
# This script is meant to be run by Claude with the MCP server connected.
# Claude calls the MCP tools (get_games, get_odds, etc.) directly.
# The script below handles saving the results Claude returns.

import argparse
import json
import os
from datetime import date

def save_games(games: list, target_date: str):
    """Save game data returned by Claude's get_games MCP tool call."""
    output_path = f"data/games/{target_date}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump({
            "date": target_date,
            "pulled_at": date.today().isoformat(),
            "games": games
        }, f, indent=2)
    print(f"Saved {len(games)} games for {target_date}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="today")
    args = parser.parse_args()
    target = date.today().isoformat() if args.date == "today" else args.date
    # In practice, Claude calls get_games(date_from=target, date_to=target)
    # via MCP and passes the result to save_games().
    print(f"Run this via Claude with MCP connected:")
    print(f"  1. Claude calls get_games(date_from='{target}', date_to='{target}')")
    print(f"  2. Results are saved to data/games/{target}.json")
```

**How the MCP data pull works:**

There is no REST API endpoint. PuckAPI is an MCP server. To pull data:

1. **Connect the MCP server** to Claude Code: ensure `.mcp.json` has the puckapi server configured, or run `claude mcp add puckapi` with the appropriate command.
2. **Claude calls the MCP tools directly** -- `get_games(date_from="2026-01-15", date_to="2026-01-15")` returns today's games. No HTTP requests, no API keys in headers.
3. **Save the results** to local JSON/SQLite using a Python script that receives Claude's tool output.

For automated pipelines (GitHub Actions, cron), use `claude -p "Pull today's games using get_games and save to data/games/"` to invoke Claude headlessly with the MCP server attached.

```python
# scripts/generate_predictions.py
import argparse
import json
import pickle
from datetime import date

def generate_predictions(target_date: str):
    """Load model and generate predictions for today's games."""
    # Load the versioned model
    model_version = get_active_model_version()
    with open(f"models/{model_version}/model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Load today's games + features
    with open(f"data/games/{target_date}.json") as f:
        games_data = json.load(f)
    
    with open(f"data/odds/{target_date}.json") as f:
        odds_data = json.load(f)
    
    predictions = []
    for game in games_data["games"]:
        features = build_features(game, odds_data)
        home_win_prob = model.predict_proba([features])[0][1]
        
        predictions.append({
            "game_id": game["id"],
            "date": target_date,
            "home_team": game["home_team"],
            "away_team": game["away_team"],
            "home_win_prob": round(home_win_prob, 4),
            "model_version": model_version,
            "generated_at": date.today().isoformat()
        })
    
    output_path = f"predictions/{target_date}.json"
    with open(output_path, "w") as f:
        json.dump(predictions, f, indent=2)
    
    print(f"Generated {len(predictions)} predictions with model {model_version}")
    return predictions

def get_active_model_version() -> str:
    """Read the active model version from the registry."""
    with open("models/registry.json") as f:
        registry = json.load(f)
    return registry["active"]

def build_features(game: dict, odds_data: dict) -> list:
    """Build feature vector for one game. Implement your feature engineering here."""
    # Replace with your actual feature engineering
    raise NotImplementedError("Implement build_features with your model's inputs")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="today")
    args = parser.parse_args()
    from datetime import date as d
    target = d.today().isoformat() if args.date == "today" else args.date
    generate_predictions(target)
```

### Step 4: SQLite prediction tracking schema

```sql
-- predictions.db schema

CREATE TABLE IF NOT EXISTS predictions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id         TEXT NOT NULL,
    game_date       DATE NOT NULL,
    home_team       TEXT NOT NULL,
    away_team       TEXT NOT NULL,
    home_win_prob   REAL NOT NULL,         -- Model probability
    model_version   TEXT NOT NULL,         -- Version that made this prediction
    generated_at    TIMESTAMP NOT NULL,
    opening_odds    REAL,                  -- Market odds at prediction time
    closing_odds    REAL,                  -- Line at game time (fill later)
    actual_result   INTEGER,               -- 1 = home win, 0 = away win (fill after game)
    notes           TEXT
);

CREATE TABLE IF NOT EXISTS model_versions (
    version         TEXT PRIMARY KEY,
    trained_at      DATE NOT NULL,
    training_games  INTEGER NOT NULL,
    val_accuracy    REAL NOT NULL,
    val_auc         REAL NOT NULL,
    feature_set     TEXT NOT NULL,         -- JSON list of features
    is_active       INTEGER DEFAULT 0,
    notes           TEXT
);

CREATE TABLE IF NOT EXISTS drift_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    check_date      DATE NOT NULL,
    window_days     INTEGER NOT NULL,
    games_in_window INTEGER NOT NULL,
    accuracy        REAL NOT NULL,
    expected_acc    REAL NOT NULL,
    drift_flag      INTEGER DEFAULT 0,     -- 1 if alert triggered
    notes           TEXT
);

-- Useful query: rolling 14-day accuracy
SELECT 
    game_date,
    AVG(CASE WHEN actual_result = ROUND(home_win_prob) THEN 1.0 ELSE 0.0 END) 
        OVER (ORDER BY game_date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS rolling_14d_acc
FROM predictions
WHERE actual_result IS NOT NULL
ORDER BY game_date;
```

### Step 5: Model versioning

```python
# models/registry.json -- update manually or via script after training
{
    "active": "v2.1.0",
    "versions": [
        {
            "version": "v1.0.0",
            "trained": "2025-10-01",
            "val_accuracy": 0.563,
            "features": ["cf_pct", "pdo", "rest_days"],
            "retired": "2025-12-15"
        },
        {
            "version": "v2.0.0",
            "trained": "2025-12-15",
            "val_accuracy": 0.571,
            "features": ["cf_pct", "xgf_pct", "pdo", "rest_days", "h2h_last5"],
            "retired": "2026-01-20"
        },
        {
            "version": "v2.1.0",
            "trained": "2026-01-20",
            "val_accuracy": 0.579,
            "features": ["cf_pct", "xgf_pct", "pdo", "rest_days", "h2h_last5", "back_to_back"],
            "is_active": true
        }
    ]
}
```

**Versioning rule:** Never overwrite a model file. Each `train_model.py` run outputs a new version directory: `models/v2.2.0/model.pkl`. Update `registry.json` to promote it to active.

### Step 6: Retrain triggers

When to retrain (pick the condition that fits your workflow):

| Condition | Trigger | Action |
|-----------|---------|--------|
| Calendar-based | Monthly, on the 1st | Run `train_model.py` with last 2 seasons of data |
| Game count | Every 50 new games | Rolling window retrain |
| Accuracy drop | 14-day accuracy falls below (expected - 3pp) | Urgent retrain + review feature importance |
| New season | October 1st | Full retrain on completed season |
| Line movement | Average CLV drops below 0% for 30 days | Model is predicting the line, not beating it |

**Do not retrain** on a bad week alone. Variance kills accurate-but-unlucky models. Require 2-3 consecutive trigger conditions before retraining mid-season.

### Step 7: Drift alerting

```python
# scripts/drift_check.py
import sqlite3
import argparse

DRIFT_THRESHOLD = 0.03  # Alert if accuracy drops 3pp below expected

def check_drift(window_days: int = 14):
    conn = sqlite3.connect("predictions.db")
    
    query = """
        SELECT 
            COUNT(*) as games,
            AVG(CASE WHEN actual_result = ROUND(home_win_prob) THEN 1.0 ELSE 0.0 END) as accuracy
        FROM predictions
        WHERE actual_result IS NOT NULL
          AND game_date >= DATE('now', '-{} days')
    """.format(window_days)
    
    result = conn.execute(query).fetchone()
    games, accuracy = result
    
    # Load expected accuracy from active model's validation score
    expected_acc = get_expected_accuracy()
    
    drift_detected = accuracy < (expected_acc - DRIFT_THRESHOLD)
    
    conn.execute("""
        INSERT INTO drift_log (check_date, window_days, games_in_window, accuracy, expected_acc, drift_flag)
        VALUES (DATE('now'), ?, ?, ?, ?, ?)
    """, (window_days, games, accuracy, expected_acc, int(drift_detected)))
    conn.commit()
    
    if drift_detected:
        print(f"DRIFT ALERT: {window_days}-day accuracy {accuracy:.1%} vs expected {expected_acc:.1%}")
        print(f"Games in window: {games}. Consider retraining if this persists.")
        # Optionally: send email, Slack message, or GitHub issue
    else:
        print(f"No drift detected: {window_days}-day accuracy {accuracy:.1%} (expected {expected_acc:.1%})")

def get_expected_accuracy() -> float:
    import json
    with open("models/registry.json") as f:
        registry = json.load(f)
    active = registry["active"]
    for v in registry["versions"]:
        if v["version"] == active:
            return v["val_accuracy"]
    return 0.55  # Fallback

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=int, default=14)
    args = parser.parse_args()
    check_drift(args.window)
```

### Step 8: Multi-source MCP orchestration

When chaining play-by-play + odds + team stats in one pipeline run:

```python
# scripts/pull_all_sources.py
import asyncio

async def pull_all_data(target_date: str):
    """Pull from multiple sources in parallel. Fail gracefully on any source."""
    
    tasks = [
        pull_games(target_date),          # 5 credits
        pull_odds(target_date),            # 10 credits per game
        pull_team_stats(target_date),      # 5 credits per team
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    games, odds, team_stats = results
    
    # Graceful degradation: proceed even if one source fails
    if isinstance(odds, Exception):
        print(f"WARNING: Odds pull failed: {odds}. Proceeding without odds data.")
        odds = {}
    
    if isinstance(team_stats, Exception):
        print(f"WARNING: Team stats pull failed: {team_stats}. Using cached stats.")
        team_stats = load_cached_team_stats()
    
    return games, odds, team_stats
```

**Credit cost for a full daily NHL run:**
- `get_games` (today's slate): 5 credits
- `get_odds` (per game, ~12 games/day average): 120 credits
- `get_team_stats` (per team, 32 teams): 160 credits
- **Total: ~285 credits per day | ~104,000 per full season**

Consider caching team stats (update weekly, not daily) to cut this to ~125 credits/day for games + odds only.

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll just run the script manually each morning" | You'll miss days, break the streak, and lose comparable data | Set up the cron/Actions now, even if imperfect |
| "I'll overwrite the model file each time I retrain" | Lose the ability to audit which model made which prediction | Version every model, update registry.json to promote |
| "Drift means I need to retrain immediately" | One bad week is variance, not drift | Require 14-day window AND 3pp drop before acting |
| "I'll track predictions in a spreadsheet" | Manual entry breaks, doesn't scale, no query layer | SQLite takes 30 minutes to set up, lasts forever |
| "I'll pull full season odds every day for backtesting" | 1,230+ credits for historical odds; wasteful if you already have them | Backfill once, store locally, pull only new games daily |

## Credit Usage

| Operation | Credits | Notes |
|-----------|---------|-------|
| Daily games pull | 5 | One `get_games` call |
| Daily odds (per game) | 10 | Average 12 NHL games/day = 120 credits |
| Team stats (32 teams) | 160 | 5 credits x 32 teams; cache weekly, not daily |
| Line movement check | 25 | Per game; use sparingly |
| Full season historical odds backfill | ~12,300 | ~1,230 regular season games x 10 credits |

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Pipeline is built and running | Automate your daily picks output | `daily-card` |
| Model accuracy is drifting | Audit recent predictions against actuals | `backtesting` |
| Drift confirmed, need to improve features | Re-engineer features with updated data | `feature-engineering` |
| Want to retrain the model | Full model rebuild with new training data | `model-building` |
| Want to track edge compression over time | Compare model probability vs. closing line | `edge-detection` |
