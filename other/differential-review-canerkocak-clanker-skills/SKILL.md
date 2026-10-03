---
name: differential-review
description: >
  Performs security-focused differential review of code changes (PRs, commits, diffs).
  Adapts analysis depth to codebase size, uses git history for context, calculates
  blast radius, checks test coverage, adjudicates candidate findings against the
  current contract, and generates comprehensive markdown reports. Automatically
  detects and prevents security regressions without promoting policy or partial
  evidence into defects.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Differential Security Review

Security-focused code review for PRs, commits, and diffs.

## Core Principles

1. **Risk-First**: Focus on auth, crypto, value transfer, external calls
2. **Evidence-Based**: Every finding backed by git history, line numbers, attack scenarios
3. **Adaptive**: Scale to codebase size (SMALL/MEDIUM/LARGE)
4. **Honest**: Explicitly state coverage limits and confidence level
5. **Artifact-Aligned**: Use the output medium the user requested. Create a
   persistent report only when the request or governing workflow requires one
   and writing it is authorized; otherwise return a self-contained chat review
6. **Adjudicated**: A candidate receives severity only after contract,
   reachability, intent, counterevidence, and decision impact are resolved

---

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Small PR, quick review" | Heartbleed was 2 lines | Classify by RISK, not size |
| "I know this codebase" | Familiarity breeds blind spots | Build explicit baseline context |
| "Git history takes too long" | History reveals regressions | Never skip Phase 1 |
| "Blast radius is obvious" | You'll miss transitive callers | Calculate quantitatively |
| "No tests = not my problem" | Missing tests reduce assurance but do not prove impact | Flag the assurance gap; do not elevate defect severity without impact evidence |
| "Just a refactor, no security impact" | Refactors can break invariants | Give it the highest applicable review priority until the changed invariant is scoped |
| "The skill always requires a file" | Output requirements come from the user and governing workflow | Write a report only when requested or authorized; otherwise preserve the full result in chat |
| "The reviewer already confirmed it" | Reviewer conclusions and structural matches are hypotheses | Run the finding-promotion gate and perform root adjudication |
| "The risk is real, so it blocks the decision" | Technical exposure and decision authority are separate contracts | Cite the decision bridge or keep the result informational |

---

## Quick Reference

### Codebase Size Strategy

| Codebase Size | Strategy | Approach |
|---------------|----------|----------|
| SMALL (<20 files) | DEEP | Read all deps, full git blame |
| MEDIUM (20-200) | FOCUSED | 1-hop deps, priority files |
| LARGE (200+) | SURGICAL | Critical paths only |

### Review-Priority Triggers

These levels prioritize review effort. They are not finding severity.

| Review Priority | Triggers |
|------------|----------|
| HIGH | Auth, crypto, external calls, value transfer, validation removal |
| MEDIUM | Business logic, state changes, new public APIs |
| LOW | Comments, tests, UI, logging |

---

## Workflow Overview

```
Pre-Analysis → Phase 0: Triage → Phase 1: Code Analysis → Phase 2: Test Coverage
    ↓              ↓                    ↓                        ↓
Phase 3: Blast Radius → Phase 4: Deep Context → Phase 5: Adversarial
    → Phase 5.5: Finding Promotion Gate → Phase 6: Report
```

---

## Decision Tree

**Starting a review?**

```
├─ Need detailed phase-by-phase methodology?
│  └─ Read: methodology.md
│     (Pre-Analysis + Phases 0-4: triage, code analysis, test coverage, blast radius)
│
├─ Analyzing a HIGH-priority review change?
│  └─ Read: adversarial.md
│     (Phase 5: Attacker modeling, exploit scenarios, exploitability rating)
│
├─ Promoting a candidate finding into severity or a decision?
│  └─ Run: yagni-anti-ceremonial
│     Use fp-check when the claim is disputed, delegated/automated, or would
│     change payment, merge, deployment, production, or acceptance.
│
├─ Writing the final report?
│  └─ Read: reporting.md
│     (Phase 6: Report structure, templates, formatting guidelines)
│
├─ Looking for specific vulnerability patterns?
│  └─ Read: patterns.md
│     (Regressions, reentrancy, access control, overflow, etc.)
│
└─ Quick triage only?
   └─ Use Quick Reference above, skip detailed docs
```

---

## Quality Checklist

Before delivering:

