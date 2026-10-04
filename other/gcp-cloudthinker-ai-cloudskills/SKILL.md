---
name: gcp
description: |
  Use when working with Gcp — cost anti-hallucination rules, MANDATORY parallel
  execution patterns (30x speedup), monitoring aligners, reusable
  billing/pricing scripts, VAT/tax handling, and filtering/pagination.
connection_type: gcp
preload: false
---

# GCP CLI Skill

Execute GCP CLI commands with proper credential injection.

## CRITICAL: Billing Data Interpretation Rules (Anti-Hallucination)

**These rules are MANDATORY when analyzing GCP billing data. Violating them produces wildly incorrect cost reports.**

### Rule 1: NET COST is the Only Real Cost

The `cost` column in billing exports is **NOT** your actual bill. It shows usage priced at contract/on-demand rates **before credits are applied**. Credits (promotional, SUDs, CUDs, free tier) are stored separately in the `credits` array with **negative** amounts.

```
-- Pre-tax net cost (filter cost_type = 'regular'):
NET COST = SUM(cost WHERE cost_type='regular') + SUM(credits.amount)

-- Tax-inclusive net cost (include all cost_types):
NET COST WITH TAX = SUM(cost) + SUM(credits.amount)
```

**NEVER report `SUM(cost)` alone as the cost.** Always compute net cost. In actual SQL, always use `CAST(... AS NUMERIC)` — see Rule 8.

### Rule 2: ALWAYS Filter by project.id

The billing export table is at the **billing account level** and contains costs for **ALL projects** under that billing account. If you query without filtering by `project.id`, you aggregate costs across 10+ unrelated projects.

```sql
-- WRONG: Aggregates ALL projects in the billing account
SELECT service.description, SUM(cost) FROM `{BILLING_TABLE}` GROUP BY 1

-- CORRECT: Scoped to the target project with net cost
SELECT service.description,
  SUM(CAST(cost AS NUMERIC))
    + SUM(IFNULL((SELECT SUM(CAST(c.amount AS NUMERIC)) FROM UNNEST(credits) c), 0)) AS net_cost
FROM `{BILLING_TABLE}`
WHERE project.id = '{PROJECT_ID}'
GROUP BY 1
```

### Rule 3: NEVER Aggregate SUM(cost) Alongside LEFT JOIN UNNEST(credits)

If a row has 3 credit entries, `LEFT JOIN UNNEST(credits)` duplicates that row 3 times, **tripling** the `SUM(cost)`. This is the most common cause of inflated cost reports.

```sql
-- WRONG: Inflates cost by N times (N = number of credits per row)
SELECT SUM(cost), SUM(credits.amount)
FROM `{BILLING_TABLE}` LEFT JOIN UNNEST(credits) AS credits

-- CORRECT: Subquery aggregates credits without duplicating cost rows
SELECT
  SUM(CAST(cost AS NUMERIC)) AS gross_cost,
  SUM(IFNULL((SELECT SUM(CAST(c.amount AS NUMERIC)) FROM UNNEST(credits) c), 0)) AS total_credits
FROM `{BILLING_TABLE}`
WHERE project.id = '{PROJECT_ID}'
```

**Note:** `LEFT JOIN UNNEST(credits)` is safe when you are ONLY aggregating `credits.amount` and NOT also aggregating `cost` — e.g., when filtering by credit type. The danger is combining it with `SUM(cost)` in the same query.

### Rule 4: Sanity-Check Costs Against Known GCP Pricing

Before reporting any cost figure, verify it's physically possible.

**Step 1: Check the currency.** GCP billing accounts can use ANY currency (USD, VND, EUR, BRL, JPY, etc.). Run `gcp_billing_currency` or check the `currency` column BEFORE interpreting any numbers. A value of `5,000,000` in VND (~$200 USD) is very different from `5,000,000` in USD.

