---
name: vault-bidirectional
description: Find bidirectional links (notes that link to each other). Triggers on "bidirectional", "bidirectional links", "mutual links", "two-way links".
auto_trigger: true
trigger_keywords:
  - "bidirectional"
  - "bidirectional links"
  - "mutual links"
  - "two-way links"
  - "reciprocal links"
  - "show bidirectional"
  - "find mutual links"
  - "linked both ways"
  - "mutual references"
  - "back and forth"
  - "symmetric links"
  - "cross-linked"
  - "linked together"
  - "both link"
allowed-tools: mcp__flywheel__get_backlinks, mcp__flywheel__get_forward_links
---

# Bidirectional Links

Find notes that link to each other (mutual/reciprocal relationships).

## Purpose

Bidirectional links indicate strong relationships between notes. These are notes that:
- Note A links to Note B
- Note B also links back to Note A

These represent validated, two-way knowledge connections.

## Process

### 1. Get All Notes with Backlinks

Use `get_backlinks` to find notes with incoming links.

### 2. Check Forward Links

For each note with backlinks, check if it links back using `get_forward_links`.

### 3. Identify Bidirectional Pairs

```javascript
bidirectional_pairs = []

for each note in vault:
  backlinks = get_backlinks(note)
  forward_links = get_forward_links(note)

  for backlink in backlinks:
    if backlink in forward_links:
      bidirectional_pairs.append((note, backlink))
```

### 4. Report Results

```
Bidirectional Links
═══════════════════════════════════════════════
Found 234 bidirectional link pairs

📊 Top Bidirectional Relationships:
   • [[Project A]] ↔ [[Technology X]] (strong project connection)
   • [[Claude Code]] ↔ [[Obsidian]] (tool integration)
   • [[Daily Notes]] ↔ [[Habits]] (workflow connection)

💡 Insights:
   • 16% of your links are bidirectional
   • Strong bidirectional clustering around: projects, tools
   • Consider linking more notes bidirectionally for stronger graph

═══════════════════════════════════════════════
```

## Use Cases

- **Validate relationships**: Bidirectional = confirmed two-way connection
- **Find project clusters**: Related project notes often link bidirectionally
- **Strengthen graph**: Identify one-way links that should be two-way
- **Knowledge mapping**: Bidirectional links show core concepts

---

**Version:** 1.0.0
