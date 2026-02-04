---
name: exa-websets-search
description: Use for creating websets, running searches, importing CSV data, managing items, and adding enrichments to extract structured data.
---

# Exa Websets Search

Comprehensive webset management including creation, search, imports, items, and enrichments.

**Use `--help` to see available commands and verify usage before running:**
```bash
exa-ai <command> --help
```

## Working with Complex Shell Commands

When using the Bash tool with complex shell syntax, follow these best practices for reliability:

1. **Run commands directly**: Capture JSON output directly rather than nesting command substitutions
2. **Parse in subsequent steps**: Use `jq` to parse output in a follow-up command if needed
3. **Avoid nested substitutions**: Complex nested `$(...)` can be fragile; break into sequential steps

Example:
```bash
# Less reliable: nested command substitution
webset_id=$(exa-ai webset-create --search '{"query":"tech startups","count":1}' | jq -r '.webset_id')

# More reliable: run directly, then parse
exa-ai webset-create --search '{"query":"tech startups","count":1}'
# Then in a follow-up command if needed:
webset_id=$(cat output.json | jq -r '.webset_id')
```

## Critical Requirements

**Universal rules across all operations:**

1. **Start with minimal counts (1-5 results)**: Initial searches are test spikes to validate quality. ALWAYS default to count:1 unless user explicitly requests more.
2. **Three-step workflow - Validate, Expand, Enrich**: (1) Create with count:1 to test search quality, (2) Expand search count if results are good, (3) Add enrichments only after validated, expanded results.
3. **No enrichments during validation**: Never add enrichments when testing with count:1. Validate search quality first, expand count second, add enrichments last.
4. **Avoid --wait flag**: Do NOT use `--wait` flag in commands. It's designed for human interactive use, not automated workflows.
5. **Maintain query AND criteria consistency**: When scaling up or appending searches, use the EXACT same query AND criteria that you validated. Omitting criteria causes Exa to regenerate them on-the-fly, producing inconsistent results.

## Credit Costs

**Pricing**: $50/month = 8,000 credits ($0.00625 per credit)

**Cost per operation**:
- Each webset item: 10 credits ($0.0625)
- Standard enrichment: 2 credits ($0.0125)
- Email enrichment: 5 credits ($0.03125)

**Why start with count:1**: Testing with 1 result costs 10 credits ($0.0625). A failed search with count:100 wastes 1,000 credits ($6.25) - 100x more expensive.

**Why enrich last**: Enriching bad results wastes credits. Always validate first, expand second, enrich last.

## Quick Command Reference

`exa-ai --help`

## Output Formats

All exa-ai webset commands support output formats:
- **JSON (default)**: Pipe to `jq` to extract specific fields (e.g., `| jq -r '.webset_id'`)
- **toon**: Compact, readable format for direct viewing
- **pretty**: Human-friendly formatted output
- **text**: Plain text output

# Webset Management

Core operations for managing webset collections.

## Entity Types

- `company`: Companies and organizations
- `person`: Individual people
- `article`: News articles and blog posts
- `research_paper`: Academic papers
- `custom`: Custom entity types (define with --entity-description)

## Create Webset from Search

```bash
webset_id=$(exa-ai webset-create \
  --search '{"query":"AI startups in San Francisco","count":1}' | jq -r '.webset_id')
```

## Create with Detailed Search Criteria

```bash
exa-ai webset-create \
  --search '{
    "query": "Technology companies focused on developer tools",
    "count": 1,
    "entity": {
      "type": "company"
    },
    "criteria": [
      {
        "description": "Companies with 50-500 employees indicating growth stage"
      },
      {
        "description": "Primary product is developer tools, APIs, or infrastructure"
      }
    ]
  }'
```

## Create with Custom Entity

```bash
exa-ai webset-create \
  --search '{
    "query": "Nonprofits focused on economic justice",
    "count": 1,
    "entity": {
      "type": "custom",
      "description": "nonprofit"
    },
    "criteria": [
      {
        "description": "Primary focus on economic justice"
      },
      {
        "description": "Annual operating budget between $1M and $10M"
      }
    ]
  }'
```

## Create from CSV Import

