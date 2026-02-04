---
name: time-helper
description: This skill should be used when users request current time information, timezone conversions, or any time-related queries. It provides a simple interface to Claude's built-in time-tools functionality for accurate time information and timezone conversions.
---

# Time Helper Skill

This skill provides time and timezone conversion capabilities using Claude's built-in time-tools functionality. It's designed to be a simple, clear interface for all time-related queries.

## When to Use This Skill

Use this skill when users ask for:
- Current time in specific locations/timezones
- Time conversion between different timezones
- Timezone information and comparisons
- Any time-related queries involving different regions
- Help with time calculations or scheduling

## Skill Purpose

Provide accurate time information and timezone conversions by:
- Getting current time for any IANA timezone
- Converting time between different timezones
- Providing timezone information and offsets
- Handling Daylight Saving Time automatically
- Supporting all IANA timezone names

## Implementation Process

### Step 1: Use Built-in Time Tools
Invoke the time-tools skill that's already available:
- Call the time-tools skill for current time queries
- Call the time-tools skill for timezone conversions
- Parse and format the response for user

### Step 2: Handle Common Queries
Process standard time-related requests:
- "What time is it now?" → Use system timezone
- "What time is it in [city]?" → Use specific timezone
- "Convert [time] from [city] to [city]" → Use conversion
- "What's the time difference between [city] and [city]?" → Compare timezones

### Step 3: Format Responses
Present time information clearly:
- Show local time and date
- Include timezone abbreviation
- Mention UTC offset
- Note if DST is active
- Provide context for time differences

## Available Tools

### time-tools skill
The built-in tool for all time operations:
- `get_current_time` - Get current time in any timezone
- `convert_time` - Convert time between timezones
- Handles IANA timezone validation
- Manages DST calculations automatically

## Reference Materials

### Common Timezones
- `references/iana_timezones.md` - List of common IANA timezone names
- Use for validating user timezone inputs
- Provides timezone abbreviations and UTC offsets

### Windows 10 Setup
- `references/windows_10_setup.md` - Windows-specific setup if needed
- Timezone configuration on Windows
- System timezone detection

## Usage Examples

### Query: "What time is it now?"
1. Execute time-tools skill with system timezone
2. Format response: "It's 3:45 PM on Tuesday, December 23, 2025 (EST)"
3. Include date, timezone abbreviation, and day of week

### Query: "What time is it in Tokyo?"
1. Execute time-tools skill with "Asia/Tokyo"
2. Format response: "It's 5:45 AM on Wednesday, December 24, 2025 (JST)"
3. Note it's already tomorrow in Tokyo

### Query: "Convert 4 PM New York time to London time"
1. Execute time-tools skill with "America/New_York", "16:00", "Europe/London"
2. Format response: "4:00 PM in New York is 9:00 PM in London"
3. Include time difference: "London is 5 hours ahead"

### Query: "What time zones are available?"
1. Reference iana_timezones.md for common timezone names
2. Provide organized list by region
3. Include examples: "America/New_York, Europe/London, Asia/Tokyo"

## Error Handling

- Validate timezone names before execution
- Handle invalid time format inputs
- Provide helpful error messages
- Suggest common timezone alternatives
- Clarify ambiguous location names

## Quality Requirements

- Always validate timezone inputs
- Use clear, readable time formats
- Include relevant context (date, timezone, DST)
- Handle edge cases gracefully
- Provide helpful suggestions for invalid inputs

## Common Timezone Names

### Popular Cities
- New York: America/New_York
- Los Angeles: America/Los_Angeles
- London: Europe/London
- Paris: Europe/Paris
- Tokyo: Asia/Tokyo
- Sydney: Australia/Sydney
- Dubai: Asia/Dubai
- Singapore: Asia/Singapore

### Timezone Abbreviations
- EST/EDT - Eastern Time
- PST/PDT - Pacific Time
- GMT/BST - Greenwich Mean/British Summer
- CET/CEST - Central European Time
- JST - Japan Standard Time
- AEST/AEDT - Australian Eastern Time

## Tips for Better Responses

1. **Be specific with timezone names** - Use IANA format (America/New_York, not just EST)
2. **Provide context** - Include date, day of week, and timezone info
3. **Handle time differences** - Mention when it's tomorrow/yesterday in other timezones
4. **Clarify ambiguity** - If user says "Paris", assume France unless specified
5. **Be helpful with errors** - Suggest correct timezone names for invalid inputs