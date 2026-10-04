---
name: agentboard
description: Skill for using the AgentBoard AI project management app and its cloud-hosted MCP server. Use when the user wants to manage phase-based projects (phases, milestones, documents, tasks), work with workspace boards (apps, boards, cards, artifacts) for ad-hoc orchestration, authenticate the AgentBoard MCP, interact with any AgentBoard MCP tool, or needs guidance on either workflow. Triggers on "manage project", "use agentboard", "agentboard workflow", "create a project in agentboard", "set up agentboard", "authenticate agentboard", "create a workspace card", "create a board", "orchestrate cards", "submit artifact", "workspace board", or "fetch a card".
---

# AgentBoard Skill

Use the AgentBoard AI project management system to create, track, and manage software projects through a structured phase-based workflow with strict state machine enforcement.

---

## 1. Setup

### 1.1 Cloud-Hosted Service

AgentBoard is fully cloud-hosted. There is **no local installation, no Node.js, no Python, no `npm` commands, and no servers to start**.

| Component | URL |
|---|---|
| AgentBoard app (UI + REST API) | `https://agent-board.app` |
| MCP server (HTTP transport) | `https://mcp.agent-board.app/mcp` |

The MCP server is always available — agents talk to it directly through the configured MCP client. Just call the tools.

### 1.2 Configure the MCP Server

The MCP servers are configured in `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "agentboard": {
      "type": "http",
      "url": "https://mcp.agent-board.app/mcp"
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
    "codebase-rag": {
      "command": "python",
      "args": [
        "C:\\Users\\maxco\\Documents\\agent-armory\\mcp-servers\\codebase-rag\\mcp-server-python\\server.py"
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

### 1.3 Authenticate

The AgentBoard MCP requires OAuth-style authentication before any tool other than the two auth tools is callable. On a fresh session — or any time tokens have expired — only `agentboard_authenticate` and `agentboard_complete_authentication` are visible. The full tool surface (health_check, projects, tasks, documents, workspace, etc.) appears only after the bootstrap completes.

**Bootstrap flow:**

1. **Start the OAuth flow** — call `agentboard_authenticate` (no parameters). It returns an authorization URL.
2. **Share the URL with the user** and ask them to open it in their browser and authorize.
3. The user authorizes; their browser is redirected to `http://localhost:<port>/callback?code=...&state=...`. On remote sessions the page itself may fail to load, but the URL in the browser's address bar is the value you need.
4. **Ask the user to copy the full URL from the browser's address bar.**
5. **Complete the flow** — call `agentboard_complete_authentication` with that URL as the `callback_url` argument. The remaining tools become available immediately.

**Detecting auth state:** if you see only `agentboard_authenticate` and `agentboard_complete_authentication` in the agentboard tool surface, run the bootstrap. If the rest of the tools are visible, you're authenticated.

**Security — handle the callback URL as a secret:**

The callback URL contains a short-lived authorization code that converts to an access token. Treat it the same way you'd treat a password:

- Use it ONLY as the `callback_url` argument to `agentboard_complete_authentication`.
- Do NOT log it, echo it back to the user, write it into a card note, an artifact, the activity log, a commit message, or any file.
- Discard it from your working memory immediately after the auth call.

### 1.4 Verify Connectivity

After authenticating, call `agentboard_health_check` to confirm the cloud service is reachable. If the call fails *post-auth*, the cloud service itself is unreachable — check status at `agent-board.app`.

### 1.5 Agent ID

Many tools require an `agent_id` parameter. Use your model identifier -- e.g., `"claude-opus-4-6"`, `"claude-sonnet-4-5"`, `"gemini-3.1-pro"`. This is mandatory for traceability in the activity log.

### 1.6 Session Startup Checklist

At the start of every session, run these steps in order:

1. **Authenticate if needed** — if only `agentboard_authenticate` and `agentboard_complete_authentication` are visible, run the bootstrap from §1.3
2. **Health check** -- call `agentboard_health_check` to confirm the cloud service is reachable
3. **List projects** -- call `agentboard_list_projects` to see existing projects
4. **Get next task** -- call `agentboard_get_next_task` with your project ID and agent ID to pick up work

---

## 2. MCP Tools Reference

### 2.1 Authentication & Connectivity

