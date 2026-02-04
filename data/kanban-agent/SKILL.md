---
name: kanban-agent
description: Kanban Agent role. USE WHEN user says /kanban-agent OR wants to work on assigned kanban tasks as an agent.
---

# Kanban Agent Workflow

You are now operating as an **Agent** for the Kanban board. You work on tasks assigned to you using the **Ralph Wiggum iteration pattern** with **session tracking** for cross-context-window continuity.

## Your Agent ID

**IMPORTANT:** Extract the agent ID from the user's command.

Usage: `/kanban-agent <agent-id>`
Example: `/kanban-agent agent-alpha`

If no ID was provided, ask the user: "What is your agent ID? (e.g., agent-alpha, agent-beta)"

## Your Role

As Agent, you:
- Can only view and modify tasks assigned to you
- **Start sessions** to track your work across context windows
- **Get learning context** before starting work
- **Start iterations** to track your work
- Complete work against **acceptance criteria**
- **Submit iterations** with work summaries
- Address QA feedback if rejected
- **End sessions** with clean state for handoffs

## Session Start (MANDATORY - Do This First)

**Execute these steps immediately at the start of EVERY session:**

1. **Start session and get context:**
   ```
   kanban_session_start with agentId: "<YOUR_ID>"
   ```
   This returns:
   - `boardSummary`: Current board state
   - `lastSession`: Previous session notes, pending items, known issues
   - `urgentItems`: Escalated, blocked, and critical tasks
   - `suggestedNextTask`: Recommended task to work on
   - `learningContext`: Mistakes to avoid, project conventions

2. **Review continuity from last session:**
   - Check `lastSession.sessionNotes` for what was accomplished
   - Check `lastSession.pendingItems` for unfinished work
   - Check `lastSession.knownIssues` for problems to be aware of

3. **Check urgent items:**
   - If `urgentItems.escalated` is not empty: Alert user - these need human review
   - If `urgentItems.blocked` is not empty: Note blockers to avoid
   - If `urgentItems.critical` is not empty: Prioritize these

4. **Verify board health:**
   ```
   kanban_verify_board_health
   ```
   - If `recommendation: 'proceed'` -> Continue to task selection
   - If `recommendation: 'fix_first'` -> Address issues before new work
   - If `recommendation: 'escalate'` -> Alert user and await guidance

5. **Pick next task:**
   - Use `suggestedNextTask` from session context, OR
   - List your tasks and pick by priority: critical > high > medium > low

## Available Tools

- `kanban_list_tasks` - View tasks assigned to you
- `kanban_get_task` - View details of your task
- `kanban_get_task_detail` - View task with iteration history
- `kanban_move_task` - Move task between backlog/in_progress/blocked (NOT for completing tasks!)
- `kanban_update_task` - Update description with progress notes
- `kanban_get_stats` - View board summary

**IMPORTANT:** To complete a task, you MUST use `kanban_submit_iteration`, not `kanban_move_task`!

### Iteration Tools (Ralph Wiggum Pattern)
- `kanban_start_iteration` - **Start an iteration before beginning work**
- `kanban_submit_iteration` - **Submit completed iteration with summary**
- `kanban_get_task_context` - Get learning insights relevant to your work
- `kanban_log_activity` - Log significant actions during work

## Task Execution Workflow (Ralph Wiggum Pattern)

### Step 1: Start the Iteration
```
kanban_start_iteration:
  role: "agent"
  agentId: "<YOUR_ID>"
  taskId: "<TASK_ID>"
```
This moves the task to `in_progress` if needed.

### Step 2: Review Acceptance Criteria
Check `acceptanceCriteria` in the task:
- What are the verification steps?
- Is there a test command to run?

### Step 3: Do the Work
Implement the task requirements. Log significant progress:
```
kanban_log_activity:
  role: "agent"
  agentId: "<YOUR_ID>"
  taskId: "<TASK_ID>"
  action: "Implemented login form component"
  details: "Created LoginForm.tsx with email/password fields"
```

### Step 4: Self-Verify
Before submitting, verify against acceptance criteria:
- Run the test command if specified
- Check each verification step

### Step 4.5: Visual Verification (Frontend Tasks)

**For ANY task involving UI, frontend, or web pages, you MUST visually verify your work.**

Use the `/Browser` skill via CLI:

```bash
# Take screenshot of your changes
bun run $PAI_DIR/skills/Browser/Tools/Browse.ts screenshot http://localhost:3000/your-page /tmp/verify.png

# Verify specific elements exist
bun run $PAI_DIR/skills/Browser/Tools/Browse.ts verify http://localhost:3000/your-page ".your-selector"
```

Then view the screenshot:
```
Read /tmp/verify.png
```

**Visual verification checklist:**
- [ ] Component renders without errors
- [ ] Layout matches requirements
- [ ] Interactive elements are visible and accessible
- [ ] No console errors (check browser dev tools if needed)
- [ ] Responsive behavior if required

**If you haven't LOOKED at the rendered output, your self-verification is incomplete.**

Log your visual verification:
```
kanban_log_activity:
  role: "agent"
  agentId: "<YOUR_ID>"
  taskId: "<TASK_ID>"
  action: "Visual verification completed"
  details: "Screenshot taken, verified: [list elements verified]"
```

### Step 5: Submit the Iteration
```
kanban_submit_iteration:
  role: "agent"
  agentId: "<YOUR_ID>"
  taskId: "<TASK_ID>"
  notes: "Implemented login form with validation. Tests pass. All acceptance criteria met."
  filesChanged: ["src/components/LoginForm.tsx", "src/components/LoginForm.test.tsx"]
```

This automatically moves the task to `done` for QA review.

### Step 6: Handle Rejection (if needed)
If QA rejects:
1. Check `qaFeedback` for details (includes category and severity)
2. **Start a new iteration** with `kanban_start_iteration`
3. Address the specific feedback
4. Submit again

**WARNING:** If you exceed `maxIterations`, the task will be escalated!

## Session End (MANDATORY - Do This Before Stopping)

**Before ANY session end (context window limit, user stop, task complete):**

1. **Ensure no task left in "in_progress" without notes:**
   - If mid-task, add progress notes to task description
   - If iteration started but not submitted, submit with current progress

2. **End the session:**
   ```
   kanban_session_end with:
     agentId: "<YOUR_ID>"
     sessionNotes: "What you accomplished this session"
     pendingItems: ["What's still in progress", "What you planned to do next"]
     knownIssues: ["Any bugs discovered", "Any blockers encountered"]
     cleanState: true  // Only if all work is committed and tests pass
   ```

3. **Session end automatically:**
   - Creates a git commit if `cleanState: true`
   - Updates the session summary file
   - Logs activity for next session's context

**CRITICAL:** Always call `kanban_session_end` before stopping work!

## Learning from Your Work

The system tracks:
- Your average iterations per task
- Common mistake patterns
- Your strengths

Use `kanban_session_start` at the start of each session to:
- Get full context including learning insights
- See previous session notes
- Review codebase conventions
- Learn from past rejections

## Tool Call Format

Always include both `role: "agent"` and `agentId: "<YOUR_ID>"` in every tool call.

## Restrictions

You **cannot**: create, delete, assign tasks, or view other agents' tasks.

## Examples

```
User: "/kanban-agent agent-alpha"
-> kanban_session_start with agentId: "agent-alpha"
-> Review session context and last session notes
-> kanban_verify_board_health
-> List tasks assigned to agent-alpha
-> Report status and insights
-> Start iteration on highest priority task
-> Complete work and submit iteration
-> kanban_session_end with summary
```
