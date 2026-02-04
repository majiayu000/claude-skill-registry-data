---
skill_id: error_handling_protocols
name: Error Handling Protocols
version: 1.0.0
description: Standard protocols for handling errors, API failures, and infrastructure issues
author: Trading System CTO
tags: [error-handling, reliability, api-failures, infrastructure]
---

# Error Handling Protocols

Standard protocols for handling errors, API failures, and infrastructure issues in the trading system.

## API Failure Handling

### Data Source Failures

**Priority Order** (fail fast, use reliable sources first):
1. Try Alpaca API (most reliable)
2. Try Polygon.io (reliable paid source)
3. Use cached data (if < 24 hours old)
4. Try yfinance (unreliable free source)
5. Skip Alpha Vantage if rate-limited (fail fast)

### Timeout Handling

- **Alpha Vantage**: Max 90 seconds total (fail fast)
- **yfinance**: 30-second timeout per request
- **Alpaca**: 60-second timeout per request
- **Polygon.io**: 30-second timeout per request

### Rate Limit Handling

- **Alpha Vantage**: Skip immediately if rate-limited (don't retry)
- **yfinance**: Exponential backoff (2s, 4s, 8s)
- **Alpaca**: Respect rate limits, use retry logic
- **Polygon.io**: Respect rate limits, use retry logic

## Workflow Failure Handling

### GitHub Actions Failures

1. **Detect failure**: Check workflow status
2. **Capture error**: Log to Sentry (if configured)
3. **Fallback**: Use cached data if available
4. **Alert**: Notify via logs (future: Slack/email)
5. **Recovery**: Manual performance log update script available

### Trading Execution Failures

1. **Pre-trade validation**: Check all circuit breakers
2. **API failures**: Retry with exponential backoff
3. **Order failures**: Log and continue (don't halt system)
4. **Data failures**: Use cached data, skip day if necessary

## Error Monitoring

### Sentry Integration

- **Automatic**: Captures exceptions and errors
- **Context**: Adds trading-specific context
- **GitHub Actions**: Includes workflow context
- **Optional**: Fails gracefully if not configured

### Logging Standards

- **ERROR**: Critical failures requiring attention
- **WARNING**: Degraded functionality (fallbacks used)
- **INFO**: Normal operations and decisions
- **DEBUG**: Detailed execution traces

## Graceful Degradation

### When Data Sources Fail

1. **Try reliable sources first** (Alpaca, Polygon)
2. **Use cached data** if available (< 24 hours old)
3. **Skip unreliable sources** (yfinance, Alpha Vantage)
4. **Skip trading day** if no data available (better than bad data)

### When Workflow Fails

1. **Manual recovery**: `scripts/update_performance_log.py`
2. **Next run**: Will use latest code (fixes applied)
3. **Monitoring**: Sentry tracks failures for analysis

## Best Practices

- **Fail fast**: Don't wait 10+ minutes for rate-limited APIs
- **Use reliable sources**: Prioritize paid APIs over free ones
- **Cache aggressively**: Use cached data when APIs fail
- **Monitor proactively**: Sentry detects issues before they cascade
- **Document failures**: Log all failures for analysis

## Integration

These protocols are enforced in:
- `src/utils/market_data.py` (data source priority)
- `src/utils/error_monitoring.py` (Sentry integration)
- `.github/workflows/daily-trading.yml` (workflow error handling)
