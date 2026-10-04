---
name: agentboard
description: Skill for using the AgentBoard AI project management app and its cloud-hosted MCP server. Use when the user wants to manage phase-based projects (phases, milestones, documents, tasks), work with workspace boards (apps, boards, cards, artifacts) for ad-hoc orchestration, authenticate the AgentBoard MCP, interact with any AgentBoard MCP tool, or needs guidance on either workflow. Triggers on "manage project", "use agentboard", "agentboard workflow", "create a project in agentboard", "set up agentboard", "authenticate agentboard", "create a workspace card", "create a board", "orchestrate cards", "submit artifact", "workspace board", or "fetch a card".
---

# AgentBoard Skill

Use the AgentBoard AI project management system to create, track, and manage software projects through a structured phase-based workflow with strict state machine enforcement.

---

## 0. Mental model — read this first

AgentBoard runs **two parallel workflows** on the same cloud backend. They share the auth surface, the activity log, the agent_id convention, and the companion MCPs (codegraph, codebase-rag), but they're independent pipelines with different state machines. Pick the right one for the work in front of you:

| Workflow | Unit of work | State authority | Lifecycle | When to use |
|---|---|---|---|---|
| **Phase-based project** | Phase document (13 fixed phases) | The document is authority; the milestone task is a reflection that the server keeps in sync. | `template → submitted → approved` (or `rejected → revise → resubmit`). Humans approve; agents never approve their own work. After phase 9, switches to free-form implementation tasks in phases 10-12. | A new feature, refactor, bug fix, migration, or integration where the rigor of "write the requirements doc, write the architecture, then implement" is appropriate. The phases force a discovery-before-implementation discipline. |
| **Workspace board** | Card on a board (kanban columns) | The card is authority; artifacts are append-only outputs attached to it. | `backlog → planning → review → implementation → audit → finished`, with two verdict-driven rejection loops: `review_note` FAIL → `planning`, `audit_report` FAIL → `implementation`. `finished` is terminal. | Ad-hoc work that doesn't fit the 13-phase rigor — orchestrated parallel cards (via `/orchestrate`), discrete cleanup tasks, work spawned by `/architecture` from a spec's Card Slices. |

**Three actors, strict separation** (applies to both workflows):

- **Worker agent** does the work and submits. Never approves, never rejects. For phase work: calls `agentboard_submit_document` (blocks until human decides). For workspace work: calls `agentboard_submit_workspace_artifact` (append-only, no blocking, no approval implied).
- **Review agent** (privileged) corrects locked documents in place via `agentboard_update_document` (phase) or appends `review_note` artifacts (workspace). Never approves, never rejects.
- **Human** is the sole approval authority. For phase work: through the UI (`PUT /documents/:id` with status). For workspace work: column transitions reflect human decisions when blocking gates are on; auto-progression when they're off (per the board's `auto_transitions`).

**The MCP-mediated state machine is strict** — illegal transitions return HTTP 422 with a structured error naming `from`, `to`, `allowed`, and `missing_fields`. Read the error; don't guess. State conflicts (someone else changed the resource between your read and your write) return HTTP 409; refetch and retry.

**`agent_id` is mandatory on every mutation** for traceability in the activity log. Use your model identifier (`"claude-opus-4-7"`, `"claude-sonnet-4-6"`, etc.). Don't invent ids; the activity log is the audit trail used to debug what happened weeks later.

**Companion MCPs are not optional context decoration** — they're how you get the data the phase documents and workspace artifacts demand. `codegraph` gives you dependency structure (in-memory, must be scanned every session). `codebase-rag` gives you semantic search (cached on-disk, first-run indexing can take significant time on non-trivial codebases). The main agent (the one driving the session) is responsible for pre-warming both before spawning subagents — see §6.0.

**The /-commands are the entry points:**
- `/foundation` — interactive spec-building session (architecturally silent) → produces `docs/specs/<file>.md`
- `/architecture` — reads an approved spec, runs the level-aware architecture pipeline → produces architecture document + workspace cards from its Card Slices
- `/orchestrate` — runs the workspace pipeline (planning → review → implementation → audit) across the cards `/architecture` created
- AgentBoard MCP tools — for ad-hoc work or to inspect/manage state outside the orchestration commands

