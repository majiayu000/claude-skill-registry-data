---
name: campaign-analyzer
description: Analyze processed D&D sessions to extract and summarize campaign knowledge including NPCs, locations, quests, items, and factions. Use when the user wants to review campaign content, find specific entities, or understand the campaign narrative.
---

# Campaign Analyzer Skill

Extract and analyze campaign knowledge from processed D&D session data.

## What This Skill Does

This skill helps you understand and navigate your D&D campaign by:

1. **Extracting Campaign Knowledge**: Identifies NPCs, locations, quests, items, factions from session data
2. **Summarizing Campaign State**: Provides overview of active quests, key NPCs, and important locations
3. **Finding Entities**: Searches for specific NPCs, locations, or items across sessions
4. **Tracking Relationships**: Maps connections between NPCs, factions, and locations
5. **Analyzing Trends**: Identifies frequently mentioned entities and story arcs

## How It Works

The skill leverages:
- Session data files in `output/` directories
- Campaign knowledge base at `data/campaign_knowledge.json`
- MCP tool: `mcp__videochunking-dev__get_campaign_knowledge_summary`
- Knowledge extraction system from processed sessions

## Usage Scenarios

### Get Campaign Overview
User: "What NPCs have we encountered in our campaign?"
User: "Show me all the locations we've visited"
User: "What quests are currently active?"

### Search for Specific Entities
User: "Tell me about Lord Blackthorn"
User: "Where is the Temple of Shadows?"
User: "What do we know about the Dragon's Hoard quest?"

### Analyze Campaign Progression
User: "What happened in the last 5 sessions?"
User: "Which NPCs appear most frequently?"
User: "Show me the faction relationships"

### Cross-Reference Information
User: "Which quests involve the Dark Forest?"
User: "Who are the members of the Thieves Guild?"
User: "What items have we found in Waterdeep?"

## Data Sources

### Campaign Knowledge Base
Location: `data/campaign_knowledge.json`

Structure:
```json
{
  "npcs": [
    {
      "name": "Lord Blackthorn",
      "first_mentioned": "session_001",
      "appearances": ["session_001", "session_003"],
      "description": "Evil wizard seeking ancient artifacts",
      "relationships": ["enemy_of:party", "allied_with:Shadow_Cult"],
      "status": "active"
    }
  ],
  "locations": [...],
  "quests": [...],
  "items": [...],
  "factions": [...]
}
```

### Session Data Files
Location: `output/YYYYMMDD_HHMMSS_sessionid/sessionid_data.json`

Contains:
- Timestamped dialogue segments
- Speaker attributions
- IC/OOC classifications
- Extracted entities per segment

## Command Reference

```bash
# View campaign knowledge summary
python cli.py knowledge summary

# Search for specific NPC
python cli.py knowledge search --type npc --name "Lord Blackthorn"

# List all entities of a type
python cli.py knowledge list --type locations

# Export campaign knowledge
python cli.py knowledge export --format json
```

## MCP Tool Integration

Use `mcp__videochunking-dev__get_campaign_knowledge_summary` to quickly retrieve:
- Total count of NPCs, locations, quests, items, factions
- Recently mentioned entities
- Active quests list
- Campaign knowledge file status

## Analysis Capabilities

### Entity Frequency Analysis
Identifies most-mentioned NPCs, locations, and items to determine importance.

### Relationship Mapping
Tracks connections:
- NPC-to-NPC relationships (allies, enemies, family)
- NPC-to-Faction memberships
- Location-to-Quest associations
- Item-to-NPC ownership

### Timeline Reconstruction
Orders events chronologically based on session timestamps and quest progression.

### Quest Tracking
Monitors quest states:
- `proposed`: Quest mentioned but not accepted
- `active`: Party is working on this quest
- `completed`: Quest resolved
- `failed`: Quest failed or abandoned
- `on_hold`: Quest paused

## Output Formats

### Summary View
```
Campaign Knowledge Summary
==========================
NPCs: 47 (12 major, 35 minor)
Locations: 23 (8 cities, 15 dungeons/landmarks)
Quests: 15 (6 active, 7 completed, 2 failed)
Items: 34 (8 magical, 26 mundane)
Factions: 9 (4 allied, 3 hostile, 2 neutral)

Recent Activity:
- Lord Blackthorn mentioned in Session 12
- New location discovered: Crystal Caverns
- Quest "Dragon's Hoard" marked completed
```

### Detailed Entity View
```
NPC: Lord Blackthorn
====================
First Mentioned: Session 1 (2024-10-15)
Recent Appearances: Sessions 1, 3, 7, 12
Role: Primary Antagonist
Description: Powerful necromancer seeking to resurrect ancient evil
Relationships:
  - Enemy of the party
  - Leader of the Shadow Cult
  - Former apprentice of Merlin
Status: Active (last mentioned Session 12)
Related Quests:
  - "Stop the Ritual" (active)
  - "Find Blackthorn's Phylactery" (active)
```

### JSON Export
Structured data for integration with other tools or visualization.

## Best Practices

1. **Regular Updates**: Process sessions frequently to keep knowledge base current
2. **Review Extractions**: Manually verify extracted entities for accuracy
3. **Enrich Data**: Add manual notes and details to extracted entities
4. **Cross-Reference**: Link related entities to build comprehensive campaign view
5. **Export Regularly**: Back up campaign knowledge for safety

## Integration with Other Skills

- **video-chunk**: Processes sessions to generate knowledge data
- **session-processor**: Automates end-to-end processing including knowledge extraction
- **diagnostics-runner**: Verifies campaign knowledge file integrity

## Troubleshooting

### No Knowledge Data
**Issue**: Campaign knowledge file doesn't exist
**Solution**: Process at least one session with knowledge extraction enabled

### Missing Entities
**Issue**: Expected NPCs or locations not in knowledge base
**Solution**:
- Verify knowledge extraction is enabled in configuration
- Check if mentioned in IC dialogue (OOC mentions aren't extracted)
- Manually add entities to knowledge base

### Duplicate Entities
**Issue**: Same entity listed multiple times with different names
**Solution**:
- Use entity merging/deduplication features
- Standardize naming conventions
- Update session data with consistent names

### Outdated Information
**Issue**: Knowledge base shows old data
**Solution**:
- Re-process recent sessions
- Check session processing succeeded
- Verify knowledge extraction ran without errors

## Example Queries

```
"Show me all NPCs from the Thieves Guild faction"
"What locations are associated with the Dragon's Hoard quest?"
"Which sessions mention the Crystal Caverns?"
"List all magical items we've acquired"
"What active quests involve Lord Blackthorn?"
"Summarize what happened with the Shadow Cult"
```

## Future Enhancements

Potential additions:
- Visual relationship graphs
- Campaign timeline visualization
- Entity search with fuzzy matching
- Automatic quest progression tracking
- Integration with D&D Beyond or Roll20
- Character sheet tracking
- Party inventory management
