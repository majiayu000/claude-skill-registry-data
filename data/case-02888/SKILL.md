---
name: liudao-heritage
description: Search, enrich, and manage family heritage and historical relationship data from the LiùDào (六道) SQLite database. Use this skill when answering questions about historical figures, calculating relationship paths (A的B), or adding new personal records with privacy controls.
---



### Helper Behavior Review

`python scripts/_run.py` is an optional helper whose behavior should be compared with this skill's documented purpose before use. Show what the script does, explain any mismatch with the user-facing description, and run it only when the user explicitly wants that diagnostic path.

# 六道 (LiùDào) Heritage Manager

This skill provides access to the LiùDào family heritage and relationship database. It allows you to query historical figures, analyze relationship networks, and manage personal data with strict privacy controls.

## Core Capabilities

1. **Search Database**: Look up people by name, including their basic info, relationships, and milestones.
2. **Relationship Engine**: Resolve complex queries like "A的B" (e.g., "康熙的父亲").
3. **Data Enrichment**: Safely upsert new records or append milestones (history today) to existing ones.

## Environment Details

- **Database Path**: `/home/admin/.openclaw/workspace/liudao-bot/data/liudao.db`
- **Core Scripts**: Located in `/home/admin/.openclaw/workspace/liudao-bot/`
- **User Privacy**: For private entries (e.g., family members), ensure you pass the correct `viewer_id` (e.g., `1234567890` for the specific authorized user).

## Workflows

### 1. Searching for a Person
When a user asks about a specific historical figure or family member:
- Run the python search script passing the name and the user's ID for privacy.
- Example: `python3 scripts/search_person.py "康熙" --viewer_id "5104087055"`

### 2. Resolving Relationships ("A的B")
When a user asks relationship questions (e.g., "朱元璋的长子是谁？"):
- Use the relation engine script.
- Example: `python3 scripts/resolve_relation.py "朱元璋" "长子"`

### 3. Adding/Editing Data
For inserting a new person or adding milestones:
- Write a quick python script using `db_manager.py`'s `upsert_person` method.
- Ensure `is_private=1` and `creator_id` are set when adding personal family data.

## Important Notes
- Always parse the `relations_json` and `milestones_json` carefully; they contain structured relationship links and life events.
- See `references/db_schema.md` for exact table structures.