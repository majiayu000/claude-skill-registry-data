---
name: cost-report
description: Tracks and reports API costs for OpenAI, Stripe, and other paid services used by edge functions. This skill should be used when monitoring API spending, identifying cost optimization opportunities, tracking costs by feature, or setting up cost alerts.
---

# Cost Report

This skill provides visibility into API costs across edge functions, helping track spending and identify optimization opportunities.

## When to Use This Skill

- Reviewing weekly/monthly API costs
- Identifying expensive operations
- Tracking cost trends over time
- Finding optimization opportunities
- Setting up cost alerts

## Tracked Services

### OpenAI (Primary Cost Driver)

| Function | Model | Est. Cost/Request | Usage |
|----------|-------|-------------------|-------|
| chat-orchestrator | GPT-4 | ~$0.10 | AI chatbot responses |
| mandate-matcher | ada-002 | ~$0.015 | Embedding search |
| vector-search | ada-002 | ~$0.002 | Similarity search |
| comps-generator | GPT-4 | ~$0.05 | Hollywood comps |
| format-fit-engine | GPT-3.5 | ~$0.01 | Format analysis |
| regenerate-embeddings | ada-002 | ~$0.0001 | Batch embeddings |

### Stripe

| Function | Cost | Usage |
|----------|------|-------|
| stripe-webhook | $0 | Event processing |
| create-checkout-session | $0 | Session creation |
| Stripe fees | 2.9% + $0.30 | Per transaction |

### Resend (Email)

| Function | Cost | Usage |
|----------|------|-------|
| send-email | ~$0.001 | Per email sent |
| send-approval-email | ~$0.001 | Admin notifications |

## Commands

```
/cost-report                           # Current month summary
/cost-report --period=weekly           # Weekly breakdown
/cost-report --period=daily            # Daily breakdown
/cost-report --function=chat-orchestrator  # Specific function
/cost-report --compare                 # Compare to previous period
/cost-report --forecast                # Project end-of-month costs
```

## Cost Tracking Methods

### Method 1: OpenAI Dashboard

Direct access to usage and costs:

1. Go to https://platform.openai.com/usage
2. Filter by date range
3. Export as CSV for detailed analysis

### Method 2: Database Logging

If logging is enabled, query from database:

```sql
-- Estimate costs from chat messages (if logged)
SELECT
  DATE(created_at) as date,
  COUNT(*) as requests,
  COUNT(*) * 0.10 as estimated_cost_usd
FROM chat_messages
WHERE role = 'assistant'
  AND created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Method 3: Edge Function Logs

Parse costs from function responses:

```bash
# Get recent function invocations
npx supabase functions logs chat-orchestrator --scroll 2>&1 | \
  grep "estimated_cost" | \
  tail -100
```

## Cost Analysis

### By Function (Typical Monthly Breakdown)

```
## Monthly Cost Estimate

| Function | Requests | Cost/Req | Total | % |
|----------|----------|----------|-------|---|
| chat-orchestrator | 500 | $0.10 | $50.00 | 65% |
| mandate-matcher | 1,000 | $0.015 | $15.00 | 19% |
| comps-generator | 200 | $0.05 | $10.00 | 13% |
| regenerate-embeddings | 500 | $0.0001 | $0.05 | 0% |
| Other | - | - | $2.00 | 3% |
|----------|----------|----------|-------|---|
| **TOTAL** | | | **$77.05** | |
```

### By Feature

```
## Cost by Feature

| Feature | Functions Used | Monthly Cost |
|---------|----------------|--------------|
| AI Chatbot | chat-orchestrator, vector-search | ~$52 |
| Mandate Matcher | mandate-matcher | ~$15 |
| Comps Generator | comps-generator | ~$10 |
| Embeddings | regenerate-embeddings | ~$0.50 |
```

### Cost Drivers

**Highest cost factors**:

1. **GPT-4 usage** in chat-orchestrator (~65% of costs)
2. **Search volume** for mandate-matcher
3. **Comps generation** frequency

## Cost Optimization Opportunities

### 1. Semantic Query Cache (Implemented)

The `search-cache` system reduces repeat queries:

```sql
-- Check cache hit rate
SELECT
  feature,
  COUNT(*) as total_queries,
  COUNT(*) FILTER (WHERE cache_hit) as cache_hits,
  ROUND(100.0 * COUNT(*) FILTER (WHERE cache_hit) / COUNT(*), 1) as hit_rate_pct
