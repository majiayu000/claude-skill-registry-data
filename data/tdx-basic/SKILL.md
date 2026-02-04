---
name: tdx-basic
description: Executes tdx CLI commands for Treasure Data. Covers `tdx databases`, `tdx tables`, `tdx query`, `tdx auth setup`, context management with profiles/sessions, and output formats (JSON/TSV/table). Use when users need tdx command syntax, authentication setup, database/table exploration, or query execution.
---

# tdx CLI - Basic Operations

## Setup

```bash
npm install -g @treasuredata/tdx

# Interactive setup (recommended)
tdx auth setup
tdx auth setup --profile production  # Multiple accounts

# Or manual: create ~/.config/tdx/.env
TDX_API_KEY=your-key-id/your-key-secret

# Verify
tdx auth
```

## Context Management

Context priority: CLI flags > session > project `tdx.json` > profile > global config

```bash
# Session context
tdx use database mydb
tdx use site jp01
tdx use profile production
tdx context              # View current
tdx context --clear      # Clear session
```

### Profiles (~/.config/tdx/tdx.json)

```json
{
  "profiles": {
    "production": { "site": "us01", "database": "analytics" },
    "dev": { "site": "jp01", "database": "dev_db" }
  }
}
```

### Project Config (tdx.json in project root)

```json
{
  "site": "us01",
  "database": "customer_analytics",
  "parent_segment": "active_users"
}
```

## Core Commands

### Databases

```bash
tdx databases                    # List all
tdx databases "prod_*"           # Filter with pattern
tdx databases --site jp01        # Specify site
tdx databases --json             # JSON output
```

Sites: `us01` (default), `jp01`, `eu01`, `ap02`

### Tables

```bash
tdx use database mydb            # Set context first
tdx tables                       # List tables
tdx tables "user_*"              # Filter
tdx describe users               # Schema
tdx show users --limit 10        # Preview data

# Pattern syntax
tdx tables "mydb.*"              # All tables from mydb
tdx tables "*.users"             # users table from all databases
```

### Queries

```bash
tdx query "select * from mydb.users limit 10"
tdx query -f query.sql           # From file
tdx query -                      # From stdin
echo "select 1" | tdx query -
tdx sg sql "Segment Name" | tdx query -  # Pipe segment SQL
```

### Output Formats

```bash
tdx databases --json             # JSON
tdx query "..." --jsonl          # JSON Lines (streaming)
tdx databases --tsv              # TSV
tdx databases --output out.json  # Save to file
```

## Global Options

```bash
tdx <command> --help             # Command help
--profile <name>                 # Use specific profile
--site <site>                    # us01, jp01, eu01, ap02
--json / --jsonl / --tsv         # Output format
--output <file>                  # Save to file
--dry-run                        # Preview without executing
```

## TD-Specific Conventions

- **Table naming**: `database_name.table_name`
- **Time column**: Unix timestamp (seconds since epoch), not datetime
- **Time filtering**: Use `td_interval(time, '-1d')` or `td_time_range(time, 'start', 'end')` for partition pruning
- **Timezone**: UTC default; use `td_interval(time, '-1d', 'JST')` for Japan

```sql
select time, from_unixtime(time) as datetime from mydb.events limit 1
```

## Common Issues

| Issue | Solution |
|-------|----------|
| TDX_API_KEY not found | `tdx auth setup` or create `~/.config/tdx/.env` |
| Database not found | Check site: `tdx databases --site jp01` |
| Pattern not working | Quote patterns: `tdx tables "prod_*"` |

## Project Folder Structure

tdx organizes resources into conventional folders:

```
my-project/
├── tdx.json                    # Project config (site, database, contexts)
├── parent_segments/            # Parent segment definitions
│   ├── customer-360.yml
│   └── demo-audience.yml
├── segments/                   # Child segments and journeys (per parent)
│   └── customer-360/
│       ├── tdx.json            # { "parent_segment": "Customer 360" }
│       ├── high-value.yml      # Segment
│       ├── onboarding.yml      # Journey (type: journey)
│       └── marketing/          # Folder organization
│           └── newsletter.yml
├── workflows/                  # Digdag workflow projects
│   └── daily-etl/
│       ├── tdx.json            # { "workflow_project": "daily-etl" }
│       └── main.dig
└── agents/                     # LLM agents (per project)
    └── my-llm-project/
        ├── tdx.json            # { "llm_project": "My LLM Project" }
        ├── support-agent/
        │   ├── agent.yml
        │   └── prompt.md
        └── knowledge_bases/
            └── faq.yml
```

Each `tdx.json` stores context for its directory—commands run from any subdirectory use the nearest config.

## Resources

- Documentation: https://tdx.treasuredata.com/
- Related: **sql-skills/time-filtering**, **segment**, **journey**, **agent**
