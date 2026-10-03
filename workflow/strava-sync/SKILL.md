---
name: strava-sync
description: Downloads and syncs training data from Strava using the Strava MCP server. This is ONE option for importing training data - athletes can also use manual logs, other platforms (Garmin, Apple Health), or provide data conversationally. Use this skill specifically when the athlete wants to sync from Strava or when the running-coach indicates Strava as the chosen data source. Stores activities in the training-log folder as markdown summaries, including lap details for workout runs.
---

# Strava Training Log Sync

## Overview

This skill downloads training data from Strava using the Strava MCP server and creates weekly markdown summaries in the `training-log` folder. Each week is stored as a single markdown file with detailed activity summaries, including lap details for runs marked as workouts.

**Note**: This is a Strava-specific data import tool. The running coach system also supports:
- Other platforms (Garmin Connect, Apple Health, Polar Flow, etc.) - athlete provides data
- Manual training logs - athlete creates markdown files directly
- Conversational input - athlete describes training verbally

This skill uses MCP tools specific to Strava (`mcp__strava__*`). Similar skills could be created for other platforms using their respective APIs or MCP servers.

## Workflow

### 1. Get Week Number from User

First, ask the user to provide the training week number:

- Prompt: "Which training week would you like to sync? (e.g., 1, 2, 3)"
- Store this number as the week identifier
- The file will be saved as `week-{n}.md` where {n} is this week number

### 2. Check Strava Connection

Verify that Strava is connected:

```bash
# Check connection status
```

Use the `mcp__strava__check-strava-connection` tool to verify the connection. If not connected, use `mcp__strava__connect-strava` to authenticate.

### 3. Fetch Recent Activities

Retrieve the last 7 days of activities from Strava:

1. Use `mcp__strava__get-recent-activities` to fetch recent activities (default 30 activities)
2. Filter activities to only those from the last 7 days
3. Calculate the week date range (e.g., "2024-01-15 to 2024-01-21")

### 4. Process Each Activity

For each activity in the last week:

1. Extract key information:
   - Activity name
   - Date and time
   - Activity type (Run, Ride, Swim, etc.)
   - Distance (convert to miles or km)
   - Duration (format as HH:MM:SS)
   - Elevation gain
   - Average pace/speed
   - Average heart rate (if available)
   - Description/notes

2. Check if the activity is marked as a workout:
   - Look for the `workout_type` field in the activity data
   - For runs: workout_type 0 = default run, 1 = race, 2 = long run, 3 = workout

3. For workout or long runs, fetch lap details:
   - Use `mcp__strava__get-activity-laps` with the activity ID
   - Extract lap information:
     - Lap number
     - Distance
     - Duration
     - Average pace
     - Average heart rate
     - Elevation gain

### 5. Calculate Week Totals

**IMPORTANT**: Use Python to calculate all totals to ensure mathematical accuracy. Do NOT calculate totals manually.

Use the `mcp__ide__executeCode` tool or Bash with Python to:
1. Group activities by type (Run, Ride, Swim, etc.)
2. For each activity type, calculate:
   - Total distance
   - Total time
   - Total elevation gain
   - Activity count
3. Calculate overall totals across all activity types

