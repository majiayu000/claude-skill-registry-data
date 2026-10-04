---
name: deploy-functions
description: Deploys Supabase edge functions individually or in groups (auth, payments, ai, data, email) with health verification and notifications. This skill should be used when deploying edge functions to Supabase, updating serverless functions, or batch deploying multiple functions.
---

# Deploy Functions

This skill automates the deployment of Supabase edge functions with grouping, health checks, and comprehensive reporting.

## When to Use This Skill

- Deploying a single edge function after changes
- Batch deploying related functions (e.g., all payment functions)
- Deploying all functions after major updates
- Verifying function health after deployment

## Function Groups

Functions are organized into logical groups for batch deployment:

### auth (3 functions)
- `create-oauth-profile` - OAuth user onboarding
- `create-buyer-profile` - Buyer signup
- `create-creator-profile` - Creator signup

### payments (6 functions)
- `stripe-webhook` - Main Stripe event handler
- `creator-stripe-webhook` - Creator payment events
- `create-checkout-session` - Buyer checkout
- `create-creator-checkout` - Creator checkout
- `create-billing-portal` - Stripe portal redirect
- `cancel-subscription` - Subscription cancellation

### ai (6 functions)
- `chat-orchestrator` - AI chatbot orchestration (GPT-4 + vector search)
- `mandate-matcher` - Producer mandate matching
- `vector-search` - Raw vector similarity search
- `comps-generator` - Hollywood comps generation
- `format-fit-engine` - Format analysis
- `regenerate-embeddings` - Embedding regeneration

### data (4 functions)
- `title-intelligence` - Platform data scraping
- `key-visuals-collector` - Visual metadata extraction
- `analyze-pitch-for-assets` - Pitch analysis
- `generate-asset` - Marketing asset generation

### email (2 functions)
- `send-email` - Unified email sender (Resend API)
- `send-approval-email` - Admin approval notifications

### billing (2 functions)
- `get-creator-billing-history` - Creator subscription history
- `cancel-subscription` - Subscription cancellation

## Commands

```
/deploy-functions chat-orchestrator           # Deploy single function
/deploy-functions --group=auth                # Deploy all auth functions
/deploy-functions --group=payments            # Deploy all payment functions
/deploy-functions --group=ai                  # Deploy all AI functions
/deploy-functions --all                       # Deploy ALL functions
/deploy-functions --all --skip-health         # Skip health checks
```

## Deployment Workflow

### Step 1: Pre-deployment Validation

Before deploying, verify requirements:

```bash
# Check Supabase CLI is available
npx supabase --version

# Verify function exists
ls supabase/functions/[function-name]/

# Check for required secrets (if function uses them)
# Note: Secrets are managed via Supabase dashboard
```

### Step 2: Deploy Function(s)

Deploy using Supabase CLI:

```bash
# Single function
npx supabase functions deploy [function-name]

# Multiple functions (run sequentially)
npx supabase functions deploy create-oauth-profile
npx supabase functions deploy create-buyer-profile
npx supabase functions deploy create-creator-profile
```

Capture output for each deployment:
- Deployment URL
- Version number
- Any warnings

### Step 3: Health Verification (unless --skip-health)

Verify each deployed function is responding:

```bash
# Get project URL
SUPABASE_URL="https://dlrnrgcoguxlkkcitlpd.supabase.co"

# Check function endpoint (OPTIONS request for CORS)
curl -s -o /dev/null -w "%{http_code}" \
  -X OPTIONS \
  "$SUPABASE_URL/functions/v1/[function-name]"
```

Expected responses:
- 200/204: Function is healthy
- 401: Function requires auth (expected for most functions)
- 500: Function has an error (investigate)

For functions that bypass JWT (webhooks):
```bash
# stripe-webhook should return 400 (missing body) not 500
curl -s -o /dev/null -w "%{http_code}" \
  -X POST \
  "$SUPABASE_URL/functions/v1/stripe-webhook"
```

### Step 4: Report Results

Generate deployment summary:

