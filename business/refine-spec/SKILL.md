---
name: refine-spec
description: >
  Refine a provisional VDM-SL specification through dialogue with the user,
  uncovering the true specification that exists in the user's mind.
  The provisional spec (from extract-spec) serves as a scaffold for questions.
  Triggered by: "refine the spec", "review the provisional spec",
  「仕様を磨きたい」「仮仕様をレビューして」「コードの意図を確認したい」「仕様を確認して」
metadata:
  version: "1.2.0"
---

# refine-spec: Specification Refinement Through Dialogue

## Core Philosophy

The provisional specification is NOT the true specification. The true specification lives in the user's mind—as intentions, assumptions, and constraints they've never fully articulated. This skill surfaces it through structured dialogue.

**Key insight:** Every difference between code behavior and user intent is a "Finding"—the most valuable output of this process. We're not validating the provisional spec; we're using it as a scaffold to uncover what was actually intended.

---

## Workflow Overview

```
Provisional Spec (from extract-spec)
    ↓
[STEP 1] Translate to natural language
    ↓
[STEP 2] Structured dialogue by category
    ├─ A: Questions (code seems wrong)
    ├─ B: Implicit specs (inferred from tests)
    ├─ C: Missing specs (no code exists)
    └─ D: Provisional confirmations (routine items)
    ↓
[STEP 3] Classify each dialogue result as Finding
    ↓
[STEP 4] Generate confirmed spec from Findings
    ↓
[STEP 5] Check convergence (all tagged items resolved)
    ↓
[STEP 6] Generate Findings Report (structured output)
```

---

## STEP 1: Natural Language Translation

### Purpose
Transform VDM-SL abstractions into plain language the user can evaluate without training in formal methods.

### Process

1. **Extract elements** from provisional spec:
   - State space (data structures, invariants)
   - Operations (pre/post conditions, behavior)
   - Rules and constraints
   - Implicit assumptions from tests/comments

2. **Translate each element** into plain English + Japanese:
   - Avoid formal syntax; use concrete examples
   - Group related items logically
   - Include type information but keep language accessible

3. **Tag each item** with confidence and source:
   ```
   [PROVISIONAL] {confidence: high|medium|low} {source: code|tests|comments}

   Example:
   [PROVISIONAL] {confidence: high} {source: code}
   When a customer requests a refund, their account balance increases by the refund amount.
   ```

4. **Organize by category** for dialogue efficiency:

   **Data Model:**
   - State variables and their meanings
   - Invariants that must always hold
   - Constraints on values

   **Operations:**
   - What each operation does (one sentence)
   - What must be true before it runs (pre-conditions)
   - What becomes true after it runs (post-conditions)

   **Rules & Constraints:**
   - Business rules affecting multiple operations
   - Error conditions and handling
   - Edge cases with special behavior

### Example Output

```
PROVISIONAL SPECIFICATION: AccountManager

DATA MODEL
  [PROVISIONAL] {confidence: high} {source: code}
  An Account stores: customer ID, balance (non-negative), creation date.

  [PROVISIONAL] {confidence: medium} {source: tests}
  Invariant: Once created, customer ID cannot change.

OPERATIONS
  [PROVISIONAL] {confidence: high} {source: code}
  deposit(amount): Adds amount to balance. Requires amount > 0.
  After operation: balance increases by exactly amount.

  [QUESTION] {confidence: medium} {source: code}
  withdraw(amount): Subtracts amount from balance if balance >= amount.
  Question: What happens if withdraw fails due to insufficient funds?
  Current code: throws exception. Is this intended?

RULES & CONSTRAINTS
  [IMPLICIT] {confidence: medium} {source: tests}
  Tests suggest: Negative balances are never allowed.
  Is this a requirement?
```

---

## STEP 2: Structured Dialogue by Category

### Category A: Questions [QUESTION] — Highest Priority

**When to ask:** Code behavior seems wrong, ambiguous, or contradicts user intent.

**Presentation strategy:**
- Lead with concrete behavior: "The code currently does X."
- Never frame as criticism: avoid "the code incorrectly...", "the code fails to..."
- Offer choices: Show what the code does, then ask if it matches intent.

**Question format:**

