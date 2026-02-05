---
name: date-formatter
description: Format dates and times in various formats, calculate date differences, and provide date-related information. Use this when the user asks about date formatting, conversion, day of week, or time calculations.
---

# Date Formatter Skill

## Instructions
1. Identify the source date format provided by the user
2. Determine the desired output format
3. Handle timezone considerations when relevant
4. Provide clear, unambiguous date representations
5. For relative dates (e.g., "next Monday"), calculate from current date

## Common Format Patterns
- ISO 8601: `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm:ss`
- US Format: `MM/DD/YYYY`
- European Format: `DD/MM/YYYY`
- Long Format: `Month DD, YYYY` (e.g., "December 25, 2025")
- Short Format: `Mon DD` (e.g., "Dec 25")

## Examples

### Example 1: Format Conversion
**User:** "Convert 2025-12-25 to long format"
**Action:** Parse ISO date, format as long
**Response:** "December 25, 2025"

### Example 2: Day of Week
**User:** "What day of the week is January 1, 2026?"
**Action:** Calculate day from date
**Response:** "January 1, 2026 is a Thursday"

### Example 3: Date Difference
**User:** "How many days between March 15, 2025 and December 25, 2025?"
**Action:** Calculate: Dec 25 - Mar 15 = 285 days
**Response:** "There are 285 days between March 15, 2025 and December 25, 2025"

### Example 4: Current Date
**User:** "What's today's date in ISO format?"
**Action:** Get current date, format as ISO
**Response:** "Today is 2025-12-25"

## Considerations
- Always clarify ambiguous dates (e.g., "01/02/2025" could be Jan 2 or Feb 1)
- Use the user's locale preference when known
- For relative dates, state the reference point (e.g., "from today")
- Handle leap years correctly
