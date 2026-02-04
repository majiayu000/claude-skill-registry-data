---
name: review-game-log
description: Automatically invoked when reviewing game simulation logs. Retrieves saved game data by ID and formats it for analysis.
---

# Review Game Log Skill

This skill activates when you need to review a saved MTG game simulation log.

## When This Skill Activates

Automatically engage when:
- User asks to review a game log by ID
- User wants to analyze a saved game
- User provides a game ID (UUID format) and asks about game events

## Workflow

### 1. Identify Game ID

The game ID is a UUID like `a1b2c3d4-e5f6-7890-abcd-ef1234567890`. Users may provide:
- Full UUID
- Partial UUID (first 8 characters)
- Reference like "the game I just saved"

### 2. Fetch Game Data

Use the Bash tool to invoke the Tauri command via the app's API or read directly from the SQLite database:

```bash
# Option 1: Query SQLite directly (preferred for Claude)
sqlite3 ~/.local/share/com.scrye3.app/scrye3.db "
SELECT
  s.game_id,
  s.player1_name,
  s.player2_name,
  s.winner,
  s.final_turn,
  s.total_log_entries,
  s.saved_at
FROM saved_games s
WHERE s.game_id LIKE 'GAME_ID_PREFIX%'
LIMIT 1;
"

# Then fetch logs
sqlite3 ~/.local/share/com.scrye3.app/scrye3.db "
SELECT
  timestamp,
  event_type,
  turn_number,
  phase,
  step,
  message,
  details
FROM game_logs
WHERE game_id = 'FULL_GAME_ID'
ORDER BY timestamp ASC, id ASC;
"
```

### 3. Format Output

Present the game summary and key events:

```
## Game Summary
- **Game ID**: {game_id}
- **Players**: {player1_name} vs {player2_name}
- **Result**: {winner} won on turn {final_turn}
- **Total Events**: {total_log_entries}
- **Saved**: {saved_at}

## Key Events

| Turn | Phase | Event | Details |
|------|-------|-------|---------|
| 1 | beginning | Game started | ... |
| 1 | precombat_main | Land played | Forest |
| ... | ... | ... | ... |
```

### 4. Analysis

After presenting the log, offer to:
- Summarize the game flow
- Identify key turning points
- Analyze player decisions
- Find specific events (combat, spells cast, etc.)

## Constraints

- Only access games that have been explicitly saved
- Game logs are read-only (cannot modify saved games)
- Database path may vary by platform:
  - Linux: `~/.local/share/com.scrye3.app/scrye3.db`
  - macOS: `~/Library/Application Support/com.scrye3.app/scrye3.db`
  - Windows: `%APPDATA%/com.scrye3.app/scrye3.db`

## Examples

**User**: "Review game a1b2c3d4"

**Claude**:
1. Query database for game starting with `a1b2c3d4`
2. Present summary and log table
3. Offer analysis options

**User**: "What happened in turn 5 of that game?"

**Claude**:
1. Filter logs for turn_number = 5
2. Present relevant events
3. Explain the game state
