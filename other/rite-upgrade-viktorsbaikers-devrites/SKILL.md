---
name: rite-upgrade
description: Audit and reconcile an older released DevRites workspace. Proves a current-contract defect, then routes its phase owner while preserving completed work and history.
argument-hint: "[feature-slug]"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/agents.md"],"triggers":{"reslice":["rite-plan/reference/slicing.md"]},"workspace":["state.md","spec.md","plan.md","tasks.md","decisions.md","questions.md","evidence.md","touched-files.md","review.md","seal.md","polish-report.md","browser-evidence.md"],"workspaceByRole":{"upgrade-planner":["state.md","spec.md","plan.md","tasks.md","decisions.md","questions.md"]}} -->
> Read-set manifest: `devrites-engine context --skills-root .pi/skills <slug> --skill rite-upgrade` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read.

# /rite-upgrade: reconcile a released workspace safely

Use when an unfinished workspace from an older release cannot resume. This is an
audit/orchestrator—not a pack update, cursor conversion, release replay,
structural migration, or generic cleanup.

## Rules consulted

Read [`core.md`](../devrites-lib/reference/standards/core.md), its agent and workspace-schema
references, and only current phase contracts needed for the observed gap.

## Invariants

- Upgrade writes no workspace artifact and never edits source, tests, dependencies,
  or Git. It observes, admits, invokes current owners, and re-audits only.
- Recognize only released workspace forms: `.devrites/work/<slug>/state.md` with v1/v2
  bullet fields (`- Phase:`, `- Next step:`, optional `- qid:`) or the v3 cursor table.
  A cursor with no `schema` row (every v1/v2 form, older v3 tables) is refused by the
  engine until the human runs the `migrate` command its refusal names (step 0). Otherwise
  preserve its encoding; only its owning rite may change fields. Never create aliases,
  journals, telemetry, version markers, or an engine migrator.
- Older provenance, cursor form, or pack version alone is never a defect. A repair requires
  a current rule, exact workspace evidence, affected gate, owning rite, exact paths, and
  the smallest behavior-neutral delta.
- Existing rites own semantic changes. Upgrade may sequence `/rite-clarify`,
  `/rite-plan repair|revise|course-correct`, `/rite-converge`, `/rite-vet`, `/rite-prove`, `/rite-polish`,
  `/rite-review`, and `/rite-seal`; it never reimplements them or starts Build or Ship.
  `/rite-doctor` owns install/config diagnosis.
- An admitted candidate route may name only the exact current gate artifacts its owner
  must refresh: `touched-files.md`, `evidence.md`, optional `browser-evidence.md`,
  `polish-report.md`, `review.md`, `seal.md`, and the owner's `state.md` fields as
  applicable. Source, completed-slice identities, answers, decisions, and unrelated
  history remain protected. Each owner preserves unrelated content and normal gates.
- Archived/`done` workspaces are no-ops. Unknown or unverifiable inputs stop without
  writes. There is no legacy fallback: never synthesize or guess scope, bytes, proof,
  freshness, or a historical pass.
- The explicit invocation authorizes only admitted, behavior-neutral workspace repairs.
  Product/policy choices, acceptance changes, irreversible risk, and human-only actions
  remain HITL.

## Workflow

0. **Orient read-only.** Apply `/rite-doctor`. Resolve the explicit or active slug.
   Archive-only is `current`; otherwise require contained regular `state.md` and read its
   cursor. A damaged/mismatched install stops at Doctor; missing live work routes
   `/rite-spec`; `done` is `current`. An unknown cursor is `unsupported`.
   A `state.md` whose cursor carries no `schema` row — or any engine refusal naming the
   workspace schema — means the workspace predates the current engine schema: structural
   normalization is a human-approved engine step that precedes this audit, not part of
   it. Stop and surface the refusal verbatim (it names the fail-closed `migrate`
   command with `--dry-run`/`--answer`); after the human runs it, restart at step 0.
