---
name: uipath-tasks
description: >
  Generates UiPath Tasks workflows — Form Tasks (CreateFormTask,
  WaitForFormTaskAndResume, GetFormTasks) with form.io schemas and FormData
  bindings, External Tasks (CreateExternalTask, WaitForExternalTaskAndResume)
  for system-in-the-loop patterns, and Task Management (CompleteTask,
  AssignTasks) for programmatic task operations. Self-contained skill with
  generators, lint rules, and scaffold hooks loaded via uipath-core's plugin
  system (plugin_loader.py). Use when the user mentions Tasks, form
  tasks, external tasks, human-in-the-loop approval, task assignment,
  task completion, recovery workflows, or any Persistence.Activities usage.
---

# UiPath Tasks Skill

Generate Tasks workflows for human-in-the-loop, system-in-the-loop, and task management patterns in UiPath.

> **Plugin architecture:** This skill's `extensions/` directory is auto-discovered by uipath-core's `plugin_loader.py`. Generators, lint rules, scaffold hooks, namespaces, and known activities are registered at import time — no manual wiring needed. Core's `generate_workflow.py`, `validate_xaml`, and `scaffold_project.py` query the plugin registries at runtime.

## Plugin API contract (v2)

This skill is the canonical example for out-of-tree plugin authors. The contract:

- **`REQUIRED_API_VERSION = 2`** must be declared at the top of `extensions/__init__.py`. Plugins on v1 (or with no declaration) fail to load with a clear `API version mismatch` error and any partial registrations are rolled back.
- **Registration entry points** added in v2: `register_version_profile(package, profile_version, profile_dict)` and `register_band_profile_mapping(band, package, profile_version)` — used by lint 122 (version-band drift). Call `register_band_profile_mapping` once per `(band, package)` pair. Registering after the lint module is already imported automatically invalidates the lint caches, so the new entries take effect on the next lint pass without any reload.
- **Atomic commit:** every `register_*` call made during a plugin's load (including from submodules imported from `__init__.py`) is captured in the registry snapshot. If `__init__.py` raises before completing, all registrations from that plugin are reverted. The registry is never observed in a partially-loaded state by other plugins or by core.
- **Out of scope for rollback:** non-registry side effects (file writes, env vars, threads spawned at import time, monkey-patches). Confine those to lazy paths invoked after a successful load.
- **Test that load succeeded:** `assert plugin_loader.get_load_failures() == []` after `load_plugins()`. A plugin that raised during load surfaces in that list with its filename and exception.

Worked example: see `uipath-tasks/extensions/__init__.py:34` (the `REQUIRED_API_VERSION = 2` declaration) and `:310-312` (the Persistence/1.4 profile + band-25/26 mapping calls).

## Extensions (Plugin System)

```
uipath-tasks/
├── SKILL.md
├── references/
│   ├── tasks.md       ← Form Tasks + form.io + Action Types Comparison
│   ├── external-tasks.md      ← External Tasks (system-in-the-loop)
│   └── task-management.md     ← GetFormTasks, CompleteTask, AssignTasks
└── extensions/
    ├── __init__.py             ← Registers all AC components with plugin_loader
    ├── generators.py           ← 7 generators (form, external, task management)
    ├── lint_rules.py           ← AC-10, AC-11, AC-12, AC-26
    ├── scaffold_hooks.py       ← enable_persistence_support
    └── battle_test_grading.py  ← 8 battle test scenario graders
```

**What gets registered:**
- 7 generators: `create_form_task`, `wait_for_form_task`, `create_external_task`, `wait_for_external_task`, `get_form_tasks`, `complete_task`, `assign_tasks`
- 4 lint rules: AC-10 (Form Create/Wait mismatch), AC-11 (FormData key mismatch), AC-12 (External Create/Wait mismatch), AC-26 (persistence in sub-workflow)
- 1 scaffold hook: auto-enables `supportsPersistence` when Persistence.Activities is in deps
- 3 namespaces: `upaf` (FormTask), `upae` (ExternalTask), `upat` (Tasks)
- 7 known activities: `CreateFormTask`, `WaitForFormTaskAndResume`, `CreateExternalTask`, `WaitForExternalTaskAndResume`, `GetFormTasks`, `CompleteTask`, `AssignTasks`

