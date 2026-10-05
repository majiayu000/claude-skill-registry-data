---
name: code-fleet
description: Orchestrate a DAG-gated fleet of Claude Code workers across isolated git worktrees, running each dependency wave as one native Workflow with parallel Claude review lenses, checkpoint bundles, seam gates, and final PR review. Use when the user asks to orchestrate many coding tasks, run a fleet, parallelize implementation safely, coordinate workers, review/merge multiple worktrees, or execute an end-to-end multi-agent coding run.
---

# CodeFleet

You are the **Orchestrator**: one coordinating Claude Code instance that turns a
goal into task nodes, builds a dependency graph, gets user approval, runs each
ready set as a single native Workflow, verifies checkpoints, integrates waves,
and ships a seam-reviewed release branch.

This skill exists to manage many related coding tasks at once without pretending
that "many worktrees" automatically means "safe parallelism."

## Two Layers (read this first)

The orchestrator is a **hybrid of two layers that compose; neither replaces the
other.**

- **The skill is the cross-process scheduler** — policy and governance. It owns
  decomposition into a DAG, thought-level calibration, the user-approval gate,
  wave integration, the global seam gate, and `/review`. It holds the run across
  process boundaries via `.orchestrator/fleet.json`.
- **Native Workflows are the in-process executor** — per-wave fan-out. Each wave
  (one ready set) runs as exactly one Workflow call with enforced concurrency,
  journaling, and resume.

**The load-bearing reason the skill still exists:** a Workflow runs to
completion with **no mid-run user input**. Therefore the mandatory
**DAG-approval gate** — and every later human gate — **must live in the skill
loop between per-wave Workflow calls.** It cannot live inside a workflow script.
The skill governs the boundaries; the Workflow executes a wave between them.

Two further consequences of the executor's sandbox, baked in throughout:

- Workflow scripts are plain JS with **no filesystem access** and **no
  wall-clock or randomness builtins** (those break resume). A wave Workflow
  therefore **returns structured data**; the **skill** writes
  `.orchestrator/fleet.json` and stamps timestamps **after** the wave Workflow
  returns.
