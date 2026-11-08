---
name: windsor-ai
description: Connect to Windsor.ai MCP for natural language access to 325+  data sources including Facebook Ads, GA4, HubSpot, Shopify, and more.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["mcporter","npx","node"],"env":["WINDSOR_API_KEY"]}},"openclaw":{"primaryEnv":"WINDSOR_API_KEY"}}
---

# Windsor.ai Analytics

Use this skill to query, explore, and analyze your [Windsor.ai](https://windsor.ai) connected and business data using natural language. Windsor.ai aggregates data from 325+ platforms: Facebook Ads, Google Analytics 4, HubSpot, Shopify, TikTok Ads, Salesforce, and hundreds more and exposes it through a single MCP interface.

## When to Use This Skill

Invoke this skill automatically when the user asks questions about:
- Campaign performance, ROAS, CPM, CPC, CTR
- Ad spend breakdowns or budget analysis across channels
- Sales pipeline, CRM data, or customer acquisition metrics
- E-commerce performance (revenue, conversion rates, AOV)
- Cross channel attribution or multi touch analytics
- Trend analysis over specific date ranges
- Data from any connected advertising, analytics, or CRM platform

The user can also invoke this skill directly with `/windsor-ai`.

## Setup

Before querying data, the Windsor.ai MCP connection must be configured. Follow these steps once:

### Step 1: Get Your Windsor.ai API Key

1. Log in to your Windsor.ai account at https://windsor.ai
2. Navigate to your account dashboard or settings
3. Locate the API Key section and copy your key

### Step 2: Store the API Key

Add your API key to the clawdbot environment file:

```bash
echo 'WINDSOR_API_KEY=your_api_key_here' >> ~/.clawdbot/.env
```

Replace `your_api_key_here` with the key you copied.

Then export it for your current session so mcporter can resolve it:

```bash
export WINDSOR_API_KEY=your_api_key_here
```

> **Note:** mcporter requires `WINDSOR_API_KEY` to be exported as a shell environment variable. Simply storing it in `~/.clawdbot/.env` is not enough — it must be available in your active shell session.
>
> **Security note:** Avoid appending the key to `~/.zshrc` or other shell rc files, as this stores your secret in plaintext and loads it into every shell session. Prefer your system keychain, a secrets manager, or a `.env` file with restricted permissions (`chmod 600 ~/.clawdbot/.env`). If you do add it to your shell rc file, remove it once no longer needed.

### Step 3: Configure mcporter

Add Windsor.ai to your mcporter configuration. Open or create `config/mcporter.json` in your project and add the following inside the `mcpServers` object:

```json
{
  "mcpServers": {
    "windsor-ai": {
      "description": "Windsor.ai MCP — natural language access to 325+  data sources.",
      "baseUrl": "https://mcp.windsor.ai/sse",
      "headers": {
        "Authorization": "Bearer ${WINDSOR_API_KEY}"
      }
    }
  }
}
```

If `mcpServers` already has other entries, add the `windsor-ai` block alongside them.

### Step 4: Verify Connection

```bash
npx mcporter list
```

You should see `windsor-ai` listed with its available tools. If you see an authentication error, confirm that `WINDSOR_API_KEY` is correctly set in `~/.clawdbot/.env`.

## Data Source Discovery

Before querying, explore which data sources are active in your Windsor.ai account:

- **List connected sources:** "What data sources do I have connected in Windsor.ai?"
- **Inspect available fields:** "What fields and metrics are available from my Facebook Ads data in Windsor?"
- **Check date coverage:** "What is the earliest date I have data for in Google Analytics 4?"
- **Discover account structure:** "Show me all ad accounts connected to Windsor.ai and their IDs."

Windsor MCP introspects your account's active connectors and returns only what is available. Only sources you have connected in your Windsor.ai dashboard will be queryable.

## Usage

Query your  data using plain English. Windsor MCP translates your questions into structured data queries against your connected sources.

### How to Frame Queries

For best results, always include:
- **The data source** — or ask Windsor to query across all connected sources
- **The metric(s)** — spend, ROAS, clicks, conversions, revenue, CPC, CTR, etc.
- **The time period** — "last 7 days", "last month", "Q1 2025", "year to date"
- **Any segmentation** — by campaign, channel, country, device, ad set, etc.

### Query Patterns

**Single source, single metric:**
"What was my total Facebook Ads spend last week?"

**Cross-channel comparison:**
"Compare spend and ROAS across Facebook Ads, Google Ads, and TikTok Ads for the last 30 days."

**Segmented breakdown:**
"Break down my Google Ads performance by campaign for March 2025, showing impressions, clicks, conversions, and cost per conversion."

**Trend over time:**
"Show me the trend in CPC and CTR for my Facebook Ads campaigns over the past 90 days."

**Top/bottom performers:**
"What were my top 5 best performing campaigns by ROAS last month? And the bottom 5?"

**Anomaly detection:**
"Which of my campaigns had an unusual spike or drop in performance last week?"

## Report Generation

Windsor MCP provides the underlying data; Claude assembles it into structured reports. Use these templates:

### Weekly Performance Report

Ask: "Generate a weekly  performance report for [date range] covering all connected channels."

Claude will structure the report as:
1. **Executive Summary** — total spend, total conversions, blended ROAS, week-over-week change
2. **Channel Breakdown** — spend and key metrics per connected ad platform
3. **Top Campaigns** — top 3 by spend and top 3 by ROAS
4. **Anomalies & Alerts** — campaigns that exceeded or undershot typical performance by more than 20%
5. **Recommendations** — budget reallocation suggestions based on channel ROAS

### Monthly Performance Report

Ask: "Generate a monthly  performance report for [month/year] across all connected sources."

Claude will structure the report as:
1. **Month-over-Month Summary** — key KPIs vs. prior month with percentage changes
2. **Channel Performance Table** — impressions, clicks, spend, conversions, CPA, ROAS per channel
3. **Campaign Highlights** — top 5 campaigns by revenue contribution
4. **Audience & Creative Insights** — top performing audiences or creatives (if social ad data is connected)
5. **Budget Pacing** — actual spend vs. planned budget per channel
6. **30-Day Outlook** — projected performance if spend holds constant based on trailing trends

### Client Ready Report

Ask: "Generate a client ready performance report for [account/brand] for [date range]. Include an executive summary, channel breakdown, top campaigns, and key recommendations. Format it as a professional document."

## Example Queries

**Campaign performance:**
- "What campaigns had the best ROAS last month across all channels?"
- "Which ad campaigns are wasting budget high spend, low conversions?"
- "How did my Black Friday campaign perform compared to last year?"

**Spend analysis:**
- "Give me a breakdown of total ad spend by channel over the past 90 days."
- "How much have I spent on Facebook Ads vs. Google Ads year to date?"
- "What is my average daily spend across all connected ad platforms this month?"

**Audience and creative:**
- "Which audience segments are converting best on Facebook Ads?"
- "What ad creative formats (image vs. video) are driving more conversions on TikTok?"

**E-commerce (requires Shopify or similar connector):**
- "What is my revenue from paid traffic vs. organic traffic this month?"
- "Which product categories have the highest conversion rate from Google Ads?"
- "Show me my customer acquisition cost broken down by traffic source."

**CRM and pipeline (requires HubSpot, Salesforce, or similar):**
- "How many leads did my  campaigns generate last quarter?"
- "What is the average deal size for leads that came through paid social?"

**Trend and forecasting:**
- "Show me the trend in my blended ROAS over the last 6 months."
- "Based on current spend trends, what will my monthly ad spend be at end of quarter?"

**Cross channel attribution:**
- "Which channels are contributing most to first touch conversions vs. last touch?"
- "How does my Facebook Ads attributed revenue compare to GA4 attributed revenue?"

## Troubleshooting

**Authentication failed / 401 error:**
- Verify `WINDSOR_API_KEY` is set in `~/.clawdbot/.env`
- Confirm the key is correct in your Windsor.ai dashboard
- Restart mcporter after updating the env file

**Failed to resolve header 'Authorization' / WINDSOR_API_KEY must be set:**
- mcporter requires the variable to be exported in your shell, not just stored in `.env`
- Run: `export WINDSOR_API_KEY=your_api_key_here && npx mcporter list`
- To load from your `.env` file: `export $(grep -v '^#' ~/.clawdbot/.env | xargs) && npx mcporter list`

**No data sources found:**
- You must connect at least one data source in your Windsor.ai dashboard before querying
- Visit https://windsor.ai to connect your ad platforms or analytics tools

**Data is not up to date:**
- Windsor.ai syncs on a schedule; freshness depends on your plan and connector
- Check the last sync time per connector in your Windsor.ai dashboard

**Tool list is empty after `npx mcporter list`:**
- Ensure `config/mcporter.json` contains the `windsor-ai` entry exactly as shown in Setup Step 3
- Confirm `WINDSOR_API_KEY` is a non-empty string in your environment