FROM search_cache_queries
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY feature;
```

**Expected savings**: 40-70% reduction in OpenAI costs

### 2. Model Downgrade Options

Consider for less critical functions:

| Current | Alternative | Savings |
|---------|-------------|---------|
| GPT-4 | GPT-4 Turbo | ~30% |
| GPT-4 | GPT-3.5 Turbo | ~95% |
| ada-002 | (no alternative) | - |

### 3. Request Batching

Batch embedding regeneration:
- Current: Individual API calls
- Optimized: Batch of 100 at once
- Savings: ~20% reduction in overhead

### 4. Response Caching

Cache common chatbot responses:
- FAQ-style queries
- Repeated title lookups
- Standard explanations

## Alerts and Monitoring

### Cost Alert Thresholds

Set alerts for unusual spending:

```javascript
const ALERT_THRESHOLDS = {
  daily: 10,     // Alert if > $10/day
  weekly: 50,    // Alert if > $50/week
  monthly: 150,  // Alert if > $150/month
  spike: 2.0     // Alert if 2x normal rate
};
```

### Monitoring Query

```sql
-- Daily cost trend (estimate)
WITH daily_costs AS (
  SELECT
    DATE(created_at) as date,
    COUNT(*) * 0.10 as chat_cost,
    -- Add other function estimates
    0 as mandate_cost
  FROM chat_messages
  WHERE role = 'assistant'
    AND created_at >= NOW() - INTERVAL '30 days'
  GROUP BY DATE(created_at)
)
SELECT
  date,
  chat_cost + mandate_cost as total_cost,
  AVG(chat_cost + mandate_cost) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as rolling_7day_avg
FROM daily_costs
ORDER BY date DESC;
```

## Report Formats

### Console Output

```
## Cost Report - December 2024

Period: Dec 1-25, 2024 (25 days)

### Summary

Total Estimated Cost: $64.25
Daily Average: $2.57
Projected Month-End: $79.50

### By Service

| Service | Cost | % of Total |
|---------|------|------------|
| OpenAI | $62.00 | 96.5% |
| Resend | $1.25 | 1.9% |
| Other | $1.00 | 1.6% |

### By Function

| Function | Requests | Cost |
|----------|----------|------|
| chat-orchestrator | 420 | $42.00 |
| mandate-matcher | 850 | $12.75 |
| comps-generator | 145 | $7.25 |

### Trends

vs Last Month: +12% ($57.25 → $64.25)
vs Last Week: -5% (trending down)

### Recommendations

1. Cache hit rate is 45% - consider warming cache
2. chat-orchestrator costs up 20% - review usage
3. Consider GPT-4 Turbo migration (est. 30% savings)
```

### Slack Notification (Weekly)

```json
{
  "text": "Weekly Cost Report",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Weekly Cost Report*\nDec 18-25, 2024"
      }
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Total Cost*\n$18.50"},
        {"type": "mrkdwn", "text": "*vs Last Week*\n-5%"},
        {"type": "mrkdwn", "text": "*Top Function*\nchat-orchestrator"},
        {"type": "mrkdwn", "text": "*Cache Hit Rate*\n48%"}
      ]
    }
  ]
}
```

## OpenAI API Key Management

### Check Current Usage

```bash
# Via OpenAI CLI (if installed)
openai api usage

# Or via dashboard
open https://platform.openai.com/usage
```

### Set Usage Limits

In OpenAI dashboard:
1. Go to Settings → Limits
2. Set monthly budget limit
3. Configure email alerts

## Stripe Cost Tracking

### Transaction Fees

```sql
-- Estimate Stripe fees from subscriptions
SELECT
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as transactions,
  SUM(amount) as gross_revenue,
  SUM(amount * 0.029 + 0.30) as stripe_fees,
  SUM(amount) - SUM(amount * 0.029 + 0.30) as net_revenue
FROM subscriptions
WHERE status = 'active'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;
```

## Best Practices

1. **Review weekly** - Catch anomalies early
2. **Set budget alerts** - In OpenAI dashboard
3. **Monitor cache hit rate** - Higher = lower costs
4. **Track by feature** - Identify expensive features
5. **Compare periods** - Understand trends

## Related Skills

- `/health-check` - Verify services are running efficiently
- `/regenerate-embeddings` - Major cost for embedding updates
- `/cache-manage` - Improve cache hit rates to reduce costs
