---
name: aws-billing
description: |
  Use when working with Aws Billing — analyze, break down, and report AWS costs
  and bills. Covers cost breakdown by service, account, or usage type;
  monthly/daily billing trends; cost anomaly detection; RI/SP utilization; cost
  forecasting; credit/discount analysis; and multi-account cost comparison. Uses
  anti-hallucination rules, mandatory currency/credit detection workflow, and
  reusable Cost Explorer functions.
connection_type: aws
preload: false
---

# AWS Billing Skill

Analyze AWS billing data with anti-hallucination guardrails and reusable Cost Explorer functions.

**Relationship to other AWS skills:**

- `aws-billing/` → "What to analyze" (anti-hallucination rules, reusable billing functions)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)
- `aws-pricing/` → "How much things cost" (on-demand pricing via `get_aws_cost`)

## CRITICAL: Billing Data Interpretation Rules (Anti-Hallucination)

**These rules are MANDATORY when analyzing AWS billing data. Violating them produces wildly incorrect cost reports.**

### Rule 1: NET COST Requires the Correct Metric

AWS Cost Explorer exposes 5 cost metrics. The correct default is **`NetUnblendedCost`**, which reflects actual charges after all discounts and credits. Never report `UnblendedCost` alone — it shows charges _before_ negotiated discounts, credits, and RI/SP adjustments.

```
WRONG:  --metrics "UnblendedCost"          → Overstates costs
WRONG:  --metrics "BlendedCost"            → Only meaningful for consolidated billing families
CORRECT: --metrics "NetUnblendedCost"      → Actual charges after discounts/credits
```

The `aws_billing_*` functions enforce `NetUnblendedCost` by default via the `_AWS_DEFAULT_METRIC` constant.

### Rule 2: Understand the 5 AWS Cost Metrics

| Metric               | What It Represents                                         | When To Use                                                                               |
| -------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **BlendedCost**      | Weighted average rate across a consolidated billing family | Multi-account cost allocation reports (rarely useful for analysis)                        |
| **UnblendedCost**    | On-demand equivalent cost before any discounts             | Comparing against on-demand pricing; calculating "what would this cost without discounts" |
| **AmortizedCost**    | Cost with RI/SP upfront fees spread over the term          | Budgeting and forecasting; shows true economic cost of RI/SP commitments                  |
| **NetAmortizedCost** | AmortizedCost minus credits and negotiated discounts       | Most accurate for financial planning with RI/SP commitments                               |
| **NetUnblendedCost** | UnblendedCost minus credits and negotiated discounts       | **DEFAULT for analysis.** Shows actual charges on the bill                                |

**Key relationships:**

```
UnblendedCost - Discounts/Credits = NetUnblendedCost
AmortizedCost - Discounts/Credits = NetAmortizedCost
AmortizedCost = UnblendedCost + RI/SP upfront amortization adjustment
```

### Rule 3: Always Detect Account Context First

AWS caller identity determines what billing data you can see:

- **Management (payer) account**: Sees all linked accounts in the organization
- **Member (linked) account**: Sees only its own costs (unless delegated access is enabled)

**MANDATORY first query**: Run `aws_billing_account` to detect:

1. Which account you're operating as (payer vs. member)
2. The billing currency
3. Which linked accounts are visible

Without this context, you may unknowingly aggregate costs across unrelated accounts or miss accounts entirely.

### Rule 4: Sanity-Check Costs Against Known Pricing

Before reporting any cost figure, verify it's physically possible.

**Step 1: Check the currency.** AWS billing is typically USD, but organizations may have custom billing currencies. The `Unit` field in CE responses reveals the currency.

**Step 2: Verify magnitude against known pricing:**

