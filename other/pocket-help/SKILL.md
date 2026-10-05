---
name: pocket-help
description: Onboarding and routing guide for the Pocket skill ecosystem. Use when someone asks what Pocket is, which Pocket skill to use, how the end-to-end flow works, or when Pocket is better than lighter Superpowers-style flows. Trigger on "what is pocket", "how do I use pocket", "which pocket skill", "explain pocket", "pocket-help", or any onboarding/routing question. This is a compact entry point — it summarizes every skill so agents and users do NOT have to load each SKILL.md to orient.
---

# Pocket Help

The map of the Pocket ecosystem. Read this first to understand what Pocket is, pick the right skill for the moment, and run the full flow from rough idea to reviewed code — **without loading every skill into context.**

**Core principle:** Orient cheaply, then load deep. This skill is a summary and a router. Load an individual skill's `SKILL.md` only when you reach the stage that uses it. That is the whole point — it preserves the context window for the actual work.

**This skill does not replace the detailed skills.** It tells you which one to open next.

## What Pocket Is

Pocket is a set of skills for **systematic, structured development** — from a vague idea to shipped, reviewed code. Instead of one agent improvising an entire feature in a single long thread, Pocket breaks the work into bounded stages with explicit gates: explore → specify (BDD) → plan (TDD) → phase → delegate → review.

Each stage produces a concrete artifact (pitch doc → spec → execution plan → phase files → commits → review reports) that the next stage consumes. Gates between stages force confirmation before proceeding, which is what keeps a long build from drifting.

## Prerequisites — Pi extensions

On Pi, Pocket's skills call extensions for their core features. Without them, skills hit dead-ends when they try to call `advisor()`, `subagent()`, or `context7_*` tools. Install them once after installing Pocket:

```bash
npx pocketto-pi setup-extensions        # required
npx pocketto-pi setup-extensions --all  # + recommended
npx pocketto-pi doctor                  # check installed vs missing
```

| Required | Feature it powers |
|----------|-------------------|
| `pi-mcp-adapter` | context7 — library-aware code generation |
| `@gotgenes/pi-subagents` | subagent delegation + parallel reviews |
| `@juicesharp/rpiv-advisor` | advisor — LLM-to-LLM review/escalation gates |

Recommended (with `--all`): `@juicesharp/rpiv-ask-user-question`, `@tintinweb/pi-tasks`, `@aliou/pi-processes`. Claude Code users get these capabilities from the harness and do not need the Pi extensions.

### Connecting context7 (MCP)

`pi-mcp-adapter` is only the bridge — context7 itself is a hosted MCP server you register once with an API key:

