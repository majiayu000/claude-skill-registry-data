---
name: vault-stale
description: Find stale notes (important notes not modified recently). Triggers on "stale notes", "old notes", "neglected notes", "outdated notes".
auto_trigger: true
trigger_keywords:
  - "stale notes"
  - "old notes"
  - "neglected notes"
  - "outdated notes"
  - "find stale"
  - "inactive notes"
  - "forgotten notes"
  - "show stale"
  - "need attention"
  - "dusty notes"
  - "need review"
  - "haven't touched"
  - "untouched notes"
  - "what needs updating"
  - "old important notes"
allowed-tools: mcp__flywheel__get_recent_notes, mcp__flywheel__get_backlinks, mcp__flywheel__search_notes
---

# Stale Notes

Find important notes that haven't been updated recently.

## Purpose

Stale notes are:
- **Important** (have many backlinks = widely referenced)
- **Outdated** (not modified in 60+ days)

These may need review, updates, or archiving.

## What Makes a Note "Important"?

- Has 5+ backlinks (widely referenced)
- OR has specific tags (#project, #active)
- OR in key folders (work/projects/, tech/)

## Process

### 1. Get Recent Activity

```javascript
recent_notes = get_recent_notes(days=60)
all_notes = search_notes({})

stale_candidates = all_notes - recent_notes
```

### 2. Filter for Important Notes

```javascript
stale_important = []

for note in stale_candidates:
  backlinks = get_backlinks(note)

  if backlinks.count >= 5:
    stale_important.append({
      path: note.path,
      backlinks: backlinks.count,
      last_modified: note.modified,
      days_stale: (today - note.modified).days
    })
```

### 3. Sort by Importance

Sort by backlink count (most referenced first).

### 4. Report Results

```
Stale Notes
═══════════════════════════════════════════════
Found 42 important but stale notes

🚨 Critical (100+ days, 10+ backlinks):
   • [[Architecture Docs]] - 156 days, 47 backlinks
   • [[Best Practices]] - 203 days, 34 backlinks
   • [[Team Onboarding]] - 178 days, 28 backlinks

⚠️ High (60-100 days, 5+ backlinks):
   • 18 notes need review

💡 Actions:
   • Review critical notes - update or archive
   • Add "last reviewed: YYYY-MM-DD" to frontmatter
   • Consider if information is still relevant

═══════════════════════════════════════════════
```

## Recommended Actions

**For each stale note:**
1. **Review**: Read and assess if still relevant
2. **Update**: Refresh outdated information
3. **Archive**: Move to archive/ if no longer needed
4. **Link**: Add to current work if relevant
5. **Tag**: Add `#reviewed/YYYY-MM-DD` frontmatter

## Ignore Patterns

Don't flag as stale:
- Daily/weekly/monthly notes (intentionally historical)
- Archive folders
- Reference material (timeless)
- Meeting notes (historical record)

---

**Version:** 1.0.0
