---
name: cdev-monorepo
description: Use when the user invokes /cdev-monorepo (with or without arguments) in a conditioned multi-repo workspace (it has workspace/repos.yaml and a global docs/develop/) — autonomously executes the active SYSTEM_BATCH coordinating the affected repos' local CDevs in parallel, reconciles states and closes batches with global verification.
---

# CDev Monorepo — orchestrating loop

Global equivalent of `/cdev` for a multi-repo workspace conditioned by `bootstrap-monorepo`.
**Elevated autonomy** mandate: work until a real blockage, never stop to ask "now what?". The
workspace is the memory: global `SPRINTS.md` = plan · global `AGENT_PROGRESS.md` = handoff ·
`state.lock.json` = snapshot · local state lives in each repo.

Invocation: `/cdev-monorepo` (resume) · `/cdev-monorepo sprint 02` · `/cdev-monorepo batch SYS-02-B01`.

## The invariant that protects the whole mechanism

```text
Global work must not break local continuity.
Local work must not break global visibility.
```

After a workspace session, `cd repo && /cdev` must be able to continue normally. After
independent work inside a repo, the next workspace session **detects and reconciles** that
progress.

## Start + reconciliation (every invocation)

1. Read in order: the global guide (`AGENTS.md`) → `docs/develop/AGENT_EXECUTION_PROTOCOL.md` →
   `SPRINTS.md` → `AGENT_PROGRESS.md` (last entry) → `workspace/repos.yaml` →
   `repo-graph.yaml` → `state.lock.json`.
2. For each repo **relevant to the active sprint/batch** (don't load repos that don't
   participate): its guide, `SPRINTS.md`, `AGENT_PROGRESS.md`, `git status/branch/log`.
3. Reconcile. **The repo is the source of truth of its local state**: renumbered sprint, batch
   finished outside the workspace, new commits, different branch, local blockage → the
   workspace updates itself; never the other way around. Divergence (workspace says DONE, repo
   says IN_PROGRESS) → the repo wins. The workspace never falsifies local state to square its
   own plan. Reconciliation covers the workspace's **own older statements** too: anything it
   asserts about a child (registry fields, snapshot values, stale blocked notes) is re-derived
   on read or checked by the verification script — never trusted on age.

## Loop (repeat until a real blockage)

1. **Select**: first `READY`/`IN_PROGRESS` SYSTEM_BATCH of the `ACTIVE` SYSTEM Sprint — and
   every other one the DAG makes runnable now (wave execution, not batch by batch).
   If a batch is `PLANNED` (unresolved references or sync points) → invoke the
   `cdev-monorepo-planner` skill before executing it.
2. **Resolve references**: every required local reference exists in the repo's `SPRINTS.md`,
   with valid numbering that respects the local sequence and its declared `Wait-for` (the
   planner's sync artifacts). Broken reference → repair via planner, don't improvise.
3. **Build the DAG** of the batch/wave from its references' `depends_on` (only the batch's
   references; unreferenced repos do not appear). A cycle in the DAG = planning error: stop
   that batch and report it, don't break the tie by eye.
4. **Execute in parallel per repo**: dispatch one `monorepo-repo-runner` agent per runnable
   reference, **in parallel only when they belong to different repos**; **a single runner per
   repo, always**. Two levels of parallelism, and only two:
   - **Across repos**: references with no mutual dependency run at once (DAG waves).
   - **Inside the repo**: batches are ALWAYS sequential (local order is sacred; never two
     batches of the same repo at once). What may be parallelized inside a batch are
     **heterogeneous tasks via the local cdev's subagents**: e.g. one subagent investigating
     read-only in the producer repo's working tree the real endpoints, another inventorying
     the repo's own reusable components, and the main agent building — which at integration
     time consumes the investigator's report, not its imagination. Functional testing or
     external-source research follows the same pattern. The decision to create those subagents
     belongs to the local `/cdev`; the workspace does not hand out that work.
   - **Self-blocking guardrail** (applies to every subagent and the main agent): no cross-repo
     endpoint, field, type or structure is integrated without being confirmed by a `Wait-for`
     artifact, a workspace contract, or real code read from the producer repo. Confirmation
     missing → wait or rotate task; inventing it "to make progress" is forbidden. Investigator
     subagents in neighbouring repos are **read-only**: writing into another repo remains an
     absolute gate.
   Dispatch rules:
   - The runner ALWAYS executes **the repo's own `/cdev`** scoped to the reference — it never
     implements on its own authority.
   - The runner's prompt includes: reference (local sprint/batch), `system_batch`, applicable
     contract, its `Wait-for` (which artifact to look for, at which path of which repo) and
     the branch policy (§ below).
   - Runner returning `WAITING` (its Wait-for does not exist yet): reassign that slot to
     another runnable reference from another repo and retry the waiting one when its producer
     closes — never leave the slot idle if runnable work exists (blocked-but-not-idle here
     too).
