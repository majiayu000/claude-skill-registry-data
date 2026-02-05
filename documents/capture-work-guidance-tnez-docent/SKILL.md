---
name: capture-work-guidance
description: Comprehensive guide for AI agents on proactive documentation capture using /docent:tell
group: docent
keywords: [documentation, capture, tell, work guidance, ai agent guidance]
version: 1.0.0
author: docent
---

# Capture Work Guidance for AI Agents

This runbook provides comprehensive guidance for AI agents on maintaining up-to-date project documentation through proactive use of `/docent:tell`.

## Philosophy: Documentation as Working Memory

Think of docent as your **persistent working memory**. Just as you maintain context within a conversation, docent maintains context **across conversations and sessions**.

**The core principle:** If it's worth knowing later, it's worth capturing now.

## When to Capture: The 5 Critical Moments

### 1. After Completing Work

**Trigger:** You've finished implementing a feature, fixing a bug, or completing any meaningful unit of work.

**What to capture:**

- What was accomplished
- Files/components changed
- Approach taken
- Any trade-offs or decisions made

**Examples:**

```
/docent:tell I completed the authentication module. Implemented JWT-based auth with refresh tokens. Modified src/auth/jwt.ts and src/middleware/auth.ts. Chose JWT over sessions for stateless scalability.

/docent:tell Fixed bug #142 where user profile images weren't loading. Root cause was incorrect CORS headers in nginx config. Updated nginx.conf to allow image/* content types.

/docent:tell Refactored the payment processing service to use the repository pattern. Extracted database logic from PaymentService into PaymentRepository. All tests still passing.
```

**Anti-pattern:** Completing work without documentation

```
❌ [Work is done, agent moves to next task without capturing]
✅ [Work is done, agent captures completion, THEN moves to next task]
```

### 2. When Making Decisions

**Trigger:** You're choosing between alternatives - architectural patterns, libraries, approaches, etc.

**What to capture:**

- The decision made
- Alternatives considered
- Reasoning behind the choice
- Context that influenced the decision

**Examples:**

```
/docent:tell I decided to use Postgres over MongoDB for user data storage. Reasoning: We need ACID transactions for payment processing, and the data model is highly relational. MongoDB would have required complex application-level transaction handling.

/docent:tell Chose to implement rate limiting at the API gateway level rather than per-service. This provides consistent rate limits across all services and reduces code duplication. Trade-off: Less granular control per service.

/docent:tell Selected Vitest over Jest for testing. Vitest has native ESM support which eliminates our current build-time transpilation issues. Migration path is straightforward due to Jest-compatible API.
```

**Why this matters:** Future agents need to understand **why** decisions were made, not just **what** was implemented. This prevents repeatedly re-evaluating the same trade-offs.

### 3. Upon Discovering Insights

**Trigger:** You've learned something important, surprising, or non-obvious about the codebase, tools, or domain.

**What to capture:**

- The insight or learning
- How you discovered it
- Why it matters
- Any implications for future work

**Examples:**

```
/docent:tell I learned that Redis requires AOF (Append-Only File) persistence enabled for data durability. The default RDB snapshots can lose up to 1 minute of data on crash. Updated redis.conf to enable AOF. This is critical for our cache-aside pattern where we store session data.

/docent:tell Discovered that the API rate limit resets at midnight UTC, not per rolling 24-hour window. This explains why we see traffic spikes right after midnight. Should consider implementing a token bucket algorithm for smoother rate limiting.

/docent:tell Found that TypeScript's strict mode was disabled in tsconfig.json. Re-enabling it revealed 47 type errors in the codebase. Many are nullable handling issues. This explains several production bugs we've seen. Need to plan migration to strict mode.
```

**Anti-pattern:** Discovering something valuable but not recording it

```
❌ "Oh, that's interesting" [keeps working, forgets by next session]
✅ "Oh, that's interesting" → /docent:tell [documented for future]
```

### 4. When Encountering Blockers

**Trigger:** You're stuck, need external input, or have discovered a problem you can't immediately solve.

**What to capture:**

- What you're blocked on
- What you've tried
- What information or resources you need
- Impact of the blocker

**Examples:**

```
/docent:tell I'm blocked on implementing OAuth integration. The API documentation is incomplete - it shows the authorization endpoint but not the token exchange flow. Need to reach out to the vendor for complete API specs. This blocks the entire external authentication feature.

/docent:tell Encountered a type error in src/services/payment.ts:47 that I can't resolve. TypeScript expects PaymentMethod to have a 'provider' field but the database schema doesn't include this. Not sure if this is a missing migration or incorrect types. Need to verify with the database schema history.

/docent:tell Tests are failing in CI but passing locally. Suspect it's a timezone-related issue since the failing tests involve date parsing. Local system uses EST, CI uses UTC. Need to investigate if we have timezone-aware date handling.
```

