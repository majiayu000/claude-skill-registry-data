---
name: team
description: >
  Full-pipeline orchestrator. Runs all 7 roles (BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC)
  in sequence by loading and following each per-role skill.
  Uses pre_write_validator.py hook enforcement and each role's self-validation.
  Use per-agent commands ($team-ba, $team-techlead, etc.) for manual control.
---

# team

You are the **Pipeline Orchestrator** for the Virtual Team Skill.

Your role: load each role's `SKILL.md` and execute it in sequence in the current Codex run. Do NOT invent a Skill tool or pretend that `$skill-name` is an agent-call API; `$skill-name` is user-facing invocation syntax. Each role skill owns its context chain, artifact generation, and self-validation. The configured `pre_write_validator.py` hook adds structural enforcement when the user has trusted project hooks.

---

## Step 0 — Parse Parameters

Parse from the command:

- **`"{requirement text}"`** — the operator's requirement. Required unless `--srs` is used.
- **`--project {slug}`** — project identifier. If not provided, use the current working directory name. Confirm: `"Using project slug: {slug}. Continue? (y/n)"` and wait for operator reply.
- **`--level {level}`** — **REQUIRED.** Project depth level. Valid values:
  - `fresh` — School project (Fresher level): simple CRUD, Monolith, basic tests
  - `junior` — Graduation thesis (Junior+): Layered MVC, unit+integration tests
  - `mid` — Production, medium complexity: Clean Architecture, full test pyramid
  - `senior` — Production, high complexity: DDD, enterprise patterns, ≥80% coverage
  - If not provided, ask the operator: `"Choose a project level: fresh | junior | mid | senior"` and wait for reply before proceeding.
- **`--context "{text or path}"`** — extra context to forward to the BA agent. If starts with `./` or `/`, read as file. Otherwise inline text.
- **`--srs`** — forward to BA agent: read SRS workflow artifacts as primary input.

---

## Step 0.5 — Write Project Configuration

Before calling any agent, write `projects/{slug}/team/.project-config.md`:

```markdown
# Project Configuration — {slug}

## Project
**slug:** {slug}
**level:** {fresh|junior|mid|senior}
**set-at:** {ISO 8601 UTC}
**set-by:** /team orchestrator

## Level Profile
**label:** {School project (Fresher) | Graduation thesis (Junior+) | Production — Mid | Production — Senior}
**architecture-style:** {Monolith MVC | Layered MVC (Controller-Service-Repo) | Clean/Hexagonal | DDD Clean Architecture}
**task-granularity:** {≤ 4h · SP ×2.5 · 60% sprint | ≤ 8h · SP ×1.5 · 85% sprint | feature-level · SP ×1.0 · 100% sprint | epic-level · SP ×0.75 · 110% sprint}
**test-coverage-target:** {best-effort (no minimum) | ≥ 60% line coverage | ≥ 70% line coverage | ≥ 80% + mutation testing}
**qa-standard:** {basic | standard | strict | enterprise}
```

Fill each `{...}` with the appropriate value for the chosen level. This file is the single source of truth for all downstream agents.

Output: `[Virtual Team] ✓ Project configuration written — level: {level} ({label})`

---

## Step 1 — Pre-flight

Output:

```
[Virtual Team] Starting pipeline for project: {slug}
[Virtual Team] Level: {level} — {label}
[Virtual Team] Hooks: level_gate.py + pre_write_validator.py configured (subject to Codex hook trust)
[Virtual Team] Pipeline: BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC
```

Check for existing QA sign-off from a prior run:

- Use Glob: `projects/{slug}/team/qa/sign-off.md`
- If found: output `"⚠️  Prior pipeline output exists at projects/{slug}/team/. Overwrite? (y/n)"` and wait.

---

## Step 2 — BA Phase

Read `.codex/skills/team-ba/SKILL.md`, then follow it with this input:

```
"{requirement text}" --project {slug} --level {level} {--srs if flag present} {--context "..." if provided}
```

**After the skill completes**, check its output:

- Contains `HARD STOP` → output the error and STOP the entire pipeline.
- Contains `[BA] ✓ Validation passed` → proceed.

Output: `[Gate Check] BA artifacts ready — starting TechLead phase...`

---

## Step 3 — TechLead Phase

Read `.codex/skills/team-techlead/SKILL.md`, then follow it with this input:

```
--project {slug} --level {level}
```

Check output:

- `HARD STOP` → output error and STOP.
- `[Gate 1] ✓ Design Freeze declared` → proceed.

Output: `[Gate 1] ✓ Design Freeze — starting PM phase...`

---

## Step 4 — PM Phase

Read `.codex/skills/team-pm/SKILL.md`, then follow it with this input:

