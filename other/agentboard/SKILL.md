---
name: agentboard
description: Use when the user wants to operate the AgentBoard cloud workflow from Codex, including project phases, milestones, documents, tasks, apps, boards, cards, artifacts, authentication, and orchestration guidance.
---

# AgentBoard

AgentBoard is a cloud-hosted project manager for AI coding work.

Use it for:

- phase-based projects with strict document gates
- workspace-board orchestration for ad hoc or parallel work
- task, document, card, and artifact management
- session handoffs and progress tracking

## Setup

AgentBoard itself is remote:

- app: `https://agent-board.app`
- MCP: `https://mcp.agent-board.app/mcp`

This plugin ships with a bundled MCP config at `.mcp.json`.

Bundled servers:

- `agentboard`
- `codegraph`
- `codebase-rag`
- `clear-thought`

Use the bundled MCP setup for this plugin. If the local companion server paths do not exist on the current machine, fix them before relying on `codegraph` or `codebase-rag`.

## Authentication

If only these tools are visible:

- `agentboard_authenticate`
- `agentboard_complete_authentication`

the session is not authenticated yet.

Bootstrap flow:

1. Call `agentboard_authenticate`.
2. Ask the user to open the returned URL and authorize.
3. Ask the user for the full browser callback URL.
4. Call `agentboard_complete_authentication` with that callback URL.
5. Call `agentboard_health_check`.

Treat the callback URL as a secret. Never echo it, log it, or write it to files, notes, artifacts, or commits.

## Agent Identity

When `agent_id` is required, use a stable Codex-facing identifier such as:

- `codex-gpt-5-5`
- `codex-gpt-5-4`

Use the same identifier consistently within one project for traceability.

## Two Workflows

### Phase-Based Projects

Use for larger or riskier work that needs explicit planning and review.

Phases:

1. Initialization
2. Codebase Survey
3. Requirements
4. Constraints
5. Risk Assessment
6. Architecture
7. Contracts
8. Test Strategy
9. Task Breakdown
10. Implementation
11. Verification
12. Review
13. Complete

Rules:

- During phases 2 through 9, humans approve documents and advance phases.
- Agents should not call `agentboard_advance_phase` during those document phases.
- Agents may call `agentboard_advance_phase` during phases 10 through 12.

### Workspace Boards

Use for refactors, migrations, cleanup, debugging, and backlog execution.

Board flow:

`backlog -> planning/review -> implementation -> audit -> finished`

Rules:

- Cards do not use the phase task state machine.
- Artifacts are append-only.
- Review and audit are quality gates, not bookkeeping.

## Core Tool Guidance

### Projects

- `agentboard_list_projects`
- `agentboard_get_project`
- `agentboard_create_project`
- `agentboard_advance_phase`
- `agentboard_revert_phase`

### Tasks

- `agentboard_list_tasks`
- `agentboard_get_task`
- `agentboard_get_next_task`
- `agentboard_create_task`
- `agentboard_update_task`

Task rules:

- Never use `agentboard_update_task` on milestone tasks.
- Milestone progress is driven through linked documents.
- For implementation tasks, moving `in-progress -> review` requires notes and acceptance criteria.

### Documents

- `agentboard_list_documents`
- `agentboard_get_document`
- `agentboard_submit_document`
- `agentboard_update_document`

Document rules:

- Workers submit documents.
- Humans approve or reject documents.
- If a document is rejected, read the feedback and resubmit.

### Workspace

- `agentboard_list_apps`
- `agentboard_create_app`
- `agentboard_list_boards`
- `agentboard_get_board`
- `agentboard_create_board`
- `agentboard_list_workspace_cards`
- `agentboard_get_card`
- `agentboard_get_next_card`
- `agentboard_create_workspace_card`
- `agentboard_update_workspace_card`
- `agentboard_submit_workspace_artifact`
- `agentboard_list_workspace_artifacts`
- `agentboard_get_workspace_artifact`

Artifact rules:

- Submit only actionable artifacts.
- No TODO, TBD, FIXME, placeholder text, or vague future-work language.
- Reference specific files and lines whenever the artifact claims code understanding or proposed change scope.

## Milestone Flow

For milestone tasks:

1. Claim the next task.
2. Read the linked document template carefully.
3. Use `codegraph` and `codebase-rag` to gather evidence.
4. Fill the document.
5. Submit it with meaningful notes.
6. Wait for approval or rejection.

Phase 9 is the exception: it has a document but no milestone task. Submit the document directly.

## Task State Machine

Allowed statuses:

- `backlog`
- `ready`
- `in-progress`
- `review`
- `done`
- `blocked`

Rules:

- `done` is final.
- `blocked` returns only to `previous_status`.
- Never skip required guard fields when moving status.

## Companion Tools

### Codegraph

Use for:

- entry points
- coupling hotspots
- change impact
- dependency analysis

Typical calls:

- `codegraph_scan`
- `codegraph_get_stats`
- `codegraph_find_entry_points`
- `codegraph_get_dependencies`
- `codegraph_get_dependents`
- `codegraph_get_change_impact`

### Codebase RAG

Use for:

- existing patterns
- constraints already present in the codebase
- related files before making coordinated changes

Typical calls:

- `rag_search`
- `rag_query_impact`

If the first call returns indexing status, retry after a short wait.

## Error Recovery

- If auth tools are the only visible tools, re-run the auth bootstrap.
- If `agentboard_health_check` fails after auth, stop and tell the user the cloud service is unreachable.
- If a task transition fails with validation errors, read the error fields and satisfy the missing guards before retrying.
- If a document or task state changed remotely, refetch current state before acting again.