**Why this matters:** Blockers documented immediately prevent duplicate investigation. The next agent (or you in the next session) won't waste time re-discovering the same problem.

### 5. At Natural Breakpoints

**Trigger:** You're about to switch context, end a session, or move to a significantly different task.

**What to capture:**

- Summary of what was accomplished
- Current state (what's done, what's in progress)
- Next steps
- Any context needed for resumption

**Examples:**

```
/docent:tell Session summary: Completed user authentication (JWT implementation), fixed CORS bug in nginx config, and started work on refresh token rotation. All tests passing. Next session: Complete refresh token rotation and add rate limiting to auth endpoints.

/docent:tell Context switch: Pausing work on payment integration to address production bug #157. Payment integration is 60% complete - Stripe SDK integrated, webhook handlers written, but transaction logging not yet implemented. Will resume after bug fix.

/docent:tell End of work session. Today's accomplishments: Migrated 12 components from class components to hooks, updated all related tests, fixed 3 type errors from strict mode. Tomorrow: Continue migration with remaining 8 components in src/dashboard/.
```

**Anti-pattern:** Abrupt context switches without documentation

```
❌ [Production issue interrupts feature work, agent context-switches immediately]
✅ [Production issue arrives, agent documents current state, THEN context-switches]
```

## Capture Patterns: What Makes Good Documentation

### Pattern 1: Specific Over Vague

**Bad:**

```
/docent:tell Fixed the bug
```

**Good:**

```
/docent:tell Fixed bug #142 where user profile images weren't loading. Root cause: incorrect CORS headers in nginx.conf. Updated to allow image/* content types.
```

**Why:** Specific documentation is searchable, understandable, and actionable.

### Pattern 2: Include "Why" Along with "What"

**Bad:**

```
/docent:tell Changed database from MongoDB to Postgres
```

**Good:**

```
/docent:tell Migrated from MongoDB to Postgres because we need ACID transactions for payment processing. MongoDB would require complex application-level transaction handling. Trade-off: Lost flexible schema, gained data consistency guarantees.
```

**Why:** Future agents need to understand the reasoning to avoid questioning or reversing good decisions.

### Pattern 3: Context for Future Agents

**Bad:**

```
/docent:tell Updated the config file
```

**Good:**

```
/docent:tell Updated redis.conf to enable AOF persistence (appendonly yes). Default RDB snapshots can lose up to 1 minute of data on crash, which is unacceptable for session storage. AOF provides better durability at slight performance cost (~10% write throughput).
```

**Why:** Include enough context that a completely new agent can understand the situation without reading the entire codebase.

### Pattern 4: Surface Important Files and Locations

**Bad:**

```
/docent:tell Implemented authentication
```

**Good:**

```
/docent:tell Implemented JWT authentication. Main files: src/auth/jwt.ts (token generation/validation), src/middleware/auth.ts (Express middleware), src/types/auth.ts (TypeScript types). Uses jsonwebtoken library with RS256 signing.
```

**Why:** Concrete file paths make it easy to find and verify the implementation.

## Anti-Patterns: What NOT to Do

### Anti-Pattern 1: "I'll Document It Later"

**Problem:** Later rarely comes, and when it does, you've forgotten critical details.

**Example:**

```
❌ Implement feature → Move to next task → Promise to document later → Never happens
✅ Implement feature → Document immediately → Move to next task
```

**Fix:** Make documentation capture a **mandatory final step** of any work unit.

### Anti-Pattern 2: Assuming Context Is Obvious

**Problem:** What's obvious now won't be obvious in 2 weeks (or to another agent).

**Example:**

```
❌ "Updated the thing in the config"
✅ "Updated nginx.conf to allow CORS for image/* content types"
```

**Fix:** Always assume the reader has zero context about what you just did.

### Anti-Pattern 3: Documentation Debt

**Problem:** Multiple completed tasks with no documentation creates a backlog that's overwhelming to capture later.

**Example:**

```
❌ Complete 5 features → Try to document all at once → Can't remember details → Give up
✅ Complete feature 1 → Document → Feature 2 → Document → ...
```

**Fix:** Document **immediately** after each unit of work. Never batch documentation.

### Anti-Pattern 4: Overly Detailed Implementation Notes

**Problem:** Documenting every line of code or every micro-decision creates noise.

**Example:**

```
❌ "I added a function called getUserById that takes an id parameter and returns..."
✅ "Implemented user service with CRUD operations in src/services/user.ts"
```

**Fix:** Document **what** and **why**, not the granular **how**. Code is self-documenting for implementation details.

## Integration with Existing Workflows

### During Feature Development

```
1. Plan feature (use /docent:ask for context if needed)
2. Implement feature
3. Test feature
4. → /docent:tell [capture completion, decisions, insights]
5. Move to next feature
```

