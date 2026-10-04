---
name: plan-to-tasks
description: Transform a plan_creation plan_v{N}.md into a structured tasks.yaml + per-WP workpackages/*.yaml using parallel Sonnet sub-agents. Use after plan-creation finishes when you need execution-friendly task structure.
when_to_use: When a plan_creation plan exists and you need an executable tasks.yaml + per-workpackage YAML files for execution-ready task tracking; supports parent/child plan linkage.
user-invocable: true
argument-hint: "<path-to-plan_v{N}.md>"
skills:
  - subagent-prompting
allowed-tools:
  - AskUserQuestion
  - Edit
  - Glob
  - Read
  - Skill
  - Task
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Plan to Tasks

Transform the verbose plan document emitted by `plan-creation` into an execution-friendly task decomposition: a `tasks.yaml` workpackage index plus one YAML file per workpackage under `plans/<slug>/workpackages/`. Supports parent/child plan linkage.

---

## When to Use This Skill

| Trigger | Action |
|---------|--------|
| `plan-creation` just emitted `plan_v{N}.md` and execution-friendly task structure is needed | Run `/plan-to-tasks plans/<slug>/plan_v{N}.md` |
| Existing plan needs structured task decomposition for downstream task-runner tooling | Run `/plan-to-tasks <path>` |
| Child plan needs parent linkage (bidirectional) | Run `/plan-to-tasks <child-plan-path>` and answer "Yes (child plan)" to AskUserQuestion |

**DO NOT use for**: plans that don't follow `plan-creation`'s YAML-block format; mechanical YAML reformatting (this skill expands per-WP detail using LLM judgment, not just file conversion).

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping. Skipping items violates SC1-SC3 (Skill Compliance Rules in Rules.md).**

This skill orchestrates parallel sub-agents to expand per-WP YAML files. You are the orchestrator, NOT the executor. Follow every item in order. Do NOT return to the user until all applicable items are checked.

- [ ] **Stage 1 — Input Resolution**: Argument parsed; plan path validated to exist
- [ ] **Stage 2 — Parent/Child**: AskUserQuestion answered (parent/child + parent path if child + slug confirmation)
- [ ] **Stage 3 — Read**: Plan + all synthesis artifacts in plan directory loaded
- [ ] **Stage 4 — Extract**: WP list extracted from plan YAML blocks (id, name, description, dependencies)
- [ ] **Stage 5 — Expand**: `general-purpose` sub-agents (Sonnet by default) spawned in parallel batches of ≤5 — you MUST NOT write per-WP YAMLs yourself; sub-agents do the work
- [ ] **Stage 5 — Expand**: Sub-agents NOT spawned with `run_in_background: true` (SA5)
- [ ] **Stage 6 — Index**: `tasks.yaml` written; `parent_plan` field added if child
- [ ] **Stage 7 — Parent Update** (if child): parent `tasks.yaml` appended in-place with reference to this child
- [ ] **Stage 8 — Summary**: report written to stdout (N WPs, parent linkage status, next-command hint)
- [ ] **Source plan_v{N}.md NEVER modified** (read-only on the source — AC7)
- [ ] **Safety gate**: if `workpackages/` already exists in target dir, AskUserQuestion before overwriting (AC8)
- [ ] **Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Transform algorithm** | `references/transform.md` | **REQUIRED** | Load at Stage 4 before sub-agent spawn |
| **AskUserQuestion prompts** | `references/askuserquestion-prompts.md` | **REQUIRED** | Load at Stage 2 |
| **Prompting skill** | `subagent-prompting` | **REQUIRED** | Load before Stage 5 sub-agent spawn |

---

## Usage

```
/plan-to-tasks <path-to-plan_v{N}.md>
```

Example:
```
/plan-to-tasks plans/auth-rewrite/plan_v1.md
```

---

## Pipeline

```fsharp
// plan-to-tasks pipeline
Stage1_InputResolution(args)
|> Stage2_ParentChildQuestion(askuserquestion)            // AskUserQuestion
|> Stage3_ReadPlanAndSynthesis(plan_path, plan_dir)
|> Stage4_ExtractWorkpackages(plan_content)
|> Stage5_ExpandPerWP(workpackages)                       // Parallel Sonnet sub-agents, batches ≤5
|> Stage6_GenerateTasksYaml(workpackages, parent_info)
|> Stage7_UpdateParentTasksYaml(parent_path)              // If child
|> Stage8_EmitSummary(counts)
```

**Per-WP sub-agent prompt** lives in `references/transform.md` (4-part GOAL/CONSTRAINTS/CONTEXT/OUTPUT). Each sub-agent reads the plan + synthesis docs and writes one `workpackages/WP-{id}.yaml` directly.

---

## Output Files

```
plans/<slug>/
├── plan_v{N}.md          # untouched — the source doc
├── tasks.yaml            # NEW — WP index (parent_plan field if child)
└── workpackages/         # NEW
    ├── WP-{id-1}.yaml
    ├── WP-{id-2}.yaml
    └── ...
```

If child: parent's `tasks.yaml` is appended in-place with a reference entry pointing to this child.

---

## Schema Reference

`references/transform.md` documents the exact field set for both `tasks.yaml` and `WP-{id}.yaml` plus the single Bulwark divergence (`parent_plan` field for bidirectional linkage). The schema is CLEAR-compatible — match field names exactly.

**Developer note** (not user-facing): Bulwark contributors validating the schema during skill development can cross-reference the CLEAR framework at `clear-framework/plans/clear-v1-completion/tasks.yaml` (parent example), `clear-framework/plans/knowledge-system-overhaul/tasks.yaml` (child example), and `clear-framework/plans/knowledge-system-overhaul/workpackages/WP-K0.1.yaml` (per-WP shape). These paths are not shipped expectations — `references/transform.md` is the single source of truth at runtime.

---

## Diagnostic Output

Write to `$CLAUDE_PROJECT_DIR/logs/diagnostics/plan-to-tasks-{ISO-8601-timestamp}.yaml` after every invocation.

```yaml
diagnostic:
  skill: plan-to-tasks
  timestamp: "{ISO-8601}"
  invocation:
    plan_path: "{input}"
    plan_slug: "{derived or user-provided}"
    parent_child_mode: standalone | child
    parent_plan_path: "{path or null}"
  execution:
    workpackages_extracted: N
    sub_agent_batches: N
    parent_tasks_yaml_updated: true | false | n/a
  output:
    tasks_yaml_path: "plans/<slug>/tasks.yaml"
    workpackages_dir: "plans/<slug>/workpackages/"
    workpackages_written: N
```

---

## Archetype Note

This skill follows the **pipeline** archetype from `create-skill` (multi-stage with parallel Sonnet sub-agents). The P10.5 brief originally referenced a "cli-orchestrator" archetype as a future addition; until that lands, the pipeline archetype is the closest fit and is used here.

---

## Related Skills

- `plan-creation` — produces the source `plan_v{N}.md` consumed by this skill
- `subagent-prompting` — 4-part prompt template used at Stage 5
