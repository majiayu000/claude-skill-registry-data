---
name: pre-flight-review
description: |
  One-command pre-execution review pipeline. Runs scope review → architecture
  review → security review → design review (auto-detects which apply) before
  executing any workflow. Surfaces only taste decisions for user approval.
  Auto-fixes obvious issues. Use before executing multi-step workflows,
  deploying, or when user says "review this plan", "check before running",
  "pre-flight", or "is this ready?". Runs CEO → eng → security automatically
  with encoded decision principles.
---

# Pre-Flight Review

You run the **full pre-execution review pipeline**. One command, comprehensive
review, surfacing only the decisions that need human judgment.

Think of it as the pre-flight checklist before takeoff. Everything the agent
can verify automatically, it does. What requires taste or tradeoff judgment,
it surfaces clearly.

**HARD GATE:** Do NOT execute the plan after review. The user decides when to proceed.

---

## When to Use

Proactively invoke when:
- A multi-step workflow is about to be executed
- User says "review this", "check before running", "pre-flight", "is this ready?"
- Before any deployment, data migration, or destructive operation
- When the user defines a plan and seems ready to execute immediately
- First time working in a project (run to establish baseline)

---

## Step 0: Detect What to Review

```bash
echo "Pre-flight review starting..."
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "Branch: $BRANCH"

# What are we reviewing?
# - A workflow definition (check for workflow JSON or active workflow)
# - A plan document (check docs/plans/, conversation context)
# - A diff/branch (check git diff)
# - A feature description (from user's message)

# Detect scope
find . -name "*.json" -path "*/workflow*" -mtime -1 2>/dev/null | head -3
find docs -name "*plan*" -o -name "*design*" -mtime -1 2>/dev/null | head -3
```

---

## Step 1: Auto-Detect Which Reviews Apply

Based on what's being reviewed:

| If the plan involves... | Run these reviews |
|------------------------|-------------------|
| User-facing features | CEO scope + Design + Security |
| API/backend only | CEO scope + Architecture + Security |
| Infrastructure/DevOps | Architecture + Security only |
| Bug fix (1-2 files) | Security only (skip scope/architecture) |
| Data migration | Architecture + Security (focus on data safety) |
| Documentation only | Skip all (just verify completeness) |

Detect automatically and tell the user: "Running: [list of reviews]."

---

## Step 2: CEO Scope Review

Run a lightweight scope check (not the full interactive `/ceo-scope-review`):

1. **Stated goal vs scope:** Does the plan match the stated goal?
2. **Completeness:** Are all requirements covered?
3. **Overreach:** Is there scope creep? Files changed that shouldn't be?
4. **Missing:** What's obviously missing?

Output: `SCOPE: CLEAN / CONCERNS (list)`

If MAJOR concerns, ask: "Scope has issues — want to run full ceo-scope-review?"

---

## Step 3: Architecture Review

Check architecture quality:

**Data flow:**
- Is data flow clear? (input → process → output for each component)
- Are there circular dependencies?
- Are state transitions explicit?

**Error handling:**
- Every async operation has error handling?
- Error states defined for each component?
- Fallback behaviors specified?

**Edge cases:**
- Empty states handled?
- Loading states defined?
- Boundary conditions considered (0, null, max, empty string)?

**Performance:**
- N+1 queries possible?
- Unnecessary re-renders/computation?
- Large payloads without pagination?

Output: `ARCHITECTURE: PASS / ISSUES (list)` with severity per finding.

---

## Step 4: Security Review

Run a security-focused check:

**OWASP Top 10 (condensed):**
1. **Injection:** SQL, shell, script injection vectors?
2. **Auth:** Authentication bypass possible? Token handling correct?
3. **Data exposure:** Sensitive data in logs, URLs, client-side?
4. **Access control:** Auth checks on all protected routes/actions?
5. **Config:** Secrets hardcoded? Default credentials?

**Infrastructure:**
- Environment variables vs hardcoded config?
- CORS configured correctly?
- Rate limiting present?

**LLM-specific (if AI agents involved):**
- Prompt injection vectors?
- User input reaching system prompts directly?
- Agent tool access scoped appropriately?

Output: `SECURITY: PASS / FINDINGS (list)` with CVE severity mapping.

---

## Step 5: Design Review (if UI involved)

Quick design check (not full `/design-review`):

1. **Consistency:** Colors, spacing, typography match existing system?
2. **AI slop detection:** Generic gradients, Inter font everywhere, bland layouts?
3. **Responsive:** Breakpoints defined? Mobile considered?
4. **States:** Hover, focus, active, disabled, loading, error, empty?

Output: `DESIGN: PASS / CONCERNS (list)`

---

## Step 6: Aggregate Results

```
PRE-FLIGHT REVIEW
═════════════════
Target: <workflow name / plan name / branch>
Reviews run: SCOPE ✅ ARCHITECTURE ✅ SECURITY ✅ DESIGN (skipped — no UI)

## Findings

### P0 — Must fix before execution
- <finding> (review: security, file: auth.ts:47)

### P1 — Strongly recommended
- <finding> (review: architecture, component: error handling)

### P2 — Consider fixing
- <finding> (review: scope, concern: missing edge case)

## Auto-fixed
- <what was fixed automatically>

## Taste decisions needed
- <decisions that require user judgment>

## Verdict
✅ READY TO EXECUTE — N findings, 0 blocking
⚠ CONDITIONAL — N blocking findings, review before proceeding
❌ BLOCKED — Must fix P0 issues before execution

## Next steps
1. <action>
2. Run /qa-tester after execution
3. Run /session-retro after completion
```

---

## Step 7: Auto-Fix (for obvious issues)

Auto-fix issues where:
- The fix is mechanical (add null check, add error handler)
- The fix has >95% confidence of being correct
- The fix doesn't change behavior or architecture
- The fix is in a single file with clear scope

Flag what was auto-fixed so the user can review.

---

## Step 8: Learnings Integration

Log any:
- New patterns recognized for this project
- Security concerns specific to this codebase
- Architecture decisions that should be documented

This makes future pre-flight reviews faster — known patterns skip review.

---

## Integration Points

- **Before:** Often invoked after `ceo-scope-review` or workflow definition
- **After:** User decides to execute → trigger workflow
- **Companion:** Run `/qa-tester` after execution, `/session-retro` after completion
- **Learnings:** Feeds into `learnings-keeper` for compounding knowledge

---

## Key Principles

- **One command, comprehensive.** Don't make the user run four separate reviews.
- **Auto-detect, don't ask.** Figure out which reviews apply from context.
- **Surface taste, automate mechanics.** Only ask the user about things that need human judgment.
- **Be fast.** A pre-flight review should take 2-5 minutes, not 20.
- **Compound knowledge.** Each review learns from previous ones via the learnings system.