```
QUESTION: {Brief title}

Current behavior (from code):
{What the code actually does, in plain language}

Is this what you intended?
  (a) Yes, this is correct and should be kept
  (b) No, this is a bug—the behavior should be different
  (c) It's more nuanced—the intended behavior is [user fills in]
  (d) I'm not sure—let's discuss further

Your answer will be recorded as a Finding for action.
```

**Examples:**

```
QUESTION: Refund handling

Current behavior:
When a customer requests a refund, the system throws an exception
if the original transaction cannot be found. The account balance is not changed.

Is this what you intended?
  (a) Yes, refuse refunds for missing transactions
  (b) No, we should still credit the account
  (c) It's more nuanced: [user's clarification]
  (d) Uncertain
```

```
QUESTION: Empty list edge case

Current behavior:
If the input list is empty, the operation skips entirely and returns
the original state unchanged.

Is this what you intended?
  (a) Yes, do nothing on empty input
  (b) No, empty input should be treated differently
  (c) It's more nuanced: [user's clarification]
  (d) Uncertain
```

**Handling "I'm not sure":**
- Mark as [UNRESOLVED] with discussion summary
- Flag for revisit in next iteration
- Don't force a decision now—premature closure is worse than uncertainty
- Ask follow-up: "Should we implement it as-is for now and revisit later, or explore it more?"

### Category B: Implicit Specs [IMPLICIT] — Inferred from Tests/Comments

**When to ask:** Behavior is clear from tests but not explicit in code; business logic is hidden in comments.

**Presentation strategy:**
- Give evidence first: "Tests show that...", "Your comments suggest..."
- Ask for confirmation, not discovery
- Keep batch size reasonable (3-5 at a time)

**Question format:**

```
IMPLICIT REQUIREMENT: {Brief title}

Evidence:
- Tests expect {specific behavior}
- Comments mention {specific constraint}

Is this a real requirement that should be in the spec?
  (a) Yes, this is required
  (b) No, this is incidental—not a true requirement
  (c) It's more nuanced: [user's clarification]
  (d) It was needed once but we can drop it now
```

**Examples:**

```
IMPLICIT REQUIREMENT: Minimum transaction amount

Evidence:
- Tests reject transactions < $0.01
- Comment: "We don't process penny orders"

Is this a real requirement that should be in the spec?
  (a) Yes, enforce $0.01 minimum
  (b) No, this was a workaround—we should process any amount now
  (c) It's more nuanced: the limit should be [user specifies]
  (d) We can drop it now
```

```
IMPLICIT REQUIREMENT: Idempotent API calls

Evidence:
- Tests show same request called twice produces same result
- No error on second call with identical data

Is this a real requirement (safe to call multiple times)?
  (a) Yes, API must be idempotent
  (b) No, this was unintended—second call should error
  (c) It's more nuanced: [user's clarification]
  (d) Uncertain
```

**Batch confirmation:** If multiple implicit specs are low-risk and user understands them clearly, offer batch:

```
These five implicit specs all appear to be basic data validations:
- Min/max constraints on field X
- Uniqueness constraint on field Y
- Non-null requirement on field Z
- Type constraint on field W
- Range constraint on field V

Do you want to confirm all five at once, or review each individually?
```

### Category C: Missing Specs [MISSING] — No Code Exists

**When to ask:** Spec might need to handle something the code doesn't currently handle; or a feature is mentioned in comments but not implemented.

**Critical:** This is where TRUE spec gaps often emerge—things the user assumed but never coded.

**Presentation strategy:**
- Frame neutrally: "The code doesn't currently handle X."
- Offer three responses: Yes (implement it), No (out of scope), or (Clarify what you want)
- This is discovery, not validation

**Question format:**

```
MISSING SPEC: {Brief title}

Current code does NOT handle:
{What the code explicitly does not address}

Should the specification include this?
  (a) Yes, we should handle it—here's what should happen: [user specifies]
  (b) No, this is out of scope for now
  (c) Maybe—let me understand what you mean by that
  (d) I need to think about this
```

**Examples:**

```
MISSING SPEC: Concurrent requests

Current code:
No locking mechanism; unclear if concurrent calls are safe.

Should the specification include concurrency guarantees?
  (a) Yes, we need thread-safety: [user specifies requirements]
  (b) No, single-threaded environment is guaranteed
  (c) Maybe—explain what scenarios you're worried about
  (d) I need to think about this
```