| Resource          | Region    | Approximate Monthly On-Demand (USD) |
| ----------------- | --------- | ----------------------------------- |
| t3.micro          | us-east-1 | ~$8/mo                              |
| t3.small          | us-east-1 | ~$15/mo                             |
| t3.medium         | us-east-1 | ~$30/mo                             |
| m5.large          | us-east-1 | ~$70/mo                             |
| m5.xlarge         | us-east-1 | ~$140/mo                            |
| r5.large          | us-east-1 | ~$91/mo                             |
| db.t3.micro (RDS) | us-east-1 | ~$15/mo                             |
| db.r5.large (RDS) | us-east-1 | ~$175/mo                            |
| NAT Gateway       | us-east-1 | ~$32/mo + $0.045/GB                 |
| ALB               | us-east-1 | ~$16/mo + LCU charges               |

**Red flags that indicate a query error or currency mismatch:**

- A single EC2 instance shows >$1,000/week (t3.medium costs ~$30/month)
- Total account cost exceeds $500,000/week for a standard workload
- Numbers are 1000x higher than expected (possible currency mismatch)

**If numbers seem unreasonably high, STOP and verify the currency before reporting.**

### Rule 5: Detect Credits/Discounts Before Alerting

If `NetUnblendedCost` is much lower than `UnblendedCost`, the account has active discounts (RI, SP, EDP, credits). This is normal — not an anomaly.

**MANDATORY second query**: Run `aws_billing_credits` FIRST to detect:

1. `discount_ratio`: `(Unblended - NetUnblended) / Unblended`
2. `ri_sp_amortization_effect`: `Amortized - Unblended`

**Interpretation:**

| discount_ratio | Meaning                                                                           |
| -------------- | --------------------------------------------------------------------------------- |
| > 0.5          | Heavy credit/discount coverage (RI/SP/EDP/credits) — costs are heavily discounted |
| 0.1 – 0.5      | Moderate discounts (typical for RI/SP usage)                                      |
| < 0.1          | Minimal discounts — mostly on-demand pricing                                      |

**If discount_ratio > 0.5:** Report that the account has significant discounts. Do NOT generate alarmist alerts about cost levels unless the user specifically asks for on-demand equivalent analysis.

### Rule 6: Anomaly Detection on Net Cost Only

`UnblendedCost` fluctuates when RI/SP coverage changes (e.g., an RI expires, a new SP starts). These fluctuations are not real spending anomalies — they're accounting changes.

```
WRONG:  Detect anomalies on UnblendedCost → false positives from RI/SP changes
CORRECT: Detect anomalies on NetUnblendedCost → real spending changes
```

The `aws_billing_anomalies` function enforces this by using `_AWS_DEFAULT_METRIC` (NetUnblendedCost).

### Rule 7: Use MONTHLY Granularity by Default

DAILY granularity with SERVICE grouping produces `N_days × N_services` rows — easily 1,000+ lines for 30 days. This wastes tokens and provides no additional insight for most analyses.

```
WRONG:  --granularity DAILY for 30 days with GROUP_BY SERVICE → token explosion
CORRECT: --granularity MONTHLY + awk aggregation + sort -rn | head -15
```

Only use DAILY granularity when:

1. The user specifically requests daily breakdown
2. You're doing anomaly detection (requires daily data points)
3. The date range is ≤ 7 days

HOURLY granularity exists but is limited to the past **14 days** and only available for EC2 instance-level data. Avoid HOURLY unless the user specifically needs sub-day resolution for a narrow window.

The `aws_billing_trend` function defaults to MONTHLY and only switches to DAILY with `--daily` flag.

### Rule 8: Cost Explorer Has Limited Lookback

AWS Cost Explorer API retains **13 months + current month** of historical data by default. With **multi-year data** enabled (in Cost Management preferences), up to **38 months** at monthly granularity is available. Resource-level data (`get-cost-and-usage-with-resources`) is limited to **14 days**.

Queries beyond the available range return a **validation error** (not empty results).

```
WRONG:  --days 500 → validation error: start date too old
CORRECT: --days 420 (safe default limit) or --days 365 (safe 12-month lookback)
```

