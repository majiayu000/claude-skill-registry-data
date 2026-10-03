---
name: initiate-task
description: Canonical task creation skill for this repo. Use when the user invokes initiate-task, asks to start a new project task, classify and approve versioned deliverable contracts, create a tracker-maintenance task with target:tracker, query current task state before creation, coordinate project tasks, or create a primary task with capability_dependencies on usable skills from another known project.
---

# Initiate Task

Use this skill as the canonical task creation entrypoint. The only task
operations are exposed as skills:

- `$initiate-task`: initiate a new task
- `$continue-task`: continue an existing task
- `$testing-session`: start, inspect, or stop a read-only project testing run

Matt Pocock phases are task state. Do not split them into separate repo-local
skills.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: workflow products in this repo are built as skills and
workflow packs for Codex, Claude Code, opencode, and Antigravity-style
environments. Do not turn task initiation into an `npx`, `npm`, Python, or raw
script calling workflow. Helper scripts may support validation and JSON state
inspection only.

## Required Reading

Before acting:

1. Read the root `AGENTS.md`.
2. Read `references/matt-pocock-skills.md`.
3. Read this skill completely.
4. Read `registry/agents-md.json`.
5. If work enters or continues a Matt phase, inspect the matching upstream Matt
   Pocock skill named in `references/matt-pocock-skills.md`.

## Load Everything First

Load, load, load, load, load before doing anything with a task.

For every initiate request:

1. Read root `AGENTS.md`.
2. Read `registry/agents-md.json`.
3. Read `projects/<project-slug>/AGENTS.md`.
4. Read `projects/<project-slug>/project.json`.
5. Read `projects/<project-slug>/tasks/index.json`.
6. Query the derived skill catalog and project task list through the read-only
   state helper when available.
7. Query the registered project-instruction state through the same helper.
8. Query testing-session summaries through the same helper. Load only the index
   summaries and pointers by default; do not read full `events.jsonl` streams
   unless the user asks or the task requires exact testing-session evidence.
9. Read every task JSON listed in the index whose status is not `done`.
10. Read the selected task JSON if a task id is provided.
11. Review active, blocked, in-progress, recently completed work, and testing
    session summaries.
12. Report conflicts or state gaps before taking any task action.

If project state is missing, do not create a separate scaffold from this skill.
Hand off to `$setup-workflow-project` first, then stop. After setup succeeds,
the next invocation may initiate the first task.

## State Model

Project state lives in `project.json`:

