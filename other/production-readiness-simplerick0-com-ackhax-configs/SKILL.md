---
name: production-readiness
description: Comprehensive checklist and guidance for preparing applications for production deployment. Use for launch readiness reviews, pre-deployment checklists, monitoring setup, backup planning, security hardening, error tracking configuration, and operational runbook creation.
---

# Production Readiness

Ensure your application is ready for real users and real stakes.

## Launch Checklist

### Infrastructure
- [ ] Hosting environment provisioned
- [ ] Domain and DNS configured
- [ ] SSL/TLS certificates installed (auto-renewal)
- [ ] CDN configured (if needed)
- [ ] Database backups automated and tested
- [ ] Environment variables secured (not in code)

### Security
- [ ] HTTPS enforced (redirect HTTP)
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Authentication tested thoroughly
- [ ] Authorization checked at every endpoint
- [ ] Secrets rotated from development
- [ ] Dependency vulnerabilities scanned
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints

### Monitoring
- [ ] Application error tracking (Sentry, etc.)
- [ ] Uptime monitoring configured
- [ ] Performance metrics collected
- [ ] Log aggregation set up
- [ ] Alerting rules defined
- [ ] On-call contact configured

### Data
- [ ] Database migrations tested
- [ ] Backup restore verified
- [ ] Data retention policy defined
- [ ] GDPR/privacy compliance (if applicable)
- [ ] Seed/test data removed

### Operations
- [ ] Deployment process documented
- [ ] Rollback procedure tested
- [ ] Health check endpoint working
- [ ] README updated with run instructions
- [ ] Environment-specific configs separated

## Monitoring Setup

### Key Metrics to Track
```
Application Health
├── Error rate (% of requests)
├── Response time (p50, p95, p99)
├── Request throughput (req/min)
└── Active users (concurrent)

Infrastructure
├── CPU utilization
├── Memory usage
├── Disk space
├── Network I/O
└── Database connections

Business Metrics
├── Signups / conversions
├── Feature usage
└── User retention signals
```

### Health Check Endpoint
```python
# Minimal health check
@app.get("/health")
def health():
    return {"status": "healthy"}

# Detailed readiness check
@app.get("/health/ready")
def readiness():
    checks = {
        "database": check_db_connection(),
        "cache": check_redis(),
        "disk": check_disk_space(),
    }
    all_healthy = all(checks.values())
    return JSONResponse(
        status_code=200 if all_healthy else 503,
        content={"ready": all_healthy, "checks": checks}
    )
```

### Alerting Thresholds
```
CRITICAL (page immediately)
- Error rate > 5%
- Response time p95 > 5s
- Service down > 1 minute
- Disk space < 10%

WARNING (notify, don't page)
- Error rate > 1%
- Response time p95 > 2s
- Memory > 80%
- Certificate expiring < 14 days
```

## Error Tracking

### What to Capture
```
Every error should include:
- Stack trace
- Request URL and method
- User ID (if authenticated)
- Request body (sanitized)
- Environment (prod/staging)
- Release version
- Browser/client info
```

### Error Grouping
Group errors by:
- Exception type + location
- Affected users count
- First/last occurrence
- Release introduced

### Sentry Setup (Example)
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://...",
    environment="production",
    release="1.0.0",
    traces_sample_rate=0.1,  # 10% of transactions
)

# Add user context
sentry_sdk.set_user({"id": user.id, "email": user.email})
```

## Backup Strategy

### What to Back Up
```
Database
- Full backup: Daily
- Point-in-time recovery: Enable
- Retention: 30 days minimum

User uploads
- Replicate to separate storage
- Consider versioning

Configuration
- Infrastructure as code (committed)
- Secrets in vault (backed separately)
```

### Backup Verification
```markdown
## Monthly Backup Test

1. Create test environment
2. Restore latest backup
3. Verify data integrity
4. Test critical user flows
5. Document results and issues
```

### Recovery Time Objectives
```
Define for your application:
- RTO (Recovery Time Objective): Max downtime acceptable
- RPO (Recovery Point Objective): Max data loss acceptable

Example (typical SaaS):
- RTO: 4 hours
- RPO: 1 hour
```

## Security Hardening

### HTTP Security Headers
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=()
```

### Secrets Management
```
Never in code:
- API keys
- Database passwords
- JWT secrets
- OAuth credentials

Use instead:
- Environment variables
- Secret managers (AWS Secrets Manager, Vault)
- Encrypted config files
```

### Dependency Security
```bash
# Python
pip-audit

# Node
npm audit

# Run in CI, block on high/critical
```

## Deployment Process

### Pre-Deployment
```markdown
1. All tests passing
2. Code reviewed and approved
3. Staging tested
4. Database migrations reviewed
5. Feature flags configured
6. Rollback plan ready
```

### Deployment Steps
```markdown
1. Announce deployment (if needed)
2. Enable maintenance mode (if needed)
3. Run database migrations
4. Deploy new code
5. Run smoke tests
6. Monitor error rates
7. Disable maintenance mode
8. Announce completion
```

### Rollback Triggers
Roll back immediately if:
- Error rate > 10%
- Critical functionality broken
- Data corruption detected
- Security vulnerability exposed

### Rollback Steps
```markdown
1. Revert to previous deployment
2. Revert database migrations (if safe)
3. Notify stakeholders
4. Investigate root cause
5. Fix and re-attempt with more testing
```

## Runbook Template

```markdown
# Runbook: [Service Name]

## Service Overview
- Purpose: [What it does]
- Dependencies: [Other services, databases]
- Owner: [Contact]

## Access
- Production URL: [URL]
- Admin panel: [URL]
- Logs: [Location]
- Metrics: [Dashboard URL]

## Common Issues

### Issue: High Error Rate
Symptoms: Error rate > 5%, alerts firing
Diagnosis:
1. Check error tracking for new errors
2. Check recent deployments
3. Check dependency health
Resolution:
- If new deployment: Rollback
- If dependency: Check their status page
- If unknown: Page on-call

### Issue: Slow Response Times
Symptoms: p95 > 2s, users complaining
Diagnosis:
1. Check database query times
2. Check external API latency
3. Check CPU/memory
Resolution:
- Database: Identify slow queries, add index
- External API: Check circuit breaker, add timeout
- Resources: Scale up or optimize

## Maintenance Procedures
- Database maintenance: [Steps]
- Certificate renewal: [Steps]
- Secret rotation: [Steps]
```

## Post-Launch

### First 24 Hours
- [ ] Monitor error rates closely
- [ ] Watch for unexpected traffic patterns
- [ ] Check all critical user flows
- [ ] Respond to user feedback quickly

### First Week
- [ ] Review all errors, fix critical ones
- [ ] Analyze performance data
- [ ] Gather user feedback
- [ ] Document any surprises

### Ongoing
- [ ] Weekly: Review error trends
- [ ] Monthly: Test backup restore
- [ ] Quarterly: Review and rotate secrets
- [ ] Annually: Full security audit