The typical flow for a new project is: `/foundation` → `/architecture` → `/orchestrate`. The typical flow for ad-hoc cleanup is `/sweep` (creates cards) → `/orchestrate`. The typical flow for a phase-based project is `agentboard_create_project` → milestone loop through phases 1-9 → implementation tasks in phases 10-12.

---

## 1. Setup

### 1.1 Cloud-Hosted Service

AgentBoard is fully cloud-hosted. There is **no local installation, no Node.js, no Python, no `npm` commands, and no servers to start**.

| Component | URL |
|---|---|
| AgentBoard app (UI + REST API) | `https://agent-board.app` |
| MCP server (HTTP transport) | `https://mcp.agent-board.app/mcp` |

The MCP server is always available — agents talk to it directly through the configured MCP client. Just call the tools.

### 1.2 MCP Servers Are Plugin-Installed

The three MCP servers this plugin uses — `agentboard` (cloud, HTTP transport), `codegraph` (local, stdio), and `codebase-rag` (local, stdio) — are configured automatically when this plugin is installed. There is nothing to add to `.mcp.json` or `.claude/settings.local.json` by hand. If the agentboard MCP tools aren't visible at all, the plugin isn't installed; if they're visible but only the two auth tools are, you need to authenticate (see §1.3).

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

The right startup sequence depends on which workflow you're about to do (see §0). Both share the first three steps, then diverge.

**Shared startup (steps 1-3 — always run, in order):**

1. **Authenticate if needed.** If only `agentboard_authenticate` and `agentboard_complete_authentication` are visible in the agentboard tool surface, run the bootstrap from §1.3. If the full tool surface is visible, you're authenticated.
2. **Health check** — call `agentboard_health_check`. Confirms the cloud service is reachable (AgentBoard is fully cloud-hosted; this is a reachability check, not a local-process check).
3. **Pre-warm companion MCPs (if you will spawn subagents or do data-intensive work).** See §6.0. This is the main agent's job — codegraph_scan upfront (in-memory, per-session), verify RAG is indexed and returns real results (not `status: "indexing"`). Subagents that hit cold-start companion MCPs silently degrade.

**Then diverge by workflow:**

**Phase-based project work (4a-5a):**

4a. **List projects** — `agentboard_list_projects` to see existing projects. If you're starting fresh, `agentboard_create_project` with `name`, `project_type`, `idea`, `target_project_path`.
5a. **Claim next task** — `agentboard_get_next_task` with your project ID and `agent_id`. The response tells you what to do next: a new milestone to fill (proceed to §3.2 milestone workflow), an in-progress task to resume, a submitted document awaiting human review (wait), or no tasks available (404 — you may be done with this phase).

**Workspace-board work (4b-5b):**

4b. **Find the board** — `agentboard_list_apps` then `agentboard_list_boards` on the chosen app. If the cards you need don't exist yet, they were probably going to be created by `/architecture` from a spec's Card Slices, or by `/sweep` from a codebase audit; see those commands' docs.
5b. **Either claim a card or run /orchestrate** — for single-card work, `agentboard_get_next_card` with `board_id`, `agent_id`, optional `column`. For orchestrated parallel-card work across multiple cards and waves, run `/orchestrate` (which uses the `orchestrate` skill — the authoritative wave-by-wave logic lives there).

**Don't mix the two workflows on the same unit of work** — phase milestones and workspace cards are independent state machines. A workspace card is never a milestone; never call `agentboard_update_task` on a card (cards use `agentboard_update_workspace_card`).

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
| `agentboard_list_tasks` | List tasks (with filters) | `project_id`, `status?`, `phase?`, `limit?`, `offset?` |
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
| `agentboard_get_activity_log` | Get audit trail | `project_id`, `actor?`, `action?`, `limit?` (default 50, cap 500), `offset?`. NOT part of the standard worker agent work loop -- primarily for debugging and project oversight. |
| `agentboard_add_log_entry` | Record significant project-wide events | `project_id`, `agent_id`, `action`, `target?`, `detail?`. Records events NOT captured by automatic status changes. Distinct from task `notes`. NOT part of the standard worker agent work loop. |