5. **Collect evidence** as each runner finishes (don't wait for the whole wave to record):
   status/branch/SHA/verification per reference → global `AGENT_PROGRESS.md` +
   `state.lock.json` + `workspace/snapshots/` if applicable.
6. **Verify globally** with `monorepo-system-tester` at the level the batch declares
   (L0 local evidence · L1 contracts · L2 partial integration · L3 end-to-end). A single-repo
   batch with locally demonstrable acceptance → L0, no artificial cross-repo tests.
   **The wave must quiesce first**: runtime verification (L2/L3) never runs while any runner
   is still moving branches in a participating repo — cross-repo parallelism and system-level
   runtime verification do not compose. Verify between waves, or give runners isolated
   working copies.
7. **Close**:
   ```text
   SYSTEM_BATCH DONE = ALL(required references == DONE) AND global acceptance == PASS
   ```
   Unreferenced repos do not participate, do not block, are not opened "just in case".
8. **Auto-advance**: next runnable wave. System sprint complete → global report, Sprint
   `DONE`, promote the next `PENDING`→`ACTIVE` if applicable, continue. The global report
   **aggregates verification debt**: it sums the batches closed as references-done-but-system-
   verification-blocked and shows the total — each such closure is individually honest, but
   their sum is a plan that reads finished over a system never exercised end to end, and that
   debt must be visible without reading every entry. Plan exhausted →
   invoke `cdev-monorepo-planner` in gap-analysis mode and leave the result as `PROPOSAL` for
   human ratification; meanwhile execute ungated global work.

## Cross-repo synchronization (pull, not push — and never mock)

- Every producer→consumer dependency is satisfied with an **artifact on disk** (the producer
  batch's technical report, path declared by the planner in the consuming reference's
  `Wait-for`). The producer publishes it as part of its acceptance; the consumer **goes
  looking for it** in the producer repo's working tree and reads it before integrating.
- Consumer without its artifact: **it does not mock the other repo's contract** to make
  progress nor fabricates integration evidence — it returns `WAITING` and the orchestrator
  reschedules it. (Unit-test stubs internal to the repo remain legitimate; what is forbidden
  is faking the cross-repo integration.)
- Communication between agents ALWAYS goes through disk (repos + workspace), never through
  conversational memory: any runner may die and resume by reading the repo.

## Branches and push (workspace policy)

- **Derivation**: each repo's first working branch within a SYSTEM Sprint is created **from
  that repo's `develop`**; subsequent batches chain per the local CDev's convention (typical:
  new branch from the previous batch's branch). The workspace does not redefine local branch
  names.
- **Push: never automatic.** On closing the SYSTEM Sprint, pushing the resulting branches is
  the human's act. If the user explicitly asks to "push", only the corresponding **working
  branch** is pushed — never `develop`/`main`, never with `--force`.
- Merge/PR/deploy: always a human gate.

## Blocked-but-not-idle (global)

Reference `BLOCKED` → SYSTEM_BATCH `BLOCKED` with reason + the minimum decision the human must
make. Continue with: another independent reference of the same batch → another SYSTEM_BATCH
with no dependency → other ungated global work. Never mark blocked work as finished.

## It only stops when

- No ungated global work remains — say which approvals would unblock what.
- A human gate blocks and everything depends on it.
- Absent product: **inventing requirements is forbidden**; open question in DECISIONS.
- Quota limit: update `AGENT_PROGRESS.md` + `state.lock.json`, commit the workspace, exit
  cleanly. Resumption picks up from the workspace, not from conversational memory.

## Safety gates (never elevated; the strictest always wins)

Each child repo's gates prevail intact — this skill never reduces them. A historical decision
documented in a repo ("authorized path", old DECISIONS) NEVER counts as a live approval of a
gate in the current session: the gate requires present human authorization. Additionally, at
workspace level: push to any repo's `main`/`develop` · merge · deploy · remote
migrations/schema · live secrets · real payments · history rewriting · data deletion.
Preparing yes (drafts, commands, manifests); executing no. The workspace also may not: alter
local numbering, skip local sprints out of system haste, mark undemonstrated work DONE, or
turn a local change into a global one without evidence.