```
MISSING SPEC: Audit logging

Current code:
No audit trail is recorded.

Should the specification include audit logging?
  (a) Yes, we must log all operations: [user specifies what to log]
  (b) No, logging is separate from core logic
  (c) Maybe—what's your use case for audit logs?
  (d) I need to think about this
```

**Handling exploration:** If user says "I need to think," offer to continue with other items and revisit this one later. Don't block convergence on one uncertain item.

### Category D: Provisional Confirmations [PROVISIONAL] — Routine Items

**When to ask:** Mechanically extracted items that are straightforward and low-risk.

**Presentation strategy:**
- Use batch confirmation for efficiency
- Keep questions very brief
- Single-choice confirmation rather than open dialogue

**Question format:**

```
PROVISIONAL CONFIRMATIONS (batch review)

Confirm these items match your intent? (Y/N for each, or bulk Y/N)

- [PROVISIONAL] Accounts have unique IDs: ___
- [PROVISIONAL] Balance is always >= 0: ___
- [PROVISIONAL] deposit() requires amount > 0: ___
```

**Batch acceptance for low-risk items:**

```
All of these appear to be basic data validations with no ambiguity:
1. Field X must be non-null
2. Field Y must be numeric
3. Field Z must be unique
4. Field W must be in range [a, b]

Confirm all four as-is? [Yes / Review individually]
```

---

## STEP 3: Finding Classification

**Definition:** A Finding is any dialogue result that changes, clarifies, or confirms the specification.

### Finding Categories

| Category | Meaning | Action |
|----------|---------|--------|
| **Bug** | Code does something different from user intent | Fix code to match intent |
| **Spec Gap** | Spec should handle something but code doesn't exist | Add code + spec |
| **Spec Refinement** | Spec is vague; needs tighter pre/post/inv | Clarify and strengthen spec |
| **Intentional** | Code matches user intent; was correct all along | Promote [PROVISIONAL] → [CONFIRMED] |
| **Debt** | Not intended, but deferring fix for now | Record as tech debt item |

### Recording Findings

**Template:**

```
FINDING #{N}: {Title}
Category: [Bug | Spec Gap | Spec Refinement | Intentional | Debt]
Severity: [Critical | High | Medium | Low]

Source question/dialogue:
{Reference to the QUESTION, IMPLICIT, or MISSING item}

User's answer:
{Exact user response}

Interpretation:
{Your understanding of what this means for the spec}

Recommended action:
- If Bug: Code change specification + priority
- If Spec Gap: Pseudo-code for missing behavior
- If Spec Refinement: Proposed new/tightened condition
- If Intentional: What to promote in spec
- If Debt: What to track and defer

```

### Example Findings

```
FINDING #1: Refund exception handling
Category: Bug
Severity: High

Source: QUESTION: Refund handling
User's answer: (b) No, we should still credit the account

Interpretation:
Current code throws exception when original transaction is missing.
User expects refund to be credited anyway. This is a logic error.

Recommended action:
Code fix: Remove exception; always credit the refund amount.
Spec addition: "refund(amount) always credits the account,
  regardless of whether original transaction exists."
```

```
FINDING #2: Minimum transaction amount
Category: Intentional
Severity: Low

Source: IMPLICIT REQUIREMENT: Minimum transaction amount
User's answer: (a) Yes, enforce $0.01 minimum

Interpretation:
Test-driven implicit spec is confirmed as real requirement.
Should be promoted to explicit spec.

Recommended action:
Promote to [CONFIRMED] in spec:
  "Pre-condition: amount >= $0.01"
```

```
FINDING #3: Concurrency safety
Category: Spec Gap
Severity: High

Source: MISSING SPEC: Concurrent requests
User's answer: (a) Yes, we need thread-safety for multi-threaded environment

Interpretation:
Current code has no concurrency protection.
User needs concurrent-call safety—this must be added.

Recommended action:
Add operation-level invariants:
  "No two concurrent calls to [operation] shall interfere"
Add implementation guidance:
  "Use mutex locking on shared state"
```

