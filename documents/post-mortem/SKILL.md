---
name: post-mortem
description: User-invoked as /post-mortem [incident-id]. Guides a blameless post-mortem; reconstructs a timeline from git log and incident data, runs five-whys, and produces action items with owners. Writes to docs/post-mortems/.
allowed-tools: Read, Grep, Glob, Bash, Write
invocation: /post-mortem [incident-id]
---

# Blameless Post-Mortem

Facilitate a blameless post-mortem for `$ARGUMENTS` (an incident id, or the most
recent incident if empty). Blameless means: focus on systems and contributing
factors, never on individual faults.

## Steps

1. **Reconstruct the timeline.**
   - From git: `git log --since=<window> --pretty=format:'%h %ad %s' --date=short` for changes around the incident.
   - From incident data: query stored `RCAReport`s (via the `postgres`/`sqlite` MCP or the filesystem store) for the incident id - detection time, consensus outcome, `SkepticVerdict`, `ConfidenceLevel`, any `HITLRequest`.
2. **Five why's** - drill from symptom to root cause; record each "why" and its evidence.
3. **Contributing factors** - what made detection/diagnosis/remediation slower (gaps in runbooks, missing tests, alert fatigue, etc.).
4. **Action items** - concrete, each with an owner and a tracking issue; route code fixes to `python-expert`, tests to `testing-expert`, doc/runbook updates to `docs-updater`, design changes to `app-architect`.

## Template (docs/post-mortems/YYYY-MM-DD-<incident-id>.md)

```markdown
# Post-Mortem - <incident-id> - <date>
- Severity: | Duration: | Detected by: | Mode:

## Summary
## Impact
## Timeline (UTC)
| Time | Event | Source |

## Root cause (five-whys)
1. Why … → because …

## What went well
## What went wrong / contributing factors
## Action items
| # | Action | Owner | Agent | Tracking |
```

## Output

Print the post-mortem path. Keep tone factual and blameless throughout. Offer to
open the action-item issues via the `github` MCP.
