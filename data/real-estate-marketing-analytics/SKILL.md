---
name: real-estate-marketing-analytics
description: Specialized knowledge for real estate marketing analytics, including SEM campaign optimization, lead generation analysis, marketing channel performance, and geographic market insights. Use when working with real estate marketing data, Snowflake databases (RDC_ANALYTICS, RDC_MARKETING schemas), analyzing paid search campaigns, lead pricing trends, conversion funnels, or cross-channel attribution. Triggers include queries about Google Ads performance, lead quality analysis, market-level metrics, campaign budget optimization, or any real estate marketing KPIs.
---

# Real Estate Marketing Analytics Skill

This skill provides domain expertise for real estate marketing analytics, focusing on SEM optimization, lead generation, channel performance analysis, and data-driven decision making.

## Business Context

### Company Overview

**Vision:** Help more Americans find their way home.

**Mission:** Be the best open real estate marketplace.

**Dominant Goal:** Become the #1 real estate marketplace.

### Two-Sided Marketplace Model

Our business operates a two-sided marketplace connecting two distinct groups:

**Consumers (Leads)**
- Individuals interested in buying, selling, or renting a home
- Marketing efforts are aimed at attracting these users
- Success measured by lead volume, quality, and expected future revenue

**Customers (Realtors)**
- Real estate agents, brokerages, and Realtors
- Use our service to connect with motivated Consumers
- Pay for connections with Consumers

**Revenue Model**
- Success-based revenue (referral fees on closed deals)
- Our success is directly tied to our Customers' success in closing deals
- **Lead quality is paramount** due to this model

### Platforms & Properties

- **Realtor.com** - Core platform (website + mobile apps), primary top-of-funnel
- **Homefinder** - Strategic incubation platform for testing high-risk strategies (e.g., VBB)
- **New-Com** - Additional property
- **Moving.com** - Additional property

### External Factors Affecting Performance

**Seasonal Trends**
- **Slower Periods:** Winter months and major holidays see reduced activity
- **Peak Seasons:** Spring and summer are busiest for buying, selling, and moving
- Lead volume fluctuates predictably throughout the year

**Macroeconomic Trends**
- **Mortgage interest rates:** Higher rates reduce affordability and transaction volume
- **Consumer confidence:** Affects willingness to make major purchases
- **Economic uncertainty:** Can delay buying/selling decisions

**Competitive Activity**
- Market for real estate leads is finite and highly competitive
- Competing with other businesses for limited pool of potential clients
- Increased competitive spend impacts our costs and lead volume

## Core Workflow

When a marketing analytics task is requested:

1. **Understand the business question** - Identify the key metric or insight needed
2. **Review relevant references** - Load appropriate schema, business logic, and glossary files
3. **Query Snowflake** - Use the snowflake tool with proper database/schema context
4. **Analyze results** - Apply marketing analytics best practices and domain knowledge
5. **Provide actionable insights** - Frame findings in business context with recommendations

## Key Metrics (Quick Reference)

**North Star Metric:** EFR (Expected Future Revenue)

| Metric | Formula | Use |
|--------|---------|-----|
| ROAS | EFR / Spend | Campaign profitability |
| RPL | EFR / Leads | Lead value |
| CPL | Spend / Leads | Acquisition efficiency |
| CPC | Spend / Clicks | Traffic cost |
| LSR | Leads / Clicks | Click-to-lead conversion |

**Quality Metrics:**
- Good Quality Ratio = GQ_SELL_LEADS / SELL_INTENT_LEADS
- Sell Leads Ratio = SELL_INTENT_LEADS / LEADS

For detailed formulas and calculations, see [references/business_logic.md](references/business_logic.md).

For complete glossary of terms and acronyms, see [references/glossary.md](references/glossary.md).

## Key Concepts & Terminology

### Campaign Types
- **DSA (Dynamic Search Ads)** - Google ad type that auto-generates ads based on website content
- **Performance Max (PMax)** - Google's automated campaign type across all inventory
- **Buy Intent Campaigns** - Targeting users with high purchase intent signals
- **Brand Campaigns** - Campaigns targeting branded search terms
- **VBB (Value-Based Bidding)** - Sophisticated bidding strategy to acquire higher-value users
- **BAU (Business As Usual)** - Baseline campaigns used for performance comparison

### Lead Metrics
- **Lead Price** - Cost to acquire a lead (can be median or mean)
- **Lead Quality** - Assessed via downstream conversion rates and engagement
- **Volume-Weighted Performance** - Metrics adjusted for campaign spend/volume
- **Zero-Lead Markets** - Geographic areas with no lead generation despite listings

### Products & Programs
- **RCC (Ready Connect Concierge)** - Success-based referral product connecting high-intent consumers with agents
- **Dual Serving** - Running traffic to two different experiences simultaneously to test performance

