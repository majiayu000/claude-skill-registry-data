---
name: gtnh-skill
description: This skill provides accurate data about GT New Horizons based on official data dumps. Use when answering questions about GTNH (GregTech New Horizons).
---

# GTNH Skill

To gain the proper context about GTNH, we can use the various resources at:
- ./beginner-faq.md - A basic set of information about GTNH, focusing on beginner-information.
- ./quest-structure.md - A detailed description of the quest system in GTNH with progression tiers. Good information to have before querying the database.

We can also use the "gtnh-skill.jar" CLI tool to query information. Quests often contain various tutorials and game information as the game progresses,
which is largely structured through the quest system itself. By reading quest information and understanding the progression, we can have accurate context about the game.


## CLI Tool Usage
```bash
java -jar gtnh-skill.jar info  # Show tables and row counts
java -jar gtnh-skill.jar query "SQL_QUERY (SQLite syntax)"
```

## Key Tables
- `quests_fts` - Full-text search (use `MATCH 'term'`)
- `quest_lines` - Quest categories (46 total)
- `quests` - All quests (3,684 total)
- `quest_prerequisites` - Quest dependencies
- `task_items` - Items required by quests
- `reward_items` - Quest rewards

## Examples
```bash
# Search for quests mentioning "quantum"
java -jar gtnh-skill.jar query "SELECT name FROM quests_fts WHERE quests_fts MATCH 'quantum'"

# List all quest lines in order
java -jar gtnh-skill.jar query "SELECT name FROM quest_lines ORDER BY display_order"

# Find quests in Tier 5
java -jar gtnh-skill.jar query "SELECT q.name FROM quests q JOIN quest_line_entries e ON q.id = e.quest_id JOIN quest_lines l ON e.quest_line_id = l.id WHERE l.name LIKE '%Tier 5%' LIMIT 20"

# Get prerequisites for a quest
java -jar gtnh-skill.jar query "SELECT p.name FROM quest_prerequisites qp JOIN quests q ON qp.quest_id = q.id JOIN quests p ON qp.prerequisite_quest_id = p.id WHERE q.name LIKE '%Quantum Storage%'"
```

## General Quest Structure

To help find relevant results, here is the general structure of quest progression:

## Non-database information

Not all questions can be answered with just the CLI tool / database. 

Other accurate sources:
- [GT New Horizons Wiki](https://wiki.gtnewhorizons.com/wiki/Main_Page) - Provides basic information and some tutorials. Links will need to be followed from this main page.
- [GT New Horizons Github](https://github.com/GTNewHorizons/GT-New-Horizons-Modpack) - rarely useful, but could contain useful information
- Pre-known knowledge about the installed mods in GTNH and minecraft - can be useful as a possibility, but **very often inaccurate** due to a high chance of hallucinations or outdated information.

If you cannot support your answer with the CLI tool or the wiki, it's still okay to present as a "possible" answer. 

## Answering questions

Once you have the proper context, you can form an answer. Try to rely on CLI/database data, then wiki content, and finally other sources. 
Make sure to mention where the information comes from so that the user can understand how to treat the information.
