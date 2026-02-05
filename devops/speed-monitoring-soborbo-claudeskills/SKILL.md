---
name: speed-monitoring
description: Performance monitoring and regression prevention. Lighthouse CI, performance budgets, Core Web Vitals monitoring, alerting. Keep sites fast over time.
---

# Speed Monitoring Skill

## Purpose

Provides patterns for continuous performance monitoring to prevent speed regressions and maintain Core Web Vitals scores. Establishes automated testing, real user monitoring, and alerting systems to catch performance issues before they impact users.

## Core Rules

1. **Budget before build** — Set performance budgets upfront in budget.json
2. **Monitor real users** — Lab data ≠ field data, track both synthetic and RUM
3. **Alert on regression** — Catch issues before users do with threshold-based alerts
4. **Block bad deploys** — CI fails on performance regression via Lighthouse CI
5. **Track over time** — Trends matter more than snapshots, store historical data
6. **Measure Core Web Vitals** — LCP, CLS, INP, FCP, TTFB in production
7. **Automated testing** — Lighthouse CI on every PR and main branch push
8. **Bundle size limits** — Enforce JS/CSS budgets in CI pipeline
9. **Real user data** — Use web-vitals library + beacon API for field data
10. **Dashboard visibility** — Make performance metrics accessible to team

## Performance Budget Targets

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| LCP    | <2.5s | 2.5-4s | >4s |
| FCP    | <1.8s | 1.8-3s | >3s |
| CLS    | <0.1  | 0.1-0.25 | >0.25 |
| INP    | <200ms | 200-500ms | >500ms |
| TBT    | <200ms | 200-600ms | >600ms |

## Resource Budgets

| Resource Type | Budget (gzip) |
|--------------|---------------|
| JavaScript   | 200KB |
| CSS          | 50KB |
| Images       | 500KB |
| Fonts        | 100KB |
| Total        | 800KB |

## Monitoring Stack

### Synthetic (Lab Data)
- Lighthouse CI in GitHub Actions
- Scheduled cron jobs for production monitoring
- Budget assertions in CI/CD pipeline

### Real User (Field Data)
- web-vitals library for Core Web Vitals
- Navigation Timing API for page metrics
- Resource Timing API for asset analysis
- sendBeacon for reliable data transmission

### Alerting Channels
- Slack webhooks for warnings
- PagerDuty for critical performance issues
- Email digests for weekly reports

## Implementation Checklist

**Initial Setup:**
- [ ] Create budget.json with performance targets
- [ ] Add lighthouserc.json configuration
- [ ] Set up Lighthouse CI GitHub Action
- [ ] Configure performance assertions (min score 90)

**Real User Monitoring:**
- [ ] Install web-vitals package
- [ ] Implement vitals tracking client-side
- [ ] Create /api/vitals endpoint
- [ ] Set up database for metrics storage

**Bundle Monitoring:**
- [ ] Create bundle-stats.js script
- [ ] Add bundle size check to CI
- [ ] Set gzip size budgets

**Alerting:**
- [ ] Configure Slack webhook
- [ ] Set performance thresholds
- [ ] Implement alert logic in API
- [ ] Test alert notifications

**Dashboard:**
- [ ] Create performance dashboard page
- [ ] Display current Core Web Vitals
- [ ] Show historical trends
- [ ] Add budget status indicators

## References

- [Performance Budgets](./references/budgets.md) - Budget configuration and bundle monitoring
- [Lighthouse CI](./references/lighthouse-ci.md) - CI setup, workflow, and configuration
- [Web Vitals Monitoring](./references/web-vitals.md) - RUM implementation and tracking
- [Performance Alerts](./references/alerts.md) - Threshold configuration and alerting setup
- [Synthetic Monitoring](./references/synthetic-monitoring.md) - Cron jobs and dashboards

## Forbidden

- No performance monitoring in production
- Ignoring field data (RUM)
- No CI performance checks
- Undefined performance budgets
- Manual-only Lighthouse runs
- Silencing performance alerts

## Definition of Done

- [ ] Performance budgets defined and documented
- [ ] Lighthouse CI running in GitHub Actions
- [ ] CI fails on performance regression (score <90)
- [ ] Web Vitals tracked in production
- [ ] Bundle size monitoring in CI
- [ ] Alerts configured for poor scores
- [ ] Weekly performance review scheduled
- [ ] Performance dashboard accessible to team
