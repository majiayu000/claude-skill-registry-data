---
name: startcycle
description: Linear multi-agent build pipeline with file hand-offs in production_artifacts/, run after /bdbrainstorm or /grill-me. This is the linear variant — no state.json, no repair loop, no dispatcher graph — distinct from startcycle-graph, which adds durable state and automated escalation.
category: bdb-core
---

# `/startcycle` — Linear Build Pipeline

A straight-line run through the BDB agent roster. Whoever invokes this skill invokes each step in turn, in order, and every hand-off between steps is a file written under `production_artifacts/`. Nothing else is shared between steps — no memory, no live conversation state, no orchestrator process watching over the run.

```
                  ┌──────────────────────────────────────────────┐
                  │ 0. BRAINSTORM & SPECIFICATION                │
                  │    (/bdbrainstorm / /grill-me)               │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │ 1. ARCHITECT                                  │
                  │    goal ──▶ 00_execution_plan.md              │
                  └──────────────────────┬───────────────────────┘
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │ 2. TECHLEAD                                   │
                  │    approve plan, or send back to Architect    │
                  │    (once)                                     │
                  └──────────────────────┬───────────────────────┘
                                         ▼
              ┌──────────────────────────┴──────────────────────────┐
              ▼                          ▼                          ▼
  ┌───────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
  │ 3a. UI/UX          │   │ 3b. ENGINEERING        │   │ 3c. MEDIA/EVENTTECH    │
  │ 01_frontend_spec.md│   │ 02_backend_schema.md   │   │ 03_media_pipeline.md   │
  │ frontend/src/       │   │ backend/src/           │   │ (only if goal needs it)│
  └──────────┬──────────┘   └───────────┬────────────┘   └───────────┬────────────┘
              └──────────────────────────┴──────────────────────────┘
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │ 4. REVIEWER                                   │
                  │    adversarial pass ──▶ review_findings.md    │
                  └──────────────────────┬───────────────────────┘
                                         ▼
                              ── pipeline ends here by default ──
                                         │
                                (only if release requested)
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │ 5. SHIPPING (optional)                        │
                  │    quality gate ──▶ 04_release_report.md      │
                  └──────────────────────────────────────────────┘
```

---

## Steps

### 1. Architect
- **Agent**: `architect`
- **Reads**: the goal (or `/bdbrainstorm` / `/grill-me` output), existing architecture.
- **Action**: turns the goal into a system plan with an explicit capability map — module boundaries, dependency direction, what streams the goal actually touches.
- **Writes**: `production_artifacts/00_execution_plan.md`
- The plan uses the agenttrail component convention: `## Name {#id}` components with optional `needs:` / `files:` lines, and tasks as `- [ ] ... {#id}`.
- The Architect renders the architecture with `aos-archify` to `production_artifacts/00_architecture.html` and links it from the relevant component with a `url:` line.
- Plan-canvas can review that HTML too.

### 2. TechLead
- **Agent**: `techlead`
- **Reads**: `00_execution_plan.md`.
- **Action**: reviews the plan for module boundaries, dependency direction, and build order. Approves it, or sends it back to Architect once for a revision. This is a gate, not a deliverable — TechLead does not invoke Architect itself; the invoker re-runs step 1 if TechLead rejects.
- **Writes**: no separate file; approval is just the invoker's own record of the gate having passed.

> **Optional — Plan Canvas.** Before or alongside TechLead's gate, the plan can be reviewed in the browser: `aos-plan-canvas open production_artifacts/00_execution_plan.md`, then `aos-plan-canvas await …`. An `approve` verdict is a human confirmation of the gate. This is optional; the pipeline runs unchanged without it. See the `plan-canvas` skill.

### 3. Build (parallel, stream-selective)

**Trigger B — start the live map:** `aos-trail --ensure` (safe to run twice: it reuses a map already running for this repo). Put the live-map link in your reply (the autostart hook also adds it as context when active). Inside AO (env var `AO_BROWSER_CAPABILITY` set) also run `ao preview <url>`. Tell each build agent to mark its tasks `[~]` before starting work, `[x]` when done, `[!]` when stuck, with an indented `by: <agent>` line, saving the plan file immediately after each change. See the `agenttrail` skill.

Run only the streams the goal actually needs. A plain backend feature does not need step 3a or 3c; a pure copy change does not need 3b. Each stream's `skills:` frontmatter already lists what it should reach for — the invoker passes that list through rather than restating it here.

