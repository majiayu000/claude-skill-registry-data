---
name: document-lifecycle
description: Unified document lifecycle management. Defines terminal statuses, unified numbering via .next-id, close procedures, and orphan detection. Load at session start.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Document Lifecycle Skill

Manages document state transitions, unified numbering, and automated closure across all agent-output directories.

---

## Core Principle

Every work chain shares a single ID. When Analyst creates analysis 080, the downstream plan, implementation, QA, UAT, and critique all use ID 080. This enables human traceability across the entire lifecycle.

Documents in terminal status belong in `closed/` subfolders. Active work stays visible; completed work is archived but accessible.

---

## Terminal Statuses

These statuses trigger document closure (move to `closed/`):

| Status | Meaning | Closed By |
|--------|---------|-----------|
| `Committed` | Changes committed to git (awaiting release) | DevOps |
| `Released` | Successfully pushed/published | DevOps |
| `Abandoned` | Explicitly dropped, will not proceed | User (manual) |
| `Deferred` | Postponed indefinitely | User (manual) |
| `Superseded` | Replaced by a newer document | User (manual) |
| `Resolved` | All findings addressed (critiques only) | Critic |

---

## Unified Numbering Protocol

### The `.next-id` File

Location: `agent-output/.next-id`

Contents: Single integer (e.g., `081`)

**Rules:**
- Only **originating agents** (Analyst, Planner when no analysis) read and increment
- Downstream agents **inherit** the ID from their source document
- Never skip numbers; always use the next available

### Document Header Format

Every document in `agent-output/` MUST include:

```yaml
---
ID: 080                    # Global sequence number
Origin: 080                # Chain origin (same as ID for originating docs)
UUID: a3f7c2b1             # 8-char random hex for collision-proofing
Status: Active             # Current lifecycle state
---
```

### ID Assignment Rules

| Scenario | Action |
|----------|--------|
| Analyst starts new investigation | Read `.next-id`, increment, use as ID, write back |
| Planner creates plan from analysis | Inherit ID/Origin from analysis doc |
| Planner creates plan from user request (no analysis) | Read `.next-id`, increment, use as ID, write back |
| Implementer/QA/UAT/Critic work on plan | Inherit ID/Origin from plan doc |
| Retrospective reviews plan | Inherit ID/Origin from plan doc |

---

## Close Procedure

When a document reaches terminal status:

1. **Update Status field** to the terminal status
2. **Add changelog entry**: `| YYYY-MM-DD | [Agent] | Document closed | Status: [status] |`
3. **Create closed folder** if needed: `mkdir -p agent-output/<domain>/closed/`
4. **Move file**: `mv agent-output/<domain>/NNN-name.md agent-output/<domain>/closed/`
5. **Log action**: "Closed document NNN-name.md (Status: [status])"

### Cross-Reference Handling

When referencing a closed document from another document, use relative paths:
- From active doc: `../closed/080-feature.md`
- From closed doc to closed doc: `./080-feature.md` (same folder)

---

## Orphan Detection

### Agent Self-Check (Every Session Start)

Before starting work, each agent MUST:

1. Scan their exclusive domain (e.g., `agent-output/qa/`) excluding `closed/`
2. Identify any document with terminal Status
3. Move orphaned documents to `closed/`
4. Log: "Found orphaned document [name] with Status [status], moved to closed/"

### Roadmap Periodic Sweep

Roadmap agent performs comprehensive sweep when reviewing roadmap:

1. Scan ALL `agent-output/*/` directories (excluding `closed/`)
2. Flag documents with terminal Status not in `closed/`
3. Report to user
4. Move to respective `closed/` folders

---

## Agent Responsibilities

| Agent | Role | Closure Trigger |
|-------|------|-----------------|
| Analyst | Originate IDs | Planner closes when plan created |
| Planner | Originate or inherit | DevOps closes after commit |
| Implementer | Inherit | DevOps closes after commit |
| QA | Inherit | DevOps closes after commit |
| UAT | Inherit | DevOps closes after commit |
| Critic | Inherit | Self-closes when findings resolved |
| DevOps | N/A | Self-closes after release |
| Retrospective | Inherit | PI closes after processing |
| PI | N/A | Self-closes own analysis |
| Architect | N/A | Evergreen docs, no closure |
| Roadmap | N/A | Orphan sweep responsibility |
| Security | Inherit | Self-check only |

---

## Quick Reference

### Creating a New Document (Originating)

```bash
# Read current ID
NEXT_ID=$(cat agent-output/.next-id)
# Increment for next use
echo $((NEXT_ID + 1)) > agent-output/.next-id
# Use $NEXT_ID as your document ID
```

### Closing a Document

```bash
# Update Status in document header to terminal status
# Add changelog entry
mkdir -p agent-output/<domain>/closed/
mv agent-output/<domain>/NNN-name.md agent-output/<domain>/closed/
```

### Self-Check Pattern

```
Before starting work:
1. List agent-output/<my-domain>/*.md (excluding closed/)
2. For each file, check Status field
3. If Status in [Committed, Released, Abandoned, Deferred, Superseded, Resolved]:
   → Move to closed/
```
