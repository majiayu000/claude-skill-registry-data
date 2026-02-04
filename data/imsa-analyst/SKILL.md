---
name: IMSA Analyst
description: use to query historical data on the IMSA Weathertech seasons
---

# IMSA Data Analysis Skill

## Purpose
Analyze IMSA racing data from the DuckDB database providing insights into lap times, driver performance, team comparisons, weather impacts, and race strategies.

# Query

Query with the skill included `./query.sh "SELECT 1"`. Schema can be found in ./schema.md

**Output Formats:**
- Default: Markdown tables (`-markdown` flag)
- CSV Use `./query.sh --csv "SELECT ..."` for token-efficient output with large result sets

You may have to use --remote parameter to access the database, and that may require the use of INSTALL httpfs if its not already there. You will figure it out.

## Quick Reference: Standard Analysis Workflow

1. **Find your session**: `WHERE event = 'X' AND session = 'race'` → get `session_id`
2. **Pick your class**: GTP, LMP2, or GTD - analyze each separately
3. **Filter properly**: `WHERE session_id = X AND class = 'Y' AND flags = 'GF' AND lap_time_driver_quartile IN (1, 2)`
4. **Never compare lap times across different tracks (events), and usually you should avoid comparing between different session_ids because the conditions change. 
5. **Never compare between different classes**
6. **Always default to `session = 'race'` and top 50% of laps unless asked otherwise**
7. **Percentages are not often useful**: In racing we want to see the difference in timespans (seconds down to the hundredths). Sometimes percentages are useful, in these cases just include both. 

## ⚠️ CRITICAL CONSTRAINTS

### 1. Sessions Are the Unit of Comparison
**Always compare within a single `session_id`**. A session_id uniquely identifies one specific session (e.g., "2025 Sebring Race"). Laps from different sessions should NOT be compared directly.

✅ **DEFAULT**: Filter by `session_id` (captures year, event, session, start_date)
❌ **AVOID**: Comparing across multiple session_ids without explicit reason

It's a good idea to start with querying the seasons table at the beginning. Example: 

```bash
./query "SELECT * FROM seasons WHERE session = 'race' AND season in (2024,2025) ORDER BY date"
```

### 2. Race Sessions Are What Matter
**Default to `session = 'race'` unless specifically asked otherwise**. Practice and qualifying have different objectives, tire strategies, and fuel loads.

✅ **ALWAYS**: Start with race sessions  
⚠️ **ONLY IF ASKED**: Look at practice or qualifying data

### 3. Classes Within Sessions Are NOT Comparable
**GTP ≠ LMP2 ≠ GTD** even in the same session. Different classes have completely different car specs and performance. 

❌ **NEVER**: Compare GTP times to GTD times  
✅ **ALWAYS**: Analyze each class separately within the session

### 4. Averages Require Session Context
When calculating average lap times, **ALWAYS filter to a single session_id AND class**. Averaging across sessions or classes produces meaningless numbers.

**The Golden Filtering Rule:**
```sql
WHERE session_id = X                     -- Single session
  AND class = 'Y'                        -- Single class
  AND bpillar_quartile IN (1, 2)         -- BPillar top 50% (race sessions only)
```

### 5. Focus on Representative Performance
**For performance analysis, use BPillar filtering** - automatically excludes pit laps, first lap, slow laps, and traffic.

✅ **ALWAYS**: Filter to `bpillar_quartile IN (1, 2)` for pace analysis in races
✅ **ALTERNATIVE**: Use `lap_time_driver_quartile IN (1, 2)` for non-race sessions
❌ **AVOID**: Including quartiles 3 and 4 when analyzing true pace

The `bpillar_quartile` column (race sessions only) intelligently filters laps:
- **Automatically excludes**: First lap of race, pit in/out laps
- **Speed requirements**: Within 110% of class fastest AND 105% of driver's fastest
- **Quartile 1** = Fastest 25% of qualifying laps (BEST)
- **Quartile 2** = 25-50% percentile of qualifying laps (still good)
- **Quartile 3** = 50-75% percentile (slower, ignore for performance)
- **Quartile 4** = Slowest 25% (ignore for performance)
- **NULL** = Non-race sessions or laps that don't meet BPillar criteria

By filtering to `bpillar_quartile IN (1, 2)`, you get only clean, representative racing pace.

