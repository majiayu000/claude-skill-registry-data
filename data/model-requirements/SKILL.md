---
name: model-requirements
description: Use this skill when gathering requirements for new BigQuery data models OR when asked to edit existing queries in bqetl. For new models, guides structured requirements interviews. For existing queries, understands current model, checks downstream dependencies, and gathers requirements for changes. Works as pre-planning before query-writer skill.
---

# Model Requirements Gatherer

**Composable:** Works before query-writer (provides requirements), references metadata-manager patterns (DAG/scheduling), uses bigquery-etl-core conventions
**When to use:**
- Before writing SQL for new models
- Before modifying existing queries in bqetl (to understand impact and gather change requirements)
- When gathering requirements from data scientists/stakeholders
- When planning data model architecture

## Overview

This skill guides requirements gathering for building and modifying BigQuery tables. It:

1. **For new models:** Structured requirements interview where user provides source tables, grain, and business logic
2. **For existing queries:** Understands current model from local files, identifies downstream dependencies, gathers requirements for changes
3. **Validates dependencies:** Uses local schema/metadata files first, then Glean Dictionary, then DataHub as last resort
4. **Warns about downstream impact:** When modifying existing tables, identifies and warns about affected downstream models
5. **Suggests useful columns:** Based on requirements and available source data
6. **Produces dual outputs:** Requirements doc (for stakeholders) + condensed working notes (for SQL development)

## When to Use This Skill

**Use this skill when:**
- Starting a new data model from scratch
- A data scientist or stakeholder requests a new table/view
- User asks to modify/edit an existing query in bqetl
- Planning architecture for a new ETL pipeline
- You need to understand downstream impact before making changes

