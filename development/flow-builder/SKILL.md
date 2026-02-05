---
name: flow-builder
description: Execute implementation work with gate checks and verification. Use when user wants to code, build features, implement iterations, or execute action items. Enforces gates, guides workflow, tracks progress.
---

# Flow Builder

Execute implementation work following Flow framework patterns. This skill guides the build phase: verify readiness → start implementation → execute action items → verify completion → mark complete.

## When to Use This Skill

Activate when the user wants to start coding:
- "Let's implement this"
- "Start coding"
- "Build the feature"
- "Time to write code"
- "Ready to implement"
- "Execute the action items"
- "Begin implementation"

## Implementation Philosophy

**Flow's Core Principle**: Design before code. Implementation happens AFTER brainstorming is complete (if needed) and pre-implementation tasks are done.

**Key Gates**:
- **Pre-Implementation Gate**: Brainstorming must be ✅ COMPLETE (if iteration had brainstorming)
- **Pre-Tasks Gate**: All pre-implementation tasks must be ✅ COMPLETE
- **Verification Gate**: All action items done, tests passing, ready for next work

**Implementation Pattern**: Start → Execute → Verify → Complete

## Pre-Implementation Gate Check

Before starting ANY implementation, verify readiness:

### Check 1: Brainstorming Status (if applicable)

```
IF iteration has brainstorming section:
    IF brainstorming status ≠ ✅ COMPLETE:
        ❌ BLOCK implementation
        SUGGEST: "Brainstorming must be completed first. Use `/flow-next-subject` to continue brainstorming."
    ELSE:
        ✅ PASS gate
ELSE:
    ✅ PASS gate (no brainstorming needed)
```

### Check 2: Pre-Implementation Tasks (if applicable)

```
IF iteration has "Pre-Implementation Tasks" section:
    IF any pre-task status ≠ ✅ COMPLETE:
        ❌ BLOCK implementation
        LIST incomplete pre-tasks
        SUGGEST: "Complete pre-tasks first, then use `/flow-implement-start`"
    ELSE:
        ✅ PASS gate
ELSE:
    ✅ PASS gate (no pre-tasks)
```

### Check 3: Iteration Status

```
IF iteration status = 🚧 IN PROGRESS:
    ✅ PASS (already implementing)
IF iteration status = 🎨 READY or ⏳ PENDING:
    SUGGEST: "Use `/flow-implement-start` to begin implementation"
```

## Implementation Workflow

### Step 1: Start Implementation

**Command**: `/flow-implement-start`

**What it does**:
- Marks iteration 🚧 IN PROGRESS
- Creates "Implementation" section in task file
- Updates DASHBOARD.md current work

**When to suggest**: User is ready to code and gates passed

### Step 2: Execute Action Items

**Sequential Execution**:
1. Read action items from iteration (or brainstorming Type D subjects)
2. Execute each action item in order
3. Check off items as completed: `- [x] Action item`
4. Document progress in "Implementation Notes"

**Parallel Execution** (when safe):
- If action items are independent (no dependencies)
- Example: Creating multiple unrelated files
- Still check off sequentially for tracking

**Handling Blockers**:
```
IF encounter blocker during implementation:
    DOCUMENT blocker in Implementation Notes
    ASSESS severity:
        - Minor (< 15 min fix): Handle and continue
        - Major (> 15 min, out of scope): STOP and notify user
        - Blocking (cannot proceed): Mark iteration ❌ BLOCKED, notify user
```

### Step 3: Verify Completion

Before marking iteration complete, verify:

**Verification Checklist**:
- [ ] All action items checked off (✅)
- [ ] Code compiles/runs without errors
- [ ] Tests passing (if applicable)
- [ ] Files modified documented
- [ ] Implementation notes updated
- [ ] No unresolved blockers

**Testing Strategy** (from PLAN.md):
- Follow Testing Strategy section in PLAN.md
- Run tests according to project conventions
- Document test results in Implementation Notes

### Step 4: Complete Implementation

**Command**: `/flow-implement-complete`

**What it does**:
- Marks iteration ✅ COMPLETE
- Updates completion date
- Updates DASHBOARD.md progress
- Advances to next iteration

**When to suggest**: All verification criteria met

## Implementation Slash Commands

### `/flow-implement-start`

**Use when**: Starting implementation for current iteration

**Prerequisites**:
- Brainstorming ✅ COMPLETE (if applicable)
- Pre-tasks ✅ COMPLETE (if applicable)
- Iteration status = 🎨 READY or ⏳ PENDING

**Effect**:
- Changes iteration status to 🚧 IN PROGRESS
- Creates implementation section in task file
- Updates DASHBOARD.md

### `/flow-implement-complete`

**Use when**: All action items done and verified

