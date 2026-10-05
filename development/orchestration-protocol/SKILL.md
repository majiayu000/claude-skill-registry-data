---
name: orchestration-protocol
description: >
  The single source of truth for how TFW commands survey their runtime, choose an
  execution mode (teams / subagents / sequential), route models, and run the TOH LOOP —
  the autonomous plan-execute-verify protocol driven by .toh/plan.md + .toh/progress.md.
  Loaded by /toh, /toh-vibe, /toh-plan. Triggers: build a whole plan, resume a plan,
  "continue building", autonomous execution, multi-agent orchestration, parallel agents,
  work until done, MVP build, big multi-task jobs.
triggers:
  - /toh (multi-task jobs)
  - /toh-vibe (autonomous builds)
  - /toh-plan (plan artifact + handoff)
  - Any request to execute or resume .toh/plan.md
---

# 🔁 Orchestration Protocol

> **Purpose:** One protocol for surveying the runtime, picking the right execution mode, and building until done — without asking the user between tasks.
> **Version:** 1.0.0
> **For:** Toh Framework v2.0.0+
> **Used by:** `/toh`, `/toh-vibe`, `/toh-plan` — MANDATORY for multi-task work

**Core idea:** the plan is a file, never chat state. `.toh/plan.md` holds the backlog, `.toh/progress.md` holds the ledger, and the loop runs until every "Done When" criterion is verified. The model only remembers what is saved to disk.

---

## 🔍 A. 2-Step Survey (run before any multi-task job)

### Step 1 — Identity (declared, never guessed)

Your runtime identity is declared by the platform context file that loaded you:

| Context file that loaded you | Runtime |
|------------------------------|---------|
| `CLAUDE.md` | Claude Code |
| `.cursor/rules/*.mdc` | Cursor |
| `AGENTS.md` | Codex **or** ZCode — the `**Runtime:**` line inside the file names which |
| `.agents/rules/toh-framework.md` | Antigravity (+ Antigravity CLI) |
| `GEMINI.md` | Gemini CLI (legacy) |

Confirm capabilities from `.toh/capabilities.json` (written by the installer). If it is missing, infer conservatively: Claude Code has subagents, teams, hooks, `/goal`, `/loop`; Cursor (2.4+) and Antigravity have native/file-based subagents but no teams; Codex and ZCode are single-session sequential.

### Step 2 — Runtime probe (ONLY for what install time cannot know)

Probe exactly these, nothing else:

| Probe | Gate |
|-------|------|
| Agent Teams | env `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is set |
| `/goal` | Claude Code >= 2.1.139 |
| Workflows | Claude Code >= 2.1.154 (can be plan-disabled) |

Do NOT invent other detection heuristics. Identity comes from Step 1; the probe only checks feature gates.

---

## 🪜 B. Execution Ladder

Three rungs, best first. **Each rung: if unavailable, fall back one rung.** Sequential is the floor and is always available.

1. **AGENT TEAMS** — Claude Code with the teams env flag set, AND the plan has >= 3 independent modules plus a QC role. Recipe in Section F. If unavailable, fall back one rung.
2. **NATIVE SUBAGENTS** — the Agent tool (Task) exists. Delegate tasks to TFW agents; parallel only under the rules below. If unavailable, fall back one rung.
3. **SEQUENTIAL SELF** — execute every task yourself, in order, in this session. This is the default mode and the correct choice more often than not.

### When to use which

| Situation | Mode |
|-----------|------|
| <= 3 tasks total | SEQUENTIAL |
| Same-file or dependent edits | SEQUENTIAL |
| Debugging / fixing | SEQUENTIAL |
| Runtime without subagents (Codex / ZCode / Gemini) | SEQUENTIAL |
| >= 2 independent tasks on disjoint files, each substantial (~5+ min) | PARALLEL subagents |
| MVP-scale: >= 3 independent modules + a QC role, teams flag set | TEAMS |

### Hard limits (load-bearing — never soften)

| Constant | Value |
|----------|-------|
| Concurrent subagents/teammates | max **4** |
| Delegation depth | <= **2** (you → worker; workers never spawn) |
| QC fix iterations per task | max **5** |
| Consecutive failures on same task → BLOCKED | **3** |
| `/goal` bound | "or stop after **40** turns" |
| `.toh/plan.md` size | <= **150** lines |

Parallelism must be earned by independence — a wrong parallel split costs more than sequential ever would.

### Delegation brief (subagents and teammates)

Every spawn prompt MUST carry:

- The plan task line verbatim (T-ID, agent, description, exact file path) — the worker touches ONLY those files.
- The phase Checkpoint command, with instructions to run it and report the actual output.
- For UI tasks: "read root `DESIGN.md` first — all tokens/typography/nav come from it."
- The reminder that its report will be re-verified by the orchestrator (Section E step 4).

---

## 🎚️ C. Model Routing

Mirrors TFW agent frontmatter; teams and subagents both honor per-agent `model` fields.

| Tier | Use for |
|------|---------|
| **haiku** | Scaffolding, boilerplate, test writing |
| **sonnet** | Builders — ui-builder, dev-builder, implementation work |
| **opus** | Planning, QC/review, design review |

On runtimes without model routing, ignore this table and proceed.

---

## 📄 D. Plan Artifact — `.toh/plan.md`

The contract between `/toh-plan` (writes it) and `/toh-vibe` (executes it). Compact state file, **<= 150 lines**, re-read once per phase.

```markdown
# Plan: <project name>
Status: draft | approved | building | done
Created: <date> by /toh-plan

## Goal
<one paragraph: what, for whom, why>

## Stack
- <framework, styling, data — bullets>

## Pages
| Page | Route | Purpose |
|------|-------|---------|

## Done When
- [ ] `npm run build` exits 0
- [ ] Every route in Pages renders without console errors
- [ ] <observable feature criterion, e.g. "adding an item updates the cart badge">

## Phase 1 — <name>
- [ ] T000 design-reviewer — generate root DESIGN.md (design identity)
- [ ] T001 [P] ui-builder — dashboard shell in app/dashboard/page.tsx
- [ ] T002 dev-builder — cart state hook in lib/use-cart.ts
**Checkpoint:** `npm run build` exits 0 AND /dashboard renders