The `_aws_parse_days` helper enforces the 420-day limit and returns an error if exceeded. If the organization has multi-year data enabled, you can modify the `_AWS_MAX_LOOKBACK_DAYS` constant.

### Rule 9: CE Date Ranges — Start Inclusive, End Exclusive

Cost Explorer uses half-open intervals: `[Start, End)`.

```
"Last 30 days" = Start: 30 days ago, End: today
```

- **Start**: The first day INCLUDED in the results
- **End**: The first day EXCLUDED from the results

If you set End = today, today's partial data IS excluded (which is correct — see Rule 10).

The `_aws_date_start` and `_aws_date_end` helpers handle this correctly.

### Rule 10: Data Has Up To 24 Hour Delay

AWS billing data updates up to 3 times daily but can take up to 24 hours to fully propagate. Today's costs are always incomplete.

**Do NOT:**

- Alert on "cost drops" for the current day
- Compare today's partial data to yesterday's full data
- Report today's costs as final

The billing functions set `End = today` (which excludes today due to Rule 9), ensuring only complete data is analyzed.

### Rule 11: RI/SP API Dimension Restrictions

Cost Explorer's reservation and savings plan APIs have strict dimension restrictions:

| API                             | Valid groupBy Dimensions                                                                                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `get-reservation-utilization`   | `SUBSCRIPTION_ID` only                                                                                                                                                   |
| `get-reservation-coverage`      | `AZ`, `CACHE_ENGINE`, `DATABASE_ENGINE`, `DEPLOYMENT_OPTION`, `INSTANCE_TYPE`, `INVOICING_ENTITY`, `LINKED_ACCOUNT`, `OPERATING_SYSTEM`, `PLATFORM`, `REGION`, `TENANCY` |
| `get-savings-plans-utilization` | No groupBy support                                                                                                                                                       |
| `get-savings-plans-coverage`    | `INSTANCE_FAMILY`, `REGION`, `SERVICE`                                                                                                                                   |

Using unsupported dimensions causes API errors. For SERVICE-level analysis, use `get-cost-and-usage` instead.

**Additional restrictions:**

- `get-reservation-utilization` defaults to EC2 if no SERVICE filter is specified. To check RDS/ElastiCache/Redshift RI utilization, you must explicitly pass a SERVICE filter.
- `get-reservation-utilization`/`get-reservation-coverage` filters only support `AND` between dimensions (no `OR`/`NOT` combinations), nesting max 1 level deep.
- `get-savings-plans-utilization`/`get-savings-plans-coverage` filters only support `AND` between dimensions.

### Rule 12: Tax Appears as a Separate Service

AWS reports taxes (VAT, consumption tax, sales tax) as a separate service line called **"Tax"** in Cost Explorer. This is not a cloud service — it's a billing artifact.

- `NetUnblendedCost` does **NOT** exclude taxes (it only excludes credits/discounts). Taxes are real charges.
- "Tax" may appear in `aws_billing_summary` as a top service. Do not confuse it with compute/storage spend.
- When comparing AWS costs to GCP, note that GCP's `cost_type` separates `tax` from `regular` charges, while AWS mixes them into the same metric.
- For tax-specific analysis, filter by `SERVICE = "Tax"` to isolate tax charges.

### Mandatory Pre-Analysis Checklist

**Before writing ANY billing analysis, verify ALL of the following:**

- [ ] **Account context detected** via `aws_billing_account` (payer vs. member, currency, linked accounts)
- [ ] **Credits/discounts detected** via `aws_billing_credits` (discount_ratio, RI/SP amortization)
- [ ] Default metric is `NetUnblendedCost` (not `UnblendedCost` or `BlendedCost`)
- [ ] Date range is within 420-day CE lookback limit
- [ ] Granularity is MONTHLY unless daily is specifically needed
- [ ] `--filter` with LINKED_ACCOUNT is used when analyzing a specific account
- [ ] Any per-resource cost is sanity-checked against known AWS pricing
- [ ] Anomaly detection uses NetUnblendedCost, not UnblendedCost
- [ ] RI/SP API calls use only supported dimensions (see Rule 11)
- [ ] **All cost figures in the report include the currency unit**

