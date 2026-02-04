---
name: PR Feedback Training-First Loop
description: Extract, learn, and integrate PR feedback into the Violet brain
---

# PR Feedback Training-First Loop

> Every PR becomes training data. Learn before you fix.

**Core Principle**: TRAINING FIRST - Extract and analyze PR feedback to fuel continuous improvement.

---

## Overview

The training-first PR review loop has 4 stages:

```
CAPTURE RAW → EXTRACT → 🚦GATE 1 → PROPOSE → 🚦GATE 2 → INTEGRATE → FIX
```

| Stage | Command | Purpose |
|-------|---------|---------|
| **STAGE 0-1** | `/v-pr-feedback:extract` | Capture raw + extract 13-category taxonomy |
| **STAGE 2** | `/v-pr-feedback:integrate` | Propose and commit learnings to brain |
| **STAGE 3** | `/v-pr-feedback:fix` | Fix code on correct branch |

---

## When to Use

**Trigger phrases**:
- "Review PR #123"
- "Review comments on PR #456"
- "Extract feedback from PR #789"
- "Check PR #42 for issues"

**All these phrases should invoke** `/v-pr-feedback:extract` to start the full loop.

---

## 13-Category Taxonomy

PR feedback is extracted using these categories (adapted from customer meeting extraction):

| # | Category | PR-Specific Meaning |
|---|----------|---------------------|
| 1 | **Sentiment Analysis** | Overall PR health, reviewer tone, approval likelihood |
| 2 | **Action Items** | Required changes, suggestions, blockers (human + bot) |
| 3 | **Bugs** | Code issues, lint violations, formatting, type errors |
| 4 | **Feature Requests** | Suggested enhancements, architectural improvements |
| 5 | **Documentation Needs** | Missing comments, unclear code, README updates |
| 6 | **Process Improvements** | CI/CD issues, workflow problems, tool suggestions |
| 7 | **Technical Context** | Architecture concerns, design patterns, dependencies |
| 8 | **Stakeholder Context** | Reviewers, approvers, domain experts |
| 9 | **Timeline & Commitments** | Merge deadlines, release blockers, urgent issues |
| 10 | **Expansion Signals** | Future work identified, refactoring opportunities |
| 11 | **Competitor Intelligence** | Alternative approaches, tools mentioned |
| 12 | **Questions & Answers** | Q&A captured, unresolved questions |
| 13 | **Key Insights** | Learnings, surprises, patterns to document |

---

## Extraction Sources

PR feedback is extracted from:

- **Human comments**: Review comments with `@claude`, `@username`, or general
- **Bot feedback**: Graphite Bot, ESLint, TypeScript compiler, Prettier
- **CI/CD results**: Test failures, build errors, security scans
- **PR metadata**: Title, description, linked Linear issues
- **Automated checks**: Linting, formatting, type checking, coverage

---

## Storage Location

All extractions are saved to **violet-brain**:

```
violet-brain/pr-learnings/{repo}/
├── YYYY-MM-DD-pr-{number}-raw.md          # Raw PR data (verbatim)
├── YYYY-MM-DD-pr-{number}-extraction.md   # 13-category extraction
├── YYYY-MM-DD-pr-{number}-fixes.md        # Commits that fixed issues
└── learnings.md                            # Aggregated patterns
```

**Templates** are in `violet-brain/pr-learnings/_templates/`:
- `raw-template.md` - Raw capture format
- `extraction-template.md` - 13-category extraction format
- `learning-integration.md` - How to integrate learnings

---

## Review Gates

### Gate 1: Extraction Accuracy

**When**: After extraction completes
**Purpose**: Verify extraction is accurate before proposing learnings

**Format**:
```
🚦 GATE 1: Review Extraction

Does this extraction look accurate and complete?

[✓] Approve - Continue to propose learnings
[✗] Modify - Edit extraction before continuing
[⊗] Reject - Stop here
```

### Gate 2: Proposed Learnings

**When**: After learning proposals are generated
**Purpose**: Approve brain updates before committing

**Format**:
```
🚦 GATE 2: Approve Changes

Review the diffs above. Approve these brain updates?

[✓] Approve - Commit all changes to brain
[✗] Modify - Edit diffs before committing
[⊗] Reject - Skip learning integration
```

---

## Learning Integration Targets

When patterns are identified, propose updates to:

| Pattern Type | Update Target |
|--------------|---------------|
| **Pre-PR preventable issue** | `patterns/pr-quality.md` checklist |
| **Common code quality issue** | `patterns/code-review-patterns.md` |
| **Missed in tech-lead review** | `agents/references/tech-lead.md` |
| **Security vulnerability** | `agents/references/security-reviewer.md` + `standards/` |
| **Process inefficiency** | `patterns/pr-quality.md` troubleshooting |

---

## Critical: Branch Workflow

**ALWAYS update the SAME branch** as the original PR. Never create a new PR for fixes.

```bash
# ✅ RIGHT - Update existing PR
git checkout feat/my-feature  # Original branch
git commit -m "fix: address PR #123 feedback"
git push origin feat/my-feature  # Updates PR automatically

# ❌ WRONG - Creates orphaned PR
git checkout -b fix/pr-123-feedback  # New branch (NO!)
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/v-pr-feedback:extract` | STAGE 0+1: Capture raw, extract 13-category |
| `/v-pr-feedback:integrate` | STAGE 2: Propose and commit learnings |
| `/v-pr-feedback:fix` | STAGE 3: Fix code on correct branch |

---

## Best Practices

### Extraction
- Extract **all** feedback, not just `@claude` comments
- Include bot feedback (automated checks are valuable)
- Don't skip "minor" issues (patterns emerge from small issues)
- Include file:line references for all code issues

### Learning Integration
- Look for patterns (don't update brain for one-off issues)
- Pattern threshold: 2+ occurrences = document it
- Be specific with detection methods and fixes
- Always attribute source PR in commits

### Fixing Code
- Always checkout the original PR branch
- Link commit message to extraction file
- Create fixes record for traceability
- Request re-review after pushing fixes

---

## Related Documentation

- `violet-brain/pr-learnings/README.md` - Complete system documentation
- `violet-brain/pr-learnings/_templates/` - Extraction templates
- `violet-brain/patterns/pr-quality.md` - PR quality standards
- `violet-brain/patterns/pr-learning-integration.md` - Learning integration process

---

*Version: 1.0.0*
*Maintained by: Violet Platform Team*
