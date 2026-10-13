---
name: cost-optimizer
description: Identifies cloud cost issues, unused resources, and billing optimization opportunities. Use when the user asks about "costs", "billing", "AWS invoice", "cloud spending", "reduce costs", or "optimize resources". Don't use for monitoring setup, deployment, or security.
---

# Cost Optimizer

Helps identify and reduce cloud infrastructure costs — especially for solo founders who may not realize what they're paying for.

## How It Works

1. Identify cloud services in use
2. Check for common cost traps
3. Detect unused or oversized resources
4. Suggest optimization strategies
5. Recommend cost monitoring tools

## Step-by-Step Procedure

### Step 1: Identify Cloud Services
Check for configuration files:
- `vercel.json` → Vercel (check plan tier)
- `serverless.yml` / `cdk.json` → AWS
- `railway.toml` → Railway
- `fly.toml` → Fly.io
- `docker-compose.yml` → Self-hosted
- `supabase/` → Supabase
- `firebase.json` → Firebase

### Step 2: Common Cost Traps

**AWS:**
- EC2 instances running 24/7 that could be serverless
- RDS instances with multi-AZ when not needed
- S3 buckets without lifecycle policies
- CloudWatch logs with no retention policy
- NAT Gateways (very expensive, often unnecessary for simple apps)
- Elastic IPs not attached to instances

**Vercel:**
- Functions running on Edge when Node.js runtime is cheaper
- Image optimization on high-traffic pages
- Analytics tier vs. free tier

**General:**
- Database connections left open
- Background workers running with no work
- CI/CD pipelines running on every push (vs. only PRs)

### Step 3: Detect in Code
```bash
# Check for cloud SDK usage
grep -rn "aws-sdk\|@aws-sdk\|boto3\|firebase\|supabase" --include="*.ts" --include="*.js" --include="*.py" . | head -20
```

### Step 4: Recommend Cost Monitoring
- **AWS**: Enable AWS Cost Explorer + Budget Alerts
- **Vercel**: Check usage dashboard monthly
- **General**: Set up billing alerts at 50%, 80%, 100% of expected budget

### Step 5: Quick Wins
Present a prioritized list of cost savings, estimated monthly impact, and effort to implement.

## Output Format
```markdown
## 💰 Cost Optimization Report

### Detected Services
- {service}: {estimated tier/cost}

### Quick Wins
1. {action} — est. savings: ${X}/mo — effort: {low/medium/high}

### Cost Monitoring Setup
- {recommended tool}: {how to set up}
```
