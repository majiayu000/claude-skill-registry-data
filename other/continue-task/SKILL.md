---
name: continue-task
description: Continue an existing JSON-tracked workflow task in ace-workflows. Use when the user asks to resume a task, continue a task, select an existing task, load a task snapshot, inspect current Matt phase, proceed with phase work after full project-state loading, or add an approved dependency_step to a primary task.
---

# Continue Task

Use this skill to continue an existing task. It is a discoverable alias for the
continue behavior defined in `.agents/skills/initiate-task/SKILL.md`.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: continue work through `$continue-task` and the selected
task's saved phase. Do not make `npx`, `npm`, Python, or raw helper commands the
operator-facing way to call a workflow skill. Helper commands are internal
support or verification only.

## Required Reading

Before acting:

1. Read root `AGENTS.md`.
2. Read `references/matt-pocock-skills.md`.
3. Read `.agents/skills/initiate-task/SKILL.md` completely.
4. Read `registry/agents-md.json`.

## Continue Contract

Follow the `Continue A Task` section of `.agents/skills/initiate-task/SKILL.md`.

Load, load, load, load, load before doing anything with the task:

1. Read root `AGENTS.md`.
2. Read `registry/agents-md.json`.
3. Read `projects/<project-slug>/AGENTS.md`.
4. Read `projects/<project-slug>/project.json`.
5. Read `projects/<project-slug>/tasks/index.json`.
6. Query the derived skill catalog and project task list through the read-only
   state helper when available.
7. Query the registered project-instruction state through the same helper.
8. Query testing-session summaries through the same helper. Load only index
   summaries and pointers unless exact testing-session evidence is needed.
9. Read every task JSON listed in the index whose status is not `done`.
10. Read the selected task JSON if a task id is provided.
11. Read the selected task's linked artifacts and `context_snapshot.must_load`.
12. Read and report `phase_guard.selected_next_action`, approved artifacts, and
    process exceptions.
13. Query the selected task's readiness projection and report migration status,
    contracts, per-deliverable readiness, and blocker codes.
14. Report conflicts, state gaps, and relevant testing-session summaries before
    taking any task action.

If no task id is provided, list selectable tasks and ask the user to choose.

If `deliverable_migration.status` is `pending`, preserve the recorded
`frozen_phase` and stop for explicit contract classification approval. Do not
infer ownership or silently advance the phase. Only the immutable legacy task
registry remains historical-compatible; a new task cannot self-grandfather by
setting `status: "done"`.

Report the current Matt phase and stop unless the user explicitly requested the
next phase action.

If the selected task is still `intake`, do not create scripts, HTML, skills,
workflow artifacts, tests, or implementation files. Before creating any such
artifact, the selected task must include a matching
`phase_guard.approved_artifacts` entry for the artifact path, phase
`implement`, `deliverable_id`, `artifact_id`, and `artifact_role`.

For a ready skill contract, delegate authoring and behavioral evaluation to
`$build-workflow-skill`. This lifecycle skill retains tracker and phase
ownership; the builder must not create tasks or mutate task JSON. Before
delegation, verify every approved implementation path is bound to the same
deliverable, artifact id, and artifact role.

For a selected task whose approved primary contracts include a
`ui-application` plus a callable `packaged-skill` or `workflow-pack`, delegate
the complete create or revamp job to `$build-workflow-product`. Keep tracker
and phase ownership here. The product builder may invoke `$build-workflow-skill`
for the callable bundle, but neither builder may duplicate the selected task or
let UI files satisfy the skill contract.

## Capability Dependency Continuation

If a continued task needs a new capability dependency mid-execution:

1. Load the selected primary task and its existing `capability_dependencies`,
   `dependency_steps`, `dependency_artifacts`, and `dependency_provenance`.
2. Load the derived `--skill-catalog`, then the referenced dependency project's
   known tracked relationship context. Do not scan arbitrary folders, use a
   remembered inventory, or treat loaded but unselected skills as approved.
3. Draft the new `dependency_step` with purpose, dependency project, selected
   skill, expected inputs, expected outputs, allowed writes, protected paths,
   provenance requirements, supported deliverable id, supported artifact id,
   artifact role, required outcome, completion condition id, and documented
   helper skills if any.
4. Draft or reference the required `dependency_write_plan`, including expected
   output paths, allowed write zones, protected paths, promotion rules,
   provenance requirements, stop conditions, and approval timestamp.
5. Ask for explicit operator approval before calling the dependency.
6. Record approved dependency steps in the primary task only. Do not mutate the
   dependency project tracker unless a separate approved tracker-maintenance
   task allows it.
7. After dependency use, record `dependency_provenance` and
   `dependency_artifacts` with the primary project, primary task id,
   dependency step id, dependency project, selected skill, helper skills used,
   inputs, generated artifacts, write plan used, phase, timestamp, and artifact
   status.
8. Stop and ask for approval if a selected dependency skill or helper would
   write outside the approved boundary.
