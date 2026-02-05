---
name: vault-hubs
description: Find hub notes (highly connected notes with many links). Triggers on "hubs", "hub notes", "most connected", "popular notes", "highly connected notes".
auto_trigger: true
trigger_keywords:
  - "hubs"
  - "hub notes"
  - "most connected"
  - "popular notes"
  - "highly connected"
  - "most linked"
  - "top notes"
  - "important notes"
  - "central notes"
  - "find hubs"
  - "key concepts"
  - "well-linked"
  - "core ideas"
  - "knowledge hubs"
allowed-tools: mcp__flywheel__find_hub_notes
---

# Hubs Skill

Find hub notes - highly connected notes that serve as central points in your knowledge graph.

## Purpose

Hub notes are the opposite of orphans. They have many connections (backlinks + forward links) and serve as:
- Knowledge entry points (MOCs, indexes)
- Central concepts (frequently referenced ideas)
- Active topics (currently being worked on)
- Important entities (key people, projects, technologies)

Finding hubs helps you:
- Identify your vault's "center of gravity"
- Understand what topics are most important to you
- Find natural MOC (Map of Content) candidates
- Discover over-connected notes that might need splitting

## When to Use

Invoke when you want to:
- **Find most connected notes**: "hubs" or "hub notes"
- **Discover vault structure**: "most connected" or "popular notes"
- **Find MOC candidates**: "central notes" or "important notes"
- **Audit note importance**: Part of vault analysis

## Process

### 1. Call MCP Tool

```
Call: mcp__flywheel__find_hub_notes
Parameters: { min_links: 5 }  # Default threshold
```

### 2. Categorize Hubs

Group hubs by type for better analysis:

**By Connection Type:**
```
Balanced hubs (many backlinks + forward links):
  - Project X: 45 backlinks, 23 forward links (good MOC)
  - Technology Y: 34 backlinks, 28 forward links (central concept)

Backlink hubs (many backlinks, few forward links):
  - Daily Habit: 300+ backlinks, 2 forward links (referenced entity)
  - Person Name: 67 backlinks, 3 forward links (person)

Forward link hubs (many forward links, few backlinks):
  - Tech Index: 3 backlinks, 45 forward links (potential MOC)
  - Work Dashboard: 2 backlinks, 38 forward links (aggregator)
```

**By Hub Strength:**
```
Super hubs (100+ total links): 3
Strong hubs (50-99 links): 12
Medium hubs (20-49 links): 45
Weak hubs (5-19 links): 96
```

### 3. Display Report

```
Hub Notes Report
═══════════════════════════════════════════════

Found 156 hub notes (11% of vault)
Threshold: 5+ total links

TOP HUBS (20 shown):

1. [[Daily Habit 1]] - 300+ total links
   ← 300 backlinks | → 2 forward links
   Type: Habit | Daily reference
   Hub strength: SUPER (daily tracking)

2. [[Main Project]] - 68 total links
   ← 45 backlinks | → 23 forward links
   Type: Project | Balanced hub
   Hub strength: STRONG ⭐ (excellent MOC!)

3. [[Core Technology]] - 56 total links
   ← 42 backlinks | → 14 forward links
   Type: Technology | Balanced hub
   Hub strength: STRONG (central tech)

═══════════════════════════════════════════════

BREAKDOWN BY TYPE:
  Habits: 3 (super hubs from daily tracking)
  Technologies: 34 (central tech concepts)
  Projects: 18 (active work)
  People: 23 (frequently mentioned)
  Concepts: 45 (important ideas)

MOC CANDIDATES (balanced hubs):
  Main Project: 45 ← | 23 → (⭐ excellent MOC)
  Core Technology: 34 ← | 28 → (⭐ good MOC)

Options:
1. Show full list (all 156 hubs)
2. Filter by type/strength
3. Find potential MOCs (balanced hubs)
```

## Implementation Details

### Hub Criteria

A note is a hub if:
- Total links (backlinks + forward links) >= min_links
- Default threshold: 5 links
- User can adjust: "hubs with 20+ links"

### Hub Strength Classification

```python
def classify_hub_strength(total_links):
    if total_links >= 100:
        return "SUPER"
    elif total_links >= 50:
        return "STRONG"
    elif total_links >= 20:
        return "MEDIUM"
    else:
        return "WEAK"
```

### Hub Balance Score

Measures how balanced backlinks vs forward links are:

```python
def hub_balance_score(backlinks, forward_links):
    if backlinks == 0 or forward_links == 0:
        return 0  # Completely unbalanced

    ratio = min(backlinks, forward_links) / max(backlinks, forward_links)
    return ratio * 100  # 0-100%
```

**Balance interpretation:**
- 80-100%: Excellent MOC candidate
- 50-79%: Good MOC candidate
- 20-49%: Could improve as MOC
- <20%: Unbalanced (entity vs aggregator)

## Related Skills

- **orphans**: Opposite of hubs (zero connections)
- **backlinks**: Show specific note's connections
- **clusters**: Find groups of related hubs
- **health**: Overall vault metrics (hub % is key metric)

## Performance

- **MCP call**: ~300-500ms for large vaults
- **Categorization**: ~100ms for 156 hubs
- **Total**: Usually <1 second
