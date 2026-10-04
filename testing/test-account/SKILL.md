---
name: test-account
version: 1.0.0
description: |
  Test account credentials for automated QA testing. Provides a suite-tier buyer
  account for browser-based testing of authenticated features. Use this skill
  before any QA, browse, or design-review session that requires sign-in.
  Trigger: before signing into the dashboard app during automated testing.
allowed-tools:
  - Bash
  - Read
---

# Test Account for Automated QA

## Dashboard (Buyer) Test Account

| Field    | Value                           |
|----------|---------------------------------|
| Email    | `claudetest@kstorybridge.com`   |
| Password | `ClaudeTest2026!`               |
| Tier     | `suite` (full access)           |
| Role     | `producer`                      |
| Company  | `KStoryBridge QA`               |
| Auth ID  | `81e1f29a-da1e-4a1d-8ffe-fd9b4ebc1237` |

## Usage

### Browser sign-in (Playwright)

1. Navigate to the sign-in page (`/signin`)
2. Fill email: `claudetest@kstorybridge.com`
3. Fill password: `ClaudeTest2026!`
4. Click "Sign In"
5. Wait for redirect to `/buyers/home` or the target page

### Programmatic sign-in (API)

```bash
curl -s -X POST "https://dlrnrgcoguxlkkcitlpd.supabase.co/auth/v1/token?grant_type=password" \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "claudetest@kstorybridge.com", "password": "ClaudeTest2026!"}'
```

## Environment URLs

| App       | Local                | Staging                              |
|-----------|----------------------|--------------------------------------|
| Dashboard | http://localhost:8081 | https://dashboard-staging.kstorybridge.com |
| Creator   | http://localhost:8083 | https://creator-staging.kstorybridge.com   |

Note: Dev server port may vary (8081 or 8082). Check the Vite output for the actual port.

## Important Notes

- This is a **suite-tier** account with full access to all features
- Do NOT use this account for destructive operations (deleting titles, etc.)
- Do NOT change the password or tier — other automated processes depend on it
- If sign-in fails, verify the account still exists:
  ```bash
  curl -s "https://dlrnrgcoguxlkkcitlpd.supabase.co/rest/v1/user_buyers?email=eq.claudetest@kstorybridge.com&select=email,tier" \
    -H "apikey: <ANON_KEY>" -H "Authorization: Bearer <ANON_KEY>"
  ```