```
## Edge Function Deployment Summary

**Deployed**: 3 functions (auth group)
**Time**: 2024-12-25 14:30 UTC

### Functions Deployed

| Function | Status | Health | Time |
|----------|--------|--------|------|
| create-oauth-profile | SUCCESS | HEALTHY | 8s |
| create-buyer-profile | SUCCESS | HEALTHY | 7s |
| create-creator-profile | SUCCESS | HEALTHY | 9s |

### Endpoints

All functions available at:
https://dlrnrgcoguxlkkcitlpd.supabase.co/functions/v1/[function-name]

### Notes
- All functions deployed successfully
- Health checks passed
- No secrets needed updating
```

## Function-Specific Notes

### JWT-Bypassed Functions

These functions verify auth differently (e.g., Stripe signature):

```toml
# From supabase/config.toml
[functions.stripe-webhook]
verify_jwt = false

[functions.creator-stripe-webhook]
verify_jwt = false

[functions.mandate-matcher]
verify_jwt = false
```

### Large Functions

These functions may take longer to deploy:

| Function | Size | Deploy Time |
|----------|------|-------------|
| chat-orchestrator | 3,328 lines | ~15s |
| stripe-webhook | 989 lines | ~10s |
| title-intelligence | 804 lines | ~10s |

### Shared Dependencies

Functions using `_shared/` utilities:
- All AI functions use `_shared/intent-detection.ts`
- Payment functions use `_shared/stripe-config.ts`
- Search functions use `_shared/search-cache.ts`

When updating shared code, redeploy all dependent functions.

## Environment Secrets

Required secrets for functions (set in Supabase dashboard):

| Secret | Used By | Required |
|--------|---------|----------|
| OPENAI_API_KEY | AI functions | Yes |
| STRIPE_SECRET_KEY | Payment functions | Yes |
| STRIPE_WEBHOOK_SECRET | stripe-webhook | Yes |
| RESEND_API_KEY | email functions | Yes |
| SUPABASE_SERVICE_ROLE_KEY | All functions | Auto-set |

To check if secrets are set:
```bash
# Via Supabase dashboard or CLI
npx supabase secrets list
```

## Error Handling

### Deployment Failures

If deployment fails:

1. Check the error message:
   - "Function not found" - Verify path exists
   - "Build failed" - Check TypeScript errors in function
   - "Network error" - Check internet/Supabase status

2. Try deploying with verbose output:
   ```bash
   npx supabase functions deploy [function] --debug
   ```

3. Check function logs after failed invocation:
   ```bash
   npx supabase functions logs [function] --scroll
   ```

### Health Check Failures

If health check fails but deployment succeeded:

1. Function may need secrets - check Supabase dashboard
2. Function may have runtime error - check logs:
   ```bash
   npx supabase functions logs [function]
   ```
3. Function may need warm-up - try again in 30 seconds

## Notification Channels

### Console Output

Show progress for each function:

```
Deploying edge functions...

[1/3] create-oauth-profile
      Deploying... done (8s)
      Health check... PASS

[2/3] create-buyer-profile
      Deploying... done (7s)
      Health check... PASS

[3/3] create-creator-profile
      Deploying... done (9s)
      Health check... PASS

All 3 functions deployed successfully!
```

### Slack Notification

```json
{
  "text": "Edge Functions Deployed",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Edge Functions Deployed*\nGroup: auth\nFunctions: 3\nStatus: All healthy"
      }
    }
  ]
}
```

### GitHub PR Comment

If deploying as part of a PR workflow:

```markdown
## Edge Functions Deployment

Deployed 3 functions from `auth` group:
- create-oauth-profile
- create-buyer-profile
- create-creator-profile

All health checks passed.
```

## Tips

- Deploy related functions together to avoid version mismatches
- Use `--skip-health` during rapid iteration, but verify before production
- After updating `_shared/` code, redeploy all dependent functions
- Check Supabase dashboard for detailed logs if issues occur
- Functions cold-start on first invocation - health check may be slow

## Related Skills

- `/deploy-staging` - Deploy apps to Vercel staging
- `/safe-migrate` - Run database migrations safely
- `/health-check` - Comprehensive system health monitoring