### 6. What IS Valid Across Sessions?
While lap times aren't comparable across sessions, these analyses ARE valid:
- **Participation tracking**: Which drivers/teams competed in which races
- **Results and standings**: Race finishes, points, championships
- **Reliability metrics**: DNF rates, mechanical issues across the season
- **Strategy patterns**: Average number of pit stops, stint lengths (as counts, not times)
- **Relative performance**: "% off pole" or "gap to leader" within each session
- **Career statistics**: Number of races, podiums, wins (not absolute lap times)
- **Consistency trends**: Is a driver's CV improving session-to-session? (calculate per session, then compare)

⚠️ **Still not valid**: Averaging lap times across different sessions, even with quartile filtering. Each session must be analyzed independently first.

Example valid cross-session query:
```sql
-- Races participated by driver (not comparing lap times!)
SELECT 
    driver_name,
    COUNT(DISTINCT session_id) as race_count,
    COUNT(DISTINCT event) as unique_venues,
    STRING_AGG(DISTINCT event, ', ' ORDER BY event) as events_raced
FROM laps
WHERE year = '2025' 
    AND session = 'race'
GROUP BY driver_name
ORDER BY race_count DESC;
```

## Core Capabilities

### 1. Lap Time Analysis
- **Fastest Laps**: Identify fastest laps by driver, class, session
- **Representative Pace**: Focus on top 50% or 25% of laps to eliminate traffic/mistakes
- **Consistency**: Calculate standard deviation and variance in clean lap times
- **Progression**: Track how lap times evolve over a stint or session
- **Comparative Analysis**: Compare drivers or teams within same session/class

### 2. Driver Performance
- **Driver Rankings**: Rank drivers by fastest lap, average pace, consistency
- **Stint Analysis**: Analyze driver performance across multiple stints
- **Head-to-Head**: Compare teammate performance or class rivals
- **License Impact**: Correlate license levels with performance
- **Driver Identification**: Use `driver_id` (VARCHAR) for stable identification across name variants

### 3. Team & Strategy Analysis
- **Pit Stop Timing**: Analyze pit stop durations and strategy windows
- **Stint Length**: Optimal stint durations by class, conditions, fuel strategy
- **Driver Rotation**: Track driver changes and their impact on pace
- **Race Strategy**: Identify caution windows, undercuts, overcuts

### 4. Weather Correlation
- **Temperature Impact**: How air/track temp affects lap times
- **Rain Performance**: Identify strong wet-weather drivers/teams
- **Condition Changes**: Track pace changes as conditions evolve
- **Optimal Conditions**: Find ideal temperature/humidity windows

### 5. Track-Specific Insights
- **Venue Comparison**: Compare performance across different tracks
- **Track Records**: Identify fastest times at each venue
- **Sector Analysis**: Deep dive into S1, S2, S3 performance
- **Track Evolution**: How the track improves over a session

## Essential Queries

### Finding the Right Session
```sql
-- First, identify the session_id you want to analyze
SELECT 
    session_id,
    year,
    event,
    session,
    start_date,
    COUNT(*) as total_laps,
    COUNT(DISTINCT class) as classes
FROM laps
WHERE year = '2025'
    AND event = 'Sebring'
    AND session = 'race'  -- almost always race
GROUP BY session_id, year, event, session, start_date
ORDER BY start_date;
```

### Finding Driver IDs
```sql
-- driver_id is a string like 'firstname lastname' - look up by name first
SELECT DISTINCT driver_id, driver_name
FROM laps
WHERE driver_name LIKE '%Beche%'  -- partial match
ORDER BY driver_name;
```

### Time Formatting Macro
Always use this macro for human-readable times:
```sql
CREATE OR REPLACE MACRO format_time(t) AS (
    CASE
        WHEN t > 3600 THEN STRFTIME('%H:%M:%S', MAKE_TIMESTAMP(CAST(t * 1000000 AS BIGINT))) || '.' || LPAD(CAST(FLOOR((t * 1000) % 1000) AS VARCHAR), 3, '0')
        ELSE STRFTIME('%M:%S', MAKE_TIMESTAMP(CAST(t * 1000000 AS BIGINT))) || '.' || LPAD(CAST(FLOOR((t * 1000) % 1000) AS VARCHAR), 3, '0')
    END
);
```

