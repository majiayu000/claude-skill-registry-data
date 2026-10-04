---
name: pre-deploy-checklist
description: Run a pre-deployment checklist before pushing to production. Reviews changed files for security, correctness, edge cases, cross-app impact, and confirms builds pass. Use when the user says they are about to deploy, asks for a final review, pre-deploy check, or code review before production.
---

# Pre-Deploy Checklist

Run this checklist before any production deployment. Be thorough â€” especially if your app handles money, personal data, or anything where a bug means more than a bad UX.

## Steps

### Step 1: Identify All Changes
- List every file changed since the last deploy (use `git diff` or `git log`).
- Group changes by area: frontend, backend, shared packages, database migrations, config.

### Step 2: Security Review
- [ ] No secrets, API keys, or tokens exposed to the client.
- [ ] All user inputs validated (Zod, Joi, or equivalent).
- [ ] No raw SQL strings (parameterized queries only).
- [ ] Access control / authorization on any new endpoints or pages.
- [ ] No sensitive data in logs or error messages.

**If your app handles money:**
- [ ] No floating point math for money calculations (use integer cents or decimal types).
- [ ] Payment/transfer endpoints have idempotency keys (so retries don't create duplicate transactions).
- [ ] Multi-step financial operations wrapped in transactions with rollback on failure.
- [ ] Transaction records are immutable â€” never updated or deleted, only appended.
- [ ] Audit logging: who did what, when, and what changed.

### Step 3: Cross-App Impact
If your project has multiple apps sharing a database or shared packages:
- [ ] If shared types changed â†’ **all consuming apps** checked for breakage.
- [ ] If database schema changed â†’ all apps' queries verified.
- [ ] If API contracts changed â†’ all consumers updated.
- [ ] If shared packages changed â†’ types/builds regenerated.

This is where most "it worked on my machine" bugs come from. A type change in the shared package that passes the build in App A but breaks App B at runtime.

### Step 4: Edge Cases & Correctness
- [ ] Error handling in place (try/catch with meaningful messages, not empty catches).
- [ ] Loading and empty states handled in UI changes.
- [ ] Null/undefined values handled in data flows.
- [ ] Race conditions considered for concurrent operations.
- [ ] What happens if this fails halfway through? Is the state recoverable?

### Step 5: Build Verification
- Run the build command and confirm **all apps** pass â€” not just the one you changed.
- Report any TypeScript errors or warnings.
- If you have multiple apps, build them all. A green build in one doesn't guarantee the other.

### Step 6: Migration Check (if applicable)
- [ ] Migration is additive (no destructive changes without discussion â€” never drop columns with production data).
- [ ] Migration has a comment block explaining what it does and why.
- [ ] Types/schemas regenerated after migration.
- [ ] If adding a view, it respects the caller's permissions (not the view owner's).

### Step 7: Manual Steps Required
- List any scripts that need to be run manually post-deploy.
- List any environment variables or config changes needed.
- Provide copy-paste ready commands for anything the user needs to run.

## Output Format

```
## Pre-Deploy Review

**Status**: [GO âœ… / NEEDS FIXES ðŸŸ¡ / DO NOT DEPLOY ðŸ”´]

### Changes Summary
- [Area]: [Brief description of what changed]

### Security
- [Any concerns or "All clear"]

### Cross-App Impact
- [Any concerns or "No cross-app impact"]

### Edge Cases
- [Any concerns or "All covered"]

### Build Status
- [App Name]: [âœ… Pass / âŒ Fail]

### Risks
- [Any risks flagged, or "No significant risks"]

### Manual Steps After Deploy
- [Any scripts to run, or "None"]

### Recommendation
[One sentence: deploy or fix first]
```
