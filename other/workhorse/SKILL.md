---
name: workhorse
description: >
  End-to-end disciplined problem resolution ladder: triages complex multi-task or
  wall-of-text intake into an atomic priority queue, establishes ground truth via
  /debug-mantra, engineers the leanest safe solution via /ponytail (reusing and
  extending existing subsystems with zero code sprawl), enforces AGENTS.md, SOP.md,
  and GUIDING PRINCIPLES governance, checks cross-repo CHANGELOG cohesion, stress-tests
  the plan via /consult with Codex and Agy, runs bounded /recon on ambiguous stateful
  targets, proves preservation before irreversible operations, and executes with verified
  runnable checks.
  Trigger on /workhorse, "workhorse", "tackle this", "work through this problem",
  "methodical progress", or when an ambiguous or complex task requires structured,
  governed execution across the full ladder.
metadata:
  argument-hint: "[task, PR, issue, wall-of-text, or problem description]"
---

# /workhorse — Governed End-to-End Problem Resolution Ladder

`workhorse` is a 7-rung execution ladder (Rung 0 + Rungs 1–6) that transforms ambiguous symptoms, wall-of-text transcripts, multi-task dumps, complex bugs, PR reviews, or feature requests into clean, minimal, cross-model-verified, durable solutions.

It coordinates existing specialized skills (`debug-mantra`, `recon`, `ponytail`, `consult`, `relay`) and repository governance rules rather than creating duplicate procedural abstractions.

---

## Recite this — verbatim, as the first thing in your first response

> **Workhorse Discipline:**
> 1. **Triage & rank intake (Rung 0).** Deconstruct walls of text, multi-symptom dumps, or LLM transcripts into an atomic priority list (P0 → P1 → P2). Hold the active queue in the session plan; record incidental out-of-scope findings in root `PARKED/`, then promote selected items through the repo's formal intake.
> 2. **Establish ground truth on current item (Rung 1).** For the top priority item, inspect raw artifacts and live state directly, capture a deterministic repro, trace fail paths end-to-end, and run disproofs first before theorizing.
> 3. **Design least-mechanism & check governance (Rungs 2–3).** Apply `/ponytail` (YAGNI, standard library first, shortest diff); strictly extend existing subsystems with zero code sprawl or duplicate write paths, complying with `AGENTS.md`/`SOP.md`.
> 4. **Stress-test via cross-model consensus (Rung 4).** Fan out the plan to independent advisors (Codex + Agy via `/consult`), surface technical disagreements without averaging, and resolve all blocking feedback.
> 5. **Prove preservation, execute & advance queue (Rungs 5–6).** Classify reversibility (`Easy`/`Costly`/`One-way door`), prove preservation invariants, apply minimal diff, verify against runnable checks, and loop back to the next item until the queue is clear.
>
> **Overall Goal:** Complete triage queue resolved serially — each item root-cause proven, simplest architecture validated across independent models, and solution executed with zero code sprawl and verified preservation.

Then begin work. When `/workhorse` is the active orchestrating skill, this recital precedes any subordinate skill invocations; subordinate skills (`/debug-mantra`, `/ponytail`, etc.) are then loaded and followed for their mechanics without duplicating conflicting recitals.

---

## The 7-Rung Ladder

```text
0. Intake Triage & Queue           ──► Deconstruct wall-of-text / multi-task dump; hold active queue, park incidental findings at root, promote selected work into formal intake
1. Ground Truth & Diagnostics  (/debug-mantra)  ──► Reproduce raw artifact, trace paths, falsify hypotheses
2. Least-Mechanism Design      (/ponytail)      ──► YAGNI, stdlib first, ZERO duplicate subsystems, minimal diff
3. Governance & Cohesion Gate                   ──► AGENTS.md, SOP.md, GUIDING-PRINCIPLES.md, CHANGELOG parity
4. Cross-Model Consensus       (/consult)       ──► Parallel fan-out (Codex + Agy), reconcile disagreements
5. Preservation & Irreversibility Gate          ──► Inventory state, prove preservation, establish rollback or confirm loss
6. Governed Execution & Verification            ──► Apply minimal diff, execute runnable checks, verify done -> loop to next
```

---

## Rung 0: Intake Triage & Queue Decomposition

When `/workhorse` is invoked on a large or ambiguous problem, intake typically arrives in one of two forms:
- **Human operator task dump:** A list or paragraph of multiple interrelated tasks, bug reports, or feature requests.
- **Agent transcript / wall of text:** A verbose diagnostic dump, subagent report, or prior LLM reasoning trace.