- Concurrency is capped (~16 concurrent agents; ~1000-agent lifetime). Neither
  workflow script throttles the inner `parallel()` lens fan-out, so the **skill
  sizes each ready set under that ceiling** before launching the wave (see
  Operating Contract #5 for the explicit budget formula).

## The Wave Workflow (one concrete script)

There is exactly **one** wave Workflow script, and this skill and
`Workflows/RunTaskFleet.md` refer to the same file:

```
workflow-scripts/wave-runner.js
```

`RunTaskFleet.md` describes how the skill invokes it and how to read its return
value; this SKILL.md describes when it runs and what gates surround it. Whenever
either doc says "the wave Workflow," it means `workflow-scripts/wave-runner.js`. The
skill never inlines a second wave script.

## Use This Skill When

- The user asks to "run the fleet", "orchestrate these tasks", "spin up
  workers", "parallelize this implementation", or "merge/review all worker
  branches".
- The work can be decomposed into multiple coding tasks that may have
  dependencies or shared seams.
- The user wants implementation, review, verification, and final merge handled
  as one coordinated workflow.

## Do Not Use This Skill When

- The request is a single small edit, code explanation, or one-off review.
- The user only wants a planning discussion and has not asked to execute.
- Worktree creation or external side effects would be inappropriate for the
  current repo state.

## Load Order

1. Read [CONTEXT.md](CONTEXT.md) for canonical vocabulary.
2. Select the workflow from the routing table below.
3. Load only the references needed for the current phase.
4. Keep `.orchestrator/fleet.json` as run state once a fleet starts — the skill
   owns this file; wave Workflows only return data for the skill to write.

## Integrated Stack

| System | Role |
| --- | --- |
| Native Workflows | Per-wave execution substrate: runs one ready set as a `pipeline(work, review, fix, verify)` with enforced concurrency, journaling, and resume. The single script is `workflow-scripts/wave-runner.js`. Returns structured data only. |
| Isolation worktree mode | Each worker agent runs in its own fresh git worktree on a named `fleet/<run-id>/task/N-<slug>` branch. Edits stay isolated; the DAG decides what runs together. |
| Claude review lenses | The Phase 2 panel: parallel Claude sub-agents, each carrying **one distinct lens** (correctness, completeness, pattern, edge, security, …), each prompted to **refute**, returning schema-validated findings deduped with provenance. Independence comes from diverse lens briefs, not a second model. |
| Claude sub-agents | Assessment, dependency mapping, codebase Q&A, fixes, behavior verification, design audit, merge support, and the higher-effort **rescue** at the re-review cap. |
| code-review | Final GitHub PR review via `/review`. |

There is no Codex and no second model anywhere in this stack. Any reference file
that still names Codex, cmux, or `codex-companion.mjs` is **stale** and must not
be routed to until it is patched Claude-only (see Workflow Routing).

## Workflow Routing

All routing targets must be **patched Claude-only** before this skill ships. A
target that still names Codex, cmux, or a second model is stale; do not route to
it — patch it first or treat its Codex instructions as non-authoritative.

| Workflow | Trigger | Load | Status |
| --- | --- | --- | --- |
| DependencyGraph | Before every fleet run; map blocking/soft dependencies and waves | [Workflows/DependencyGraph.md](Workflows/DependencyGraph.md) | Claude-only |
| RunTaskFleet | "orchestrate these tasks", "run the fleet", "spin up workers" | [Workflows/RunTaskFleet.md](Workflows/RunTaskFleet.md) | Claude-only (invokes `workflow-scripts/wave-runner.js`) |
| FinalMerge | "merge the worktrees", "combine all tasks", after all waves are integrated | [Workflows/FinalMerge.md](Workflows/FinalMerge.md) | Claude-only |
| DesignAudit | UI/design verification or SOP compliance checks | [Workflows/DesignAudit.md](Workflows/DesignAudit.md) | Claude-only |

## References

| Reference | Load when | Status |
| --- | --- | --- |
| [references/orchestration-principles.md](references/orchestration-principles.md) | Decomposing work, deciding wave order, sizing tasks within the concurrency cap, resolving ambiguity | Claude-only |
| [references/review-verification.md](references/review-verification.md) | Writing worker briefs, composing the Claude lens panel, dispositioning findings, verifying green status | Claude-only — canonical lens/finding schema |
| [references/runtime-commands.md](references/runtime-commands.md) | Driving worktrees, invoking `workflow-scripts/wave-runner.js`, writing the ledger, final PR review | Claude-only |
| [references/examples.md](references/examples.md) | Needing a quick behavioral example | Claude-only |
| [docs/adr/0001-dag-gated-wave-scheduler.md](docs/adr/0001-dag-gated-wave-scheduler.md) | Needing the rationale for DAG-gated waves | Claude-only |

## Architecture

```text
Orchestrator (skill — cross-process scheduler)
  -> decompose goal into task nodes
  -> dependency mapper sub-agent proposes DAG (blocking vs soft edges)
  -> orchestrator arbitrates DAG, waves, checkpoints, seams
  -> assessor sub-agent calibrates each task L1-L4
  -> orchestrator sizes each ready set under the ~16-agent budget   <-- skill
  -> USER APPROVES the graph                         <-- gate (skill only)
  -> for each wave, in dependency order:
       -> run ONE native Workflow (workflow-scripts/wave-runner.js):
            pipeline(work, review, fix, verify), one item per ready-set task,
            isolation worktree mode per worker; returns structured data
       -> skill writes .orchestrator/fleet.json + stamps timestamps
       -> wave integration: git merge one branch at a time, seam check  <-- gate
  -> FinalMerge: global seam gate over all integrated waves             <-- gate
  -> /review on the release PR
```

Each box marked `<-- gate` is a skill-loop step **between** Workflow calls. The
Workflow owns everything inside a wave; the skill owns everything between waves.

## Operating Contract

1. **Graph before workers.** Always run `DependencyGraph` before thought-level
   calibration or any wave Workflow. Show the wave table, blocking edges, soft
   edges, checkpoints, and ledger to the user before execution.
2. **User approval before execution, between every wave.** Do not launch the
   first wave Workflow until the user approves the DAG. Because a Workflow takes
   no mid-run input, every approval and integration gate happens **in the skill
   loop between Workflow calls** — never inside a script.
3. **One wave = one Workflow.** There is no `runWorkflow()` primitive: the agent
   running this skill invokes each ready set by **calling the Workflow tool**
   once — `Workflow({ scriptPath: "workflow-scripts/wave-runner.js", args:
   wavePayload })` (inline-script fallback if `scriptPath` is unavailable; ADR
   0003). The script self-executes via the `args` global and runs a
   `pipeline(work, review, fix, verify)`, one item per task, each worker in
   **isolation worktree mode**. The DAG, not the worktree layout, decides what
   may run in parallel.
4. **Worktrees isolate edits, not meaning.** Every worker gets its own fresh
   worktree on branch `fleet/<run-id>/task/N-<slug>`. A fresh engine worktree
   has **no fetched deps**: every worker brief must run `mix deps.get` before
   `mix compile` or `mix test`. `deps/`, `_build/`, and `mix.lock` are
   gitignored and stay unstaged so wave merges stay clean.
5. **Parallelism is by ready set, within an explicit agent budget.** Only tasks
   with satisfied blocking dependencies run in the same wave. Soft edges may run
   together but create seam obligations. Because **neither workflow script
   throttles the inner `parallel()` lens fan-out**, the skill must size each
   ready set so the peak concurrent agent count stays under the ~16 ceiling.
   Budget the wave as:

   ```
   wave_agents = Σ over ready-set tasks of
       ( panel_lenses(level)        # L1=1, L2=3, L3=5, L4=8
       + design_lens(task)          # +1 if UI/design task (lens D), else 0
       + acj_agents(level)          # +3 at L4 (Advocate, Critic, Judge), else 0
       + peak_fixers(task) )        # worst-case concurrent ACCEPT fixers, one per finding
   ```

   If `wave_agents > 16`, the skill **splits the ready set into sub-waves**
   (each its own Workflow call) so no single wave exceeds the cap. The budget is
   recorded per wave in `.orchestrator/fleet.json`.
6. **Checkpoints unblock dependents.** A commit alone is not enough. A blocking
   dependency is satisfied only by a reviewed checkpoint bundle with produced
   contract/artifact, commit SHA, review verdict, verification evidence, and
   known limitations.
7. **The skill owns the ledger; the Workflow returns data.** Workflow scripts
   are plain JS with no filesystem, wall-clock, or randomness. The wave Workflow
   returns structured results; the **skill** writes `.orchestrator/fleet.json`
   and stamps timestamps after the wave returns.
8. **Workers implement; the orchestrator coordinates.** The orchestrator does
   not do task work directly. It decomposes, briefs, launches waves, integrates,
   gates, and arbitrates.
9. **Review is Claude-only, independence from diverse lenses.** The Phase 2
   panel is parallel Claude sub-agents, each carrying one distinct lens and each
   prompted to **refute / be skeptical**. Each lens returns a schema-validated
   record using the canonical lens schema in
   `references/review-verification.md`: `{severity, file, line, finding,
   suggested_fix, lens, refuted}`, where **`refuted: true` means the lens
   actively looked and found nothing in scope** (an explicit "nothing here,"
   not a missing answer). Findings are deduped by `(file, line, finding)` with
   provenance — multi-lens overlap raises confidence. At L4, the
   Advocate-Critic-Judge debate is **three more Claude sub-agents** (Advocate,
   Critic, Judge), not a single judge. At the re-review cap, rescue is a
   **higher-effort Claude sub-agent**, not a second model.
10. **Independent verification gates green.** Worker-says-done is not enough. A
    task reaches `checkpoint_ready` only after worker completion, clean review
    disposition, and **independent verifier evidence reproduced against the
    task's own branch state** — the verifier must observe the same tree the fix
    sub-agents committed to (the worker's worktree / its branch ref **after**
    fixes land), so it never verifies a stale checkout (see
    `references/review-verification.md` for the shared-vs-isolation reconciliation).
11. **Disposition every finding.** Every finding becomes ACCEPT, FIX_LATER, or
    DEFER. Only ACCEPT blocks. FIX_LATER goes to `techdebt.md`. Disposition is
    assigned by the **worker's judgment** (single-lens findings are dispositioned
    with judgment; L4-contested findings are dispositioned by the ACJ Judge
    verdict), and the chosen disposition is written into the finding's
    `disposition` field so the pipeline can act on it deterministically.
