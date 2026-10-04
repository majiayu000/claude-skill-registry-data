---
name: health-check
description: Verifies system health across all apps, edge functions, and database connectivity. This skill should be used for quick deployment verification, debugging service issues, daily operations checks, or before/after major deployments.
---

# Health Check

This skill provides comprehensive health monitoring across all KStoryBridge services, including apps, edge functions, and database connectivity.

## When to Use This Skill

- Quick verification after deployments
- Debugging service availability issues
- Daily operations health checks
- Before/after major deployments
- Investigating user-reported issues
- Verifying staging vs production parity

## Monitored Services

### Applications (3 Apps)

| App | Local Port | Staging URL | Production URL |
|-----|------------|-------------|----------------|
| Dashboard | 8081 | dashboard-staging.kstorybridge.com | dashboard.kstorybridge.com |
| Creator | 8083 | creator-staging.kstorybridge.com | creator.kstorybridge.com |
| Website | 5173 | - | kstorybridge.com |

### Edge Functions (25 Functions)

**Auth Group** (3):
- `create-oauth-profile`
- `create-buyer-profile`
- `create-creator-profile`

**Payments Group** (6):
- `stripe-webhook`
- `creator-stripe-webhook`
- `create-checkout-session`
- `create-creator-checkout`
- `create-billing-portal`
- `cancel-subscription`

**AI Group** (6):
- `chat-orchestrator`
- `mandate-matcher`
- `vector-search`
- `comps-generator`
- `format-fit-engine`
- `regenerate-embeddings`

**Data Group** (4):
- `title-intelligence`
- `key-visuals-collector`
- `analyze-pitch-for-assets`
- `generate-asset`

**Email Group** (2):
- `send-email`
- `send-approval-email`

**Other** (4):
- `handle-new-title`
- `comp-navigator`
- `hello-world`
- `search-cache`

### Database

- Supabase PostgreSQL connectivity
- Critical table accessibility
- RLS policy verification

## Commands

```
/health-check                    # Quick check (apps + database)
/health-check --comprehensive    # All services including edge functions
/health-check --functions        # Edge functions only
/health-check --apps             # Apps only
/health-check --database         # Database only
/health-check --staging          # Check staging environment
/health-check --production       # Check production environment
```

## Health Check Workflows

### Quick Check (Default)

Fast verification of core services:

```bash
# Check apps are responding
curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/
curl -s -o /dev/null -w "%{http_code}" http://localhost:8083/
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/

# Check database connectivity
npx supabase db ping
```

### Comprehensive Check

Full system verification:

```bash
# 1. Check all apps
for app in dashboard creator website; do
  curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}/"
done

# 2. Check all edge functions
npx supabase functions list

# 3. Test critical edge functions
curl -X POST "$SUPABASE_URL/functions/v1/hello-world" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY"

# 4. Verify database tables
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM titles;"
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM user_buyers;"
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM user_creators;"
```

### Edge Function Health Test

Test individual function availability:

```bash
# Test hello-world (simplest function)
curl -X POST "$SUPABASE_URL/functions/v1/hello-world" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json"

# Test chat-orchestrator (AI function)
curl -X POST "$SUPABASE_URL/functions/v1/chat-orchestrator" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "ping", "dry_run": true}'
```

### Database Health Queries

```sql
-- Check table accessibility
SELECT
  'titles' as table_name, COUNT(*) as row_count FROM titles
UNION ALL
SELECT 'user_buyers', COUNT(*) FROM user_buyers
UNION ALL
SELECT 'user_creators', COUNT(*) FROM user_creators
UNION ALL
SELECT 'subscriptions', COUNT(*) FROM subscriptions;

-- Check embedding coverage
SELECT
  COUNT(*) as total_titles,
  COUNT(*) FILTER (WHERE combined_embedding IS NOT NULL) as with_embeddings,
  ROUND(100.0 * COUNT(*) FILTER (WHERE combined_embedding IS NOT NULL) / COUNT(*), 1) as coverage_pct
FROM titles;

-- Check recent activity
SELECT
  DATE(created_at) as date,
  COUNT(*) as new_titles
FROM titles
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

## Health Check Script

Create a comprehensive health check script:

```javascript
// scripts/health-check.js
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

