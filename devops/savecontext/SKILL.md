---
name: savecontext
description: This skill should be used when the user asks to "save context", "remember this decision", "track my progress", "checkpoint my work", "resume where I left off", "continue from last session", "persist state across sessions", "prepare for compaction", "restore from checkpoint", "switch sessions", or when starting work and needing to check for existing sessions. Also triggers on compound workflows like "wrap up session", "wrap up and checkpoint", "end of day checkpoint", "resume fully", "pick up where I left off and show status", "checkpoint with tags", "log work and checkpoint", "tag and checkpoint", "prepare for handoff", "handoff to another agent".
---

# SaveContext

Persistent context management for AI coding agents. Save decisions, track progress, and maintain continuity across sessions.

> **ALWAYS USE MARKDOWN:** When saving context, creating issues, or adding descriptions - use proper markdown formatting (headers, bullets, bold, code blocks). Well-structured content is essential for useful restoration.

## When to Use SaveContext

Use SaveContext when:
- Work spans multiple sessions or days
- Making architectural decisions worth remembering
- Approaching context limits (40+ messages)
- Switching between tasks or branches
- Collaborating with multiple agents on the same project

Do NOT use for:
- Single-session quick fixes
- Information already in the codebase
- Temporary debugging notes

## Session Start Protocol

When beginning work on a project:

1. **Check for existing session**
   ```
   context_session_start name="descriptive-task-name" description="what you're working on"
   ```
   This auto-resumes if an active session exists.

2. **Review existing context**
   ```
   context_get category="decision" priority="high"
   ```
   Check what decisions were already made.

3. **Check status**
   ```
   context_status
   ```
   See item count, checkpoint count, and if compaction is needed.

**Session Naming:**
- Good: `"implementing-oauth2-authentication"`, `"fixing-payment-webhook-bug"`
- Bad: `"working on stuff"`, `"session 1"`, `"test"`

## Compound Workflows

When user requests compound actions, execute these sequences automatically.

### Wrap Up Session
**Triggers:** "wrap up", "wrap up session", "end of day", "checkpoint everything", "wrap up and checkpoint"

Execute in order:
1. `context_save` - Log current progress with what was accomplished
2. `context_tag` - Tag recent items with relevant work stream tags
3. `context_checkpoint` - Create checkpoint with descriptive name
4. `context_session_pause` - Pause session for later resumption

### Resume Fully
**Triggers:** "resume fully", "pick up where I left off and show status", "continue and show context"

Execute in order:
1. `context_session_start` - Resume existing session
2. `context_status` - Show session stats (item count, checkpoints)
3. `context_get priority="high"` - Display critical decisions/blockers
4. `context_get category="reminder"` - Show pending reminders and next steps

### Checkpoint with Tags
**Triggers:** "checkpoint with tags", "tag and checkpoint", "log work and checkpoint"

Execute in order:
1. `context_get` - Review recent items in session
2. Ask user (or infer) what tags to apply
3. `context_tag` - Tag items with specified tags
4. `context_checkpoint` - Create checkpoint **filtering to those tags**:
   ```
   context_checkpoint name="feature-complete" include_tags=["the-tags-just-applied"]
   ```

**Important:** Without `include_tags`, the checkpoint captures ALL session items. Always filter when checkpointing after tagging.

### Prepare for Handoff
**Triggers:** "prepare for handoff", "handoff to another agent", "hand off"

Execute in order:
1. `context_save` - Log final progress summary
2. `context_tag` - Tag all items with `handoff` tag
3. `context_checkpoint name="handoff-ready"` - Create handoff checkpoint
4. Display: session name, checkpoint ID, and key context for receiving agent

## What to Save

### Categories

| Category | Use For | Example |
|----------|---------|---------|
| `decision` | Architectural choices, library selections | "Chose JWT over sessions for stateless scaling" |
| `progress` | What was completed, current state | "Auth login flow complete. Refresh tokens next." |
| `reminder` | Current work items, next steps | "TODO: Add rate limiting to token endpoint" |
| `note` | Reference info, gotchas, discoveries | "Stripe webhooks fail if body parsed as JSON first" |

