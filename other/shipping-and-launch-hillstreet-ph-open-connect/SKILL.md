---
name: shipping-and-launch
description: Prepares production launches. Use when preparing to deploy to production, need a pre-launch checklist, setting up monitoring, planning a staged rollout, or need a rollback strategy.
license: MIT
---

# Shipping and Launch

Prepares production launches with checklists, monitoring, staged rollout, and rollback strategy.

## When to Use This Skill

**Trigger conditions:**
- User preparing to deploy to production
- User asks for pre-launch checklist
- User setting up monitoring
- User planning staged rollout
- User needs rollback strategy

## Pre-Launch Checklist

### Code Quality
- [ ] All tests passing
- [ ] No `console.log` in production code
- [ ] Error handling covers expected failure modes

### Security
- [ ] No secrets in code or version control
- [ ] `npm audit` shows no critical/high vulnerabilities
- [ ] Input validation on all user-facing endpoints
- [ ] Authentication and authorization checks in place
- [ ] Security headers configured (CSP, HSTS)
- [ ] Rate limiting on authentication endpoints
- [ ] CORS configured to specific origins (not wildcard)

### Performance
- [ ] Core Web Vitals within "Good" thresholds
- [ ] No N+1 queries in critical paths
- [ ] Images optimized
- [ ] Bundle size within budget
- [ ] Database queries have appropriate indexes

### Monitoring
- [ ] Error tracking configured
- [ ] Latency monitoring in place
- [ ] Health check endpoint available
- [ ] Logging configured

## Staged Rollout

### Strategy

```markdown
## Staged Rollout Plan

### Stage 1: Internal (5-10%)
- Who: Internal team
- Purpose: Smoke test in production-like environment
- Duration: 1-2 days

### Stage 2: Beta Users (10-25%)
- Who: Beta users / power users
- Purpose: Real-world testing
- Duration: 2-7 days

### Stage 3: Percentage Rollout (25-100%)
- Who: All users
- Purpose: Full release
- Duration: Based on stability
```

### Rollout Metrics

Monitor:
- Error rate
- Latency (P95)
- Conversion rates
- User feedback

## Rollback Strategy

Every deployment needs a rollback plan:

```markdown
## Rollback Plan

### Trigger Conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of specific issues

### Rollback Steps
1. Disable feature flag (if applicable)
OR
1. Deploy previous version
2. Verify rollback
3. Communicate with team

### Time to Rollback
- Feature flag: < 1 minute
- Redeploy: < 5 minutes
- Database rollback: < 15 minutes
```

## Post-Launch Verification

In the first hour after launch:

1. Check health endpoint returns 200
2. Check error monitoring dashboard
3. Check latency dashboard
4. Test critical user flow manually
5. Verify logs are flowing
6. Confirm rollback mechanism works

## Common Rationalizations

| Rationalization | Reality |
|---------------|--------|
| "It works in staging, it'll work in production" | Production has different data and edge cases |
| "We don't need feature flags" | Every feature benefits from a kill switch |
| "Monitoring is overhead" | Without monitoring, users tell you about problems |

## See Also

- `references/security-checklist.md` - Security pre-launch checks
- `references/performance-checklist.md` - Performance checklist
- `references/accessibility-checklist.md` - Accessibility verification