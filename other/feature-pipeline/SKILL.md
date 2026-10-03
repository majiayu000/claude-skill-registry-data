---
name: feature-pipeline
description: Evaluate, score, approve or reject, implement, and stage GitHub feature requests for Aries AI. Use when a GitHub issue is classified as a feature, enhancement, idea, or product request that must be compared against current priorities before being built or closed with reasoning.
---

# Feature Pipeline

Use this skill for GitHub issues that represent new features, enhancements, or product requests.

## Read this when needed
- Scoring rubric: `references/feature-evaluation-rubric.md`

## Required inputs
- GitHub issue number
- Repo root: `/app/aries-app`
- Feedback log: `data/feedback-processing-log.json`

## Required planning sources
Read these before deciding:
- `PRIORITIES.md`
- `generated/validated/project-progress.json`
- `generated/validated/canonical-roadmap-baseline.md`

## Required procedure
1. Confirm the issue record is pending in the feedback log:
   - Inspect `data/feedback-processing-log.json` for the issue entry.
2. Inspect the issue in GitHub:
   - `gh issue view <number> --repo DeliciousHouse/aries-app --json title,body,labels,comments,url`
3. Score the request:
   - `effortHours`
   - `impactScore`
   - `alignmentScore`
4. Decide `approved` or `rejected`.
   - Reject when it conflicts with the current roadmap, widens an unsupported surface, or is weakly aligned.
   - Approval here means approved for implementation and staging only, never production.
5. If rejected:
   - update the feedback log with the reasoning
   - comment on the issue with a concise explanation
   - close the issue
6. If approved:
   - scope the work into a tight implementation slice
   - create a branch named `feature/issue-<number>-<slug>`
   - implement the feature
   - run the most relevant tests
   - deploy to staging using the project's staging deploy process; if none is configured, record `staging: none`
   - comment on the issue with the scope summary and staging URL
   - if useful, open a draft PR for review
7. Update `data/feedback-processing-log.json` so the record includes:
   - `effortHours`
   - `impactScore`
   - `alignmentScore`
   - `approvalDecision`
   - `approvalReason`
   - `branch`
   - `stagingUrl`
   - `status`
   - `summaryPending`

## Guardrails
- All features require Brendan's approval before production shipping.
- Prefer rejection over stealth scope creep when the feature fights the current roadmap.
- Keep rationale concrete. Do not close requests with generic wording.
- Do not describe staging as production.

## Output format
Return only:
- `status:` success or failed
- `issue:` `#<number>`
- `decision:` approved or rejected
- `effort_hours:` number
- `impact:` 1-5
- `alignment:` 1-5
- `branch:` branch name or `none`
- `staging:` URL or `none`
- `reason:` short sentence
- `next_step:` short operator follow-up or `none`
