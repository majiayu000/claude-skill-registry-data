---
name: lcmp_recommendation
description: Suggest LCMP compaction when explicitly requested - provides guidance on promoting durable information to decisions.md, insights.md, and gotchas.md without auto-compaction
schema_version: 1.0
---

# lcmp_recommendation

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK (all modes)
**Priority:** Low

## Trigger Reference

This skill activates on:
- Keywords: "/squish", "compaction", "LCMP", "context cleanup", "context compaction"
- Intent patterns: "compact.*?context", "LCMP.*(compaction|cleanup)", "/squish"

From: `skill-rules.json` - lcmp_recommendation configuration

## Purpose

Suggest LCMP (Lean Context Master Pattern) compaction when explicitly requested by the user. This skill NEVER auto-compacts but provides guidance on what information should be promoted to LCMP Tier-1 docs (decisions.md, insights.md, gotchas.md).

## Core Behavior

In any DAIC mode, when explicitly requested:

1. **Compaction Opportunity Analysis**
   - Review recent work context (completed tasks, discussions, learnings)
   - Identify information that:
     - Survived at least one DAIC cycle
     - Affects future work (designs, constraints, tradeoffs)
     - Represents recurring patterns or expensive gotchas
   - Flag information that's ephemeral vs. durable

2. **LCMP Categorization Suggestions**
   - **decisions.md** - Architectural decisions, tradeoffs, rationale
   - **insights.md** - Patterns, learnings, best practices discovered
   - **gotchas.md** - Pitfalls, failure modes, edge cases encountered

3. **Recommendation Presentation**
   - List candidate information for each LCMP file
   - Explain why each item is worth preserving
   - Show proposed format/structure
   - Wait for user approval before any action

4. **User-Driven Compaction**
   - Only compact when user explicitly says "yes" / "squish" / "do it"
   - Never auto-compact based on context usage or heuristics
   - After user approval, suggest specific edits to LCMP files
   - Verify user reviews and approves actual changes

## Safety Guardrails

**ANALYSIS-ONLY RULES:**
- ✓ NEVER call write tools (Edit, Write, MultiEdit)
- ✓ NEVER auto-compact without explicit user approval
- ✓ NEVER bypass user review of proposed changes
- ✓ Only provide analysis and recommendations
- ✓ Safe to run in any DAIC mode

**LCMP Preservation Rules:**
- Only suggest promoting durable information
- Avoid promoting ephemeral details (e.g., specific file paths that change often)
- Preserve existing LCMP content (additive, not replacement)
- Maintain chronological order in LCMP files
- Include context dates and references

**Anti-Auto-Compaction:**
- NEVER trigger on context percentage thresholds
- NEVER trigger on elapsed time
- NEVER trigger on task count
- ONLY trigger on explicit user request

## Examples

### When to Activate

✓ User explicitly types: "/squish"
✓ "Compact the context into LCMP files"
✓ "What should we preserve from this session?"
✓ "Squish this into decisions.md"
✓ After major epic completes and user asks: "What did we learn?"

### Typical Output

**Scenario: Compaction Recommendation After Feature**
```markdown
### LCMP Compaction Recommendation

I've reviewed the recent work on the authentication feature. Here's what I suggest preserving in LCMP files:

---

#### For `context/decisions.md`:

**1. JWT vs. Session Cookies Decision**
```markdown
### Authentication Strategy: 2025-11-15
- **Decision:** Use JWT with httpOnly cookies instead of localStorage
- **Rationale:**
  - XSS protection (cookies not accessible to JS)
  - CSRF mitigation with SameSite=Strict
  - Refresh token rotation for security
- **Tradeoffs:**
  - ✓ More secure than localStorage
  - ✗ More complex token refresh logic
  - ✗ Requires backend cookie management
- **Alternative Considered:** Session cookies (rejected due to scalability concerns)
- **Context:** Task m-implement-auth-2025-11-15
```

**2. Password Hashing Choice**
```markdown
### Password Hashing: bcrypt vs. argon2: 2025-11-15
- **Decision:** Use bcrypt with cost factor 12
- **Rationale:**
  - Well-tested, widely supported
  - Good balance of security and performance
  - Node.js bcrypt library is mature
- **Tradeoffs:**
  - ✓ Standard choice, no surprises
  - ✗ argon2 is slightly more secure
  - ✗ bcrypt sensitive to long passwords (>72 bytes)
- **Prevention:** Document max password length (72 chars)
- **Context:** Auth implementation discussion
```

---

#### For `context/insights.md`:

**1. Express Async Error Handling Pattern**
```markdown
### Async Handler Wrapper Pattern: 2025-11-15
**Learning:** All async Express routes need error boundary

**Pattern Discovered:**
```javascript
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

**Why This Matters:**
- Unhandled promise rejections crash the server
- Express doesn't catch async errors by default
- This pattern standardizes error handling

**Application:**
- Use for all async routes
- Combine with Sentry for error tracking
- Document in API development guide
```