1. Sign up at <https://context7.com/> and create an API key (dashboard → API Keys).
2. Add it to `~/.pi/agent/mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp",
      "headers": { "CONTEXT7_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

`pi-mcp-adapter` picks this file up automatically (it also supports `${CONTEXT7_API_KEY}` interpolation if you'd rather keep the key in an env var). The hosted server requires the key — without it the tools won't work.

**Stuck on the JSON?** Ask the agent — it can create or edit `~/.pi/agent/mcp.json` for you once you paste in your API key.

## Two Kinds of Skills

| Kind | Skills | Use for |
|------|--------|---------|
| **Chained** (`pocket-*`) | pocket-pitching · pocket-grinding · pocket-planning · pocket-structuring · pocket-development · pocket-closing | Real features, non-trivial work. Each stage hands off to the next, carrying spec/plan/criteria forward. |
| **Standalone** (lighter, daily use) | bug-hunting · hotfix · brand-design · structured-research · pocket-help · pocket-init · create-pr | Everyday work that does NOT need the full pipeline. Single-purpose, no handoff chain. |

The `pocket-*` prefix marks a skill as part of the chained pipeline (`pocket-init` and `pocket-help` are the exceptions — standalone setup/routing helpers). `bug-hunting`, `hotfix`, `brand-design`, and `structured-research` are deliberately *not* prefixed — they stand alone and are the right, lighter choice for most day-to-day tasks. `create-pr` is the Pocket Enterprise PR recorder (see below).

## Router — Which Skill Right Now?

Match your situation to one skill. Open only that skill.

| Your situation | Skill | Kind |
|----------------|-------|------|
| Rough idea, no clear problem yet — need to explore | `pocket-pitching` | chained |
| Clear problem — need a spec + acceptance criteria | `pocket-grinding` | chained |
| Approved spec — need a TDD execution plan | `pocket-planning` | chained |
| Execution plan ready — sequence/phase it | `pocket-structuring` | chained |
| Plan or phase file ready — execute task-by-task (in-loop audit + phase-level pass included) | `pocket-development` | chained |
| Phase-level pass done, all verdicts pass — close out the plan | `pocket-closing` | chained |
| A bug, a failure, or "audit this code" | `bug-hunting` | standalone |
| Small-to-medium change, full pipeline is overkill | `hotfix` | standalone |
| Design system / brand identity / UI tokens | `brand-design` | standalone |
| An assumption to validate before it enters planning | `structured-research` | standalone |
| "What is Pocket / which skill / how does this flow?" | `pocket-help` (you are here) | standalone |
| New/existing repo needs Pocket set up (CLAUDE.md, enterprise) | `pocket-init` | standalone |
| Enterprise phase done — open the linked PR | `create-pr` | standalone (enterprise) |

**Routing rules of thumb:**
- Don't know if the problem is even well-formed? → `pocket-pitching`.
- Problem is clear but it's a real feature? → start at `pocket-grinding`.
- It's a quick, well-understood change? → `hotfix` (not the pipeline).
- Something is broken? → `bug-hunting` (not the pipeline).
- Holding an unverified assumption? → `structured-research` (validate it before it enters planning).
- Already have an approved spec? → skip pitching/grinding, start at `pocket-planning`.

## The End-to-End Flow (chained pipeline)

```
rough idea
   │  pocket-pitching        explore → pitch doc (2–3 directions)        [user picks next]
   ▼
clear problem
   │  pocket-grinding        BDD discovery → spec + GWT acceptance       [auto-invokes planning]
   ▼
approved spec
   │  pocket-planning        TDD plan → Pocket Packets + test intent    [validates, routes to structuring]
   ▼
execution plan
   │  pocket-structuring     decomposes into index + per-task files      [hands phases one at a time]
   ▼
plan / phase file
   │  pocket-development      delegate task-by-task via subagents;        [emits PHASE_COMPLETE]
   │                          in-loop audit per task (mechanical gate +
   │                          read-only auditor) + phase-level pass once
   │                          every task is DONE, incl. append-only fixes
   │                          for any REVIEW_FAIL finding
   ▼
phase-level pass written (all pass)
   │  pocket-closing         User invokes · gate · log close [CLOSED / PHASE_ADVANCED / CLOSE_BLOCKED]
   ▼
