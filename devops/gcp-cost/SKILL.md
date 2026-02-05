---
name: gcp-cost
description: Expert in retrieving and analyzing GCP cost data from L'Oréal's BTDP infrastructure. **Use this skill whenever the user mentions "GCP cost", "GCP costs", "cloud cost", "cloud spending", "billing", "GCP expenses", or asks about cost breakdown, cost analysis, or cost optimization for Google Cloud Platform.**
---

# GCP Cost Analysis Skill

## Workflow

To query GCP Cost, first:
1. Analyze clearly the question
2. Use `btdp-it-masterdata-retrieval` skill to ensure the correct spelling of each information provided
3. Load the schema of the table
4. Generate the query to answer user question
5. Execute the query
6. Generate a fancy output according to user request (or use default method)
 

## Key Information

### Cost Table

**Primary table for GCP costs:**
```
itg-btdppublished-gbl-ww-pd.btdp_ds_c2_0m1_gcpbilling_eu_pd.costs_distributed_per_day_v1
```

Load the schema first to ensure columns availability and descriptions.

### Default Cost Column

**ALWAYS use `cost_after_discount_euro` as the default cost column.**

This column represents the actual cost after applying all discounts and is the most accurate reflection of real spending.

### Default Cost Scope

**BY DEFAULT, EXCLUDE MARKETPLACE COSTS unless explicitly requested.**

When querying costs, use this filter:
```sql
WHERE (is_marketplace = FALSE OR is_marketplace IS NULL)
```

This excludes third-party marketplace services and focuses on direct GCP service costs.

**Only include marketplace costs when:**
- User explicitly asks for "marketplace costs"
- User asks for "total costs including marketplace"
- User requests a breakdown of marketplace vs non-marketplace costs

## Best Practices

### Filter by Date

Always include date filters to:
- Improve query performance
- Ensure relevant results
- Reduce costs

```sql
WHERE EXTRACT(YEAR FROM usage_date) = 2025
-- or
WHERE usage_date >= '2025-01-01'
-- or
WHERE invoice_month = '2025-01-01'
```

### Round Currency Values

Always round currency values for readability but at the end of the calculations:
```sql
ROUND(SUM(cost_after_discount_euro), 2) as total_cost_euro
```

### Use Appropriate Aggregations

- `SUM()` for total costs
- `COUNT(DISTINCT ...)` for counting items
- `AVG()` for average costs
- `MAX()/MIN()` for range analysis

### BigQuery Categories

If the user is asking for BigQuery Categories, you can use something like this:
```sql
     CASE
        -- BigQuery on-demand queries
        WHEN service_description = 'BigQuery' AND LOWER(sku_description) LIKE '%analysis%'
          THEN 'BigQuery No reservation Analysis'

        -- BigQuery committed slots queries
        WHEN service_description = 'BigQuery Reservation API' AND LOWER(sku_description) LIKE '%year%'
          THEN 'BigQuery Reservations committed (slots)'

        -- BigQuery uncommitted slots queries
        WHEN service_description = 'BigQuery Reservation API' AND LOWER(sku_description) NOT LIKE '%year%'
          THEN 'BigQuery Reservations uncommitted (slots flex)'

        -- BigQuery Storage
        WHEN service_description = 'BigQuery' AND LOWER(sku_description) LIKE '%storage%'
          THEN 'BigQuery Storage'

        -- BigQuery BI Engine
        WHEN service_description = 'BigQuery BI Engine'
          THEN 'BigQuery BI Engine'

        -- BigQuery other (Storage API, Streaming, Networking, etc.)
        WHEN service_description LIKE '%BigQuery%'
          THEN 'BigQuery (other)'

        -- Non BigQuery cost
        ELSE 'Non BigQuery cost'
      END AS bigquery_category,
```

## Query Execution

Execute queries using the exploration project:
```bash
bq --project_id oa-data-btdpexploration-np query --nouse_legacy_sql ...
```

## Output Formatting

### Default

By default, use a fancy formatting using tables or text generated diagram. Before sending the result and the analysis, always starts by showing the SQL query.

### Spreadsheets extraction

**ONLY create spreadsheets when the user explicitly requests data extraction, export, or a spreadsheet.**

Examples of when to create a spreadsheet:
- "Extract GCP costs to a spreadsheet"
- "Create a spreadsheet with GCP costs by IT organization"
- "Export the cost data"
- "Show me GCP costs in a spreadsheet"
- "Give me a spreadsheet of..."

**When user requests spreadsheet extraction, follow these MANDATORY rules:**

1. **Location**: Create the spreadsheet in the "Notes" folder
   - Folder ID: `16VBlrwK2FAmIfzqN1g9h-sCkQ4YuHz8x`
   - Path: My Drive / Documents / Professionnel / Sébastien / L'Oréal 2020 - Today / Doc L'Oréal / Notes

2. **Spreadsheet title**: Use a descriptive, fancy name
   - Include time period (e.g., "2025", "Q1 2025", "January 2025")
   - Include breakdown type (e.g., "by IT Organization", "by Service", "by Project")
   - Examples: "GCP Costs 2025 by IT Organization", "GCP Monthly Trends 2025", "Top GCP Services Q1 2025"

3. **Sheet name**: Give the data sheet a descriptive name (not "Sheet1")
   - Examples: "Costs by IT Org", "Monthly Breakdown", "Service Analysis", "Project Costs"
   - Should reflect the content of the data

4. **Use formulas**: ALWAYS use formulas for calculated values
   - Do NOT hardcode calculated values
   - Use formulas for: totals, subtotals, percentages, derived metrics
   - Only hardcode raw data from SQL queries that cannot be calculated dynamically
   - Examples:
     - Column D (Total Cost) = `=B2+C2` (sum of marketplace + non-marketplace)
     - Total row = `=SUM(B2:B17)` for each column
     - Percentage = `=B2/B$18` (with absolute reference to total)

5. **Currency format**: Use French format `# ### ### ##0 €` (no decimals, space as thousand separator)
   - Supports millions and billions properly
   - For values with decimals, use `# ### ### ##0.00 €`

6. **Total row**: ALWAYS add a total row at the bottom with:
   - Label "TOTAL" in column A
   - SUM formulas for all numeric columns
   - Fancy formatting: dark blue background (#1F4788), white bold text, font size 12

7. **SQL query note**: Include the SQL query as a note in the header cell (A1)

8. **Header styling**: Blue background (#4285F4), white bold text, font size 11

9. **Open spreadsheet**: IMMEDIATELY after creating and populating the spreadsheet, run the `open` command
   - Use: `open "<spreadsheet_url>"`
   - This allows the user to see the data loading in real-time

10. **Use spreadsheet-manager skill** for all formatting operations