**Step 2: Verify magnitude against known pricing (in the account's currency):**

| Machine Type  | Region          | Monthly On-Demand Price (USD) |
| ------------- | --------------- | ----------------------------- |
| e2-micro      | asia-southeast1 | ~$8/mo                        |
| e2-small      | asia-southeast1 | ~$15/mo                       |
| e2-medium     | asia-southeast1 | ~$30/mo                       |
| e2-standard-2 | asia-southeast1 | ~$60/mo                       |
| n1-standard-2 | asia-southeast1 | ~$60/mo (before SUD)          |
| n2-standard-2 | asia-southeast1 | ~$70/mo                       |

**Red flags that indicate a query error or currency mismatch:**
- A single VM shows >$1,000 USD/week (e2-standard-2 costs ~$60/month)
- Total project cost exceeds $100,000 USD/week for a standard workload
- AI/API costs look 1,000x-25,000x higher than expected (likely VND/JPY reported as USD)

**If numbers seem unreasonably high, STOP and verify the currency before reporting.** Do NOT present cost numbers to users without confirming the currency unit.

### Rule 5: Detect Credit Programs Before Alerting

If `net_cost` is consistently $0 (or near-zero) while `gross_cost` is large, the account is on a **promotional credit program** (free trial, startup credits, enterprise credits). This is normal — not an anomaly.

**MANDATORY first query** before any billing analysis:

```sql
-- Step 0: Detect credit program status
SELECT
  c.type AS credit_type,
  c.full_name AS credit_name,
  COUNT(*) AS line_items,
  SUM(CAST(c.amount AS NUMERIC)) AS total_credit_amount
FROM `{BILLING_TABLE}`, UNNEST(credits) AS c
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND project.id = '{PROJECT_ID}'
GROUP BY 1, 2
ORDER BY total_credit_amount ASC
```

**Interpretation:**

- `PROMOTION` credits with large amounts → account is on promotional/trial program
- `SUSTAINED_USAGE_DISCOUNT` → automatic discounts on N1/N2/N2D/C2/M1/M2 instances
- `COMMITTED_USAGE_DISCOUNT` → organization has CUD commitments
- `FREE_TIER` → usage within free tier limits

**If PROMOTION credits fully offset costs:** Report that the account is on a credit program. Do NOT generate alarmist alerts about "projected costs when credits expire" unless the user specifically asks for that analysis.

### Rule 6: Detect Anomalies on NET Cost, Not Gross Cost

Gross cost fluctuates when credits are added/removed/adjusted. Only net cost reflects actual spending changes.

```sql
-- Pseudocode (not valid SQL — see Anomaly Detection query in BigQuery section for working version)

-- WRONG: Anomaly on gross cost → false positive from credit changes
HAVING SUM(cost) > threshold

-- CORRECT: Anomaly on net cost → real spending change
HAVING (SUM(cost) + SUM(credits_subquery)) > threshold
```

### Rule 7: Verify Services Actually Exist Before Alerting

If billing data shows charges for a service (e.g., App Engine, Load Balancer) but `gcloud` commands show that service doesn't exist in the project, the charges are likely from **another project in the same billing account** that leaked into your unfiltered query. Go back to Rule 2 and add `WHERE project.id = ...`.

### Rule 8: Use NUMERIC Casting for Financial Precision

The `cost` and `credits.amount` fields are Float type. Summing millions of rows accumulates floating-point errors. Always cast:

```sql
SUM(CAST(cost AS NUMERIC)) -- not SUM(cost)
```

### Rule 9: Understand invoice.month vs usage_start_time

- `invoice.month` (YYYYMM): The invoice this line item belongs to. **Use for invoice reconciliation.**
- `usage_start_time`: When usage actually occurred. **Use for trend analysis.**
- These can differ: late-reported usage from month N may appear on month N+1's invoice.
- See the **Invoice Reconciliation** query in the BigQuery Billing Export Patterns section for a working example.

### Rule 10: Data Has 24-48 Hour Delay

Billing export data takes up to 24-48 hours to fully propagate. Do NOT alert on "missing data" for the current day or yesterday.

### Rule 11: Always Detect and Report Currency

GCP billing accounts can be configured in **any currency** (USD, EUR, VND, BRL, JPY, GBP, etc.). The `currency` column in the billing export table identifies the billing currency. **NEVER assume USD.**

**MANDATORY**: Run `gcp_billing_currency` (or check `SELECT DISTINCT currency FROM TABLE`) as part of the first billing query. Include the currency in every cost report.

```sql
-- Check billing currency
SELECT DISTINCT currency FROM `{BILLING_TABLE}` WHERE project.id = '{PROJECT_ID}'
```

**Reporting rules:**
- **ALWAYS include the currency code** when presenting costs (e.g., "5,368,844 VND" not "$5,368,844")
- **NEVER use `$` symbol** without confirming the currency is USD
- If the user needs USD conversion, state the approximate exchange rate used and note it may not be current
- **Do NOT hardcode exchange rates in SQL queries.** Report costs in their native currency and provide approximate USD equivalent separately if needed

**Common non-USD currencies and approximate rates (for sanity-checking only):**
- VND: ~25,000 VND = 1 USD (costs appear 25,000x larger than USD equivalent)
- JPY: ~150 JPY = 1 USD (costs appear 150x larger)
- EUR: ~0.92 EUR = 1 USD
- BRL: ~5 BRL = 1 USD

### Mandatory Pre-Analysis Checklist

**Before writing ANY billing query, verify ALL of the following:**

- [ ] **Currency has been detected** via `gcp_billing_currency` or equivalent query
- [ ] Query includes `WHERE project.id = '{PROJECT_ID}'` filter
- [ ] Net cost is computed as `SUM(CAST(cost AS NUMERIC)) + SUM(IFNULL((SELECT SUM(CAST(c.amount AS NUMERIC)) FROM UNNEST(credits) c), 0))`
- [ ] NO `LEFT JOIN UNNEST(credits)` used alongside `SUM(cost)`
- [ ] Cost fields use `CAST(... AS NUMERIC)` for precision
- [ ] Credit program detection query has been run FIRST
- [ ] Any per-resource cost is sanity-checked against known GCP pricing **in the detected currency**
- [ ] Anomaly detection uses net cost, not gross cost
- [ ] `cost_type` is considered (regular vs tax vs adjustment vs rounding_error)
- [ ] **All cost figures in the report include the currency unit**

## CLI Tips

### Parallel Execution Requirement (CRITICAL)

**ALL independent operations MUST run in parallel using background jobs (&) and wait**

ENFORCEMENT RULES:

- **FORBIDDEN**: Sequential loops like `for item in $items; do cmd $item; done` (causes O(n) runtime)
- **MANDATORY**: Every independent operation spawns a background job: `{ cmd1 } & { cmd2 } & { cmd3 } & wait`
- **DETECTION**: If your script processes N resources/metrics/regions and N > 1, the script MUST contain at least N background jobs
- **TIME IMPACT**: Sequential execution with 30 instances x 2 seconds per call = 60 seconds. Parallel = 2 seconds (30x faster)
- **VALIDATION CHECKLIST** (agent must mentally verify before output):
  - Count independent operations: \_\_\_
  - Count background jobs (&): \_\_\_
  - These numbers MUST match, or script will be REJECTED
  - Do all operations depend on each other? (Only valid exception to parallel requirement)

PARALLEL PATTERN (CORRECT):

```bash
for instance in $instances; do
  operation "$instance" &  # ← Spawn as background job
done
wait  # ← Wait for all to complete
```

SEQUENTIAL PATTERN (FORBIDDEN - ONLY if operations have data dependencies):

```bash
result=$(operation1)
operation2 "$result"  # ← Only valid if operation2 requires operation1's output
```

### Agent Output Rules

- The script output is for the agent itself to read and process, NOT for human reading
- Do NOT add visual formatting, icons, or decorative elements (no emojis, borders, or separators)
- NEVER USE echo statements for section breaks, headers, or formatting (no "--------", "====", or similar)
- Focus on raw data extraction and minimal, parseable output
- Use plain text format with consistent delimiters for easy parsing
- Prioritize machine-readability over human presentation
- NEVER run commands or scripts that print, log, or expose environment variables, credentials, or GCP keys (e.g., GOOGLE_APPLICATION_CREDENTIALS)

### Execution Guidelines

- **PARALLEL EXECUTION IS MANDATORY**: Always use background jobs (`&`) and `wait` for independent operations
  - Process multiple instances/resources in parallel: `{ ... } &` with `wait` at the end
  - Fetch multiple metrics for the same resource in parallel, then `wait` before processing
  - Sequential loops are FORBIDDEN unless operations have strict dependencies
  - Parallel execution reduces runtime from O(n \* time_per_operation) to O(max_operation_time) - use it always
- GCP region and project ID are already preconfigured in the environment - no need to set them manually
- Always consolidate related steps into single CLI Bash script if possible
- Only use read-only commands (e.g., list, describe, get) - never modify resources
- Always format CLI output as plain text (never JSON or table) so that it's easy for the agent to parse. For GCP use --format=text or --format="value(...)" as appropriate. Also use filtering/query flags to limit output to what is needed. These practices are crucial for efficiency and accuracy.
- **NON-INTERACTIVE MODE**: Use `--quiet` (`-q`) flag or `export CLOUDSDK_CORE_DISABLE_PROMPTS=1` to disable prompts in scripts

### Filtering Guidance

**FILTERING ORDER MATTERS - Understand server-side vs client-side**

1. **`--filter` (VARIES BY COMMAND)** - Can be server-side OR client-side
   - Some commands send filter to API (server-side) → reduces network payload
   - Other commands filter locally (client-side) → full data still transferred
   - Use `--log-http` to verify: if filter appears in API request, it's server-side
   - Server-side is MORE efficient for large datasets

2. **`--format` (ALWAYS CLIENT-SIDE)** - Formatting after data retrieval
   - Use `--format="value(...)"` for clean, parseable output
   - Use projections to select specific fields
   - Always applied AFTER --filter

**PERFORMANCE IMPACT**:

- Server-side --filter: API returns only matching records
- Client-side --filter: API returns ALL records, filtered locally
- Use `--log-http` to check which mode your command uses

**EXAMPLES**:

```bash
# Efficient: --filter with --format for minimal output
gcloud compute instances list --filter="status=RUNNING" \
    --format="value(name,zone.scope(zones),machineType.scope(machineTypes))"

# Verify if filter is server-side (look for filter in HTTP request)
gcloud compute instances list --filter="status=RUNNING" --log-http 2>&1 | grep -i filter

# Multiple filter conditions
gcloud compute instances list \
    --filter="status=RUNNING AND machineType~n1-standard" \
    --format="value(name,zone)"
```

**COMMON FILTER OPERATORS**:

- `=` exact match, `!=` not equal, `~` regex match, `!~` regex not match
- `:` substring match (HAS operator)
- `>`, `>=`, `<`, `<=` for comparisons
- `AND`, `OR`, `NOT` for boolean logic

### Pagination Guidelines

**PAGINATION FOR LARGE DATASETS - Prevent timeouts and memory issues**

**KEY PARAMETERS**:

- `--limit=N`: Maximum total items to return (stops early)
- `--page-size=N`: Items per API call (internal pagination, still returns all unless --limit set)
- `--sort-by=FIELD`: Sort results (prefix with ~ for descending)

**ORDER OF OPERATIONS** (gcloud applies in this order):

1. `--flatten` → 2. `--sort-by` → 3. `--filter` → 4. `--limit`

**EXAMPLES**:

```bash
# Get first 10 instances only
gcloud compute instances list --limit=10 --format="value(name,zone)"

# Paginate with smaller chunks (memory efficiency)
gcloud compute instances list --page-size=50 --limit=200 \
    --format="value(name,zone)"

# Sort by creation time, newest first
gcloud compute instances list --sort-by=~creationTimestamp --limit=5 \
    --format="value(name,creationTimestamp)"
```

**BEST PRACTICE**: Combine --filter + --limit to minimize data transfer:

```bash
# Filter server-side, limit client-side
gcloud compute instances list --filter="status=RUNNING" --limit=100 \
    --format="value(name,zone)"
```

### Format Projections

**USEFUL PROJECTION FUNCTIONS - Reduce post-processing with built-in transforms**

**EXTRACTION FUNCTIONS**:

- `.scope(segment)` - Extract last URL segment (e.g., zone name from full URL)
- `.basename()` - Get filename from path
- `.segment(n)` - Get nth segment from URL

**DATE/TIME FUNCTIONS**:

- `.date(format)` - Format timestamp (e.g., `.date('%Y-%m-%d')`)
- `.date(tz=LOCAL)` - Convert to local timezone

**STRING FUNCTIONS**:

- `.yesno(yes, no)` - Convert boolean to custom strings
- `.list()` - Format as comma-separated list

**EXAMPLES**:

```bash
# Extract zone name from full URL
gcloud compute instances list \
    --format="value(name,zone.scope(zones),machineType.scope(machineTypes))"
# Output: my-vm  us-central1-a  n1-standard-1

# Format creation date
gcloud compute instances list \
    --format="table(name,creationTimestamp.date('%Y-%m-%d'),status)"

# Boolean formatting
gcloud compute instances list \
    --format="value(name,scheduling.preemptible.yesno('preemptible','on-demand'))"

# Get single value (no headers)
gcloud config get-value project --format="value(.)"
```

**REFERENCE**: Run `gcloud topic projections` for full documentation

### Efficient CLI Script Example

**ANTI-PATTERN EXAMPLE (SEQUENTIAL - SLOW - UNACCEPTABLE)**

```bash
#!/bin/bash
# RUNTIME: ~60 seconds for 30 instances (2 sec per call x 30)
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%SZ")

echo "GCP VM Metrics Summary ($START_TIME to $END_TIME)"

PROJECT_ID=$(gcloud config get-value project)
echo "Project: $PROJECT_ID"

# Get zones and instances
gcloud compute zones list --format="value(name)" | while read zone; do
    instances=$(gcloud compute instances list --zones="$zone" --format="value(name)" --project="$PROJECT_ID")
    if [ -n "$instances" ]; then
        echo "Zone: $zone"

        # This SEQUENTIAL loop is FORBIDDEN
        echo "$instances" | while read instance_name; do
            echo "  Instance: $instance_name"

            # Sequential metric fetches - UNACCEPTABLE
            gcloud monitoring time-series list \
                --filter="resource.labels.project_id='$PROJECT_ID' AND resource.labels.zone='$zone' AND resource.labels.instance_id='$instance_name' AND metric.type='compute.googleapis.com/instance/cpu/utilization'" \
                --interval.start-time="$START_TIME" \
                --interval.end-time="$END_TIME" \
                --aggregation.alignment-period=3600s \
                --aggregation.per-series-aligner="ALIGN_MEAN" \
                --format="value(points[].value.doubleValue)" \
                --project="$PROJECT_ID"

            gcloud monitoring time-series list \
                --filter="resource.labels.project_id='$PROJECT_ID' AND resource.labels.zone='$zone' AND resource.labels.instance_id='$instance_name' AND metric.type='compute.googleapis.com/instance/network/received_bytes_count'" \
                --interval.start-time="$START_TIME" \
                --interval.end-time="$END_TIME" \
                --aggregation.alignment-period=3600s \
                --aggregation.per-series-aligner="ALIGN_RATE" \
                --format="value(points[].value.doubleValue)" \
                --project="$PROJECT_ID"
        done
    fi
done
# TOTAL TIME: ~60 seconds (UNACCEPTABLE for 30+ instances)
```

**CORRECT EXAMPLE (PARALLEL - FAST - REQUIRED)**

```bash
#!/bin/bash
# RUNTIME: ~2 seconds for 30 instances (all run simultaneously)
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%SZ")
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

# Fetch a single metric (called in parallel)
get_metric() {
    local instance=$1 zone=$2 metric=$3 aligner=$4
    gcloud monitoring time-series list \
        --filter="resource.labels.instance_id='$instance' AND metric.type='$metric'" \
        --interval.start-time="$START_TIME" --interval.end-time="$END_TIME" \
        --aggregation.alignment-period=3600s \
        --aggregation.per-series-aligner="$aligner" \
        --format="value(points[].value.doubleValue)" \
        --project="$PROJECT_ID" \
        | awk -v i="$instance" -v m="$metric" '{sum+=$1; count++} END {if(count>0) printf "%s\t%s\t%.2f\n", i, m, sum/count}'
}

# Process one instance: fetch multiple metrics in parallel
process_instance() {
    local instance=$1 zone=$2
    get_metric "$instance" "$zone" "compute.googleapis.com/instance/cpu/utilization" "ALIGN_MEAN" &
    get_metric "$instance" "$zone" "compute.googleapis.com/instance/network/received_bytes_count" "ALIGN_RATE" &
    wait  # Wait for all metrics of this instance
}

# Process ALL instances in parallel
instances=$(gcloud compute instances list --format="value(name,zone.scope(zones))" --project="$PROJECT_ID")
echo "$instances" | while read instance zone; do
    process_instance "$instance" "$zone" &
done
wait  # Wait for all instances to complete
```

**PERFORMANCE COMPARISON TABLE**
| Pattern | Instances | Time/Call | Total Time | Speed |
|---------|-----------|-----------|-----------|-------|
| Sequential (❌) | 30 | 2 sec | ~60 sec | Baseline |
| Parallel (✅) | 30 | 2 sec | ~2 sec | **30x faster** |
| Sequential (❌) | 100 | 2 sec | ~200 sec | Baseline |
| Parallel (✅) | 100 | 2 sec | ~2 sec | **100x faster** |

**KEY DIFFERENCES IN THIS SCRIPT (What Makes It Parallel)**
- In the main loop: `process_instance "$instance" "$zone" &` - spawns each instance as background job
- After the loop: `wait` - waits for all instances to complete
- Inside `process_instance`: metrics are fetched in parallel (with `&` and inner `wait`)
- Uses `--format="value(name,zone.scope(zones))"` for efficient extraction

**VALIDATION CHECKLIST FOR AGENT**
Before outputting ANY script, check every item:

- [ ] Count number of independent resources/metrics/zones to process: \_\_\_
- [ ] Count number of `&` background job spawns in script: \_\_\_
- [ ] If these counts don't match, the script is WRONG - REJECT it and rewrite
- [ ] Verify each background job block is followed by a `wait` statement
- [ ] Check that NO sequential loops exist for independent operations
- [ ] Confirm expected runtime is ~2-10 seconds (not ~30+ seconds)
- [ ] Verify GCP monitoring aligners are correct (ALIGN_MEAN, ALIGN_MAX, ALIGN_RATE, etc.)
- [ ] Confirm script uses --format=text or --format="value(...)" with proper filtering

### Common GCP CLI Patterns

- List all projects: `gcloud projects list --format="value(projectId,name,lifecycleState)"`
- List compute instances: `gcloud compute instances list --format="value(name,zone,machineType.scope(machineTypes),status)"`
- Get instance details: `gcloud compute instances describe myInstance --zone=us-central1-a --format="value(name,machineType,status,scheduling.preemptible)"`
- List Cloud Storage buckets: `gcloud storage buckets list --format="value(name,location,storageClass)"`
- List Cloud SQL instances: `gcloud sql instances list --format="value(name,databaseVersion,region,tier,state)"`
- Get current project (preconfigured): `gcloud config get-value project --format="value(.)"`
- List App Engine services: `gcloud app services list --format="value(id,split.allocations.keys())"`
- List Cloud Functions: `gcloud functions list --format="value(name,status,trigger.eventTrigger.eventType)"`
- Get billing info: `gcloud billing accounts list --format="value(name,displayName,open)"`
- List Kubernetes clusters: `gcloud container clusters list --format="value(name,location,status,currentMasterVersion)"`

### GCP Service Naming Patterns

- Compute Engine: e2-micro, n1-standard-1, c2-standard-4, n2-highmem-2
- Cloud Storage: STANDARD, NEARLINE, COLDLINE, ARCHIVE
- Cloud SQL: db-f1-micro, db-n1-standard-1, db-n1-highmem-2
- App Engine: F1, F2, F4, F4_1G (for automatic scaling)
- Cloud Functions: Various memory sizes (128MB, 256MB, 512MB, 1GB, 2GB, 4GB, 8GB)

### Billing CLI Commands

**BILLING ACCOUNT & BUDGET MANAGEMENT - gcloud billing commands**

**LIST BILLING ACCOUNTS** (accounts you have access to):

```bash
# List all billing accounts with key fields
gcloud billing accounts list --format="value(name,displayName,open)"

# Get billing account ID only (for scripting)
gcloud billing accounts list --format="value(name)" --filter="open=true"
```

**DESCRIBE BILLING ACCOUNT**:

```bash
# Get account details (check if sub-account)
gcloud billing accounts describe BILLING_ACCOUNT_ID \
    --format="value(displayName,masterBillingAccount,open)"
# If masterBillingAccount is set, this is a reseller sub-account
```

**LIST PROJECTS UNDER BILLING ACCOUNT**:

```bash
# List all projects linked to a billing account
gcloud billing projects list --billing-account=BILLING_ACCOUNT_ID \
    --format="value(projectId,billingEnabled)"

# Filter to only enabled projects
gcloud billing projects list --billing-account=BILLING_ACCOUNT_ID \
    --filter="billingEnabled=true" --format="value(projectId)"
```

**CHECK PROJECT BILLING STATUS**:

```bash
# Check if specific project has billing enabled
gcloud billing projects describe PROJECT_ID --format="value(billingEnabled)"
# Returns: True or False

# Get billing account linked to project
gcloud billing projects describe PROJECT_ID \
    --format="value(billingAccountName)"
```

**BUDGET MANAGEMENT**:

```bash
# List all budgets for a billing account
gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID \
    --format="value(displayName,amount.specifiedAmount.units,amount.specifiedAmount.currencyCode)"

# Describe specific budget details
gcloud billing budgets describe BUDGET_ID --billing-account=BILLING_ACCOUNT_ID \
    --format="value(displayName,amount,budgetFilter,thresholdRules)"
```

**PARALLEL PATTERN FOR MULTI-ACCOUNT ANALYSIS**:

```bash
# Fetch billing info for multiple accounts in parallel
accounts=$(gcloud billing accounts list --format="value(name)" --filter="open=true")
for account in $accounts; do
    {
        projects=$(gcloud billing projects list --billing-account="$account" \
            --format="value(projectId)" --filter="billingEnabled=true")
        echo "$account: $(echo "$projects" | wc -l) projects"
    } &
done
wait
```

### VAT/Tax Handling

**CRITICAL: VAT/TAX AWARENESS - Why your costs may differ from Console**

**IMPORTANT**: GCP Pricing API and BigQuery billing exports return **TAX-EXCLUSIVE** (pre-tax) prices.
The GCP Console dashboard shows **TOTAL costs INCLUDING taxes** (VAT, GST, sales tax, etc.).

**THIS CAUSES DISCREPANCIES** between API results and what customers see in their Console!

**HOW GCP HANDLES TAXES**:

1. **Pricing API**: Returns base list prices WITHOUT tax
2. **BigQuery Billing Export**: `cost` column is PRE-TAX; taxes are separate rows with `cost_type = "tax"`
3. **Console Dashboard**: Shows aggregated totals WITH taxes included
4. **Invoices**: Show taxes as separate line items by project

**TAX RATES BY REGION** (examples - varies by location and changes over time):

- EU countries: 19-27% VAT (varies by country)
- UK: 20% VAT
- Australia: 10% GST
- India: 18% GST
- Canada: 5-15% (varies by province)
- Bahrain: 10% VAT (since Feb 2022)
- US: State sales tax varies (0-10%+)

**TO GET TAX-INCLUSIVE TOTALS FROM BIGQUERY**:

```sql
-- Get total cost INCLUDING taxes (matches Console dashboard)
-- Note: project.id filter required per Rule 2
SELECT
  invoice.month AS invoice_month,
  SUM(CASE WHEN cost_type != 'tax' THEN CAST(cost AS NUMERIC) ELSE 0 END) AS pre_tax_cost,
  SUM(CASE WHEN cost_type = 'tax' THEN CAST(cost AS NUMERIC) ELSE 0 END) AS tax_amount,
  SUM(CAST(cost AS NUMERIC))
    + SUM(IFNULL((SELECT SUM(CAST(c.amount AS NUMERIC)) FROM UNNEST(credits) c), 0)) AS net_cost_with_tax
FROM `{BILLING_TABLE}`
WHERE project.id = '{PROJECT_ID}'
  AND invoice.month = FORMAT_DATE('%Y%m', CURRENT_DATE())
GROUP BY 1

-- Get tax breakdown by project (intentionally no project.id filter: multi-project breakdown)
SELECT
  project.id AS project_id,
  SUM(CASE WHEN cost_type != 'tax' THEN CAST(cost AS NUMERIC) ELSE 0 END) AS usage_cost,
  SUM(CASE WHEN cost_type = 'tax' THEN CAST(cost AS NUMERIC) ELSE 0 END) AS tax_cost,
  SUM(CAST(cost AS NUMERIC))
    + SUM(IFNULL((SELECT SUM(CAST(c.amount AS NUMERIC)) FROM UNNEST(credits) c), 0)) AS net_total_with_tax
FROM `{BILLING_TABLE}`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY net_total_with_tax DESC

-- Get tax types (VAT, GST, sales tax, etc.)
SELECT
  sku.description AS tax_type,
  SUM(CAST(cost AS NUMERIC)) AS tax_amount
FROM `{BILLING_TABLE}`
WHERE project.id = '{PROJECT_ID}'
  AND cost_type = 'tax'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 2 DESC
```

**WHEN REPORTING COSTS TO USERS**:

- ALWAYS clarify whether costs are pre-tax or post-tax
- If comparing to Console, include taxes: "Total cost (including VAT): $X"
- For budgeting, use tax-inclusive figures to match what they'll be invoiced
- Include tax breakdown when relevant: "Usage: $X + VAT: $Y = Total: $Z"

**COST COMPARISON FORMULA** (pseudocode — use CAST/UNNEST subquery pattern in actual SQL):

```
Console Total = Usage Cost + Credits + Taxes
              = SUM(cost WHERE cost_type='regular')
              + SUM(credits.amount)    -- credits are negative
              + SUM(cost WHERE cost_type='tax')
              = SUM(cost) + SUM(credits.amount)   -- simplified: all cost_types
```

### Pricing Script (`get_pricing_gcp.sh`)

**DO NOT read or modify the script file.** Only source and call the function.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/gcp/gcp/scripts/get_pricing_gcp.sh
```

**FUNCTION**: `get_gcp_cost RESOURCE REGION`

Auto-detects the GCP service from the resource name prefix and returns on-demand pricing in TOON format.

**NOTE**: All prices are TAX-EXCLUSIVE. See VAT/Tax Handling for tax-inclusive calculations.

**Supported resource prefixes:**

| Prefix | Service | Example |
|--------|---------|---------|
| `e2-`, `n1-`, `n2-`, `c2-`, `c3-` | Compute Engine | `e2-standard-2` |
| `cloudsql-`, `db-` | Cloud SQL | `cloudsql-db-n1-standard-2` |
| `gcs-` | Cloud Storage | `gcs-standard` |
| `functions-` | Cloud Functions | `functions-256mb` |
| `cloudrun-` | Cloud Run | `cloudrun-1cpu-512mb` |
| `redis-` | Memorystore | `redis-basic-1gb` |
| `bq-` | BigQuery | `bq-ondemand` |
| `pd-` | Persistent Disk | `pd-ssd-100gb` |
| `lb-` | Load Balancer | `lb-forwarding-rule` |
| `cloudnat-` | Cloud NAT | `cloudnat-standard` |
| `gke-` | GKE | `gke-standard` |

**Compute Engine detail**: GCP bills vCPU and RAM separately. The script has a built-in machine spec table and queries both Core and Ram SKUs, combining them into a total hourly/monthly estimate.

**Examples:**

```bash
source ./_skills/connections/gcp/gcp/scripts/get_pricing_gcp.sh
get_gcp_cost e2-standard-2 asia-southeast1
get_gcp_cost n2-standard-4 us-central1
get_gcp_cost gcs-standard us-central1
get_gcp_cost cloudsql-db-n1-standard-2 asia-southeast1
```

### Monitoring and Metrics

**COMMON METRICS**:

- CPU utilization: compute.googleapis.com/instance/cpu/utilization
- Network traffic: compute.googleapis.com/instance/network/received_bytes_count, sent_bytes_count
- Disk I/O: compute.googleapis.com/instance/disk/read_bytes_count, write_bytes_count
- Memory usage (with monitoring agent): agent.googleapis.com/memory/percent_used

**ALIGNERS** (per-series-aligner):

- ALIGN_MEAN: Average value over alignment period (use for utilization metrics)
- ALIGN_MAX: Maximum value (use for peak detection)
- ALIGN_MIN: Minimum value
- ALIGN_RATE: Rate of change (use for counter metrics like bytes_count)
- ALIGN_SUM: Sum of values (use for uptime, request counts)

**CRITICAL: alignment-period MUST be >= 60 seconds**
If you specify a per-series-aligner other than ALIGN_NONE, alignment-period is REQUIRED and must be at least 60 seconds.

**CROSS-SERIES REDUCERS** (aggregate across multiple resources):

- REDUCE_MEAN: Average across all time series
- REDUCE_MAX: Maximum across all time series
- REDUCE_SUM: Sum across all time series
- REDUCE_COUNT: Count of time series

**CROSS-SERIES EXAMPLE** (aggregate CPU across all instances in a zone):

```bash
gcloud monitoring time-series list \
    --filter="metric.type='compute.googleapis.com/instance/cpu/utilization'" \
    --aggregation.alignment-period=3600s \
    --aggregation.per-series-aligner=ALIGN_MEAN \
    --aggregation.cross-series-reducer=REDUCE_MEAN \
    --aggregation.group-by-fields="resource.labels.zone" \
    --format="value(points[].value.doubleValue)"
```

### Billing Script (`get_billing_gcp.sh`)

**DO NOT read or modify the script file.** Only source and call the functions.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/gcp/gcp/scripts/get_billing_gcp.sh
```

**All functions enforce anti-hallucination rules**: `WHERE project.id` filter, `CAST(... AS NUMERIC)` on financial fields, net cost via UNNEST subquery (never LEFT JOIN UNNEST + SUM(cost)), `cost_type = 'regular'` where appropriate. Output is TOON format (tab-separated).

**TABLE NAMING CONVENTION**:

- Standard usage: `dataset.gcp_billing_export_v1_<BILLING_ACCOUNT_ID_NO_DASHES>`
- Detailed usage: `dataset.gcp_billing_export_resource_v1_<BILLING_ACCOUNT_ID_NO_DASHES>`
- Billing Account ID `012ABC-456DEF-789GHI` becomes table suffix `012ABC456DEF789GHI` (dashes removed)

**FUNCTION REFERENCE**:

| Function | Purpose | Signature |
|----------|---------|-----------|
| `gcp_billing_currency` | Detect billing currency (MANDATORY first) | `TABLE PROJECT_ID` |
| `gcp_billing_credits` | Credit program detection (MANDATORY second) | `TABLE PROJECT_ID` |
| `gcp_billing_summary` | Top services by net cost | `TABLE PROJECT_ID [--days N]` |
| `gcp_billing_trend` | Daily net cost trend | `TABLE PROJECT_ID [--days N]` |
| `gcp_billing_anomalies` | Z-score anomaly on net cost | `TABLE PROJECT_ID` |
| `gcp_billing_by_resource` | Resource-level breakdown (detailed export) | `TABLE PROJECT_ID [--days N]` |
| `gcp_billing_by_sku` | SKU-level breakdown | `TABLE PROJECT_ID [--days N]` |
| `gcp_billing_invoice` | Invoice reconciliation (uses `invoice.month`) | `TABLE PROJECT_ID [--month YYYYMM]` |
| `gcp_billing_compare` | Multi-project comparison (no project filter) | `TABLE [--days N]` |

**MANDATORY WORKFLOW** (every billing analysis):

1. **Always run `gcp_billing_currency` first** to detect the billing currency (see Rule 11)
2. **Always run `gcp_billing_credits` second** to detect credit programs
3. Interpret `credit_coverage_ratio`: close to -1.0 = fully covered by credits (do NOT alarm); -0.3 to -0.01 = partial discounts (normal); ~0 = minimal credits
4. Then run `gcp_billing_summary` or other functions as needed
5. Sanity-check costs against known GCP pricing **in the detected currency** (see Rule 4)

**Examples:**

```bash
source ./_skills/connections/gcp/gcp/scripts/get_billing_gcp.sh
TABLE="dataset.gcp_billing_export_v1_012ABC456DEF789GHI"
PROJECT="my-project-id"

# Step 0a: Detect billing currency (MANDATORY - see Rule 11)
gcp_billing_currency "$TABLE" "$PROJECT"

# Step 0b: Detect credit programs (MANDATORY)
gcp_billing_credits "$TABLE" "$PROJECT"

# Top services by net cost (last 30 days)
gcp_billing_summary "$TABLE" "$PROJECT" --days 30

# Daily trend
gcp_billing_trend "$TABLE" "$PROJECT" --days 14

# Anomaly detection
gcp_billing_anomalies "$TABLE" "$PROJECT"

# Resource-level breakdown (requires detailed export table)
gcp_billing_by_resource "$TABLE" "$PROJECT" --days 7

# SKU-level breakdown
gcp_billing_by_sku "$TABLE" "$PROJECT" --days 7

# Invoice reconciliation (current month)
gcp_billing_invoice "$TABLE" "$PROJECT"

# Invoice reconciliation (specific month)
gcp_billing_invoice "$TABLE" "$PROJECT" --month 202601

# Multi-project comparison (no project filter)
gcp_billing_compare "$TABLE" --days 7
```

**BILLING EXPORT SCHEMA REFERENCE** (key columns):

| Column              | Description                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------- |
| `currency`          | ISO 4217 currency code (USD, VND, EUR, etc.). **Check this FIRST — never assume USD.**   |
| `cost`              | Usage cost at contract/on-demand rate, BEFORE credits. NOT your actual bill.             |
| `cost_at_list`      | Cost at public list price (before negotiated discounts).                                 |
| `credits`           | Array of credit entries. Each has `type`, `amount` (always negative), `full_name`.       |
| `credits.type`      | PROMOTION, SUSTAINED_USAGE_DISCOUNT, COMMITTED_USAGE_DISCOUNT, FREE_TIER, DISCOUNT, etc. |
| `cost_type`         | "regular", "tax", "adjustment", or "rounding_error".                                     |
| `project.id`        | GCP project ID. ALWAYS filter by this.                                                   |
| `invoice.month`     | YYYYMM string. Use for invoice reconciliation.                                           |
| `usage_start_time`  | When usage occurred. Use for trend analysis.                                             |
| `resource.name`     | Resource identifier (detailed export only).                                              |

**CREDIT TYPES**:

| Credit Type                            | Meaning                                                    | Typical Coverage          |
| -------------------------------------- | ---------------------------------------------------------- | ------------------------- |
| `PROMOTION`                            | Trial credits, startup credits, enterprise promotional     | Can be 100% (full offset) |
| `SUSTAINED_USAGE_DISCOUNT`             | Auto-discount for N1/N2/N2D/C2/M1/M2 running >25% of month | Up to 30% for N1          |
| `COMMITTED_USAGE_DISCOUNT`             | Resource-based CUD commitment                              | 37-55% depending on term  |
| `COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE` | Spend-based CUD commitment                                 | Varies by commitment      |
| `FREE_TIER`                            | Always-free tier usage                                     | Small amounts             |
| `DISCOUNT`                             | Other negotiated discounts                                 | Varies                    |
| `RESELLER_MARGIN`                      | Reseller margin credits                                    | Varies                    |

**NOTE on SUDs**: E2 machine types are NOT eligible for Sustained Use Discounts. Only N1, N2, N2D, C2, M1, M2 families receive SUDs.

### gcloud Topic References

**BUILT-IN HELP - Learn filter/format/projection syntax**

```bash
gcloud topic filters      # Filter expression syntax and operators
gcloud topic formats      # Output format options and projections
gcloud topic projections  # Projection functions (.scope(), .date(), etc.)
```

### Parallel vs Sequential Rules Summary

**PARALLEL vs SEQUENTIAL - Quick Reference**

- **ALWAYS PARALLEL**: Multiple instances, metrics, zones, or projects
- **ONLY SEQUENTIAL**: When operation B requires output from operation A
- **PATTERN**: `for item in $items; do operation "$item" & done; wait`

**FORBIDDEN ANTI-PATTERNS** (see detailed examples above):

- ❌ Sequential loops: `for x in $list; do cmd; done` → use `& done; wait`
- ❌ Sequential commands: `result1=$(cmd1); result2=$(cmd2)` → use `cmd1 & cmd2 & wait`
- ❌ Individual describe calls when list is available

## Output Format

Present results as a structured report:
```
Gcp Report
══════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

