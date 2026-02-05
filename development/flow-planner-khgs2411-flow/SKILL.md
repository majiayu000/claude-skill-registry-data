---
name: flow-planner
description: Plan phases, tasks, and iterations. Use when structuring new work, adding features, or organizing development plans.
---

# Flow Planner

Help users plan and structure new work using Flow framework. Guide task structure decisions (standalone vs iterations) and suggest brainstorming for complex features.

## When to Use This Skill

Activate when the user wants to add new work:
- "Add a new task"
- "Plan this feature"
- "Create iterations for..."
- "Break this down into steps"
- "How should we structure this?"
- "Add this to the plan"

## Planning Philosophy

**Flow's Core Principle**: Plan before code. Structure work hierarchically (phases → tasks → iterations) with clear boundaries.

**Key Decision**: Every task is EITHER:
- **Standalone** - Direct action items, no iterations
- **Task with Iterations** - No direct action items, ONLY iterations

**NEVER mix both** - This is the Golden Rule.

## Task Structure Decision Tree

```
User wants to add work
    ↓
Is it complex/multi-step?
    ↓
YES → Task with Iterations
    Break into 3-5 iterations
    Each iteration = milestone
    ↓
NO → Standalone Task
    Direct action items
    Complete in one go
```

## When to Suggest Brainstorming

**Always suggest brainstorming for**:
- Complex features with multiple approaches
- Architectural decisions needed
- Integration with external systems
- Performance-critical features
- Database schema changes
- API contract design
- Security-sensitive features

**Skip brainstorming for**:
- Simple additions (new file, basic function)
- Well-defined tasks (clear requirements)
- Repetitive work (similar to previous tasks)
- Bug fixes with obvious solutions

## Brainstorming Subject Resolution Types

When users DO need brainstorming, help them understand how subjects get resolved:

### Type A: Pre-Implementation Task

**When**: Small blocking code change needed BEFORE iteration starts

**Criteria**: Required for iteration (blocking), small scope (< 30 min), can be done independently

**Examples**: Fix interface, rename file, update enum, fix bug

**What happens**: Action items go into "Pre-Implementation Tasks" section, must complete BEFORE main implementation

### Type B: Immediate Documentation

**When**: Architectural decision that affects system design

**Criteria**: No code changes yet, updates PLAN.md Architecture section NOW

**Examples**: Design pattern choice, API contract, data model

**What happens**: AI updates PLAN.md immediately during brainstorming

### Type C: Auto-Resolved

**When**: Subject answered by another subject's decision

**Criteria**: No independent decision needed, cascade from another subject

**What happens**: No action items, just note which subject resolved this

### Type D: Iteration Action Items

**When**: Substantial feature work that IS the iteration

**Criteria**: Main implementation work, takes significant time (> 30 min)

**Examples**: Build API endpoint, implement validator, create service

**What happens**: These action items become the iteration's implementation action items

## Complexity Indicators

### Simple Task (No Brainstorming)

**Indicators**: Single file change, clear requirements, no integration points, < 1 hour, similar to previous work

**Examples**: "Add validation function", "Fix typo", "Export function", "Add logging"

**Guidance**: "This looks straightforward - standalone task with direct action items. No brainstorming needed."

### Complex Task (Needs Brainstorming)

**Indicators**: Multiple approaches possible, affects architecture, integration needed, > 4 hours, user unsure

**Examples**: "Add authentication", "Integrate Stripe", "Implement caching", "Design database"

**Guidance**: "This is complex - I recommend brainstorming first. Let's discuss: [list 3-5 subjects]."

### Borderline Task (Ask User)

**Indicators**: Moderate complexity (2-4 hours), some design decisions, user hasn't expressed preference

**Examples**: "Add error handling to API", "Refactor data layer", "Implement search"

**Guidance**: "This could go either way. We could brainstorm first, or jump into iterations if you have a clear vision. Which do you prefer?"

## Step-by-Step Planning Workflow

### Step 1: Understand the Request

Ask clarifying questions:
- "What's the goal of this feature?"
- "Are there any constraints or requirements?"
- "Does this build on existing work?"

### Step 2: Determine Complexity

**Simple** → Standalone task
**Complex** → Task with iterations
**Uncertain** → Suggest brainstorming first

### Step 3: Propose Structure

