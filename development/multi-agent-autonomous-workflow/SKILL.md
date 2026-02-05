---
name: multi-agent-autonomous-workflow
description: Long-running autonomous workflow for feature implementation. Runs until complete with minimal human intervention.
---

# Long-Running Autonomous Workflow

Run for hours until the goal is complete. The Stop hook blocks exit until done.

## Core Execution Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    LONG-RUNNING EXECUTION                        │
│                                                                  │
│  1. ANALYZE: Break goal into stories                            │
│  2. LOOP: For each story, iterate until verified                │
│  3. COMPLETE: All stories done → create PR → WORKFLOW_COMPLETE  │
│                                                                  │
│  Stop hook blocks exit until WORKFLOW_COMPLETE marker output    │
└─────────────────────────────────────────────────────────────────┘
```

## Guiding Principles

1. **Persist state** - Survive any interruption
2. **Verify before progressing** - Build and tests must pass
3. **Learn from failures** - Use failures as context for retry
4. **Escalate when stuck** - Don't loop forever, ask for help
5. **Think before acting** - Reason about risks, don't just execute

**Everything else is agent reasoning.** You already know about flaky tests, merge conflicts, external dependencies, performance issues. Use that knowledge.

---

## Workflow Steps

### Phase 0: Recovery Check

```bash
python .claude/core/state.py recover
```

If resuming, continue from where you left off.

### Phase 1: Analysis

1. **Explore codebase first** - Before asking questions, understand:
   - Project structure and architecture
   - Existing patterns and conventions
   - Related code that might be affected
   - What already exists vs what needs building

2. **Ask informed questions** (use AskUserQuestion tool)

   Based on codebase analysis, ask specific questions like:
   - "I see you have X pattern. Should the new feature follow this?"
   - "This will affect modules A, B, C. Any concerns?"
   - "I found existing Y. Should I extend it or build new?"

   Not generic questions like "What framework?" - you already know from the code.

3. **Initialize workflow:**
   ```bash
   python .claude/core/state.py init "Goal description"
   ```

4. **Break goal into stories:**
   ```bash
   python .claude/core/state.py add-story "Story title" --size M
   ```

### Phase 2: Story Loop

For each story:

1. **Start story:**
   ```bash
   python .claude/core/state.py update S1 in_progress
   ```

2. **Implement with TDD** (write test → make it pass → refactor)

3. **Verify (MANDATORY):**
   ```bash
   # Get platform commands
   BUILD_CMD=$(python .claude/core/platform.py get-command build)
   TEST_CMD=$(python .claude/core/platform.py get-command test)

   # Run them
   eval "$BUILD_CMD" && eval "$TEST_CMD"
   ```

4. **If verification fails:** Don't exit. Use the failure as context. Try again.

5. **If verification passes:**
   ```bash
   python .claude/core/state.py verify S1 buildPasses --passed
   python .claude/core/state.py verify S1 testsPasses --passed
   python .claude/core/state.py update S1 completed
   ```

6. **Repeat** until no incomplete stories remain.

### Phase 3: Completion

1. **Final verification** - Build + test must pass
2. **Create PR** with summary of changes
3. **Complete workflow:**
   ```bash
   python .claude/core/state.py complete
   ```
4. **Output completion marker:**
   ```
   ## WORKFLOW_COMPLETE

   PR created. All stories verified.
   ```

---

## Handling Problems

### Build/Test Fails
Don't exit. Analyze the error. Fix it. Try again.

### Stuck After 3+ Attempts
```bash
python .claude/core/state.py blocker "Description of what's blocking"
```
Escalate to user or try a different approach.

### Need Human Action
```bash
python .claude/core/state.py await-user "What needs to be fixed" --check "verification command"
```
Stop hook will allow exit. User fixes issue, runs `user-fix-complete`, restarts.

### External Dependencies
Think about what's needed. Mock it for tests. If credentials required, use await-user.

---

## State Commands

```bash
# Lifecycle
python .claude/core/state.py init "Goal"
python .claude/core/state.py status
python .claude/core/state.py recover
python .claude/core/state.py complete

# Stories
python .claude/core/state.py add-story "Title" --size M
python .claude/core/state.py update S1 in_progress
python .claude/core/state.py update S1 completed
python .claude/core/state.py verify S1 buildPasses --passed
python .claude/core/state.py next

# Problems
python .claude/core/state.py blocker "Description"
python .claude/core/state.py await-user "Description"
python .claude/core/state.py user-fix-complete

# Git
python .claude/core/state.py checkpoint "Before risky change"
python .claude/core/state.py rollback
```

## Platform Commands

```bash
python .claude/core/platform.py detect      # Auto-detect platform
python .claude/core/platform.py get-command build
python .claude/core/platform.py get-command test
```

---

## Stop Hook Behavior

The Stop hook (`stop.py`) implements persistent execution:

- **On exit attempt:** Checks for `WORKFLOW_COMPLETE` marker
- **If not found:** Blocks exit, provides context to continue
- **If found:** Allows normal exit
- **Safety limit:** Max 100 iterations prevents infinite loops
- **User intervention:** If `awaiting_user`, allows exit with instructions

---

## Key Points

- **Never exit without WORKFLOW_COMPLETE** (stop hook enforces)
- **Never skip verification** (build + test before completing story)
- **Iterate on failures** (failures are context, not blockers)
- **Use your reasoning** (you know more than any checklist)
