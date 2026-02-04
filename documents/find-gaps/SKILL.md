---
name: vault-gaps
description: Find knowledge gaps (topics mentioned but not documented). Triggers on "knowledge gaps", "content gaps", "missing notes", "gaps".
auto_trigger: true
trigger_keywords:
  - "knowledge gaps"
  - "content gaps"
  - "missing notes"
  - "gaps"
  - "find gaps"
  - "show gaps"
  - "missing topics"
  - "undocumented"
  - "missing links"
  - "linking opportunities"
  - "connection gaps"
  - "enhance connections"
  - "should document"
  - "what's missing"
  - "topic holes"
allowed-tools: mcp__flywheel__find_broken_links, mcp__flywheel__get_unlinked_mentions, mcp__flywheel__search_notes
---

# Knowledge Gaps

Find topics that are mentioned but not properly documented.

## Purpose

Knowledge gaps are:
- Topics mentioned in multiple notes
- But have no dedicated note
- OR broken wikilinks (mentioned but file doesn't exist)
- OR unlinked mentions (not yet formalized)

These represent opportunities to create new content.

## Types of Gaps

**1. Broken Links** - Explicitly linked but file missing
```
[[Feature Not Built Yet]] → No file exists
```

**2. Unlinked Mentions** - Mentioned but not linked
```
"We should implement authentication" → Not wikilinked
```

**3. Stub Pages** - Note exists but empty/minimal content
```
# Authentication
(2 lines, no substance)
```

## Process

### 1. Find Broken Links

```javascript
broken = find_broken_links()
  → Group by frequency (how many notes reference this missing topic)
```

### 2. Find Unlinked Mentions

```javascript
// Check for common unlinked topics
topics = ["authentication", "api", "deployment", "testing", ...]

unlinked = []
for topic in topics:
  mentions = get_unlinked_mentions(topic)
  if mentions.count > 3:
    unlinked.append(topic)
```

### 3. Find Stub Pages

```javascript
all_notes = search_notes({})

stubs = []
for note in all_notes:
  backlinks = get_backlinks(note)
  if backlinks.count > 5 and note.word_count < 100:
    stubs.append(note)
```

### 4. Report Results

```
Knowledge Gaps
═══════════════════════════════════════════════
Found 34 knowledge gaps

🚨 High Priority Broken Links (10+ references):
   • [[API Authentication]] - Referenced 24 times, no file
   • [[Deployment Guide]] - Referenced 18 times, no file
   • [[Testing Strategy]] - Referenced 12 times, no file

⚠️ Frequently Unlinked Topics (5+ mentions):
   • "authentication" - 15 unlinked mentions
   • "deployment" - 12 unlinked mentions
   • "api design" - 8 unlinked mentions

📝 Stub Pages (high backlinks, low content):
   • [[Best Practices]] - 34 backlinks, 45 words
   • [[Team Process]] - 28 backlinks, 67 words

💡 Actions:
   • Create notes for high priority broken links
   • Formalize frequently mentioned topics
   • Expand stub pages with proper content

═══════════════════════════════════════════════
```

## Recommended Actions

**For each gap:**
1. **Create note**: Make the missing file
2. **Add content**: Write documentation
3. **Link existing**: Use unlinked-mentions skill to find and link
4. **Expand stubs**: Add substance to minimal notes

---

**Version:** 1.0.0
