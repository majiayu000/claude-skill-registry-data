---
name: recording-diary
description: Records session learnings and decisions before context compaction. Use before ending a long session or when the user asks to save session notes.
---

<quick_start>
- Before compaction or session end, write `diary_{YYYY-MM-DD_HH-MM}.md` to `./.{AGENT_NAME}/skills/memories/` via `$writing-memories`.
</quick_start>

<templates>
<diary>
Gotchas:
-
Workarounds:
-
Useful commands:
-
Dead ends:
-
Project quirks:
-
Open questions:
-
</diary>
</templates>

<consolidation>
If more than 5 diary entries exist, merge them into `diary-consolidated.md`, keeping only high-signal items. Delete the older entries after consolidation.
</consolidation>

<decision_points>
- Nothing new learned -> skip the diary.
- Many related notes -> consolidate immediately.
</decision_points>

<failure_modes>
- Time format unclear: use local time or `date` output.
- Memory dir missing: create it before writing.
</failure_modes>