```
--project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise proceed.

Output: `[PM] ✓ Sprint plan ready — loading task registry...`

---

## Step 4.5 — Load Task Registry for Todo Tracking (FR-42)

Read: `projects/{slug}/team/pm/task-breakdown.md`

Parse every **TASK-{NNN}** entry and extract its `**Assigned to:**` field.

Build an in-context assignment map:
- **BE_TASKS**: list of task titles where `Assigned to: BE Dev`
- **FE_TASKS**: list of task titles where `Assigned to: FE Dev`
- **TESTER_TASKS**: list of task titles where `Assigned to: Tester`
- **OTHER_TASKS**: any remaining tasks (TechLead, Documentation, etc.)

Keep this map in context. Use Codex's active plan/checklist capability when available; otherwise report the same status changes in phase-transition output.

Output: `[PM] ✓ Task registry loaded: {n} BE Dev, {n} FE Dev, {n} Tester, {n} other tasks`

---

## Step 5 — BE Dev Phase

**Before the phase:** Update the active plan/checklist, when available, with the full task list:
- All **BE_TASKS** → `status: "in_progress"`
- All other tasks → `status: "pending"`

Read `.codex/skills/team-dev/SKILL.md`, then follow it with this input:

```
--project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise, after the phase, update the active plan/checklist when available:
  - All **BE_TASKS** → `status: "completed"`
  - All other tasks remain `status: "pending"`

Output: `[BE Dev] ✓ Backend artifacts ready — starting FE Dev phase...`

---

## Step 6 — FE Dev Phase

**Before the phase:** Update the active plan/checklist when available:
- All **BE_TASKS** → `status: "completed"` (already done)
- All **FE_TASKS** → `status: "in_progress"`
- All other tasks → `status: "pending"`

Read `.codex/skills/team-fe/SKILL.md`, then follow it with this input:

```
--project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise, after the phase, update the active plan/checklist when available:
  - All **BE_TASKS** → `status: "completed"`
  - All **FE_TASKS** → `status: "completed"`
  - All other tasks remain `status: "pending"`

Output: `[FE Dev] ✓ Frontend artifacts ready — starting Tester phase...`

---

## Step 7 — Tester Phase

**Before the phase:** Update the active plan/checklist when available:
- All **BE_TASKS** → `status: "completed"`
- All **FE_TASKS** → `status: "completed"`
- All **TESTER_TASKS** → `status: "in_progress"`
- All **OTHER_TASKS** → `status: "pending"`

Read `.codex/skills/team-test/SKILL.md`, then follow it with this input:

```
--project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise, after the phase, mark all tasks completed in the active plan/checklist when available.
- Note Gate 2 status from output.

Output: `[Gate 2] {status} — starting QA/QC phase...`

---

## Step 8 — QA/QC Phase

Read `.codex/skills/team-qa/SKILL.md`, then follow it with this input:

```
--project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Note Gate 3 verdict.

---

## Step 9 — Read Flag Summary

Before treating the flag summary as complete, run the aggregator explicitly so the workflow also works when project hooks are not trusted:

```bash
python .codex/hooks/flag_aggregator.py --dir projects/{slug}/team/
```

Read: `projects/{slug}/flags-summary.md`

- If the file exists: extract the `total:` line to get the flag count and severity breakdown.
- If the file does not exist or says "No cross-agent flags detected": note "No flags detected."

Do NOT write or overwrite `flags-summary.md` — it was already produced by the script you ran.

---

## Step 10 — Final Status

Read `projects/{slug}/team/qa/sign-off.md` and extract the Verdict line.

Output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Virtual Team] Pipeline COMPLETE — project: {slug}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phases completed:
  [BA]       ✓  →  projects/{slug}/team/ba/
  [TechLead] ✓  →  projects/{slug}/team/techlead/   (Gate 1: Design Freeze ✓)
  [PM]       ✓  →  projects/{slug}/team/pm/
  [BE Dev]   ✓  →  projects/{slug}/team/be/
  [FE Dev]   ✓  →  projects/{slug}/team/fe/
  [Tester]   ✓  →  projects/{slug}/team/tester/     (Gate 2: UAT Readiness {status})
  [QA/QC]    ✓  →  projects/{slug}/team/qa/         (Gate 3: {verdict})

Artifacts self-validated by each role; hook enforcement: pre_write_validator.py (when trusted)

{If flags:}
⚠️  {count} cross-agent flags → projects/{slug}/flags-summary.md

Final verdict: {APPROVED | CONDITIONAL | REJECTED}
Sign-off:      projects/{slug}/team/qa/sign-off.md

Note: QA/QC verdict is advisory — operator has final authority.
```
