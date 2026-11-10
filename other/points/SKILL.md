---
name: points
description: Member points, the leaderboard and event check-ins.
---

# Points

Use it to give points for events, look up a member's points, and show the leaderboard.

## Flow

1. `points.leaderboard` for the top members.
2. `points.history` for one member, `points.entries` for every entry.
3. `points.award` gives the same points to up to 100 members for one event. A negative value takes points away.
4. `points.import_csv` gives points to each checked-in row of an attendance CSV, once per email.

## Watch out

- If one member in `points.award` is not in the org, nothing changes. Check the list first.
- `points.delete` removes entries by id or every entry of an event.
- Points are a currency in the store, so a wrong award lets members buy things.
