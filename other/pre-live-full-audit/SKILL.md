---
name: pre-live-full-audit
description: Master orchestrator skill for performing pre-live quality, security, performance, accessibility, and release readiness audits.
---

# PRE-LIVE-FULL-AUDIT Skill

## Overview
Coordinates parallel specialist audit lanes to review codebases, web applications, APIs, dependencies, and infrastructure before production release.

## When to Use
- Before any major release, deploy, or customer presentation.
- When evaluating external PRs or unfamiliar repositories.
- When running weekly or automated compliance health checks.

## Protocol
1. **Discover:** Run `TechDetector` to profile languages, frameworks, DBs, cloud, and test runners.
2. **Scan:** Run `ToolRunner` with real linters, `npm audit`, secret regexes, and OWASP patterns.
3. **Review:** Dispatch specialist review lenses (Security, Correctness, Architecture, Adversarial).
4. **Verify:** Run `FindingVerifier` to confirm every finding against the physical filesystem.
5. **Consolidate:** Deduplicate overlapping findings, correlate root causes, and evaluate Release Gate (`BLOCKED`, `READY_FOR_REVIEW`, `PASS`).
6. **Report:** Output the 13 required audit deliverables to `audit-reports/`.
