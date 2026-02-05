---
name: dst-tables
description: Search and list Danmarks Statistik tables by subject or keyword. Use when user needs to find specific tables or browse tables within a subject area.
---

# DST Tables Skill

## Purpose

Find DST tables by subject or search term. This skill bridges the gap between browsing subjects and accessing specific data tables. Use it to discover which tables contain the data you need.

## When to Use

- User mentions a specific topic (population, employment, housing, etc.)
- User wants to see all tables in a subject area
- User searches for tables by keyword
- After browsing subjects with the dst-subjects skill
- Need to identify the table ID for data fetching

## How to Use

### List All Tables

Get all available tables (warning: large list):
```bash
python scripts/api/get_tables.py
```

### Filter by Subject

Get tables for a specific subject:
```bash
python scripts/api/get_tables.py --subject <subject_id>
```

### Search by Keyword

Find tables matching a search term:
```bash
python scripts/api/get_tables.py --search "<term>"
```

### Combined Filtering

Use both subject and keyword filters:
```bash
python scripts/api/get_tables.py --subject <id> --search "<term>"
```

### Save Results

Save to a file for later reference:
```bash
python scripts/api/get_tables.py --subject 02 --output tables.json
```

## Expected Output

The script returns a JSON array of table objects. Each table contains:

- **id**: Table identifier (e.g., "FOLK1A")
- **text**: Human-readable table name
- **description**: What the table contains (if available)
- **updated**: Last update timestamp from DST
- **firstPeriod**: First available time period
- **latestPeriod**: Most recent time period
- **active**: Whether table is currently maintained
- **variables**: Array of variable IDs (dimensions/filters)
- **unit**: Measurement unit (number, kroner, percentage, etc.)

Example output:
```json
[
  {
    "id": "FOLK1A",
    "text": "Population at the first day of the quarter",
    "unit": "Number",
    "updated": "2025-03-15T08:00:00",
    "firstPeriod": "2008K1",
    "latestPeriod": "2025K1",
    "active": true,
    "variables": ["OMRÅDE", "KØN", "ALDER", "CIVILSTAND", "Tid"]
  }
]
```

### Dataset Statistics
- **Total tables**: 5,542 (2,223 active + 3,319 inactive)
- **Active tables**: Currently maintained and updated
- **Inactive tables**: Discontinued or archived
- **Subject filtering**: Reduces results to relevant category

## Key Fields

Understanding what each field tells you:

- **id**: Table identifier - use this for tableinfo and data fetching (case-insensitive)
- **text**: Short description of the table content
- **unit**: What the numbers represent (number, DKK, percentage, index, etc.)
- **updated**: Last update timestamp - recent dates indicate fresh data
- **firstPeriod / latestPeriod**: Time coverage span
- **active**: true = currently maintained, false = discontinued/archived
- **variables**: Array of dimension IDs you can filter by (OMRÅDE, Tid, KØN, etc.)

### Reading Table Descriptions

- **text** field: Brief table title
- **unit** field: Critical for understanding values
  - "Number" = count of items
  - "Number (thousands)" = values in thousands
  - "1,000 DKK" = monetary values in thousands
  - "Percentage" = 0-100 scale
  - "Index (2015=100)" = relative to base year

### Time Period Formats
- **Annual**: "2024"
- **Quarterly**: "2024K1" (K=Kvartal/Quarter)
- **Monthly**: "2024M01"
- **Weekly**: "2024U01" (U=Uge/Week)

## Next Steps

After identifying an interesting table:

1. Note the table ID (e.g., "FOLK1A")
2. Use **dst-tableinfo** skill to get detailed metadata:
   ```bash
   python scripts/api/get_tableinfo.py --table-id FOLK1A
   ```
3. Or use **dst-data** skill to fetch the actual data:
   ```bash
   python scripts/fetch_and_store.py --table-id FOLK1A
   ```

## Examples

### Example 1: Tables in specific subject
```bash
# Population and elections (subject 1)
python scripts/api/get_tables.py --subject 1
```

### Example 2: Search across all subjects
```bash
python scripts/api/get_tables.py --search "population"
```
Note: Search is case-insensitive and searches both text and description fields