**Triage Protocol:**
1. **Atomic Decomposition:** Extract individual, falsifiable items from the dump. Do not attempt a single omnibus fix for multiple disjoint problems.
2. **Severity/Priority Ranking:** Order the items (P0 critical / blockers → P1 core fixes → P2 polish / optimizations).
3. **Queue Segmentation:**
   - **Active Session Queue:** Hold the immediate in-flight items (Top 1–3) in the active session plan / scratchpad.
   - **Incidental Findings (`PARKED/` first):** For a finding outside the current task, check for an existing record, then write a short sourced item under `<repo-root>/PARKED/` when that folder is part of the repository's governance. Do not invent the folder in another repo or open an issue merely to park the finding; follow that repo's intake policy. During triage here, promote selected work through structured intake (`PROJECT/1-INBOX/GH-<NUM>-<topic>.md` plus RELEASES roadmap); mark the PARKED item with the promoted issue/doc link. Preserve one execution record and do not duplicate a canonical plan. Work required to finish the current task stays in the active queue.
4. **Serial Execution Loop:** Select the highest-priority item from the active queue and advance it through Rungs 1–6. Upon completion, advance to the next item in the queue until all active items are resolved.

---

## Rung 1: Ground Truth & Diagnostics (`/debug-mantra`)

Establish primitive ground truth before theorizing or proposing any changes. Load and follow `/debug-mantra` for detailed diagnostic mechanics.

1. **First is reproducibility / raw artifact inspection:**
   - For a failure/bug: capture a fast, deterministic runnable repro (failing test, curl, CLI run).
   - For an attribution or architecture question: inspect the raw object (database row, message payload, exact file lines) before assuming. Screenshots, rendered views, and memory are **hypothesis-zero**, not axioms.
2. **Know the fail path:**
   - Trace the execution path end-to-end. Enumerate all controlling knobs (configs, env vars, branch conditions, concurrency).
   - Flip one axis at a time in the differential.
3. **Question your hypothesis (Disproof First):**
   - Generate 2–3 ranked hypotheses. Identify the cleanest **disproof** for each.
   - Run the disproof first: if the disproof succeeds (falsifying the hypothesis), discard that hypothesis immediately to avoid chasing phantoms.
4. **Every run is a breadcrumb:**
   - Maintain a running session ledger of observations, probes, and ruled-out paths.

*When the target is a plan, PR, or architecture (Plan Pivot):*
- Measure ground truth at plan time (re-run live counts and file:lines; do not cite remembered state).
- Trace the exact path being modified across all callers before proposing modifications.
- Falsify acceptance criteria (specify how each criterion fails and where red-control evidence lands).
- Maintain a recon ledger against what has already shipped.

---

## Rung 2: Least-Mechanism Architecture (`/ponytail`)

Channel a pragmatic senior engineer: build the simplest, shortest, most durable mechanism that satisfies the requirement.

1. **The Ponytail Rungs:**
   - *Rung 1:* Does this added code/machinery need to exist at all? (YAGNI).
   - *Rung 2:* Standard library does it? Use it.
   - *Rung 3:* Native platform/framework feature covers it? Use it.
   - *Rung 4:* Already-installed dependency solves it? Use it. Never add dependencies for what a few lines can do.
   - *Rung 5:* Can it be a small focused diff? Shortest working diff wins.
2. **The Subsystem Reuse Law:**
   - **Do not invent new modules, helper utilities, or parallel execution paths.**
   - Audit existing modules in `src/rebalance/lib/`, `XYZ-forge/utils/`, etc., and extend them logically.
   - Extending an existing abstraction beats standing up a parallel, siloed system that will silently drift.
3. **Deliberate Shortcuts & Runnable Checks:**
   - Mark deliberate minimal simplifications with an explanatory comment (e.g. `// ponytail: sqlite single-thread, revisit if throughput exceeds threshold`).
   - Every non-trivial change leaves behind **one runnable check** (an assert-based check, unit test, or integration probe).

---

## Rung 3: Governance & Cross-Repo Cohesion

Validate that the proposed minimal solution complies with the repository's foundational rules and history.

1. **`AGENTS.md` Alignment:**
   - Respect single entry points (e.g. orchestrator dispatch chains in `index_ops.py` or `releases_app.py`).
   - Honor disabled or paused subsystems (never silently revive paused components).
   - Adhere to containment and worktree safety rules.
2. **`SOP.md` Alignment:**
   - Any performance or efficacy claim must be backed by measurable, reproducible test evidence.
   - Follow the issue-first and capture-doc protocols where required.
