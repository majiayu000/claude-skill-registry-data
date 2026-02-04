---
name: conference-scheduler
description: Generate optimized conference schedules using Google OR-Tools CP-SAT solver. Use when the user needs to create conference schedules from CSV data with constraints like speaker conflicts, track distribution, room assignments, educational flow, and speaker availability. Supports both single-day and multi-day conferences. Handles inputs from Google Sheets CSV exports with talks (ID, title, summary, track, level, speakers, availability) and schedule slots (day, times, rooms). Outputs CSV and Markdown schedules.
---

# Conference Scheduler Skill

Generate optimized conference schedules using Google OR-Tools CP-SAT constraint solver. Supports single-day and multi-day conferences.

## Quick Start

```bash
pip install ortools --break-system-packages
python assets/scheduler.py schedule.csv talks.csv output.csv --time-limit 30
```

## Input Formats

### Single-Day Schedule CSV

```csv
"from hour";"to hour";"session type";"room name"
"10:35";"11:20";Conference;Room 2
"10:35";"11:20";Conference;Room 8
"11:30";"12:15";Conference;Room 3
```

### Multi-Day Schedule CSV

Add a "day" column as the first column:

```csv
"day";"from hour";"to hour";"session type";"room name"
"Wednesday";"09:30";"10:15";Conference;Room 1
"Wednesday";"10:35";"11:20";Conference;Room 2
"Thursday";"09:30";"10:15";Conference;Room 1
```

Day values can be: day names (Monday, Tuesday), dates (2024-03-15), or labels (Day 1, Day 2).

### Talks CSV

```csv
"Talk ID";"Talk Title";"Audience Level";"Talk Summary";"Track Name";"Speaker Availability days";"Available from";"Available to";"Speaker names"
1411;Unit Test Your Architecture;BEGINNER;ArchUnit is...;Development Practices;Wednesday,Thursday;;;Roland Weisleder
3872;Full-stack development;INTERMEDIATE;Java developers...;UI & UX;;;;Simon Martinelli
```

**Speaker Availability** formats (column 6):
- Day names: `Wednesday,Thursday`
- Day numbers: `1,2,3`
- Empty = available all days

## Constraints

### Hard Constraints (Must satisfy)

| Constraint | Description |
|------------|-------------|
| Speaker conflict | Same speaker can't be in two rooms at same time |
| Room conflict | Two talks can't be in same room at same time |
| Track conflict | Same track can't have talks in different rooms simultaneously |
| Speaker availability | Speaker must be available on scheduled day |

### Soft Constraints (Optimization)

| Constraint | Description |
|------------|-------------|
| Educational flow | Beginner → Intermediate → Advanced within track |

## Output

### CSV Output

Single-day:
```csv
"Talk ID";"From";"To";"Room";"Title";"Speakers";"Level";"Track"
```

Multi-day:
```csv
"Day";"Talk ID";"From";"To";"Room";"Title";"Speakers";"Level";"Track"
```

### Markdown Output

Generated alongside CSV with `.md` extension, includes tables grouped by timeslot (and day for multi-day).

## Programmatic Usage

```python
from pathlib import Path
from scheduler import (
    read_schedule_csv, read_talks_csv, solve_schedule,
    write_csv_output, write_markdown_output, print_schedule
)

# Read input
timeslots, rooms, day_names = read_schedule_csv(Path("schedule.csv"))
talks = read_talks_csv(Path("talks.csv"), day_names)

# Solve (30 second time limit)
talks, status = solve_schedule(timeslots, rooms, talks, time_limit_seconds=30)

# Output
print_schedule(talks, multi_day=len(day_names) > 1)
write_csv_output(talks, Path("output.csv"), multi_day=len(day_names) > 1)
```

## Time Limits

- Small conferences (< 30 talks): 10-30 seconds
- Medium conferences (30-100 talks): 30-120 seconds
- Large conferences (100+ talks): 2-10 minutes

## Troubleshooting

### INFEASIBLE status

The constraints cannot all be satisfied. Check for:
- More talks than available slots
- Speaker with more talks than available timeslots
- Too many talks in same track for parallel slots

### Missing ortools

```bash
pip install ortools --break-system-packages
```
