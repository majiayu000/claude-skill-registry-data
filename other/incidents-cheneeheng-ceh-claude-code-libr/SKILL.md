---
name: incidents
description: >-
  Load this skill when responding to a production incident, writing a post-mortem, executing a
  hotfix, or classifying incident severity. Auto-load whenever a production issue is reported, a
  P1/P2/P3 classification is needed, a hotfix branch is being created, or a post-mortem document is
  being written. Not for routine deploys (see deploy) or git tagging (see ceh-git-workflow).
---

# Incident Response

## Severity Levels

| Level | Definition                                    | Response Time         |
| ----- | --------------------------------------------- | --------------------- |
| P1    | Production is down or data is corrupted       | Immediate — all hands |
| P2    | Major feature broken, no workaround for users | < 1 hour              |
| P3    | Feature degraded, workaround exists           | < 1 business day      |

## Response Steps

1. **Detect** — identify from monitoring alerts or user report
2. **Triage** — classify severity, identify scope
3. **Mitigate** — roll back if available; disable the feature if possible
4. **Fix** — hotfix process (minimal scope, all CI must pass, staging still required)
5. **Post-mortem** — written within 48 hours for P1/P2

## Hotfix Process

1. **Branch:** `fix/critical-<description>` from `main`
2. **Scope:** Minimal fix only — no unrelated changes
3. **Review:** 1 approval minimum, fast-tracked
4. **CI:** All checks must pass — do **not** skip CI under pressure. A broken hotfix is worse than a delayed one.
5. **Merge:** Merge commit to `main` (never squash — preserve the commits)
6. **Tag:** Bump PATCH version, apply tag
7. **Deploy:** Staging → production (abbreviated but both still required)

## Post-Mortem Format (Required for P1 and P2)

```markdown
## Incident Post-Mortem: <Short Title>

**Date:** YYYY-MM-DD
**Severity:** P1 | P2
**Duration:** <how long production was impacted>

### What Happened

Brief timeline of events.

### Root Cause

The single underlying cause (not symptoms).

### Impact

What was broken. How many users/requests affected.

### Detection

How was the incident discovered? How long between impact and detection?

### Resolution

What fixed it?

### Prevention

What changes prevent recurrence?

- [ ] Action item (owner, due date)
```