3. **`GUIDING-PRINCIPLES.md` Alignment:**
   - Check the North Star: Durable, Reversible, DRY.
   - Single-writer per contract/table.
   - State Complexity: Introduce an FSM only when state complexity exceeds approximately 4 distinct states with non-trivial transitions (per SWE rubric & repo governance); otherwise use lean enums, flags, or explicit conditions.
4. **`CHANGELOG.md` Check:**
   - Review recent entries in `CHANGELOG.md` across relevant repos (`XYZ-forge`, `rebalanceOS`, etc.).
   - Ensure terms, patterns, and architectural conventions match the active codebase state rather than legacy/superseded patterns.
5. **PDDA & Releases Ledger Intake:**
   - *Tracking Doc:* For non-trivial tasks, confirm a capture doc exists under the applicable lifecycle contract (e.g. `PROJECT/1-INBOX/` with `status: proposed` / `status: draft`, or `PROJECT/2-WORKING/` with `status: active`).
   - *Releases DB / Roadmap:* For repos using the releases ledger, verify the issue is registered in `releases.db` via canonical roadmap commands (`python3 utils/py/releases_app.py roadmap add --issue-num N --issue-url U --title T --created YYYY-MM-DD --doc-path P` with flags per `ROUTER.md:38`). Serial task queueing (`releases jog add`) is a separate optional enqueueing step, not an alternative to roadmap registration.

---

## Rung 4: Cross-Model Consensus (`/consult`)

Stress-test the finalized plan or architecture across independent AI models before touching production code.

1. **Fan-Out (`/consult`):**
   - Load and invoke the `/consult` skill (`skills/1-hourly/consult/SKILL.md`), adhering to its cwd-independent locator and `CONSULT_ROOT` pin.
   - Query **Codex** and **Agy** in parallel in isolated throwaway worktrees. If an advisor is unavailable, handle degraded output per `/consult` instructions.
2. **Reconcile Without Averaging (Surface the Seams):**
   - **TLDR:** 1–2 sentence summary of the reconciled call and confidence level.
   - **Disagreements:** Explicitly list every point where advisors differed, with your adjudication and technical rationale.
   - **Agreements:** Highlight points where both models independently concurred.
   - **Sorted Categories:**
     - **Blocking:** Legitimate risks or defects caught by an advisor; must be addressed before proceeding.
     - **Worth Doing / Optional:** Valid improvements or cleanups to consider.
     - **Skip / Out of Scope:** Ideas noted and explicitly dismissed with rationale.
3. **Finalize the Plan:** Incorporate blocking feedback directly into the execution steps.
   - If an action is not plainly Easy to reverse, include its provisional resolved target,
     reversibility classification, preservation invariant, evidence, and rollback in the consult.
     Rung 5 revalidates them immediately before execution.

---

## Rung 5: Preservation & Irreversibility Gate

Run this rung before **every** mutation. Easy work records the classification in one line. Costly
and One-way-door operations must produce the full preservation proof below; implementation
complexity never lowers this requirement.

1. **Resolve and classify the exact target:** Name the concrete path, ref, record, service, or
   published artifact and classify the action `Easy`, `Costly`, or `One-way door`. If the target is
   unresolved, stop.
2. **Inventory the relevant state carriers:** Record each carrier as `checked`, `not applicable`, or
   `unknown`; any `unknown` blocks mutation. For multiple stale clones or folders, evaluate each
   candidate separately. If its origin, purpose, or relationship to the canonical destination is
   ambiguous, run a bounded `/recon` **for that candidate** and retain the Recon Map as evidence.
3. **State the preservation invariant:** Say exactly what must remain true after the operation and
   what pre-mutation evidence would prove nothing is lost. Match the evidence to the claim:
   - ancestry proves graph reachability;
   - patch equivalence proves change-set similarity;
   - content or semantic evidence proves bytes or behavior;
   - provenance evidence proves origin and attribution.

   None substitutes for another unless it answers the invariant. In particular, a commit not being
   an ancestor is **not** evidence that its content is missing, and a clean diff is not provenance.
4. **Make recovery or permanent loss explicit (Preservation Split):**
   - *Costly Operations:* Require a tested rollback and restoration procedure, explicitly disclosing
     what intervening writes restoration would lose.
   - *One-Way Doors:* A true One-way door has no rollback: state the exact permanent loss, residual
     uncertainty, and resolved target, then obtain fresh, operation-specific operator confirmation.
     Never claim impossible rollback proofs. General permission to work unattended is not confirmation
     of a particular permanent loss.