### During Bug Fixing

```
1. Investigate bug
2. → /docent:tell [capture findings: root cause, diagnosis process]
3. Implement fix
4. Test fix
5. → /docent:tell [capture resolution: what was fixed, how, why]
6. Close bug ticket
```

### During Refactoring

```
1. Identify refactoring target
2. → /docent:tell [capture decision: what to refactor, why]
3. Implement refactoring
4. → /docent:tell [capture completion: what changed, benefits, trade-offs]
5. Verify tests
```

### During Research/Exploration

```
1. Research question or technology
2. Evaluate options
3. → /docent:tell [capture findings: options evaluated, pros/cons, recommendation]
4. Make decision
5. → /docent:tell [capture decision: choice made, reasoning]
```

## Frequency Expectations

**Minimum:** Capture at least once per logical unit of work (feature, bug fix, task).

**Recommended:** Capture 3-5 times per work session:

- Session start: Context from previous session
- Mid-session: Progress update, decisions made
- Session end: Summary, next steps

**Optimal:** Capture whenever ANY of the 5 critical moments occur (completion, decision, insight, blocker, breakpoint).

## Verification: Are You Capturing Enough?

Ask yourself these questions at the end of each work session:

1. **Could another agent resume my work without asking questions?**
   - If no: You haven't captured enough context

2. **Have I documented all decisions I made today?**
   - If no: Go back and capture those decisions

3. **Did I learn anything surprising or non-obvious?**
   - If yes and undocumented: Capture those insights

4. **If I read only my captured documentation, would I understand what happened today?**
   - If no: Add more detail to your captures

5. **Are there any incomplete tasks that need context for resumption?**
   - If yes and undocumented: Capture current state and next steps

## Example: A Full Work Session with Good Capture Habits

```
# Session Start
/docent:ask what was I working on yesterday
[Reviews context]

# Feature Work
[Implements authentication feature]
/docent:tell Completed JWT authentication implementation. Main files: src/auth/jwt.ts (token gen/validation), src/middleware/auth.ts (Express middleware). Used RS256 signing with jsonwebtoken library. Tokens expire in 1 hour with refresh token support.

# Decision Point
[Choosing between different token storage strategies]
/docent:tell Decided to store refresh tokens in Redis instead of database. Reasoning: Refresh tokens are accessed on every token refresh request, Redis provides <1ms lookup vs ~10ms for Postgres. Trade-off: Redis failure means users need to re-authenticate, but we have Redis HA setup so acceptable risk.

# Discovery
[Realizes rate limiting is missing]
/docent:tell Discovered that authentication endpoints don't have rate limiting. This is a security risk - allows brute force attacks on login endpoint. Need to add rate limiting middleware before production deployment. Suggest: 5 requests per minute per IP for /auth/login.

# Bug Found
[Encounters type error]
/docent:tell Encountered type error in src/middleware/auth.ts:23 - TypeScript expects User type to have 'roles' field but our database schema only has 'role' (singular). Need to verify if this is a schema migration we're missing or if types are incorrect. Blocking adding role-based authorization.

# Session End
/docent:tell Session summary: Implemented JWT authentication with refresh tokens, chose Redis for token storage, identified missing rate limiting as security concern, and discovered schema mismatch blocking role-based auth. Next session: Resolve User type/schema mismatch, implement rate limiting, add role-based authorization.
```

**Notice:**

- Every significant milestone is captured
- Decisions include reasoning
- Discoveries are documented immediately
- Blockers are clearly stated
- Session ends with clear summary and next steps

## Tools and Templates

### Journal Entry Template

Use the `journal-entry` template for structured daily documentation:

```
/docent:act create journal-entry
```

### Session Summary Template

Use the `agent-session` template for formal session documentation:

```
/docent:act create agent-session
```

### Quick Capture Patterns

Memorize these common patterns:

- **Completion:** `/docent:tell Completed [feature]: [details]`
- **Decision:** `/docent:tell Decided [choice] over [alternatives] because [reasoning]`
- **Insight:** `/docent:tell Learned that [insight] - [why it matters]`
- **Blocker:** `/docent:tell Blocked on [issue] - [what's needed]`
- **Summary:** `/docent:tell Session summary: [accomplishments], [state], [next steps]`

## Conclusion

**Remember:** The goal is not perfect documentation. The goal is **sufficient context** for effective work continuity.

Every `/docent:tell` invocation is an investment in future productivity. The time spent documenting now is multiplied many times over when the next agent (or you in the next session) can pick up work instantly without re-discovery.

**Make proactive capture a habit, not an afterthought.**

---

**Related Resources:**

- Run `/docent:ask` to search existing documentation
- Run `/docent:act bootstrap` to initialize project documentation structure
- Run `/docent:act process-journals` to extract valuable knowledge from journal entries into formal documentation
