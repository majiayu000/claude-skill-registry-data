---
name: release-cycle
description: Full release from quality check to deployment to reporting
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# Release Cycle

Chain: quality-lint → quality-audit → quality-coverage → pm-changelog → ops-deploy → pm-status-report

## Process

1. Lint and fix code quality issues
2. Security audit dependencies
3. Verify test coverage meets threshold
4. Generate changelog
5. Deploy to target environment
6. Generate status report

Stop on any quality gate failure.