```
FINDING #4: Audit logging
Category: Debt
Severity: Medium

Source: MISSING SPEC: Audit logging
User's answer: (c) Maybe—we should log important operations, but not critical for MVP

Interpretation:
User wants logging eventually but not in current scope.
Should be recorded as tech debt for post-MVP.

Recommended action:
Record in tech debt log:
  "TODO: Add audit logging for all operations
   Priority: Medium (nice-to-have for MVP)
   Estimated effort: 2 days"
```

---

## STEP 4: Confirmed Spec Generation

### Process

1. **Start with provisional spec** (all items tagged [PROVISIONAL])

2. **Apply Findings** in order:
   - Remove or modify items based on Bug/Spec Refinement findings
   - Add new items from Spec Gap findings
   - Promote [PROVISIONAL] → [CONFIRMED] for Intentional findings
   - Add tech debt annotations for Debt findings

3. **Annotate provenance** for every line:
   ```
   [CONFIRMED] {source: confirmed by user in refine-spec dialogue}
   [CONFIRMED] {source: Finding #3 (Spec Gap)}
   [CONFIRMED] {source: Finding #7 (Spec Refinement)}
   ```

4. **Remove meta-tags:**
   - Remove [PROVISIONAL] tags
   - Remove [QUESTION]/[IMPLICIT]/[MISSING] tags
   - Keep only substantive content

5. **File naming:**
   - Provisional: `filename.provisional.vdmsl`
   - Confirmed: `filename.vdmsl` (drop `.provisional`)

### Example Transformation

**Before (Provisional):**
```vdmsl
-- Account.provisional.vdmsl
types
  Account = record
    id: CustomerId
    balance: real
    created: Date
  end
  inv a == a.balance >= 0
  [PROVISIONAL] {confidence: high} {source: code}

operations
  deposit: real +> AccountState
  deposit(amount) ==
    pre amount > 0
    post balance_after = balance_before + amount
    [PROVISIONAL] {confidence: high} {source: code}

  refund: real +> AccountState
  refund(amount) ==
    pre transaction_exists(id)
    post if transaction_exists then balance_after = balance_before + amount
    [QUESTION] {confidence: medium}
    -- What happens if transaction doesn't exist?
```