| Tool | Purpose | Notes |
|---|---|---|
| `agentboard_authenticate` | Start the OAuth flow. Returns an authorization URL for the user to open. | No parameters. See §1.3 for the full bootstrap. Available pre-auth. |
| `agentboard_complete_authentication` | Complete the OAuth flow with the callback URL from the user's browser. | Required: `callback_url`. Treat the URL as a secret — see §1.3. Available pre-auth. |
| `agentboard_health_check` | Verify the cloud service is reachable | Call first after authenticating. Not visible pre-auth. |

### 2.2 Projects

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_projects` | List all projects | None |
| `agentboard_get_project` | Get project details | `project_id` |
| `agentboard_create_project` | Create a new project | `agent_id`, `name`, `project_type`, `idea`, `target_project_path?` |
| `agentboard_advance_phase` | Move to next phase | `project_id`, `agent_id`. **Agents only call this during implementation phases (10-12).** During doc phases (2-9), the human advances the phase after approving the document. |
| `agentboard_revert_phase` | Go back one phase | `project_id`, `agent_id`. Destructive. |

**Project types:** `new_feature`, `refactor`, `bug_fix`, `migration`, `integration`

### 2.3 Tasks

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_tasks` | List tasks (with filters) | `project_id`, `status?`, `phase?` |
| `agentboard_get_task` | Get single task details | `task_id` |
| `agentboard_get_next_task` | Auto-claim next actionable task | `project_id`, `agent_id`. Returns one of 4 response patterns: **(1) New task claimed** (200): a `ready` task was auto-claimed to `in-progress`, returns `{task, document}`. **(2) Existing task resumed** (200): an `in-progress` task already assigned to you, same shape. **(3) Pending review** (200): your submitted document is awaiting human review, returns `{task: null, document: null, pending_review: {...}}` -- wait. **(4) No tasks available** (404): returns `{error: "No tasks available"}`. |
| `agentboard_create_task` | Create a new task | `project_id`, `agent_id`, `title`, and optional fields |
| `agentboard_update_task` | Update task / transition status | `task_id`, `agent_id`, and fields to update. **Privileged tool** -- intended for Review Agents making corrections, NOT for worker agents managing their own task status. Never use on milestone tasks (`task_type: 'milestone'`) -- their status is managed automatically by the server's milestone-sync logic. |

**Task types:** `milestone` (auto-created, linked to phase documents) and `implementation` (created by agents or humans during phase 10+).

### 2.4 Documents

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

This separation is a design convention; the server does not enforce it today, so it depends on agents following this skill correctly.

### 2.5 Activity Log

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_get_activity_log` | Get audit trail | `project_id`, `actor?`, `action?`. NOT part of the standard worker agent work loop -- primarily for debugging and project oversight. |
| `agentboard_add_log_entry` | Record significant project-wide events | `project_id`, `agent_id`, `action`, `target?`, `detail?`. Records events NOT captured by automatic status changes. Distinct from task `notes`. NOT part of the standard worker agent work loop. |

**Valid `action` values:** `project_created`, `phase_approved`, `task_created`, `task_started`, `task_completed`, `task_updated`, `note_added`, `document_filled`, `document_approved`, `document_superseded`, `document_rejected`, `log_entry`.

**`response_format` parameter:** Read-only tools accept `response_format` (`"markdown"` or `"json"`, default `"markdown"`): in the core surface — `health_check`, `list_projects`, `get_project`, `list_tasks`, `get_task`, `list_documents`, `get_document`, `get_activity_log`; in the workspace surface — `list_apps`, `list_boards`, `get_board`, `list_workspace_cards`, `get_card`, `list_workspace_artifacts`, `get_workspace_artifact`. Mutating tools (creates, updates, submits) do NOT accept it.

---

### 2.6 Workspace Boards

Workspace boards are a separate, ad-hoc pipeline alongside the phase system — for everyday work that doesn't go through the 13-phase document workflow. Cards move through columns: `backlog → planning → review → implementation → audit → finished`. For the orchestration pipeline (parallel agents per wave, checkpoint logic, blocking toggles) see the `workspace-orchestration` skill.

**Apps** group boards (typically one app per codebase or product).

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_apps` | List all apps | None |
| `agentboard_create_app` | Create an app | `name`, optional `target_project_path` |

