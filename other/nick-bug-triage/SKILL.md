---
name: nick-bug-triage
description: Practical bug triage and release-readiness judgment for Nick's projects. Use when grouping bugs by severity, deciding what to fix first, judging go/no-go for release, or turning messy bug lists into a prioritized action plan.
---

# Nick Bug Triage

Use this as the default bug triage skill.

## Focus
- severity
- reproducibility
- user impact
- release risk
- regression risk

## Hard rules
- prioritize by user impact and release risk
- separate blockers from annoyances
- keep severity practical, not inflated
- focus on what must be fixed before release

## References
- `references/severity-guide.md`
- `references/release-judgment.md`
- `references/repro-quality.md`

## Bundled scripts
- `scripts/generate-bug-triage-sheet.sh`
- `scripts/generate-release-go-no-go.sh`