1. **Freeze preservation evidence.** Record `git status --short`, cursor form/fields,
   `devrites-engine orient <slug>` (cursor, `task_graph`, `artifact_budgets`,
   `bulk_files`), and
   hashes of completed-slice fields, candidate gate artifacts, existing answers/decisions,
   and protected history. Inventory every path that could change; absence is evidence,
   never permission to synthesize history. **Rerun after a mid-run stop:** frozen hashes die
   with the stopped run, so never re-baseline over bytes its owners may have changed. The
   durable baseline is `HEAD`: a workspace path that differs from it is recorded
   `pre-changed` with its diff, not frozen as clean, and step 5 accepts it only as an
   admitted path of this run's assessment, else `gap`. An untracked workspace has no durable
   baseline: if its `state.md` cursor shows an owner's HITL/blocked stop, stop for the human
   to confirm the current bytes as baseline before step 2. For a post-Build workspace, also retain the
   exact result of `devrites-engine check candidate <slug>`; at or after Seal retain the
   exact result of `devrites-engine check seal <slug>`.
2. **Assess from fresh context.** Dispatch exact `devrites-upgrade-planner` with the named
   installed contracts, workspace paths, cursor form, current phase, and frozen baseline.
   Require one read-only typed assessment. It writes and asks nothing.
3. **Admit the assessment fail closed.** Accept `current` only when every applicable axis has
   cited evidence and no finding. Accept `repairable` only when every finding names the
   current rule, exact workspace evidence, affected gate, owning rite, exact writable paths,
   minimal delta, and protected invariants. Missing fields become `gap`.
   Unsupported shapes remain untouched. Reject version-only, speculative, alias-creating,
   source-changing, history-changing, or acceptance-changing advice.
4. **Route; do not duplicate.** For `repairable`, invoke only the admitted current owners,
   one at a time:
   - decision coverage or a material assumption → `/rite-clarify`;
   - stale/inconsistent planning or traceability with settled intent → `/rite-plan repair`;
   - over-budget `state.md` or planning artifacts carrying checkpoint narrative, or
     packets/traces in the workspace root → `/rite-plan revise` (verbatim relocation to
     `history/` / `packets/`, current view only; IDs, meaning, answers and decisions
     unchanged; nothing deleted);
   - unbuilt slices beyond the [feature ceiling](../rite-plan/reference/slicing.md#feature-ceiling-split-an-epic-never-override-the-budget)
     → `/rite-plan course-correct` (trigger `reslice` loads [`slicing.md`](../rite-plan/reference/slicing.md);
     `MVP cut` plus the named continuation sequence;
     built slices and their evidence stay);
   - live code and recorded intent disagreement → `/rite-converge`;
   - any changed planning input or readiness defect → `/rite-vet`;
   - a missing/malformed strict manifest, missing/malformed/mismatched evidence binding,
     a browser-binding defect when that file exists, or current candidate-check failure
     → `/rite-prove`;
   - candidate-affecting capability-ledger, `DESIGN.md`, or ADR rollups still deferred by
     an old Ship-era workspace → `/rite-polish`;
   - a missing, stale, or mismatched review binding → `/rite-review`;
   - a missing, stale, or mismatched seal binding or failed Seal gate → `/rite-seal`.

   Sequence only applicable owners; candidate owners stay in the Prove → Polish → Review
   → Seal order above. Each owner keeps normal gates/write limits. Stop on HITL/blocked.
   Never infer `/rite-customize --import-legacy`; that mode requires the exact token in the
   user's current invocation.
5. **Re-audit and prove preservation.** Re-dispatch the planner once against the changed
   candidate. `gap`, `unsupported`, or a remaining finding stops. Compare the frozen hashes
   and Git status; only admitted paths may differ. Cursor changes must match the owning
   rite while preserving form. Any unadmitted, protected, or source change is a gap and
   stops; Upgrade never restores it itself.
   For a post-Build workspace, run `devrites-engine check candidate <slug>` and require
   the assessed bindings to match it. At or after Seal, also run
   `devrites-engine check seal <slug>`. Run readiness where applicable:
   ```bash
   devrites-engine check readiness <slug>; echo "readiness rc=$?"
   ```
   Any nonzero result or mismatch remains a `gap` and stops.
6. **STOP.** Do not advance to Build or Ship. A repeated `/rite-upgrade` is a no-op only
   when the fresh assessment independently returns `current`; no marker may manufacture
   that result.

## Output

```text
Done: workspace <slug> compatibility <current | reconciled>.
Changed: <admitted active-workspace paths | none>
Evidence: assessment=current; candidate rc=<n|n/a>; seal rc=<n|n/a>; readiness rc=<n|n/a>; protected history/source unchanged
Open: <none | exact unsupported shape, evidence gap, or human gate>
Next: <state.md next action | one owning rite>
Record: <owning rite's state.md — written by the owner, not Upgrade>
↻ Hygiene: /clear before the next lifecycle step
```