Present options to user:
```
I suggest structuring this as:

**Option A: Standalone Task** - "Add Feature X"
- Direct action items
- Single completion
- Estimated: 1-2 hours

**Option B: Task with 3 Iterations**
- Iteration 1: Basic implementation
- Iteration 2: Add advanced features
- Iteration 3: Polish and optimize
- Estimated: 4-6 hours

Which approach fits better?
```

### Step 4: Create the Structure

Read DASHBOARD.md to find current phase and task count, then create appropriate files:

**For new phase**: Create `.flow/phase-N/` directory, update DASHBOARD.md with new phase entry

**For new task**: Create `.flow/phase-N/task-M.md`, add to DASHBOARD.md progress overview

**For new iteration**: Add iteration section to existing task file

Use templates from [TEMPLATES.md](TEMPLATES.md) for proper structure.

### Step 5: Add Context

Help user fill in:
- **Purpose**: Why this task exists
- **Dependencies**: What it requires/blocks
- **Design Notes**: Key considerations
- **Action Items**: Concrete steps (standalone) or iteration goals (with iterations)

## Starting Work (Phase/Task)

### Starting a Phase

When user wants to begin work on a phase:

1. Read DASHBOARD.md to find the phase
2. Verify phase status is ⏳ PENDING (not already 🚧 IN PROGRESS)
3. Update DASHBOARD.md:
   - Change phase status from ⏳ PENDING to 🚧 IN PROGRESS
   - Update "Current Work" section to point to this phase
4. Report to user: "Phase N: [Name] is now in progress. Starting with Task 1."

### Starting a Task

When user wants to begin work on a task:

1. Read DASHBOARD.md to find the task
2. Verify task status is ⏳ PENDING (not already 🚧 IN PROGRESS)
3. Update task file:
   - Change `**Status**: ⏳ PENDING` to `**Status**: 🚧 IN PROGRESS`
4. Update DASHBOARD.md:
   - Change task status marker from ⏳ to 🚧
   - Update "Current Work" section to point to this task
5. Report to user: "Task N: [Name] is now in progress. [Guidance on first step]"

## Next Action Suggestions

When user asks "what's next" or "what should I work on":

### If Nothing In Progress

Read DASHBOARD.md to find next ⏳ PENDING item:
- If current phase has pending tasks → "Start Task N: [Name]"
- If current phase complete → "Start Phase N+1: [Name]"
- If project complete → "All work complete! 🎉"

### If Work In Progress

Read current work context:
- If task has pending iterations → "Continue with Iteration N"
- If iteration needs planning → "Add iterations to break down the work"
- If unclear → "What aspect would you like to work on next?"

## Task Structure Patterns

See [TEMPLATES.md](TEMPLATES.md) for complete templates:
- **Standalone Task**: Direct action items, no iterations
- **Task with Iterations**: Skeleton → Veins → Flesh pattern
- **Task with Brainstorming**: Design decisions first, then implementation

## Best Practices

1. **Always clarify complexity** - Don't assume, ask user
2. **Suggest iterations for complex work** - Better to break down than have massive tasks
3. **Propose brainstorming when uncertain** - Design first, implement second
4. **Use Flow's metaphor** - Skeleton → Veins → Flesh
5. **Keep iterations focused** - Each should have clear goal and completion criteria

## Task Structure Golden Rules

**DO**:
- ✅ Standalone task with action items
- ✅ Task with iterations (no direct action items)
- ✅ Each iteration has specific goal
- ✅ Iterations build on each other

**DON'T**:
- ❌ Mix action items and iterations in same task
- ❌ Create task with only 1 iteration (make it standalone)
- ❌ Make iterations too large (break down further)
- ❌ Skip brainstorming for complex features

## Iteration Sizing Guidelines

**Good Iteration Size**:
- Completable in 1-2 hours
- Clear completion criteria
- Testable milestone
- Adds incremental value

**Too Large** (split into multiple iterations):
- "Implement entire feature"
- "Build and test everything"
- No clear milestone

**Too Small** (combine or make standalone):
- "Add one line of code"
- "Rename a variable"
- Trivial changes

## Examples

### Example 1: User Asks to Add Feature

