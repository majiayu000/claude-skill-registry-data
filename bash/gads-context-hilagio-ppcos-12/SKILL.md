---
name: gads-context
description: Pull Google Ads account data (campaigns, keywords, ads, search terms) to context/google-ads/ as CSVs and markdown summaries. Use to refresh, pull, or gather ads context.
argument-hint: "[account] [--days N]"
---

# Google Ads Context Gatherer

Pull Google Ads account data and save to `context/google-ads/` for AI context. Batch-oriented workflow that pulls all core entities in one run.

**Output Structure:**
- `context/google-ads/data/` - Raw CSV data files
- `context/google-ads/` - Markdown summary files

## Command Format

```
/gads-context [account] [--days N]
```

**Examples:**
- `/gads-context` - Use default account, 30 days
- `/gads-context acme` - Specific account by name/alias
- `/gads-context acme --days 90` - 90-day lookback

**Defaults:**
- Days: 30
- Account: From `ads-context.config.json`

## Process

### Step 1: Load Account Configuration

Check for account config in this order:

1. **ads-context.config.json** in working directory under config/ads-context.config.json:
   ```json
   {
     "googleAds": {
       "customerId": "1234567890",
       "loginCustomerId": "9876543210",
       "dateRange": 30,
       "conversionActions": ["action1", "action2", "action3"],
       "searchTermMinImpressions": 100
     }
   }
   ```

   **Config options:**
   - `searchTermMinImpressions`: Minimum impressions threshold for search terms (default: 100). Search terms with conversions are always included regardless of impressions.
### Step 2: Calculate Date Range

Calculate BETWEEN dates based on `--days` parameter (default 30):
```sql
WHERE segments.date BETWEEN '2025-12-15' AND '2026-01-13'
```

Date math rules used by `query.js`:
- End date = **yesterday** in account timezone (never today unless explicitly requested elsewhere)
- Start date = `end date - (days - 1)` to get an exact inclusive N-day range

Replace `{DATE_RANGE}` placeholder in all GAQL queries.

### Step 3: Execute Queries

Run all queries in a single batch using `scripts/run-all.js`:

```bash
node .claude/skills/gads-context/scripts/run-all.js --days={days}
```

This runs all ~20 queries from `config/ads-context.config.json` in one process:
- Core queries (campaigns, ad groups, keywords, ads, search terms, device performance)
- Negative keywords (campaign, ad group, shared, shared links)
- Conversion actions (loops per action from config, then merges)
- Optional data (assets, audiences, geo, shopping) with `--allow-empty`

Output goes to `context/google-ads/data/`. The script prints a summary table and a `__RESULTS_JSON__` line with structured results.

**GAQL file notes:**
- All `.gaql` files live in the skill's `references/` directory
- The batch runner reads them via `--query-file` — no manual query typing
- Placeholders (`{DATE_RANGE}`, `{CONVERSION_ACTION_NAME}`) are handled automatically
- The search terms query is unified across all campaign types (Search, PMax, Shopping)

**Empty results handling:** Queries with `--allow-empty` write a 0-byte CSV and output `Rows: 0` when no data exists. When generating markdown summaries for empty CSVs, output a minimal file noting the data type isn't configured for this account.

**Fallback — individual queries:** If the batch runner fails or you need to run a single query, use `query.js` directly with `--query-file` (avoids shell subshells):

```bash
node .claude/skills/gads-context/scripts/query.js \
  --customer-id={customer_id} \
  --login-customer-id={login_customer_id} \
  --query-file=.claude/skills/gads-context/references/{entity}.gaql \
  --days={days} \
  --output=context/google-ads/data/{entity}.csv
```

### Step 4: Load Business Context for Comparison

**Before generating summaries, check for business context:**

Read `context/business.md` and extract:
- `Performance Targets > Current vs Target` - Target CPA, ROAS, conversions, spend
- `Performance Targets > Hard Constraints` - Max CPA, min ROAS thresholds