---

## Billing Script (`get_billing_aws.sh`)

**DO NOT read or modify the script file.** Only source and call the functions.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/aws/aws-billing/scripts/get_billing_aws.sh
```

**All functions enforce anti-hallucination rules**: NetUnblendedCost default metric, account filter when specified, 420-day lookback limit, TOON output format.

**FUNCTION REFERENCE**:

| Function                    | Purpose                                                    | Signature                             |
| --------------------------- | ---------------------------------------------------------- | ------------------------------------- |
| `aws_billing_account`       | Detect caller, currency, linked accounts (MANDATORY first) | `[--days N]`                          |
| `aws_billing_credits`       | Credit/discount program detection (MANDATORY second)       | `[--account ID] [--days N]`           |
| `aws_billing_summary`       | Top 15 services by net cost                                | `[--account ID] [--days N]`           |
| `aws_billing_trend`         | Cost trend (monthly/daily)                                 | `[--account ID] [--days N] [--daily]` |
| `aws_billing_anomalies`     | Z-score anomaly on net cost (45-day lookback)              | `[--account ID]`                      |
| `aws_billing_by_usage_type` | Top 20 usage types by net cost                             | `[--account ID] [--days N]`           |
| `aws_billing_forecast`      | CE cost forecast with prediction intervals                 | `[--account ID] [--days N]`           |
| `aws_billing_ri_sp`         | RI and Savings Plan utilization                            | `[--account ID] [--days N]`           |
| `aws_billing_compare`       | Multi-account comparison (no account filter)               | `[--days N]`                          |

**MANDATORY WORKFLOW** (every billing analysis):

1. **Always run `aws_billing_account` first** to detect caller identity, currency, and linked accounts (see Rule 3)
2. **Always run `aws_billing_credits` second** to detect discount programs (see Rule 5)
3. Interpret `discount_ratio`: > 0.5 = heavily discounted (do NOT alarm); 0.1–0.5 = moderate discounts; < 0.1 = minimal discounts
4. Then run `aws_billing_summary` or other functions as needed
5. Sanity-check costs against known AWS pricing (see Rule 4)

**Examples:**

```bash
source ./_skills/connections/aws/aws-billing/scripts/get_billing_aws.sh

# Step 1: Detect account context and currency (MANDATORY)
aws_billing_account

# Step 2: Detect credit/discount programs (MANDATORY)
aws_billing_credits

# Top services by net cost (last 30 days)
aws_billing_summary --days 30

# Filter to specific linked account
aws_billing_summary --account 123456789012 --days 30

# Monthly trend (last 90 days)
aws_billing_trend --days 90

# Daily trend (last 14 days)
aws_billing_trend --days 14 --daily

# Anomaly detection
aws_billing_anomalies

# Usage type breakdown
aws_billing_by_usage_type --days 30

# Cost forecast (next 30 days)
aws_billing_forecast --days 30

# RI and Savings Plan utilization (last 90 days)
aws_billing_ri_sp --days 90