```bash
import_id=$(exa-ai import-create companies.csv \
  --count 100 \
  --title "Companies" \
  --format csv \
  --entity-type company | jq -r '.import_id')

exa-ai webset-create --import $import_id
```

## Three-Step Workflow: Validate → Expand → Enrich

### Step 1: VALIDATE - Create with count:1 (NO enrichments)

```bash
webset_id=$(exa-ai webset-create \
  --search '{"query":"tech startups","count":1}' | jq -r '.webset_id')

exa-ai webset-item-list $webset_id
```

**⚠️ REQUIRED: Manually verify the result is relevant before continuing. If not, adjust the query and start over.**

---

### Step 2: EXPAND - Gradually increase count with verification at each stage

```bash
# Expand to 2 results (use same query and criteria from validation)
exa-ai webset-search-create $webset_id \
  --query "tech startups" \
  --behavior override \
  --count 2

exa-ai webset-item-list $webset_id
```

**⚠️ REQUIRED: Check quality at this scale. Repeat with larger counts (5, 10, 25, 50, 100) until you reach your target.**

**Loop this step:** Keep expanding gradually (2 → 5 → 10 → 25 → 50 → 100) with verification between each expansion.

---

### Step 3: ENRICH - Add enrichments only after confirming quality

```bash
exa-ai enrichment-create $webset_id \
  --description "Company website" --format url --title "Website"

exa-ai enrichment-create $webset_id \
  --description "Employee count" --format text --title "Team Size"
```

## Interpreting Criterion Success Rates

**CRITICAL**: Criteria are evaluated conditionally - when one criterion fails, others may not run. A low success rate doesn't indicate that criterion is restrictive; it means OTHER criteria are filtering results first. Only interpret a low success rate as "restrictive" when OTHER criteria have high success rates (>80%).

## Manage Websets

```bash
exa-ai webset-list
exa-ai webset-get ws_abc123
exa-ai webset-update ws_abc123 --metadata '{"status":"active","owner":"team"}'
exa-ai webset-delete ws_abc123
```

---

# Search Operations

Run searches within a webset to add new items.

## Search Behavior

Control how new search results are combined with existing items:

- **append** (default): Add new items to existing collection
  - Requires previous search results to exist
  - Error if webset has no previous search: "No previous search found"
  - Default behavior when `--behavior` is omitted

- **override**: Replace entire collection with search results
  - REQUIRED for first search on a webset
  - Use when starting fresh or completely replacing results

**CRITICAL - First search requirement**: The first `webset-search-create` on a webset MUST explicitly use `--behavior override`. Since the default is append, omitting `--behavior` will fail with "No previous search found" error. Subsequent searches can omit the flag (defaults to append).

## Query and Criteria Consistency

**CRITICAL**: When appending or scaling up searches, maintain IDENTICAL query and criteria from your validated search.

### Why This Matters

Using different criteria causes Exa to generate new search parameters on-the-fly, which:
- Violates consistency and produces mismatched results
- Reduces result quality compared to validated criteria
- Makes it impossible to reproduce or debug issues

### Complete Example

```bash
# Step 1: Test search with criteria (MUST use override for first search)
exa-ai webset-search-create ws_abc123 \
  --query "Progressive nonprofits in California" \
  --behavior override \
  --count 1 \
  --criteria '[
    {"description": "Annual budget between $1M and $10M"},
    {"description": "Primary focus on economic justice, affordability, living wages, or worker power"},
    {"description": "Established communications, narrative strategy, or messaging function"}
  ]'

# Verify quality, then append MORE results with IDENTICAL query and criteria
exa-ai webset-search-create ws_abc123 \
  --query "Progressive nonprofits in California" \
  --behavior append \
  --count 5 \
  --criteria '[
    {"description": "Annual budget between $1M and $10M"},
    {"description": "Primary focus on economic justice, affordability, living wages, or worker power"},
    {"description": "Established communications, narrative strategy, or messaging function"}
  ]'
```

### Best Practice: Save Criteria to File

