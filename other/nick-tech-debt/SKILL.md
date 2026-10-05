---
name: nick-tech-debt
description: Practical technical debt scanning and prioritization for Nick's projects. Use during maintenance reviews, when a codebase feels slow to work in, or when checking what debt is actually hurting development velocity. Focus on high-impact debt, not style nitpicks.
---

# Nick Tech Debt

Use this as the default technical debt assessment skill.

## Purpose
Identify technical debt that actually slows shipping, increases bug risk, or makes projects harder to change.

## What to focus on
- duplicated code
- dead code / stale code paths
- oversized or overly complex files/functions
- weak test coverage around risky flows
- outdated patterns that make changes harder
- brittle auth/data logic
- config/env drift
- debt that blocks feature velocity

## Hard rules
- Focus on debt that impacts development velocity, reliability, or change safety
- Do not waste time on cosmetic style nitpicks
- Separate high-impact debt from cleanup-later debt
- Give practical effort/payoff estimates
- Prefer next-action guidance over broad theory

## Default workflow
1. Scan the codebase for obvious debt signals
2. Identify what most slows edits, testing, or understanding
3. Classify debt by impact
4. Estimate effort vs payoff
5. Compare with previous scan when available
6. Produce a practical prioritized report

## Default output
- High-impact debt
- Medium/cleanup debt
- Risky hotspots
- Missing test coverage around risky areas
- Quick wins
- Trend comparison to last scan
- Recommended next fixes

## Priority buckets
- Blocker
- Slows shipping
- Cleanup later

## References
- Read `references/high-impact-signals.md` for what matters most
- Read `references/prioritization.md` for effort/payoff logic
- Read `references/trend-tracking.md` for comparing scans over time
- Read `references/report-shape.md` for output structure

## Bundled scripts
- `scripts/init_debt_report.sh` — create a debt report stub
- `scripts/generate_hotspot_checklist.sh` — create hotspot review checklist
- `scripts/generate_trend_stub.sh` — create trend comparison stub