**If business.md exists:**
- Include "Performance vs. Targets" section in campaigns.md
- Flag keywords exceeding max CPA in keywords.md
- Note campaigns/keywords hitting constraints

**If business.md not found:**
- Skip target comparison sections
- Add note: "Configure context/business.md for target comparison"

### Step 5: Propose Summary Files

After CSV files are created, **do NOT automatically write markdown summaries**. Instead:

1. Read the CSV data and prepare the summaries mentally
2. Present the user with a list of summaries that are ready to generate:

```markdown
### Markdown Summaries Ready

The following summaries can be generated from the pulled data:

| Summary | CSV Source | Output Path |
|---------|-----------|-------------|
| Campaigns | campaigns.csv ({n} rows) | context/google-ads/campaigns.md |
| Keywords | keywords.csv ({n} rows) | context/google-ads/keywords.md |
| ... | ... | ... |

Write all summaries? Or specify which ones you want.
```

3. **Only write the summary files after the user confirms** (e.g., "yes", "write them", "all", or specifies a subset)

**Summary files available:**

| CSV Source | Template | Output |
|-----------|----------|--------|
| `data/campaigns.csv` | `references/templates/campaigns.md` | `context/google-ads/campaigns.md` |
| `data/keywords.csv` | `references/templates/keywords.md` | `context/google-ads/keywords.md` |
| `data/ads.csv` | `references/templates/ads.md` | `context/google-ads/ads.md` |
| `data/search-terms.csv` | `references/templates/search-terms.md` | `context/google-ads/search-terms.md` |
| `data/adgroups.csv` | `references/templates/adgroups.md` | `context/google-ads/adgroups.md` |
| `data/device-performance.csv` | `references/templates/device-performance.md` | `context/google-ads/device-performance.md` |
| `data/assets.csv` + `data/assets-campaign-performance.csv` + `data/assets-adgroup-performance.csv` | `references/templates/assets.md` | `context/google-ads/assets.md` |
| `data/audiences-campaign.csv` + `data/audiences-adgroup.csv` | `references/templates/audiences.md` | `context/google-ads/audiences.md` |
| `data/geo-targeted.csv` + `data/geo-user-location.csv` | `references/templates/geo-performance.md` | `context/google-ads/geo-performance.md` |
| `data/shopping-performance.csv` + `data/shopping-products.csv` + `data/product-groups.csv` | `references/templates/shopping.md` | `context/google-ads/shopping.md` |

When writing (after user confirms), read each template file, populate with actual data from CSVs, and write to the output path. For optional data types (assets, audiences, geo, shopping), check if CSVs are empty first — the template includes instructions for both empty and populated states.

### Step 6: Present Summary

After data pull completes (summaries may or may not be written yet):

```markdown
## Google Ads Context Updated

**Account:** {account_name}
**Date range:** {days} days
**Output:** context/google-ads/

### Files Created

**Data (context/google-ads/data/):**
| File | Rows | Status |
|------|------|--------|
| campaigns.csv | {n} | OK |
| adgroups.csv | {n} | OK |
| keywords.csv | {n} | OK |
| ads.csv | {n} | OK |
| search-terms.csv | {n} | OK |
| conversions.csv | {n} | OK |
| negative-keywords-campaign.csv | {n} | OK |
| negative-keywords-adgroup.csv | {n} | OK |
| negative-keywords-shared.csv | {n} | OK |
| negative-keywords-shared-links.csv | {n} | OK |
| device-performance.csv | {n} | OK |
| assets.csv | {n} | OK / No extensions |
| assets-campaign-performance.csv | {n} | OK / No extensions |
| assets-adgroup-performance.csv | {n} | OK / No extensions |
| audiences-campaign.csv | {n} | OK / No audiences |
| audiences-adgroup.csv | {n} | OK / No audiences |
| geo-targeted.csv | {n} | OK / No geo data |
| geo-user-location.csv | {n} | OK / No geo data |
| shopping-performance.csv | {n} | OK / No Shopping |
| shopping-products.csv | {n} | OK / No Shopping |
| product-groups.csv | {n} | OK / No Shopping |

**Summaries (context/google-ads/):**
| File | Status |
|------|--------|
| campaigns.md | Ready / Written |
| adgroups.md | Ready / Written |
| keywords.md | Ready / Written |
| ads.md | Ready / Written |
| search-terms.md | Ready / Written |
| conversions.md | Ready / Written |
| device-performance.md | Ready / Written |
| assets.md | Ready / Written / No data |
| audiences.md | Ready / Written / No data |
| geo-performance.md | Ready / Written / No data |
| shopping.md | Ready / Written / No data |

> Show "Ready" if user hasn't confirmed yet, "Written" after writing.

### Quick Insights

- {insight_1}
- {insight_2}
- {insight_3}

### What's Next?

1. Review context/google-ads/ files
2. Run /ads-context [URL] to gather brand context
3. Start working on ad copy or optimization
```

