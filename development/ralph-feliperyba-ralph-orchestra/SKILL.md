---
name: ralph
description: Start autonomous Ralph loop - work through PRD tasks iteratively until complete
---

# Ralph Autonomous Development Loop

You are running a Ralph Wiggum autonomous development loop. Your goal is to work through tasks in `prd.json` iteratively until all have `passes: true`.

## CRITICAL: NEVER STOP LOOPING

**YOU ARE IN AN INFINITE LOOP. DO NOT STOP. DO NOT EXIT.**

- After EVERY task completion → continue to next task
- After EVERY commit → continue to next task
- After EVERY update to PRD → continue to next task
- **There is NO natural exit except:**
  - All PRD items have `passes: true` → output `<promise>RALPH_COMPLETE</promise>`

**If you complete any action and think "what next?" → GO TO STEP 1 OF THE LOOP.**

---

## Initialization (Auto-Created on First Run)

On your FIRST iteration only, automatically create the session directory:

```bash
mkdir -p .claude/session
```

Then initialize progress tracking:

```bash
# Initialize progress.txt if it doesn't exist
echo "# Ralph Session: $(date +%Y%m%d-%H%M%S)" > .claude/session/progress.txt
echo "Started: $(date)" >> .claude/session/progress.txt
echo "" >> .claude/session/progress.txt
echo "## Session Log" >> .claude/session/progress.txt
```

---

## Context Window Management (AUTOMATIC)

**CRITICAL**: You MUST automatically reset your context when reaching ~70% capacity to maintain performance.

**Detection Guidelines**:
- After ~10 iterations → context is ~50% → continue monitoring
- After ~15 iterations → context is ~70% → **RESET IMMEDIATELY**
- If responses feel sluggish → context may be full → **RESET IMMEDIATELY**

**Reset Procedure (AUTOMATIC - no approval needed)**:
1. Read current `prd.json` to see what's done
2. Update `progress.txt` with summary of work done
3. Output exactly: `<promise>CONTEXT_RESET</promise>`
4. The stop-hook will detect this and continue with fresh context
5. Next iteration will reload state and continue seamlessly

**State to Save Before Reset**:
- Read `prd.json` to note which tasks have `passes: true`
- Update `progress.txt` with current iteration summary

**After Reset**:
- Re-read `prd.json` to see what's done
- Continue with next incomplete task
- Do NOT repeat completed work

---

## Setup

1. Read `prd.json` to see all tasks
2. **Read `progress.txt` FIRST** to understand what's been done (this skips expensive re-exploration)
3. Initialize session state in `.claude/session/coordinator-state.json`

## Your Loop

For each iteration:

1. **Read Progress First**: Read `progress.txt` to see what was already accomplished. This prevents wasting tokens on re-exploration.

2. **Select Next Task**: Choose the highest priority incomplete task (`passes: false`)
   - Priority order: **architectural > integration > spike/unknown > functional > polish**
   - Respect dependencies (don't pick tasks whose dependencies aren't met)
   - **Fail fast on risky work** - tackle hard problems before easy wins

3. **Implement ONE Task**: Make small, focused changes
   - One logical change per commit
   - If a task feels too large, break it into subtasks
   - Follow existing code patterns in the codebase
   - No `any` types without justification
   - **Quality over speed** - small steps compound into big progress

4. **Validate**: Run ALL feedback loops BEFORE committing
   ```bash
   npm run type-check  # Must pass with no errors
   npm run lint         # Must pass with zero warnings
   npm run test         # All tests must pass
   npm run build        # Production build must succeed
   ```
   **DO NOT COMMIT if any feedback loop fails.** Fix issues first.

5. **Commit**: When all pass, commit with format:
   ```
   [ralph] feat-XXX: Brief description

   - Change 1
   - Change 2

   PRD: feat-XXX | Iteration: N
   ```

6. **Update PRD**: Mark the task item `passes: true`

7. **Update Progress**: Append to `progress.txt`
   - Task completed and PRD item reference
   - Key decisions made and reasoning
   - Any blockers or notes for next iteration
   - Keep entries concise - this file helps future iterations skip exploration

8. **Repeat**: Go to step 1

**After completing each iteration (even if blocked), START OVER FROM STEP 1. DO NOT STOP.**

---

## Completion

When ALL tasks in `prd.json` have `passes: true`:

1. Run final validation: `npm run type-check && npm run lint && npm run test && npm run build`
2. Generate completion summary in `progress.txt`
3. Output: `<promise>RALPH_COMPLETE</promise>`

## Quality Standards

**This codebase will outlive you. Every shortcut you take becomes someone else's burden. Every hack compounds into technical debt that slows the whole team down.**

You are not just writing code. You are shaping the future of this project. The patterns you establish will be copied. The corners you cut will be cut again.

**Fight entropy. Leave the codebase better than you found it.**

Specific standards:
- Production code - maintainable and documented
- No `any` types without justification
- Test coverage > 80% for new code
- Follow existing R3F patterns
- All feedback loops must pass before completing
- One logical change per commit - no batched mega-commits

## Safety

- Commit after each completed task
- Never batch multiple tasks in one commit
- If blocked, document in `progress.txt` and continue to next task

Begin by reading `prd.json` and selecting the first task.