5. **Durable Operation Identity & Safe Retry (Interrupted-Work Recovery):**
   - Before dispatching any external side-effecting mutation (cloud resource creation, package
     publishing, payment/external API mutation, branch/PR creation, or database mutation), record a
     durable operation identity tuple: `{operation_id, target_arn_or_url, request_fingerprint, idempotency_key}`.
   - **Reconciliation-Before-Retry:** On resuming after a turn crash, process timeout, or dropped
     transport, reuse the recorded operation identity and unchanged request fingerprint, evaluating
     4 distinct remote states:
     1. *Confirmed Success:* Extract existing receipt/output and advance without re-dispatch.
     2. *Authoritative Non-Execution:* Safe to re-dispatch using the original idempotency key and unchanged request fingerprint.
     3. *Pending / In-Flight:* Wait or poll with bounded backoff up to a total reconciliation deadline / attempt cap (e.g., 5 attempts or 300s timeout); do not re-dispatch.
     4. *Unknown / Unavailable Lookup / Expired Deduplication / Deadline Exhausted:* **STOP and escalate to human decision**; automatic replay is strictly forbidden.
   - For targets lacking native idempotency, require natural unique constraints or conditional
     preconditions (e.g. `If-Match`, `version == N`), or stop when non-execution cannot be established.
6. **Stale-Writer Fence:**
   - Local process liveness checks (`kill -0`, PID verification) are strictly scoped to operations
     whose complete write lifetime is demonstrably local (e.g. local repo locks or file mutations).
   - For remote mutations, an elapsed lease or dead local client process does NOT guarantee remote
     completion; a true remote stale-writer fence requires target-enforced monotonic fencing tokens /
     generation numbers that reject stale writers, or else must fall back to the Unknown/Pending stop rule.
7. **Operational Containment (Secrets & Leakage):**
   - If an operational defect exposes credentials, tokens, or sensitive material, immediately execute
     the containment protocol defined in [`ci-debug`](../ci-debug/SKILL.md): Provider-level Revocation/Rotation
     first → Audit Blast Radius in access logs → Preserve Sanitized Evidence → Explicitly authorized
     history scrubbing preserving worktree safety.
8. **Bind and refresh the proof:** Bind evidence to the resolved target and current state. Re-run the
   inventory and preservation checks immediately before mutation; a changed path, ref, worktree,
   process/session, or evidence artifact invalidates the prior proof.

**Repository retirement minimum.** Follow `WORKTREE-SAFETY.md` and `/merge-cleanup`, and require its
report to cover dirty, untracked, and relevant ignored files; all ref namespaces, reflogs,
unreachable objects, and stashes; registered worktrees; nested repositories/submodules and
local-only object stores where applicable; remotes and PR state; hooks/config; and active processes
or sessions. A specialized handoff supplies domain mechanics; it does not waive this rung. Reject
an incomplete report and run `/recon` per preservation-unproven clone before disposition.

---

## Rung 6: Governed Execution & Verification

1. **Execute:** Apply the approved minimal diff to the working branch.
2. **Verify (Semantic Post-Mutation Verification):**
   - Run the runnable check left behind in Rung 2.
   - Execute the repository validation suite (e.g., `validate.sh` in XYZ-forge or `pytest` in rebalanceOS).
   - Verify semantic data content, schema integrity, and state invariants, not merely process exit code `0`.
   - Ensure working tree and tests are green.
   - For destructive work, verify the preservation invariant against the destination or recovery
     artifact. Post-deletion absence alone cannot prove that nothing was lost; the proof must already
     exist from Rung 5.
3. **Ledger Closeout & PDDA Reconciliation:**
   - *Doc Promotion:* If a working doc was created, update frontmatter to `status: completed` and move to `PROJECT/3-COMPLETED/` (or let `wave_reconcile` handle it).
   - *Ledger & Lifecycle Integrity:* Run the applicable canonical repository checks (e.g. `python3 utils/py/releases_app.py check`, `utils/pdda/pdda.sh roadmap-coverage`, `roadmap`, `stale`, `issue-doc-sync`, and `utils/pdda-local-checks.sh`). Inspect reported warnings/findings rather than relying on exit code alone, and ensure all ledger invariants, milestone mappings, and doc sync contracts are satisfied.
4. **Report & Close:**
   - Present a concise completion summary:
     - Root cause & ground truth established (Rung 1).
     - Minimal diff & reused modules (Rung 2).
     - Governance checks passed (Rung 3).
     - Consult reconciliation takeaways (Rung 4).
     - Preservation proof, reversibility classification, and confirmation result (Rung 5).
     - Test execution and verification results (Rung 6).