---

#### For `context/gotchas.md`:

**1. bcrypt Async Import Gotcha**
```markdown
### bcrypt Must Use Async Methods: 2025-11-15
**Problem:** Using bcrypt.hashSync() in async functions blocks event loop

**Symptom:**
- API requests hang during password hashing
- Server becomes unresponsive under load

**Root Cause:**
- bcrypt.hashSync() is CPU-intensive and blocks Node.js event loop
- Should use bcrypt.hash() (async) instead

**Fix:**
```javascript
// ❌ WRONG - blocks event loop
const hash = bcrypt.hashSync(password, 12);

// ✅ CORRECT - non-blocking
const hash = await bcrypt.hash(password, 12);
```

**Prevention:**
- Always use async bcrypt methods in async functions
- Lint rule: no-sync-in-async-function
- Document in auth implementation guide
```

---

**Would you like me to add these to LCMP files?**
(Requires explicit approval and IMPLEMENT mode)
```

**Scenario: User Declines**
```markdown
### LCMP Compaction: User Declined

No problem! I won't make any changes to LCMP files.

**When to compact:**
- After completing major features/epics
- When patterns are solidified (not while experimenting)
- When learnings are durable (not one-off fixes)

You can always trigger compaction later with: /squish
```

### When NOT to Activate

✗ Context usage high (never auto-suggest based on %)
✗ Task completed (never auto-suggest based on completion)
✗ User didn't explicitly request compaction
✗ User is just asking about LCMP files (not requesting compaction)

## Compaction Criteria

### Information Worth Preserving

**YES - Promote to LCMP:**
- Architectural decisions with rationale
- Patterns that apply to multiple features
- Gotchas that are expensive to rediscover
- Constraints that affect future work
- Tradeoffs between competing approaches

**NO - Keep Ephemeral:**
- Specific file paths (change often)
- Temporary workarounds
- One-off debugging steps
- Implementation details (belong in code comments)
- Task-specific TODOs

### Decision Quality Check

Before suggesting a decision for LCMP:
- ✓ Decision affects multiple features
- ✓ Rationale is clear and documented
- ✓ Tradeoffs are explained
- ✓ Alternatives were considered
- ✓ Context is provided

### Insight Quality Check

Before suggesting an insight for LCMP:
- ✓ Pattern applies broadly
- ✓ Learning is non-obvious
- ✓ Costs significant time to rediscover
- ✓ Example code helps explain it
- ✓ Application guidance is clear

### Gotcha Quality Check

Before suggesting a gotcha for LCMP:
- ✓ Problem is recurring or expensive
- ✓ Root cause is explained
- ✓ Fix is clear and tested
- ✓ Prevention strategy noted
- ✓ Context helps identify similar issues

## LCMP File Formats

### decisions.md Format
```markdown
### [Decision Title]: [YYYY-MM-DD]
- **Decision:** [What was decided]
- **Rationale:** [Why this decision]
- **Tradeoffs:**
  - ✓ [Advantage 1]
  - ✗ [Disadvantage 1]
- **Alternatives Considered:** [What else was considered]
- **Context:** [Task/issue reference]
```

### insights.md Format
```markdown
### [Pattern/Learning Title]: [YYYY-MM-DD]
**Learning:** [One-line summary]

**Pattern Discovered:**
[Code example or description]

**Why This Matters:**
[Explanation of importance]

**Application:**
[How/when to use this]
```

### gotchas.md Format
```markdown
### [Gotcha Title]: [YYYY-MM-DD]
**Problem:** [What goes wrong]

**Symptom:**
[Observable behavior]

**Root Cause:**
[Why it happens]

**Fix:**
[Code or solution]

**Prevention:**
[How to avoid in future]
```

## User Approval Flow

1. **Analyze** → Review context, identify candidates
2. **Suggest** → Present recommendations with formatting
3. **Wait** → User must explicitly approve
4. **Implement** → Only after approval (requires IMPLEMENT mode)
5. **Verify** → User reviews actual LCMP changes

Never skip steps 3 & 4 (user approval is mandatory).

## Decision Logging

When compaction is performed:

```markdown
### LCMP Compaction Performed: [Date]
- **Trigger:** User explicitly requested ("/squish")
- **Files Updated:** decisions.md, insights.md, gotchas.md
- **Items Added:** 2 decisions, 1 insight, 1 gotcha
- **Context Saved:** ~45% reduction in session context
- **Review:** User approved all additions
```

## Related Skills

- **framework_health_check** - Checks LCMP freshness (but doesn't suggest compaction)
- **cc-sessions-core** - For understanding DAIC/LCMP relationship
- **framework_repair_suggester** - If LCMP files are corrupted or missing

---

**Last Updated:** 2025-11-15
**Framework Version:** 2.0