## Phase 2 — <name>
- [ ] T003 ...
**Checkpoint:** <runnable command + expected result>
```

### Schema rules

- **Task grammar:** `- [ ] T001 [P] agent-name — description in app/exact/path.tsx`. Exact file path mandatory. `[P]` = parallel-safe (disjoint files only). Each task sized to fit one context window.
- **T000 rule:** any project/feature with UI gets `T000 design-reviewer — generate root DESIGN.md` as the FIRST task, before any UI task. UI tasks depend on it.
- **Checkpoint per phase:** a runnable command + expected result. Phases end at checkpoints, not at vibes.
- **Done When:** runnable/observable acceptance criteria for the whole plan — completion is verified against these, never self-assessed.
- **Blocked marker:** flip `- [ ]` to `- [!]` and append `BLOCKED: <one-line diagnosis>`.
- **NO Progress Log in plan.md** — state history lives in `.toh/progress.md`. Keep plan.md a compact snapshot: checkboxes ARE the state.
- **Status lifecycle:** `draft` (written, awaiting one approval) → `approved` (user said Go, or /toh-vibe auto-approves its own mini-plan) → `building` (loop running) → `done` (all Done When verified).
- **Terminal statuses — auto-resume exemption:** a plan whose Status is `done`, `draft`, `blocked`, or `paused` (any case) is TERMINAL for auto-resume: report the status, do not resume its checkboxes. `blocked`/`paused` are manual header overrides for parking a plan; flip Status back to `approved`/`building` (or say "continue the plan") to make it resumable again.
- **Archive:** when a new plan is needed and Status is `done` (or the user says "fresh start"), move the old file to `.toh/memory/archive/plan-<date>.md` first. One active plan at a time.
- **Memory pointer:** `.toh/memory/active.md` holds only a POINTER — plan status + next unchecked task — never a plan dump.

### Ledger — `.toh/progress.md`

Append-only, one line per state change, plus learnings:

```
2026-07-16 14:02 T001 queued
2026-07-16 14:03 T001 running (ui-builder)
2026-07-16 14:11 T001 done — CHECK_OK: npm run build exit 0
2026-07-16 14:30 T004 blocked — BLOCKED: STRIPE_SECRET_KEY missing, checkout untestable
LEARNING: Tailwind 4 needs @import "tailwindcss" not @tailwind directives
```

Learnings are gotchas worth remembering across sessions — append them when discovered; promote durable ones to `.toh/memory/decisions.md`.

---

## 🔁 E. The TOH Loop

The universal execution protocol. Runs identically on every runtime; Claude Code merely enforces it harder (Section G).

0. **SURVEY** — Section A, then choose a rung from Section B.
1. **LOAD** — read `.toh/plan.md` + `.toh/progress.md`. If plan.md is absent, write a mini-plan first (4–8 tasks, Done When, Checkpoint per phase, Status: approved), then continue.
2. **PICK** — the first unchecked, unblocked task. Append `T00x running` to progress.md.
3. **IMPLEMENT** — only that task. Delegate per Sections B/C, or do it yourself on the sequential rung. One task per iteration.
4. **QC GATE** — run the phase Checkpoint **YOURSELF** and **QUOTE the actual output lines** into the conversation. A builder/teammate report is evidence to verify, never proof. Only a quoted passing run counts as done.
5. **IF RED** — state the root cause from the quoted text, apply a minimal fix, re-run. Budget: max **5** fix iterations per task; **3 consecutive failures** on the same task → mark it `[!] BLOCKED: <one-line diagnosis>` in plan.md, log it in progress.md, and return to step 2 for independent work.
6. **IF GREEN** — flip `- [ ]` to `- [x]`, append `T00x done — CHECK_OK: <command + result>` and any learnings to progress.md, update the pointer in `.toh/memory/active.md`, and go to step 2 **WITHOUT asking the user**. Emit exactly ONE status line per task (e.g. `CHECK_OK T003 — cart hook, build green`), nothing more.
7. **REPEAT** — until no unchecked, unblocked tasks remain.
8. **FINISH** — run EVERY `Done When` criterion and quote its output.
   - All green and nothing blocked → set Status: done, output `<promise>COMPLETE</promise>`, then close per **engineer-harness Section C** (the announce/next-actions contract lives there — follow it, do not improvise).
   - Blocked tasks exist → escalate: per-task one-line diagnosis, then close per engineer-harness Section C with unblocking as the recommended action.

### Loop rules

- **Never ask "continue?" between tasks or phases.** Interrupt only for genuine blockers: missing credentials, destructive/irreversible choices, or a contradiction in the plan itself.
- **Foundation deadlock:** if a blocked task makes everything downstream dependent (nothing independent remains), stop and deliver one clear blocker report — do not thrash on dependent tasks.
- **Checkbox-resume:** any fresh session (any IDE, any day) reads plan.md and continues at the first unchecked task — unless the plan header carries a terminal status (`Status: done/draft/blocked/paused`): then report the status and stop, do not resume. This is the crash/context-loss recovery mechanism — keep the file states accurate at all times.
- **Completion is a contract:** `<promise>COMPLETE</promise>` may only follow quoted, passing Done When runs. Never emit it on feel.

---

## 👥 F. Teams Recipe (Claude Code, env-gated)

Preconditions: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` set AND plan has >= 3 independent modules. Otherwise fall back one rung (Section B).