### Fastest Lap in a Session
```sql
-- Get fastest laps per class in a specific race session
SELECT
    driver_name,
    team_name,
    car,
    class,
    format_time(lap_time) AS lap_time,
    lap AS lap_number
FROM laps
WHERE session_id = 12345              -- ← Use the session_id from query above
    AND class = 'GTP'                 -- ← Analyze each class separately
    AND bpillar_quartile IN (1, 2)    -- BPillar top 50% (auto-excludes pit/slow laps)
ORDER BY lap_time ASC
LIMIT 10;
```

### Driver Consistency Analysis
```sql
-- Compare drivers within a single race session using their best laps
SELECT
    driver_name,
    COUNT(*) AS total_laps,
    format_time(MIN(lap_time)) AS fastest,
    format_time(AVG(lap_time)) AS average,
    format_time(STDDEV(lap_time)) AS std_dev,
    ROUND(STDDEV(lap_time) / AVG(lap_time) * 100, 2) AS cv_percent
FROM laps
WHERE session_id = 12345                    -- ← Single session only
    AND class = 'GTP'                       -- ← Single class only
    AND bpillar_quartile IN (1, 2)          -- BPillar top 50% representative pace
GROUP BY driver_name
HAVING COUNT(*) >= 5                        -- Minimum lap sample for bpillar top 50%
ORDER BY cv_percent ASC;
```

### Pit Stop Analysis
```sql
-- Analyze pit stops in a specific race
SELECT 
    driver_name,
    team_name,
    car,
    lap,
    format_time(pit_time) AS pit_duration,
    session_time_lap_number
FROM laps
WHERE session_id = 12345    -- ← Single race session
    AND pit_time IS NOT NULL
ORDER BY pit_time ASC
LIMIT 20;
```

### Weather Impact on Pace
```sql
-- Weather effects within a single race session and class
SELECT
    CAST(track_temp_f / 10 AS INT) * 10 AS temp_bucket,
    COUNT(*) AS laps,
    format_time(AVG(lap_time)) AS avg_lap_time,
    format_time(MIN(lap_time)) AS fastest_lap
FROM laps
WHERE session_id = 12345                    -- ← Single race session
    AND class = 'GTP'                       -- ← Single class
    AND bpillar_quartile IN (1, 2)          -- BPillar representative performance
    AND track_temp_f IS NOT NULL
GROUP BY temp_bucket
ORDER BY temp_bucket;
```

### Stint Performance Degradation
```sql
-- Track tire degradation for a specific driver in a race
-- NOTE: Using ALL laps here to see full degradation curve
SELECT
    driver_name,
    stint_number,
    stint_lap,
    format_time(lap_time) AS lap_time,
    lap_time_driver_quartile,
    session_time_lap_number
FROM laps
WHERE session_id = 12345              -- ← Single race session
    AND driver_id = 'tobi lutke'      -- ← Use driver_id string (e.g., 'firstname lastname')
    AND lap_time IS NOT NULL
    AND flags = 'GF'                  -- Green flag only to exclude cautions
ORDER BY stint_number, stint_lap;

-- Alternative: Focus only on clean, representative laps
-- WHERE ... AND lap_time_driver_quartile IN (1, 2)
```

### Head-to-Head Teammate Comparison
```sql
-- Compare teammates in a single race session using representative pace
WITH teammate_stats AS (
    SELECT
        driver_name,
        team_name,
        COUNT(*) AS laps,
        MIN(lap_time) AS fastest,
        AVG(lap_time) AS average
    FROM laps
    WHERE session_id = 12345              -- ← Single race session
        AND team_name = 'Porsche Penske Motorsport'
        AND bpillar_quartile IN (1, 2)    -- BPillar top 50% pace
    GROUP BY driver_name, team_name
)
SELECT
    driver_name,
    laps,
    format_time(fastest) AS fastest_lap,
    format_time(average) AS avg_lap,
    format_time(average - (SELECT MIN(average) FROM teammate_stats)) AS gap_to_fastest,
    ROUND((average - (SELECT MIN(average) FROM teammate_stats)), 3) AS gap_seconds
FROM teammate_stats
ORDER BY average;
```

## Best Practices

