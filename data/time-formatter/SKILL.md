---
name: time-formatter
description: |
  Automatically detect time/date mentions in user messages and convert them to
  multiple timezones or formats. Use when user mentions times, dates, or asks
  about timezone conversions. Examples: "15:00 Berlin time", "What time is 3 PM EST in Tokyo?",
  "Convert 2025-01-15 10:00 CET to PST".
allowed-tools: [mcp__datetime__get_current_time, mcp__datetime__convert_timezone, mcp__datetime__calculate_duration]
---

# Time Formatter Skill

## When to Use

Activate this skill automatically when user:
- Mentions specific times with timezone ("15:00 CET", "3 PM EST")
- Asks "what time is..." questions
- Requests timezone conversions
- Provides dates/times for scheduling
- Compares times across locations

## Detection Patterns

### Explicit Timezone Mentions
- "15:00 Berlin"
- "3 PM EST"
- "10:30 America/New_York"
- "noon CET"

### Implicit Conversions
- "What time is it in Tokyo?"
- "When is 5 PM here in New York?"
- "Convert 14:00 to PST"

### Scheduling Context
- "Let's meet at 3 PM my time" (need to detect user timezone)
- "Schedule for tomorrow 9 AM Berlin"

## Instructions

### Step 1: Detect Time/Timezone in Input

Parse user message for:
1. **Time**: HH:MM format or descriptive (e.g., "noon", "5 PM")
2. **Timezone**: Name, abbreviation, or location
3. **Date**: Optional date reference

**Timezone Mapping**:
```
CET/CEST → Europe/Berlin
EST/EDT → America/New_York
PST/PDT → America/Los_Angeles
JST → Asia/Tokyo
GMT/UTC → UTC
```

### Step 2: Use MCP DateTime Tools

#### For "current time" queries:
```
Use: get_current_time
Parameters:
  - timezone: detected location
  - format: "human" (readable)
```

#### For "convert time" queries:
```
Use: convert_timezone
Parameters:
  - time: extracted time (ISO format)
  - from_tz: source timezone
  - to_tz: target timezone
```

#### For "time difference" queries:
```
Use: calculate_duration
Parameters:
  - start: first time
  - end: second time
  - unit: "hours" (default)
```

### Step 3: Format Output

**Single Timezone Query**:
```
Current time in Tokyo:
Tuesday, 15. January 2025 18:30:00 JST
(2025-01-15T18:30:00+09:00)
```

**Timezone Conversion**:
```
3 PM EST (America/New_York)
  = 9 PM CET (Europe/Berlin)
  = 5 AM JST (Asia/Tokyo, next day)
```

**Duration Calculation**:
```
From: 9:00 AM Berlin
To: 5:00 PM Berlin
Duration: 8.0 hours (28800 seconds)
```

### Step 4: Handle Edge Cases

**Ambiguous Input**:
- "What time is it?" → Ask: "Which timezone?"
- "3 PM" → Ask: "Which timezone? (assuming user's local)"

**Invalid Timezone**:
- "3 PM XYZ" → Suggest valid timezones
- Show list of common zones

**Date Handling**:
- "tomorrow 3 PM" → Calculate tomorrow's date
- "next Monday" → Infer date

## Examples

### Example 1: Simple Current Time
**Input**: "What time is it in Berlin?"

**Actions**:
1. Detect timezone: "Berlin" → "Europe/Berlin"
2. Call: `get_current_time(timezone="Europe/Berlin", format="human")`
3. Format output:
   ```
   Current time in Berlin (Europe/Berlin):
   Tuesday, 15. January 2025 14:30:45 CET
   ```

### Example 2: Timezone Conversion
**Input**: "Convert 3 PM EST to CET"

**Actions**:
1. Parse:
   - Time: "3 PM" → "15:00"
   - From: "EST" → "America/New_York"
   - To: "CET" → "Europe/Berlin"
2. Get current date (if not specified)
3. Call: `convert_timezone(time="2025-01-15T15:00:00", from_tz="America/New_York", to_tz="Europe/Berlin")`
4. Output:
   ```
   3:00 PM EST (New York)
   = 9:00 PM CET (Berlin)

   (+6 hours difference)
   ```

### Example 3: Multi-Timezone Display
**Input**: "Show me 10 AM Berlin in all major timezones"

**Actions**:
1. Base time: "10:00" Berlin
2. Convert to:
   - UTC
   - EST (New York)
   - PST (Los Angeles)
   - JST (Tokyo)
3. Output table:
   ```
   10:00 AM Berlin (CET) is:

   UTC:          09:00 AM
   New York:     04:00 AM (EST)
   Los Angeles:  01:00 AM (PST)
   Tokyo:        06:00 PM (JST)
   ```

### Example 4: Meeting Duration
**Input**: "How long from 9 AM to 5:30 PM?"

**Actions**:
1. Parse times (assume same timezone)
2. Call: `calculate_duration(start="2025-01-15T09:00:00", end="2025-01-15T17:30:00", unit="hours")`
3. Output:
   ```
   Duration: 8.5 hours

   From: 09:00 AM
   To:   05:30 PM

   (That's 8 hours 30 minutes / 30600 seconds)
   ```

### Example 5: Complex Scheduling
**Input**: "If the meeting starts at 2 PM Berlin time and lasts 90 minutes, what time does it end in Tokyo?"

**Actions**:
1. Start time: "14:00" Berlin
2. Duration: 90 minutes
3. Calculate end time: 14:00 + 1:30 = 15:30 Berlin
4. Convert to Tokyo:
   ```
   Meeting Schedule:

   Start: 2:00 PM Berlin (14:00 CET)
         = 10:00 PM Tokyo (22:00 JST)

   End:   3:30 PM Berlin (15:30 CET)
         = 11:30 PM Tokyo (23:30 JST)

   Duration: 1.5 hours (90 minutes)
   ```

## Error Handling

### Unknown Timezone
**Input**: "What time is it in Atlantis?"
**Response**:
```
⚠️ Unknown timezone: "Atlantis"

Did you mean:
- Atlanta (America/New_York, EST)
- Atlantic Standard Time (America/Halifax, AST)

Or try: Europe/Berlin, America/New_York, Asia/Tokyo
```

### Invalid Time Format
**Input**: "Convert 25:00 to EST"
**Response**:
```
⚠️ Invalid time: "25:00"

Please use 24-hour format (00:00 - 23:59)
or 12-hour format with AM/PM (e.g., "1:00 PM")
```

### Ambiguous Date
**Input**: "3 PM next week"
**Response**:
```
⚠️ "next week" is ambiguous.

Please specify:
- Day of week (e.g., "next Monday")
- Exact date (e.g., "2025-01-22")
```

## Performance

- ✅ Instant responses (no network calls for MCP)
- ✅ Works offline (local datetime calculations)
- ✅ Handles 200+ timezone names
- ✅ Supports DST (Daylight Saving Time) automatically

## Tips

1. **Always be proactive**: If you see ANY time/date mention, consider using this skill
2. **Show multiple formats**: Users appreciate seeing both human and ISO formats
3. **Timezone abbreviations**: Always clarify (EST vs EDT, CET vs CEST)
4. **Visual formatting**: Use tables for multi-timezone comparisons
