---
name: bankr-error-handling
description: >
  Self-healing diagnostics for Bankr API errors.
  Handles 401s, timeouts, rate limits, and configuration issues.
  Source: https://github.com/BankrBot/claude-plugins
  NOTE: Replace this placeholder with actual skill from BankrBot repo.
---

# Bankr Error Handling — Self-Healing API Diagnostics

## Source

Install from: `https://github.com/BankrBot/claude-plugins`
Path: `bankr-error-handling/`

## Setup

```bash
git clone https://github.com/BankrBot/claude-plugins.git /tmp/bankr-plugins
cp -r /tmp/bankr-plugins/bankr-error-handling/* ./
rm -rf /tmp/bankr-plugins
```

## When to Use

- HTTP 401 from Bankr API
- "Invalid API key" errors
- Job failures or timeouts
- Rate limit (429) responses
- Any BANKR_API_KEY configuration issues

## Self-Healing Flow

```
Bankr API error detected
  ↓
1. Check BANKR_API_KEY is set and starts with bk_
2. Verify api.bankr.bot is reachable (curl -I)
3. Check rate limit status (100 msg/day standard)
4. If rate-limited: wait + retry after reset
5. If auth error: alert Ogie — key may need rotation
6. If network error: retry with exponential backoff (3 attempts)
7. If all fail: alert Ogie on Telegram with diagnostic report
```

## Integration

- SafetyAgent uses this for Bankr-related checks
- DeployAgent uses this for deploy execution errors
- Auto-retry with backoff before alerting Ogie