```json
{
  "project_slug": "health",
  "name": "Health",
  "project_state": "active",
  "goal": "",
  "domain": "",
  "agents_md": "projects/health/AGENTS.md",
  "active_conventions": [],
  "ecc_concepts_applied": [],
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

Task index lives in `tasks/index.json`:

```json
{
  "project_slug": "health",
  "tasks": [
    {
      "task_id": "health-001",
      "title": "Short task title",
      "task_kind": "workflow-change",
      "status": "todo",
      "matt_phase": "intake",
      "updated_at": "YYYY-MM-DD"
    }
  ]
}
```

Each task lives in `tasks/<task-id>.json`:

```json
{
  "task_id": "health-001",
  "project_slug": "health",
  "title": "Short task title",
  "task_kind": "workflow-change",
  "status": "todo",
  "matt_phase": "intake",
  "explicit_next_action_required": true,
  "summary": "What this task is trying to build",
  "acceptance_criteria": [],
  "ecc_concepts_applied": [],
  "context_snapshot": {
    "summary": "",
    "must_load": []
  },
  "phase_guard": {
    "selected_next_action": "none",
    "approved_artifacts": [],
    "process_exceptions": []
  },
  "deliverable_migration": {
    "status": "native",
    "target_contract_version": 1,
    "frozen_phase": null,
    "approved_at": "YYYY-MM-DD",
    "approval_note": "Operator approved the proposed deliverable contract."
  },
  "deliverable_contracts": [
    {
      "deliverable_id": "health-workflow-skill",
      "contract_version": 1,
      "kind": "packaged-skill",
      "operation": "create",
      "role": "primary",
      "ownership_boundary": "project-packaged",
      "owner_project": "health",
      "target_surface": "projects/health/skills/health-workflow",
      "runtime_visibility": "project-local-inactive",
      "runtime_targets": ["codex"],
      "member_deliverable_ids": [],
      "required_artifacts": [
        {
          "artifact_id": "health-workflow-bundle",
          "artifact_role": "primary",
          "locator_type": "path",
          "locator": "projects/health/skills/health-workflow",
          "validation": "packaged-skill-bundle"
        }
      ],
      "allowed_support_artifacts": [],
      "required_guidance": [
        {
          "guidance_id": "health-project-policy",
          "source": "projects/health/AGENTS.md",
          "evidence": "The packaged skill follows the owning project's file, domain, and runtime policy."
        }
      ],
      "eval_plan": [
        {
          "eval_id": "health-workflow-fresh-agent",
          "kind": "fresh-agent",
          "required": true
        }
      ],
      "completion_conditions": [
        {
          "condition_id": "health-workflow-bundle-valid",
          "type": "artifact-valid",
          "reference": "health-workflow-bundle"
        },
        {
          "condition_id": "health-workflow-behavior-passed",
          "type": "eval-passed",
          "reference": "health-workflow-fresh-agent"
        }
      ]
    }
  ],
  "artifact_bindings": [
    {
      "deliverable_id": "health-workflow-skill",
      "artifact_id": "health-workflow-bundle",
      "artifact_role": "primary",
      "locator_type": "path-prefix",
      "locator": "projects/health/skills/health-workflow/"
    }
  ],
  "behavior_evidence": [],
  "capability_dependencies": [],
  "dependency_steps": [],
  "dependency_artifacts": [],
  "dependency_provenance": [],
  "dependencies": [],
  "related_tasks": [],
  "linked_artifacts": [
    "projects/health/skills/health-workflow"
  ],
  "session_log": [],
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

The dependency fields are optional and should be omitted for ordinary tasks with
no external workflow capability use.

The deliverable fields are required for every new task. A task must have one or
more version-1 contracts and at least one primary deliverable before its JSON is
written. Each contract declares a stable id, kind, create/update operation,
role, ownership boundary, owner, target surface, runtime visibility and
targets, required and allowed-support artifacts, required guidance, eval plan,
and completion conditions. Show this proposed contract to the operator before
task creation; unresolved ownership or missing contract fields stop creation.

Bind every required, allowed-support, phase-approved, or dependency-generated
artifact through `artifact_bindings`. Path bindings must also appear in
`linked_artifacts`. Phase approvals at implementation identify the owning
`deliverable_id`, `artifact_id`, and `artifact_role`. Scripts and UI code cannot
satisfy a skill contract unless the contract separately requires those
deliverables.

When present, `capability_dependencies` records confirmed external project
workflow capabilities that the primary task may call. Each dependency must use
known tracker context or explicit operator input, not broad live project-folder
scans or project self-advertising.

When present, `dependency_steps` records ordered calls to selected dependency
skills. Each step must name the purpose, dependency project, selected skill,
expected inputs, expected outputs, allowed writes, protected paths, provenance
requirements, and, before implementation, a `dependency_write_plan`.

When present, `dependency_artifacts` records artifacts created through
dependency calls. These artifacts are owned by the primary task and keep
dependency provenance.

When present, `dependency_provenance` records completed dependency-step runs,
including helper skills used, inputs, generated artifacts, write plan used,
phase, timestamp, and artifact status.

Allowed project states:

```text
active, paused, archived
```

Allowed task statuses:

```text
todo, in-progress, blocked, done
```

Allowed task kinds:

```text
workflow-change, tracker-maintenance
```

Allowed Matt phases:

```text
intake, grilling, prd, issues, implement, code-review, done
```

## ECC Concepts

Document ECC concepts applied at project and task level. Use these names unless
there is a clear reason to add a more specific concept:

```text
workflow contract
input contract
output artifact
eval gate
human boundary
handoff
reviewer lane
parallel task context
project state preload
```

## Initiate A Task

Use when the user invokes `$initiate-task` or asks to create/start a new task.

Required input:

- `project:<slug>`
- `title:"..."`

Accept:

- `target:tracker` to create a tracker-maintenance task
- capability dependency intent in structured form or natural language, such as
  a primary project task that needs to use `real-life-workflows` skills

Process:

1. Load the whole project state first.
2. If the project is missing, hand off to `$setup-workflow-project` and stop.
3. Classify the requested outputs into one or more deliverable contracts. Use
   `canonical-skill`, `packaged-skill`, `standalone-skill`, `workflow-pack`,
   `ui-application`, `validator-query-helper`, `documentation-handoff`, or
   `tracker-only`. Distinguish primary deliverables from support deliverables.
4. Resolve create versus update, ownership, exact target surface, runtime
   visibility, runtime targets, required artifacts, allowed support, guidance,
   evals, and completion conditions. Ambiguous ownership stops here.
   Documentation-only, validator-only, and tracker-only requests still require
   a lifecycle contract and operator approval; zero writes is not a completed
   outcome when the requested artifact has not been produced.
   Report `ownership-unresolved` and no selected builder while destination is
   ambiguous. For script/helper pressure on a requested skill, preserve the
   `canonical-skill` intent and eventual `$build-workflow-skill` authority, but
   return `command-first`, `helper-only`, or `thin-wrapper` instead of approving
   the substitute. Do not reclassify a request to "call it a skill" as
   documentation merely because the proposed implementation is invalid.
   For create-UI, revamp-UI, workflow-product, or local-sidecar intent, inspect
   existing project tasks before creating anything. Continue the existing
   product task when it already owns the request; never duplicate the
   underlying workflow or skill task. Otherwise propose a target-project task
   with separate `ui-application` and callable `packaged-skill` or
   `workflow-pack` contracts. After implementation approval, route the complete
   product job to `$build-workflow-product`; that skill delegates only callable
   skill-bundle authoring to `$build-workflow-skill`.
5. Show the complete proposed contract and wait for explicit operator approval
   before writing task JSON. Skill authoring is not performed by this lifecycle
   skill; an implementation-ready skill contract later routes to
   `$build-workflow-skill`, while an implementation-ready workflow-product
   contract routes to `$build-workflow-product`.
6. Detect whether the request needs capability dependencies. Treat this as
   true only when the operator explicitly names another known project workflow
   capability, or when natural language strongly implies that a primary project
   task needs usable skills from another known project.
7. If capability dependency intent is present, query only known registered
   project trackers, the derived `--skill-catalog`, and existing
   project/task/artifact records. Do not
   scan arbitrary project folders for possible dependencies, and do not require
   projects to advertise reusable capabilities.
8. If a dependency is inferred, ask the operator to confirm it before creating
   the task.
9. For each confirmed dependency project, load all usable known skills or skill
   metadata plus enough relationship/context notes to understand how selected
   skills can be called. Do not audit or load the entire workflow agent unless a
   separate tracked task asks for that.
10. Build a final task draft before writing task JSON. Include primary project,
   title, summary, confirmed `capability_dependencies`, ordered
   `dependency_steps`, selected dependency skill map, allowed writes, protected
   paths, expected artifacts, and acceptance criteria.
11. The dependency skill map lists only selected dependency skills. Loaded but
   not selected skills are outside the approved call surface.
12. Wait for explicit operator approval of the final task draft before writing
   task JSON.
13. Generate the next id as `<project-slug>-NNN`.
14. Create the task at `status: "todo"` and `matt_phase: "intake"`.
15. Set `task_kind` to `tracker-maintenance` when `target:tracker` is provided;
   otherwise set it to `workflow-change`.
16. Set `explicit_next_action_required: true`.
17. Populate `ecc_concepts_applied` with at least `workflow contract`,
   `human boundary`, and `project state preload`.
18. Populate `phase_guard` with `selected_next_action: "none"`, empty
   `approved_artifacts`, and empty `process_exceptions`.
19. Persist `deliverable_migration.status: "native"`, contract version `1`, the
   operator approval evidence, `deliverable_contracts`, complete bindings for
   every declared required or allowed-support artifact, and empty
   `behavior_evidence`.
20. For `tracker-maintenance`, add tracker files expected to change to
   `linked_artifacts`, such as `project.json`, `tasks/index.json`, task JSON
   files, or `registry/agents-md.json`.
21. For capability-dependent tasks, populate `capability_dependencies` and
   `dependency_steps` from the approved final task draft. Do not create a helper
   task in the dependency project by default.
22. For capability-dependent tasks, keep dependency project trackers read-only
   by default. Store or index dependency-created artifacts under the primary
   task unless a later explicitly approved tracker task allows dependency
   tracker mutation.
23. Populate `context_snapshot.must_load` with root `AGENTS.md`,
   `registry/agents-md.json`, project `AGENTS.md`, project JSON, index JSON, and
   all non-done task JSON files known at creation time.
24. If `projects/<project-slug>/artifacts/testing-sessions/index.json` exists,
    add that path to `context_snapshot.must_load` as a lightweight project
    preload pointer. Do not copy full testing-session events into task JSON.
25. Update `tasks/index.json`.
26. Report the created task and stop.

Do not enter grilling, PRD, issues, implementation, or review in the same turn
unless the user explicitly asks to continue that task after creation.

Creating a `tracker-maintenance` task is the allowed bootstrap tracker write.
After that task exists, further tracker edits must happen through
`$continue-task` on that task.

## Capability Dependency Draft Contract

Use this contract when a task needs selected skills from another known project.

Each `capability_dependencies` entry should include:

```json
{
  "dependency_id": "real-life-workflows-workflow-packets",
  "dependency_project": "real-life-workflows",
  "purpose": "Discover and prepare workflow packet candidates for the primary task.",
  "source": "known-tracker-context",
  "status": "confirmed",
  "selected_skills": [
    {
      "skill": "real-world-workflow-finder",
      "purpose": "Find relevant workflow candidates.",
      "call_boundary": "Use only for the primary task's approved dependency step.",
      "expected_artifacts": ["workflow packet candidates"],
      "allowed_writes": ["primary task dependency artifact area"],
      "protected_paths": ["dependency project AGENTS.md", "dependency project tracker", "dependency skill definitions"]
    }
  ]
}
```

Allowed `source` values are:

- `operator-explicit`
- `confirmed-natural-language`
- `known-tracker-context`

Do not use `live-folder-scan` as a dependency source. If the dependency cannot
be grounded in known tracker context or explicit operator input, stop and ask.

Each `dependency_steps` entry should include:

```json
{
  "step_id": "dep-step-001",
  "capability_dependency_id": "real-life-workflows-workflow-packets",
  "dependency_project": "real-life-workflows",
  "selected_skill": "real-world-workflow-finder",
  "purpose": "Create candidate workflow packet material for the primary task.",
  "supported_deliverable_id": "workflow-packet",
  "supported_artifact_id": "candidate-packet-files",
  "artifact_role": "support",
  "required_outcome": "Validated candidate workflow packet files exist inside the approved primary-task write zone.",
  "completion_condition_id": "candidate-packets-ready",
  "expected_inputs": ["primary task topic and constraints"],
  "expected_outputs": ["candidate workflow packet files"],
  "allowed_writes": ["primary task dependency artifact area"],
  "protected_paths": ["dependency project tracker", "dependency skill definitions"],
  "provenance_requirements": ["primary task id", "dependency project", "selected skill", "generated artifacts"]
}
```

Selected dependency skills may call documented helper skills when those helpers
are part of the selected skill's normal workflow. Record helper usage in
`dependency_provenance` after use.

## Dependency Artifacts

Dependency calls during intake or grilling may create real artifacts when they
are needed to understand or prepare the task. Label them as intake or grilling
dependency artifacts, index them under the primary task, and record:

- primary project
- primary task id
- dependency step id
- dependency project
- source workflow or skill
- phase
- purpose
- generated files
- protected boundary metadata

When the post-grilling PRD names an intake or grilling dependency artifact, the
artifact becomes an official task artifact. Preserve the original dependency
provenance and add promotion metadata. If the PRD does not name the artifact,
keep it as linked evidence or context, not as a final deliverable.

## Dependency Write Plan

Before implementation starts, every dependency step must have a
`dependency_write_plan`. The plan must name:

- expected output paths or patterns
- allowed write zones
- protected paths
- artifact promotion rules
- provenance requirements
- stop conditions
- approval timestamp

Implementation must preflight the write plan before running dependency steps.
If a selected dependency skill or documented helper tries to write outside the
approved boundary, stop and ask the operator. Do not redirect or mutate the
dependency project tracker unless a later explicitly approved tracker task
allows it.

## Continue A Task

Use when the user invokes `$continue-task`, asks to continue a task, or asks to
resume/revert back to a task.

Process:

1. Load the whole project state first.
2. If no task id is provided, list selectable tasks using
   `scripts/query-workflow-state.mjs` when available and ask the user to choose.
3. Load root `AGENTS.md`, the registry, project `AGENTS.md`, the selected task's
   `context_snapshot`, and linked artifacts.
4. Load the project testing-session index summary when
   `projects/<project-slug>/artifacts/testing-sessions/index.json` exists.
   Keep full `events.jsonl` streams unloaded unless exact evidence is needed.
5. Report current `status`, `matt_phase`, ECC concepts, open dependencies,
   related tasks, capability dependencies, dependency steps, testing-session
   summaries, and conflicts.
6. Report `phase_guard.selected_next_action`, approved artifacts, and process
   exceptions.
7. If execution reveals a new capability dependency, propose a new
   `dependency_step` instead of calling the dependency ad hoc. Load the
   dependency project's usable known skills or skill metadata, draft the step
   with purpose, selected skill, expected inputs and outputs, allowed writes,
   protected paths, provenance requirements, and required
   `dependency_write_plan`, then ask for explicit operator approval before use.
8. Ask for the next explicit instruction if the user did not provide one.

Resume/revert means resume snapshot only:

- Load all project and task context.
- Continue from the saved Matt phase.
- Do not run `git revert`.
- Do not mark artifacts superseded unless the user explicitly asks.

If the task changes project agent behavior, target
`projects/<project-slug>/AGENTS.md`, add it to `linked_artifacts`, and keep it
in `context_snapshot.must_load`.

## Phase Guard

Artifact creation is phase-gated.

- If the selected task is still `intake`, do not create scripts, HTML, skills,
  workflow artifacts, tests, or implementation files.
- Before creating any script, HTML, skill, workflow artifact, test, or other
  implementation artifact, the selected task must include a matching
  `phase_guard.approved_artifacts` entry with the artifact `path`, phase
  `implement`, `deliverable_id`, `artifact_id`, `artifact_role`,
  `approval_note`, and `approved_at`. It must match a declared
  `artifact_bindings` entry.
- A task with `deliverable_migration.status: "pending"` is frozen at
  `deliverable_migration.frozen_phase`; do not advance it until the operator
  approves complete version-1 contracts and the migration becomes `approved`.
- Tracker bootstrap writes are allowed only for creating the
  `tracker-maintenance` task itself. Further tracker edits must continue that
  tracker-maintenance task.
- If validation reports an unapproved artifact, stop and return to the current
  Matt phase. Do not adopt the artifact as design unless the user explicitly
  approves the phase action.

## Matt Phase Handling

Matt phases are allowed only inside a selected task.

- `grilling`: use Matt's `grill-with-docs` and ask one blocking question at a
  time.
- `prd`: use Matt's `to-prd` and write/link the PRD under project artifacts.
- `issues`: use Matt's `to-issues` and write/link issue artifacts under project
  artifacts.
- `implement`: use Matt's `implement`, which drives `tdd`.
- `code-review`: use Matt's `code-review` against standards and spec.

Never create repo-local phase substitute skills such as `write-workflow-prd`,
`split-workflow-issues`, or `advance-task-phase`.

## Output Contract

Every invocation must report:

```text
PROJECT
- slug
- project_state
- root AGENTS.md loaded
- registry loaded
- project AGENTS.md loaded
- tracker files read
- testing-session index summary checked

PROJECT TASK STATE
- active / blocked / in-progress / recently completed tasks reviewed
- testing-session summaries reviewed when present
- conflicts or none found

TASK
- id
- title
- status
- task_kind
- matt_phase
- ECC concepts applied
- context snapshot loaded
- phase guard loaded

ACTION
- initiated / continued / waiting for task selection / blocked
- explicit next instruction required
```

## Developer Verification

Run before committing workflow-state changes:

```bash
node scripts/validate-workflow-state.mjs
```

Use query helper when selecting or inspecting tasks:

```bash
node scripts/query-workflow-state.mjs --project health --list-tasks
node scripts/query-workflow-state.mjs --project health --task health-001
```
