---
name: continuity-ledger
description: |
  Create or update continuity ledger for state preservation across /clear operations.
  Ledgers maintain session state externally, surviving context resets with full fidelity.

trigger: |
  - Before running /clear
  - Context usage approaching 70%+
  - Multi-phase implementations (3+ phases)
  - Complex refactors spanning multiple sessions
  - Any session expected to hit 85%+ context

skip_when: |
  - Quick tasks (< 30 min estimated)
  - Simple single-file bug fixes
  - Already using handoffs for cross-session transfer
  - No multi-phase work in progress
---

# Continuity Ledger

Maintain a ledger file that survives `/clear` for long-running sessions. Unlike handoffs (cross-session), ledgers preserve state within a session.

**Why clear instead of compact?** Each compaction is lossy compression - after several compactions, you're working with degraded context. Clearing + loading the ledger gives you fresh context with full signal.

## When to Use

- Before running `/clear`
- Context usage approaching 70%+
- Multi-day implementations
- Complex refactors you pick up/put down
- Any session expected to hit 85%+ context

## When NOT to Use

- Quick tasks (< 30 min)
- Simple bug fixes
- Single-file changes
- Already using handoffs for cross-session transfer

## Ledger Location

Ledgers are stored in: `$PROJECT_ROOT/.ring/ledgers/`
Format: `CONTINUITY-<session-name>.md`

**Use kebab-case for session name** (e.g., `auth-refactor`, `api-migration`)

## Process

### 1. Determine Ledger File

Check if a ledger already exists:
```bash
ls "$PROJECT_ROOT/.ring/ledgers/CONTINUITY-"*.md 2>/dev/null
```

- **If exists**: Update the existing ledger
- **If not**: Create new file with the template below

### 2. Create/Update Ledger

**REQUIRED SECTIONS (all must be present):**

```markdown
# Session: <name>
Updated: <ISO timestamp>

## Goal
<Success criteria - what does "done" look like?>

## Constraints
<Tech requirements, patterns to follow, things to avoid>

## Key Decisions
<Choices made with brief rationale>
- Decision 1: Chose X over Y because...
- Decision 2: ...

## State
- Done:
  - [x] Phase 1: <completed phase>
  - [x] Phase 2: <completed phase>
- Now: [->] Phase 3: <current focus - ONE thing only>
- Next:
  - [ ] Phase 4: <queued item>
  - [ ] Phase 5: <queued item>

## Open Questions
- UNCONFIRMED: <things needing verification after clear>
- UNCONFIRMED: <assumptions that should be validated>

## Working Set
<Active files, branch, test commands>
- Branch: `feature/xyz`
- Key files: `src/auth/`, `tests/auth/`
- Test cmd: `npm test -- --grep auth`
- Build cmd: `npm run build`
```

### 3. Checkbox States

| Symbol | Meaning |
|--------|---------|
| `[x]` | Completed |
| `[->]` | In progress (current) |
| `[ ]` | Pending |

**Why checkboxes in files:** TodoWrite survives compaction, but the *understanding* around those todos degrades each time context is compressed. File-based checkboxes are never compressed - full fidelity preserved.

### 4. Real-Time Update Rule (MANDATORY)

**⛔ HARD GATE: Update ledger IMMEDIATELY after completing ANY phase.**

You (the AI) are the one doing the work. You know exactly when:
- A phase is complete
- A decision is made
- An open question is resolved

**There is NO excuse to wait for the user to ask.** This is the same discipline as `TodoWrite` - update in real-time.

| After This Event | MUST Do This | Before |
|------------------|--------------|--------|
| Complete a phase | Mark `[x]`, move `[->]` to next | Proceeding to next phase |
| All phases done | Add `Status: COMPLETED` | Telling user "done" |
| Make key decision | Add to Key Decisions section | Moving on |
| Resolve open question | Change UNCONFIRMED → CONFIRMED | Proceeding |

**Anti-Rationalization:**

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "I'll update after I finish" | You'll forget. State drifts. User asks why ledger is stale. | **Update NOW** |
| "It's just one phase" | One phase becomes three. Ledger shows Phase 2 when you're on Phase 5. | **Update NOW** |
| "User will ask me to update" | User shouldn't have to. You're the AI doing the work. You know. | **Update NOW** |
| "I'm in the flow, don't want to stop" | 10 seconds to update vs. explaining why ledger is wrong later. | **Update NOW** |

### 5. Update Guidelines

**When to update the ledger:**
- **IMMEDIATELY after completing a phase** (MANDATORY - see above)
- Session start: Read and refresh
- After major decisions
- Before `/clear`
- At natural breakpoints
- When context usage >70%

**What to update:**
- Move completed items from "Now" to "Done" (change `[->]` to `[x]`)
- Update "Now" with current focus
- Add new decisions as they're made
- Mark items as UNCONFIRMED if uncertain
- Add `Status: COMPLETED` when all phases done

### 6. After Clear Recovery

When resuming after `/clear`:

1. **Ledger loads automatically** (SessionStart hook)
2. **Find `[->]` marker** to see current phase
3. **Review UNCONFIRMED items**
4. **Ask 1-3 targeted questions** to validate assumptions
5. **Update ledger** with clarifications
6. **Continue work** with fresh context

## Template Response

After creating/updating the ledger, respond:

```
Continuity ledger updated: .ring/ledgers/CONTINUITY-<name>.md

Current state:
- Done: <summary of completed phases>
- Now: <current focus>
- Next: <upcoming phases>

Ready for /clear - ledger will reload on resume.
```

## UNCONFIRMED Prefix

Mark uncertain items explicitly:

```markdown
## Open Questions
- UNCONFIRMED: Does the auth middleware need updating?
- UNCONFIRMED: Are we using v2 or v3 of the API?
```

After `/clear`, these prompt you to verify before proceeding.

## Comparison with Other Tools

| Tool | Scope | Fidelity |
|------|-------|----------|
| CLAUDE.md | Project | Always fresh, stable patterns |
| TodoWrite | Turn | Survives compaction, but understanding degrades |
| CONTINUITY-*.md | Session | External file - never compressed, full fidelity |
| Handoffs | Cross-session | External file - detailed context for new session |

## Example

```markdown
# Session: auth-refactor
Updated: 2025-01-15T14:30:00Z

## Goal
Replace JWT auth with session-based auth. Done when all tests pass and no JWT imports remain.

## Constraints
- Must maintain backward compat for 2 weeks (migration period)
- Use existing Redis for session storage
- No new dependencies

## Key Decisions
- Session tokens: UUID v4 (simpler than signed tokens for our use case)
- Storage: Redis with 24h TTL (matches current JWT expiry)
- Migration: Dual-auth period, feature flag controlled

## State
- Done:
  - [x] Phase 1: Session model
  - [x] Phase 2: Redis integration
  - [x] Phase 3: Login endpoint
- Now: [->] Phase 4: Logout endpoint and session invalidation
- Next:
  - [ ] Phase 5: Middleware swap
  - [ ] Phase 6: Remove JWT
  - [ ] Phase 7: Update tests

## Open Questions
- UNCONFIRMED: Does rate limiter need session awareness?

## Working Set
- Branch: `feature/session-auth`
- Key files: `src/auth/session.ts`, `src/middleware/auth.ts`
- Test cmd: `npm test -- --grep session`
```

## Additional Notes

- **Keep it concise** - Brevity matters for context
- **One "Now" item** - Forces focus, prevents sprawl
- **UNCONFIRMED prefix** - Signals what to verify after clear
- **Update frequently** - Stale ledgers lose value quickly
- **Clear > compact** - Fresh context beats degraded context
