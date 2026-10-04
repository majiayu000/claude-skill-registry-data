---
name: superpowers-autoplan
description: >
  Use when asked to "autoplan", "run the review pipeline", "full review", "review my plan",
  "check everything", "multi-review", or when you want to run CEO, design, and engineering
  reviews sequentially and surface taste decisions at a final gate. Orchestrates plan-ceo-review,
  plan-design-review, and plan-eng-review in sequence with a final approval gate.
---

> **DEPRECATED** — use `/autoplan` instead. This skill is a legacy alias and will be removed in a future cleanup.
# AutoPlan — Multi-Review Pipeline

**Purpose:** Run CEO → design → engineering reviews sequentially, surface taste decisions at a final gate, log everything to disk.

**Input:** An implementation plan file. Requires `/superpowers-office-hours` output if available.

---

## Prerequisites

```bash
# Check for plan file
ls docs/superpowers/plans/*.md 2>/dev/null | head -5

# Check for office-hours output
ls docs/superpowers/specs/*office-hours*.md 2>/dev/null | head -3
```

If no plan file: "No plan found. Run `/superpowers-brainstorming` first to create a design, then `/superpowers-writing-plans` to create the implementation plan."

If office-hours output exists: read it and reference it throughout the review.

---

## Detect Base Branch

```bash
gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null || echo "main"
```

---

## Phase 1: CEO Review (Strategy)

Run `/superpowers-plan-ceo-review` against the plan.

This phase answers:
- Is the scope right?
- Is this ambitious enough?
- What's the 10-star product?
- What was missed?

**Output:** Scope decisions, expansion proposals, foundational assumptions challenged.

**Auto-decide** any scope expansions that are:
- Low effort (AI: <15 min) and high impact
- Already covered by existing decisions
- Safe defaults that cost nothing to add

**Human gate** for:
- Significant scope additions
- Deferrals of planned features
- Challenging foundational assumptions

---

## Phase 2: Design Review (UX/UI)

Run `/superpowers-plan-design-review` if the plan has UI scope.

Skip if no UI components in the plan. Detect with:

```bash
grep -rE "ui|frontend|react|vue|svelte|html|css|style|component|page|screen" docs/superpowers/plans/*.md 2>/dev/null | grep -v "node_modules" | head -10
```

If skipped: note "No UI scope detected — design review skipped."

This phase answers:
- What's the design direction?
- Are the UI components coherent?
- What's missing from a design standpoint?
- How does this look at a 10?

**Output:** Design decisions, component inventory, coherence assessment.

---

## Phase 3: Engineering Review (Architecture)

Run `/superpowers-plan-eng-review` against the plan.

This phase answers:
- Is the architecture sound?
- Are there security gaps?
- Is test coverage addressed?
- Are error paths handled?
- Is performance considered?

**Output:** Architecture decisions, security posture, test strategy, error registry.

---

## Phase 4: Six Taste Decision Principles

Before the final gate, apply these auto-decision principles to any remaining questions:

| Principle | Decision rule |
|-----------|-------------|
| **1. Completeness** | If the complete option costs minutes more with AI, prefer it |
| **2. Boil the Lake** | If something is a lake (boilable), boil it. Don't ship shortcuts |
| **3. Pragmatic** | If a simpler approach achieves 90% with 10% of the effort, prefer it — unless that 10% matters |
| **4. DRY** | If there's duplication that isn't obviously needed, eliminate it |
| **5. Explicit over clever** | If code can be read by someone who doesn't know the codebase, prefer that |
| **6. Bias toward action** | If stuck on a decision with no strong reason either way, pick one and move. Reversibility matters more than optimality |

Log every auto-decision with its principle:

```
AUTO-DECISIONS (principle-based)
════════════════════════════════
[Decision] → [Choice] [Principle: #N — reason]
```

---

## Phase 5: Final Approval Gate

Present all unresolved decisions for user approval:

```
FINAL APPROVAL GATE
════════════════════════════════
CEO Review:     [N findings] — [N resolved auto, N need decision]
Design Review:  [N findings] — [N resolved auto, N need decision] (or SKIPPED)
Eng Review:      [N findings] — [N resolved auto, N need decision]
════════════════════════════════
Taste decisions remaining: N
════════════════════════════════
```

For each remaining decision, present one AskUserQuestion with:
1. Re-ground (the decision, why it matters)
2. Simplify (plain English)
3. Recommend (Completeness X/10)
4. Options (lettered, effort shown)

After all taste decisions are resolved:

```
APPROVE — All decisions resolved. Plan is ready for implementation.
REVICE — Specific issues to address.
REJECT — Plan needs significant rethinking. Return to Phase 1.
```

---

## Phase 6: Log to Disk

Save the review pipeline results:

```bash
mkdir -p .claude/review-reports
REPORT_FILE=".claude/review-reports/autoplan-$(date +%Y-%m-%d-%H%M%S).json"

cat > "$REPORT_FILE" << 'EOF'
{
  "date": "YYYY-MM-DD",
  "plan_file": "...",
  "phases": {
    "ceo": { "findings": N, "auto_resolved": N, "human_decisions": N },
    "design": { "findings": N, "auto_resolved": N, "human_decisions": N, "skipped": false },
    "eng": { "findings": N, "auto_resolved": N, "human_decisions": N }
  },
  "taste_decisions": [...],
  "final_verdict": "APPROVED / REVISED / REJECTED"
}
EOF
```

Also write a markdown summary:

```
# AutoPlan Review Report — YYYY-MM-DD

## Summary
Plan: [filename]
CEO: [N] findings, [N] auto-resolved
Design: [N] findings, [N] auto-resolved (skipped: [yes/no])
Eng: [N] findings, [N] auto-resolved
Taste decisions: [N] — all resolved

## Verdict: [APPROVED / NEEDS WORK]

## Key Decisions
- [Decision 1] → [Choice]
- [Decision 2] → [Choice]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

---

## Key Principles

- **Sequential, not parallel** — each review builds on the previous
- **Auto-decide where safe** — use the six principles to resolve obvious choices
- **Only human gate for taste** — technical decisions are auto-resolved unless genuinely ambiguous
- **Log everything** — review history enables trend tracking

---

## Completion Status

- **DONE** — All phases complete, final gate passed, report saved
- **DONE_WITH_CONCERNS** — Approved but with warnings
- **BLOCKED** — No plan file found
- **NEEDS_CONTEXT** — Need office-hours output or more plan detail