12. **Wave integration is one branch at a time.** Merge each ready-set branch
    into the wave integration branch sequentially (no octopus), resolving
    conflicts before the next merge, and verify checkpoints and soft-edge seam
    obligations before unlocking dependents.
13. **FinalMerge is a global seam gate.** Wave integration already combined task
    branches. FinalMerge starts from the latest verified wave integration,
    creates `release/<goal-slug>`, checks cross-wave seams, opens the PR, and
    runs `/review`. It is not the first integration.
14. **The skill owns teardown.** Worktrees persist once they hold a commit and
    are not auto-cleaned. After a branch is merged, the integration/teardown
    phase runs `git worktree remove --force` plus `git branch -D` for it.

## Per-Task Status Vocabulary

The wave Workflow (`workflow-scripts/wave-runner.js`, `toTaskResult`) emits one
of exactly three per-task statuses. The skill, the Phase table, and the
Completion Criteria all use this same enum — there is no separate `green` /
`failed` vocabulary:

| Status | Meaning | Skill action between waves |
| --- | --- | --- |
| `checkpoint_ready` | Worker done, review clean of ACCEPT, verifier PASS reproduced against the branch. The checkpoint bundle is complete. | Eligible to integrate; unblocks dependents. |
| `held` | Did not reach a clean checkpoint within the re-review cap, OR a soft-edge seam obligation is unmet. The bundle is incomplete. | **Hold all dependents** keyed off `status: "held"`. Resolve per the rescue/escalation ladder before integrating. |
| `needs_orchestrator` | The wave hit a condition only the skill can resolve (ambiguity beyond worker scope, conflicting contracts, cap exhausted after rescue). | Pause integration of this task and its dependents; orchestrator arbitrates, then re-waves if needed. |

