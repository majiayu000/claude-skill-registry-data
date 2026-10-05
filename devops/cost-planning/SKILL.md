---
name: cost-planning
description: Plan and optimize infrastructure costs for solo developers and small teams. Use for cloud cost estimation, choosing cost-effective architectures, setting up billing alerts, comparing hosting options, and optimizing for bootstrap/side-project budgets.
---

# Cost Planning

Make informed infrastructure decisions that balance capability with budget.

## Cost-Conscious Mindset

### Solo/Bootstrap Priorities
1. **Start free** - Use free tiers aggressively
2. **Pay for value** - Only upgrade when free limits hurt
3. **Avoid lock-in** - Prefer portable solutions
4. **Right-size** - Don't over-provision "just in case"
5. **Monitor early** - Set billing alerts before you need them

### Cost vs Time Trade-off
```
Cheap but manual     vs    Expensive but automated
─────────────────────────────────────────────────
Self-hosted DB            Managed database
Manual deployments        CI/CD platform
DIY monitoring            SaaS observability

Rule: Automate only when manual becomes painful.
Your time has value, but cash constraints are real.
```

## Free Tier Strategies

### Compute
| Provider | Free Tier |
|----------|-----------|
| Fly.io | 3 shared VMs, 3GB storage |
| Railway | $5/month credit |
| Render | Static sites, 750 hours/month |
| Vercel | Unlimited static, 100GB bandwidth |
| Cloudflare Workers | 100k requests/day |

### Database
| Provider | Free Tier |
|----------|-----------|
| Supabase | 500MB, 2 projects |
| PlanetScale | 5GB, 1B row reads |
| Neon | 512MB, unlimited projects |
| MongoDB Atlas | 512MB shared |
| Turso | 9GB, 500M rows read |

### Other Services
| Service | Free Tier |
|---------|-----------|
| Cloudflare | DNS, CDN, basic DDoS |
| Sentry | 5k errors/month |
| PostHog | 1M events/month |
| Resend | 3k emails/month |
| Upstash | 10k requests/day Redis |

## Cost Estimation

### Monthly Cost Template
```markdown
## Infrastructure Budget: [Project Name]

### Compute
- Web server: $X/month
- Background workers: $X/month
- Serverless functions: $X/month

### Data
- Database: $X/month
- Object storage: $X/month
- Redis/cache: $X/month

### Services
- Email: $X/month
- Error tracking: $X/month
- Analytics: $X/month

### Operations
- Domain: $X/year ÷ 12 = $X/month
- SSL: $0 (Let's Encrypt)

### Total: $X/month
### With 2x buffer: $X/month
```

### Scaling Cost Projection
```
Users    Requests/mo    Est. Cost
─────────────────────────────────
100      10k            Free tier
1,000    100k           $20-50
10,000   1M             $100-200
100,000  10M            $500-1000

Note: Costs vary wildly by architecture.
These are rough estimates for typical web apps.
```

## Architecture for Cost

### Cheap Patterns
```
Static-first
- SSG/SSR to static files
- CDN-served (often free)
- API only for dynamic data

SQLite + Litestream
- Single-file database
- Replicated to S3 ($0.023/GB)
- No managed DB costs

Serverless for bursty
- Pay per request
- Scale to zero
- Good for side projects with variable traffic
```

### Expensive Patterns to Avoid
```
Always-on compute for variable traffic
- Kubernetes cluster (overkill for small apps)
- Multiple redundant servers (before you need them)

Managed services for simple needs
- Managed Redis for basic caching (use in-memory)
- Managed Kafka for simple queues (use Postgres)

Premium tiers before limits hit
- Upgrading "just in case"
- Features you don't use yet
```

### Cost-Effective Stack Example
```
Solo Project Stack ($0-20/month)
├── Frontend: Vercel/Cloudflare Pages (free)
├── Backend: Fly.io free tier or Railway
├── Database: Turso/Supabase/PlanetScale free
├── Auth: Built-in or Clerk free tier
├── Email: Resend free tier
├── Monitoring: Sentry + UptimeRobot free
└── DNS/CDN: Cloudflare free

Growth Stack ($50-100/month)
├── Frontend: Same (still free)
├── Backend: Fly.io/Railway paid ($10-20)
├── Database: Managed Postgres ($15-30)
├── Cache: Upstash Redis ($10)
├── Storage: S3/R2 ($5-10)
└── Monitoring: Basic paid tiers ($10-20)
```

## Billing Protection

### Set Alerts Early
```
Configure before you need them:
- 50% of expected budget: Notification
- 80% of expected budget: Warning
- 100% of expected budget: Alert
- 150%: Hard limit if possible
```

### Prevent Surprise Bills
```
AWS
- Enable AWS Budgets
- Set billing alarms in CloudWatch
- Consider AWS Organizations for hard limits

GCP
- Set budget alerts
- Enable quota limits
- Use committed use discounts carefully

General
- Remove unused resources monthly
- Check for orphaned storage/volumes
- Review bills line by line monthly
```

### Common Surprise Costs
```
Data transfer (egress)
- Often free in, expensive out
- CDN can reduce origin egress

Storage that accumulates
- Logs that aren't rotated
- Old backups not deleted
- Unused container images

Idle resources
- Dev/staging environments left running
- Load balancers with no traffic
- Reserved capacity unused
```

## Optimization Tactics

### Quick Wins
```
1. Delete unused resources
   - Old deployments
   - Test databases
   - Orphaned volumes

2. Right-size running resources
   - Drop to smaller instance
   - Reduce over-provisioned storage

3. Use spot/preemptible (where appropriate)
   - 60-90% discount
   - Good for stateless workers

4. Reserved instances (only if stable)
   - 30-60% discount
   - Requires commitment
```

### When to Optimize
```
Don't optimize prematurely:
- Traffic < 10k requests/day: Focus on building
- Cost < $50/month: Not worth the time
- Pre-product-market-fit: Features > cost

Do optimize when:
- Costs growing faster than revenue
- Hitting provider limits
- Architecture clearly wasteful
```

## Provider Comparison

### For Side Projects
```
Best value: Fly.io, Railway, Render
- Simple deployment
- Generous free tiers
- Good developer experience

Best for static: Vercel, Cloudflare Pages
- Free for most use cases
- Built-in CDN
- Edge functions available

Best for full-stack: Supabase, PocketBase
- Database + auth + storage
- Single provider simplicity
```

### For Growing Apps
```
Consider:
- AWS/GCP/Azure for complex needs
- DigitalOcean/Vultr for simple VPS
- Hetzner for best price/performance (EU)

Evaluate:
- Actual feature needs (not marketing)
- Egress costs for your traffic pattern
- Support quality for your tier
```

## Cost Review Checklist

Monthly review:
- [ ] Check billing dashboard for anomalies
- [ ] Delete unused resources
- [ ] Review largest cost items
- [ ] Check for better pricing tiers
- [ ] Verify billing alerts are working

Quarterly review:
- [ ] Compare current vs 3 months ago
- [ ] Evaluate alternative providers
- [ ] Consider reserved capacity if stable
- [ ] Update budget projections
