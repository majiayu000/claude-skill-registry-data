---
name: meeting-notes
description: Format raw meeting notes into a structured summary. Use when someone provides meeting discussion points and wants a clean structured output.
license: MIT
---

# Meeting Notes Formatter

Formats raw meeting notes into a structured `meeting-YYYY-MM-DD.md`.

## Output Format

```
**Meeting: [Title]**
Date: YYYY-MM-DD

**Decisions:**
- [Decision text] — Owner: @name, By: YYYY-MM-DD

**Action Items:**
- [ ] [Task description] — @owner by YYYY-MM-DD

**Parking Lot:**
- [Topic] (deferred — reason)
```

## Rules

- Decisions must include both an owner (@mention) and a deadline date in YYYY-MM-DD format
- Action items use checkbox format: `[ ]`
- Parking Lot items must include the reason for deferral in parentheses: `(deferred — reason)`
- If no parking lot items arose, omit the Parking Lot section entirely
- Save to `meeting-YYYY-MM-DD.md` using the meeting date