# Multi-account comparison (no account filter)
aws_billing_compare --days 30
```

---

## CLI Execution Patterns

The `aws_billing_*` functions handle CE queries correctly by default. For custom `aws ce` commands, read `docs/ce-cli-patterns.md` in this skill directory for:
- Cost Explorer output aggregation and token efficiency rules
- Heredoc syntax pitfalls (options MUST come before `<<EOF`)
- CloudTrail event parsing with `jq fromjson`

---

## Cost Metrics Deep Reference

### UnblendedCost

The cost of usage at the rate the account is charged — i.e., the on-demand rate minus any RI/SP hourly discount, but **before** credits and negotiated discounts (EDP). For accounts with RI/SP, the RI/SP-covered hours show the discounted RI/SP rate, while uncovered hours show on-demand rate.

**When to use:** Comparing against on-demand pricing; understanding what each resource "costs" at its charged rate.

### NetUnblendedCost

`UnblendedCost` minus credits, EDP discounts, and other negotiated adjustments. This is what actually appears on your bill.

**When to use:** **Default for all analysis.** Shows actual charges.

### BlendedCost

The weighted average rate across all accounts in a consolidated billing family. AWS computes this by pooling usage across accounts to maximize tiered pricing benefits, then redistributing the blended rate.

**When to use:** Rarely. Only useful for cross-account cost allocation in organizations that want to distribute volume discounts evenly.

### AmortizedCost

Spreads RI/SP upfront payments evenly across the term. For example, a $10,000 1-year All Upfront RI shows ~$27.40/day instead of $10,000 on day 1 and $0 thereafter.

**When to use:** Budgeting and forecasting; understanding the true daily economic cost of RI/SP commitments.

### NetAmortizedCost

`AmortizedCost` minus credits and negotiated discounts. The most accurate metric for financial planning when you have RI/SP commitments.

**When to use:** Long-term financial planning with RI/SP commitments; board-level cost reporting.

---

## AWS Pricing Sanity-Check Table

Approximate monthly on-demand costs in USD (us-east-1). Use to validate query results.

| Resource    | Type              | ~Monthly USD |
| ----------- | ----------------- | ------------ |
| EC2         | t3.micro          | $8           |
| EC2         | t3.small          | $15          |
| EC2         | t3.medium         | $30          |
| EC2         | m5.large          | $70          |
| EC2         | m5.xlarge         | $140         |
| EC2         | c5.xlarge         | $124         |
| EC2         | r5.large          | $91          |
| RDS         | db.t3.micro       | $15          |
| RDS         | db.t3.small       | $29          |
| RDS         | db.r5.large       | $175         |
| ElastiCache | cache.t3.micro    | $13          |
| NAT Gateway | per gateway       | $32 + data   |
| ALB         | per ALB           | $16 + LCU    |
| S3          | Standard/GB       | $0.023       |
| EBS         | gp3/GB            | $0.08        |
| Lambda      | 1M req, 1s, 128MB | $2.10        |

If your query shows a single t3.medium costing $3,000/month, something is wrong.

---

## Discount and Credit Types

| Type                                  | Source                                 | Typical Savings         | How It Affects Metrics                                                     |
| ------------------------------------- | -------------------------------------- | ----------------------- | -------------------------------------------------------------------------- |
| **Reserved Instances (RI)**           | Upfront commitment (1yr or 3yr)        | 30–72% vs on-demand     | Lowers UnblendedCost for covered hours; AmortizedCost spreads upfront fee  |
| **Savings Plans (SP)**                | Hourly commitment (1yr or 3yr)         | 20–72% vs on-demand     | Same effect as RI but more flexible (Compute SP covers EC2+Fargate+Lambda) |
| **Enterprise Discount Program (EDP)** | Spend commitment with AWS              | 5–20% off entire bill   | Difference between Unblended and NetUnblended                              |
| **Free Tier**                         | Automatic for new accounts (12 months) | 100% for eligible usage | Shows as $0 NetUnblendedCost for covered usage                             |
| **Promotional Credits**               | AWS programs (startups, migrations)    | Up to 100%              | Shows as gap between Unblended and NetUnblended                            |

**Key insight:** `discount_ratio` from `aws_billing_credits` captures the combined effect of ALL discount types. If > 0.5, the account is heavily discounted.

---

## CE API Quick Reference

### Filter Syntax

```bash
# Single account
--filter '{"Dimensions":{"Key":"LINKED_ACCOUNT","Values":["123456789012"]}}'

# Single service
--filter '{"Dimensions":{"Key":"SERVICE","Values":["Amazon Elastic Compute Cloud - Compute"]}}'

# AND: account + service
--filter '{"And":[{"Dimensions":{"Key":"LINKED_ACCOUNT","Values":["123456789012"]}},{"Dimensions":{"Key":"SERVICE","Values":["Amazon Elastic Compute Cloud - Compute"]}}]}'

