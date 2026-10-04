---
name: agentboard
description: Skill for using the AgentBoard AI project management app and its MCP server. Use when the user wants to manage projects through AgentBoard, start the AgentBoard servers, interact with the AgentBoard MCP tools, or needs guidance on the AgentBoard workflow (phases, milestones, documents, tasks). Triggers on "start agentboard", "manage project", "use agentboard", "agentboard workflow", "create a project in agentboard", or "set up agentboard".
---

# AgentBoard Skill

Use the AgentBoard AI project management system to create, track, and manage software projects through a structured phase-based workflow with strict state machine enforcement.

---

## 1. Setup and Server Startup

### 1.1 Prerequisites

AgentBoard requires **Node.js** (with npm) and **Python 3.10+**.

**Install Node.js dependencies** (one-time, from the project root):

```bash
cd /path/to/Project-Manager
npm install
npm install --prefix server
npm install --prefix client
```

**Install MCP server dependencies** (one-time):

```bash
pip install -r agentboard_mcp/requirements.txt
```

This installs: `httpx`, `mcp[cli]`, `pydantic`.

### 1.2 Start the AgentBoard Server

The AgentBoard server **must be running** before using any MCP tools. There are two ways to start it:

**Option A -- Via MCP tool (recommended when MCP server is already configured):**

Call the `agentboard_start_server` MCP tool. It checks health first and won't restart a healthy server.

**Option B -- Via command line:**

```bash
# Development mode (hot reload, server :3000 + client :5173)
npm run dev

# Production mode (server only :3000, serves pre-built client)
npm run build   # build client first
npm start
```

**Verify the server is running:**

```bash
curl http://localhost:3000/api/health
# Expected: {"status":"ok","timestamp":"..."}
```

### 1.3 Configure the MCP Server

The MCP servers are configured in `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "codebase-rag": {
      "command": "python",
      "args": [
        "C:\\Users\\maxco\\Documents\\agent-armory\\mcp-servers\\codebase-rag\\mcp-server-python\\server.py"
      ]
    },
    "codegraph": {
      "type": "stdio",
      "command": "cmd",
      "args": [
        "/c",
        "node",
        "C:\\Users\\maxco\\Documents\\agent-armory\\mcp-servers\\codegraph-mcp\\dist\\index.js"
      ],
      "env": {}
    },
    "agentboard": {
      "command": "python",
      "args": [
        "agentboard_mcp/server.py"
      ]
    }
  }
}
```

Enable all three in `.claude/settings.local.json`:

```json
{
  "enabledMcpjsonServers": ["agentboard", "codebase-rag", "codegraph"]
}
```

**Environment variables** (optional):

| Variable | Default | Purpose |
|---|---|---|
| `AGENTBOARD_URL` | `http://localhost:3000/api` | API base URL |
| `AGENTBOARD_PROJECT_DIR` | Parent of `agentboard_mcp/` | Project root for `npm` commands |

### 1.4 Agent ID

Many tools require an `agent_id` parameter. Use your model identifier -- e.g., `"claude-opus-4-6"`, `"claude-sonnet-4-5"`, `"gemini-3.1-pro"`. This is mandatory for traceability in the activity log.

### 1.5 Session Startup Checklist

At the start of every session, run these steps in order:

1. **Start the AgentBoard server** -- call `agentboard_start_server` (or run `npm run dev` manually)
2. **Health check** -- call `agentboard_health_check` to confirm the server is responding
3. **List projects** -- call `agentboard_list_projects` to see existing projects
4. **Get next task** -- call `agentboard_get_next_task` with your project ID and agent ID to pick up work

---

## 2. MCP Tools Reference

### 2.1 Server Management

| Tool | Purpose | Notes |
|---|---|---|
| `agentboard_health_check` | Verify server is reachable | Call first every session |
| `agentboard_start_server` | Start the AgentBoard server | Modes: `dev` (default) or `production`. Safe to call if already running. |
| `agentboard_server_status` | Check if server is running | Returns `{running: true/false}` |
| `agentboard_stop_server` | Stop the server | Destructive -- disconnects all clients |

### 2.2 Apps

