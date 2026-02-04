---
name: vault-strength
description: Calculate connection strength between two notes based on multiple factors. Triggers on "connection strength", "how related", "relationship score", "strength between".
auto_trigger: true
trigger_keywords:
  - "connection strength"
  - "how related"
  - "relationship score"
  - "strength between"
  - "how strongly connected"
  - "relationship strength"
  - "connection score"
  - "how connected are"
  - "relationship quality"
  - "link strength"
  - "affinity between"
  - "closeness"
  - "related score"
  - "connection quality"
  - "how tight is link"
allowed-tools: mcp__flywheel__get_connection_strength
---

# Connection Strength Calculator

Calculate the overall relationship quality between two notes using multiple factors.

## When to Use

Invoke when you want to:
- Quantify how related two notes are
- Understand relationship factors (not just links)
- Compare relationship strengths between different pairs
- Get a holistic view beyond simple link counting

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `note_a` | Yes | First note (title or path) |
| `note_b` | Yes | Second note (title or path) |

## Process

### 1. Parse User Input

Identify the two notes:
- "connection strength between [[Project A]] and [[Technology X]]"
- "how related are [[React]] and [[Vue]]"
- "relationship score for daily note and weekly note"

### 2. Call MCP Tool

```
mcp__flywheel__get_connection_strength(
  note_a: "path/to/first/note.md",
  note_b: "path/to/second/note.md"
)
```

### 3. Format Results

```
Connection Strength
=================================================

[[Project A]] <-> [[Technology X]]

Overall Score: 78/100 (Strong Connection)

-------------------------------------------------

Factor Breakdown:

  Direct Links:        25/30  (+25)
    - A links to X: Yes (10 pts)
    - X links to A: Yes (10 pts)
    - Link frequency: 3 mentions (5 pts)

  Shared References:   18/25  (+18)
    - Common neighbors: 6 notes
    - Overlap ratio: 72%

  Structural:          20/25  (+20)
    - Same folder: Yes (10 pts)
    - Path distance: 1 hop (10 pts)

  Metadata:            15/20  (+15)
    - Shared tags: 3 (#project, #tech, #active)
    - Same type: Yes (project notes)

-------------------------------------------------

Interpretation:
  - STRONG: These notes are highly related
  - Direct bidirectional links exist
  - High shared context (6 common references)
  - Same folder reinforces relationship
  - Shared tags confirm topical similarity

=================================================
```

## Score Interpretation

| Score | Rating | Meaning |
|-------|--------|---------|
| 80-100 | Very Strong | Core relationship, highly integrated |
| 60-79 | Strong | Significant connection |
| 40-59 | Moderate | Notable relationship |
| 20-39 | Weak | Some connection exists |
| 0-19 | Minimal | Little to no relationship |

## Scoring Factors

The strength score considers:

1. **Direct Links** (up to 30 points)
   - Does A link to B?
   - Does B link to A?
   - How many times are they mentioned?

2. **Shared References** (up to 25 points)
   - Common neighbors count
   - Overlap ratio with total links

3. **Structural** (up to 25 points)
   - Same folder = higher connection
   - Shorter path = higher connection

4. **Metadata** (up to 20 points)
   - Shared tags
   - Same note type (if using frontmatter)

## Use Cases

- **Relationship validation**: "Is this connection as strong as I thought?"
- **Comparison**: "Which project is more related to this technology?"
- **Graph optimization**: "Should I add more links between these?"
- **Knowledge mapping**: "What's the strongest connection in this cluster?"

## Integration

Works well with other skills:
- **path**: Trace the actual link path between notes
- **common**: See the specific shared references
- **bidirectional**: Check if direct two-way link exists
- **clusters**: See which cluster each note belongs to

---

**Version:** 1.0.0
