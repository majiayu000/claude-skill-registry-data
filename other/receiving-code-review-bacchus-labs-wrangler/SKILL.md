---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (explicit CLAUDE.md violation)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implementing-issue that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implementing-issue anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Source-Specific Handling

### From your human partner
- **Trusted** - implementing-issue after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From External Reviewers
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**your human partner's rule:** "External feedback - be skeptical, but check carefully"

## YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implementing-issue properly
```

**your human partner's rule:** "You and reviewer both report to me. If we don't need this feature, don't add it."

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implementing-issue in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with your human partner's architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Involve your human partner if architectural

**Signal if uncomfortable pushing back out loud:** "Strange things are afoot at the Circle K"

## Acknowledging Correct Feedback

When feedback IS correct:
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** Actions speak. Just fix it. The code itself shows you heard the feedback.

**If you catch yourself about to write "Thanks":** DELETE IT. State the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## Real Examples

**Performative Agreement (Bad):**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**Technical Verification (Good):**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI (Good):**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Unclear Item (Good):**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## Extended Example: Receiving Feedback with Technical Rigor

### Scenario 1: Verifying "Valid" Concern

**Reviewer:** "IMPORTANT: Missing progress reporting for long-running operations."

**You (Verify first):**

1. Check operation duration:
   - Tested with 10,000 items: 2.3 seconds
   - Tested with 100,000 items: 24 seconds

2. User experience impact:
   - Operations >10s appear frozen without feedback
   - Progress reporting is valuable for 100k+ items

3. Implementation cost:
   - Logging every item: expensive (24s becomes 40s)
   - Report every 100 items: reasonable (every ~250ms)

**Verification result:** Valid concern for 100k+ datasets

**Response to reviewer:**
```
"Verified with 100k items - operation takes 24s which would appear frozen. I'll add progress reporting every 100 items (approximately every 250ms). Implementation: log to console with percentage complete."
```

**Notice:** No "great point!" - just verification work and technical decision.

---

### Scenario 2: Cost-Benefit Analysis Leading to Pushback

**Reviewer:** "Consider making chunk size configurable instead of hardcoded 100."

**You (Verify first):**

1. Is there a use case for different chunk sizes?
   - Current: 100 items per batch
   - Why 100? Based on memory testing (1MB per 100 items)
   - Different sizes: Could help if memory constrained

2. What's the cost?
   - Add parameter: `{ chunkSize?: number }`
   - Add validation (10 ≤ chunkSize ≤ 1000)
   - Add tests for different chunk sizes
   - Document safe ranges
   - Cost: ~30 min implementation, ongoing maintenance

3. What's the benefit?
   - Users with limited memory: use chunkSize: 10
   - Users wanting speed: use chunkSize: 500
   - Benefit: Flexibility for edge cases

**Cost-benefit analysis:** Low benefit (most users fine with 100), medium cost (validation, testing, docs)

**Verification result:** Not worth implementing currently

**Response to reviewer:**
```
"I analyzed cost vs benefit. Chunk size of 100 is based on memory testing (1MB per 100 items). Making it configurable adds ~30 min implementation + ongoing maintenance (validation, tests, docs) but benefit is low since most users don't need to change it. I think keeping it internal and optimizing for the common case is better. If we get user requests for configurability, we can add it later. Do you have a specific use case I'm missing?"
```

**Notice:** Pushing back with technical reasoning, not accepting immediately as "good idea".

---

### Scenario 3: Recognizing Incorrect Suggestion and Pushing Back

**Reviewer:** "You should use Promise.all() instead of sequential processing for better performance."

**You (Verify first):**

1. Current implementation:
   ```typescript
   for (const conversation of conversations) {
     await verifyConversation(conversation); // Sequential
   }
   ```

2. Reviewer suggests:
   ```typescript
   await Promise.all(
     conversations.map(c => verifyConversation(c)) // Parallel
   );
   ```

3. Why current is sequential:
   - verifyConversation() writes to database
   - Database has connection pool limit (10 connections)
   - 10,000 conversations = 10,000 concurrent writes = pool exhaustion
   - Sequential: slow but safe
   - Parallel: fast but crashes with "too many connections"

**Verification result:** Reviewer suggestion would break the system

**Response to reviewer:**
```
"I don't think Promise.all() would work here. verifyConversation() writes to the database, and we have a connection pool limit of 10. Processing 10,000 conversations in parallel would exhaust the pool and crash. Current sequential approach is intentionally conservative. If we want better performance, we'd need batched parallelism (process 10 at a time) rather than full parallelism. Should I implementing-issue batched parallelism, or is sequential acceptable?"
```

**Reviewer:** "Oh, good point. I didn't realize it was writing to DB. Sequential is fine."

**You:** "Keeping it sequential then."

**Notice:** No apology for pushing back. Just state the technical reality and move on.

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implementing-issue.

No performative agreement. Technical rigor always.