**Valid `action` values:** `project_created`, `phase_approved`, `task_created`, `task_started`, `task_completed`, `task_updated`, `note_added`, `document_filled`, `document_approved`, `document_superseded`, `document_rejected`, `log_entry`.

**`response_format` parameter:** Read-only tools accept `response_format` (`"markdown"` or `"json"`, **default `"json"`** — JSON is data; markdown is presentation, so machine callers get JSON by default and a human browsing a transcript opts in with `response_format="markdown"`): in the core surface — `health_check`, `list_projects`, `get_project`, `list_tasks`, `get_task`, `list_documents`, `get_document`, `get_activity_log`; in the workspace surface — `list_apps`, `list_boards`, `get_board`, `list_workspace_cards`, `get_card`, `list_workspace_artifacts`, `get_workspace_artifact`, `resolve_artifact_prefix`. Mutating tools (creates, updates, submits) do NOT accept it.

---

### 2.6 Workspace Boards

Workspace boards are a separate, ad-hoc pipeline alongside the phase system — for everyday work that doesn't go through the 13-phase document workflow. Cards move through columns: `backlog → planning → review → implementation → audit → finished`. For the orchestration pipeline (parallel agents per wave, checkpoint logic, blocking toggles) see the `orchestrate` skill.

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
| `agentboard_list_workspace_cards` | List cards on a board (filter by status/column) | `board_id`, `status?`, `fields?` (default slim set — omits description/notes bodies), `include_notes?` (`count` default / `latest` / `all`), `limit?`, `offset?`. **Default returns `notes_count` int, not full notes array — use `get_card` or `include_notes="all"` for note bodies.** |
| `agentboard_get_card` | Fetch a card by ID. Returns artifacts bundled. | `card_id`, `include_notes?` (`all` default / `latest` / `count`), `response_format?` |
| `agentboard_get_next_card` | Auto-claim the next actionable card from a column. Triggers the workspace-card-guidance hook. | `board_id`, `agent_id`, `column?` |
| `agentboard_create_workspace_card` | Create a card on a board. Use when an agent needs to spawn follow-up work from the card it's currently on (e.g. a planning agent splits a card into smaller implementation cards). Don't pollute one card with multiple distinct units of work. | `board_id`, `title`, `description?`, `priority?`, `depends_on?` |
| `agentboard_update_workspace_card` | Append notes / update fields (title, description, priority, assignee, files_touched; notes and files_touched append). Triggers the workspace-card-guidance hook. It *can* force a `status`/column change, but **in the orchestration pipeline cards advance automatically on artifact submission** — manually moving a pipeline card fights the auto-advance and is rarely correct (see "Workspace pipeline" below). | `card_id`, `agent_id`, fields to update |

**Artifacts** are the outputs an agent produces for a card — typed records like `plan`, `review_note`, `implementation_note`, `audit_report`. Storage is **append-only**: nothing is deleted or content-rewritten, and `column_at_creation` is captured for audit context.

**Implicit auto-supersede (server-enforced, no flag):** submitting a new wave-deliverable (`plan`, `review_note`, `implementation_note`, `audit_report`) to a card that already has one of the same type automatically marks the predecessor *superseded* — the prior row stays in the DB (readable via `include_superseded=true`) but drops out of the default list. `general` artifacts (facts bundles, research notes) **stack** as active siblings and are never auto-superseded. There is no caller-supplied supersede parameter. The POST response includes `superseded_artifact_ids` telling you what your submission replaced.

**`review_note` verdict marker (MANDATORY):** every `review_note` body MUST contain `## Verdict: PASS` or `## Verdict: FAIL` — a level-2 markdown heading on its own line, value inline, case-insensitive. Missing/malformed → HTTP 422 `REVIEW_NOTE_MISSING_VERDICT` (read the `instructions_for_agents` field; the app is NOT broken). FAIL routes the card back to `planning` (both blocking and non-blocking modes); PASS keeps the existing blocking-aware advance to `implementation`. Reviewers never call `update_workspace_card` to move the card — the verdict drives routing.