```bash
# Create criteria file once
cat > criteria.json <<'EOF'
[
  {"description": "Annual budget between $1M and $10M"},
  {"description": "Primary focus on economic justice, affordability, living wages, or worker power"},
  {"description": "Established communications, narrative strategy, or messaging function"}
]
EOF

# Use consistently across all searches (first search needs override)
exa-ai webset-search-create ws_abc123 \
  --query "Progressive nonprofits in California" \
  --behavior override \
  --count 1 \
  --criteria @criteria.json

exa-ai webset-search-create ws_abc123 \
  --query "Progressive nonprofits in California" \
  --behavior append \
  --count 5 \
  --criteria @criteria.json
```

## Basic Search Operations

```bash
# First search on webset (must use override)
exa-ai webset-search-create ws_abc123 \
  --query "AI startups in San Francisco" \
  --behavior override \
  --count 1

# Append to collection
exa-ai webset-search-create ws_abc123 \
  --query "SaaS companies Series B" \
  --behavior append \
  --count 1

# Override collection
exa-ai webset-search-create ws_abc123 \
  --query "top tech companies" \
  --behavior override \
  --count 1
```

## Monitor Search Progress

```bash
webset_id="ws_abc123"
search_id=$(exa-ai webset-search-create $webset_id \
  --query "fintech startups" \
  --behavior override \
  --count 1 | jq -r '.search_id')

exa-ai webset-search-get $webset_id $search_id
exa-ai webset-search-cancel $webset_id $search_id
```

---

# CSV Imports

Upload CSV files to create websets from existing datasets.

## CSV Format Requirements

1. First row contains column headers
2. Each row represents one entity
3. Include at minimum a name or identifier column

## Basic Import Workflow

```bash
# Create import
import_id=$(exa-ai import-create companies.csv \
  --count 100 \
  --title "Tech Companies" \
  --format csv \
  --entity-type company | jq -r '.import_id')

# Create webset from import
webset_id=$(exa-ai webset-create --import $import_id | jq -r '.webset_id')
```

## Custom Entity Type

```bash
exa-ai import-create products.csv \
  --count 5 \
  --title "Product List" \
  --format csv \
  --entity-type custom \
  --entity-description "Consumer electronics products"
```

## Manage Imports

```bash
exa-ai import-list
exa-ai import-get imp_abc123
```

---

# Import vs Search Scope

`--import` loads data for enrichment. `search.scope` filters searches to specific sources.

**⚠️ NEVER use same ID in both - returns 400:**

```bash
# ❌ INVALID
exa-ai webset-create --import import_abc \
  --search '{"scope":[{"source":"import","id":"import_abc"}]}'

# ✅ Scoped search only
exa-ai webset-create \
  --search '{"query":"CEOs","scope":[{"source":"import","id":"import_abc"}]}'

# ✅ Relationship traversal
exa-ai webset-search-create ws_abc --query "investors" --behavior override \
  --scope '[{"source":"webset","id":"webset_abc","relationship":{"definition":"investors of","limit":5}}]'
```

---

# Item Management

Manage individual items in websets.

## Basic Operations

```bash
# List items
exa-ai webset-item-list ws_abc123
exa-ai webset-item-list ws_abc123 --output-format pretty

# Get item details
exa-ai webset-item-get item_xyz789

# Delete item
exa-ai webset-item-delete item_xyz789
```

## Extract Item Data

```bash
# Get all item IDs
exa-ai webset-item-list ws_abc123 --output-format json | jq -r '.[].id'

# Count items
exa-ai webset-item-list ws_abc123 --output-format json | jq 'length'
```

---

# Enrichments

Add structured data fields to all items in a webset using AI extraction.

## Enrichment Formats

- **text**: Free-form text extraction (employee count, description, technology stack)
- **url**: Extract URLs only (website, LinkedIn, GitHub)
- **options**: Categorical data with predefined options (industry, funding stage, size range)

## Key Concepts

- **description**: The primary AI prompt that drives extraction. This tells the enrichment WHAT to extract. (Can be updated)
- **instructions**: Optional additional guidance on HOW to extract or format. (Creation-only, cannot be updated)
- Use `exa-ai enrichment-create --help` and `exa-ai enrichment-update --help` to see all available parameters

## Create Enrichments