**Prerequisites**:
- All action items checked off
- Verification criteria met
- No unresolved blockers

**Effect**:
- Marks iteration ✅ COMPLETE
- Updates completion date
- Advances to next iteration or task

## Action Item Execution Patterns

### Pattern 1: Sequential Implementation

**Use when**: Action items depend on each other

```markdown
Action Items:
- [x] Create database schema
- [x] Implement data access layer (depends on schema)
- [x] Add service layer (depends on DAL)
- [x] Create API endpoints (depends on service)
```

**Approach**:
1. Complete item 1
2. Verify item 1 works
3. Move to item 2
4. Repeat until all done

### Pattern 2: Parallel Implementation

**Use when**: Action items are independent

```markdown
Action Items:
- [ ] Create logger utility
- [ ] Create validator utility
- [ ] Create formatter utility
```

**Approach**:
1. Create all three files
2. Verify each works independently
3. Check off all items

### Pattern 3: Incremental Verification

**Use when**: Complex implementation with multiple steps

```markdown
Action Items:
- [x] Implement basic authentication (VERIFY: can login)
- [x] Add JWT token generation (VERIFY: tokens valid)
- [x] Add token refresh (VERIFY: refresh works)
- [x] Add logout (VERIFY: tokens invalidated)
```

**Approach**:
1. Complete one action item
2. Test/verify immediately
3. Document verification in notes
4. Move to next item

## Pre-Implementation Tasks Pattern

### What Are Pre-Implementation Tasks?

Small blocking tasks (< 30 min) that must be completed BEFORE main iteration work starts.

**Examples**:
- Refactor interface to support new pattern
- Update enum with missing values
- Fix bug in legacy code
- Rename file to match convention

### When to Complete Pre-Tasks

```
IF iteration has "Pre-Implementation Tasks" section:
    FOR EACH pre-task:
        Complete pre-task
        Mark ✅ COMPLETE with date
        Document changes in pre-task section
    ONLY AFTER ALL PRE-TASKS DONE:
        Run /flow-implement-start for main iteration
```

### Pre-Task Structure

```markdown
#### Pre-Implementation Tasks

##### ⏳ Pre-Task 1: Update ErrorHandler to support async

**Why Blocking**: Retry logic requires async error handling

**Scope** (< 30 min):
- Update ErrorHandler.ts with async support
- Add retryAsync() method
- Update 3 call sites

**Files**:
- src/utils/ErrorHandler.ts

---

##### ✅ Pre-Task 1: Update ErrorHandler to support async

**Completed**: 2025-10-30

**Changes Made**:
- Added async support to ErrorHandler class
- Implemented retryAsync() method with exponential backoff
- Updated call sites in BillingService, PaymentService, OrderService
- Added unit tests for async error handling

**Files Modified**:
- src/utils/ErrorHandler.ts (+42 lines)
- tests/utils/ErrorHandler.test.ts (+28 lines)
```

## Verification Best Practices

### What to Verify

**Code Quality**:
- [ ] No syntax errors
- [ ] No linting errors
- [ ] Follows project conventions
- [ ] Code is readable and well-structured

**Functionality**:
- [ ] Feature works as intended
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] No regressions introduced

**Testing**:
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing done (if no automated tests)

**Documentation**:
- [ ] Implementation notes updated
- [ ] Files modified list complete
- [ ] Verification results documented

### When to Mark ❌ BLOCKED

Mark iteration ❌ BLOCKED when:
- External dependency not available
- Blocker requires > 1 hour to resolve
- Need user decision before proceeding
- Technical limitation discovered

**Blocked Pattern**:
```markdown
### ❌ Iteration 2: Error Handling

**Status**: ❌ BLOCKED

**Blocker**: Stripe SDK doesn't support custom retry logic in v12

**Options**:
A) Downgrade to Stripe SDK v11 (supports custom retry)
B) Wait for v13 release (eta 2 weeks)
C) Implement wrapper around SDK calls

**Waiting for**: User decision on approach
```

## Detailed Verification Guidance

For comprehensive guidance on verification, testing patterns, completion criteria, bug documentation, and decision-making, see **[VERIFICATION.md](VERIFICATION.md)**.

That resource includes:
- **Testing Patterns**: Unit testing, integration testing, manual testing checklists, and TDD patterns with complete code examples
- **What "Done" Looks Like**: 6 detailed completion criteria with examples
- **When to Document Bugs and Issues**: Bug documentation templates, severity levels, and fix-immediately vs defer guidance
- **Deciding: ❌ BLOCKED vs Continue**: Decision flowchart, 8 scenarios with examples, and real-world case studies

## Scope Boundary Rules

### When You Discover New Work

During implementation, if you discover issues NOT in current action items:

