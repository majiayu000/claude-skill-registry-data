---
name: character-arc
description: Track and analyze character development arcs throughout the manuscript
category: analysis
---

# Character Arc Tracking Skill

Analyze character development and track character arcs across the narrative.

## Usage

```bash
/character-arc --character anna
/character-arc --all
```

## Features

- Track character appearances across sections
- Analyze character development progression
- Identify arc milestones (introduction, growth, climax, resolution)
- Detect inconsistencies in character behavior
- Visualize character journey

## Arc Analysis

Analyzes:
- **Introduction**: When and how character is introduced
- **Development**: Changes in traits, relationships, goals
- **Turning Points**: Key moments that transform the character
- **Resolution**: Final state and arc completion

## Query Example

```sql
SELECT
    section.sequence,
    section.content,
    character.description
FROM character:anna<-appears_in<-section
ORDER BY section.sequence
```
