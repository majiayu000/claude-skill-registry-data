---
name: commitments
description: Extract and track builder commitments from critique exegesis. Use /commitments to audit promises made in prose, verify implementation status, and identify unfulfilled obligations.
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(gh:*)
---

# Commitment Tracker

This skill closes the accountability gap between **promises in prose** and **implementation in code**.

## Purpose

Exegesis generates concrete commitments. Without tracking, these become:
- Forgotten intentions
- Unfulfilled promises
- Accountability theater

This skill extracts commitments, links them to issues/PRs, and reports on fulfillment status.

## Invocation

```bash
/commitments                # Full audit of all commitments
/commitments extract        # Extract new commitments from exegesis
/commitments status         # Show fulfillment status
/commitments [slug]         # Audit specific critique's commitments
/commitments unfulfilled    # List only unfulfilled commitments
```

## Commitment Detection

### Patterns That Indicate Commitments

Look for these phrases in `<div class="exegesis">` blocks:

```
"Adding to..."           → Task commitment
"Opening issue..."       → Issue commitment
"Implementing..."        → Code commitment
"Refactoring..."         → Code commitment
"Let me commit to..."    → Explicit commitment
"Adding to the roadmap"  → Roadmap commitment
"needs to change"        → Implicit commitment
"I'll add..."            → Task commitment
"Target: before..."      → Deadline commitment
```

### Commitment Categories

1. **Code Commitments** - Changes to source files
   - Pattern: "refactor", "implement", "add", "change"
   - Verification: Check git log for relevant commits

2. **Issue Commitments** - GitHub issues to create
   - Pattern: "opening issue", "tracking in #"
   - Verification: Check `gh issue list`

3. **Documentation Commitments** - Docs to update
   - Pattern: "document", "publish", "README"
   - Verification: Check doc file changes

4. **Governance Commitments** - Process changes
   - Pattern: "DAO", "governance", "vote"
   - Verification: Check governance files

## Extraction Procedure

### 1. Parse Exegesis Blocks

```bash
# Extract all exegesis content
grep -A 10 '<div class="exegesis">' src/posts/data.ts
```

### 2. Identify Commitment Statements

For each exegesis block, look for:
- Action verbs: "adding", "implementing", "opening", "creating"
- Future tense: "will", "going to", "need to"
- File references: `code blocks`, path mentions
- Issue references: #123, "issue to track"

### 3. Structure Commitments

```json
{
  "id": "commit-001",
  "source": "the-hyphal-hierarchy/section-viii",
  "statement": "Implement Gini coefficient measurement",
  "category": "code",
  "target": "univrs-enr or univrs-network",
  "status": "unfulfilled",
  "verificationMethod": "grep for 'gini' in ecosystem repos",
  "linkedIssue": null,
  "linkedPR": null,
  "dateExtracted": "2026-01-02"
}
```

## Verification Procedures

### For Code Commitments

```bash
# Search for implementation across repos
for repo in univrs-dol univrs-vudo univrs-enr univrs-network cryptosaint.io; do
  echo "=== $repo ==="
  git -C ~/repos/$repo log --oneline --since="2026-01-01" --grep="[commitment keyword]"
done
```

### For Issue Commitments

```bash
# Check if issue exists
gh issue list --repo ardeshir/[repo] --search "[commitment keyword]"
```

### For Documentation Commitments

```bash
# Check for doc changes
git log --oneline --since="2026-01-01" -- "*.md" "docs/"
```

## Output Format

### Status Report

```
┌─────────────────────────────────────────────────────────────┐
│                  COMMITMENT AUDIT                           │
├─────────────────────────────────────────────────────────────┤
│  Total commitments: 12                                      │
│  Fulfilled: 3 (25%)                                         │
│  In progress: 2 (17%)                                       │
│  Unfulfilled: 7 (58%)                                       │
└─────────────────────────────────────────────────────────────┘

UNFULFILLED COMMITMENTS:

1. [the-hyphal-hierarchy] Implement Gini coefficient
   Category: code
   Target: univrs-enr
   Days since commitment: 0

2. [the-brics-bridge] Add governance.rs to CryptoSaint
   Category: code
   Target: cryptosaint.io
   Days since commitment: 0

3. [the-progress-machine] Add user metrics to MilestoneTracker
   Category: code
   Target: learn.univrs.io
   Days since commitment: 0
```