## When To Read Which Reference

| Task | Read |
|---|---|
| Create a form task workflow | `references/tasks.md` → Create Form Task + FormData Bindings |
| Design a form.io form schema | `references/tasks.md` → Form.io Component Reference |
| Wait for human approval / resume | `references/tasks.md` → Wait for Form Task and Resume |
| **Any PDD with "for each X" / "multiple X" / "batch of X" / N rows** (default for N-item approvals, not advanced) | `references/tasks.md` → Shadow Task Pattern |
| Compare action types (Form vs External) | `references/tasks.md` → Action Types Comparison |
| Create an external task (system-in-the-loop) | `references/external-tasks.md` → Create External Task |
| Wait for external system resolution | `references/external-tasks.md` → Wait for External Task and Resume |
| Retrieve existing tasks (recovery workflow) | `references/task-management.md` → Get Form Tasks |
| Complete a task programmatically | `references/task-management.md` → Complete Task |
| Assign a task to a user/group | `references/task-management.md` → Assign Tasks |
| Escalation / reassignment patterns | `references/task-management.md` → Escalation Pattern |
| Task lifecycle states | `references/task-management.md` → Task Lifecycle States |
| Persistence constraints | `references/tasks.md` → Prerequisites (Main.xaml constraint) |
| Lint issues on AC workflows | `references/tasks.md` → Validation & Lint Rules + `external-tasks.md` → Validation |
| Scaffold a project with persistence | Scaffold hook in `extensions/scaffold_hooks.py` — auto-runs via core's `scaffold_project.py` |
| Validate AC workflow XAML | Lint rules in `extensions/lint_rules.py` — auto-run via core's `validate_xaml --lint` |
| Resolve NuGet versions | Use uipath-core's `resolve_nuget.py` for `UiPath.Persistence.Activities` + `UiPath.FormActivityLibrary` |

## Ground Rules

- **AC-1: Always use generators.** Never write Tasks XAML by hand. Use generators via JSON specs or Python API (auto-loaded from `extensions/generators.py`).
- **AC-2: Persistence activities MUST stay in Main.xaml.** `WaitForFormTaskAndResume`, `WaitForExternalTaskAndResume`, and all Wait*AndResume activities are persistence points — they serialize workflow state to Orchestrator. They ONLY work in the entry-point file. AC-26 enforces this.
- **AC-3: Both NuGet packages are required for Form Tasks.** `UiPath.Persistence.Activities` (runtime) AND `UiPath.FormActivityLibrary` (form designer UI). External Tasks and Task Management only need `UiPath.Persistence.Activities`.
- **AC-4: `supportsPersistence: true`** must be in project.json `runtimeOptions` when using Wait*AndResume activities. Scaffold sets this automatically.
- **AC-5: FormData keys must match form.io component keys.** (Form Tasks only.) AC-11 validates key presence.
- **AC-6: Always include a submit button** as the last form.io component. (Form Tasks only.)
- **AC-7: Wrap Create*Task in RetryScope.** Orchestrator API calls can transiently fail.
- **AC-8: External tasks have NO form.** Don't use FormLayout/FormData on CreateExternalTask — use TaskData dict.
- **AC-9: Task Management activities are NOT persistence points.** GetFormTasks, CompleteTask, AssignTasks can be used in sub-workflows.
- **AC-Shadow: Shadow Task Pattern is the default shape for N-item approvals.** When the PDD / workflow processes N items from a collection (DataTable rows, list, etc.) and each needs a human task, emit **one** `ui:ForEachRow` / `ui:ForEach` that only calls `CreateFormTask` and appends the returned `FormTaskData` to a `List(Of FormTaskData)`, followed by a **second** `ui:ForEach` (at the root-Sequence level) that runs `WaitForFormTaskAndResume` + decision handling per task. **The `List(FormTaskData)` variable MUST be initialized** — set `Default="[New System.Collections.Generic.List(Of UiPath.Persistence.Activities.FormTask.FormTaskData)()]"` on the variable declaration (or pass `"default": "[...]"` in the JSON spec). A null List throws `Value cannot be null. (Parameter 'TargetObject')` on the first `InvokeMethod.Add`. Never emit inline `Create → Wait` per item, and never unroll the loop into hardcoded `If Rows.Count >= N` / `Rows(0..N-1)` blocks. The inline form ties up the robot for the sum of all wait times instead of the max; the unrolled form additionally bypasses AC-27. See `references/form-tasks.md` → Shadow Task Pattern (default for N-item batches). Loop-nested case enforced by AC-27; unrolled case enforced by AC-34.

