---
name: search-skill-database
description: Query ALL available Skills database in Notion with filters. Load when user mentions "search skill database", "query notion", "search skills database", "find skills in notion", or "browse notion skills".
---

# Query Notion Database

Search and filter the Beam Nexus Skills database to discover skills created by teammates.

## Purpose

Browse the company skills library in Notion. Filter by team, integration, or skill name to find relevant skills. Returns skill metadata for display or import.

**Use cases:**
- Discover skills created by teammates
- Find skills for specific integrations (Beam AI, Linear, etc.)
- Check if a skill already exists before creating
- Browse skills by team (General, Solutions, Engineering, Sales)

**Time Estimate**: 1-2 minutes

---

## Workflow

### Step 1: Validate Configuration

**ALWAYS run configuration check first:**

```bash
python ../../notion-master/scripts/check_notion_config.py
```

**If configuration missing:**
- Option A: Run setup wizard: `python ../../notion-master/scripts/setup_notion.py`
- Option B: See [../../notion-master/references/setup-guide.md](../../notion-master/references/setup-guide.md)

**Expected output if configured:**
```
✅ ALL CHECKS PASSED
You're ready to use Notion skills
```

---

### Step 2: Query Database

Use the `query_db.py` script with filters:

**Basic query (all skills):**
```bash
python ../../notion-master/scripts/query_db.py
```

**Filter by team:**
```bash
python ../../notion-master/scripts/query_db.py --team General
python ../../notion-master/scripts/query_db.py --team Solutions
```

**Filter by integration:**
```bash
python ../../notion-master/scripts/query_db.py --integration "Beam AI"
python ../../notion-master/scripts/query_db.py --integration "Linear"
```

**Search by name:**
```bash
python ../../notion-master/scripts/query_db.py --name notion
python ../../notion-master/scripts/query_db.py --name agent
```

**Combined filters:**
```bash
python ../../notion-master/scripts/query_db.py --team Solutions --integration "Beam AI"
```

**Sort and limit:**
```bash
python ../../notion-master/scripts/query_db.py --sort name --limit 10
```

---

### Step 3: Display Results

**Human-readable output:**

The script automatically displays results in readable format:
```
[RESULTS] Found 5 skills

1. beam-list-agents
   Team: Solutions
   Description: List all agents in Beam AI workspace...
   Integrations: Beam AI
   Created: 2025-12-01
   URL: https://notion.so/...

2. query-notion-db
   Team: General
   Description: Query Notion databases with filters...
   Integrations: Notion
   Created: 2025-11-15
   URL: https://notion.so/...
```

**JSON output (for programmatic use):**
```bash
python ../../notion-master/scripts/query_db.py --json
```

Returns JSON array of skill objects with full metadata.

---

### Step 4: User Selection (Optional)

After displaying results, ask user which skill to import (if applicable):

```
Which skill would you like to import? (1-5, or 'none')
```

If user selects a skill:
1. Get the page ID from results
2. Trigger `import-skill-to-nexus` skill with page ID

---

## Available Filters

| Filter | Flag | Example | Description |
|--------|------|---------|-------------|
| Team | `--team` | `--team General` | General, Solutions, Engineering, Sales |
| Integration | `--integration` | `--integration "Beam AI"` | Tool the skill integrates with |
| Name | `--name` | `--name notion` | Partial match on skill name |
| Owner | `--owner` | `--owner user-id` | Filter by creator (user ID) |
| Sort | `--sort` | `--sort name` | created (default) or name |
| Limit | `--limit` | `--limit 10` | Max results to return |

---

## Error Handling

**Common errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check `NOTION_API_KEY` in `.env` |
| 404 Not Found | Database ID incorrect | Verify `NOTION_SKILLS_DB_ID` in `.env` |
| No results found | Filter too restrictive | Try broader filters |
| Network timeout | Connection issue | Check internet, retry |

**For detailed troubleshooting:**
- See [../../notion-master/references/error-handling.md](../../notion-master/references/error-handling.md)

---

## Integration with Other Skills

**Typical workflow:**
```
1. query-notion-db (find skills)
2. import-skill-to-nexus (download selected skill)
```

**Example:**
```
User: "Find Beam AI skills in Notion"

AI: [Runs query_db.py --integration "Beam AI"]
    [Displays 3 results]

    Which would you like to import?

User: "Number 2"

AI: [Triggers import-skill-to-nexus with page ID]
    [Downloads and installs skill]
```

---

## Advanced Usage

**Custom database query:**

For queries beyond the script's filters, use the Notion API directly or see:
- [../../notion-master/references/api-reference.md](../../notion-master/references/api-reference.md) - API patterns and examples

**Database schema reference:**
- [../../notion-master/references/database-schema.md](../../notion-master/references/database-schema.md) - Field definitions and filter examples

---

## Notes

- **Pagination**: Script automatically handles pagination (fetches all results)
- **Rate limits**: Notion allows 3 requests/second (script handles this)
- **Database ID**: Default is Beam Nexus Skills (`2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e`)
- **Team filter**: Matches exact team name (case-sensitive)
- **Name filter**: Partial match, case-insensitive

---

**Version**: 2.0
**Created**: 2025-11-04
**Updated**: 2025-12-10
**Status**: Production Ready
