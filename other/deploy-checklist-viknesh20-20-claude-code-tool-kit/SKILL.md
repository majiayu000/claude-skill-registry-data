---
name: deploy-checklist
description: "Runs a comprehensive pre-deployment verification checklist covering tests, security, environment config, migrations, rollback plan, and breaking changes. Use before deploying to staging or production."
argument-hint: "[staging or production]"
allowed-tools: Read, Grep, Glob, Bash(git *)
---

# Pre-Deployment Checklist

## Current State
!`git branch --show-current 2>/dev/null`
!`git log --oneline -10 2>/dev/null`
!`git status --short 2>/dev/null`

---

## Verification Checklist

Go through each section. Mark items as PASS, FAIL, WARN, or N/A.

### 1. Code Readiness
- [ ] All changes are committed — no uncommitted work
- [ ] Branch is up to date with main/master
- [ ] No merge conflicts
- [ ] All PRs for this release are merged
- [ ] No draft PRs accidentally included

### 2. Testing
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] End-to-end tests pass (if applicable)
- [ ] No new test failures compared to main branch
- [ ] Edge cases for new features are tested
- [ ] Performance-sensitive changes have been load tested

### 3. Code Quality
- [ ] No `console.log` / `print` / debug statements left in
- [ ] No `TODO` or `FIXME` comments that should be resolved
- [ ] No commented-out code blocks
- [ ] Linting passes with zero errors
- [ ] Type checking passes (if applicable)

### 4. Security
- [ ] No hardcoded secrets, tokens, or API keys
- [ ] No new dependencies with known vulnerabilities
- [ ] Input validation in place for new endpoints
- [ ] Authentication/authorization checked for new routes
- [ ] CORS configuration is correct for the target environment

### 5. Database & Migrations
- [ ] All migrations are created and tested
- [ ] Migrations are backwards compatible (can rollback)
- [ ] No destructive migrations without data backup plan
- [ ] Indexes added for new queries
- [ ] Migration order is correct

### 6. Configuration & Environment
- [ ] All new environment variables are documented
- [ ] Environment variables are set in target environment
- [ ] Feature flags are configured correctly
- [ ] Third-party service configs are updated (if needed)
- [ ] SSL/TLS certificates are valid

### 7. API & Breaking Changes
- [ ] No breaking API changes without versioning
- [ ] API documentation is updated
- [ ] Deprecation notices added for removed features
- [ ] Consumers (frontend, mobile, third-party) are notified

### 8. Monitoring & Observability
- [ ] Logging is adequate for new features
- [ ] Error tracking covers new code paths
- [ ] Alerts configured for critical paths
- [ ] Dashboards updated if needed

### 9. Rollback Plan
- [ ] Rollback steps are documented
- [ ] Database rollback migration tested
- [ ] Feature flags can disable new features without rollback
- [ ] Previous version is tagged and accessible

### 10. Web Compliance & SEO (skip ONLY if not a public website)
- [ ] Privacy Policy live at `/privacy` and linked in footer
- [ ] Terms of Service live at `/terms` and linked in footer (if signup/payments)
- [ ] Cookie Policy + cookie consent banner present (if any non-essential cookies)
- [ ] No tracking scripts load before user consent
- [ ] `sitemap.xml` accessible at site root and lists all canonical URLs
- [ ] `robots.txt` accessible at site root with sitemap reference
- [ ] Production environment NOT disallowed in `robots.txt` (common deploy bug)
- [ ] Every page has unique `<title>` and `<meta description>`
- [ ] Every page has canonical URL, Open Graph tags, Twitter Card tags
- [ ] 404 page returns HTTP 404 (not 200)
- [ ] HTTPS-only with HSTS header
- [ ] WCAG 2.1 AA verified (contrast, keyboard, focus, alt text)
- [ ] Core Web Vitals within budget (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1)
- [ ] If applicable: GDPR/CCPA "Do Not Sell" link, DSAR endpoint, consent records retained

If any item in this section fails, run `/web-launch-check` for a structured audit and `/legal-pages` or `/seo-scaffold` to generate the missing pieces.

---

## Output

### Summary Table
| Category | Status | Issues |
|----------|--------|--------|
| Code Readiness | PASS/FAIL | ... |
| Testing | PASS/FAIL | ... |
| ... | ... | ... |

### Blocking Issues
List any FAIL items that must be resolved before deployment.

### Warnings
List any WARN items that should be addressed but aren't blocking.

### Deploy Verdict
- **READY** — All checks pass, safe to deploy
- **CONDITIONAL** — Deploy after resolving blocking issues
- **NOT READY** — Significant issues require more work
