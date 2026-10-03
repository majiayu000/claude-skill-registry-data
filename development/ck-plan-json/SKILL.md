---
name: ck:plan-json
description: Create a machine-readable phased JSON plan bundle from a spec or feature description. Produces a compact master manifest plus per-phase step files for resumable ck:cook execution.
user-invocable: true
---

# ck:plan-json — Phased JSON Planning

Every mode always creates `plans/{slug}/plan.json` and one or more phase JSON files. The master stays compact so an AI executor loads step detail only for the active phase.

No legacy or single-file format compatibility is supported.

---

### Step 0 — Load Input

Resolve the primary requirement input in this order:

1. `--spec <path>` — preferred: load the supplied `spec.md`.
2. If no spec is supplied, use the inline feature description or requirement text.
3. If neither exists, ask for a description or spec path.

Also accept:

- `--project {slug}` — project ID; default is the current directory name.
- `--mode {fast|hard}` — override automatic scope detection.
- `--output <path>` — master entry point; default is `plans/{slug}/plan.json`. Phase files are siblings beside this master.

---

### Step 1 — Analyze Scope and Phases

Report:

```text
Scope:
  Phases: {N}
  Files: {N total, N new, N modify}
  Complexity: {Fast | Hard}
```

- **Fast** — one small component and at most three affected files. Fast creates exactly one phase JSON file.
- **Hard** — two or more phases, at least four files, multiple components, or external integrations.

If Hard has no spec, suggest `/ck:brainstorm` before continuing.

Decompose work into ordered, dependency-aware phases. Use deterministic kebab-case names and `phase-{phase_id:02d}-{name}.json` filenames. Maximum 15 steps per phase; add another phase when more steps are needed.

---

### Step 2 — Generate Phase Files First

Phase files contain and own detailed steps. Write every complete phase file first, before the master exists or is updated.

Each phase file uses this structure:

```json
{
  "plan_id": "{slug}",
  "phase_id": 1,
  "name": "setup-project",
  "goal": "Initialize the project",
  "status": "pending",
  "current_step": 1,
  "design_constraints": [
    "Cook confirms unit-test and quality-gate choices before each phase"
  ],
  "quality_profile": {
    "repository_conventions": {},
    "boundaries": {},
    "applicable_rules": [],
    "allowed_exceptions": []
  },
  "quality": { "status": "not_evaluated", "report": "", "receipt": "", "remediation_cycles": 0 },
  "testing": { "status": "not_started", "report": "" },
  "steps": [
    {
      "step_id": 1,
      "description": "Create the project structure",
      "status": "pending",
      "input_files": [],
      "output_files": ["src/README.md"],
      "ai_generated_code": "",
      "debug_logs": [],
      "success_criteria": ["The expected file exists"]
    }
  ]
}
```

Rules:

- Step IDs are unique, sequential, and one-indexed within the phase.
- `input_files` must already exist or be produced by earlier steps or dependency phases.
- `output_files` lists every file created or modified.
- `success_criteria` contains at least one automation-verifiable condition.
- `ai_generated_code` starts as an empty string and `debug_logs` starts as an empty array.
- `design_constraints`, `quality_profile`, `quality`, and `testing` are optional; leave them at their `pending`-equivalent defaults (empty arrays/objects, `not_evaluated`, `not_started`) at plan-creation time — see `rules/plan-design.md` § Quality and Testing State for what owns each field and when it changes.

---

### Step 3 — Generate the Master Last

Write the master last, after all referenced phase files exist. `plan.json` is the orchestration manifest and contains ordered phase entries; the master must not contain inline steps.

```json
{
  "plan_id": "{slug}",
  "goal": "{one-line deliverable}",
  "status": "pending",
  "current_phase": 1,
  "global_context": {
    "framework": "{detected framework or empty}",
    "architecture": "{detected pattern or empty}",
    "target_folder": "{primary output directory}",
    "constraints": []
  },
  "phases": [
    {
      "phase_id": 1,
      "name": "setup-project",
      "description": "Initialize project structure",
      "file": "phase-01-setup-project.json",
      "status": "pending",
      "depends_on": [],
      "quality_status": "not_evaluated",
      "testing_status": "not_started"
    }
  ]
}
```

All plan, phase, and step statuses start as `pending`. `current_phase` starts at `1`, and every phase `current_step` starts at `1`.

Dependencies may reference unique earlier phase IDs only. A step object appears in exactly one phase file and is never duplicated in the master.

`quality_status`/`testing_status` are the master's compact mirror of each phase's `quality.status`/`testing.status` — never the full profile or report. Both start at `not_evaluated`/`not_started` and must match the phase file's values whenever both declare one.

---

### Step 4 — Mandatory Bundle Validation

Mandatory validation must use the master path so the bundle validator checks the manifest and every referenced sibling:

```text
python {ck-plan-json-skill-root}/hooks/plan_validator.py plans/{slug}/plan.json
```

Resolve `{ck-plan-json-skill-root}` from the `SKILL.md` currently loaded so the command works in pack-root, Claude, Codex, and Antigravity installations.

If validation fails, fix the relevant phase or master file and rerun validation. Do not report success until the validator exits with code `0`.

On success, report exactly these bundle details:

```text
[ck:plan-json] ✓ phased plan bundle written
Master path: plans/{slug}/plan.json
Phase paths:
  - plans/{slug}/phase-01-{name}.json
Mode: {Fast | Hard}
Phase count: {N}
Total step count: {N}

Next: /ck:cook --json plans/{slug}/plan.json
```

Use `references/plan-schema.json`, its referenced canonical phase file, and `rules/plan-design.md` as the detailed contract.
