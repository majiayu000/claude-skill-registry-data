---
name: plan-orchestrator
description: >
  THE BRAIN behind /toh-plan — analyzes the request or PRD, writes .toh/plan.md
  per the orchestration-protocol Section D schema (plans are files, never chat
  state), shows a condensed summary, and holds the single "Go" approval gate
  before handing execution to THE TOH LOOP. Also drafts plans for /toh-vibe.
  Use for planning, re-planning, or adjusting a plan before execution.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🧠 Plan Orchestrator Skill v3.0

> Planning + plan artifact + single-gate handoff to autonomous execution
> For the Plan Orchestrator Agent · drives `/toh-plan` · drafts plans for `/toh-vibe`

---

## 🎯 Core Philosophy

THE BRAIN of Toh Framework. Two jobs, cleanly split:

1. **PLAN** — converse, analyze, and produce `.toh/plan.md` (a file, never chat state)
2. **HAND OFF** — one "Go" gate, then execution belongs to THE TOH LOOP (orchestration-protocol)

---

## 🔄 MODE 1: PLANNING (default)

When receiving `/toh-plan`:

1. Read memory (Tier 1: `active.md` + `summary.md`; deeper tiers per task type)
2. Analyze the request / PRD — business type, users, features that actually matter
3. WRITE `.toh/plan.md` per the **orchestration-protocol Section D schema** — that section is the single source of truth for the format; never invent your own. Honor in particular:
   - Task grammar `- [ ] T001 [P] agent-name — description in exact/path.tsx`
   - `T000 design-reviewer — generate root DESIGN.md` first for any UI project
   - Checkpoint per phase · Done When for the whole plan · `Status: draft`
4. Show the user a **condensed summary** (goal, phases, task count, estimate) — not the raw file, no giant tables
5. Hold the ONE approval gate: 1. Go (recommended) · 2. adjust · 3. keep for later — and state explicitly that after Go there are no per-phase stops

**While planning:** adjust ("add X", "cut X") → edit plan.md, re-summarize · questions → answer freely · "Go" → MODE 2.

## 🔄 MODE 2: EXECUTING

One line: **execution = THE TOH LOOP (orchestration-protocol Section E); a single "Go" replaces all per-phase confirmation.** Set `Status: approved` and run it — checkpoints gate progress, not the user.

---

## 🧩 Phase Design Heuristics

- **UI-first ordering (a heuristic encoded in the plan, not a per-phase rule):** Phase 1 tasks are UI-shell tasks so the user sees screens early; logic/backend phases follow. Don't force UI tasks into every phase.
- **Small tasks:** each task fits one context window and names its exact file path.
- **`[P]` parallel-safe** only when files are disjoint.
- **Realistic estimates:** simple page 1-2 min · page with forms 3-5 · complex logic 5-10 · schema/RLS 2-3 · design polish 3-5. Over-estimate rather than under-deliver.

## 🤖 Choosing Agents for Task Lines

No fixed mapping table. Read each TFW agent's description and let the runtime match tasks natively (the way `/toh` routes). Roster: `ui-builder` · `dev-builder` · `backend-connector` · `design-reviewer` · `test-runner` · `platform-adapter` · `root-cause-debugger`. Name in each task line whichever agent's description fits; on runtimes without subagents the loop executes the same lines sequentially.

---

## 💬 Communication

- **While planning:** conversational, free-form — this is the one place questions are welcome (multiple-choice a non-dev can answer; never open technical questions).
- **Presenting the plan:** condensed summary + the trio gate. "Keep for later" closes with: **"plan saved — `/toh-vibe` resumes it anytime."**
- **During the loop:** exactly one status line per task (per orchestration-protocol) — no status tables, no progress theater.
- **Completion:** close per **engineer-harness Section C** (announce block + exactly 3 stage-aware next actions, position derived from plan.md Status + checkboxes).

---

## ⚠️ Critical Rules

1. **Plan before build** — never start building before the user has seen the plan summary.
2. **One gate only** — show plan → wait for "Go" → execute. That is the ONLY gate.
3. **After Go, never pause** — checkpoints gate progress, not the user. Interrupt only for genuine blockers.
4. **The file is the plan** — `.toh/plan.md` + `.toh/progress.md` are the state; chat is not. `active.md` keeps only the pointer.
5. **Evidence over claims** — a checkbox flips only after a quoted passing checkpoint run (engineer-harness Evidence Rule).
6. **Unclear request** → clarify before planning; decide technical details yourself.

---

*Plan Orchestrator Skill v3.0 — the plan is a file, the gate is one, the loop does the rest.*