const APPS = {
  dashboard: { local: 8081, staging: 'dashboard-staging.kstorybridge.com', prod: 'dashboard.kstorybridge.com' },
  creator: { local: 8083, staging: 'creator-staging.kstorybridge.com', prod: 'creator.kstorybridge.com' },
  website: { local: 5173, staging: null, prod: 'kstorybridge.com' }
};

const CRITICAL_FUNCTIONS = [
  'hello-world',           // Smoke test
  'chat-orchestrator',     // AI chatbot
  'mandate-matcher',       // Search
  'stripe-webhook',        // Payments
  'send-email'             // Notifications
];

async function checkApp(name, url) {
  try {
    const response = await fetch(url, { timeout: 5000 });
    return { name, status: response.status, ok: response.ok };
  } catch (error) {
    return { name, status: 'error', ok: false, error: error.message };
  }
}

async function checkFunction(name) {
  try {
    const response = await fetch(`${SUPABASE_URL}/functions/v1/${name}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ dry_run: true })
    });
    return { name, status: response.status, ok: response.status < 500 };
  } catch (error) {
    return { name, status: 'error', ok: false, error: error.message };
  }
}

async function runHealthCheck(options = {}) {
  console.log('🏥 Running health check...\n');

  const results = {
    apps: [],
    functions: [],
    database: null,
    summary: { total: 0, passed: 0, failed: 0 }
  };

  // Check apps
  if (!options.functionsOnly) {
    console.log('📱 Checking apps...');
    for (const [name, urls] of Object.entries(APPS)) {
      const url = options.production
        ? `https://${urls.prod}`
        : options.staging
          ? `https://${urls.staging}`
          : `http://localhost:${urls.local}`;

      if (url.includes('null')) continue;

      const result = await checkApp(name, url);
      results.apps.push(result);
      results.summary.total++;
      result.ok ? results.summary.passed++ : results.summary.failed++;

      console.log(`  ${result.ok ? '✅' : '❌'} ${name}: ${result.status}`);
    }
  }

  // Check functions
  if (!options.appsOnly && (options.comprehensive || options.functionsOnly)) {
    console.log('\n⚡ Checking edge functions...');
    for (const name of CRITICAL_FUNCTIONS) {
      const result = await checkFunction(name);
      results.functions.push(result);
      results.summary.total++;
      result.ok ? results.summary.passed++ : results.summary.failed++;

      console.log(`  ${result.ok ? '✅' : '❌'} ${name}: ${result.status}`);
    }
  }

  // Summary
  console.log('\n📊 Summary');
  console.log(`  Total checks: ${results.summary.total}`);
  console.log(`  Passed: ${results.summary.passed}`);
  console.log(`  Failed: ${results.summary.failed}`);
  console.log(`  Health: ${Math.round(100 * results.summary.passed / results.summary.total)}%`);

  return results;
}

// Run if called directly
runHealthCheck({
  comprehensive: process.argv.includes('--comprehensive'),
  staging: process.argv.includes('--staging'),
  production: process.argv.includes('--production'),
  functionsOnly: process.argv.includes('--functions'),
  appsOnly: process.argv.includes('--apps')
});
```

## Console Output

### Quick Check
```
🏥 Running health check...

📱 Checking apps...
  ✅ dashboard: 200
  ✅ creator: 200
  ✅ website: 200

📊 Summary
  Total checks: 3
  Passed: 3
  Failed: 0
  Health: 100%
```

### Comprehensive Check
```
🏥 Running health check...

📱 Checking apps...
  ✅ dashboard: 200
  ✅ creator: 200
  ✅ website: 200