plan closed (fix findings & loop phases until every phase is DONE)
```

**Handoff facts that matter (so you don't double-invoke or stall):**
- `pocket-grinding` **auto-invokes** `pocket-planning` after you approve the spec.
- `pocket-planning`, after you approve the plan (**plan approval** — authorize derived artifacts), validates it with `structure --dry-run` and routes all plans to `pocket-structuring`.
- `pocket-structuring` decomposes all plans into an execution index (`execution-plan/index.md`) + per-task files (`execution-plan/tasks/T*-*.md`), generating phase manifests (`execution-plan/phase-N.md`) only when `phaseCount > 1`, then asks for **execution approval** before handing off phases one at a time.
- `pocket-development` runs the review in-loop — it does **NOT** wait for a separate user-triggered reviewer. After every task's implementer reports DONE it runs the in-loop audit (mechanical gate, then a read-only auditor subagent covering spec compliance and code quality). Once all tasks in the phase are DONE, it dispatches a phase-level pass over the whole phase and, for any `REVIEW_FAIL` finding, delegates and records an append-only fix as part of that same flow (main agent stays Delegator + Auditor — never writes the fix itself). A passing run sets the phase to `REVIEW` and emits a `PHASE_COMPLETE` handoff naming `pocket-closing` as the user-triggered next step — pocket-closing is always invoked directly by the user, never auto-chained. pocket-development does **NOT** advance a phase to `DONE` or close the plan (closing owns `REVIEW → DONE` and `log close`).
- `pocket-pitching` does **not** auto-chain — it presents handoff options and you choose whether to start `pocket-grinding`.

> `pocket-closing` is the terminal stage: it reconciles review verdicts, advances `REVIEW → DONE`, runs `log close`, and writes a `closeout.md`. Without it a fully reviewed plan stays in `IN_PROGRESS`/`REVIEW` limbo. Any `REVIEW_FAIL`/`REVIEW_BLOCKED` or unreviewed task makes it `CLOSE_BLOCKED` — resolve it through `pocket-development`'s phase-level pass before re-closing.

For the flow walked stage-by-stage with a worked example and every gate, load `references/end-to-end-flow.md`.

## Pocket Enterprise (opt-in team layer)

The pipeline above is local-first. With **Pocket Enterprise** enabled (`/pocketto:pocket-init` or `pocketto-pi mode init`), the same stages also leave a GitHub trace — nothing else changes:

- `pocket-grinding` → creates a GitHub issue from the approved spec (summary + full spec in a collapsible section).
- `pocket-development` → offers `/pocketto:create-pr` at PHASE_COMPLETE, posts the phase-level pass's verdicts as a PR summary comment + inline findings (reconciled, no duplicates), and syncs a task-checklist comment to the issue.
- `create-pr` → opens the phase PR on the current branch, linked to the issue (`refs`/`closes`).
- `pocket-closing` → posts the closeout comment to the issue; with `require_approval: true` it blocks the close until the PR is APPROVED. Pocket never merges PRs or closes issues — humans do.

Detection is fail-closed: without a valid `## Pocket Enterprise` block in `AGENTS.md`/`CLAUDE.md`, every skill behaves exactly as local mode with **zero** GitHub calls.

## When Pocket Beats a Lighter Flow

If you already use Superpowers-style skills (or just let one agent code straight through), Pocket is **stronger** when the work has any of these:

- **High ambiguity** — the problem isn't crisp yet (pitching/grinding force clarity first).
- **Multi-step build** — many tasks across files/layers (planning + development bound each one).
- **BDD/TDD discipline required** — acceptance criteria and test-first are non-negotiable.
- **Subagent delegation** — work spread across implementers needs contracts, not vibes.
- **Phase gates** — long builds drift; phase boundaries are checkpoints.
- **Context preservation** — phasing + summaries stop the thread from blowing its window.
- **Auditable execution** — every task has evidence (commits, tests, review reports).

Pocket is **overkill** when the change is small and well-understood. Then:
- known bug / failure → `bug-hunting`
- quick small-to-medium change → `hotfix`
- just UI tokens / a brand → `brand-design`
- an unverified assumption to validate → `structured-research`

For the full comparison and a "which do I reach for?" decision guide, load `references/pocket-vs-superpowers.md`.

## Context Budget Guidance

This skill exists to protect your context window. Follow this order:

1. **Start here** (`pocket-help`) to orient and route.
2. **Load one skill** — the single skill for your current stage. Not the whole set.
3. **Load that skill's references on demand** — each skill lists Reference Triggers; pull a reference only when its step says to.

Reading every `pocket-*` SKILL.md up front (≈2,800 lines combined) is exactly the waste this skill prevents.

## Reference Triggers

| Reference | When to Load |
|-----------|--------------|
| `references/skill-map.md` | Need a one-block summary of each skill — what it does, its input, its output/handoff, when to use vs skip |
| `references/end-to-end-flow.md` | Need the full pipeline walked stage-by-stage with a worked example and gates |
| `references/pocket-vs-superpowers.md` | Deciding between Pocket and a lighter Superpowers-style / standalone flow |