### 1. Filter Strategy (CRITICAL)
- **ALWAYS filter by session_id**: This is your primary key for any lap time analysis
- **Default to race sessions**: Use `session = 'race'` unless specifically asked for practice/qualifying
- **ALWAYS filter by class**: GTP/LMP2/GTD must be analyzed separately
- **ALWAYS filter to top laps**: Use `lap_time_driver_quartile IN (1, 2)` for representative pace
- **The golden rule**: `WHERE session_id = X AND class = 'Y' AND lap_time_driver_quartile IN (1, 2)`
- **Then filter on flags**: Use `flags = 'GF'` for clean lap comparisons
- **Exception - degradation analysis**: When studying tire wear or stint degradation, you may want all laps

### 2. Aggregation Tips
- **Focus on representative laps**: Filter to top 50% or 25% for pace analysis
- **Averages require session context**: NEVER average lap times across different session_ids
- **Adjust sample sizes**: When using top 50% filter, ~10 laps minimum; without filter, ~20 laps minimum
- **Time formatting**: Always format times for human output using the macro
- **NULL handling**: Many fields can be NULL; use `IS NOT NULL` filters
- **Class separation**: Each class must be aggregated independently
- **Green flag only**: For pace analysis, use `flags = 'GF'` to exclude caution laps

### 3. Performance Optimization
- **Use session_id**: Single most efficient filter for partitioning data
- **Use bpillar_quartile**: Pre-calculated, indexed, and contains all necessary filters
- **Avoid cross-session queries**: Rarely needed and computationally expensive
- **Leverage year views**: Use `laps_2025` instead of `WHERE year = '2025'` if available
- **Sector queries**: S1/S2/S3 times can have NULLs; always check
- **Weather is pre-joined**: No need for separate lookups
- **Index-friendly filters**: session_id, then class, then bpillar_quartile

### 4. Common Gotchas
- **🚨 MOST IMPORTANT**: Use session_id for all lap time comparisons - never compare across sessions
- **🚨 SECOND MOST IMPORTANT**: Almost always use `session = 'race'` unless explicitly asked otherwise
- **🚨 THIRD MOST IMPORTANT**: Filter to `bpillar_quartile IN (1, 2)` for race pace analysis
- **driver_id is VARCHAR**: Use string values like `driver_id = 'tobi lutke'`, not numeric IDs
- **Car numbers are strings**: `'01'` ≠ `'1'` - use exact matches
- **stint_lap is 0-indexed**: First lap after driver change is lap 0
- **session_time_lap_number**: Tracks leader's progress, not individual car laps
- **Driver IDs vs names**: Use `driver_id` (VARCHAR) for joins/filters, `driver_name` for display
- **Practice ≠ Race**: Different fuel loads, tire strategies, and objectives
- **bpillar_quartile is NULL for non-race sessions**: Use `lap_time_driver_quartile` for practice/qualifying
- **BPillar automatically handles filtering**: No need to manually exclude pit laps, first lap, or slow laps

## Investigation Workflows

### Before Any Lap Time Analysis - Validation Checklist
✅ Have I identified the specific session_id?
✅ Have I specified a single class?
✅ Am I using `session = 'race'` (unless specifically asked for practice/qualifying)?
✅ Have I filtered to `bpillar_quartile IN (1, 2)` for race analysis?
✅ Am I only comparing lap times within these boundaries?
✅ For averages, am I filtering to one session_id + one class + bpillar quartiles 1-2?

### New Event Analysis
1. Find the race session: 
   ```sql
   SELECT session_id, start_date, COUNT(*) as laps
   FROM laps 
   WHERE event = 'Sebring' AND year = '2025' AND session = 'race'
   GROUP BY session_id, start_date;
   ```
2. Identify classes in that session:
   ```sql
   SELECT DISTINCT class FROM laps WHERE session_id = X;
   ```
3. **Analyze each class separately** - pull fastest laps per class
4. Analyze weather conditions during race (per class)
5. Review pit strategies and stint lengths (per class)

### Driver Deep Dive
1. Find all race sessions for driver:
   ```sql
   SELECT DISTINCT session_id, event, year, class
   FROM laps
   WHERE driver_id = 'tobi lutke' AND session = 'race'  -- driver_id is VARCHAR
   ORDER BY year, event;
   ```
