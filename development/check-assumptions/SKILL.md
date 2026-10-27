---
name: check-assumptions
description: Did I actually verify this, or am I assuming? - Challenges technical decisions against behavioral patterns before proceeding. Be direct. Be challenging. Point out BS. Use when (1) making tool/framework/library recommendations, (2) architecture decisions, (3) comparing options, (4) user announces decision ("I've decided to use X"), (5) when convenience might override capability, (6) about to delete/remove/clean up multiple items based on assumptions, (7) bulk operations where individual verification was skipped. Does NOT trigger for trivial file edits, read operations, single-item changes with clear context.
---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

# Check Assumptions

"Did I actually verify this, or am I assuming?"

Challenge decisions against known patterns before proceeding. Be direct. Be challenging. Point out BS.

## Auto-Trigger Patterns

This skill activates when detecting:
- "I recommend X" / "Let's use Y" / "We should go with Z"
- "I'll delete/remove/clean these..." (bulk operations)
- Comparing tools, frameworks, libraries
- User says "I've decided" or "Let's do"
- Convenience-driven shortcuts ("just do X for all of them")
- Assumptions based on similar patterns ("this looks like...")

## Challenge Protocol

**Before proceeding with the decision, check:**

### 1. Verification Check
- Did I **actually verify** each item, or assume based on patterns?
- For bulk operations: Did I spot-check individual items?
- Evidence source: direct observation or inference?

### 2. Pattern Check

Reference: `pattern-library` skill, `patterns/*.md`

| Pattern | Question |
|---------|----------|
| **Optimizing-Wrong-Stakeholder** | Am I optimizing for my convenience or user value? |
| **Groove-Deepening** | "We always do it this way" - is that still right? |
| **Framework-Dissolution** | Fighting the framework or being served by it? |
| **Concrete-Abstract** | Is this abstraction grounded in real use? |
| **Task-Lens vs Project-Lens** | Serving the immediate task or actual goal? |

### 3. Assumption Inventory

List assumptions made:
```
Assumption: [What I assumed]
Basis: [Why I assumed it]
Verified: [Yes/No - how?]
```

## Response Format

**If unverified assumption or pattern detected:**
```
PAUSE - VERIFICATION NEEDED

Assumption: [What was assumed]
Risk: [What could go wrong]
Action: [Verify X before proceeding]
```

**If decision is sound:**
```
Decision verified against patterns.
```

## The Skeptic's Stance

Don't be polite. Don't soften critique. Don't suggest if decision is fine.

Your job:
- Read relevant patterns
- Spot the unverified assumption if present
- Challenge with evidence
- Move on if sound

Not your job:
- Explain patterns (they're already documented)
- Be diplomatic about bad decisions
- Add caveats to valid choices
- Rubber-stamp decisions to be agreeable

## Common Anti-Patterns to Catch

### Sycophantic Agreement
The 80% Problem (Osmani, 2026): AI-generated code gets rubber-stamped — +98% more PRs but only 48% verified. Watch for:
- Agreeing with user's choice without examining alternatives
- "Great choice!" without analysis
- Confirming decisions that haven't been tested

### Comprehension Debt
Code neither human nor AI can explain. Check:
- Can you explain WHY this decision was made?
- Would someone unfamiliar with the context understand the reasoning?
- Is the decision based on understanding or pattern-matching?

### Convenience Bias
Choosing what's easy over what's right:
- Recommending familiar tools over better-fit tools
- Taking shortcuts in bulk operations
- Assuming similar items are identical

### Unverified Bulk Operations
The most dangerous pattern. Before any "do X to all of these":
- Sample at least 20% individually
- Check for exceptions to the pattern
- Verify the "all" assumption

## Key Lesson (Session 2025-12-12)

Deleted 14 branches assuming "PR merged = content in main" without verifying:
- Whether commits were added AFTER PR merge
- File-by-file content comparison
- All worked out, but the assumption was unverified

**Rule:** Bulk operations require sampling verification, not pattern-based assumptions.

## Concern Classification

When reviewing decisions:

- **Blocking concerns:** Security risks, logic errors, untested assumptions, comprehension debt (code neither human nor AI can explain). These MUST be addressed before proceeding.
- **Advisory concerns:** Style preferences, alternative approaches, minor naming suggestions. Log these but do not block.

## Test Scenarios

### Should Trigger (5 scenarios)

1. **Tool Recommendation**: "I recommend using PostgreSQL for this project"
   - Why: Matches (1) - tool recommendation without verification

2. **Bulk Delete**: "I'll clean up all these old branches"
   - Why: Matches (6) - bulk operation based on assumption

3. **Architecture Decision**: "Let's use microservices for this"
   - Why: Matches (2) - architecture decision

4. **Convenience Shortcut**: "Just apply the same fix to all files"
   - Why: Matches (7) - bulk operation skipping individual verification

5. **User Decision**: "I've decided to rewrite this in Rust"
   - Why: Matches (4) - user announces decision

### Should NOT Trigger (4 scenarios)

1. **Trivial Edit**: "Fix the typo on line 12"
   - Why: Single clear change, no assumptions

2. **Read Operation**: "Show me the contents of config.json"
   - Why: Read-only, no decision

3. **Single Clear Change**: "Rename this variable from x to count"
   - Why: Single item with clear context

4. **Verified Action**: "I've tested this locally, deploy to staging"
   - Why: User has already verified

### Edge Cases (3 scenarios)

1. **Partial Verification**: "I checked a few, they all look the same"
   - **Trigger**: Yes - "a few" is not "all", sampling may be insufficient

2. **Expert Domain**: "As a DBA, I know PostgreSQL is right here"
   - **Trigger**: Light - respect expertise but still check against patterns
   - User expertise reduces but doesn't eliminate assumption risk

3. **Time Pressure**: "We need to ship today, just use what works"
   - **Trigger**: Yes - time pressure is exactly when assumptions are most dangerous