```bash
# Text enrichment
exa-ai enrichment-create ws_abc123 \
  --description "Number of employees as of latest data" \
  --format text \
  --title "Team Size"

# URL enrichment
exa-ai enrichment-create ws_abc123 \
  --description "Primary company website URL" \
  --format url \
  --title "Website"

# Options enrichment
exa-ai enrichment-create ws_abc123 \
  --description "Current funding stage" \
  --format options \
  --options '[
    {"label":"Pre-seed"},
    {"label":"Seed"},
    {"label":"Series A"},
    {"label":"Series B"},
    {"label":"Series C+"},
    {"label":"Public"}
  ]' \
  --title "Funding Stage"
```

## Use Options from File

```bash
cat > industries.json <<'EOF'
[
  {"label": "SaaS"},
  {"label": "Developer Tools"},
  {"label": "AI/ML"},
  {"label": "Fintech"},
  {"label": "Healthcare"},
  {"label": "Other"}
]
EOF

exa-ai enrichment-create ws_abc123 \
  --description "Primary industry or sector" \
  --format options \
  --options @industries.json \
  --title "Industry"
```

## Add Instructions for Precision

```bash
exa-ai enrichment-create ws_abc123 \
  --description "Technology stack" \
  --format text \
  --instructions "Focus only on backend technologies and databases. Ignore frontend frameworks." \
  --title "Backend Tech"
```

## Manage Enrichments

```bash
# List enrichments
exa-ai enrichment-list ws_abc123
exa-ai enrichment-list ws_abc123 --output-format pretty

# Get details
exa-ai enrichment-get ws_abc123 enr_xyz789

# Update extraction prompt (description)
exa-ai enrichment-update ws_abc123 enr_xyz789 \
  --description "Exact employee count from most recent source"

# Update format and options
exa-ai enrichment-update ws_abc123 enr_xyz789 \
  --format options \
  --options '[{"label":"Small"},{"label":"Medium"},{"label":"Large"}]'

# Update metadata
exa-ai enrichment-update ws_abc123 enr_xyz789 \
  --metadata '{"source":"manual","updated":"2024-01-15"}'

# Note: Cannot update --instructions or --title (creation-only parameters)
# To change instructions, delete and recreate the enrichment

# Delete
exa-ai enrichment-delete ws_abc123 enr_xyz789

# Cancel running enrichment
exa-ai enrichment-cancel ws_abc123 enr_xyz789
```

## Common Enrichment Patterns

**Company websets**: Website (url), Team Size (text), Funding Stage (options), Industry (options)

**Person websets**: LinkedIn (url), Job Title (text), Company (text), Location (text)

**Research papers**: Publication Year (text), Authors (text), Venue (text), Research Area (options)

---

# Best Practices

1. **Start small, validate, then scale**: Always use count:1 for initial searches
2. **Follow three-step workflow**: Validate → Expand → Enrich
3. **Never enrich during validation**: Only enrich after validated, expanded results
4. **Avoid --wait flag**: Do NOT use `--wait` in commands. It's designed for human interactive use, not automated workflows.
5. **Maintain query AND criteria consistency**: When appending or scaling up, use IDENTICAL query and criteria from validated search. Save criteria to file for consistency.
6. **CRITICAL - First search must use override**: The library defaults to `--behavior append`. First search on a webset MUST explicitly use `--behavior override` or it will fail with "No previous search found" error.
7. **Use correct parameter names**:
   - Use `--behavior append` or `--behavior override` (NOT `--mode`)
   - Commands like `webset-search-get` require both webset_id and search_id
8. **Choose specific entity types**: Use company, person, etc. for better results
9. **Save IDs**: Use `jq` to extract and save IDs for subsequent commands

---

# Detailed Reference

For complete command references, syntax, and all options, consult [REFERENCE.md](REFERENCE.md) and component-specific reference files.

### Shared Requirements

<shared-requirements>

## Schema Design

### MUST: Use object wrapper for schemas

**Applies to**: answer, search, find-similar, get-contents

When using schema parameters (`--output-schema` or `--summary-schema`), always wrap properties in an object:

```json
{"type":"object","properties":{"field_name":{"type":"string"}}}
```

**DO NOT** use bare properties without the object wrapper:
```json
{"properties":{"field_name":{"type":"string"}}}  // ❌ Missing "type":"object"
```

**Why**: The Exa API requires a valid JSON Schema with an object type at the root level. Omitting this causes validation errors.