The hold-dependents logic keys off `held` (and `needs_orchestrator`), **not**
`failed` — the script never emits `failed`. "Green" in prose is a synonym for
`checkpoint_ready` only; never test for a literal `green` or `failed` status.

## Wave-Result Contract (single shape)

The wave Workflow returns one object the skill reads verbatim. There is one
contract; `RunTaskFleet.md` and this doc both use these exact keys.

Per-task entry (from `toTaskResult`):

```jsonc
{
  "task_id": "3",
  "slug": "auth-token-store",
  "branch": "fleet/<run-id>/task/3-auth-token-store",
  "commit": "<sha or null>",           // null unless status is checkpoint_ready. NOT "commit_sha"
  "status": "checkpoint_ready",        // | "held" | "needs_orchestrator"
  "produced_contract": "…",            // the artifact/interface this task exposes
  "known_limitations": ["…"],
  "review": { "verdict": "pass", "rounds": 2, "rescued": false, "findings": [] },
  "verification": { "reproduced": true, "evidence": "…", "ref": "fleet/<run-id>/task/3-auth-token-store" }
}
```

PASS/FAIL is carried by `status` (and `review.verdict`), not a `verdict` key on
`verification`. Wave-level entry: a single top-level `techdebt` array (the script
builds it via `results.flatMap`), each entry:

```jsonc
{
  "task_id": "3",
  "branch": "fleet/<run-id>/task/3-auth-token-store",
  "file": "lib/pixir/auth/token_store.ex",
  "line": 42,
  "finding": "…",
  "lenses": ["S", "E"],                // array; provenance of every lens that raised it
  "disposition": "FIX_LATER",          // FIX_LATER | DEFER (ACCEPT items are fixed, never debt)
  "reason": "…"                        // why it is non-blocking
}
```

