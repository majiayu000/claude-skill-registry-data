---
name: infrastructure-cost-estimation
description: |
  Help you discover how much you spend on AWS/GCP/Azure. This rulebook guides practitioners through proper cloud cost calculations, systematic resource discovery (via IaC analysis and live environment enumeration), authoritative pricing research and analysis/estimation.
license: MIT
tags:
  - cost
  - cloud
  - pricing
  - cost optimization
  - analysis
  - aws
  - gcp
  - azure
  - cloud spend
  - finops
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

# Infrastructure Cost Estimation Methodology

 

## CRITICAL REQUIREMENT: EXCLUDE ALL CREDITS BY DEFAULT

**MANDATORY**: Always exclude credits, promotional offers, and discounts to get TRUE infrastructure cost. Report:

1. **Gross Cost** (without credits) - PRIMARY NUMBER
2. **Net Cost** (with credits) - comparison only

Credits are temporary and mask real costs. Always plan for post-credit expenses.

## Core Principles

1. **Native Cost Tools First**: Use cloud provider billing tools as primary source
2. **Credits Excluded**: Always exclude credits unless analyzing discount impact
3. **Comprehensive Discovery**: Identify ALL infrastructure components
4. **Current Pricing**: Research real-time standard pricing only
5. **Python Calculations**: Use Python for ALL numeric operations

## Phase 1: Native Cost Estimation

### Time Period Requirements

**CRITICAL**: Always use the most recent complete months for analysis:

* **Primary Analysis**: Last 3 complete months (most recent data)
* **Trend Analysis**: Last 6 complete months (for patterns)
* **Never use data older than 6 months** unless specifically requested
* **Always specify actual date ranges** in your analysis
* **Determine current date first**, then calculate recent complete months

### Credit Exclusion Steps - CLI Commands

**CRITICAL**: Use these exact CLI commands to exclude credits and get true infrastructure costs:

#### AWS CLI Credit Exclusion

```
# Exclude all credits and promotional charges
aws ce get-cost-and-usage \
  --time-period Start=YYYY-MM-01,End=YYYY-MM-01 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --filter '{
    "Not": {
      "Dimensions": {
        "Key": "RECORD_TYPE",
        "Values": ["Credit", "Refund", "SavingsPlanNegation", "DiscountedUsage"]
      }
    }
  }' \
  --group-by Type=DIMENSION,Key=SERVICE

```

#### Azure CLI Credit Exclusion

Create query file `exclude-credits.json`:

```
{
  "type": "Usage",
  "timeframe": "Custom",
  "timePeriod": {
    "from": "YYYY-MM-01T00:00:00.000Z",
    "to": "YYYY-MM-01T00:00:00.000Z"
  },
  "dataset": {
    "granularity": "Monthly",
    "filter": {
      "not": {
        "dimensions": {
          "name": "ChargeType",
          "operator": "In",
          "values": ["Credit", "Refund", "RoundingAdjustment"]
        }
      }
    },
    "aggregation": {
      "totalCost": {
        "name": "PreTaxCost",
        "function": "Sum"
      }
    },
    "grouping": [{"type": "Dimension", "name": "ServiceName"}]
  }
}

```

Execute with:

```
az rest --method POST \
  --url "https://management.azure.com/subscriptions/$(az account show --query id -o tsv)/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --body @exclude-credits.json

```

#### Google Cloud Credit Exclusion

**Note**: Google Cloud requires BigQuery queries. No direct CLI credit filtering available.

```
# First, execute BigQuery to exclude promotional credits
bq query --use_legacy_sql=false '
SELECT 
  invoice.month,
  service.description,
  SUM(cost) as gross_cost_no_credits
FROM `PROJECT-ID.DATASET.gcp_billing_export_v1_BILLING-ACCOUNT-ID`
WHERE invoice.month IN ("YYYYMM", "YYYYMM", "YYYYMM")
GROUP BY invoice.month, service.description
ORDER BY gross_cost_no_credits DESC;'

```

**Key Filter Parameters by Provider**:

* **AWS**: Exclude RECORD\_TYPE values: "Credit", "Refund", "SavingsPlanNegation", "DiscountedUsage"
* **Azure**: Exclude ChargeType values: "Credit", "Refund", "RoundingAdjustment"
* **Google Cloud**: Use BigQuery on billing export tables, no promotional credits included

### Native Tools

**AWS**: Cost Explorer, Pricing Calculator, Budgets, Cost & Usage Reports, Billing Dashboard **Azure**: Cost Management + Billing, Pricing Calculator, Advisor, Resource Graph\
**Google Cloud**: Cloud Billing, Pricing Calculator, Asset Inventory, Recommender

## Phase 2: Resource Discovery

**Methods**: IaC analysis, live environment queries, API enumeration **Categories**: Compute, storage, networking, platform services, security, monitoring, development, data services **Coverage**: All environments, regions, scaling policies, shared resources

## Phase 3: Pricing Research