1. **Spawn** teammates from TFW agent definitions by name (their `tools` + `model` frontmatter is honored): one builder per independent module (**sonnet**), one QC teammate (**opus**). Respect the cap of 4 concurrent.
2. **Plan approval, autonomous:** require plan approval for builders. YOU (the lead) approve or reject — no human in the loop — against exactly these criteria: *the plan names its verify command AND touches only files disjoint from every other teammate.* Reject with the reason otherwise.
3. **Delegate mode:** the lead coordinates only — never edits files itself.
4. **Task list:** create tasks from plan.md task lines with their dependencies; each teammate owns disjoint files.
5. **Dispatch → wait → synthesize:** one dispatch per wave, then wait for completion reports (SendMessage mailbox). **No polling** — do not repeatedly check on teammates.
6. **Trust boundary:** teammate reports are evidence to verify, never proof. The lead re-runs each phase Checkpoint itself (Section E step 4) before flipping any checkbox.
7. **Hooks as backstop:** optional hardening you can add to `.claude/settings.json` (not shipped by the installer): a `TaskCompleted` hook (exit 2 if the verify command fails → the task cannot be marked complete) and a `TeammateIdle` hook (exit 2 with remaining work → idle teammate keeps going).

---

## ⚙️ G. Claude Code Enforcement Notes

Section E is the floor on every runtime. On Claude Code the installer ships machinery that enforces it:

| Mechanism | What it does |
|-----------|--------------|
| **Stop hook** (prompt-type, in `.claude/settings.json`) | Blocks ending the session while plan.md has unchecked, unblocked tasks — returns `{"ok": false, "reason": "<first unchecked task>"}`. Guarded: if `stop_hook_active` and no progress since the last block, or every remaining task is `[!]` blocked, or plan.md is absent or its header says `Status: done/draft/blocked/paused`, it returns ok — respecting the 8-consecutive-block cap. |
| **`.claude/loop.md`** (<= 25KB) | Heartbeat prompt for bare `/loop`: if plan.md is absent or its header carries a terminal status (`Status: done/draft/blocked/paused`), report that in one line and stop — never auto-resume a parked plan (same exemptions as the Stop hook); otherwise continue the first unchecked task per the TOH Loop, fix from quoted failure output, say COMPLETE in one line when green. Note: on Bedrock/Vertex/Foundry, bare `/loop` prints usage instead of reading this file — run `/loop <prompt>` explicitly there. |
| **`/goal` recipe** (>= 2.1.139) | Set the finish line before coding: `/goal every task in .toh/plan.md is checked and the build command exits 0 — or stop after 40 turns`. A Haiku evaluator judges the condition FROM THE TRANSCRIPT — one more reason the QC gate quotes actual output: unquoted results are invisible to the evaluator. |
| **Workflows** (>= 2.1.154, optional) | `/toh-sweep` (not shipped — optional pattern you can save to `.claude/workflows/`) can fan out fixers per failing task until checks pass. |

**Antigravity** runs the same loop and also gets a deterministic Stop hook (`.agents/hooks.json`) that blocks ending a session while `.toh/plan.md` has unchecked tasks (both hooks exempt a terminal-status plan). **Every other runtime** (Cursor / Codex / ZCode / Gemini) runs the SAME loop as prose in one session — no hooks, no `/goal`. The recovery mechanism there is checkbox-resume: a fresh session picks up at the first unchecked task — unless the plan header carries a terminal status (done/draft/blocked/paused), which is reported instead of resumed. If context runs low mid-plan, flush state (plan checkboxes + progress.md + active.md pointer), then tell the user to re-run the command — it resumes exactly where it stopped.

---

## 🔗 Integration

Commands load this skill for any multi-task job and pair it with the closing contract:

```yaml
skills:
  - orchestration-protocol   # survey + ladder + plan artifact + TOH Loop
  - engineer-harness         # Section C: announce block + next actions (canonical)
```

Division of labor: this skill owns HOW work gets executed and verified; engineer-harness Section C owns how every stage ENDS (status, evidence, exactly the right next actions). Reference both; duplicate neither.

---

*Orchestration Protocol v1.0.0 — survey, ladder, plan artifact, and the TOH Loop in one place. Commands reference this skill; they never duplicate it.*
