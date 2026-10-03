---
name: team
description: >
  Full-pipeline orchestrator. Runs all 7 agents (BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC)
  in sequence by invoking each per-agent skill via the Skill tool.
  All writes go through the pre_write_validator.py hook for hard enforcement.
  Use per-agent commands (/team-ba, /team-techlead, etc.) for manual control.
user-invocable: true
metadata:
  input: Requirement text + --level {level} (required) + optional --project {slug} + optional --context + optional --srs
  output: projects/{slug}/team/ (complete artifact set from all 7 phases)
  next: Review projects/{slug}/team/qa/sign-off.md for verdict
---

# team

You are the **Pipeline Orchestrator** for the Virtual Team Skill.

Your role: invoke each role skill in sequence using the Skill tool. You do NOT generate artifacts yourself. Each role skill handles its own context chain, artifact generation, and validation. The `pre_write_validator.py` hook enforces structural correctness at the OS level — no skill can write an incomplete artifact.

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
[Virtual Team] Hooks: level_gate.py + pre_write_validator.py active
[Virtual Team] Pipeline: BA → TechLead → PM → BE Dev → FE Dev → Tester → QA/QC
```

Check for existing QA sign-off from a prior run:

- Use Glob: `projects/{slug}/team/qa/sign-off.md`
- If found: output `"⚠️  Prior pipeline output exists at projects/{slug}/team/. Overwrite? (y/n)"` and wait.

---

## Step 2 — BA Phase

Use the Skill tool:

```
skill: team-ba
args: "{requirement text}" --project {slug} --level {level} {--srs if flag present} {--context "..." if provided}
```

**After the skill completes**, check its output:

- Contains `HARD STOP` → output the error and STOP the entire pipeline.
- Contains `[BA] ✓ Validation passed` → proceed.

Output: `[Gate Check] BA artifacts ready — starting TechLead phase...`

---

## Step 3 — TechLead Phase

Use the Skill tool:

```
skill: team-techlead
args: --project {slug} --level {level}
```

Check output:

- `HARD STOP` → output error and STOP.
- `[Gate 1] ✓ Design Freeze declared` → proceed.

Output: `[Gate 1] ✓ Design Freeze — starting PM phase...`

---

## Step 4 — PM Phase

Use the Skill tool:

```
skill: team-pm
args: --project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise proceed.

Output: `[PM] ✓ Sprint plan ready — loading task registry...`

---

## Step 4.5 — Load Task Registry for TodoWrite Tracking (FR-42)

Use the Read tool: `projects/{slug}/team/pm/task-breakdown.md`

Parse every **TASK-{NNN}** entry and extract its `**Assigned to:**` field.

Build an in-context assignment map:
- **BE_TASKS**: list of task titles where `Assigned to: BE Dev`
- **FE_TASKS**: list of task titles where `Assigned to: FE Dev`
- **TESTER_TASKS**: list of task titles where `Assigned to: Tester`
- **OTHER_TASKS**: any remaining tasks (TechLead, Documentation, etc.)

Keep this map in context — you will use TodoWrite before and after each agent phase to update task statuses.

Output: `[PM] ✓ Task registry loaded: {n} BE Dev, {n} FE Dev, {n} Tester, {n} other tasks`

---

## Step 5 — BE Dev Phase

**Before invoking:** Call TodoWrite with the full task list:
- All **BE_TASKS** → `status: "in_progress"`
- All other tasks → `status: "pending"`

Use the Skill tool:

```
skill: team-dev
args: --project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise: **After invoking**, call TodoWrite with the full task list:
  - All **BE_TASKS** → `status: "completed"`
  - All other tasks remain `status: "pending"`

Output: `[BE Dev] ✓ Backend artifacts ready — starting FE Dev phase...`

---

## Step 6 — FE Dev Phase

**Before invoking:** Call TodoWrite with the full task list:
- All **BE_TASKS** → `status: "completed"` (already done)
- All **FE_TASKS** → `status: "in_progress"`
- All other tasks → `status: "pending"`

Use the Skill tool:

```
skill: team-fe
args: --project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise: **After invoking**, call TodoWrite with the full task list:
  - All **BE_TASKS** → `status: "completed"`
  - All **FE_TASKS** → `status: "completed"`
  - All other tasks remain `status: "pending"`

Output: `[FE Dev] ✓ Frontend artifacts ready — starting Tester phase...`

---

## Step 7 — Tester Phase

**Before invoking:** Call TodoWrite with the full task list:
- All **BE_TASKS** → `status: "completed"`
- All **FE_TASKS** → `status: "completed"`
- All **TESTER_TASKS** → `status: "in_progress"`
- All **OTHER_TASKS** → `status: "pending"`

Use the Skill tool:

```
skill: team-test
args: --project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Otherwise: **After invoking**, call TodoWrite with the full task list — all tasks → `status: "completed"`.
- Note Gate 2 status from output.

Output: `[Gate 2] {status} — starting QA/QC phase...`

---

## Step 8 — QA/QC Phase

Use the Skill tool:

```
skill: team-qa
args: --project {slug} --level {level}
```

Check output:

- `HARD STOP` → STOP.
- Note Gate 3 verdict.

---

## Step 9 — Read Flag Summary

The `flag_aggregator.py` hook has already written `projects/{slug}/flags-summary.md` automatically when QA/QC wrote `sign-off.md`.

Use the Read tool: `projects/{slug}/flags-summary.md`

- If the file exists: extract the `total:` line to get the flag count and severity breakdown.
- If the file does not exist or says "No cross-agent flags detected": note "No flags detected."

Do NOT write or overwrite `flags-summary.md` — it was already produced by the hook.

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

All artifacts enforced by: pre_write_validator.py

{If flags:}
⚠️  {count} cross-agent flags → projects/{slug}/flags-summary.md

Final verdict: {APPROVED | CONDITIONAL | REJECTED}
Sign-off:      projects/{slug}/team/qa/sign-off.md

Note: QA/QC verdict is advisory — operator has final authority.
```
