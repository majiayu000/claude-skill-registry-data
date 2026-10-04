---
name: templateclaw-refactor
description: "Generate refactoring checklists — performance optimization, security audit, and database migration guides. Actionable step-by-step guides with verification commands."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[type: performance|security|db-migration]"
---

# TemplateClaw — Refactoring Checklists

Generate actionable refactoring guides with verification steps.

## When Invoked

1. If argument provided (e.g., `/templateclaw-refactor security`), generate that checklist
2. If no argument, ask: "Which checklist? (performance / security / db-migration)"

## Available Checklists

### Performance Optimization (`/templateclaw-refactor performance`)

**Output: `docs/performance-checklist.md`**

```markdown
# Performance Optimization Checklist

## Frontend
- [ ] Bundle size analysis (webpack-bundle-analyzer / source-map-explorer)
- [ ] Image optimization (WebP, lazy loading, responsive srcset)
- [ ] Code splitting (dynamic imports, route-based)
- [ ] CSS purging (unused styles removal)
- [ ] Font optimization (subset, display=swap, preload)
- [ ] Core Web Vitals targets: LCP<2.5s, FID<100ms, CLS<0.1

## Backend
- [ ] Database query profiling (EXPLAIN ANALYZE)
- [ ] N+1 query detection and resolution
- [ ] Connection pooling configured
- [ ] Response caching (Redis / in-memory / CDN)
- [ ] Pagination for list endpoints
- [ ] Async processing for heavy operations

## Infrastructure
- [ ] CDN for static assets
- [ ] Gzip/Brotli compression
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] DNS prefetch for external resources
- [ ] Service worker for offline caching (PWA)

## Measurement
- [ ] Lighthouse CI score > 90
- [ ] Load test baseline established
- [ ] APM monitoring configured (response times, error rates)
```

**Bonus**: Scan the current project and highlight specific optimization opportunities.

### Security Audit (`/templateclaw-refactor security`)

**Output: `docs/security-audit.md`**

```markdown
# Security Audit Checklist

## Authentication & Authorization
- [ ] Password hashing (bcrypt/argon2, NOT md5/sha1)
- [ ] JWT expiry < 24h, refresh token rotation
- [ ] Rate limiting on auth endpoints (5 attempts/min)
- [ ] RBAC/ABAC properly implemented
- [ ] Session invalidation on password change

## Input Validation
- [ ] All user input validated (type, length, format)
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding, CSP headers)
- [ ] CSRF tokens on state-changing requests
- [ ] File upload restrictions (type, size, scanning)

## Secrets Management
- [ ] No hardcoded secrets in code
- [ ] .env in .gitignore
- [ ] Secrets rotated on schedule
- [ ] API keys scoped to minimum permissions
- [ ] Audit log for secret access

## Infrastructure
- [ ] HTTPS everywhere (HSTS header)
- [ ] Security headers (CSP, X-Frame-Options, etc.)
- [ ] Dependencies scanned (npm audit / safety / cargo audit)
- [ ] Container images scanned
- [ ] Principle of least privilege on all services

## OWASP Top 10 Quick Check
- [ ] A01 Broken Access Control
- [ ] A02 Cryptographic Failures
- [ ] A03 Injection
- [ ] A07 Authentication Failures
- [ ] A09 Security Logging & Monitoring
```

**Bonus**: Run `npm audit` / `pip audit` / `cargo audit` and report findings.

### Database Migration Guide (`/templateclaw-refactor db-migration`)

**Output: `docs/db-migration-guide.md`**

```markdown
# Database Migration Guide

## Pre-Migration
- [ ] Current schema documented
- [ ] Backup created and verified
- [ ] Migration script written and reviewed
- [ ] Rollback script prepared
- [ ] Downtime window communicated (if needed)

## Migration Script Standards
- [ ] Idempotent (safe to run twice)
- [ ] Forward-only (avoid ALTER TABLE DROP in production)
- [ ] Batched for large tables (1000 rows/batch)
- [ ] Indexes created CONCURRENTLY (PostgreSQL)
- [ ] Foreign keys validated after migration

## Zero-Downtime Patterns
1. Add new column (nullable) → deploy code that writes both → backfill → make NOT NULL → remove old column
2. Expand-Contract pattern for schema changes
3. Feature flags to control read path

## Post-Migration
- [ ] Data integrity verified (row counts, checksums)
- [ ] Application smoke tests passed
- [ ] Monitoring confirmed (no error spikes)
- [ ] Rollback script tested in staging
- [ ] Old migration files archived
```

## Context-Aware Behavior

When invoked in a project:
1. Detect tech stack from project files
2. Customize checklist items to the specific stack
3. Run automated checks where possible (audit commands)
4. Generate project-specific recommendations
