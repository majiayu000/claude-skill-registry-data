---
name: incident
description: Analyze production incidents and generate prioritized triage checklists
---

# Incident Triage & Response

**Current Time:** !`date`
**K8s Context:** !`kubectl config current-context`

Analyze a production incident and generate a prioritized triage checklist. Writes findings to Obsidian incident log.

## Input

- Problem statement: symptoms, error messages, affected systems
- Optional: logs, metrics, alerts, or stack traces

## Investigation Strategy

Launch three parallel investigation tracks:

### Track 1: External Research (librarian agent)

- Search for known issues matching error signatures
- Check dependency changelogs for recent breaking changes
- Look for CVEs or security advisories in affected components
- Find similar incidents/solutions in public issue trackers

### Track 2: Codebase Exploration (explore agent)

- Identify code paths related to error messages/symptoms
- Find recent commits touching affected areas
- Locate error handling and logging for affected services
- Map service dependencies and failure modes

### Track 3: Code Analysis (inferred agent: go/frontend/postgres/etc.)

- Infer appropriate agent from problem statement context
- Deep analysis of suspect code paths
- Identify potential failure modes
- Review error handling completeness
- Assess rollback safety of recent changes

## Output

Write to Obsidian via `obsidian_append_content` at:
`$OBSIDIAN_PATH/Incidents/YYYY-MM-DD-HHMM-brief-title.md`

> **Note**: `$OBSIDIAN_PATH` must be a vault-relative path (e.g., `Projects/myapp`), set per-project via direnv. The `obsidian_append_content` tool expects paths relative to the vault root.

### Document Structure

Use this template for the Obsidian document:

@~/.config/opencode/templates/incident-triage.md

## Behavior

1. Parse problem statement to extract symptoms, errors, affected systems
2. Infer appropriate code agent from context (go, frontend, postgres, etc.)
3. Launch librarian, explore, and inferred code agent in parallel
4. Synthesize findings from all three tracks
5. Generate customized checklist with specific file:line references
6. Rank mitigation options by speed-to-recovery
7. Write incident document to Obsidian via `obsidian_append_content` with auto-generated filename: `YYYY-MM-DD-HHMM-brief-title.md`

$ARGUMENTS