⚡ Checking edge functions...
  ✅ hello-world: 200
  ✅ chat-orchestrator: 200
  ✅ mandate-matcher: 200
  ✅ stripe-webhook: 200
  ✅ send-email: 200

🗄️ Checking database...
  ✅ Connection: OK
  ✅ titles: 1,234 rows
  ✅ user_buyers: 156 rows
  ✅ user_creators: 89 rows
  ✅ Embedding coverage: 95.6%

📊 Summary
  Total checks: 13
  Passed: 13
  Failed: 0
  Health: 100%
```

### Failure Example
```
🏥 Running health check...

📱 Checking apps...
  ✅ dashboard: 200
  ❌ creator: 503
  ✅ website: 200

⚡ Checking edge functions...
  ✅ hello-world: 200
  ❌ chat-orchestrator: timeout
  ✅ mandate-matcher: 200

📊 Summary
  Total checks: 6
  Passed: 4
  Failed: 2
  Health: 67%

⚠️ Issues detected:
  - creator app: 503 Service Unavailable
  - chat-orchestrator: Request timed out (check OpenAI API key)
```

## Slack Notification

```json
{
  "text": "System Health Check",
  "attachments": [
    {
      "color": "good",
      "fields": [
        {"title": "Environment", "value": "Production", "short": true},
        {"title": "Health", "value": "100%", "short": true},
        {"title": "Apps", "value": "3/3 ✅", "short": true},
        {"title": "Functions", "value": "5/5 ✅", "short": true},
        {"title": "Database", "value": "OK", "short": true},
        {"title": "Embeddings", "value": "95.6%", "short": true}
      ]
    }
  ]
}
```

## Troubleshooting

### App Not Responding

1. Check if dev server is running:
   ```bash
   ps aux | grep "vite"
   ```

2. Check port availability:
   ```bash
   lsof -i :8081
   lsof -i :8083
   lsof -i :5173
   ```

3. Restart dev server:
   ```bash
   npm run dev:dashboard
   npm run dev:creator
   npm run dev:website
   ```

### Edge Function Failing

1. Check function logs:
   ```bash
   npx supabase functions logs [function-name] --scroll
   ```

2. Verify function is deployed:
   ```bash
   npx supabase functions list
   ```

3. Check environment secrets:
   ```bash
   npx supabase secrets list
   ```

### Database Connection Issues

1. Verify DATABASE_URL:
   ```bash
   echo $DATABASE_URL | head -c 50
   ```

2. Test direct connection:
   ```bash
   psql "$DATABASE_URL" -c "SELECT 1;"
   ```

3. Check Supabase status:
   - Visit https://status.supabase.com

## Environment Variables

Required for health checks:

```bash
# Supabase
SUPABASE_URL=https://dlrnrgcoguxlkkcitlpd.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...

# Database (for direct queries)
DATABASE_URL=postgresql://...

# App URLs (for remote checks)
DASHBOARD_URL=https://dashboard.kstorybridge.com
CREATOR_URL=https://creator.kstorybridge.com
WEBSITE_URL=https://kstorybridge.com
```

## Automation

### Scheduled Health Checks

Add to cron for regular monitoring:

```bash
# Every 5 minutes
*/5 * * * * node /path/to/scripts/health-check.js >> /var/log/health-check.log

# Daily comprehensive check
0 9 * * * node /path/to/scripts/health-check.js --comprehensive
```

### CI/CD Integration

Run health check after deployments:

```yaml
# .github/workflows/deploy.yml
- name: Health Check
  run: |
    npm run health-check -- --production
    if [ $? -ne 0 ]; then
      echo "Health check failed!"
      exit 1
    fi
```

## Related Skills

- `/deploy-staging` - Deploy before running health checks
- `/deploy-functions` - Deploy functions if health check fails
- `/cost-report` - Check API costs alongside health
- `/test-e2e` - Full end-to-end testing after health verification