- [ ] All changed files analyzed
- [ ] Git blame on removed security code
- [ ] Blast radius calculated for HIGH-priority review surfaces
- [ ] Attack scenarios are concrete (not generic)
- [ ] Findings reference specific line numbers + commits
- [ ] Every reported finding passed the promotion gate
- [ ] Intent/policy evidence and strongest counterevidence are reconciled
- [ ] Structural `verified` results are not presented as bug verification
- [ ] Severity is separate from review priority and confidence
- [ ] Every blocker cites an explicit decision-contract bridge
- [ ] State-machine/accounting remedies include canonical-owner and non-interference proof
- [ ] Requested output delivered in the authorized medium and location
- [ ] User notified with summary

---

## Integration

**audit-context-building skill:**
- Pre-Analysis: Build baseline context
- Phase 4: Deep context on HIGH-priority review changes
- Consume only flows, invariants, assumptions, contradictions, and unknowns;
  discard any finding, fix, or severity included in a context handoff

**yagni-anti-ceremonial skill:**
- Mandatory Phase 5.5 adjudication for every candidate that could receive
  severity, enter recommendations, or change a user decision

**fp-check skill:**
- Mandatory for disputed or delegated/automated decision-changing findings and
  for complex money/auth/state-machine claims before promotion

**issue-writer skill:**
- Transform findings into formal audit reports
- Command: `issue-writer --input DIFFERENTIAL_REVIEW_REPORT.md --format audit-report`

---

## Example Usage

### Quick Triage (Small PR)
```
Input: 5 file PR, 2 HIGH-priority review files
Strategy: Use Quick Reference
1. Classify risk level per file (2 HIGH, 3 LOW)
2. Focus on 2 HIGH files only
3. Git blame removed code
4. Generate minimal report
Time: ~30 minutes
```

### Standard Review (Medium Codebase)
```
Input: 80 files, 12 HIGH-priority review changes
Strategy: FOCUSED (see methodology.md)
1. Full workflow on HIGH-priority review files
2. Surface scan on MEDIUM
3. Skip LOW risk files
4. Complete report with all sections
Time: ~3-4 hours
```

### Deep Audit (Large, Critical Change)
```
Input: 450 files, auth system rewrite
Strategy: SURGICAL + audit-context-building
1. Baseline context with audit-context-building
2. Deep analysis on auth changes only
3. Blast radius analysis
4. Adversarial modeling
5. Comprehensive report
Time: ~6-8 hours
```

---

## When NOT to Use This Skill

- **Greenfield code** (no baseline to compare)
- **Documentation-only changes** (no security impact)
- **Formatting/linting** (cosmetic changes)
- **User explicitly requests quick summary only** (they accept risk)

For these cases, use standard code review instead.

---

## Red Flags (Stop and Investigate)

**Immediate escalation triggers:**
- Removed code from "security", "CVE", or "fix" commits
- Access control modifiers removed (onlyOwner, internal → external)
- Validation removed without replacement
- External calls added without checks
- High blast radius (50+ callers) + HIGH risk change

These patterns require adversarial analysis even in quick triage. They raise
review priority, not defect severity; only the promotion gate assigns a finding
disposition and permits severity.

---

## Tips for Best Results

**Do:**
- Start with git blame for removed code
- Calculate blast radius early to prioritize
- Generate concrete attack scenarios
- Reference specific line numbers and commits
- Be honest about coverage limitations
- Record policy evidence and the strongest counterevidence
- Distinguish call-chain verification from bug adjudication
- Use the requested output medium; create a persistent artifact only when
  requested or required by an authorized governing workflow

**Don't:**
- Skip git history analysis
- Make generic findings without evidence
- Copy delegated severity into the report without root adjudication
- Invent approval roles or decision conditions absent from the active contract
- Claim full analysis when time-limited
- Forget to check test coverage
- Miss high blast radius changes
- Ignore the user's requested output format or write an unsolicited artifact

---

## Supporting Documentation

- **[methodology.md](methodology.md)** - Detailed phase-by-phase workflow (Phases 0-4)
- **[adversarial.md](adversarial.md)** - Attacker modeling and exploit scenarios (Phase 5)
- **[reporting.md](reporting.md)** - Report structure and formatting (Phase 6)
- **[patterns.md](patterns.md)** - Common vulnerability patterns reference

---

**For first-time users:** Start with [methodology.md](methodology.md) to understand the complete workflow.

**For experienced users:** Use this page's Quick Reference and Decision Tree to navigate directly to needed content.