### Commitment Detail

```
┌─────────────────────────────────────────────────────────────┐
│  COMMITMENT: Implement Gini coefficient                     │
├─────────────────────────────────────────────────────────────┤
│  Source: the-hyphal-hierarchy / Section VIII                │
│  Statement: "If I can't measure inequality, I can't claim   │
│             to be reducing it."                             │
│  Category: code                                             │
│  Status: UNFULFILLED                                        │
│  Linked Issue: None                                         │
│  Linked PR: None                                            │
├─────────────────────────────────────────────────────────────┤
│  VERIFICATION ATTEMPTED:                                    │
│  - Searched univrs-enr for "gini": 0 matches                │
│  - Searched univrs-network for "gini": 0 matches            │
│  - No issues found mentioning "gini coefficient"            │
└─────────────────────────────────────────────────────────────┘
```

## Known Commitments (Extracted Cycle 5)

From exegesis across all 4 critiques:

| # | Commitment | Source | Category | Target |
|---|------------|--------|----------|--------|
| 1 | Add user metrics to MilestoneTracker | progress-machine | code | learn.univrs.io |
| 2 | Add /status command showing role/priority | hyphal-hierarchy | code | univrs-network |
| 3 | Implement Gini coefficient measurement | hyphal-hierarchy | code | univrs-enr |
| 4 | Add governance.rs to CryptoSaint | brics-bridge | code | cryptosaint.io |
| 5 | Bioregional weight >= satellite weight | brics-bridge | code | cryptosaint.io |
| 6 | Emergency alerts to all participants | brics-bridge | code | cryptosaint.io |
| 7 | Make fee distribution DAO-controlled | brics-bridge | code | cryptosaint.io |
| 8 | Show "0/1 users" honestly in dashboard | progress-machine | code | learn.univrs.io |
| 9 | Publish model assumptions as DOL schemas | brics-bridge | docs | univrs-dol |
| 10 | Document BRICS alignment explicitly | brics-bridge | docs | cryptosaint.io |

## Integration with Evolution Loop

```
/critique → [generates critique]
    ↓
/respond → [adds exegesis with commitments]
    ↓
/commitments extract → [identifies new commitments]
    ↓
/evolve → [tracks commitment fulfillment as gap metric]
    ↓
[Builder implements]
    ↓
/commitments status → [verifies fulfillment]
    ↓
/evolve → [updates metrics, proposes next focus]
```

## The Accountability Question

Every commitment audit must answer:

1. **Are commitments being made faster than fulfilled?**
   - If yes: slow down critique cycle, speed up implementation
   - Commitment debt is technical debt with moral weight

2. **Are unfulfilled commitments being acknowledged?**
   - Transparency about gaps > pretending they don't exist
   - Update exegesis with "still unfulfilled" notes

3. **Is this skill creating more work than value?**
   - If tracking commitments becomes busywork, deprecate
   - The goal is accountability, not administration

## Storage

Commitments are tracked in `.claude-flow/metrics/commitments.json`:

```json
{
  "version": "1.0.0",
  "lastAudit": "2026-01-02",
  "commitments": [
    {
      "id": "commit-001",
      "source": "the-hyphal-hierarchy/viii",
      "statement": "Implement Gini coefficient measurement",
      "category": "code",
      "status": "unfulfilled",
      "dateExtracted": "2026-01-02",
      "dateFulfilled": null,
      "linkedPR": null
    }
  ],
  "summary": {
    "total": 10,
    "fulfilled": 0,
    "inProgress": 0,
    "unfulfilled": 10
  }
}
```

## Off-Ramp

If commitment tracking becomes:
- More overhead than value
- A source of guilt rather than action
- Performance theater rather than accountability

The builder can:
```bash
rm -rf .claude/skills/commitments/
rm .claude-flow/metrics/commitments.json
```

Commitments still exist in exegesis. This skill just makes them visible.

---

*"Promises in prose without accountability in code are just words. This skill makes words heavier."*