**Do NOT use this skill for:**
- Ad-hoc analysis queries (not part of bqetl)
- Questions about what data exists (that's exploration, not construction)

## Discovery Priority for Construction

When validating dependencies or checking schemas:

1. **Local `/sql` directory** - ALWAYS check first (schema.yaml, metadata.yaml, query.sql files)
2. **Glean Dictionary** - For `_live`/`_stable` tables via https://dictionary.telemetry.mozilla.org/
3. **DataHub** - Last resort or to validate what you've found

**Key principle:** User provides source tables. You validate they exist and understand downstream impact.

## Requirements Interview Process

### Step 1: Understand the Business Need

Ask the user these key questions (don't ask all at once - follow conversational flow):

**Core questions:**
1. **What business activity does this model represent?** (e.g., "install attribution", "user retention", "revenue reporting")
2. **Who will use this model and what decisions will they make with it?** (data scientists, dashboards, ML models)
3. **What are 3-5 key questions this model should answer?** (be specific, e.g., "How many installs per campaign per day?")

**Capture:**
- Business purpose in 1-2 sentences
- Primary stakeholders/consumers
- Core use cases and questions

### Step 2: Define the Grain

This is THE most critical decision - everything else flows from grain.

**Ask:** "What should one row represent?"

**Good examples:**
- "One row per client per day"
- "One row per install event"
- "One row per search interaction"
- "One row per subscription, aggregated monthly"

**Bad/vague examples:**
- "User data" (what grain? per day? per event? lifetime?)
- "Search metrics" (per query? per day? per client?)

**If grain is unclear, help clarify:**
- "Will this be daily aggregates or event-level data?"
- "Should this track changes over time or snapshot state?"
- "How will downstream consumers typically filter/join this?"

**Capture:**
- Exact grain statement
- Time dimension (daily, hourly, event-level, lifetime)

### Step 3: Get Source Tables from User

**Ask:** "What source tables should this model use?"

**User provides table names** - they tell you what upstream models/tables to use.

#### For Each Source Table

**Capture from user:**
- Full table name (project.dataset.table)
- Why this table is needed (what fields/data it provides)
- Join keys (how it connects to other sources)
- Any filter logic (WHERE clauses, date ranges)

#### Validate Source Tables Exist

After user provides source tables, validate they exist using discovery priority:

1. **Check local `/sql` directory:**
   ```bash
   find sql/ -path "*/<dataset>/<table>"
   ```
   - Read schema.yaml and metadata.yaml if found
   - Understand available columns for later column suggestions

2. **For `_live`/`_stable` tables, check Glean Dictionary:**
   - URL: `https://dictionary.telemetry.mozilla.org/apps/<app_id>/tables/<table_name>`
   - Use WebFetch to get schema

3. **If not found in local files or Glean, use DataHub as last resort:**
   - Validate table exists
   - Get schema for join key validation

**Capture:**
- Table description (from metadata.yaml or Glean Dictionary)
- Owner (from metadata.yaml)
- Available columns (for later column suggestions)

### Step 4: Understand Transformations

**Ask:** "What transformations or calculations are needed?"

**Listen for:**
- Aggregations (SUM, COUNT, AVG, etc.)
- Filtering logic (active users, specific countries, etc.)
- Derived fields (calculations, CASE statements, etc.)
- Deduplication logic
- Window functions

**Capture:**
- High-level transformation logic (don't write SQL yet!)
- Key derived fields and their business definitions
- Any complex business rules or edge cases

### Step 5: Determine Scheduling and Partitioning

**Ask scheduling questions:**
1. **How fresh does this data need to be?** (daily, hourly, real-time)
2. **How much history do we need?** (30 days, 1 year, all time)
3. **Will this run incrementally or full refresh?** (usually incremental for large tables)

**Infer partitioning:**
- Daily grain → daily partitioning
- Hourly grain → hourly partitioning
- Event-level → usually daily partitioning on submission_date

**Reference metadata-manager patterns:**
- Check similar tables in same product area for DAG patterns
- Suggest existing DAGs when appropriate

**Capture:**
- Refresh frequency
- Partitioning strategy
- Retention policy
- Candidate DAG (or note: "new DAG needed")

### Step 6: Identify Dependencies and Blockers

**Ask:** "Are there any blockers or dependencies we should know about?"

**Common blockers:**
- Upstream tables don't exist yet
- Need access to specific datasets
- Waiting for new metrics to be added to Glean schema
- Need to coordinate with another team

**Capture:**
- Upstream dependencies (what must exist first)
- Downstream consumers (what will use this)
- Blockers (with owners/timelines if known)

## After Gathering Requirements: Validate and Suggest

After gathering full requirements from user:

### 1. Check Downstream Dependencies (if modifying existing table)

**CRITICAL:** If user is modifying an existing query, warn about downstream impact.

1. **Check local files first** - Look for tables that reference this one in their query.sql:
   ```bash
   grep -r "project.dataset.table_name" sql/ --include="query.sql"
   ```

2. **Check metadata.yaml files** for explicit dependencies in `depends_on` fields

3. **If needed, use DataHub lineage to validate:**
   ```bash
   python .claude/skills/metadata-manager/scripts/datahub_lineage.py <table_name> --direction downstream
   ```

**Warn user:** "⚠️ This table is used by X downstream models: [list]. Changes may impact these."

### 2. Suggest Useful Columns

Based on requirements and available source columns:

1. **Review source table schemas** (from local files, Glean Dictionary, or DataHub)
2. **Identify useful columns** that match the stated requirements
3. **Suggest fields for:**
   - Join keys
   - Dimensions for grouping (country, channel, version, etc.)
   - Metrics for calculations (counts, sums, etc.)
   - Timestamps for partitioning/filtering

**Example:** "Based on your requirements to track installs by campaign, these columns from adjust_derived.installs_v1 would be useful: campaign_id, campaign_name, install_date, install_count"

## Output Format

Generate TWO artifacts:

### 1. Requirements Document (Full)

Use the template from `assets/requirements_template.md` and populate with:

**Include these sections:**
- Overview (business purpose, 1-2 sentences)
- Grain (exact row definition)
- Source Data (table with join keys, filters, notes)
- Field Summary (key derived fields and their business logic)
- Questions This Model Should Answer (3-5 specific questions)
- Dependencies (upstream, downstream, blockers)
- Validation & QA (row count checks, null thresholds, freshness)
- Owner & Status (primary owner, reviewers, target date)

**Optional sections (include if relevant):**
- Useful Links (if user provided notebooks, dashboards, prior work)
- Lineage Diagram (if DataHub lineage available)
- Data Governance (if PII, retention policies, or classification discussed)

**Minimize busywork:**
- Skip sections not relevant to this model
- Keep descriptions concise
- Focus on what helps with SQL development

### 2. Working Notes (Condensed)

Create a condensed version for SQL development:

```markdown
## <Model Name> - Working Notes

**Grain:** <one row per ...>

**Source Tables:**
- `project.dataset.table1` - <why needed>
- `project.dataset.table2` - <why needed>

**Key Transformations:**
- <transformation 1>
- <transformation 2>

**Derived Fields:**
- `field_name` - <business logic>

**Partitioning:** <daily/hourly on field>

**Scheduling:** <DAG name or "new DAG needed">

**Blockers:** <any blockers or "None">
```

## Integration with Other Skills

### Before query-writer

This skill runs **before** query-writer to gather requirements. After generating requirements doc and working notes:

1. Ask user: "Ready to start writing SQL based on these requirements?"
2. If yes, pass working notes to query-writer skill
3. query-writer uses requirements as context for SQL development

### References metadata-manager

Use metadata-manager patterns for:
- Schema validation (priority: /sql → Glean Dictionary → DataHub)
- Partitioning strategies (daily vs hourly)
- DAG configuration patterns

### Uses datahub_lineage.py (when needed)

For impact analysis and validation:
- Check downstream dependencies when modifying existing tables
- Validate upstream dependencies if user is unsure
- Last resort after checking local files and Glean Dictionary

## Best Practices

### For Requirements Interviews

- **Don't ask all questions at once** - follow conversational flow
- **Clarify vague grain** - grain is the foundation, must be precise
- **User provides source tables** - don't suggest alternatives unless they're unsure
- **Focus on business logic** - not SQL syntax yet
- **Capture decisions and rationale** - why we chose X over Y

### For Modifying Existing Queries

- **ALWAYS check downstream dependencies first** - warn about impact
- **Read existing query.sql** - understand current logic before planning changes
- **Check for schema changes** - schema changes require coordination with downstream consumers
- **Document impact analysis** - include in requirements doc

### For Validation and Column Suggestions

- **Follow discovery priority** - local files → Glean Dictionary → DataHub
- **Validate sources exist** - don't assume tables are available
- **Review source schemas** - understand available columns before suggesting
- **Match requirements to columns** - suggest fields that directly support stated needs

### For Output Quality

- **Make requirements doc useful for SQL development** - not just paperwork
- **Working notes should be quick reference** - condense to essentials
- **Skip irrelevant sections** - don't force every template field
- **Include downstream impact** - critical for modification scenarios

## Key Commands Reference

```bash
# Check downstream dependencies when modifying existing table
grep -r "project.dataset.table_name" sql/ --include="query.sql"

# Find schema for source table
find sql/ -path "*/<dataset>/<table>/schema.yaml"

# Check metadata.yaml for dependencies
find sql/ -path "*/<dataset>/<table>/metadata.yaml"

# Validate downstream impact with DataHub (if needed)
python .claude/skills/metadata-manager/scripts/datahub_lineage.py <table_name> --direction downstream

# Find tables by keyword
find sql/ -path "*/*keyword*" -name "schema.yaml"
```

## Common Scenarios

### Scenario 1: New Model - Install Attribution

**User says:** "I need to track install attribution from Adjust using adjust_derived.installs_v1"

**Workflow:**
1. **Gather requirements:** Grain (one row per install), business questions, transformations needed
2. **User provides source:** `adjust_derived.installs_v1`
3. **Validate source exists:** Check local schema.yaml or DataHub
4. **Review source columns:** campaign_id, campaign_name, install_date, install_count
5. **Suggest useful columns:** Based on requirements about attribution
6. **Output:** Requirements doc + working notes for query-writer

### Scenario 2: Modify Existing Query

**User says:** "Add country dimension to telemetry_derived.clients_daily_v1"

**Workflow:**
1. **Read existing query.sql** to understand current logic
2. **Check downstream dependencies:**
   ```bash
   grep -r "clients_daily_v1" sql/ --include="query.sql"
   ```
3. **Warn about impact:** "⚠️ This table is used by 47 downstream models. Schema change will require coordination."
4. **Gather requirements:** Why country is needed, how it affects downstream
5. **Validate country exists in source:** Check normalized_country column availability
6. **Output:** Requirements doc with impact analysis + working notes

### Scenario 3: Understanding Upstream Dependencies

**User says:** "Create revenue dashboard model" but unsure what upstream tables exist

**Workflow:**
1. **Gather what user knows:** Grain, business questions, general data needs
2. **User says:** "I think there's a revenue table somewhere?"
3. **Help find it:**
   ```bash
   find sql/ -path "*/revenue*" -name "schema.yaml"
   ```
4. **Show options:** revenue_derived.revenue_data_v1 found
5. **User confirms:** "Yes, use that one"
6. **Continue with validation and column suggestions**

## Reference Files

- `assets/requirements_template.md` - Full requirements document template
- See metadata-manager skill for schema discovery patterns