**After (Confirmed, with Finding #1 applied):**
```vdmsl
-- Account.vdmsl
types
  Account = record
    id: CustomerId
    balance: real
    created: Date
  end
  inv a == a.balance >= 0
  [CONFIRMED] {source: confirmed by user in refine-spec dialogue}

operations
  deposit: real +> AccountState
  deposit(amount) ==
    pre amount > 0
    post balance_after = balance_before + amount
    [CONFIRMED] {source: confirmed by user in refine-spec dialogue}

  refund: real +> AccountState
  refund(amount) ==
    -- Finding #1 (Bug fix): Always credit, regardless of transaction existence
    post balance_after = balance_before + amount
    [CONFIRMED] {source: Finding #1 (Bug)}
```

---

## STEP 5: Convergence Check

### Convergence Criteria

A specification is converged when:

1. ✓ **All [PROVISIONAL] items resolved**
   - Either promoted to [CONFIRMED] or removed
   - No untagged items remain

2. ✓ **All [QUESTION] items answered**
   - Every question category has a Finding
   - User chose (a), (b), or (c)—no (d) uncertain items remain

3. ✓ **All [IMPLICIT] items addressed**
   - Either confirmed or dropped
   - None left unresolved

4. ✓ **All [MISSING] items decided**
   - User said Yes (implement), No (out of scope), or Debt (defer)
   - None left in limbo

5. ✓ **User approves final spec**
   - User reviews confirmed spec
   - Explicitly says "yes, this is the spec" or equivalent

### Non-Convergence: Return to Dialogue

If convergence not achieved:

- **Unresolved items remain:** Offer to loop: "Shall we do another round of dialogue to resolve the remaining items?"
- **New questions emerged:** "Your clarification raised a new question about X. Can we address it?"
- **User says "not ready":** "No problem. Here's what we've confirmed so far, and here's what's still open. We can pick this up again when you're ready."

### Convergence Announcement

When converged:

```
SPECIFICATION CONVERGENCE ACHIEVED

All items resolved:
- [PROVISIONAL]: X items → all promoted to [CONFIRMED]
- [QUESTION]: X items → X bugs, Y refinements, Z intentional
- [IMPLICIT]: X items → all confirmed
- [MISSING]: X items → Y implemented, Z deferred

Findings generated: {total count}
- Bugs: N (code fixes required)
- Spec Gaps: N (new code + spec)
- Spec Refinements: N (spec tightening)
- Intentional: N (confirmed as-is)
- Debt: N (deferred to future)

Confirmed spec ready: {filename}.vdmsl
Findings report: {filename}-findings.md
```

---

## STEP 6: Findings Report Generation

### Report Structure

```markdown
# Findings Report: {Specification Name}

Generated: {Date}
Dialogue rounds: {N}
Total items reviewed: {N}

---

## Executive Summary

{One paragraph: what changed, how significant, next steps}

---

## Finding Categories

### Bugs Found: {N} [CRITICAL IF > 0]

| ID | Title | Severity | Status |
|----|-------|----------|--------|
| #1 | {title} | Critical | Code fix required |
| #2 | {title} | High | Code fix required |

**Details:**

**Finding #1: {Title}**
- **Severity:** Critical
- **User intent:** {What user intended}
- **Current code:** {What it actually does}
- **Recommended code change:** {Specific change}
- **Spec impact:** {What spec line needs updating}

---

### Spec Gaps Found: {N} [IF CRITICAL, HIGHLIGHT]

| ID | Title | Scope | Status |
|----|-------|-------|--------|
| #3 | {title} | Large | Add code + spec |

**Details:**

**Finding #3: {Title}**
- **What's missing:** {What code doesn't handle}
- **User requirement:** {What should happen}
- **Proposed implementation:** {Pseudo-code or spec change}
- **Effort estimate:** {Small / Medium / Large}

---

### Spec Refinements: {N}

| ID | Title | Status |
|----|-------|--------|
| #5 | {title} | Tighten pre-condition |

**Details:**

**Finding #5: {Title}**
- **Current spec:** {Vague condition}
- **Refined spec:** {Tighter condition}
- **Why this matters:** {Impact on correctness}

---

### Intentional (Confirmed As-Is): {N}

| ID | Title |
|----|-------|
| #7 | {title} |

**Details:**

**Finding #7: {Title}**
- **What was questioned:** {Original ambiguity}
- **User confirmation:** {How user confirmed}
- **Spec entry:** {Now [CONFIRMED]}

---

### Tech Debt: {N}

| ID | Title | Priority | Effort |
|----|-------|----------|--------|
| #9 | {title} | Medium | 2 days |

**Details:**

**Finding #9: {Title}**
- **Deferred reason:** {Why not MVP}
- **Future action:** {What to do post-MVP}
- **Prerequisites:** {What must be done first}

---

## Recommended Action Plan

### Critical (Do Now)
- Finding #{N}: {Bug title} — Fix code
- Finding #{N}: {Spec Gap title} — Add code + spec

### High Priority (Sprint)
- Finding #{N}: {title}

### Medium Priority (Later)
- Finding #{N}: {title}

### Tech Debt (Future)
- Finding #{N}: {title}

---

## Spec Changes Summary

### Added to Spec
- {New line or section}
- {New line or section}

### Removed from Spec
- {Old line or section}
- {Old line or section}

### Tightened in Spec
- {Before} → {After}

### Promoted to [CONFIRMED]
- {Item count} provisional items now confirmed

---

## Next Steps

1. {Action 1} (e.g., "Fix code for Finding #1")
2. {Action 2} (e.g., "Implement Finding #3 spec gap")
3. {Action 3} (e.g., "Review refined spec")
4. {Action 4} (e.g., "Run formal verification against new spec")

---

## Appendix: Raw Dialogue

{Complete transcript of all Q&A and user responses}
```

---

## Important Notes & Edge Cases

### 1. Never Assume Code Is Correct

- The code may be wrong, tests may be incomplete, comments may be outdated
- Your job is to surface intent, not defend code
- "The code does X" is neutral; ask "is X what you intended?"

### 2. "I Don't Know" Answers

When user says "I'm not sure":

```
I'm recording this as [UNRESOLVED] for now.

Do you want to:
  (a) Implement it as the code currently does, and revisit later?
  (b) Explore this question more now?
  (c) Leave it unspecified for now and decide later?
```

Don't force closure. Uncertainty is honest and valuable.

### 3. Batch Confirmation Best Practices

**Safe to batch:**
- Multiple data validation constraints (min/max, type checks, non-null)
- Identical behavior patterns across similar operations
- Low-risk items user immediately understands

**NOT safe to batch:**
- Items with conflicting semantics
- Questions about error handling
- Concurrency or timing behavior
- Any item user pauses before answering

**Example batch:**
```
Quick confirms (low-risk):
- All string fields are non-empty: ___ Y/N
- All numeric IDs are positive: ___ Y/N
- All timestamps are ordered: ___ Y/N

Bulk confirm all three? [Yes / Review individually]
```

### 4. Conflicting Requirements

If user's answers contradict:

```
Hold on—I'm seeing a conflict.

Earlier you said:
- Finding #2: "Refunds must always succeed"

But now you're saying:
- Finding #8: "Refunds must fail if no transaction record exists"

These seem to contradict. Can you clarify what should actually happen?
```

Document the conflict and mark both as [UNRESOLVED] until user resolves it.

### 5. Code Behavior Changes During Dialogue

If you realize during dialogue that the code does something different than initially extracted:

```
CORRECTION: I initially extracted behavior X, but reviewing the code more carefully,
it actually does Y. Let me re-ask this question with the correct behavior:

Current behavior (corrected):
{Actual behavior}

Is this what you intended?
```

Show honesty about corrections.

### 6. Spec Ambiguity in Provisional Spec

If the provisional spec itself is ambiguous:

```
PROVISIONAL SPEC AMBIGUITY: The code for Operation X is unclear to me.
It could mean either:
  (A) {Interpretation A}
  (B) {Interpretation B}

Which interpretation matches your intent? Or is it something else?
```

Ask user to clarify before asking if code matches intent.

---

## Engagement Tips

### Pacing
- Don't ask all questions at once—cognitive overload kills dialogue
- Group related items (3-5 per batch)
- Alternate between QUESTION (harder), IMPLICIT (medium), PROVISIONAL (easier)

### Language
- Use user's own words when they clarify things
- Avoid jargon; if you must use it, define it
- "Is this right?" is friendlier than "Confirm this assumption"

### Validation
- Read back what you heard: "So you're saying X should happen?"
- Let user correct your interpretation
- Don't paraphrase—use their exact words in Finding record

### Momentum
- Celebrate convergence: "Great, that's one less ambiguity"
- Show progress: "That's 8 of 12 items resolved"
- Don't rush to closure on uncertain items

---

## Bilingual Support (EN/JP)

**All output and dialogue presented in both languages:**

```
QUESTION: Refund exception handling
例: 払い戻し例外処理

Current behavior:
When a customer requests a refund, the system throws an exception
if the original transaction cannot be found.

現在の動作:
顧客が払い戻しをリクエストすると、元の取引記録が見つからない場合、
システムは例外をスロー（発生）させます。

Is this what you intended?
  (a) Yes, refuse refunds for missing transactions
     はい、紛失した取引については払い戻しを拒否する
  ...
```

Keep format consistent and ensure both translations are equally clear.

---

## Summary Checklist

Before starting dialogue:
- [ ] Provisional spec loaded and organized
- [ ] Items tagged by type (QUESTION, IMPLICIT, MISSING, PROVISIONAL)
- [ ] Confidence levels assigned
- [ ] Organized for efficient dialogue (high-priority first)

During dialogue:
- [ ] Recording every answer as a Finding
- [ ] Classifying each Finding by category
- [ ] Checking for conflicts and ambiguities
- [ ] Pacing at 3-5 items per round
- [ ] Using bilingual presentation

After convergence:
- [ ] All items tagged/resolved
- [ ] Confirmed spec generated with provenance
- [ ] Findings report created with recommended actions
- [ ] User approves final spec
- [ ] File renamed `.vdmsl` (drop `.provisional`)

This skill succeeds when: **The confirmed spec reflects the user's true intent, and every difference between provisional code and that intent is documented as a Finding with a recommended action.**
