---
name: cross-repo-communication
description: Standardized methodology for inter-orchestrator communication across the EvaLok ecosystem. Use when processing, polling, or responding to cross-repo issues between the main, QC, and audit repos.
user-invocable: false
---

# Cross-repo Communication Protocol

Standardized methodology for inter-orchestrator communication across the EvaLok ecosystem. Adopted per [audit #53](https://github.com/EvaLok/schema-org-json-ld-audit/issues/53).

## Core Principles

1. **Write only to your own repo.** Messages go OUT as labeled issues on the sender's repo.
2. **Discover by polling.** Receivers find messages by polling other repos' issues via `gh api`.
3. **Respond on your own repo.** Create a tracking issue on YOUR repo referencing the source.
4. **Track in state.json.** Record processed issue numbers to avoid double-processing.
5. **Trust only EvaLok.** All issue authors must be verified as `EvaLok`.

## Message Types (Labels)

| Label | Created on | Created by | Consumed by | Purpose |
|-------|-----------|-----------|------------|---------|
| `audit-outbound` | Audit repo | Audit | Main, QC | Process recommendation |
| `audit-inbound` | Main/QC repo | Main/QC | Audit | Response to audit recommendation |
| `qc-outbound` | QC repo | QC | Main | QC validation report |
| `qc-inbound` | Main repo | Main | QC | Response to QC report |
| `qc-outbound` (title `[QC-REQUEST]`) | Main repo | Main | QC | Validation request |
| `qc-ack` | QC repo | QC | Main | Acknowledgment of request |
| `input-from-eva` | Any repo | Eva | Target repo | Human directive |
| `question-for-eva` | Any repo | Any | Eva | Question for human operator |

## Communication Flows

### Audit recommendation flow

```
Audit repo                     Main/QC repo
(audit-outbound #N)  -------->  Polls, discovers, evaluates
                                Creates audit-inbound issue on OWN repo
                     <--------  Audit polls main/QC for audit-inbound issues
```

### QC report flow

```
QC repo                        Main repo
(qc-outbound #N)    -------->  Polls, discovers, evaluates
                                Creates qc-inbound issue on main repo
                     <--------  QC polls main for qc-inbound issues
```

### Validation request flow

```
Main repo                      QC repo
(qc-outbound request) ------->  Polls, discovers, evaluates
                                 Creates qc-ack issue on QC repo
                      <--------  Main polls QC for qc-ack issues
```

## Main Repo Polling Templates

### Step 4 — QC repo polling

```bash
# Discover new QC reports
gh api "repos/EvaLok/schema-org-json-ld-qc/issues?labels=qc-outbound&state=open&creator=EvaLok&sort=created&direction=asc" --paginate --jq '.[] | {number, title, created_at}'

# Discover QC acknowledgments of our requests
gh api "repos/EvaLok/schema-org-json-ld-qc/issues?labels=qc-ack&state=all&sort=created&direction=desc&per_page=5" --jq '.[] | {number, title, state, created_at}'
```

### Step 5 — Audit repo polling

```bash
# Discover new audit recommendations
gh api "repos/EvaLok/schema-org-json-ld-audit/issues?labels=audit-outbound&state=open&creator=EvaLok&sort=created&direction=asc" --paginate --jq '.[] | {number, title, created_at}'
```

**Response channel**: `audit-inbound` issues on THIS repo. The main orchestrator does NOT have write access to the audit repo.

## Response Issue Format

### Title format

`[{label}] {Decision}: {brief description} (source #{number})`

Examples:
- `[audit-inbound] Accept: Cross-repo communication skill (audit #53)`
- `[qc-inbound] Fix dispatched: Recipe missing properties (qc #72)`

### Body template

```markdown
## Source
- **Repo**: {repo name}
- **Issue**: [{repo}#{number}]({full URL})
- **Title**: {source issue title}

## Decision
{accept | reject | defer | acknowledge | in-progress}

## Actions taken
- {bullet list of concrete actions}

## Notes
{additional context}
```

## State Tracking

Track processed issue numbers in `docs/state.json`. Arrays contain issue numbers from the SOURCE repo.

Current main repo schema:
```json
{
  "audit_processed": [2, 3, 4, ...],
  "qc_processed": [8, 57, 72, ...],
  "qc_requests_pending": [331]
}
```

Processing logic:
1. Poll for issues matching target label on source repo
2. Filter for trusted author (EvaLok)
3. Compare issue numbers against processed array
4. For each new issue: read body, evaluate, create response issue on own repo, add to processed array
5. Update `last_polled` timestamp

## Lifecycle Management

- **Response issues**: Create when processing a message. Close when action is complete.
- **Source issues**: Managed by the sender. Don't close issues on repos you don't control.
- **Stale cleanup**: During housekeeping, cross-reference open response issues against source issue state.

## Full Cross-repo URLs

Always use full GitHub URLs for cross-repo references:

```
# Correct
Responding to https://github.com/EvaLok/schema-org-json-ld-audit/issues/53

# Avoid
Responding to EvaLok/schema-org-json-ld-audit#53
```
