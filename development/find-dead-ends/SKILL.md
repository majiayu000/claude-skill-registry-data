---
name: vault-dead-ends
description: Find dead-end notes (have backlinks but no outgoing links). Triggers on "dead ends", "dead end notes", "endpoint notes".
auto_trigger: true
trigger_keywords:
  - "dead ends"
  - "dead end notes"
  - "endpoint notes"
  - "dead end pages"
  - "notes with no outlinks"
  - "terminal notes"
  - "find dead ends"
  - "leaf notes"
  - "sink notes"
  - "don't link out"
  - "only receive links"
  - "cul-de-sacs"
  - "no outgoing links"
  - "end points"
allowed-tools: mcp__flywheel__get_backlinks, mcp__flywheel__get_forward_links
---

# Dead End Notes

Find notes that receive links but don't link to anything (dead ends).

## Purpose

Dead end notes are:
- Referenced by other notes (have backlinks)
- But don't reference anything themselves (no outgoing links)

These represent incomplete knowledge integration - they're mentioned but not connected.

## Characteristics

**Good dead ends:**
- Reference pages (people, companies)
- Glossary terms
- Index pages
- Atomic concepts

**Bad dead ends:**
- Project notes with no connections
- Meeting notes with no follow-up links
- Incomplete drafts
- Stub pages

## Process

### 1. Find Notes with Backlinks

```javascript
get_backlinks(all_notes)
  → Filter notes with backlink_count > 0
```

### 2. Check Outgoing Links

```javascript
for each note in notes_with_backlinks:
  forward_links = get_forward_links(note)
  if forward_links.length == 0:
    dead_ends.append(note)
```

### 3. Categorize by Backlink Count

- High priority: 10+ backlinks, 0 outlinks (widely referenced but isolated)
- Medium priority: 3-9 backlinks, 0 outlinks
- Low priority: 1-2 backlinks, 0 outlinks

### 4. Report Results

```
Dead End Notes
═══════════════════════════════════════════════
Found 87 dead end notes

🚨 High Priority (10+ backlinks):
   • [[Meeting 2025-03-15]] - 24 backlinks, 0 outlinks
   • [[Project Alpha]] - 18 backlinks, 0 outlinks
   • [[Technical Spec]] - 12 backlinks, 0 outlinks

⚠️ Medium Priority (3-9 backlinks):
   • 34 notes need connections

✅ Low Priority (1-2 backlinks):
   • 50 notes (likely reference pages)

💡 Recommendations:
   • Review high priority notes - add relevant connections
   • Consider if these should link to related concepts
   • Some may be intentional (person pages, glossary)

═══════════════════════════════════════════════
```

## When to Fix

**Fix these:**
- Project notes (should link to related projects/tech)
- Meeting notes (should link to action items/people)
- Technical docs (should link to implementation/tools)

**Keep these:**
- Person pages (reference only)
- Company names (reference only)
- Glossary terms (atomic concepts)

---

**Version:** 1.0.0