```
User: "I want to add real-time notifications"

AI Process:
1. Assess complexity: Complex feature (WebSocket, multiple components)
2. Suggest structure: Task with 3 iterations
3. Propose brainstorming: Technology choice, message format, persistence
4. Create task file with iteration structure

Structure Created:
**Task: Real-Time Notifications** (3 iterations)

**Iteration 1: Skeleton - WebSocket Connection**
- Goal: Establish basic WebSocket connection
- Set up WebSocket server, implement client connection, basic keepalive

**Iteration 2: Veins - Notification System**
- Goal: Core notification sending/receiving
- Design message format, server-side broadcast, client-side handlers

**Iteration 3: Flesh - UI & Polish**
- Goal: User-facing notification display
- Create UI component, add history, implement dismiss/mark-read

Before Starting:
Suggest brainstorming: WebSocket library choice (ws, socket.io, native)? Notification types? Persistence strategy?
```

### Example 2: User Asks to Fix Bug

```
User: "The search filter isn't working correctly"

AI Process:
1. Assess complexity: Simple bug fix (focused scope)
2. Suggest structure: Standalone task
3. Skip brainstorming: Clear requirements
4. Create task file with action items

Task Created:
**Task: Fix Search Filter Bug**

**Action Items**:
- [ ] Reproduce bug with test case
- [ ] Debug filter logic
- [ ] Identify root cause (likely query building)
- [ ] Implement fix
- [ ] Add unit test for this scenario
- [ ] Verify fix resolves issue

Estimated: 1-2 hours
```

### Example 3: Guiding Brainstorming Subject Resolution

```
User: "Let's brainstorm the retry logic for API calls"

AI Response:
Great! Let me suggest subjects to discuss:

Subjects:
1. Retry Strategy - Exponential backoff vs fixed delay?
2. Error Classification - Which errors trigger retry?
3. Max Retry Attempts - How many before giving up?
4. Existing Error Handler - Need to update ErrorHandler.ts for async?
5. Timeout Configuration - Per-request vs total operation?

I'll help categorize each decision by resolution type (A/B/C/D).

---

[After discussing Subject 4...]

User: "We need to update ErrorHandler.ts to support async operations"

AI Response:
This is Type A (Pre-Implementation Task):

✅ Blocking? YES - Can't implement retry without async support
✅ Small? YES - Estimated 20-30 minutes
✅ Independent? YES - Self-contained change

Resolution Type: A

Action Items (Pre-Implementation):
- [ ] Update ErrorHandler.ts to support async operations
- [ ] Add retryAsync() method
- [ ] Update 3 existing call sites
- [ ] Add tests for async error handling

Must complete BEFORE running implementation.

---

[After discussing Subject 1...]

User: "Let's use exponential backoff with base delay of 1 second"

AI Response:
This is Type D (Iteration Action Items):

✅ Substantial work? YES - Core feature implementation
✅ Takes > 30 min? YES - Estimated 2-3 hours
✅ Main iteration work? YES - This IS what we're building

Resolution Type: D

Action Items (Implementation):
- [ ] Create RetryPolicy class
- [ ] Implement exponential backoff algorithm (base: 1s, max: 32s)
- [ ] Add configuration for max retries (default: 3)
- [ ] Integrate with API client
- [ ] Add tests for retry scenarios

These become the iteration's implementation action items.
```

## Files Read/Write

**READ**:
- `.flow/DASHBOARD.md` - Find current phase, count tasks, check structure
- `.flow/phase-N/task-M.md` - Existing tasks (when adding iterations)

**WRITE**:
- `.flow/phase-N/` - Create new phase directories
- `.flow/phase-N/task-M.md` - Create new task files, add iterations
- `.flow/DASHBOARD.md` - Add tasks/phases to progress overview, update status

## Validation Gates

- Before adding phase: Verify previous phase has at least one task
- Before adding task: Verify phase directory exists
- Before starting task/phase: Verify not already IN PROGRESS
- Before adding iteration: Verify task file exists

## References

- **Task Structure Rules**: [TEMPLATES.md](TEMPLATES.md) - Complete templates for all task types
- **Framework Reference**: .flow/framework/DEVELOPMENT_FRAMEWORK.md lines 238-566 (Task structure)
- **Brainstorming Pattern**: .flow/framework/DEVELOPMENT_FRAMEWORK.md lines 1167-1797