5. **Orchestrator Re-Entry & Autonomous Loop (Batch Execution):**
   - When `/workhorse` is invoked to diagnose, repair, or resolve an item within a parent orchestrator or multi-item queue (`merge-cleanup`, `jog`, `marathon`, `/10days`):
     - **A repair is an intermediate checkpoint, never the end of the turn.** Do NOT stop after committing a repair to report to the operator or ask what to do next.
     - Record the outcome in the item's attempt record (e.g. `finish --outcome resolved` or `parked`).
     - **Immediately re-invoke the parent orchestrator with `--resume`** (e.g. `python3 skills/2-daily/merge-cleanup/scripts/merge_cleanup.py --primary <primary> --prefix <prefix> --execute --resume`).
     - **Autonomous Loop Invariant:** Repeat the `drive → repair/park → --resume → loop` cycle autonomously until the entire batch is completed, all remaining items are parked/held, or an unresolvable external blocker requires operator escalation.
     - **Anti-Abandonment:** Completing one sub-item repair while other queue items remain unattempted is an active in-flight state, not a milestone to prompt the operator.

---

## Proportional Rigor & Escape Hatches

- **Fast-Track (Trivial + Easy to Reverse):**
  Only when an action is both obvious/mechanical/trivial **and** classified Easy to reverse:
  - Execute Rungs 1, 2, 3, 5, and 6 directly (observe ground truth → shortest diff → verify governance/cohesion → classify Easy reversibility → verify runnable checks).
  - Explicitly skip Rung 4 in one line: `[workhorse fast-track: trivial and Easy to reverse; skipped consult]`.
  - Destructive, externally published, Costly, or One-way-door actions never fast-track, however
    simple the command or small the diff.

- **Handoff to Specialized Skills:**
  - **Stalled Loop / No Goal Movement:** If successive passes only polish supporting machinery,
    reopen settled decisions, or exhaust a review cap **without qualifying movement**, invoke
    `/unstuck` as a blocking interrupt. Cap exhaustion alone is insufficient while evidenced
    correctness findings are still converging. When movement resumes, return here; Rung 5 and Rung 6
    remain mandatory. Do not restart the ladder or add another consult cycle by default.
  - **Iterative 1:1 Co-Authoring:** If Rung 4 reveals that an artifact requires multiple iterative drafting rounds, scaffold via `/relay` and drive via `/relay-xyz` when supported on the repo.
  - **Open-Ended Research / Ideation:** If the task is purely investigatory without code modifications, hand off to `/recon` or `/feynman`.
  - **Ambiguous Stale State:** For each stale clone or folder whose disposition is not already
    proven, run a bounded `/recon` before deciding whether to preserve, merge, archive, or remove it.
  - **Immediate Landing / Fleet Cleanup:** When the task is purely about consolidating branches and
    merging PRs, route to `/merge-cleanup` within Rung 5's preservation contract; reject execution
    when its report leaves a relevant carrier unchecked or unknown.

- **Pushback & Routing Authority:**
  If an operator invokes `/workhorse` on an emergency fire drill (incident rollback) or pure open-ended Q&A:
  - For emergency rollbacks: Apply Fast-Track rules if the operation is trivial and Easy to reverse (executing Rungs 1, 2, 3, 5, 6 while skipping Rung 4 consult); if the action is Costly or One-way door, execute the full ladder including full Rung 5 preservation proof, tested rollback/loss disclosure, and fresh verification before mutating.
  - For pure open-ended Q&A: Route cleanly to research/recon mode (`/recon`).

---

## Operating Rules

- Execute Rung 0 once per intake, then apply Rungs 1–6 in order for each active queue item. Never skip Rung 1 (ground truth), Rung 3 (governance), or Rung 5 (preservation) to jump to Rung 6 (execution).
- Keep communication concise and results-driven.
- If a consult or verification surfaces unexpected failure, loop back to Rung 1 (falsify hypothesis & trace fail path) rather than guessing a patch.
- **Anti-Downgrade Rail:** If an orchestrator or batch sequence was requested (e.g. merging a series of PRs, clearing an issue queue), never report "Done" or "Complete" if the primary workflow was bypassed or truncated (e.g., Phase 0 refused landing and the agent ran `--teardown-only` to prune clones). The agent must either resolve the blocker within authorized scope, or report the exact blocker stopping the sequence; it must never silently redefine the goal to a safe sub-action and declare victory.
- **Tripwire to `/unstuck`:** If successive iterations of a batch loop fail to reduce queue depth, or if tools encounter repeated non-zero exit codes without a qualifying state change, immediately invoke `/unstuck` as a blocking interrupt rather than continuing to narrate or halting.