Apps are the top-level organizational container in AgentBoard. Every project belongs to an app. Use `list_apps` to discover existing apps, or `create_app` to make a new one before creating projects.

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_apps` | List all apps | Supports `response_format` |
| `agentboard_create_app` | Create a new app | `name` (required), `description?`, `target_project_path?` |
| `agentboard_get_app` | Get single app by ID | `app_id`. Supports `response_format` |

### 2.3 Projects

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_projects` | List all projects | None |
| `agentboard_get_project` | Get project details | `project_id` |
| `agentboard_create_project` | Create a new project | `app_id`, `agent_id`, `name`, `project_type`, `idea`, `target_project_path?` |
| `agentboard_advance_phase` | Move to next phase | `project_id`, `agent_id`. **Agents only call this during implementation phases (10-12).** During doc phases (2-9), the human advances the phase after approving the document. |
| `agentboard_revert_phase` | Go back one phase | `project_id`, `agent_id`. Destructive. |

**Project types:** `new_feature`, `refactor`, `bug_fix`, `migration`, `integration`

### 2.4 Tasks

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_tasks` | List tasks (with filters) | `project_id`, `status?`, `phase?` |
| `agentboard_get_task` | Get single task details | `task_id` |
| `agentboard_get_next_task` | Auto-claim next actionable task | `project_id`, `agent_id`. Returns one of 4 response patterns: **(1) New task claimed** (200): a `ready` task was auto-claimed to `in-progress`, returns `{task, document}`. **(2) Existing task resumed** (200): an `in-progress` task already assigned to you, same shape. **(3) Pending review** (200): your submitted document is awaiting human review, returns `{task: null, document: null, pending_review: {...}}` -- wait. **(4) No tasks available** (404): returns `{error: "No tasks available"}`. |
| `agentboard_create_task` | Create a new task | `project_id`, `agent_id`, `title`, and optional fields |
| `agentboard_update_task` | Update task / transition status | `task_id`, `agent_id`, and fields to update. **Privileged tool** -- intended for Review Agents making corrections, NOT for worker agents managing their own task status. Never use on milestone tasks (`task_type: 'milestone'`) -- their status is managed automatically by `milestoneSync.js`. |

**Task types:** `milestone` (auto-created, linked to phase documents) and `implementation` (created by agents or humans during phase 10+).

### 2.5 Documents

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_documents` | List all phase documents | `project_id` |
| `agentboard_get_document` | Get full document content | `document_id` |
| `agentboard_submit_document` | Submit or resubmit a document for review | `document_id`, `agent_id`, `content?`, `notes` (required). **Status guard:** document must be in `template` or `rejected` status (any other returns HTTP 400). **Milestone guard:** linked milestone must be in `in-progress` status (otherwise returns HTTP 409 Conflict). **Blocks until reviewed.** |
| `agentboard_update_document` | Correct locked documents (review agents only) | `document_id`, `agent_id`, `content?`, `status?`, `rejection_feedback?` |

**Three actors, strict separation:**

- **Worker agents** use `agentboard_submit_document` to submit work. This locks the document and blocks the response until a human decides. Workers NEVER approve or reject.
- **Review agents** (privileged) use `agentboard_update_document` to correct locked (submitted) documents without changing status. Review agents NEVER approve or reject -- they only fix content.
- **Humans** are the sole authority for approval and rejection, acting through the UI (`PUT /documents/:id` with `status: "approved"` or `status: "rejected"`).