### Geographic Hierarchy
- **DMA (Designated Market Area)** - TV market regions used for geographic analysis
- **State-Level Analysis** - Broader geographic segmentation
- **Market Alignment** - Comparing lead acquisition patterns with listing inventory

### Channel Attribution
- **Paid Search** - Google Ads, Bing Ads, etc.
- **Organic Search** - Unpaid search traffic
- **Direct** - Direct URL entry or bookmarked traffic
- **Referral** - Traffic from other websites

## Database Resources

For detailed schema information, table relationships, and query patterns:

- **See [references/snowflake_schema.md](references/snowflake_schema.md)** - Comprehensive database schema documentation
  - When to load: Any query involving Snowflake tables, joins, or data exploration
  - Contains: Table structures, key relationships, common query patterns

- **See [references/business_logic.md](references/business_logic.md)** - Business rules and metric definitions
  - When to load: Calculating KPIs, understanding metric definitions, applying business rules
  - Contains: Metric formulas, data quality rules, aggregation methods

- **See [references/glossary.md](references/glossary.md)** - Comprehensive terminology reference
  - When to load: Understanding acronyms, platform names, or business model context
  - Contains: All acronyms, platform definitions, external factors

## Team Goals & Priorities

### Current Focus Areas

1. **SEM Campaign Optimization**
   - Identify underperforming ad groups for budget reallocation
   - Analyze spend efficiency across campaign types
   - Track lead quality trends by campaign
   - Monitor ROAS and optimize for EFR

2. **Lead Generation Analysis**
   - Monitor lead pricing trends across channels
   - Analyze geographic distribution vs. inventory
   - Identify zero-lead markets and opportunities
   - Track Good Quality Ratio and Sell Leads Ratio

3. **Channel Performance**
   - Compare paid vs. organic search effectiveness
   - Track lead quality by acquisition channel
   - Measure volume-weighted campaign performance
   - Analyze RPL differences across channels

4. **Cross-Functional Collaboration**
   - Share insights via Slack with revenue teams
   - Track action items in Jira (MOPS project)
   - Coordinate with product on conversion optimization

## Common Analysis Patterns

### Campaign Performance Analysis
```
Goal: Identify underperforming campaigns/ad groups
Approach:
1. Pull spend, lead volume, and EFR data
2. Calculate ROAS, CPL, and RPL by segment
3. Compare against benchmarks
4. Identify reallocation opportunities
```

### Geographic Market Analysis
```
Goal: Align marketing spend with market opportunity
Approach:
1. Analyze lead volume by DMA/state
2. Compare with listing inventory
3. Identify misalignment (over/under-invested markets)
4. Calculate market-specific lead prices and ROAS
```

### Channel Attribution
```
Goal: Understand channel effectiveness
Approach:
1. Track leads by acquisition channel
2. Calculate CPL and RPL by channel
3. Analyze quality indicators (Good Quality Ratio)
4. Compare volume vs. quality trade-offs
```

### Clickstream Analysis
```
Goal: Track user journey from discovery to lead
Approach:
1. Query clickstream data (RDC_ANALYTICS.CLICKSTREAM)
2. Track sessions from SRP to lead submission
3. Identify drop-off points
4. Calculate conversion rates by step (LSR)
```

## Tools & Integrations

- **Snowflake** - Primary data warehouse (use snowflake MCP tool)
- **Google Ads** - Campaign management (bulk upload sheets for changes)
- **Jira** - Project tracking (MOPS project)
- **Slack** - Team communication and reporting

## Best Practices

### Query Optimization
- Always specify database and schema: `RDC_ANALYTICS.SCHEMA_NAME`
- Use CTEs for complex multi-step queries
- Filter early to reduce data volume
- Use appropriate aggregation levels

### Data Quality
- Check for null values in key fields
- Validate date ranges before analysis
- Cross-reference metrics across tables when possible
- Flag anomalies in the data

### Reporting
- Lead with the business insight, not the data
- Provide context (comparisons, trends, benchmarks)
- Include actionable recommendations
- Visualize when appropriate (Mermaid charts)
- **Always calculate ROAS using EFR**

### Collaboration
- Document assumptions and methodology
- Share reproducible queries
- Tag relevant team members in findings
- Track follow-up actions in Jira

## Updating This Skill

This skill should evolve as new insights emerge. Update when:

- **New tables or schemas** are added to Snowflake
- **Business logic changes** (metric definitions, calculation methods)
- **Team priorities shift** (new focus areas or KPIs)
- **Best practices emerge** from successful analyses
- **Common patterns** are identified through repeated work
- **New platforms or products** are launched

To update: Modify SKILL.md, add new reference files, or update existing documentation. Repackage the skill after changes.
