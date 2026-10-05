---
name: cm-execution
description: Use when executing approved implementation plans. Routes to 1 of 6 execution modes (batch/subagent/parallel/RARV/TRIZ/party) based on task shape. Loads detail refs on-demand.
token_budget: 1800
token_core: 450
token_refs:
  mode-a-batch: 280
  mode-b-subagent: 380
  mode-c-parallel: 240
  mode-d-rarv: 520
  mode-e-triz-parallel: 460
  mode-f-party: 420
  persona-dispatch: 180
  security-rules: 540
compressed: true
deprecated: false
---

# Execution — Execute Plans at Scale

## TL;DR
- **Use when** running an approved plan from `cm-planning`
- **Reads** `handoff/plan.json` or `openspec/changes/[name]/tasks.md`
- **Writes** `handoff/exec.json`
- **Autonomy**: one scoped authorization, no step/batch re-approval
- **Always** verify before reporting done
- **Next** `cm-code-review`

> **Role: Lead Developer.** You execute plans systematically with continuous verification and non-blocking status updates.

Follow [`_shared/autonomy-policy.md`](../_shared/autonomy-policy.md). Treat an approved plan as scoped execution authorization through verification. Do not request per-step or per-batch re-approval inside that scope.

## Step 0: Load Working Memory (MANDATORY)
Per `_shared/helpers.md#Load-Working-Memory`. After EACH completed task: `_shared/helpers.md#Update-Continuity`.

## Step 1: Pre-flight Skill Coverage Audit
Scan plan tasks for tech keywords, cross-reference `cm-skill-index`, check installed skills, and use `npx skills find` when the plan reaches beyond current coverage. If `codegraph` or `cm-codeintell` context is available, inject it into agent prompts so execution skips redundant repo searching.

Confirm the authorization state from the handoff, not by asking the user again:
- Approved plan → execute its stated scope through verification.
- Clear, reversible micro task directly requested by the user → proceed with zero approval.
- Meaningful change without an approved plan → present a concise plan and request one approval at the plan-to-execution boundary.
- Material scope change or sensitive action → pause under the shared policy; execution-mode selection itself never needs approval.

## Step 2: Choose Mode

```
Have an approved plan?
├─ Have 2+ independent tasks where parallel execution helps?
│   ├─ File/dependency analysis and conflict pre-flight pass?
│   │   └─ YES → Mode E (TRIZ-Parallel) ★ recommended
│   └─ Tasks are ordered/dependent and isolated subagents are available?
│       └─ YES → Mode B (Subagent-Driven)
├─ One non-trivial task, want multi-perspective without subagent cost?
│   └─ YES → Mode F (Party, persona rotation)
├─ Multiple independent failures across subsystems?
│   └─ YES → Mode C (Parallel Dispatch)
├─ Autonomous loop with backlog (`/cm-start` flow)?
│   └─ YES → Mode D (RARV)
└─ Otherwise
    └─ Mode A (Batch Execution)
```

| Mode | One-line summary | Load |
|---|---|---|
| A | Batch 3 tasks, report, then continue | `references/mode-a-batch.md` |
| B | Fresh subagent per task + 2-stage review | `references/mode-b-subagent.md` |
| C | One agent per independent problem domain | `references/mode-c-parallel.md` |
| D | Reason → Act → Reflect → Verify loop | `references/mode-d-rarv.md` |
| E | Dependency-aware parallel + per-agent quality gate | `references/mode-e-triz-parallel.md` |
| F | Single agent rotates Architect → Engineer → Reviewer | `references/mode-f-party.md` |

**Action:** Pick exactly one mode, read only that reference, and execute from there.

Before selecting Mode B, verify the harness supports fresh and resumable isolated sessions. If it does not, route to Mode F (reduced review independence) or Mode A; never silently simulate independent reviewers in one context. Mode B is serial. Mode E remains the only mode for independent parallel tasks and always retains conflict pre-flight.

## Conditional References
- **Mode B / E / F** → also read `references/persona-dispatch.md`
- **Task touches auth, files, subprocess, DOM, config paths, or user input** → MUST read `references/security-rules.md` before writing code

## Karpathy Discipline — Surgical Changes
- Touch only what the task requires. No "while I'm here" refactors.
- Match existing style even if you would write it differently.
- Notice unrelated dead code? Mention it, do not delete it.
- Clean only your own orphans. Pre-existing dead code stays unless asked.
- **Diff test:** every changed line must trace to the task.
- After a task or batch, send a non-blocking status update and continue while scoped execution authorization remains valid.

## Integration
| Skill | When |
|---|---|
| `cm-planning` | Produces the plan this skill consumes |
| `cm-tdd` | Use per task when implementing or fixing |
| `cm-quality-gate` | VERIFY phase / pre-report validation |
| `cm-code-review` | Final review after all tasks are done |
| `cm-design-system` | Recommended before frontend-heavy tasks |

## Workflows
| Command | Purpose |
|---|---|
| `/cm-start` | Create tasks + launch RARV + open dashboard |
| `/cm-status` | Quick terminal progress summary |
| `/cm-dashboard` | Open browser dashboard |

## The Bottom Line
**Choose your mode → load that one reference → execute the authorized scope → verify → review.**