Example Python calculation:
```python
from collections import defaultdict

# Given activities list
activities = [...]  # Your activities data

# Group by activity type
by_type = defaultdict(list)
for activity in activities:
    activity_type = activity['type']  # e.g., 'Run', 'Ride', 'Swim'
    by_type[activity_type].append(activity)

# Calculate totals per activity type
type_totals = {}
for activity_type, activities_of_type in by_type.items():
    total_distance = sum(a['distance'] for a in activities_of_type)  # in meters
    total_time = sum(a['moving_time'] for a in activities_of_type)  # in seconds
    total_elevation = sum(a['total_elevation_gain'] for a in activities_of_type)  # in meters
    count = len(activities_of_type)
    
    # Convert to display units
    distance_miles = total_distance * 0.000621371
    hours = total_time // 3600
    minutes = (total_time % 3600) // 60
    seconds = total_time % 60
    elevation_feet = total_elevation * 3.28084
    
    type_totals[activity_type] = {
        'count': count,
        'distance': f"{distance_miles:.2f} miles",
        'time': f"{hours:02d}:{minutes:02d}:{seconds:02d}",
        'elevation': f"{elevation_feet:.0f} ft"
    }

# Calculate overall totals
total_distance = sum(a['distance'] for a in activities)
total_time = sum(a['moving_time'] for a in activities)
total_elevation = sum(a['total_elevation_gain'] for a in activities)
total_count = len(activities)

# Convert to display units
overall_distance_miles = total_distance * 0.000621371
overall_hours = total_time // 3600
overall_minutes = (total_time % 3600) // 60
overall_seconds = total_time % 60
overall_elevation_feet = total_elevation * 3.28084

print(f"Overall Total Activities: {total_count}")
print(f"Overall Total Distance: {overall_distance_miles:.2f} miles")
print(f"Overall Total Time: {overall_hours:02d}:{overall_minutes:02d}:{overall_seconds:02d}")
print(f"Overall Total Elevation: {overall_elevation_feet:.0f} ft")
print("\nBy Activity Type:")
for activity_type, totals in type_totals.items():
    print(f"\n{activity_type}:")
    print(f"  Count: {totals['count']}")
    print(f"  Distance: {totals['distance']}")
    print(f"  Time: {totals['time']}")
    print(f"  Elevation: {totals['elevation']}")
```

### 6. Format as Markdown

Create a markdown file with the following structure, using the calculated totals:

```markdown
# Training Log: [Start Date] to [End Date]

## Week Summary

### Overall Totals
- **Total Activities**: [count from calculation]
- **Total Distance**: [distance from calculation] miles/km
- **Total Time**: [duration from calculation]
- **Total Elevation**: [elevation from calculation] ft/m

### By Activity Type

#### Run
- **Activities**: [count]
- **Distance**: [distance] miles
- **Time**: [HH:MM:SS]
- **Elevation**: [elevation] ft

#### Ride
- **Activities**: [count]
- **Distance**: [distance] miles
- **Time**: [HH:MM:SS]
- **Elevation**: [elevation] ft

[Include sections for each activity type present in the week]

## Activities

### [Date] - [Activity Name]

**Type**: [Run/Ride/Swim/etc.]
**Distance**: [distance] mi
**Duration**: [HH:MM:SS]
**Pace**: [pace per mile/km]
**Elevation**: [elevation] ft
**Heart Rate**: [avg bpm] (max: [max bpm])

[Activity description/notes if available]

#### Lap Details

| Lap | Distance | Time | Pace | HR | Elevation |
|-----|----------|------|------|-----|-----------|
| 1   | [dist]   | [time] | [pace] | [hr] | [elev] |
| 2   | [dist]   | [time] | [pace] | [hr] | [elev] |

---

[Continue for each activity...]
```

### 7. Save to training-log Folder

1. Create the `training-log` folder if it doesn't exist:
   ```bash
   mkdir -p training-log
   ```

2. Generate filename using the week number provided by the user:
   - Format: `week-{n}.md` where {n} is the week number
   - Example: `week-1.md`, `week-2.md`, `week-3.md`, etc.

3. Write the markdown content to the file

### 8. Provide Summary

After syncing, provide a brief summary:
- Week number
- Number of activities synced
- Date range covered
- File location (e.g., `training-log/week-1.md`)
- Any activities that are workouts with lap details
- Confirm that totals were calculated using Python/script

## MCP Tools Used

- `mcp__strava__check-strava-connection`: Verify Strava authentication
- `mcp__strava__connect-strava`: Connect to Strava if needed
- `mcp__strava__get-recent-activities`: Fetch recent activities
- `mcp__strava__get-activity-details`: Get detailed info for specific activities (if needed)
- `mcp__strava__get-activity-laps`: Fetch lap details for workout runs

## Error Handling

- If Strava is not connected, prompt user to authenticate
- If no activities found in the last week, inform the user
- If lap details are unavailable, note this in the markdown
- Handle API rate limits gracefully

## Notes

- The skill focuses on the last 7 days of data
- Workout detection is specific to runs (workout_type field)
- Lap details are only fetched for activities marked as workouts
- Distance and pace units should match user preference (miles vs km)
- All times should be in local time zone
