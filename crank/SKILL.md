---
name: crank
description: 'Fully autonomous epic execution. Runs until ALL children are CLOSED. Loops through beads issues, runs /implement on each, validates with /vibe. NO human prompts, NO stopping.'
---

# Crank Skill

> **Quick Ref:** Autonomous epic execution. Loops `/implement` on all issues until DONE. Output: closed issues + final vibe.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Autonomous execution: implement all issues until the epic is DONE.

**Requires:** bd CLI (beads) for issue tracking, OR in-session TaskList for task-based tracking.

## Global Iteration Limit

**MAX_EPIC_ITERATIONS = 50** (hard limit across entire epic)

This prevents infinite loops on circular dependencies or cascading failures.

**Why 50?**
- Typical epic: 5-10 issues
- With retries: ~5 iterations per issue max
- 50 = safe upper bound (10 issues × 5 retries)

## Completion Enforcement (The Sisyphus Rule)

**THE SISYPHUS RULE:** Not done until explicitly DONE.

After each task, output completion marker:
- `<promise>DONE</promise>` - Epic truly complete, all issues closed
- `<promise>BLOCKED</promise>` - Cannot proceed (with reason)
- `<promise>PARTIAL</promise>` - Incomplete (with remaining items)

**Never claim completion without the marker.**

## Execution Steps

Given `/crank [epic-id]`:

### Step 1: Identify the Epic

**If epic ID provided:** Use it directly. Do NOT ask for confirmation.

**If no epic ID:** Discover it:
```bash
bd list --type epic --status open 2>/dev/null | head -5
```

If bd not available, look for a plan:
```bash
ls -lt .agents/plans/ 2>/dev/null | head -3
```

If multiple epics found, ask user which one.

### Step 1a: Initialize Iteration Counter

```bash
# Initialize crank tracking in epic notes
bd update <epic-id> --append-notes "CRANK_START: iteration=0 at $(date -Iseconds)" 2>/dev/null
```

Track in memory: `iteration=0`

### Step 2: Get Epic Details

```bash
bd show <epic-id> 2>/dev/null
```

Or read the plan document if using file-based tracking.

### Step 3: List Ready Issues

Find issues that can be worked on (no blockers):
```bash
bd ready 2>/dev/null
```

Or parse the plan document for Wave 1 issues.

Or use TaskList tool if using in-session task tracking.

### Step 3a: Pre-flight Check - Issues Exist

**Verify there are issues to work on:**

**If 0 ready issues found:**
```
STOP and return error:
  "No ready issues found for this epic. Either:
   - All issues are blocked (check dependencies)
   - Epic has no child issues (run /plan first)
   - All issues already completed"
```

Do NOT proceed with empty issue list - this produces false "epic complete" status.

### Step 4: Execute Each Issue (with iteration tracking)

**BEFORE each issue:**
```bash
# Increment and check iteration counter
iteration=$((iteration + 1))
bd update <epic-id> --append-notes "CRANK_ITERATION: $iteration at $(date -Iseconds)" 2>/dev/null

# CHECK GLOBAL LIMIT
if [[ $iteration -ge 50 ]]; then
    echo "<promise>BLOCKED</promise>"
    echo "Global iteration limit (50) reached. Remaining issues:"
    bd children <epic-id> --status open 2>/dev/null
    # STOP - do not continue
fi
```

**FOR EACH ready issue, USE THE SKILL TOOL:**

```
Tool: Skill
Parameters:
  skill: "agentops:implement"
  args: "<issue-id>"
```

Wait for implement to complete before moving to next issue.

**Check for BLOCKED/PARTIAL markers from implement:**
- If `<promise>BLOCKED</promise>` returned → record blocker, try next issue
- If `<promise>PARTIAL</promise>` returned → record remaining, try next issue
- If `<promise>DONE</promise>` returned → continue normally

### Step 5: Track Progress (No Per-Issue Vibe)

After implement completes:

1. Update issue status:
```bash
bd update <issue-id> --status closed 2>/dev/null
```
Or use TaskUpdate to mark task completed.

2. Track changed files in memory or use TaskCreate to note them.

**Note:** Skip per-issue vibe - validation is batched at the end to save context.

### Step 6: Check for More Work

After completing an issue:
1. Check if new issues are now unblocked (use `bd ready` or TaskList)
2. If yes, return to Step 4
3. If no more issues after 3 retry attempts, proceed to Step 7
4. **Max retries:** If issues remain blocked after 3 checks, escalate: "Epic blocked - cannot unblock remaining issues"

### Step 7: Final Batched Validation

When all issues complete, run ONE comprehensive vibe on recent changes:

```bash
# Get list of changed files from recent commits
git diff --name-only HEAD~10 2>/dev/null | sort -u
```

**Run vibe on recent changes:**
```
Tool: Skill
Parameters:
  skill: "agentops:vibe"
  args: "recent"
```

**If CRITICAL issues found:**
1. Fix them
2. Re-run vibe on affected files
3. Only proceed to completion when clean

### Step 8: Report Completion

Tell the user:
1. Epic ID and title
2. Number of issues completed
3. Total iterations used (of 50 max)
4. Final vibe results
5. Suggest running `/post-mortem` to extract learnings

**Output completion marker:**
```
<promise>DONE</promise>
Epic: <epic-id>
Issues completed: N
Iterations: M/50
```

If stopped early:
```
<promise>BLOCKED</promise>
Reason: <global limit reached | unresolvable blockers>
Issues remaining: N
Iterations: M/50
```

## The FIRE Loop

Crank follows FIRE for each issue:

| Phase | Action |
|-------|--------|
| **FIND** | `bd ready` - get unblocked issues |
| **IGNITE** | `/implement <issue>` - do the work |
| **REAP** | `/vibe` - validate the work |
| **ESCALATE** | Fix issues or mark blocked |

Loop until all issues are CLOSED.

## Key Rules

- **If epic ID given, USE IT** - don't ask for confirmation
- **One issue at a time** - implement → close → next
- **Batch validation at end** - ONE vibe at the end saves context
- **Fix CRITICAL before completion** - address findings before reporting done
- **Loop until done** - don't stop until all issues closed
- **Autonomous execution** - minimize human prompts
- **Respect iteration limit** - STOP at 50 iterations (hard limit)
- **Output completion markers** - DONE, BLOCKED, or PARTIAL (required)

## Without Beads

If bd CLI not available:
1. Use the plan document as the source of truth
2. Track completed issues by checking git commits
3. Mark issues done by noting in the plan document
