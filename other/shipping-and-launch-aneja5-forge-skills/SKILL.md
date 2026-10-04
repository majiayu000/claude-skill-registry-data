---
name: shipping-and-launch
description: Use before any production deployment or release, when preparing to launch a feature, when validating release readiness, when a rollback plan is needed before shipping, or when a pre-launch gate is required before approving a deploy.
---

# Shipping and Launch

## Overview

A go/no-go gate before production. Six check domains. Any Critical finding is a hard blocker. Any Important finding must be explicitly accepted before proceeding. Rollback plan defined before deploy begins.

## When to Use

- Before any production deployment
- Before tagging a release
- Before a significant feature goes live
- `/ship` command invoked

## When NOT to Use

- Local development or staging — this gate is for production
- Emergency hotfix in progress — run a compressed version of domains 1-3 only

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Tests pass, we're good to ship" | Tests don't check observability, infra config, or rollback plan |
| "We'll add monitoring after launch" | Monitoring must exist before launch to detect launch failures |
| "The rollback plan is obvious" | Obvious plans aren't written down — write it down |
| "Security review can happen next sprint" | Post-launch security reviews happen after breaches |
| "The README is good enough" | If someone can't deploy this without you, the README isn't good enough |

## Red Flags

- No monitoring or alerting configured for the new surface area
- Rollback plan is "redeploy the previous version" with no specifics
- Environment variables not verified in production environment
- Database migrations not tested on a production-size data snapshot
- No CHANGELOG entry for a user-visible change

## Six Check Domains

### 1. Code Quality
- [ ] Full test suite passes in CI
- [ ] Build clean — no lint errors, no type errors
- [ ] No TODO, FIXME, or debug logs committed
- [ ] No dead code or commented-out blocks
- [ ] Bundle size within acceptable range (if frontend)

### 2. Security
- [ ] All user inputs validated and sanitized
- [ ] No secrets in source code, logs, or error messages
- [ ] Authentication required before authorization before business logic
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options if applicable)
- [ ] Dependency audit clean (`npm audit` / `pip audit` / equivalent)

### 3. Performance
- [ ] No N+1 queries introduced
- [ ] Database queries have appropriate indexes
- [ ] No synchronous blocking in async request paths
- [ ] Core Web Vitals within targets (if frontend)
- [ ] Load tested at expected peak volume (if significant new surface)

### 4. Observability
- [ ] Structured logging for all new error paths
- [ ] Metrics / traces in place for new endpoints or background jobs
- [ ] Alerts configured for error rate, latency, and resource usage
- [ ] Dashboards updated to include new surface area

### 5. Infrastructure
- [ ] Environment variables set in production environment (not just local)
- [ ] Database migrations tested — rollback migration available
- [ ] Rollback plan written and validated:
  - What triggers a rollback?
  - Who can execute it?
  - What are the steps?
  - What's the estimated time?
- [ ] Feature flags in place if a staged rollout is needed

### 6. Documentation
- [ ] README updated if install steps, config, or public interface changed
- [ ] CHANGELOG entry added (user-visible changes)
- [ ] ADR written if any architectural decision was made during this release
- [ ] API docs updated if external API changed
- [ ] On-call runbook updated for new failure modes

## Go / No-Go Decision

After running all six domains:

**GO** — all Criticals clear, all Importants explicitly accepted with owner assigned.

**NO-GO** — any Critical finding unresolved.

State the decision explicitly: "GO — shipping T001-T005. Rollback plan: [specifics]."

## Verification

- [ ] All six domains checked
- [ ] Each finding categorized (Critical / Important / OK)
- [ ] All Critical findings resolved before proceeding
- [ ] Rollback plan written with specific steps and trigger criteria
- [ ] Go/no-go decision stated explicitly
