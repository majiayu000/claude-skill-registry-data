---
name: fitness-tracker
description: Log and analyze workouts. Use when the user wants to (1) record a workout at the gym via conversation, (2) parse workout markdown files to CSV, (3) query exercise history with DuckDB, or (4) track fitness progress. Triggers on "log workout", "record workout", "track workout", "add exercises", "what did I lift", etc.
---

# Fitness Tracker

Log workouts via conversation and save to github and analyze workout data with DuckDB.

## Chat Mode - Logging Workouts

Use this conversational flow when the user wants to record a workout:

### Step 1: Date
Ask for the workout date or default to today. Format: YYYY-MM-DD

### Step 2: Muscle Group
Ask what they're working. Categories from `reference/exercises.md`:
- Chest, Back, Shoulders, Legs
- Arms - Biceps, Arms - Triceps
- Core, Compound, Cardio

### Step 3: Exercise Selection
Show exercises from that category. Let user pick or type their own.

### Step 4: Sets Entry
User enters sets naturally:
- "135 for 10, 10" → `- 135 - 10, 10`
- "185 - 8, 8, 8" → `- 185 - 8, 8, 8`
- "10, 10, 10" (bodyweight) → `- 10, 10, 10`
- "30 minutes" (cardio) → `- 30m`
- Add "warmup" or other notes as `// comment`

### Step 5: More Exercises?
Ask if they want to add another exercise. Repeat steps 2-4 as needed.

### Step 6: Save
Save the workout to GitHub (or Obsidian as fallback):
- File: `YYYY-MM-DD.md` (one file per day, e.g., `2026-01-02.md`)
- If file exists, append new exercises (multiple workouts per day are supported)
- Push to GitHub using `scripts/github_sync.py`

### Example Conversation
```
User: Log my workout
Claude: What date? (default: today, 2026-01-02)
User: Today
Claude: What are you working? (Chest, Back, Shoulders, Legs, Arms, Core, Cardio)
User: Chest
Claude: Chest exercises: Bench Press, Incline Bench Press, Dumbbell Press, Cable Flyes, Push-ups, Dips...
User: Bench
Claude: Enter your sets (e.g., "135 - 10, 10" or "185 for 8, 8, 8"):
User: 135 for 10, 10 warmup, then 185 - 8, 8, 8
Claude: Got it:
  Bench Press
  - 135 - 10, 10 // warmup
  - 185 - 8, 8, 8

  Another exercise?
User: Cable flyes, 30 - 12, 12, 12
Claude: Added. Another exercise?
User: Done
Claude: Saved to 2026-01-02.md
```

## Workout File Format

Files are named `YYYY-MM-DD.md` (one file per day). Multiple workouts in a day append to the same file.

Example: `2026-01-02.md`
```markdown
Bench
- 135 - 10, 10 // warmup
- 185 - 8, 8, 8

Situps
- 10, 10, 10

Treadmill
- 30m
```

### Format Rules

- **Filename**: `YYYY-MM-DD.md` (date is in the filename)
- **Exercise name**: Plain text on its own line
- **Weighted sets**: `- weight - reps, reps, reps` (e.g., `- 185 - 8, 8, 8`)
- **Bodyweight sets**: `- reps, reps, reps` (e.g., `- 10, 10, 10`)
- **Duration**: `- 30m` or `- 1h30m`
- **Notes**: `// comment` at end of line

## Configuration

Edit `scripts/config.json` to configure GitHub (default) or Obsidian storage:

```json
{
  "github_repo": "username/repo-name",
  "github_token": "github_pat_xxxxx",
  "github_branch": "main",
  "github_workout_dir": "workouts",
  "obsidian_workout_dir": "/path/to/obsidian/vault/Fitness"
}
```

### GitHub Configuration (Default)
- `github_repo`: Your repository in `username/repo-name` format
- `github_token`: Personal Access Token with `repo` scope. Create at: https://github.com/settings/tokens
- `github_branch`: Target branch (default: `main`)
- `github_workout_dir`: Directory in repo for workout files (default: `workouts`)

