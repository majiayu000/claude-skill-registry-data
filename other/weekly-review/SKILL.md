---
name: weekly-review
description: "Runs a 5-minute weekly check-in to review system performance and gather improvement feedback. Use when Mandy says 'weekly review', 'Friday check-in', 'how did we do this week', or on Fridays."
---

# Weekly Review

## Important
- Manual-only.

## Instructions
1. Usage stats from activity logs (7 days). Git stats: `git -C matters/ log --oneline --since="7 days ago"`.
2. Issues: unsent drafts >3 days, re-extractions, feedback entries, inactive matters.
3. Ask 3 questions: (a) Letters heavily rewritten? (b) Manual tasks I should handle? (c) Missed deadlines/developments?
4. Save to `feedback/weekly-reviews/YYYY-MM-DD.md`.
5. Generate `feedback/developer-summaries/YYYY-MM-DD.md`.