**Boards** are kanban-style column sets that hold cards. Each board has an `auto_transitions` setting (`{review_blocking, audit_blocking}`) that controls whether the orchestration pipeline pauses at review and audit checkpoints.

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_boards` | List boards in an app | `app_id` |
| `agentboard_get_board` | Fetch a single board's config (`auto_transitions`, description). Use this before orchestrating to read the checkpoint settings. | `board_id` |
| `agentboard_create_board` | Create a board | `app_id`, `name`, optional `auto_transitions` |

**Cards** are the unit of agent work. Each card moves through the orchestration pipeline column-by-column. **Cards do NOT use the phase task state machine** — their lifecycle is governed entirely by board column transitions and the orchestration pipeline. Never reach for `agentboard_update_task` on a card.

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_list_workspace_cards` | List cards on a board (filter by status/column) | `board_id`, `status?` |
| `agentboard_get_card` | Fetch a card by ID. Returns artifacts bundled. | `card_id`, `response_format?` |
| `agentboard_get_next_card` | Auto-claim the next actionable card from a column. Triggers the workspace-card-guidance hook. | `board_id`, `agent_id`, `column?` |
| `agentboard_create_workspace_card` | Create a card on a board. Use when an agent needs to spawn follow-up work from the card it's currently on (e.g. a planning agent splits a card into smaller implementation cards). Don't pollute one card with multiple distinct units of work. | `board_id`, `title`, `description?`, `priority?`, `depends_on?` |
| `agentboard_update_workspace_card` | Update card fields (title, description, notes, status/column). Triggers the workspace-card-guidance hook. | `card_id`, `agent_id`, fields to update |

**Artifacts** are the outputs an agent produces for a card — typed records like `plan`, `review_note`, `implementation_note`, `audit_report`. They are **append-only**: there is no edit or delete, and `column_at_creation` is captured for audit context. To correct a prior artifact, submit a new one.

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_submit_workspace_artifact` | Append an artifact to a card. Triggers the SUBMISSION QUALITY GATE hook — the artifact must be free of TODO/TBD/placeholder text and reference specific files/line numbers. | `card_id`, `agent_id`, `artifact_type`, `content` |
| `agentboard_list_workspace_artifacts` | List artifacts on a card without pulling the full card. Use this for cross-card lookups (e.g. an implementation agent reading the planning card's plan artifact). | `card_id` |
| `agentboard_get_workspace_artifact` | Fetch a single artifact by ID. Cheaper than `get_card` when only one artifact body is needed. | `artifact_id` |

**Workspace pipeline at a glance:**

```
backlog → planning → review → implementation → audit → finished
           ↑           ↓ (rejection)
           └───────────┘
```

Agents are spawned per-card per-wave by the `/orchestrate` command. Each agent fetches the card, performs its wave's work, and submits an artifact + updates the card's column. The `workspace-orchestration` skill has the per-wave prompt templates and full pipeline logic.

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

Milestone task status is a **reflection** of document status, managed automatically by the server's milestone-sync logic. Agents should NEVER use `agentboard_update_task` on milestone tasks. The agent's only direct interaction is submitting the document via `submit_document` -- all milestone state transitions flow automatically from that.

Milestone tasks are auto-created for phases 1-8 and linked to phase documents. The workflow:

1. **Claim milestone** -- `agentboard_get_next_task` auto-claims the next `ready` milestone
2. **Read the template** -- the response includes the linked document; study it carefully
3. **Research using companion tools** -- use codegraph and RAG to gather the data the template asks for (see Section 6 for which tools to use per phase)
4. **Fill and submit** -- `agentboard_submit_document` with your content and notes
5. **Wait for review** -- the call blocks until a human approves or rejects
6. **If approved** -- milestone auto-transitions to `done`, next milestone becomes `ready`
7. **If rejected** -- read feedback, revise, and resubmit

**About the templates:** Each document template contains `<!-- Agent: ... -->` inline instructions that tell you exactly what to write in each section. The templates have pre-structured tables, fields, and prompts -- follow them. Templates vary by project type (`new_feature`, `refactor`, `bug_fix`, `migration`, `integration`); you don't need to find them yourself -- `get_next_task` returns the appropriate template content in the response.

The `ready->in-progress` guard requires only `assignee` (set automatically by `get_next_task`). Milestone tasks have `acceptance_criteria` pre-seeded by the server, which satisfies the `in-progress->review` guard when the server submits notes during milestone-sync.

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
1. agentboard_health_check          -- verify cloud service is reachable
2. agentboard_list_projects         -- find or create project
3. agentboard_get_next_task         -- claim work
4. (do the work: read template, fill document, or implement code)
5. agentboard_submit_document       -- for milestones: submit and wait for review
   OR submit for review with notes  -- for implementation: see Section 4.3
6. agentboard_get_next_task         -- claim next work item
7. (repeat 4-6 until phase complete)
8. (human advances phase during doc phases 2-9)
   agentboard_advance_phase         -- agents call this ONLY during implementation phases 10-12
9. (repeat 3-8 until project complete)
```