### Obsidian Configuration (Fallback)
- `obsidian_workout_dir`: Local path to Obsidian vault directory (used if GitHub not configured)

## Writing Workout Files

When saving workouts in chat mode:

### GitHub Workflow

**Important:** Must `cd` into the scripts directory so `github_sync.py` can find `config.json`.

#### Step 1: Fetch existing file from GitHub (if any)

```bash
cd /mnt/skills/user/fitness-tracker/scripts
uv run github_sync.py --fetch workouts/2026-01-02.md > /tmp/2026-01-02.md
```

If the file doesn't exist yet, create it empty.

#### Step 2: Append exercises to the local file

```bash
cat >> /tmp/2026-01-02.md << 'EOF'

Pull-ups
- 10, 10, 10
EOF
```

#### Step 3: Push back to GitHub

```bash
cd /mnt/skills/user/fitness-tracker/scripts
uv run github_sync.py \
  --file /tmp/2026-01-02.md \
  --dest workouts/2026-01-02.md \
  -m "Add workout for 2026-01-02"
```

#### Step 4: Update CSV

Fetch existing CSV, parse the new workout, and update:

```bash
cd /mnt/skills/user/fitness-tracker/scripts
uv run github_sync.py --fetch workouts/workouts.csv > /tmp/workouts.csv
uv run parse_workout.py /tmp/2026-01-02.md -o /tmp/workouts.csv --append
uv run github_sync.py \
  --file /tmp/workouts.csv \
  --dest workouts/workouts.csv \
  -m "Update workout data"
```

The `--append` flag replaces rows for the parsed date(s) while keeping other dates intact.

### Obsidian (Fallback)

If GitHub is not configured (`github_repo` is empty):
1. Use `obsidian_workout_dir` from config
2. Target file: `{obsidian_workout_dir}/YYYY-MM-DD.md`
3. Use Obsidian MCP tools or write directly to filesystem

## Parse Mode - Analyzing Workouts

```bash
# Parse all daily workout files in a directory
uv run scripts/parse_workout.py /path/to/workouts/ -o workouts.csv

# Parse a single day and update existing CSV (replaces that date's rows)
uv run scripts/parse_workout.py /tmp/2026-01-02.md -o workouts.csv --append

# Parse and run a query
uv run scripts/parse_workout.py /path/to/workouts/ --query "SELECT * FROM workouts"
```

The parser matches files named `YYYY-MM-DD.md` and extracts the date from the filename.

## Exercise Validation

The parser checks exercise names against `reference/exercises.md` and suggests corrections for typos:

```
Unrecognized exercises:
  'Bech Press' - did you mean 'Bench Press'?
  'Squatts' - did you mean 'Squats'?
```

Add new exercises to `reference/exercises.md` to expand the known list.

## Output CSV Schema

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Workout date (YYYY-MM-DD) |
| exercise | VARCHAR | Exercise name |
| set_num | INTEGER | Set number within exercise |
| weight | DECIMAL | Weight used (empty for bodyweight) |
| reps | INTEGER | Rep count (empty for duration exercises) |
| duration_min | INTEGER | Duration in minutes (for timed exercises) |
| notes | VARCHAR | Comments from `// note` |

## Example Queries

```sql
-- Total volume per exercise
SELECT exercise, SUM(weight * reps) as volume
FROM workouts GROUP BY exercise ORDER BY volume DESC;

-- Bench press max weight over time
SELECT date, MAX(weight) as max_weight
FROM workouts WHERE exercise = 'Bench' GROUP BY date;

-- Weekly workout frequency
SELECT DATE_TRUNC('week', date) as week, COUNT(DISTINCT date) as days
FROM workouts GROUP BY 1 ORDER BY 1;

-- Exercises by total sets
SELECT exercise, COUNT(*) as total_sets
FROM workouts GROUP BY exercise ORDER BY total_sets DESC;
```