**Examples**:
```bash
# ✅ CORRECT - object wrapper included
exa-ai search "AI news" \
  --summary-schema '{"type":"object","properties":{"headline":{"type":"string"}}}'

# ❌ WRONG - missing object wrapper
exa-ai search "AI news" \
  --summary-schema '{"properties":{"headline":{"type":"string"}}}'
```

---

## Output Format Selection

### MUST NOT: Mix toon format with jq

**Applies to**: answer, context, search, find-similar, get-contents

`toon` format produces YAML-like output, not JSON. DO NOT pipe toon output to jq for parsing:

```bash
# ❌ WRONG - toon is not JSON
exa-ai search "query" --output-format toon | jq -r '.results'

# ✅ CORRECT - use JSON (default) with jq
exa-ai search "query" | jq -r '.results[].title'

# ✅ CORRECT - use toon for direct reading only
exa-ai search "query" --output-format toon
```

**Why**: jq expects valid JSON input. toon format is designed for human readability and produces YAML-like output that jq cannot parse.

### SHOULD: Choose one output approach

**Applies to**: answer, context, search, find-similar, get-contents

Pick one strategy and stick with it throughout your workflow:

1. **Approach 1: toon only** - Compact YAML-like output for direct reading
   - Use when: Reading output directly, no further processing needed
   - Token savings: ~40% reduction vs JSON
   - Example: `exa-ai search "query" --output-format toon`

2. **Approach 2: JSON + jq** - Extract specific fields programmatically
   - Use when: Need to extract specific fields or pipe to other commands
   - Token savings: ~80-90% reduction (extracts only needed fields)
   - Example: `exa-ai search "query" | jq -r '.results[].title'`

3. **Approach 3: Schemas + jq** - Structured data extraction with validation
   - Use when: Need consistent structured output across multiple queries
   - Token savings: ~85% reduction + consistent schema
   - Example: `exa-ai search "query" --summary-schema '{...}' | jq -r '.results[].summary | fromjson'`

**Why**: Mixing approaches increases complexity and token usage. Choosing one approach optimizes for your use case.

---

## Shell Command Best Practices

### MUST: Run commands directly, parse separately

**Applies to**: monitor, search (websets), research, and all skills using complex commands

When using the Bash tool with complex shell syntax, run commands directly and parse output in separate steps:

```bash
# ❌ WRONG - nested command substitution
webset_id=$(exa-ai webset-create --search '{"query":"..."}' | jq -r '.webset_id')

# ✅ CORRECT - run directly, then parse
exa-ai webset-create --search '{"query":"..."}'
# Then in a follow-up command:
webset_id=$(cat output.json | jq -r '.webset_id')
```

**Why**: Complex nested `$(...)` command substitutions can fail unpredictably in shell environments. Running commands directly and parsing separately improves reliability and makes debugging easier.

### MUST NOT: Use nested command substitutions

**Applies to**: All skills when using complex multi-step operations

Avoid nesting multiple levels of command substitution:

```bash
# ❌ WRONG - deeply nested
result=$(exa-ai search "$(cat query.txt | tr '\n' ' ')" --num-results $(cat config.json | jq -r '.count'))

# ✅ CORRECT - sequential steps
query=$(cat query.txt | tr '\n' ' ')
count=$(cat config.json | jq -r '.count')
exa-ai search "$query" --num-results $count
```

**Why**: Nested command substitutions are fragile and hard to debug when they fail. Sequential steps make each operation explicit and easier to troubleshoot.

### SHOULD: Break complex commands into sequential steps

**Applies to**: All skills when working with multi-step workflows

For readability and reliability, break complex operations into clear sequential steps:

```bash
# ❌ Less maintainable - everything in one line
exa-ai webset-create --search '{"query":"startups","count":1}' | jq -r '.webset_id' | xargs -I {} exa-ai webset-search-create {} --query "AI" --behavior override

# ✅ More maintainable - clear steps
exa-ai webset-create --search '{"query":"startups","count":1}'
webset_id=$(jq -r '.webset_id' < output.json)
exa-ai webset-search-create $webset_id --query "AI" --behavior override
```

**Why**: Sequential steps are easier to understand, debug, and modify. Each step can be verified independently.

</shared-requirements>
