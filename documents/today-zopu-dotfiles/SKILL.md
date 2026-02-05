---
name: today
description: Get today's date for web searches and date-sensitive tasks. Auto-invoke before any WebSearch that includes a year (e.g., "React 2024", "Python 2025"), when searching for current documentation, latest releases, or recent information. Ensures searches use the correct current year instead of outdated dates.
---

# Today's Date

Get the current date before performing web searches or date-sensitive operations.

## Instructions

1. Run `date "+%Y-%m-%d"` to get today's date
2. Extract the current year from the result
3. Use this year in web search queries instead of any assumed or hardcoded year
4. Report the current date, then proceed with the task using correct dates

## When to use

- Before web searches that would include a year (e.g., "React Query 2024" should become "React Query 2025" if we're in 2025)
- When searching for "latest", "current", "recent", or "up-to-date" documentation
- When the user asks about recent releases, current versions, or contemporary information
- Any task where using an outdated year would return stale results

## Example

If asked to search for "Next.js best practices 2024" and today is 2025-12-25:
1. Get current date: 2025-12-25
2. Update search to: "Next.js best practices 2025"
3. Perform the corrected search
