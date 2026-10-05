---
name: review
description: "Trigger: /review, code review, PR review, diff review. Run focused review lenses and report actionable findings."
license: Apache-2.0
metadata:
  author: "nutria-ai"
  version: "1.0"
---

## Activation Contract

Use this skill for `/review` or an explicit request to review a completed change. Review only the diff and directly relevant context. Do not create an aggregate reviewer agent.

## Hard Rules

- For management/TL PR gates, use exactly the four generic management profiles in `bundles/management/agents`: `review-risk`, `review-resilience`, `review-readability`, and `review-reliability`. Each applies to any PR scope and loads `management_review`.
- For developer workflow review, select backend or frontend reviewer variants from `bundles/development/agents` based on changed scope; for mixed scope, run both applicable variants.
- Run the four lenses: risk, resilience, readability, and reliability.
- Treat an unavailable required lens as a **BLOCKER** and report it; do not silently substitute another lens.
- Report actionable findings only. Deduplicate overlapping findings and preserve lens attribution. No praise, essays, speculative nitpicks, merge/deploy actions, or approval claims.

## Execution Steps

1. Determine whether `/review` is being run for the management/TL PR gate or the developer workflow.
2. Determine changed scope and inspect the diff plus directly relevant context only.
3. Run all four lenses from the correct bundle: generic management profiles for any management/TL PR scope, or development backend/frontend variants for developer workflow scope.
4. Normalize each finding as `SEVERITY | file:line | lens | evidence | required fix`.
5. Return a concise `READY` or `NOT READY` recommendation. `NOT READY` applies to any unresolved finding or unavailable lens.

## Output Contract

Return only actionable findings, blockers, and the recommendation. Use stable severities: `BLOCKER`, `CRITICAL`, `WARNING`, or `SUGGESTION`. State `No findings` for a clean lens and preserve the lens name on deduplicated findings.

## References

- `bundles/management/AGENTS.md` — management/TL PR gate review workflow.
- `bundles/development/AGENTS.md` — developer workflow review and backend/frontend variants.
- `bundles/agent-libraries.json` — development `review` and management `management_review` libraries.
