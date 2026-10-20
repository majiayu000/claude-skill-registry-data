---
name: swarm-plan
owner: baseline
description: Decompose an approved spec into a dependency-ordered swarm plan — one task per component, each with an explicit write_set. Produces `.claude/state/swarm/<slug>.json` with tasks + waves. The wave scheduler guarantees pairwise-disjoint write_sets within each wave so parallel dispatch is provably conflict-free.
---

# swarm-plan — Phase 5.5: decompose for parallel execution

Invoked after `/approve-direction` and before `/tdd` on any spec that has ≥ `project.json → swarm.min_tasks_worth_swarming` independent components worth parallelizing (default 1, so swarm is the default code-generation route). A spec whose dependency graph exposes no independent component falls through to `/tdd` solo.

**Post-§18 amendment.** Beyond the canonical `.claude/state/swarm/<slug>.json` plan, swarm-plan ALSO emits a runtime sub-track overlay at `.claude/state/swarm/<slug>.jsonl` (JSONL) when the chosen workflow track contains a selector node whose `swarm-implementation` alternate is chosen. The overlay's single line is a transient Track record with `selectable: false`, `track_id: "swarm-runtime-<slug>"`, and `nodes[]` enumerating the swarm-worker dispatches as `can_parallel: true` peers. The harness reloads runtime overlays from `.claude/state/swarm/*.jsonl` at the same time it reads `.claude/workflows.jsonl`, so the runtime Track set is the union. The overlay is deleted by `/archive` along with the rest of the workflow's swarm state.

## Prereqs

1. `.claude/state/spec_approvals/<slug>.approval` exists (spec is human-approved).
2. `docs/specs/<slug>.md` exists and passes `/spec-lint`.
3. `docs/scout/<slug>.md` exists (component → file mapping is its job).

If any prereq is missing, stop and surface what's needed.

## Output contract

`.claude/state/swarm/<slug>.json`:

```json
{
  "slug": "<slug>",
  "spec": "docs/specs/<slug>.md",
  "created_at": <epoch>,
  "status": "planned",
  "tasks": [
    {
      "id": "T-001",
      "title": "<what the task does — one line>",
      "component": "<component id from C4 Component diagram>",
      "acs": ["AC-001", "AC-002"],
      "write_set": ["src/foo/bar.py", "tests/foo/test_bar.py"],
      "read_set": ["src/common/http.py"],
      "depends_on": [],
      "execution": "worker-safe"
    }
  ],
  "waves": null
}
```

You produce `tasks[]`. The validator (`validate.mjs`) computes `waves[]` deterministically via Kahn-with-disjointness.

## Steps

1. **Read upstream**: the spec, the scout report, the approval token. If an older `.claude/state/swarm/<slug>.json` exists, confirm with the user whether to overwrite (replan) or abort.
2. **Extract inputs** from the spec:
   - **Components**: every `Component(id, …)` in the C4 Component diagram (there may be multiple C4 Component diagrams, one per container).
   - **ACs**: every row in the Acceptance criteria table.
   - **Dependency edges**: every `A --> B` in the spec's dependency-graph fence.
   - **Behavior ↔ component mapping**: for each AC, the sequence diagram it references names participants; treat each non-actor, non-external participant as a component this AC touches.
3. **Get file mapping** from the scout report: for each component id, the files that back it. If the spec introduces greenfield components not in the scout, propose new file paths and flag them under a "new_paths" note in your plan summary — they will be accepted by the boundary guard when declared in `write_set`.
4. **Construct tasks** — one per component (per `swarm.granularity: component`):
   - `id`: T-001, T-002, … in stable order.
   - `title`: one-line imperative description.
   - `component`: the C4 component id.
   - `acs`: every AC whose sequence names this component.
   - `write_set`: union of (component files) + (test files covering those ACs). Every file must be explicit; no globs.
   - `read_set`: files this task will consult but not modify. Advisory; not enforced.
   - `depends_on`: for each component B such that this component depends on B (per the dependency graph), include the task id of the task owning B.
   - `execution` (REQUIRED — D5 of swarm-mode-first-run-hardening): classify whether this task is safe to hand to a worker. **`worker-safe`** = pure + fully-specified by the spec (no design decision left, does not touch live shipped code that gate-A/the running harness depends on, depends on no not-yet-shipped API). **`needs-main-context`** = design-laden, touches live shipped code, or depends on an API a sibling task in this plan introduces. `validate.mjs` rejects a plan task whose `execution` is missing or outside `{worker-safe, needs-main-context}`. At `/swarm-dispatch`, only `worker-safe` tasks are spawned as workers; `needs-main-context` tasks are completed in main context. Classifying this UP FRONT (not mid-build) is what keeps the gate-B plan honest — the first real swarm run pulled tasks back to main context mid-wave precisely because the plan assumed every task was worker-safe.
5. **Merge overlapping tasks where forced**:
   - If two tasks share any file AND have no `depends_on` relationship, either introduce a `depends_on` edge (making them sequential across waves) or merge them into one task. Merging is preferred when they're on the same component.
6. **Validate the plan**:
   ```
   node .claude/skills/swarm-plan/validate.mjs docs/specs/<slug>.md .claude/state/swarm/<slug>.json
   ```
   The validator checks: required fields, depends_on references resolve, DAG is acyclic, and assigns `waves[]`. If validation fails, it prints a precise error — fix the plan and re-run.
7. **Surface the plan** to the user as a table:

   ```
   Swarm plan for <slug> — <N> tasks across <M> waves
   
   wave 1:
     T-001  webhook-worker       [AC-001, AC-002]   3 files  worker-safe
     T-003  backoff-policy       [AC-004]           2 files  worker-safe
   wave 2:
     T-002  webhook-retry        [AC-003]           2 files  needs-main-context  (needs T-001)
   ```

   The `execution` column is part of the gate-B review surface — the human approving the swarm at `/approve-swarm` sees which tasks will run as workers vs in main context.

8. Tell the user: "Swarm planned at `.claude/state/swarm/<slug>.json`. Review it, then run `/approve-swarm <slug>`. After approval, run `/swarm-dispatch <slug>`."

## Constraints

- **Never dispatch from this skill.** Planning and execution are separated by a human consent gate (`/approve-swarm`).
- **Every file in a `write_set` must be a concrete path**, not a glob. The boundary guard does string-level membership checks.
- **The `validate.mjs` script is the source of truth for wave assignment.** Do not hand-write `waves[]`.
- **Greenfield files are allowed** in `write_set` even if they don't exist yet — the guard checks declared ownership, not disk presence.
- **If validation keeps failing**, the problem is usually that two tasks share a file with no dependency. Either merge or introduce a dependency edge.