### Example 3: Combined filtering
Find age-related tables in the labour subject:
```bash
python scripts/api/get_tables.py --subject 2 --search "age"
```

### Example 4: Recently updated tables
```bash
# Tables updated in last 7 days
python scripts/api/get_tables.py --pastDays 7
```

### Example 5: Include discontinued tables
```bash
python scripts/api/get_tables.py --subject 1 --includeInactive
```
Warning: Adds 3,319 inactive tables, much slower response

### Example 6: Save to file for reference
```bash
python scripts/api/get_tables.py --subject 2 --output labour_tables.json
```

### Example 7: Find specific table pattern
```bash
# Find all FOLK* tables (population tables)
python scripts/api/get_tables.py --search "FOLK"
```

### Example 8: Multi-subject search
```bash
# Get tables from multiple subjects (if supported by script)
python scripts/api/get_tables.py --subject 1 --subject 2
```

## Tips

### Search Strategy
- **Use subject filter** when you know the category (more focused results)
- **Use keyword search** for exploratory discovery across all subjects
- **Combine filters** to narrow down large result sets
- **Note table IDs** for the next steps in your workflow

### Evaluating Tables
- **Check updated date**: Recent timestamps indicate fresh data
- **Check active status**: false means table is discontinued
- **Review time period coverage**: firstPeriod to latestPeriod shows data span
- **Note variable names**: Shows what dimensions are available for filtering
- **Check unit field**: Critical for understanding what numbers represent

### Performance Considerations
- **Response times**:
  - All tables: 390ms (~500 KB, 2,223 tables)
  - By subject: 190ms (~65 KB, varies by subject)
  - With inactive: 670ms (~1.2 MB, 5,542 tables)
- **Filtering at API level**: More efficient than client-side filtering
- **Subject filtering uses OR logic**: Multiple subjects return union of results

### API Limitations (Workarounds)
- **No text search at API**: Search implemented client-side in script
- **No ID filtering at API**: Must fetch and filter locally
- **Subject filter only**: Can filter by subject, pastDays, and includeInactive

## Common Search Terms

### English Search Terms
- Population: "population", "inhabitants", "demographic"
- Employment: "employment", "labour", "workforce", "job"
- Income: "income", "earnings", "salary", "wage"
- Housing: "housing", "dwelling", "building", "construction"
- Education: "education", "school", "university", "student"
- Health: "health", "hospital", "medical", "healthcare"
- Business: "business", "company", "enterprise", "firm"
- Prices: "price", "inflation", "cost", "consumer"
- Energy: "energy", "electricity", "power", "consumption"

### Danish Search Terms (also searchable)
- Befolkning (population)
- Arbejde (work/labour)
- Indkomst (income)
- Bolig (housing)
- Uddannelse (education)
- Sundhed (health)
- Virksomhed (business)

Note: API returns tables with descriptions in chosen language, but search works across both.

## Troubleshooting

### Too Many Results
- **Add subject filter**: Narrow to specific category
- **Use more specific search**: Add more keywords
- **Filter by update date**: Use pastDays parameter (API level)
- **Exclude inactive**: Remove discontinued tables from results

### No Results Found
- **Try broader search**: Use fewer/simpler keywords
- **Try Danish terms**: Some descriptions only match Danish keywords
- **Check subject ID**: Verify valid subject (1-9, 19)
- **Try without filters**: Start broad, then narrow down
- **Check for typos**: Verify spelling of search terms

### Invalid Subject ID
Error: API returns 400 Bad Request
- Valid subject IDs: 1-9, 19 (top-level only)
- Sub-subject IDs not supported in tables endpoint
- Use parent subject ID instead

### Understanding Results
- **Empty "description" field**: Some tables only have "text" field
- **Many variables**: Large tables can have 5+ dimensions - normal
- **Old update dates**: Check "active" field - may be discontinued
- **Overlapping tables**: Multiple tables may cover similar topics with different granularity

### Performance Issues
- **Slow with includeInactive**: 3,319 extra tables to process
- **Use specific filters**: Subject filter dramatically reduces response time
- **Cache results**: Save to file if doing multiple lookups
- **Client-side search**: Script searches locally after API fetch (no API text search)