---

## 4. Common Patterns

### 4.1 Create a New Project

```
agentboard_create_project(
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
- "Found that the server's milestone-sync logic already handles the cascade -- no new code needed"

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

## 6. Companion MCP Servers

AgentBoard works alongside two other MCP servers. These are not optional extras -- they provide the data you need to fill document templates properly instead of guessing.

**Load tools via `ToolSearch` before first use** (search for `codegraph` or `rag`).

### 6.1 Codegraph (dependency analysis)

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

### 6.2 Codebase RAG (semantic search)

The codebase-rag MCP exposes two tools. The server auto-detects the project root (looking for `.git`, `package.json`, `pyproject.toml`, `Cargo.toml`, or `go.mod`, or honoring `RAG_PROJECT_ROOT`), auto-builds the index in a per-machine cache on first call, and runs a filesystem watcher to keep it current. There is no setup, init, status, or health-check tool — just call the search tools directly.

| Tool | Purpose |
|---|---|
| `rag_search` | Semantic search across the project. Inputs: `query` (3–2000 chars), `num_results` (1–20, default 5), `source_type` (`"all"` (default) / `"docs"` (constraints + patterns) / `"code"` / `"constraints"`). Returns ranked results with file paths and relevance scores. |
| `rag_query_impact` | Show what depends on a file before you change it: exports, importers, and semantically similar files that may need coordinated edits. Inputs: `file_path` (relative to project root, forward slashes), `num_similar` (1–20, default 5). |

**First-call note:** if the project has never been indexed, the first call may return `status: "indexing"` while the index builds (a few seconds). Try again. If the server can't find a project root, it returns `status: "no_project"` with a hint.

**When to use RAG in the workflow:**

| Phase | What To Do |
|---|---|
| **2 -- Codebase Survey** | Use `rag_search` with `source_type="docs"` to surface existing architectural patterns and conventions for §7 Architectural Patterns and §10 Code Conventions. |
| **4 -- Constraints** | **Critical phase for RAG.** Use `rag_search` with `source_type="constraints"` and queries like "database access patterns", "API conventions", "error handling", "module boundaries" to discover constraints that already exist in the codebase. The constraints doc should reflect reality, not invent rules. |
| **6 -- Architecture** | Before submitting, use `rag_search` with your proposed architectural changes to verify they don't violate existing patterns. |
| **7 -- Contracts** | Use `rag_search` (`source_type="docs"` or `"all"`) to find existing API contracts and interface patterns. Your contracts doc must be consistent with what already exists. |
| **10+ -- Implementation** | Before writing code, use `rag_search` describing your planned change to surface relevant patterns and constraints. Use `rag_query_impact` on files you plan to modify to understand blast radius. |

### 6.3 Setup Sequence

At the start of a session, after authenticating to AgentBoard:

```
1. ToolSearch("codegraph")             -- load codegraph tools
2. ToolSearch("rag")                   -- load RAG tools (rag_search, rag_query_impact)
3. codegraph_scan(path="<target>")     -- REQUIRED every session (graph is in-memory only, lost when MCP server restarts)
4. rag_search("<first query>")         -- RAG auto-bootstraps; first call in a never-indexed project takes a few seconds
```

**Codegraph** rebuilds from scratch every session — its graph lives in memory only. **Codebase RAG** auto-detects the project root, builds an index in a per-machine cache directory on first run, and watches the filesystem to keep it current. No setup, init, or status calls are needed — call `rag_search` or `rag_query_impact` directly. If the first query returns `status: "indexing"`, retry after a few seconds.

Both servers are configured in `.mcp.json` and enabled in `.claude/settings.local.json`.