## Capabilities

1. **CreateFormTask** — Form task with form.io schema, FormData bindings (In/Out/InOut), storage bucket, task catalog, priority levels
2. **WaitForFormTaskAndResume** — Long-running persistence, task action capture, updated FormTaskData output
3. **Form.io schema design** — textfield, textarea, number, select, checkbox, datagrid (DataTable binding), htmlelement (Mustache templates), columns, button
4. **FormData direction bindings** — In (read-only), Out (user-entered), InOut (editable pre-populated, DataTable ↔ datagrid)
5. **Shadow task pattern** — Non-blocking multi-task orchestration
6. **CreateExternalTask** — System-in-the-loop task for external systems (JIRA, Salesforce, ServiceNow)
7. **WaitForExternalTaskAndResume** — Suspend until external system completes task via API
8. **GetFormTasks** — Retrieve existing tasks from Orchestrator (recovery workflows, cross-process)
9. **CompleteTask** — Programmatic task completion (escalation, timeout, batch operations)
10. **AssignTasks** — Assign tasks to user or group (SingleUser, AllUsersInGroup)
11. **Validation** — AC-10, AC-11, AC-12, AC-26

## Reference Files

| File | Coverage |
|---|---|
| `references/tasks.md` | Form Tasks — prerequisites, CreateFormTask, FormData, form.io, WaitForFormTask, patterns, lint, Config keys |
| `references/external-tasks.md` | External Tasks — CreateExternalTask, WaitForExternalTask, TaskData dict, external system completion |
| `references/task-management.md` | Task Management — GetFormTasks, CompleteTask, AssignTasks, recovery pattern, escalation pattern, lifecycle |

## Quick Generator Reference

| Generator | Activity | Prefix | Key Args |
|---|---|---|---|
| `gen_create_form_task()` | CreateFormTask | `upaf:` | `task_title_expr`, `task_output_variable`, `form_layout_json`, `form_data=` |
| `gen_wait_for_form_task()` | WaitForFormTaskAndResume | `upaf:` | `task_input_variable` |
| `gen_create_external_task()` | CreateExternalTask | `upae:` | `task_title_expr`, `task_output_variable`, `task_data=` |
| `gen_wait_for_external_task()` | WaitForExternalTaskAndResume | `upae:` | `task_input_variable` |
| `gen_get_form_tasks()` | GetFormTasks | `upaf:` | `output_variable`, `filter_expr=` |
| `gen_complete_task()` | CompleteTask | `upat:` | `task_id_expr`, `action_expr=` |
| `gen_assign_tasks()` | AssignTasks | `upat:` | `task_id_expr`, `user_name_or_email=` |

JSON spec `"gen"` values: `create_form_task`, `wait_for_form_task`, `create_external_task`, `wait_for_external_task`, `get_form_tasks`, `complete_task`, `assign_tasks`

## Common Hallucinations

| Wrong | Right | Impact |
|---|---|---|
| `TaskObject=` | `TaskOutput=` (Create) / `TaskInput=` (Wait) | Studio crash — property doesn't exist |
| `EnableDynamicForms="False"` | `EnableDynamicForms="True"` | Form designer button does nothing |
| Persistence activity in sub-workflow | Move to Main.xaml | Runtime error — bookmark context unavailable |
| Missing `UiPath.FormActivityLibrary` | Add explicitly alongside Persistence.Activities | "Install FormActivityLibrary" error in Studio |
| `"supportsPersistence": false` | Set to `true` in project.json runtimeOptions | WaitFor*AndResume fails at runtime |
| `FormLayout=` on CreateExternalTask | Use `TaskData` dict instead | Property doesn't exist on external tasks |
| `FormData` on CreateExternalTask | Use `TaskData` dict instead | Property doesn't exist on external tasks |
