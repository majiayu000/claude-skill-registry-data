---
name: db-migrate
description: '[DevOps] Use when running or creating database migrations.'
disable-model-invocation: false
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Create or run database migrations following the repository's documented patterns.

**Workflow:**

1. **Identify** — Determine migration type (schema migration vs data/document migration)
2. **Create** — Generate migration using the configured migration tool or data migration executor (see backend-patterns-reference.md under the reference-docs root, default docs/project-reference, overridable via docsRoots.projectReference.path in docs/project-config.json)
3. **Verify** — Run migration and confirm schema/data changes

**Key Rules:**

- Follow the repository's migration patterns (see CLAUDE.md / project-reference docs)
- For CREATE: present the migration design and wait for explicit user approval before creating migration files
- Always backup data before destructive migrations
- Use the configured data migration executor for data/document migrations (see backend-patterns-reference.md under the reference-docs root, default docs/project-reference, overridable via docsRoots.projectReference.path in docs/project-config.json)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

Database migration: $ARGUMENTS

## Instructions

1. **Parse arguments**:
    - `add <name>` → Create new schema/data migration with the configured tool
    - `update` → Apply pending migrations
    - `list` → List all migrations and status
    - `rollback` → Revert last migration
    - No argument → Show migration status

2. **Identify database provider + migration tooling** from project config and project-reference docs:
    - Relational stores: managed by the configured schema-migration tool.
    - Document/key-value/event stores: may use code-based migrations or startup executors defined by the repository.

3. **For schema migrations**:

Add migration:

    ```bash
    {configured-migration-add-command} <MigrationName>
    ```

Update database:

    ```bash
    {configured-migration-update-command}
    ```

List migrations:

    ```bash
    {configured-migration-list-command}
    ```

4. **For data/document migrations**:
    - Often code-based migrations run by the configured migration executor (see backend-patterns-reference.md under the reference-docs root, default docs/project-reference, overridable via docsRoots.projectReference.path in docs/project-config.json)
    - Location: the repository's configured migration folder — discover from `backend-patterns-reference.md` under that same reference-docs root (`docsRoots.projectReference.path` in `docs/project-config.json`)
    - Migrations run automatically on application startup
    - To create: Generate new migration class following existing patterns

5. **Safety checks**:
    - Warn before applying migrations to production
    - Show what changes will be applied
    - Recommend backup before destructive operations

6. **Migration Safety Review (MANDATORY for non-local environments)**:
    - Before applying to staging/production, spawn `database-admin` sub-agent (`agent_type: "database-admin"`) for safety review
    - Review criteria: locking behavior on large tables, index creation impact under concurrent writes, rollback strategy, zero-downtime feasibility
    - Present findings and get explicit user approval before running the configured migration apply command on non-local environments

## Sub-Agent Type Override

> **MANDATORY for non-local migration apply:** Spawn `database-admin` sub-agent (`agent_type: "database-admin"`) for safety review BEFORE applying to staging or production.
> **Rationale:** `database-admin` specializes in query plans, index impact analysis, locking behavior, backup/restore, and replication — context the main agent lacks for production-safe migration decisions.

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

**Prerequisites:** **MUST ATTENTION READ** before executing:

- `domain-entities-reference.md` under the reference-docs root (default `docs/project-reference`; `docsRoots.projectReference.path` in `docs/project-config.json` overrides) — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `source-test-drift-check` — When source behavior changes, reconcile the affected tests from evidence; code, fix, test or review work changes behavior → .claude/skills/shared/protocols/source-test-drift-check.md
- `sub-agent-selection` — Pick the sub-agent type from the routing guide; choosing which sub-agent to spawn → .claude/skills/shared/protocols/sub-agent-selection.md
- `understand-code-first` — Read and trace the target and existing patterns before changing code; planning or editing code → .claude/skills/shared/protocols/understand-code-first.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code/conventions BEFORE any modification or explanation. The code graph is optional advice for high-risk blast radius (a hint that may be stale), never a requirement.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim; never speculate. Confidence >80% to act, <60% = do NOT recommend; "not enough evidence" is valid output.

<!-- /SYNC:evidence-based-reasoning:reminder -->


<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->


## Closing Reminders

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Source/Test Drift:** Source change → inspect affected tests; don't test migration code.
- **Sub-Agent Selection:** Route specialized domains to matching specialist agent; NEVER `code-reviewer`.
- **Nested Task Creation:** Expand child phases, link parent when nested, one `in_progress`.
- **Understand Code First:** Search 3+ patterns and read code before any modification.

- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.
  **MANDATORY IMPORTANT MUST ATTENTION** READ the following files before starting:

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

> **[IMPORTANT]** Analyze how big the task is and break it into many small todo tasks systematically before starting — this is very important.