| Stream | Agent | Reads | Writes |
|---|---|---|---|
| 3a. Frontend | `godmode-ui-ux` | `00_execution_plan.md` | `production_artifacts/01_frontend_spec.md` + `frontend/src/` |
| 3b. Backend | `godmode-engineering` | `00_execution_plan.md` | `production_artifacts/02_backend_schema.md` + `backend/src/` |
| 3c. Media/EventTech | `godmode-media-eventtech` | `00_execution_plan.md` | `production_artifacts/03_media_pipeline.md` |

3c is for TouchDesigner, show-control, DMX/grandMA3, 3D, or other media-pipeline goals — most goals are not this. Skip it unless the plan actually calls for it.

> **Injecting a specific skill.** `/startcycle --skill=<name> <goal>`
> (repeatable, quote a name with spaces) forces that skill into this run as
> a hard requirement — for a private skill of your own that isn't part of
> any build agent's own `skills:` frontmatter. Since this variant has no
> dispatcher script or `state.json` to carry it automatically, the invoker
> does the work `startcycle-graph`'s script does for you: extract the
> `--skill=` flag(s) from the invocation text before anything else runs,
> confirm each name resolves to a real `SKILL.md` (under
> any harness's global skills directory — `~/.claude/skills/<name>/`,
> `~/.agents/skills/`, `~/.codex/skills/`, `~/.cursor/skills/` or `~/.roo/skills/`
> — or this project's own `skills/` tree) — stop
> and tell the user if one doesn't, don't silently proceed without it —
> note the validated list in `00_execution_plan.md`, and include it as a
> **hard requirement, not a suggestion** in each Build stream's dispatch
> prompt at step 3. Reviewer (step 4) checks the resulting artifacts for
> evidence the skill was actually applied, not just available, and treats
> an ignored mandate as a contract-misread finding. See
> [`.agents/graph.md`](../../../.agents/graph.md)'s "Mandatory Skill
> Injection" section for the full rationale — this is the same mechanic,
> just invoker-driven instead of script-driven.

### 4. Reviewer
- **Agent**: `reviewer`
- **Reads**: the artifacts each build stream produced (01/02/03) and the plan's stated contract (`00_execution_plan.md`) — nothing else. Never the goal directly, never a build agent's own claim that it's done; passing that claim through biases the review toward agreement.
- **Action**: adversarial pass — "find what is wrong," never "does this look good." Every finding is classified by fixed precedence:
  1. contract misread
  2. valid & actionable (blocking)
  3. valid trade-off (advisory)
  4. noise
- **Writes**: `production_artifacts/review_findings.md`
- **Optional — architecture delta**: compare planned vs built architecture with `aos-archify` (see the `archify` skill, architecture delta).

**The linear pipeline ends here by default.** A plain build or refactor goal is done at step 4 — it does not automatically drag a quality gate and release report behind it.

### 5. Shipping — optional, not a hard-wired terminal step
- **Agent**: `godmode-shipping`
- **Runs only when**: the user explicitly asks for it, or the original goal was itself a release.
- **Action**: lint, typecheck, tests, a11y, SEO — the mechanical quality gate, deliberately separate from Reviewer's adversarial correctness pass.
- **Writes**: `production_artifacts/04_release_report.md`

If the invoker isn't sure whether shipping applies, treat step 4 as the finish line and ask before running step 5.

---

## Explicit non-goals

This skill deliberately does **not** have:
- `production_artifacts/state.json` or `.agents/state.schema.json`
- `.agents/graph.md` bootstrap
- a dispatcher script or `Workflow` tool call
- a repair loop, an iteration counter, a no-progress guard, or escalation machinery
- agents invoking each other — whoever runs the skill invokes each step in turn; no agent hands off directly to the next

If a run needs any of the above, it needs `startcycle-graph`, not this skill.

---

## Which startcycle do I want?

| Skill | Use when |
|---|---|
| `startcycle` (this one) | Linear, predictable, cheapest of the three. You want a straight run through the agents with file hand-offs and no state machine. |
| `startcycle-graph` | You need the full dispatcher graph: durable `state.json`, a Reviewer repair loop with a no-progress guard, an automated quality gate, escalation to a human, and a resumable record. |
| `startcycle-graph-user` | A small throwaway fan-out (2-4 nodes) in any project, nothing persistent left behind. |

---

## Safety

`git push`, `npm publish`, and `npm version` are blocked by `.claude/hooks/go-gate.mjs` unless the user's immediately preceding message is the literal word `GO`. This skill never pushes on its own — Shipping (step 5) prepares the release report; the invoker still needs a fresh `GO` before anything leaves the machine.