1. **STOP** - Don't make assumptions
2. **ASSESS** - Categorize the issue:
   - Syntax error in file you're editing? Fix and document
   - Missing functionality? Discuss with user
   - New feature idea? Defer to future iteration
   - Blocking bug? Propose pre-implementation task

3. **NOTIFY** user with structured options:
   - **Option A**: Create pre-implementation task (< 30 min, blocking)
   - **Option B**: Add as new brainstorming subject (design needed)
   - **Option C**: Handle immediately (if user approves)
   - **Option D**: Defer to separate iteration (after current work)

4. **AWAIT** user decision before proceeding

### Example: Scope Boundary Alert

```
⚠️ SCOPE BOUNDARY ALERT

During implementation of Iteration 2 (Error Handling), discovered:

**Issue**: PaymentService.ts uses deprecated error format that conflicts with new retry logic

**Impact**: Cannot complete current action item without addressing this

**Options**:
A) Create pre-implementation task (estimated 20 min):
   - Update PaymentService error format
   - Update 2 call sites
   - Add to Pre-Implementation Tasks section

B) Add as brainstorming subject:
   - Need to design error format standard across all services
   - Affects more than just PaymentService

C) Handle immediately:
   - Fix PaymentService.ts now as part of current work
   - Document change in Implementation Notes

D) Defer to separate iteration:
   - Work around issue for now
   - Create new iteration for error format standardization

Which approach would you prefer?
```

## Common Implementation Patterns

### Pattern: Feature Implementation

```
User: "Let's implement the authentication system"

AI Response:
I'll help you implement the authentication system. Let me check readiness:

✅ Brainstorming Session - COMPLETE (4 subjects resolved)
✅ Pre-Implementation Tasks - COMPLETE (updated User model)
✅ Iteration Status - 🎨 READY

Ready to implement! Use `/flow-implement-start` to begin.

Action items from brainstorming:
1. Create AuthService class
2. Implement login/logout methods
3. Add JWT token generation
4. Integrate with API endpoints
5. Add authentication middleware

Estimated time: 3-4 hours

Should I start implementation?
```

### Pattern: Handling Blockers

```
User: "Start implementing the payment integration"

AI Response:
I'll help you implement payment integration. Let me check readiness:

❌ Pre-Implementation Tasks - INCOMPLETE

Found 2 incomplete pre-tasks:
1. ⏳ Pre-Task 1: Refactor PaymentConfig interface
2. ⏳ Pre-Task 2: Update environment variables

These tasks must be completed before main implementation. Should I help you complete them now?
```

### Pattern: Verification Before Completion

```
User: "Are we done with this iteration?"

AI Response:
Let me verify completion criteria:

✅ All action items checked off (5/5)
✅ Code compiles without errors
✅ Tests passing (unit: 12/12, integration: 3/3)
✅ Files modified documented (4 files)
✅ Implementation notes updated
✅ No unresolved blockers

Verification complete! All criteria met.

Use `/flow-implement-complete` to mark this iteration done and move to the next one.
```

### Pattern: Incremental Progress

```
User: "How's the implementation going?"

AI Response:
Implementation progress for Iteration 2: Error Handling

Completed (3/5):
- [x] Create RetryPolicy class
- [x] Implement exponential backoff algorithm
- [x] Add configuration for max retries

In Progress (1/5):
- [ ] Integrate with StripeClient ← CURRENT (60% done)

Pending (1/5):
- [ ] Add tests for retry scenarios

Estimated completion: 1 hour

Working on integrating RetryPolicy with StripeClient.ts. Will move to tests next.
```

## Examples

### Example 1: Starting Implementation After Brainstorming

```
User: "Let's start building the retry logic"

AI Process:
1. Read current iteration from task file
2. Check brainstorming status: ✅ COMPLETE (4 subjects resolved)
3. Check pre-tasks: ✅ COMPLETE (updated ErrorHandler.ts)
4. Verify iteration status: 🎨 READY

AI Response:
"Ready to start implementation! All gates passed:
✅ Brainstorming complete (4 subjects resolved)
✅ Pre-tasks complete (ErrorHandler updated)
✅ Iteration status: READY

Action items from brainstorming (Type D):
- [ ] Create RetryPolicy class
- [ ] Implement exponential backoff algorithm
- [ ] Add configuration for max retries
- [ ] Integrate with StripeClient
- [ ] Add tests for retry scenarios

Use `/flow-implement-start` to begin, then I'll execute these action items."
```

### Example 2: Handling Incomplete Pre-Tasks