This separation is a design convention documented in `agentboard_mcp/DECISIONS.md`, not enforced by server code. Until server-side role enforcement is implemented (TODO.md Item #15), it depends on agents following this skill correctly.

### 2.6 Activity Log

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_get_activity_log` | Get audit trail | `project_id`, `actor?`, `action?`. NOT part of the standard worker agent work loop -- primarily for debugging and project oversight. |
| `agentboard_add_log_entry` | Record significant project-wide events | `project_id`, `agent_id`, `action`, `target?`, `detail?`. Records events NOT captured by automatic status changes. Distinct from task `notes`. NOT part of the standard worker agent work loop. |

**Valid `action` values:** `project_created`, `phase_approved`, `task_created`, `task_started`, `task_completed`, `task_updated`, `note_added`, `document_filled`, `document_approved`, `document_superseded`, `document_rejected`, `log_entry`.

**`response_format` parameter:** 16 read-only tools accept `response_format` (`"markdown"` or `"json"`, default `"markdown"`): `health_check`, `list_apps`, `get_app`, `list_projects`, `get_project`, `list_tasks`, `get_task`, `list_documents`, `get_document`, `get_activity_log`, `get_card`, `list_boards`, `get_board`, `list_workspace_cards`, `list_workspace_artifacts`, `get_workspace_artifact`. The other mutating tools do NOT accept it.

### 2.7 Workspace

Workspace boards are a lightweight kanban system under apps. Cards flow through: `backlog` -> `planning` -> `review` -> `implementation` -> `audit` -> `finished`. Artifacts are submitted at each stage to record plans, review notes, implementation notes, and audit reports.

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_boards` | List boards for an app | `app_id`. Supports `response_format` |
| `agentboard_create_board` | Create a board under an app | `app_id`, `agent_id`, `name`, `description?` |
| `agentboard_get_board` | Fetch a single board (incl. blocking-toggle policy) | `board_id`. Supports `response_format` |
| `agentboard_get_card` | Fetch a specific card + artifacts | `card_id`. Read-only. Supports `response_format` |
| `agentboard_get_next_card` | Auto-claim next available card | `board_id`, `agent_id`. Returns card + artifacts |
| `agentboard_submit_workspace_artifact` | Submit artifact to a card | `card_id`, `agent_id`, `content`, `type?` |
| `agentboard_list_workspace_cards` | List all cards on a board | `board_id`. Supports `response_format` |
| `agentboard_create_workspace_card` | Create a new card on a board (lands in `backlog`) | `board_id`, `agent_id`, `title`, optional `description`, `priority`, `assignee`, `depends_on`, `files_touched`, `notes` |
| `agentboard_update_workspace_card` | Update card status/fields | `card_id`, `agent_id`, plus fields to update |
| `agentboard_list_workspace_artifacts` | List artifacts on a card (append-only audit trail) | `card_id`. Supports `response_format` |
| `agentboard_get_workspace_artifact` | Fetch a single artifact's full content | `artifact_id`. Supports `response_format` |

---

## 3. The AgentBoard Workflow

### 3.1 Phase System

Every project progresses through 13 phases:

| Phase | Name | Document Required |
|---|---|---|
| 1 | Initialization | No (auto-completed) |
| 2 | Codebase Survey | `codebase_survey` |
| 3 | Requirements | `requirements` |
| 4 | Constraints | `constraints` |
| 5 | Risk Assessment | `risk_assessment` |
| 6 | Architecture | `architecture` |
| 7 | Contracts | `contracts` |
| 8 | Test Strategy | `test_strategy` |
| 9 | Task Breakdown | `task_breakdown` |
| 10 | Implementation | No |
| 11 | Verification | No |
| 12 | Review | No |
| 13 | Complete | No |

**Advance rule:** During doc phases (2-9), the human advances the phase after approving the document -- agents do not call `advance_phase` here. During implementation phases (10-12), agents call `agentboard_advance_phase` to advance freely.

### 3.2 Milestone Workflow (Phases 1-8)

Milestone task status is a **reflection** of document status, managed automatically by `milestoneSync.js`. Agents should NEVER use `agentboard_update_task` on milestone tasks. The agent's only direct interaction is submitting the document via `submit_document` -- all milestone state transitions flow automatically from that.

Milestone tasks are auto-created for phases 1-8 and linked to phase documents. The workflow:

1. **Claim milestone** -- `agentboard_get_next_task` auto-claims the next `ready` milestone
2. **Read the template** -- the response includes the linked document; study it carefully
3. **Research using companion tools** -- use codegraph and RAG to gather the data the template asks for (see Section 7 for which tools to use per phase)
4. **Fill and submit** -- `agentboard_submit_document` with your content and notes
5. **Wait for review** -- the call blocks until a human approves or rejects
6. **If approved** -- milestone auto-transitions to `done`, next milestone becomes `ready`
7. **If rejected** -- read feedback, revise, and resubmit

**About the templates:** Each document template contains `<!-- Agent: ... -->` inline instructions that tell you exactly what to write in each section. The templates have pre-structured tables, fields, and prompts -- follow them. Templates vary by project type (`new_feature`, `refactor`, `bug_fix`, `migration`, `integration`) and live in `server/src/templates/{project_type}/`. You don't need to find them yourself -- `get_next_task` returns the template content in the response.

The `ready->in-progress` guard requires only `assignee` (set automatically by `get_next_task`). Milestone tasks have `acceptance_criteria` pre-seeded from `milestoneTasks.js`, which satisfies the `in-progress->review` guard when milestoneSync submits notes.

**Phase 9 exception:** Phase 9 (Task Breakdown) has a document but no milestone task. Submit the document manually via `agentboard_submit_document`. The human advances the phase after approval.

### 3.3 Task State Machine

Tasks follow a strict state machine. Violations return HTTP 422.

```
backlog -----> ready -----> in-progress -----> review -----> done (FINAL)
  |              |              |                  |
  +-> blocked <--+-- blocked <--+---- blocked <----+
```

**Transitions:**

| From | Allowed To | Guards |
|---|---|---|
| `backlog` | `ready`, `blocked` | None |
| `ready` | `backlog`, `in-progress`, `blocked` | `in-progress` requires `assignee` |
| `in-progress` | `ready`, `review`, `blocked` | `review` requires at least one note AND `acceptance_criteria` |
| `review` | `in-progress`, `done`, `blocked` | `done` requires at least one note |
| `done` | (none) | **Final state -- no changes allowed to ANY field** |
| `blocked` | `previous_status` only | Automatically saved when entering blocked |

**Same-status no-op:** Transitioning a task to its current status succeeds silently without triggering validation. Relevant for Review Agents using `update_task` to add notes or correct metadata without changing state.

### 3.4 Typical Agent Session

```
1. agentboard_start_server          -- start if not running
2. agentboard_health_check          -- verify server is responding
3. agentboard_list_projects         -- find or create project
4. agentboard_get_next_task         -- claim work
5. (do the work: read template, fill document, or implement code)
6. agentboard_submit_document       -- for milestones: submit and wait for review
   OR submit for review with notes  -- for implementation: see Section 4.3
7. agentboard_get_next_task         -- claim next work item
8. (repeat 5-7 until phase complete)
9. (human advances phase during doc phases 2-9)
   agentboard_advance_phase         -- agents call this ONLY during implementation phases 10-12
10. (repeat 4-9 until project complete)
```

---

## 4. Common Patterns

### 4.1 Create a New Project

```
agentboard_create_project(
  app_id="<app-id>",
  agent_id="my-agent",
  name="Website Redesign",
  project_type="new_feature",
  idea="Redesign the company website with a modern UI and improved performance",
  target_project_path="/path/to/website-repo"
)
```

This creates: the project at phase 1, all phase documents (templates), and milestone tasks for phases 1-8. Phase 1 milestone is auto-completed; Phase 2 milestone starts as `ready`.

### 4.2 Work Through a Milestone

```
# 1. Claim the milestone
agentboard_get_next_task(project_id="<id>", agent_id="my-agent")
# Returns: {task: {milestone info}, document: {template content}}

# 2. Read the template, do research, fill the document

# 3. Submit with your content
agentboard_submit_document(
  document_id="<doc-id>",
  agent_id="my-agent",
  content="# Codebase Survey\n\n## Architecture\n...",
  notes="Surveyed the codebase. Key findings: React frontend, Express backend, SQLite DB. No major risks identified."
)
# This call BLOCKS until human reviews
```

### 4.3 Work an Implementation Task

```
# 1. Claim the task
agentboard_get_next_task(project_id="<id>", agent_id="my-agent")
# Returns: {task: {implementation task}, document: null}

# 2. Do the work (write code, run tests, etc.)

# 3. Submit for review with notes and acceptance criteria
agentboard_update_task(
  task_id="<id>",
  agent_id="my-agent",
  status="review",
  acceptance_criteria="API endpoint returns 200 with correct data format",
  notes=[{text: "Implemented endpoint with input validation...", timestamp: "2026-02-23T10:00:00Z", author: "my-agent"}],
  files_touched=["server/src/routes/users.js"]
)
```

Note: `update_task` is used here for the `in-progress->review` transition because no `submit_work` equivalent exists for implementation tasks (unlike `submit_document` for milestones). This is distinct from the privileged Review Agent usage.

### 4.4 Add Notes to Track Progress

Notes use **append semantics** -- they are added to the existing array, never replacing.

```
agentboard_update_task(
  task_id="<id>",
  agent_id="my-agent",
  notes=[{
    text: "Found a dependency issue with the auth module. Working around it by...",
    timestamp: "2026-02-23T14:30:00Z",
    author: "my-agent"
  }]
)
```

**Good notes** (context not in the document/code):
- "Chose SQLite over PostgreSQL because the project is single-node and persistence requirements are simple"
- "Skipped unit tests for the WebSocket relay because it's a thin pass-through with no logic"
- "Found that milestoneSync.js already handles the cascade -- no new code needed"

**Bad notes** (prohibited -- summaries of the action):
- "Document submitted"
- "Updated content"
- "Completed the architecture document"

**Principle:** Notes capture decisions, tradeoffs, surprises, and context. If none apply, say "No additional context -- straightforward document."

### 4.5 Block and Unblock a Task

```
# Block (previous_status saved automatically)
agentboard_update_task(task_id="<id>", agent_id="my-agent", status="blocked")

# Unblock (must return to previous_status)
# First check what previous_status is:
agentboard_get_task(task_id="<id>")
# Then transition back:
agentboard_update_task(task_id="<id>", agent_id="my-agent", status="in-progress")
```

---

## 5. Error Handling

### State Machine Violations (HTTP 422)

When a transition is invalid, the error response includes all 7 fields:

| Field | Type | Purpose |
|---|---|---|
| `valid` | boolean | Always `false` for violations |
| `error` | string | Human-readable explanation -- **read this first** |
| `code` | string | Machine-readable error code (e.g., `INVALID_TRANSITION`) |
| `from` | string | Current task status |
| `to` | string | Attempted target status |
| `allowed` | array | Valid transitions from current status |
| `missing_fields` | array | Guard fields that are missing |

**Always read the `error` field carefully** -- it tells you exactly what to fix.

### State Conflict (HTTP 409)

The resource's state changed between when you last read it and when you tried to act on it. Most common: trying to submit a document whose linked milestone was moved out of `in-progress`. **Recovery:** Refetch resources (`get_project`, `get_task`, `get_document`) to get current state, then decide whether to retry.

### Common Mistakes

| Mistake | Fix |
|---|---|
| Skip states (e.g., `backlog` -> `done`) | Follow valid transitions one step at a time |
| Move to `in-progress` without `assignee` | Set `assignee` in the same update |
| Move to `review` without notes or acceptance_criteria | Add at least one note AND `acceptance_criteria` in the same update or beforehand |
| Try to modify a `done` task | `done` is final -- no field changes allowed |
| Call `advance_phase` during doc phases (2-9) | Only the human advances doc phases. Agents use `advance_phase` only during phases 10-12. |
| Unblock to wrong status | Can only return to `previous_status` |

---

## 6. WebSocket Events

The AgentBoard UI uses WebSocket for real-time updates. If you're building a client:

- Connect to `ws://localhost:3000/ws`
- Events: `connected`, `project_created`, `task_updated`, `phase_advanced`, `document_updated`
- `connected` -- sent immediately on new connection. Payload: `{ event: 'connected', data: { timestamp: '<ISO8601>' } }`. Confirms the WebSocket link is live.
- **Always refetch from API** after receiving events -- never update state directly from payloads

---

## 7. Companion MCP Servers

AgentBoard works alongside two other MCP servers. These are not optional extras -- they provide the data you need to fill document templates properly instead of guessing.

**Load tools via `ToolSearch` before first use** (search for `codegraph` or `rag`).

### 7.1 Codegraph (dependency analysis)

| Tool | Purpose |
|---|---|
| `codegraph_scan` | Scan project, build dependency graph. **Must call first.** |
| `codegraph_get_stats` | File counts, most connected/depended-on files |
| `codegraph_get_dependencies` | What does file X import? |
| `codegraph_get_dependents` | What imports file X? (what breaks if X changes) |
| `codegraph_get_change_impact` | Blast radius of changing file(s) |
| `codegraph_get_subgraph` | Dependency subgraph around a file |
| `codegraph_find_entry_points` | Find entry point files |
| `codegraph_list_files` | List all scanned files |

**When to use codegraph in the workflow:**

| Phase | Template Sections It Feeds | What To Do |
|---|---|---|
| **2 -- Codebase Survey** | §2 Directory Structure, §3 Entry Points, §4 Module Inventory, §8 Dependency Analysis, §13 Integration Points | Run `codegraph_scan` on the target project first. Use `get_stats` for the overview, `find_entry_points` for §3, `list_files` + `get_dependencies` for §4, `get_stats` for §8. This is your primary research tool for this phase. |
| **5 -- Risk Assessment** | Complexity hotspots, change-risk areas | Use `get_stats` to find most-connected files (high coupling = high risk). Use `get_dependents` on files you plan to modify to understand blast radius. |
| **6 -- Architecture** | §3 Component Architecture, §10 File Structure | Use `get_subgraph` to understand how proposed components relate to existing modules. Use `get_dependencies`/`get_dependents` to validate your component boundaries aren't creating circular deps. |
| **9 -- Task Breakdown** | Task ordering, dependency chains | Use `get_change_impact` to understand which files a task will touch and what else might break. This informs task dependencies (`depends_on`). |
| **10+ -- Implementation** | Before writing code | Use `get_change_impact` before modifying files to check what tests/modules you might break. |

### 7.2 Codebase RAG (constraint enforcement)

| Tool | Purpose |
|---|---|
| `rag_search` | **Primary tool.** Semantic search across constraints, patterns, and code. Supports `source_type` filter (`"all"`, `"docs"`, `"code"`, `"constraints"`). |
| `rag_query_impact` | Blast radius analysis for changing a specific file (exports, dependents, semantically similar files). |

**When to use RAG in the workflow:**

| Phase | What To Do |
|---|---|
| **2 -- Codebase Survey** | Use `rag_search` to discover existing architectural patterns, coding conventions, and API contracts for §7 Architectural Patterns and §10 Code Conventions. The index auto-builds on first call. |
| **4 -- Constraints** | **Critical phase for RAG.** Use `rag_search(source_type="constraints")` with queries like "database access patterns", "API conventions", "error handling", "module boundaries" to discover constraints that already exist in the codebase. The constraints doc should reflect reality, not invent rules. |
| **6 -- Architecture** | Before submitting, run `rag_search(source_type="docs")` with your proposed architectural changes to verify they don't violate existing patterns. |
| **7 -- Contracts** | Use `rag_search(source_type="docs")` to find existing API contracts and interface patterns. Your contracts doc must be consistent with what already exists. |
| **10+ -- Implementation** | Before writing code, run `rag_search` describing your planned change. Use `source_type="docs"` first for rules, then `source_type="code"` for examples. After implementation, run `rag_query_impact` on modified files to catch downstream breakage. |

### 7.3 Setup Sequence

At the start of a session, after the AgentBoard server is running:

```
1. ToolSearch("codegraph")              -- load codegraph tools
2. ToolSearch("rag")                    -- load RAG tools
3. codegraph_scan(path="<target>")      -- REQUIRED every session (graph is in-memory only, lost when MCP server restarts)
4. rag_search(query="<initial topic>")  -- first call auto-bootstraps the index for this project
```

**Codegraph** rebuilds from scratch every session -- its graph lives in memory only (`let currentGraph = null` in the MCP server). **RAG** persists to disk via ChromaDB in a per-machine cache (`%LOCALAPPDATA%\codebase-rag\<project-hash>\` on Windows; `~/.cache/codebase-rag/<project-hash>/` elsewhere) -- nothing is written into the project tree. The new server auto-detects the project root, builds the index on first call (a few seconds), and runs an in-process filesystem watcher so the index stays current as files change. There is no manual setup, indexing, or status step.

Both servers are configured in `.mcp.json` and enabled in `.claude/settings.local.json`.
