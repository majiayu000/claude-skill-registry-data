---
name: taxonomy-updater
description: Generate campaign taxonomy CSV updates for Google Ads campaigns. Use when identifying campaigns that need taxonomy mapping, detecting vertical mismatches in mixed-vertical accounts, or creating properly formatted taxonomy CSV files for ingestion. Triggers on requests involving campaign taxonomy, budget attribution, vertical classification, or taxonomy CSV generation.
---

# Taxonomy Updater

Generate campaign-level taxonomy entries for Google Ads accounts with mixed verticals.

## Workflow

1. **Identify campaigns needing taxonomy** - Query campaign data to find campaigns missing from taxonomy or with incorrect vertical attribution
2. **Check for vertical mixing** - Determine if account has campaigns across multiple verticals (buy, rent, sell, new_construction, etc.)
3. **Generate taxonomy CSV** - Create properly formatted CSV with all required fields

## Key Tables

```sql
-- Taxonomy reference
SELECT * FROM rdc_marketing.team_digital_marketing.taxonomy_hist;

-- Google campaign data
SELECT * FROM fivetran_martech.raw_google_campaign.campaign;
```

## Detecting Mixed-Vertical Accounts

```sql
-- Check if account has multiple verticals
SELECT 
    CASE 
        WHEN LOWER(NAME) LIKE '%_buy_%' OR LOWER(NAME) LIKE '%for sale%' THEN 'buy'
        WHEN LOWER(NAME) LIKE '%rental%' THEN 'rent'
        WHEN LOWER(NAME) LIKE '%newcon%' THEN 'new_construction'
        WHEN LOWER(NAME) LIKE '%sell%' THEN 'sell'
        ELSE 'unknown'
    END as inferred_vertical,
    COUNT(DISTINCT ID) as campaign_count
FROM fivetran_martech.raw_google_campaign.campaign
WHERE CUSTOMER_ID = <account_id>
  AND DATE >= DATEADD(month, -3, CURRENT_DATE)
GROUP BY 1;
```

If multiple verticals exist, campaign-level taxonomy entries are required.

## Getting Campaign Start Dates

```sql
SELECT 
    CAST(ID AS VARCHAR) as campaign_id,
    NAME,
    MIN(DATE) as first_active_date
FROM fivetran_martech.raw_google_campaign.campaign
WHERE CUSTOMER_ID = <account_id>
GROUP BY ID, NAME;
```

## CSV Output Format

Generate CSV **without headers**. Fields in order:

| Field | Description |
|-------|-------------|
| start_date | First active date of campaign (YYYY-MM-DD) |
| end_date | Leave empty for active campaigns |
| mapping_id | Format: `_<account_id>_<campaign_id>_` |
| account_id | Google Ads customer ID |
| campaign_id | Google Ads campaign ID |
| ad_group_id | Leave empty for campaign-level |
| channel | See allowed values |
| tactic | See allowed values |
| partner | See allowed values |
| media_type | See allowed values |
| budget_name | See allowed values |
| budget_id | See allowed values |
| target_platform | web or app |
| target_customer | b2c or b2b |
| target_audience | new, existing, or both |
| target_vertical | buy, rent, sell, new_construction, mortgage, mixed |

## Allowed Values Reference

See [references/allowed-values.md](references/allowed-values.md) for complete list of valid taxonomy field values.

## Media Type Selection

- **PMax campaigns**: Use `mixed`
- **Search/DSA campaigns**: Use `search`
- **Display campaigns**: Use `display_static` or `display_video`

## Common Budget Mappings

| budget_name | budget_id | Use for |
|-------------|-----------|--------|
| sem | 721000 | Paid search campaigns |
| rentals | 210 | Rentals vertical campaigns |
| brand_digital | 750001 | Brand awareness campaigns |
| retargeting_display | 720001 | Retargeting campaigns |