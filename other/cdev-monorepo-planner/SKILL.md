---
name: cdev-monorepo-planner
description: Use when cross-repo work must be planned in a CDev Monorepo workspace — turning a system objective into SYSTEM_BATCHes with real local references, or analyzing all repos to find gaps (half-integrated features, broken contracts, pending parity) and proposing the next SYSTEM Sprints. Also when the user invokes /cdev-monorepo-planner or asks "plan the monorepo", "what's left to integrate", "planifica el monorepo", "qué falta por integrar".
---

# CDev Monorepo Planner

Planning brain of the workspace. **Never implements code.** Two modes depending on what is
asked; without a clear argument, run both: gap analysis first, then materialize what is approved.

## Mode 1 — Materialize an objective (objective → executable SYSTEM_BATCH)

**Before writing each SYSTEM_BATCH, close its open decisions with the human.** The rule lives
in one place — § "Closing open decisions" of the `cdev-planner` skill: resolve this skill's
base directory to its real path, read `../cdev-planner/SKILL.md`, and apply that section per
SYSTEM_BATCH (including its no-human branch). System-level sources of open decisions, beyond
that section's: which repos participate and which explicitly do not, the terms of a
cross-repo contract, the sync-point artifact, implementation and deploy order, the
verification level.

1. **Define the batch**: `SYS-<sprint>-B<n>` in the global `SPRINTS.md` with an observable
   objective, affected repos (and explicitly the non-affected ones if that clarifies scope),
   global acceptance and verification level L0–L3. It is born `PLANNED`.
2. **Read the local CDev of each affected repo** (`SPRINTS.md`, `AGENT_PROGRESS.md`, protocol):
   active sprint, existing batches, blockages, order. **Absolute respect for local order**:
   - existing work that already matches → **adopt** the reference, don't duplicate;
   - fits the active sprint → new batch at the end of that sprint;
   - belongs to a later phase → batch in the next `PENDING` local sprint (without forcing it
     to `ACTIVE` or renumbering anything).
3. **Write bidirectional references**:
   - workspace: repo / local sprint / local batch / required / depends_on;
   - repo: `System Reference: SYS-XX-BXX` in the local batch + note in its `AGENT_PROGRESS.md`.
   The repo must be able to continue alone, without the workspace open.
4. **Cross-repo contract** if the batch touches an interface between repos:
   `workspace/contracts/SYS-XX-BXX.md` (objective, repos, API/data contract, compatibility,
   implementation order, per-repo and global acceptance, deploy order). Copy/extract into the
   repo's `docs/develop/external-contracts/` when local independence needs it.
5. **DAG**: `depends_on` between the batch's references (only the batch's own). Producer before
   consumer (typical: backend exposes → frontend consumes).
6. **Sync points (mandatory on every producer→consumer dependency)**: fix the **concrete
   artifact** that materializes the handoff — a technical report the producer batch publishes
   as part of its acceptance (use the report convention the producer repo already has; if it
   has none, `docs/develop/reports/<sprint>-<batch>.md`). Write in the consuming reference the
   line `Wait-for: <producer-repo>/<report-path>`: during execution, the consuming agent
   **goes looking for** that file (pull, not notification) and waits/rotates if it does not
   exist — that is how integration happens without mocking the other repo's contract. Without
   a declared sync point, a cross-repo dependency is not planned.
7. **Promote to `READY`** only when the batch's open decisions are closed, every required
   reference exists, respects the local
   sequence, has sufficient acceptance and its sync points declared.

Two independent numberings: SYSTEM Sprint/Batch ≠ local sprint/batch. Never equate them, never
force every repo to participate, never create mirror local sprints.

## Mode 2 — Gap analysis (find what to do and what is left to integrate)

Sweep the workspace + registered repos and produce a report with actionable candidates:

1. **Half-done integration**: features DONE in one repo whose consumer does not consume them
   yet (backend sprint reports vs the frontend's real queries; exposed endpoints without UI;
   UI waiting for a non-existent contract).
2. **Contracts**: divergence between the producer's schema/API and consumers' types/queries;
   contracts in `workspace/contracts/` not reflected in repos; breaking changes without an
   adoption batch.
3. **CDev state**: repos `CDEV_PARTIAL`/`NOT_CONDITIONED`, repos with no `ACTIVE` sprint
   (plan exhausted — natural candidate for the next SYSTEM Sprint), old local blockages,
   unreconciled workspace↔repo divergences.
4. **Graph domains**: for each domain in `repo-graph.yaml`, are the domain's repos at the same
   functional level? Asymmetries = candidates.
5. **Coordination debt**: global `BLOCKED` batches with a pending human decision, outdated
   snapshots, global verification never run.

Output: table candidate → repos → evidence → proposal (draft SYSTEM_BATCH). Approved ones
enter the global `SPRINTS.md` as `PROPOSAL`/`PLANNED` via Mode 1. **Findings not derivable
from documentary evidence are not invented**: open question in `DECISIONS.md`.

## Rules

- The local source of truth is the repo; the planner reads, references and proposes — it does
  not mark local states or execute implementation work.
- Every finding with evidence (file/line/commit), not impressions.
- The domain graph suggests impact; actual participation is fixed by each batch.
- Record planning decisions in the global `DECISIONS.md`, dated.