## Data Formatting

When generating markdown summaries:
- **Currency:** Divide cost_micros by 1,000,000
- **Percentages:** Multiply decimals by 100 (CTR: 0.0633 → 6.33%)
- **Large numbers:** Use thousands separators

## Error Handling

**No credentials found:**
```
Error: Missing Google Ads credentials

Setup required:
1. Create config/.env with OAuth credentials
2. Include: GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_REFRESH_TOKEN

See config/.env.example for template.
```

**Account not found:**
```
Account "{input}" not found.

Available accounts:
- Account Name (alias1, alias2)
- Account Name 2 (alias3)

Specify account: /gads-context [account-name]
```

**Query fails:**
- Show API error message
- Check if credentials expired
- Suggest re-authentication

## Prerequisites

1. **config/.env** with:
   - GOOGLE_ADS_CLIENT_ID
   - GOOGLE_ADS_CLIENT_SECRET
   - GOOGLE_ADS_DEVELOPER_TOKEN
   - GOOGLE_ADS_REFRESH_TOKEN

2. **Node.js** with dependencies installed:
   ```bash
   cd .claude/skills/gads-context/scripts && npm install
   ```

3. **Account access** - Valid Google Ads account with API permissions

## Bundled Resources

- **scripts/run-all.js** - Batch runner: executes all queries in one process (preferred — single permission prompt)
- **scripts/query.js** - Execute individual GAQL queries, output CSV (supports `--query-file` and `--allow-empty`)
- **scripts/merge-csv.js** - Combine multiple CSVs with deduplication
- **references/campaigns.gaql** - Campaign performance query
- **references/adgroups.gaql** - Ad group performance query
- **references/keywords.gaql** - Keywords with quality score
- **references/ads.gaql** - RSA ads with headlines/descriptions
- **references/conversions.gaql** - Conversion actions
- **references/search-terms.gaql** - Unified search terms query (all campaign types, no impression filter)
- **references/negative-keywords-campaign.gaql** - Campaign-level negative keywords
- **references/negative-keywords-adgroup.gaql** - Ad group-level negative keywords
- **references/negative-keywords-shared.gaql** - Shared negative keyword lists
- **references/negative-keywords-shared-links.gaql** - Shared set to campaign links
- **references/device-performance.gaql** - Campaign performance by device type
- **references/assets.gaql** - Asset/extension inventory (sitelinks, callouts, snippets, images)
- **references/assets-campaign-performance.gaql** - Campaign-level asset performance
- **references/assets-adgroup-performance.gaql** - Ad group-level asset performance
- **references/audiences-campaign.gaql** - Campaign-level audience segment performance
- **references/audiences-adgroup.gaql** - Ad group-level audience segment performance
- **references/geo-targeted.gaql** - Targeted location performance (location_view)
- **references/geo-user-location.gaql** - User location performance (geographic_view)
- **references/shopping-performance.gaql** - Shopping product performance by item
- **references/shopping-products.gaql** - Product feed status and availability
- **references/product-groups.gaql** - Product group structure and performance

- **references/templates/*.md** - Markdown summary templates for Step 5 output generation