### Issues vs Context Reminders

Use the right tool for tracking work:

| Use Case | Tool |
|----------|------|
| Quick inline TODOs for current session | `context_save category="reminder"` |
| Feature requests, bugs, enhancements | `context_issue_create` |
| Work needing status tracking | `context_issue_create` |
| Tasks with dependencies | `context_issue_create` |
| Temporary reminders | `context_save category="reminder"` |
| Trackable across sessions | `context_issue_create` |

**Rule of thumb:** If it's something another agent or future session should pick up and track to completion, use `context_issue_create`. If it's a quick reminder for the current session only, use `context_save category="reminder"`.

### Priorities

| Priority | Use For |
|----------|---------|
| `high` | Critical decisions, blockers, must-remember info |
| `normal` | Standard progress and notes |
| `low` | Nice-to-have context, minor details |

### What's Worth Saving

**Save:**
- Architectural decisions and rationale
- API endpoints, database schemas, important URLs
- Gotchas discovered during debugging
- Current task and next steps

**Don't Save:**
- Code snippets (they're in the codebase)
- Generic best practices
- Temporary debugging info

### Key Naming

Keys should be descriptive and grep-able:
- Good: `"auth-jwt-decision"`, `"stripe-webhook-gotcha"`, `"db-schema-v2"`
- Bad: `"decision1"`, `"note"`, `"temp"`

## Formatting Context Values

**Critical:** Well-formatted context is the difference between useful restoration and useless noise. **Always use markdown formatting** - assume the user wants structured, scannable content.

### Structure Guidelines (ALWAYS FOLLOW)

1. **Always use markdown** - Headers (`##`), bullets (`-`), bold (`**`), code blocks
2. **Lead with the essential insight** - First line should be the most important point
3. **Keep items atomic** - One concept per context item
4. **Include rationale** - "What" without "why" is useless later
5. **Add actionable next steps** - Future you needs to know what's next
6. **Reference files** - Include `file.ts:line` references where relevant

### Formatting Patterns by Category

**Decisions (most critical to format well):**
```
## [Decision Title]

**Choice:** [What was decided]
**Rationale:** [Why this over alternatives]
**Trade-offs:** [What we gave up]
**Alternatives rejected:** [What else was considered]

Impact: [Files/systems affected]
```

**Progress updates:**
```
## [Feature/Task] - [Status]

**Completed:**
- Item 1
- Item 2

**Current state:** [Where things stand]

**Next:** [Immediate next action]
**Blocked by:** [If applicable]
```

**Notes/Gotchas:**
```
## [Topic] Gotcha

**Problem:** [What goes wrong]
**Cause:** [Root cause]
**Solution:** [How to fix/avoid]

File: `path/to/relevant/file.ts`
```

**Reminders:**
```
## TODO: [Reminder title]

**Context:** [Why this needs doing]
**Approach:** [How to tackle it]
**Acceptance:** [How to know it's done]

Files: `file1.ts`, `file2.ts`
```

### Good vs Bad Examples

**Decision - BAD:**
```
context_save key="auth" value="we decided to use jwt" category="decision"
```
Problems: No rationale, no context, no alternatives, will be useless later.

**Decision - GOOD:**
```
context_save key="auth-jwt-decision" value="## Authentication: JWT with Refresh Tokens

**Choice:** JWT access tokens (15min) + refresh tokens (7 days)
**Rationale:** Stateless auth scales horizontally; refresh tokens balance security with UX

**Rejected alternatives:**
- Sessions: Requires shared state/Redis, adds complexity
- JWT only: Too short = bad UX, too long = security risk

**Trade-off:** Token revocation requires maintaining a blocklist

Impact: `auth/`, `middleware/`, `lib/tokens.ts`" category="decision" priority="high"
```

**Progress - BAD:**
```
context_save key="progress" value="did some work on the api" category="progress"
```
Problems: Vague, no specifics, doesn't help future sessions.

**Progress - GOOD:**
```
context_save key="api-endpoints-progress" value="## REST API Implementation - 70%

**Completed:**
- GET/POST/PUT/DELETE for `/users`
- GET/POST for `/projects`
- Authentication middleware
- Rate limiting (100 req/min)

**Current state:** CRUD operations working, tests passing

**Next:** Implement `/projects/:id/tasks` endpoints
**Blocked by:** Need schema decision for task priorities" category="progress"
```

**Note - BAD:**
```
context_save key="note1" value="stripe is weird" category="note"
```

**Note - GOOD:**
```
context_save key="stripe-webhook-raw-body" value="## Stripe Webhook Signature Gotcha

**Problem:** Webhook signature verification always fails
**Cause:** Express JSON middleware parses body before Stripe can verify
**Solution:** Use `express.raw({type: 'application/json'})` for webhook route ONLY

```typescript
// WRONG - global JSON parsing breaks signature
app.use(express.json());

// RIGHT - raw body for webhooks
app.post('/webhook', express.raw({type: 'application/json'}), handleWebhook);
```

File: `routes/webhooks.ts:15`" category="note" priority="high"
```

### Length Guidelines

| Category | Target Length | Max Length |
|----------|--------------|------------|
| Decision | 200-500 chars | 1000 chars |
| Progress | 150-400 chars | 800 chars |
| Note | 100-300 chars | 600 chars |
| Reminder | 100-250 chars | 500 chars |

**If it's longer:** Split into multiple context items with related keys (e.g., `auth-decision-jwt`, `auth-decision-refresh`).

### What NOT to Include

- **Code blocks over 10 lines** - Reference the file instead
- **Full error stack traces** - Summarize the error
- **Conversation summaries** - Save insights, not transcripts
- **Generic knowledge** - Only project-specific context
- **Temporary debug info** - Will clutter future sessions

### Multi-Item Patterns

For complex decisions, split into related items:

```
context_save key="db-schema-users" value="..." category="decision"
context_save key="db-schema-projects" value="..." category="decision"
context_save key="db-schema-relations" value="..." category="decision"
context_tag keys=["db-schema-users", "db-schema-projects", "db-schema-relations"] tags=["db", "schema-v2"] action="add"
```

This enables:
- Selective restore (`restore_tags=["db"]`)
- Targeted search (`context_get query="database schema"`)
- Clean checkpoint splitting

## Tagging Strategy

**Always tag before checkpointing.** Tags enable selective restore and checkpoint splitting.

```
context_tag keys=["auth-decision", "auth-progress"] tags=["auth"] action="add"
```

Tag conventions:
- Short, descriptive: `auth`, `ui`, `api`, `payments`
- Consistent across sessions
- By work stream or feature

## Checkpoint Triggers

Create checkpoints at these moments:

1. **Before major changes**
   ```
   context_checkpoint name="pre-refactor" include_git=true
   ```

2. **At milestones**
   After completing a feature or fixing a bug.

3. **Before context compaction**
   When context gets long, `context_prepare_compaction` auto-creates a checkpoint.

4. **Before switching branches**
   Checkpoint your current work stream before context-switching.

## Fixing Checkpoints

Made a checkpoint with wrong items? Use these tools to fix it:

### Delete and Recreate
If checkpoint captured too much:
```
context_checkpoint_delete checkpoint_id="..." checkpoint_name="..."
context_checkpoint name="correct-name" include_tags=["desired-tag"]
```

### Add Missing Items
If checkpoint missed items:
```
context_checkpoint_add_items checkpoint_id="..." checkpoint_name="..." item_keys=["key1", "key2"]
```

### Remove Unwanted Items
If checkpoint has items that shouldn't be there:
```
context_checkpoint_remove_items checkpoint_id="..." checkpoint_name="..." item_keys=["unwanted-key"]
```

### Split Mixed Checkpoints
If checkpoint mixed multiple work streams:
1. First, tag items by work stream:
   ```
   context_get_checkpoint checkpoint_id="..."  # See all items
   context_tag keys=["auth-item1", "auth-item2"] tags=["auth"] action="add"
   context_tag keys=["ui-item1", "ui-item2"] tags=["ui"] action="add"
   ```
2. Then split:
   ```
   context_checkpoint_split source_checkpoint_id="..." source_checkpoint_name="..." splits=[
     {"name": "auth-work", "include_tags": ["auth"]},
     {"name": "ui-work", "include_tags": ["ui"]}
   ]
   ```

**Tip:** Always verify with `context_get_checkpoint` after fixing.

## Context Compaction

When conversation exceeds 40 messages or context usage is high:

```
context_prepare_compaction
```

This:
- Creates a checkpoint of all context
- Summarizes critical items (high-priority decisions, active tasks)
- Returns restore instructions for the next session

**After compaction**, in a new conversation:
```
context_restore checkpoint_id="..." checkpoint_name="..."
```

## Memory vs Context

| Type | Scope | Use For |
|------|-------|---------|
| **Context** (`context_save`) | Current session | Decisions, progress, notes for this task |
| **Memory** (`context_memory_save`) | All sessions | Commands, configs, permanent project info |

**Memory examples:**
```
context_memory_save key="test_cmd" value="npm test -- --coverage" category="command"
context_memory_save key="prod_api" value="https://api.example.com/v1" category="config"
```

Memory persists across ALL sessions for this project.

## Project Management

Projects organize sessions, issues, and memory by codebase. Use project tools for multi-project workflows.

### Creating Projects

**Always format project creation with markdown structure:**

```
context_project_create
  project_path="/path/to/project"
  name="Project Display Name"
  description="Brief project description"
  issue_prefix="PROJ"
```

**Good project setup:**
```
context_project_create
  project_path="/Users/dev/my-api"
  name="My API Service"
  description="REST API for mobile app with PostgreSQL backend"
  issue_prefix="API"
```

The `issue_prefix` creates readable issue IDs like `API-1`, `API-2`.

### Project Tools Reference

| Tool | Purpose |
|------|---------|
| `context_project_create` | Create new project with name, description, prefix |
| `context_project_list` | List all projects (with session counts if needed) |
| `context_project_get` | Get project details by path |
| `context_project_update` | Update name, description, or prefix |

### Issue Tracking

Projects enable issue tracking across sessions:

```
context_issue_create
  title="Implement user authentication"
  description="## Requirements\n\n- JWT tokens\n- Refresh token rotation\n- Rate limiting"
  issueType="feature"
  priority=3
  labels=["auth", "security"]
```

**Always format issue descriptions in markdown:**

```markdown
## Requirements

- Bullet point 1
- Bullet point 2

## Acceptance Criteria

1. Numbered item
2. Numbered item

## Notes

Additional context here
```

### Issue Workflow

```
# Create issues for a feature
context_issue_create title="Design auth schema" issueType="task"
context_issue_create title="Implement JWT tokens" issueType="task"
context_issue_create title="Add refresh token rotation" issueType="task"

# Link dependencies
context_issue_add_dependency issueId="PROJ-2" dependsOnId="PROJ-1"
context_issue_add_dependency issueId="PROJ-3" dependsOnId="PROJ-2"

# Get ready issues (no blockers)
context_issue_get_ready

# Claim and work
context_issue_claim issue_ids=["PROJ-1"]
# ... do work ...
context_issue_complete id="PROJ-1" issue_title="Design auth schema"
```

## Planning with Epics

For larger refactors or features, create an epic with hierarchical subtasks. This enables structured planning that persists across sessions.

### When to Use Each Issue Type

| Type | Use When | Examples |
|------|----------|----------|
| `epic` | Work spans 5+ subtasks, multiple sessions, or is a major initiative | "Implement authentication system", "Refactor database layer" |
| `feature` | New capability, standalone or with 1-3 subtasks | "Add dark mode toggle", "Create export to CSV" |
| `bug` | Something is broken and needs fixing | "Login fails on Safari", "Race condition in checkout" |
| `task` | General work item, often a subtask of epic/feature | "Update type definitions", "Write unit tests" |
| `chore` | Maintenance, cleanup, no user-facing change | "Update dependencies", "Clean up dead code" |

**Decision guide:**
- **Epic vs Feature:** If it needs a plan with multiple coordinated subtasks, use epic. If it's a single deliverable (even if complex), use feature.
- **Bug vs Task:** If it's fixing broken behavior, use bug. If it's new work or improvement, use task.
- **Standalone vs Subtask:** One-off fixes = standalone. Part of larger work = subtask with parentId.

### Writing Good Descriptions

Descriptions go in the `description` field and should explain **what** and **why**.

**For Epics:**
```markdown
## Overview
Brief explanation of what this epic accomplishes and why it matters.

## Scope
- Area 1 affected
- Area 2 affected
- Area 3 affected

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Out of Scope
- Thing we're NOT doing
```

**For Features/Tasks:**
```markdown
## Goal
What this accomplishes in 1-2 sentences.

## Files Affected
- `path/to/file1.ts`
- `path/to/file2.ts`

## Approach
Brief description of how to implement.
```

**For Bugs:**
```markdown
## Problem
What's broken and how it manifests.

## Expected Behavior
What should happen instead.

## Reproduction Steps
1. Step 1
2. Step 2

## Root Cause (if known)
Technical explanation.
```

### Writing Implementation Details

The `details` field is for **how** - technical implementation notes that help execute the work.

**When to use details:**
- Complex implementation requiring specific approach
- Code patterns to follow
- Dependencies or order of operations
- Technical gotchas to watch for

**Example:**
```
context_issue_create
  title="Update MCP tool definitions"
  description="Update enum values in tool schemas for reminder category"
  details="## Implementation

Search for 'task' in enum arrays within:
- `context_save` inputSchema.properties.category.enum
- `context_get` inputSchema.properties.category.enum
- `context_update` inputSchema.properties.category.enum

Replace with 'reminder'. ~12 occurrences total.

**Pattern:**
\`\`\`typescript
enum: ['decision', 'progress', 'reminder', 'note']
\`\`\`

Run build after to catch any type errors."
  issueType="task"
  labels=["mcp"]
```

**Details vs Description:**
- `description`: What and why (for understanding the issue)
- `details`: How (for executing the work)

### Creating an Epic with Subtasks

**Step 1: Create the parent epic**
```
context_issue_create
  title="Implement user authentication"
  description="## Overview\n\nAdd JWT-based authentication with refresh tokens.\n\n## Scope\n\n- Auth middleware\n- Login/logout endpoints\n- Token refresh logic\n- Protected routes\n- User session management"
  issueType="epic"
  priority=3
  labels=["auth", "security"]
```

**Step 2: Create subtasks linked to epic**
```
context_issue_create
  title="Create auth middleware"
  description="Implement JWT verification middleware for protected routes:\n- `middleware/auth.ts`\n- `lib/tokens.ts`"
  issueType="task"
  parentId="PROJ-abc"  # Parent epic ID
  labels=["auth"]
```

Subtasks automatically get hierarchical IDs: `PROJ-abc.1`, `PROJ-abc.2`, etc.

### Batch Creating Subtasks

For multiple subtasks, use batch creation:

```
context_issue_create_batch issues=[
  {
    "title": "Update type definitions",
    "description": "...",
    "issueType": "task",
    "labels": ["types"]
  },
  {
    "title": "Update MCP tool schemas",
    "description": "...",
    "issueType": "task",
    "labels": ["mcp"]
  },
  {
    "title": "Update validation",
    "description": "...",
    "issueType": "task",
    "labels": ["validation"]
  }
] dependencies=[
  {"issueIndex": 1, "dependsOnIndex": 0, "dependencyType": "parent-child"},
  {"issueIndex": 2, "dependsOnIndex": 0, "dependencyType": "parent-child"}
]
```

### Viewing Epic Progress

List subtasks for an epic:
```
context_issue_list parentId="PROJ-abc"
```

Returns all subtasks with their status, letting you track epic completion.

### Epic Execution Pattern

When the user says "begin" or "start the epic":

1. **List subtasks in order**
   ```
   context_issue_list parentId="EPIC-ID"
   ```

2. **Claim first ready subtask**
   ```
   context_issue_claim issue_ids=["EPIC-ID.1"]
   ```

3. **Execute the work**
   Read files, make changes, run builds

4. **Complete and move to next**
   ```
   context_issue_complete id="EPIC-ID.1" issue_title="..."
   ```

5. **Repeat until epic is done**

### Presenting Plans to Users

When you create a plan, present it clearly:

```markdown
## Epic: [Title]

**[EPIC-ID]** | Priority: [X] | Type: Epic

[Brief description of what this epic accomplishes]

---

### Subtasks

| ID | Title | Labels | Status |
|---|---|---|---|
| **EPIC-ID.1** | First subtask | `label` | open |
| **EPIC-ID.2** | Second subtask | `label` | open |
| **EPIC-ID.3** | Third subtask | `label` | blocked |

---

Ready to execute when you are.
```

This format gives users a clear view of the plan and enables easy tracking.

## Plans (PRDs & Specifications)

Plans are high-level documents (PRDs, specs, technical designs) that organize related epics and issues. Use plans when work requires a specification document that multiple issues should reference.

### When to Use Plans

| Use Plans When | Don't Use Plans When |
|----------------|---------------------|
| Work requires a PRD or specification | Single feature with clear scope |
| Multiple epics relate to same initiative | Simple bug fix or task |
| Need to track success criteria separately | Work is fully described in epic |
| Large project spanning weeks/months | Quick refactor or cleanup |

### Creating a Plan

```
context_plan_create
  title="User Authentication System"
  content="## Overview

This plan covers the complete authentication system redesign.

## Goals
- Implement JWT-based stateless auth
- Add MFA support
- Improve session management

## Requirements

### Phase 1: Core Auth
- Login/logout endpoints
- JWT token generation
- Refresh token rotation

### Phase 2: MFA
- TOTP support
- Backup codes
- Recovery flow

## Success Criteria
- [ ] All auth endpoints have <100ms p99 latency
- [ ] MFA adoption >50% within 30 days
- [ ] Zero auth-related security incidents"
  successCriteria="- All auth endpoints <100ms p99\n- MFA adoption >50%\n- Zero security incidents"
  status="active"
```

### Linking Issues to Plans

When creating epics or issues, use `planId` to link them to a plan:

```
# First, find or create your plan
context_plan_list  # Find existing plan ID

# Create epic linked to plan
context_issue_create
  title="Phase 1: Core Authentication"
  description="Implement JWT-based auth with refresh tokens"
  issueType="epic"
  planId="PLAN-abc123"  # Links epic to plan
  priority=3
```

### Batch Creating Issues for a Plan

Link all issues in a batch to the same plan:

```
context_issue_create_batch
  planId="PLAN-abc123"  # All issues link to this plan
  issues=[
    {
      "title": "Create auth middleware",
      "issueType": "task",
      "labels": ["auth"]
    },
    {
      "title": "Implement JWT tokens",
      "issueType": "task",
      "labels": ["auth"]
    },
    {
      "title": "Add refresh token rotation",
      "issueType": "task",
      "labels": ["auth"]
    }
  ]
```

### The Full Hierarchy

Plans establish a three-level hierarchy:

```
Plan (PRD/Spec)
├── Epic (Major initiative)
│   ├── Task (Implementation work)
│   ├── Task
│   └── Bug (Issues discovered)
├── Epic
│   ├── Task
│   └── Chore (Maintenance)
└── Feature (Standalone capability)
    └── Task
```

Epics and features are siblings linked to the same plan. Epics contain tasks, bugs, and chores as subtasks. Features can also have task subtasks if complex.

**Example flow:**
1. Create plan with `context_plan_create`
2. Create epics/features with `planId` pointing to plan
3. Create tasks with `parentId` pointing to their parent epic or feature
4. View plan progress with `context_issue_list planId="PLAN-xxx"`

### Plan Tools Reference

| Tool | Purpose |
|------|---------|
| `context_plan_create` | Create new plan with title, content, success criteria |
| `context_plan_list` | List plans (filter by status: draft/active/completed) |
| `context_plan_get` | Get plan details including linked epics |
| `context_plan_update` | Update plan content, status, or success criteria |

### Viewing Plan Progress

```
# Get plan with linked epics
context_plan_get plan_id="PLAN-abc123"

# List all issues linked to plan
context_issue_list planId="PLAN-abc123"

# Filter by status
context_issue_list planId="PLAN-abc123" status="in_progress"
```

### Plan-Issue Synchronization

**Critical workflow:** When you modify epics or tasks under a plan, always update the plan to reflect those changes. Plans and issues must stay in sync.

**When to update the plan:**
- Completing an epic/phase → Update plan to show completion
- Adding/removing tasks → Update plan's execution order
- Scope changes → Update plan's content and success criteria
- Restructuring dependencies → Update plan's stages

**Synchronization workflow:**

1. **After completing a phase/epic:**
   ```
   # Complete the epic
   context_issue_complete id="EPIC-ID" issue_title="Phase A: ..."

   # Update plan to reflect completion
   context_plan_update id="PLAN-ID"
     content="... Phase A: ✅ COMPLETE ..."
   ```

2. **After restructuring tasks:**
   ```
   # Delete old tasks, create new ones with proper dependencies
   context_issue_delete id="..." issue_title="..."
   context_issue_create_batch issues=[...] dependencies=[...]

   # Update plan with new structure
   context_plan_update id="PLAN-ID"
     content="... updated execution order ..."
     successCriteria="... updated criteria ..."
   ```

3. **Before starting a phase:**
   ```
   # Verify plan matches current issue structure
   context_plan_get plan_id="PLAN-ID"
   context_issue_list parentId="EPIC-ID"

   # Update plan if needed, then claim and start
   context_issue_update id="EPIC-ID" issue_title="..." status="in_progress"
   context_issue_claim issue_ids=["FIRST-TASK-ID"]
   ```

**The loop:**
```
Audit → Update Issues → Update Plan → Claim → Execute → Complete → Update Plan
        ↑___________________________________________________|
```

**Why this matters:**
- Plans become the single source of truth for project state
- Future agents can resume by reading the plan
- Progress is visible at both plan and issue level
- No drift between documentation and actual work

## Semantic Search

Find context by meaning, not just exact match:

```
context_get query="how did we handle authentication"
```

Search tips:
- Use natural language questions
- Lower threshold (0.3) for more results, higher (0.7) for precision
- Add `search_all_sessions=true` to search across all your sessions

## Quick Reference

### Sessions & Context
| Task | Tool |
|------|------|
| Start/resume session | `context_session_start` |
| Save decision | `context_save category="decision" priority="high"` |
| Track progress | `context_save category="progress"` |
| Find previous work | `context_get query="..."` |
| Tag items | `context_tag keys=[...] tags=[...] action="add"` |
| Create checkpoint | `context_checkpoint name="..."` |
| Pause session | `context_session_pause` |
| Prepare for compaction | `context_prepare_compaction` |
| Restore from checkpoint | `context_restore` |

### Projects & Issues
| Task | Tool |
|------|------|
| Create project | `context_project_create project_path="..." name="..."` |
| List projects | `context_project_list` |
| Create issue | `context_issue_create title="..." issueType="feature"` |
| List issues | `context_issue_list` |
| Get ready issues | `context_issue_get_ready` |
| Complete issue | `context_issue_complete id="..." issue_title="..."` |

Full tool reference: [savecontext.dev/docs/reference/tools](https://savecontext.dev/docs/reference/tools)

## Reference Files

- [references/WORKFLOWS.md](references/WORKFLOWS.md) - Detailed workflow patterns for multi-session projects, pre-refactor checkpointing, and compaction recovery.