# NOT: exclude specific service
--filter '{"Not":{"Dimensions":{"Key":"SERVICE","Values":["AWS Support (Business)"]}}}'

# Tag filter
--filter '{"Tags":{"Key":"Environment","Values":["production"]}}'
```

### GroupBy Syntax

```bash
# By service
--group-by Type=DIMENSION,Key=SERVICE

# By linked account
--group-by Type=DIMENSION,Key=LINKED_ACCOUNT

# By usage type
--group-by Type=DIMENSION,Key=USAGE_TYPE

# By tag (must be activated in billing console)
--group-by Type=TAG,Key=Environment

# Multiple groups (max 2)
--group-by Type=DIMENSION,Key=SERVICE Type=DIMENSION,Key=LINKED_ACCOUNT
```

### Heredoc & Output Rules

For raw CE query patterns (heredoc ordering, awk aggregation, output size limits), see docs/ce-cli-patterns.md in this skill directory.

### get-cost-forecast Notes

- Uses `--metric` (singular), not `--metrics` (plural)
- **Metric names use SCREAMING_SNAKE_CASE** (e.g., `NET_UNBLENDED_COST`), NOT CamelCase like `get-cost-and-usage`
- Valid metric values: `AMORTIZED_COST`, `BLENDED_COST`, `NET_AMORTIZED_COST`, `NET_UNBLENDED_COST`, `UNBLENDED_COST`
- Start date must be **tomorrow or later** (cannot forecast the past)
- Maximum forecast period: **3 months** at DAILY granularity, **18 months** at MONTHLY granularity
- Prediction intervals are only available for certain granularities

### CE API Pricing

Cost Explorer API charges **per paginated request** ($0.01/request). Cache results when possible and avoid redundant queries. Use filtering and appropriate granularity to minimize pagination.

---

## Common Errors

| Error                                             | Cause                                              | Solution                                                            |
| ------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------- |
| `Start date must be after today`                  | `get-cost-forecast` start date is today or earlier | Use `_aws_date_end_future 1` for start                              |
| `The requested time range is not available`       | Date range exceeds ~14 months                      | Limit to 420 days max                                               |
| `ValidationException: groupBy Dimensions`         | Invalid dimension for RI/SP APIs                   | See Rule 11 for valid dimensions                                    |
| `Metrics must contain only one element`           | `get-cost-forecast` called with multiple metrics   | Use `--metric` (singular) with one metric                           |
| `Value 'NetUnblendedCost' for metric is invalid`  | Wrong casing for `get-cost-forecast` metric        | Use SCREAMING_SNAKE_CASE: `NET_UNBLENDED_COST`                      |
| `OptIn is not supported for the following metric` | NetUnblendedCost not enabled                       | Enable in Cost Explorer settings (24h activation)                   |
| `Access Denied` for CE APIs                       | Member account without delegated access            | Check organization delegated administrator settings                 |
| `DataUnavailable`                                 | Querying dates before CE was activated             | CE data starts from account activation date                         |
| `BillingPeriodRange` / start date too old         | Date range beyond available lookback               | Reduce to 420 days (or 38mo if multi-year enabled)                  |
| `UnrecognizedClientException`                     | STS session expired or invalid credentials         | Re-authenticate or re-assume role                                   |
| Costs seem 0 but account is active                | Account on Free Tier or full credit coverage       | Run `aws_billing_credits` to check discount_ratio                   |
| Forecast returns error for long period            | Exceeds forecast limit (3mo daily, 18mo monthly)   | Reduce forecast period or switch to MONTHLY granularity             |
| RI utilization shows only EC2                     | `get-reservation-utilization` defaults to EC2      | Pass `--filter` with SERVICE dimension for RDS/ElastiCache/Redshift |

## Output Format

Present results as a structured report:
```
Aws Billing Report
══════════════════
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

