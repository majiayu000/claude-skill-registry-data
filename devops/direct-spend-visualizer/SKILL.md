---
name: direct-spend-visualizer
description: Visualize FeedMob direct spend data as ASCII line charts. Use this skill when users request to view, display, chart, or visualize direct spend metrics for one or more click URL IDs. Trigger when users ask to "show direct spend," "visualize spend data," "chart the spending," or similar requests involving FeedMob direct spend visualization.
---

# Direct Spend Visualizer

## Overview

This skill enables visualization of FeedMob direct spend data as ASCII line charts. It fetches data using the FeedMob MCP API and displays net spend and gross spend trends over time in an easy-to-read format. All spend values are reported in USD currency.

## When to Use This Skill

Use this skill when users request:
- Visualization of direct spend data for specific click URL IDs
- Line charts showing spend trends over time
- Comparison of net spend vs gross spend
- Visual representation of FeedMob campaign spending

Example user requests:
- "Show me a chart of direct spend for click_url 22271"
- "Visualize the spending for the last 30 days"
- "Display spend trends for multiple campaigns"
- "Chart the direct spend data"

## Workflow

### Step 1: Fetch Direct Spend Data

Use the FeedMob MCP tool to retrieve direct spend data:

```
mcp__feedmob__get_direct_spends
```

Required parameters:
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format
- `click_url_ids`: Array of click URL IDs (as strings)

Example:
```json
{
  "start_date": "2025-11-07",
  "end_date": "2025-11-14",
  "click_url_ids": ["22271", "22272"]
}
```

### Step 2: Save the API Response

Save the JSON response from the API to a temporary file. This allows the visualization script to process the data.

Example:
```python
import json

# API response data
api_response = {
  "status": 200,
  "data": [
    {
      "feedmob_click_url_id": 22271,
      "campaign_name": "Campaign_Name",
      "date": "2025-11-07",
      "feedmob_net_spend": 119.92,
      "feedmob_gross_spend": 78.00
    }
    # ... more records
  ]
}

# Write to temp file
with open('/tmp/direct_spend_data.json', 'w') as f:
    json.dump(api_response, f)
```

### Step 3: Visualize the Data

Execute the visualization script to generate ASCII line charts:

```bash
python scripts/visualize_direct_spend.py /tmp/direct_spend_data.json
```

The script can also read from stdin:
```bash
echo '{"data": [...]}' | python scripts/visualize_direct_spend.py
```

### Step 4: Present the Results

The script outputs:
1. **ASCII line chart** - Visual representation of spend trends with Y-axis values in USD
2. **Legend** - Explains chart symbols (N = Net Spend, G = Gross Spend)
3. **Data table** - Detailed daily breakdown with totals, all values formatted in USD

Display this output to the user directly.

## Script Reference

### visualize_direct_spend.py

Located in `scripts/visualize_direct_spend.py`, this script:

**Input:** JSON data from `mcp__feedmob__get_direct_spends`

**Output:** ASCII line charts with:
- Scaled line chart showing net and gross spend trends
- Y-axis with spend values in USD (formatted with $ symbol)
- X-axis with date labels
- Detailed data table with totals (all values in USD)
- Summary statistics

**Features:**
- Handles multiple click URL IDs (creates separate charts)
- Automatically scales to data range
- Shows both net and gross spend on same chart
- Provides detailed numeric breakdown

**Usage:**
```bash
# From file
python scripts/visualize_direct_spend.py data.json

# From stdin
cat data.json | python scripts/visualize_direct_spend.py
```

## Example Complete Workflow

User request: "Show me direct spend for click_url 22271 for the last 7 days"

1. Calculate date range (today minus 7 days to today)
2. Call `mcp__feedmob__get_direct_spends` with:
   - start_date: "2025-11-07"
   - end_date: "2025-11-14"
   - click_url_ids: ["22271"]
3. Save response to `/tmp/direct_spend.json`
4. Execute: `python scripts/visualize_direct_spend.py /tmp/direct_spend.json`
5. Display the resulting chart and table to the user

## Tips

- For large date ranges, the chart may become crowded. Consider breaking into smaller periods.
- The script supports multiple click URL IDs and will create separate charts for each.
- If no data is returned from the API, inform the user that no spend data exists for the specified parameters.
- Date format must be YYYY-MM-DD for both the API and the script.
- All spend values from FeedMob are in USD currency and will be displayed with the $ symbol.
