---
name: grey-haven-incident-response
description: "Handle production incidents with SRE best practices including detection, investigation, mitigation, recovery, and postmortems. Use when dealing with production outages, SEV1/SEV2 incidents, creating postmortems, or updating runbooks."
# v2.0.43: Skills to auto-load for incident response
skills:
  - grey-haven-code-style
  - grey-haven-observability-monitoring
  - grey-haven-smart-debugging
# v2.0.74: Tools for incident response
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - TodoWrite
  - WebFetch
---

# Incident Response Skill

Handle production incidents with SRE best practices including detection, investigation, mitigation, recovery, and postmortems.

## Description

Production incident response following SRE methodologies with incident timeline tracking, RCA documentation, and runbook updates.

## What's Included

- **Examples**: SEV1 incident handling, postmortem templates
- **Reference**: SRE best practices, incident severity levels
- **Templates**: Incident reports, RCA documents, runbook updates

## Use When

- Production outages
- SEV1/SEV2 incidents
- Postmortem creation
- Runbook updates

## Related Agents

- `incident-responder`

**Skill Version**: 1.0
