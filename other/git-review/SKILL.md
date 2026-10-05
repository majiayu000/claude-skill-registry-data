---
name: git-review
description: |
  Goal-directed review of git history for change coherence.
  Trigger when:
  - Analyzing project history, reviewing diffs, or checking commit messages for alignment.
  - Prompt contains: /git-review, git history, commit log, change coherence.
---

# Git Review Workflow

A structured approach to reviewing change history with an **explicit purpose**. Never browse history aimlessly — always state what you're looking for.

> **Adversarial path anchor.** This lens is invoked on the Verification Dual's adversarial path ([rules.md](../../rules.md) §2 Invariant 1): when no deterministic evaluator can close a change-coherence condition, context-free agents using this protocol supply the decorrelated review. See [skills/refine/SKILL.md](../refine/SKILL.md) AUDIT §"Sibling Skills Consultation" for the wiring point.

---

## Entry: State Your Purpose

Before reviewing history, declare what you're investigating — state your purpose and scope (commits, timeframe, file path, or keyword).

**Examples:**

- "Trace how the auth module evolved before modifying it"
- "Find where the API contract changed and whether it was justified"
- "Locate commits related to the parsing bug we're debugging"

---

## Modes

### SUMMARY — Get the lay of the land

```bash
git log --oneline -n 20                    # Recent commits
git log --oneline --since="1 week ago"     # Time-bounded
git shortlog -sn --since="1 month ago"     # By author
```

### SEARCH — Find commits relevant to your purpose

```bash
git log --grep="keyword" --oneline         # Message search
git log --all --oneline -- "path/to/file"  # File history
git log -S "function_name" --oneline       # Code change search
```

### EXPAND — Examine specific commits

```bash
git show <hash>                   # Full commit details
git diff <hash>^..<hash>          # Diff only
git show <hash> --stat            # Changed files summary
```

---

## Review Procedure

1. **STATE PURPOSE** — What are you trying to trace or verify?
2. **SUMMARY** — Scan relevant history for context
3. **SEARCH** — Narrow to commits relevant to your purpose
4. **EXPAND** — Examine suspicious or unclear commits
5. **ASSESS** — Apply the coherence checklist

---

## Coherence Checklist

When examining a commit, assess:

- [ ] **Scope Alignment:** Does the change match its commit message?
- [ ] **API Consistency:** Does the change follow existing patterns?
- [ ] **Breaking Changes:** Are they documented and justified?
- [ ] **Debt Tracking:** Are shortcuts documented with follow-up tasks?
- [ ] **Commit Atomicity:** Is each commit a single logical change?

---

## Output Format

```
GIT REVIEW
PURPOSE: [stated purpose]
SCOPE: [what was searched]

COMMITS EXAMINED: N

RELEVANT:
- <hash>: <summary>
  Finding: [how it relates to purpose]

CONCERNS:
- <hash>: <summary>
  Issue: [problem identified]

CONCLUSION: [what was learned, relative to purpose]

RECOMMENDATIONS:
1. [Actionable item]
```

---

## Integration with the Active Workflow

The active closed-loop execution workflow ([/core](../core/SKILL.md), [/refine](../refine/SKILL.md)) requires ledger updates and JUSTIFICATION blocks at each COMMIT boundary. Well-formed commits should:

- Have atomic scope matching the commit message
- Document any scope drift, breaking changes, or technical debt
- Be independently reviewable

**Red flags:** Commits with "and" in the message, unexplained scope changes, or missing context.

**Recovery:** If inconsistencies are found, use `/core` to plan remediation.