**`audit_report` verdict marker (MANDATORY):** every `audit_report` body MUST contain `## Verdict: PASS`, `## Verdict: PASS WITH NOTES`, or `## Verdict: FAIL` — a level-2 markdown heading on its own line, single value inline. A bold `**Verdict:**`, an `### Verdict:`, or a line listing all three values → HTTP 422 `AUDIT_REPORT_MISSING_VERDICT` (read `instructions_for_agents`; the app is NOT broken). FAIL routes the card to `implementation` **unconditionally** (regardless of `audit_blocking`); PASS / PASS WITH NOTES advances to `finished` only when `audit_blocking` is OFF, else holds in `audit` for a human checkpoint. Audit agents never call `update_workspace_card` to move the card — the verdict drives routing.

**Always pass an explicit `artifact_type` (`type`) on every submit.** Column inference was removed: an omitted type is stored as `general`, which triggers **no** transition and silently strands the card. Pass `plan` / `review_note` / `implementation_note` / `audit_report` for the four advancing wave deliverables, and `general` for non-advancing outputs (facts bundles, research notes, the architecture-pipeline artifacts which carry their real type in a leading sentinel line).

**Recognized artifact types** (the plugin has hooks that gate them by type, so use these exact strings):

| Type | Produced by | Triggers gate |
|---|---|---|
| `plan` | `plan-compose-agent` (Wave 1 Phase B) | existing `artifact-quality-gate` (TODO/TBD/placeholder check + codegraph/RAG-usage prompt) |
| `review_note` | `review-agent` (Wave 2) | existing `artifact-quality-gate` |
| `implementation_note` | `implementation-agent` (Wave 3) | existing `artifact-quality-gate` |
| `audit_report` | `audit-compose-agent` (Wave 4 Phase B) | existing `artifact-quality-gate` |
| `ARCH_FACTS_BUNDLE_V2` | `architecture-research-agent` (Phase A of `/architecture`) | `validate-architecture-artifact` (sentinel + JSON schema + classification rules check) |
| `ARCH_BUNDLE_AUDIT_V2` | `architecture-classification-auditor` (Phase A audit) | `validate-architecture-artifact` |
| `architecture_document` | `architecture-compose-l{1,2,3}` (Phase B of `/architecture`) | `validate-architecture-artifact` (level marker, required sections, slice schema, R#/Q# coverage) |
| `ARCH_DESIGN_REVIEW_V1` | `architecture-design-reviewer` (Phase B review) | `validate-architecture-artifact` (findings schema, audit_artifact_id field check) |

**Gate dispatch is artifact-type-aware** (post-architecture-pipeline rework): the existing `artifact-quality-gate.sh` script early-exits cleanly for the four architecture-pipeline artifact types — those are handled by `validate-architecture-artifact.sh` instead. The "no open questions" and "you used codegraph/RAG" prompt injection from `inject-quality-gate-prompt.sh` is suppressed for architecture-pipeline submissions (architecture-compose agents legitimately surface open questions in design, and they don't use codegraph/RAG by design — discovery is done by `architecture-research-agent`). For the four original types (`plan`, `review_note`, `implementation_note`, `audit_report`), the existing gate behavior is unchanged: artifacts must be free of TODO/TBD/placeholder text and reference specific files/line numbers.

| Tool | Purpose | Key Parameters |
|---|---|---|
| `agentboard_submit_workspace_artifact` | Append an artifact to a card. Triggers either the `artifact-quality-gate` (original four types) or `validate-architecture-artifact` (architecture-pipeline types) per the dispatch table above. `review_note` additionally requires the `## Verdict:` marker (above) — without it the server returns HTTP 422. | `card_id`, `agent_id`, `artifact_type`, `content` |
| `agentboard_list_workspace_artifacts` | List artifacts on a card — **metadata-only by default** (no bodies; superseded hidden). Use this for cross-card lookups (e.g. an implementation agent finding the planning card's `plan` artifact). Pass `fields='...,content'` or `view='full'` for bodies, `include_superseded=true` for history, `limit`/`offset` to paginate. Returns the `{total, artifacts}` envelope. | `card_id`, `view?`, `fields?`, `include_superseded?`, `limit?`, `offset?` |
| `agentboard_get_workspace_artifact` | Fetch a single artifact by full ID, with content (bodies up to 500 000 chars return in full). Cheaper than `get_card` when only one artifact body is needed. This is the path Phase B compose agents (plan-compose, audit-compose, architecture-compose-l{1,2,3}, architecture-design-reviewer) use to fetch their input bundle — orchestrators pass the artifact ID, agents fetch. | `artifact_id` |
| `agentboard_resolve_artifact_prefix` | Resolve an 8–32 hex-char artifact UUID prefix to a single artifact within a card or board scope. Use when a list was truncated before emitting full UUIDs or you only have a short id. Unique match → artifact; ambiguous → 409 with `candidates[]`; none → 404. | `scope_id`, `scope` (`card`\|`board`), `prefix` |

**Workspace pipeline at a glance:**

```
backlog → planning → review → implementation → audit → finished
              ▲          │            ▲            │
              │  review  │ FAIL       │  audit     │ FAIL
              └──────────┘            └────────────┘
   review_note FAIL → planning     audit_report FAIL → implementation
```

Agents are spawned per-card per-wave by `/orchestrate`. Each agent fetches the card, performs its wave's work, and **submits its artifact — which advances the card automatically**. All transitions are **server-enforced and verdict-driven**; agents never move a card themselves:

- `planning → review` happens on `plan` submit (unconditional).
- `implementation → audit` happens on `implementation_note` submit (unconditional).
- `review` routes on the `review_note` verdict: FAIL → `planning` (unconditional); PASS → `implementation` when `review_blocking` is OFF, else holds for human approval.
- `audit` routes on the `audit_report` verdict: FAIL → `implementation` (unconditional); PASS / PASS WITH NOTES → `finished` when `audit_blocking` is OFF, else holds for a human checkpoint.

Waves 2 and 4 additionally open with a single **board-level cross-card consistency barrier** (`cross-card-plan-reviewer` / `cross-card-implementation-auditor`) that holds all cards in the column at once and finds inconsistencies *between* cards that the per-card agents cannot see. It runs before the per-card agents and fails each inconsistent card itself by submitting that wave's FAIL verdict (`review_note` / `audit_report` with `## Verdict: FAIL`), so the server routes the card back the normal way above; the per-card agents then run only on the cards it cleared.

Wave agents do NOT call `agentboard_update_workspace_card` to move the card. The `orchestrate` skill has the per-wave prompt templates and full pipeline logic.

---

## 3. The AgentBoard Workflow

### 3.1 Phase System

Every project progresses through 13 phases. Phases 1-9 are document phases (an authored, reviewed, approved document is the deliverable for each); phases 10-12 are implementation phases (free-form tasks); phase 13 is the terminal state. The structure enforces discovery-before-implementation: you cannot start phase 10 (Implementation) without having approved all 9 prior documents.

| Phase | Name | Document | What it's FOR |
|---|---|---|---|
| 1 | Initialization | none (auto-completed) | Project scaffold exists — server creates the project record, all phase document templates, and the milestone tasks for phases 1-8. No agent work. |
| 2 | Codebase Survey | `codebase_survey` | Establish ground truth about what the codebase currently is — directory structure, entry points, module inventory, dependency analysis, integration points, code conventions. This is the empirical baseline every later phase reasons against. **codegraph is the primary tool here.** |
| 3 | Requirements | `requirements` | What the work must accomplish, in concrete acceptance-criteria form — R-numbered requirements and Q-numbered quality requirements. The spec the rest of the project is judged against. |
| 4 | Constraints | `constraints` | The named rules and conventions the work must respect — state-machine constraints, naming conventions, security policies, performance targets, contract invariants. **RAG is the primary tool here** (`source_type="constraints"` queries to discover what already exists). The constraints doc should reflect reality, not invent rules. |
| 5 | Risk Assessment | `risk_assessment` | What could go wrong, where the blast radius lives, which coupling hotspots the work touches. **codegraph `get_stats` and `get_dependents` are the primary tools here** — high-coupling files imply high change-risk. |
| 6 | Architecture | `architecture` | Component architecture, structural decisions, and the level-aware design output. Often produced by the `/architecture` skill rather than authored by hand (the skill runs a research → audit → classification → compose → review pipeline and produces this document plus workspace cards from its Card Slices section). |
| 7 | Contracts | `contracts` | The interface contracts between components — function signatures, API surfaces, message shapes, schemas. Must be consistent with what already exists (use RAG to verify). |
| 8 | Test Strategy | `test_strategy` | The verification plan — what kinds of tests, what coverage, how each requirement maps to its verification. Test code does not get written here; the strategy does. |
| 9 | Task Breakdown | `task_breakdown` | Implementation tasks ordered by dependency. **Phase 9 is the exception**: it has a document but no milestone task; submit the document manually. After approval, the project moves to phase 10 and the task list authored here becomes the queue of implementation tasks. |
| 10 | Implementation | none | Free-form implementation tasks (not milestones) created by agents or humans. Agents call `agentboard_advance_phase` to move forward; the document state machine doesn't gate progression here. |
| 11 | Verification | none | Execute the test strategy from phase 8 against the implementation from phase 10. Tasks here are about running, observing, and fixing — not adding features. |
| 12 | Review | none | Final review before completion. Anything surfaced here either gets fixed (back to phase 10/11) or accepted as a known limitation. |
| 13 | Complete | none | Terminal state. No further transitions. The project is done. |

**Advance rule:** During doc phases (2-9), the human advances the phase after approving the document — agents do not call `advance_phase` here. During implementation phases (10-12), agents call `agentboard_advance_phase` to advance freely. The phase-1 transition to phase 2 is automatic on project creation.

**Why the structure is strict:** without forcing the doc-before-code order, agents will write code against assumptions that the requirements phase would have caught, against constraints the constraints phase would have surfaced, against an architecture the architecture phase would have explicitly rejected. The 13 phases exist to make those failure modes impossible by sequencing.

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

### 3.4 Typical Agent Sessions

There are two shapes depending on which workflow you're in (§0). Both share the §1.6 startup; the diverge happens at step 4.

**Phase-based project session (worker agent):**

```
1-3. §1.6 shared startup: auth → health_check → companion-MCP pre-warm (§6.0)
4.   agentboard_list_projects        -- pick the project, or agentboard_create_project to start one
5.   agentboard_get_next_task        -- claim next milestone or task (response shape tells you which)
6.   (do the work: study the linked template, do research via codegraph/RAG, fill the document fields)
7.   agentboard_submit_document      -- milestone: submit + wait (call blocks until human approves/rejects)
     OR agentboard_update_task       -- implementation task: status="review" + notes + acceptance_criteria
8.   On approval: server auto-completes the milestone and the next milestone becomes `ready`. On rejection:
     read rejection_feedback, revise, resubmit (status returns to `template` then back through `submit_document`).
9.   agentboard_get_next_task        -- claim the next item
10.  Repeat 6-9 until the phase is done.
11.  Phase 2-9: human advances the phase after approving the document; agents do NOT call advance_phase here.
     Phase 10-12: agents call agentboard_advance_phase to move forward.
12.  Repeat 5-11 until phase 13 (Complete) is reached.
```

**Workspace-board session (single-card worker):**

```
1-3. §1.6 shared startup: auth → health_check → companion-MCP pre-warm (§6.0)
4.   agentboard_list_apps + agentboard_list_boards  -- find the board you're working on
5.   agentboard_get_next_card        -- auto-claim the next actionable card in a column
                                        OR agentboard_get_card on a specific card_id
6.   (do the work specific to your wave: planning agents write plans, review agents validate plans,
     implementation agents write code, audit agents verify against the plan + acceptance criteria)
7.   agentboard_submit_workspace_artifact   -- append the typed artifact (always pass an explicit `type`:
                                               plan / review_note / implementation_note / audit_report).
                                               SUBMITTING IS WHAT ADVANCES THE CARD: planning → review and
                                               implementation → audit happen automatically on submit; the
                                               review transition routes on the review_note's `## Verdict:`
                                               marker (PASS → implementation, FAIL → planning); the audit
                                               transition routes on the audit_report's `## Verdict:` marker
                                               (FAIL → implementation unconditionally; PASS / PASS WITH NOTES
                                               → finished when audit_blocking is OFF, else holds). All
                                               server-side (§2.6). Storage is append-only; a new same-type
                                               deliverable auto-supersedes the prior one (§2.6).
8.   (no manual card move)                  -- do NOT call agentboard_update_workspace_card to move the card
                                               through the pipeline; submission drives advancement. Use
                                               update_workspace_card only to append notes or update fields
                                               (title, description, files_touched, priority).
9.   Repeat for the next card you claim, or end the session if /orchestrate handed you a single card.
```

**Orchestrated workspace session (main agent driving multiple cards in parallel):** don't follow the single-card pattern above. Run `/orchestrate` — the `orchestrate` skill carries the wave-by-wave logic, prompt templates, checkpoint policy, retry policy, and per-wave failure handling. Do not duplicate that here.

**A worked example for new project flow (most common):**

```
/foundation                          -- interactive spec-building session → docs/specs/<file>.md
/architecture                        -- reads the spec, runs the level-aware architecture pipeline
                                        → architecture document + cards on a workspace board
/orchestrate                         -- runs the planning → review → implementation → audit pipeline
                                        across the cards from /architecture
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

### Workspace Artifact & Card Errors

These surface on the workspace-board pipeline (`submit_workspace_artifact`, card transitions), distinct from the phase task state machine above.

| Code | HTTP | When | Recovery |
|---|---|---|---|
| `REVIEW_NOTE_MISSING_VERDICT` | 422 | `review_note` body has no valid `## Verdict: PASS\|FAIL` level-2 heading | Read `instructions_for_agents`; resubmit with the heading. The app is not broken. |
| `AUDIT_REPORT_MISSING_VERDICT` | 422 | `audit_report` body has no valid `## Verdict: PASS\|PASS WITH NOTES\|FAIL` level-2 heading (bold `**Verdict:**`, `### Verdict:`, or a line listing all three all fail) | Read `instructions_for_agents`; resubmit with a single level-2 heading carrying one value. |
| `CARD_FINISHED` | 422 | artifact submit (or in-place edit) on a card already in `finished` — `finished` is terminal | Reopen first: `agentboard_update_workspace_card` to PATCH the card's `status` to a non-finished column (e.g. `audit`), then resubmit. The response body carries a `reopen_with` hint. |
| `INVALID_IDEMPOTENCY_KEY` | 400 | `Idempotency-Key` header outside 1–255 printable-ASCII characters | Use a valid key (or omit it — submissions are idempotent automatically). |
| `IDEMPOTENCY_KEY_REUSED` | 409 | the same `Idempotency-Key` was reused for a *different* request | Use a fresh key for the new request, or refetch to confirm the prior submission already landed. |

**`finished` is terminal (Rule 4).** A `finished` card rejects any artifact submission or in-place edit with `422 CARD_FINISHED`. To reopen, a human (or an agent acting on explicit instruction) PATCHes the card to a non-finished status via `agentboard_update_workspace_card` first. SYSTEM transitions never reopen a finished card — only a MANUAL status change does.

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

AgentBoard works alongside two other MCP servers. These are not optional extras — they provide the data you need to fill document templates properly instead of guessing.

**Load tools via `ToolSearch` before first use** (search for `codegraph` or `rag`).

### 6.0 Main-Agent Pre-warm Responsibility

**The main agent (the one driving the session, the one that spawns subagents via `/orchestrate`, `/architecture`, or direct `Agent` calls) is responsible for pre-warming the companion MCPs before spawning subagents that may use them.** This is non-optional. Cold-start failure modes are silent:

- **codegraph is in-memory and per-session.** Every fresh MCP process restart wipes the graph. If a subagent calls `codegraph_get_dependencies` before any agent in the session has called `codegraph_scan`, the call fails (no graph loaded) and the subagent may silently fall back to guessing structure from filenames. **Main-agent action:** run `codegraph_scan` on the target project root once, upfront, at session start. Verify it returned a non-empty stats result.
- **codebase-rag indexes on first call.** First-run indexing builds an on-disk vector index for the project tree. The build time is variable — small projects finish in seconds; non-trivial plugin or monorepo trees can take significantly longer (minutes are realistic). While indexing, `rag_search` returns `status: "indexing"` with a hint to retry. If indexing fails or the HNSW index is corrupted, calls return a hard error (`Error loading hnsw index`). If a subagent calls `rag_search` during the indexing window, it may retry once and then proceed without semantic results — silently degrading the data it produces. **Main-agent action:** call `rag_search` with any short test query upfront, confirm it returns real results (not `status: "indexing"`, not a transport error), THEN spawn subagents. If indexing isn't finishing, surface that to the user before doing the work; don't spawn agents into a known-degraded environment.

**Detection signature for subagent-silent-skip:** a Wave 1 plan or implementation_note that doesn't cite specific file:line ranges and doesn't reference patterns from `existing_patterns_hits` or `constraint_hits` — that subagent's RAG was probably unavailable at call time and it filled the gap with general knowledge instead of project facts. The main agent's pre-warm is what prevents that.

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

**First-call note:** if the project has never been indexed, the first call returns `status: "indexing"` while the index builds. Build time varies with codebase size — seconds for small projects, minutes for non-trivial plugin or monorepo trees. The main agent is responsible for pre-warming this before spawning subagents (see §6.0 — subagents that hit `status: "indexing"` may silently degrade). If the server can't find a project root, it returns `status: "no_project"` with a hint. If the server returns a transport-level error like `Error loading hnsw index`, the index itself is corrupted — clearing the cache and re-indexing is the recovery path, not a retry.

**When to use RAG in the workflow:**

| Phase | What To Do |
|---|---|
| **2 -- Codebase Survey** | Use `rag_search` with `source_type="docs"` to surface existing architectural patterns and conventions for §7 Architectural Patterns and §10 Code Conventions. |
| **4 -- Constraints** | **Critical phase for RAG.** Use `rag_search` with `source_type="constraints"` and queries like "database access patterns", "API conventions", "error handling", "module boundaries" to discover constraints that already exist in the codebase. The constraints doc should reflect reality, not invent rules. |
| **6 -- Architecture** | Before submitting, use `rag_search` with your proposed architectural changes to verify they don't violate existing patterns. |
| **7 -- Contracts** | Use `rag_search` (`source_type="docs"` or `"all"`) to find existing API contracts and interface patterns. Your contracts doc must be consistent with what already exists. |
| **10+ -- Implementation** | Before writing code, use `rag_search` describing your planned change to surface relevant patterns and constraints. Use `rag_query_impact` on files you plan to modify to understand blast radius. |

### 6.3 Setup Sequence (Main Agent, Every Session)

At the start of every session, after authenticating to AgentBoard:

```
1. ToolSearch("codegraph")             -- load codegraph tools
2. ToolSearch("rag")                   -- load RAG tools (rag_search, rag_query_impact)
3. codegraph_scan(path="<target>")     -- REQUIRED every session (graph is in-memory only,
                                          lost on MCP server restart). Verify it returns a
                                          non-empty stats result before continuing.
4. rag_search("<short test query>")    -- pre-warm RAG. The first call in a never-indexed
                                          project returns status: "indexing" while the index
                                          builds. Build time varies with codebase size; retry
                                          on a calm cadence until you get real results back.
                                          DO NOT spawn subagents until this returns hits — a
                                          subagent that hits an indexing window may silently
                                          degrade its output (§6.0).
```

**If RAG is taking unreasonably long** (more than a few minutes on a codebase you don't expect to be huge) or returns a transport-level error like `Error loading hnsw index`, **stop and surface to the user** — don't spawn subagents into a degraded environment. The recovery is clearing the per-project cache and re-indexing, not retrying the query.

**Codegraph** rebuilds from scratch every session — its graph lives in memory only. **Codebase RAG** auto-detects the project root, builds an on-disk index in a per-machine cache directory on first run, and watches the filesystem to keep it current after that. No setup, init, or status calls are needed beyond the pre-warm above. Both MCP servers are auto-installed by this plugin (see §1.2).