```
User: "Start implementing the payment flow"

AI Process:
1. Read current iteration from task file
2. Check brainstorming: ✅ COMPLETE
3. Check pre-tasks: Found 2 incomplete pre-tasks

AI Response:
"Cannot start implementation yet. Pre-tasks must be completed first:

❌ Pre-Implementation Tasks - INCOMPLETE

Blocking tasks:
1. ⏳ Pre-Task 1: Update PaymentStatus enum - Add PENDING_RETRY and FAILED_PERMANENT states
2. ⏳ Pre-Task 2: Refactor PaymentService.process() - Extract validation logic to separate method

These must be done BEFORE main implementation. Should I complete these pre-tasks now?"

User: "Yes, complete them"

AI Process:
1. Complete Pre-Task 1 (update enum, update switch statements)
2. Mark Pre-Task 1 ✅ COMPLETE with date and changes
3. Complete Pre-Task 2 (extract validation method)
4. Mark Pre-Task 2 ✅ COMPLETE with date and changes
5. Verify all pre-tasks done

AI Response:
"All pre-tasks completed:
✅ Pre-Task 1: PaymentStatus enum updated (4 files modified)
✅ Pre-Task 2: Validation logic extracted (2 files modified)

Now ready for main implementation. Use `/flow-implement-start` to begin."
```

### Example 3: Verification Before Marking Complete

```
User: "I think we're done with this iteration"

AI Process:
1. Read current iteration action items
2. Check completion status
3. Verify each completion criterion

AI Response:
"Let me verify completion criteria:

✅ Action Items (5/5):
  - [x] Create RetryPolicy class
  - [x] Implement exponential backoff algorithm
  - [x] Add configuration for max retries
  - [x] Integrate with StripeClient
  - [x] Add tests for retry scenarios

✅ Code Quality:
  - No syntax errors
  - Linting passed
  - Follows project conventions

✅ Tests:
  - Unit tests: 8/8 passing
  - Integration tests: 2/2 passing

✅ Documentation:
  - Files modified documented (4 files)
  - Implementation notes updated

All verification criteria met! Use `/flow-implement-complete` to mark this iteration complete."
```

### Example 4: Scope Boundary During Implementation

```
User: [AI is implementing action items]

AI Process:
1. Working on "Integrate RetryPolicy with StripeClient"
2. Discovers PaymentService.ts uses deprecated error format
3. Realizes this is out of scope

AI Response:
"⚠️ SCOPE BOUNDARY ALERT

While integrating RetryPolicy with StripeClient, I discovered:

**Issue**: PaymentService.ts uses deprecated error format that conflicts with new retry logic

**Impact**: Current action item can continue, but this will cause issues when we add retry to PaymentService later

**Options**:
A) Create pre-implementation task for NEXT iteration:
   - Estimated: 20-30 minutes
   - Update PaymentService error format
   - Update 3 call sites

B) Add as new brainstorming subject:
   - Design error format standard across all services
   - Affects PaymentService, BillingService, OrderService

C) Handle immediately (expand current scope):
   - Fix PaymentService.ts now
   - Document as scope expansion

D) Defer to separate iteration:
   - Work around for now (document workaround)
   - Create new task for error format standardization

I recommend Option A (pre-task for next iteration) as it's small and blocking for future work. Which approach would you prefer?"
```

## Interaction with Other Flow Skills

**Design Stage** (flow-designer Skill):
- `/flow-brainstorm-start` - Design decisions
- `/flow-brainstorm-complete` - Generate action items

**Build Stage** (This Skill):
- `/flow-implement-start` - Begin work ← YOU ARE HERE
- `/flow-implement-complete` - Finish iteration ← YOU ARE HERE

**Navigation Stage** (flow-navigator Skill):
- `/flow-status` - Check progress
- `/flow-next` - What to do next

## References

- **Implementation Pattern**: DEVELOPMENT_FRAMEWORK.md lines 1798-1836
- **Status Markers**: DEVELOPMENT_FRAMEWORK.md lines 1872-1968
- **Brainstorming Pattern**: DEVELOPMENT_FRAMEWORK.md lines 1167-1797
- **Pre-Implementation Tasks**: DEVELOPMENT_FRAMEWORK.md lines 1683-1723
- **Scope Boundary Rules**: DEVELOPMENT_FRAMEWORK.md lines 339-540

## Implementation Gate Checklist

Before implementing, verify ALL gates passed:

```
[ ] Brainstorming complete (if applicable)
[ ] Pre-implementation tasks complete (if applicable)
[ ] Current iteration status = 🎨 READY or ⏳ PENDING
[ ] User confirmed ready to implement
```

If ALL checked → Use `/flow-implement-start`

If ANY unchecked → Address blockers first

## Completion Checklist

Before marking complete, verify ALL criteria met:

```
[ ] All action items checked off
[ ] Code compiles/runs
[ ] Tests passing
[ ] Files modified documented
[ ] Implementation notes updated
[ ] No unresolved blockers
[ ] Verification completed
```

If ALL checked → Use `/flow-implement-complete`

If ANY unchecked → Continue implementation