2. For each session_id + class combination:
   - Calculate pace statistics (using top 50% laps)
   - Compare to teammates and class competitors
   - Identify strongest/weakest sectors
   - Analyze consistency metrics (CV, std dev)
3. Look for patterns across multiple sessions (but analyze each session independently first)

### Strategy Investigation (for a specific race session)
1. Set your session_id: Focus on one race at a time
2. Map pit windows: When did leaders pit? (filter by class)
3. Compare stint lengths across teams in that class
4. Identify caution periods (`flags = 'FCY'` or similar)
5. Calculate time gained/lost in pits
6. Assess undercut/overcut opportunities within the session

### Weather Analysis (for a specific race session)
1. Choose a session_id and class to analyze
2. Correlate lap times with temperature buckets within that session
3. Identify rain periods (`raining = TRUE`) during the session
4. Compare pace across dry/wet conditions (same session, same class)
5. Track tire degradation in heat (stint analysis)
6. Find optimal operating windows for that track/class combination

## Output Formatting

### For Human Consumption
- Format all times: `format_time(lap_time)`
- Round percentages: `ROUND(x, 2)`
- Use descriptive aliases: `AS fastest_lap`, not `AS fl`
- Sort meaningfully: Usually by time ASC or lap count DESC
- Limit results: Top 10-20 unless specifically asked for more

### For Further Analysis
- Include row counts and sample sizes
- Provide both absolute and relative metrics
- Show distribution statistics (min, max, avg, stddev)
- Include confidence indicators (lap counts, conditions)
- Note any data quality issues or missing values

## Common Analysis Requests

**"Who's fastest at [track]?"**
→ Find the race session_id, then query fastest laps per class (use top 50% filter)

**"Who won the [event] race?"**
→ Valid question - find the race session_id, analyze by class

**"Who's fastest overall in 2025?"**
→ ❌ INVALID - lap times aren't comparable across different tracks

**"What's [driver]'s average pace?"**
→ Must specify session_id and class, filter to `bpillar_quartile IN (1, 2)`

**"How did [driver] do in the race?"**
→ Get all laps for driver_id at specific session_id, show pace relative to class using bpillar quartiles

**"Compare [team A] vs [team B]"**
→ Only valid within same session_id and same class, filter to `bpillar_quartile IN (1, 2)`

**"What was the pit strategy at Sebring?"**
→ Filter to the Sebring race session_id, show pit_time entries per class

**"How does weather affect pace at Road America?"**
→ Choose the Road America race session_id, group by temperature within each class (top laps only)

**"Who's most consistent in GTP?"**
→ Calculate CV for a specific race session_id, filtered to GTP class and top 50% laps

**"Show me tire degradation for [driver]"**
→ Use ALL laps for specific session_id to see full wear curve (exception to quartile rule)

**"Best lap times for [driver]?"**
→ Specify session_id + class, show their fastest laps using `bpillar_quartile IN (1, 2)`

## Key Reminders

1. **🚨 Use session_id for all lap time comparisons**: Never compare across different sessions
2. **🚨 Default to race sessions**: `session = 'race'` unless specifically asked for practice/qualifying
3. **🚨 Filter to BPillar laps**: Use `bpillar_quartile IN (1, 2)` for race pace analysis
4. **Each class is independent**: Analyze GTP, LMP2, GTD separately within each session
5. **Averages require single session + single class + bpillar filtering**: Otherwise the number is meaningless
6. **When to use ALL laps**: Stint degradation analysis, race distance simulations, or specific requests
7. **BPillar handles most filtering**: No need for manual `flags = 'GF'` or pit lap exclusions
8. **Weather is pre-joined**: Already aligned to each lap
9. **driver_id is VARCHAR**: Use string values like `'tobi lutke'` for filtering/joins, `driver_name` for display
10. **Format times for humans**: Always use the format_time macro
11. **Quartile logic**: Q1 = fastest 25%, Q2 = 25-50%, Q3 = 50-75%, Q4 = slowest 25%
12. **BPillar vs lap_time_driver_quartile**: Use bpillar for races (intelligent filtering), lap_time_driver for practice/qualifying
13. **Output formats**: Default markdown tables, use `--csv` flag for token efficiency with large results

---

**Remember**: The goal is actionable insights within the context of a specific race session. Always filter to session_id + class + top laps first, then analyze. Present findings clearly and suggest follow-up questions when appropriate.