**Requirements**:

* Official provider pricing pages only
* Region-specific standard rates
* No promotional or discount pricing
* Current pay-as-you-go rates

## Phase 4: Python Calculations

### Credit Analysis Template

```
def analyze_credit_impact(billing_data, analysis_period="recent_months"):
    """
    Analyze credit impact for recent complete months
    Calculate recent months dynamically based on current date
    """
    from datetime import datetime, timedelta
    
    # Determine current date and calculate recent complete months
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Calculate the last 3 complete months
    recent_months = []
    for i in range(3):
        month_offset = i + 1
        if current_month - month_offset <= 0:
            month = 12 + (current_month - month_offset)
            year = current_year - 1
        else:
            month = current_month - month_offset
            year = current_year
        recent_months.append((year, month))
    
    recent_months.reverse()  # Put in chronological order
    
    # Filter billing data to recent complete months
    recent_billing_data = [
        charge for charge in billing_data 
        if (charge['date'].year, charge['date'].month) in recent_months
    ]
    
    analysis = {
        'analysis_period': f"Recent 3 complete months: {recent_months[0][1]}/{recent_months[0][0]} - {recent_months[2][1]}/{recent_months[2][0]}",
        'gross_monthly_cost': sum(
            charge['amount'] for charge in recent_billing_data 
            if charge['type'] in ['Usage', 'Tax', 'Fee']
        ) / 3,  # Average over 3 months
        'net_monthly_cost': sum(charge['amount'] for charge in recent_billing_data) / 3,
        'total_credits_applied': 0,
        'credit_sustainability': 'TEMPORARY - Assume all credits expire'
    }
    
    analysis['total_credits_applied'] = (
        analysis['gross_monthly_cost'] - analysis['net_monthly_cost']
    )
    
    return analysis

```

### Basic Cost Calculation

```
def calculate_monthly_costs(resources, pricing_data):
    HOURS_PER_MONTH = 730
    total_cost = 0
    cost_breakdown = {}
    
    for service_name, service_config in resources.items():
        service_cost = 0
        
        # Fixed costs (standard hourly rates)
        if 'instances' in service_config:
            hourly_rate = pricing_data[service_name]['standard_hourly_rate']
            instance_count = service_config['instances']
            service_cost += hourly_rate * instance_count * HOURS_PER_MONTH
        
        # Usage-based costs (standard rates)
        if 'usage_metrics' in service_config:
            for metric, usage in service_config['usage_metrics'].items():
                unit_cost = pricing_data[service_name]['standard_usage'][metric]
                service_cost += usage * unit_cost
        
        cost_breakdown[service_name] = round(service_cost, 2)
        total_cost += service_cost
    
    return {
        'total_monthly_cost': round(total_cost, 2),
        'service_breakdown': cost_breakdown
    }

```

## Implementation Checklist

### Credit Exclusion (MANDATORY FIRST)

* [ ] Excluded ALL credits from native tool analysis
* [ ] Calculated gross monthly cost (true infrastructure cost)
* [ ] Assessed credit expiration timeline

### Analysis Steps

* [ ] Used native cost tools or CLI commands with credits excluded for **recent 3 complete months**
* [ ] Applied correct CLI filters for each provider (AWS: RECORD\_TYPE, Azure: ChargeType, GCP: BigQuery)
* [ ] Specified exact date range in analysis
* [ ] Discovered all resources across all environments
* [ ] Researched current standard pricing rates
* [ ] Calculated costs using Python with standard rates
* [ ] Validated native vs calculated costs using gross amounts from recent months

## Output Format

### 1. Credit Impact Analysis

* **Analysis Period**: \[Specify actual 3 months analyzed]
* **Gross Monthly Cost** (without credits): $X,XXX - **PRIMARY NUMBER**
* **Net Monthly Cost** (with credits): $X,XXX
* **Credits Applied**: $XXX/month
* **Credit Expiration Risk**: Timeline assessment

### 2. True Infrastructure Costs

* **Total Monthly Cost**: Min/avg/max scenarios at standard pricing
* **Service Breakdown**: Cost per service without discounts
* **Environment Breakdown**: Cost per environment at standard rates

### 3. Validation & Assumptions

* Native gross cost vs calculated cost comparison
* Key assumptions and methodology
* Python scripts for reproducibility

## Critical Reminders

* **ALWAYS EXCLUDE CREDITS FIRST** - Use specific CLI commands for each provider
* **USE RECENT 3 COMPLETE MONTHS** - Calculate current date, then use last 3 complete months
* **Correct CLI Filters**: AWS (RECORD\_TYPE), Azure (ChargeType + REST API), Google Cloud (BigQuery only)
* **Use native tools** - Most accurate real-time data
* **Standard pricing only** - No promotional rates
* **Python for all math** - Prevent calculation errors
* **Include ALL resources** - Incomplete discovery causes surprises
* **Document assumptions** - Enable validation and updates
