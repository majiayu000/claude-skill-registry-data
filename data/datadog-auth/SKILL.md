---
name: datadog-auth
description: Troubleshoot Datadog API authentication issues (401/403 errors), understand API keys vs app keys, and configure correct regions. Use when hitting auth errors or setting up Datadog API access.
---

# Datadog API Authentication

## TL;DR

- Most v2 endpoints require **two headers**:
  - `DD-API-KEY` — org-scoped API key (32 hex chars)
  - `DD-APPLICATION-KEY` — application key VALUE (secret; 40 hex chars)
- Do **not** send key IDs (UUIDs) in headers. Always send the key **values** (secrets).
- Pick the correct region/site (e.g., `us3.datadoghq.com`) so the base is `https://api.<DD_SITE>`.
- Some APIs (including Incidents v2) do not support scoped app keys. Use an unscoped app key.

## Terms at a Glance

| Item | Example | Use in requests |
| --- | --- | --- |
| API key (value) | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` (32 hex) | Header `DD-API-KEY` |
| Application key (value, secret) | `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` (40 hex) | Header `DD-APPLICATION-KEY` |
| API key ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (UUID) | **Not for auth** |
| Application key ID | `yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy` (UUID) | **Not for auth** |

## Regions / Sites

| Region | API Base |
| --- | --- |
| US1 | `https://api.datadoghq.com` |
| US3 | `https://api.us3.datadoghq.com` |
| US5 | `https://api.us5.datadoghq.com` |
| EU1 | `https://api.datadoghq.eu` |
| AP1 | `https://api.ap1.datadoghq.com` |
| AP2 | `https://api.ap2.datadoghq.com` |

## Quick Validation

```bash
# Test API key only (no app key needed)
curl -sS -H "DD-API-KEY: $DD_API_KEY" https://api.$DD_SITE/api/v1/validate

# Or use the CLI
dd validate
```

## Common Errors

| HTTP | Symptom | Likely cause | Fix |
| --- | --- | --- | --- |
| 401 | `Unauthorized` | Wrong app key value, wrong site/org, using key ID instead of value | Use the secret value, verify region |
| 403 | `scoped app keys not supported` | Using a scoped app key | Use an unscoped app key |
| 403 | Generic | Missing permission on owner's role | Adjust role permissions |

## Troubleshooting Checklist

1. **API key valid?** Run `dd validate`
2. **Region mismatch?** Check which site returns 200:
   ```bash
   for site in us3.datadoghq.com datadoghq.com datadoghq.eu; do
     code=$(curl -s -o /dev/null -w "%{http_code}" -H "DD-API-KEY: $DD_API_KEY" "https://api.$site/api/v1/validate")
     echo "$site -> $code"
   done
   ```
3. **Copy/paste artifacts?** Strip whitespace:
   ```bash
   export DD_APP_KEY="$(printf %s "$DD_APP_KEY" | tr -d '\r\n')"
   ```

## Scoped vs Unscoped Application Keys

- **Unscoped**: inherits permissions from its owner. Use when API doesn't support scoped keys.
- **Scoped**: limited to listed scopes. Use for least privilege when supported.

If you see "This API does not support scoped app keys," use an unscoped app key.

## References

- [Datadog API Authentication](https://docs.datadoghq.com/account_management/api-app-keys/)
- [Incidents API](https://docs.datadoghq.com/api/latest/incidents/)
