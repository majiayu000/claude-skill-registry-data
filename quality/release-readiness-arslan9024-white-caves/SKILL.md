---
name: release-readiness
description: 'Validates release readiness through compile, quality, risk, and rollback checks before deployment'
---

# Release Readiness

Use this skill at the end of an implementation wave or before merge-to-main/release.

## Readiness Gates

1. **Compile/Build**
   - Backend typecheck/build clean
   - Frontend typecheck/build clean
2. **Quality**
   - Lint/tests for changed scope pass
   - No high-severity open regressions
3. **Operational Safety**
   - Critical env vars documented
   - Migrations/DB changes reviewed and reversible
4. **Security/Compliance**
   - No unresolved critical security findings
   - Compliance-sensitive changes identified and verified
5. **Deployment + Rollback**
   - Deployment steps are explicit
   - Rollback strategy exists and is realistic

## Execution Steps

1. Collect changed files and categorize by risk.
2. Run/verify compile and quality checks.
3. Confirm tracker notes reflect real validation results.
4. Produce release decision:
   - READY
   - READY WITH CONDITIONS
   - NOT READY

## Output Format

- Decision status
- Evidence table (check -> result -> proof)
- Blocking items and owner
- Rollback notes

## Gotchas

- Do not mark READY without actual validation evidence.
- Keep release notes concise and operationally actionable.

<!-- Inspired by awesome-copilot release workflow patterns -->