The skill, on wave return, appends each `techdebt[]` entry to the repo's
`techdebt.md` using the canonical convention in `references/review-verification.md`
(rendering `lenses` as `(lens: S+E)`), then writes the per-task bundles into
`.orchestrator/fleet.json` and stamps wave timestamps. Do not expect the older
per-task `id` / `produced` / `limitations` / per-task `techdebt` shape; that
contract is retired.

## Execution-Mode Reconciliation (verify against the right tree)

Isolation follows **ADR 0003** (verified live; the `workspace:{mode}` option an
earlier draft used is **inert** — the runtime discards it):

- **Work, fix, rescue** pass the real workflow flag **`isolation: "worktree"`**.
  The runtime gives a fresh worktree on an auto-named branch; the brief then
  `git checkout`s the named branch `fleet/<run-id>/task/N-<slug>` and commits
  there. **Fixes run sequentially** (one branch ≠ two worktrees at once).
- **Review and verify** take **no** isolation flag; the brief reads the
  **committed branch tip** from git (`git diff <base>...<branch>`,
  `git show <branch>:<file>`, or a scratch `git worktree add`). Because fixes are
  *committed*, the gates always see them — never stale state.
- The contract is therefore **uncommitted work is invisible to review/verify**;
  the worker brief says so explicitly.
- Because a fresh checkout also has no deps, every building stage runs
  `mix deps.get` before `mix compile` / `mix test` (Operating Contract #4).
- Isolation worktrees **persist** once committed; the skill removes them at
  integration/teardown (`git worktree remove --force`).

`Workflows/RunTaskFleet.md`, `references/review-verification.md`, and
`workflow-scripts/wave-runner.js` all pin this **same** mechanism; the binding
contract is **ADR 0003** as the script implements it (verified end-to-end live).

## Canonical Phases

| Phase | Owner | Where it runs | Gate |
| --- | --- | --- | --- |
| 0.25 Dependency Graph | Orchestrator + mapper sub-agent | Skill loop | User approves DAG and ledger |
| 0.5 Thought-Level Calibration | Assessor sub-agent | Skill loop | Task level L1-L4 recorded; ready set sized under the agent budget |
| 1 Work | Worker | Inside the wave Workflow | Task implementation committed to its branch |
| 2 Review | Parallel Claude lens sub-agents | Inside the wave Workflow | Lens findings harvested, schema-validated (`refuted` set), deduped with provenance |
| 3 Disposition + Fix | Worker + fix sub-agents | Inside the wave Workflow | Each finding's `disposition` set; ACCEPT fixed on-branch, FIX_LATER logged, DEFER noted |
| 4 Re-review | Claude lens panel (rescue at cap) | Inside the wave Workflow | No remaining ACCEPT within round cap (rescue sub-agent at the cap) |
| 5 Verify | Verifier sub-agent | Inside the wave Workflow | PASS evidence reproduced against the post-fix branch tip |
| Wave Integration | Orchestrator | Skill loop, between Workflow calls | Checkpoints and seam obligations verified; ledger + techdebt written |
| 6 FinalMerge | Merge sub-agent + orchestrator | Skill loop | Release branch reviewed and PR opened |

Phases 1–5 are the per-wave Workflow's `pipeline` stages and run with no human
input. A task that clears Phase 5 returns `status: "checkpoint_ready"`; a task
that cannot returns `held` or `needs_orchestrator`. Everything in the **Skill
loop** column is a gate between Workflow calls.

## Completion Criteria

A fleet run is complete only when:

- `.orchestrator/fleet.json` records the approved graph, waves, the per-wave
  agent budget, per-task statuses (`checkpoint_ready` / `held` /
  `needs_orchestrator`), checkpoints, seam obligations, review rounds,
  verification evidence, and skill-stamped wave timestamps.
- Every task is `checkpoint_ready`; no task remains `held` or
  `needs_orchestrator` (each was resolved, re-waved, or consciously downgraded
  to FIX_LATER with a logged rationale).
- All waves are integrated in order, one branch at a time.
- All blocking checkpoints remain represented in the release branch.
- All seam obligations are resolved or consciously logged.
- The release branch has passed the global seam gate and `/review`.
- Worktrees and their branches have been torn down (`git worktree remove
  --force` + `git branch -D`) after merge.
