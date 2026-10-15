---
name: measure
position: both
description: 'Write a SLICE''s measure lens as a grounding doc (measure.md) — the delivery-measurement focus, the metrics that prove it (baseline / target / proof, triangle-primary speed/tokens/cognition), and what is out of scope — then, when all seven lens docs line up, stamp the slice realized on the spine. The DELIVER pipe of realize (runs last): it opens its own branch (start-change) and closes it (commit → propose → review → merge). Reads the hub from the spine; the single play that flips a slice to realized — the marker /grill checks. Writes the lens doc + decisions + the realized stamp directly on the live model (ADR 026 direct-model-write).'
user-invocable: true
---

# measure

Write a shaped slice's **measure lens** as the grounding doc `measure.md` — what delivery the slice is
proving, the metrics that prove it (each a baseline, a target, and a proof; triangle-primary on
speed/tokens/cognition), and what is out of scope — and, when the slice **lines up** (all seven lens
docs present), **stamp it realized**. /measure reads the slice's **hub** — its functionalities'
grounding docs plus the profile, both from the spine. It is the **deliver** lens, the last of the
three realize pipes, and the one play that flips a slice's `status` to `realized` on the spine — the
single marker /grill checks before it cuts delivery work.

**Pipeline position: both.** /measure is the DELIVER pipe — a single-play pipe that runs last (after
the functional pipe ux → agentic → marketing and the non-functional pipe architecture → quality → run
have merged to main). The D2 rule prepends `start-change` (opens the deliver issue, cuts a fresh
branch off main, inits STM) and, after the lens is persisted, the realized stamp is made, and both are
guarded, appends the close sequence `commit-change → propose-change → review-change → merge-change`,
merging the realized slice to main. (#437; 3-pipe realize 2026-06-26)

**Write discipline (ADR 026, `standards/rules/direct-model-write.md`).** The LLM authoring skill
(author-measure-lens) writes ONLY the per-node grounding doc (the slice's `lens/measure.md`) straight
to the live model; every shared-file mutation — the new decision records under the slice's
`decisions/`, and the ONE spine field the run may set (this slice's `status` → `realized`, gated by
lines-up) — is done by the deterministic keyed persist script (`persist_measure.py`), in place, keyed
to the slice so it cannot touch another slice, another field, another spine collection, or edit an
accepted decision. The model tree is asserted clean once start-change has cut the branch (F15) and the
play commits its own `feat(model)` delta after the checkpoint (C14), before the injected close sequence
runs — so the working-tree diff vs the branch base is exactly this run's delta. Containment is a
post-write scoped guard (`scoped_write_guard.py`), not a draft. There is no draft model copy and no
apply/promote step.

## Compiled From

This play was compiled from the measure ICE (`reference/ice.md`) by play-editor (#466 Batch C, Level 3
rollout per ADR 025; #467 Batch B — the checkpoint upgraded to a conditional learned gate, see
`standards/rules/gate-config.md`; #500 — migrated to direct-model-write per ADR 026 and
`standards/rules/direct-model-write.md`). Intent defines constraints (C1–C14) and failure conditions
(F1–F15); the expectation defines success scenarios (S1–S6), a Done means (D1–D4, baked to
`stop-condition.yaml` — D4 counts BOTH stamp outcomes as done), and one recovery entry per failure
condition. To modify this play, update `reference/ice.md` and recompile with play-editor. Do NOT edit
this file manually — it is a compiled artifact.

## Role

You are the orchestrator. You own the workflow and step order. You delegate the domain work —
authoring the measure lens grounding doc — to the `product-os-keeper` agent via a JSON contract over
files on disk, and you run the mechanical work (readiness/hub resolution, the shape linter, the
content-quality eval, grounding + coverage, KB grounding, the keyed in-place persist, the lines-up
gate, the realized stamp, and the post-write scoped guard) through bundled scripts and an isolated
judge. You never write the lens or the spine yourself, you never stamp a slice that has not lined up,
and you never COMMIT the model delta before the single checkpoint's gate resolves (C11) — a typed
approval, a recorded config skip, or a recorded policy auto-pass.

**Forbidden:** hand-writing the lens or a decision; writing the shared files (`_spine.yaml`, the
slice's `decisions/`) by any route other than `scripts/persist_measure.py`; stamping the slice realized
when a lens doc is missing (C8); reading or grounding on another realize lens (C7); committing the
model delta before the Step 5 gate resolves (C11); running the writes against a dirty product-os tree
(C14/F15); closing COMPLETED without the stop-condition verdict reading held (C13/F13).

**Agent boundaries:**

| Agent | Domain | Skill it invokes | Phases |
|-------|--------|------------------|--------|
| `product-os-keeper` | Author the slice's measure lens (focus / metrics / out-of-scope) in place on the live model, from the hub + KB measurement-frame grounding, and emit the shared-file deltas (grounds, decisions, doc record) into the manifest | `kb-search`, `author-measure-lens` | Draft |

`product-os-keeper` is the single domain agent this play uses (1 of the ≤5 budget). The utility work —
cutting the branch and resolving the issue — is `start-change` (injected head), not a domain agent. The
content-quality judge always runs as an isolated, clean-context sub-agent (optionally on a configured
different model) — never the orchestrator's own context.

## Pre-flight

| Check | Constraint | Action on Failure |
|-------|-----------|-------------------|
| Resolve config + `product_base` (`.garura/core/config.yaml`) | — | Hard halt |
| Resolve `grounding-eval.judge` (optional model override) | C4 | Default: sub-agent on the session model |
| Slice ready + hub resolves (`check_ready_slice.py`) | C1 | Hard halt (REC1) |
| **Clean model tree** — after start-change (Step 0), `git status --porcelain -- <product_base>product-os` is empty | C14/F15 | Hard halt (REC15) |

Resolve the pre-flight facts mechanically with the bundled resolver:

```
python3 scripts/preflight.py --play measure --config .garura/core/config.yaml
```

Then resolve the slice and its hub from the spine — the readiness gate every realize lens shares:

```
python3 scripts/check_ready_slice.py --product-base <product_base> --slice <slice-id>
```

It asserts the profile is `set` (from the spine), resolves the slice record, and resolves every
`functionality_ref` through the spine to its `functionality.md` grounding doc — the hub. If the slice
is absent, a functionality does not resolve, or the profile is not firmed, hard halt (C1/REC1).

The run's working root (`<working>` below) is `{stm_base}_realize/measure/` — the manifests, the
lines-up capture, the keyed persist record (`persist-manifest.json`), the captured scoped-guard report
(`guard-report.json`), the stamp record (`stamp-record.json`), and the `status/` markers all live under
it. These are STM, non-model artifacts (ADR 008/017) — the model itself is written IN PLACE under
`<product_base>product-os/`, never into `<working>`. The stop condition evaluates against `<working>`.

**Clean-tree assertion (C14/F15, ADR 026).** start-change cuts the branch off fresh main, so the
product-os tree is clean by construction; still assert it right after Step 0 — the branch base is only
a correct reference for the scoped guard and the change-shape if the tree is clean before the writes:

```
test -z "$(git status --porcelain -- <product_base>product-os)" || { echo "HALT: dirty product-os tree (REC15)"; exit 1; }
```

If dirty, halt and ask for a clean model tree (commit or revert the pending model edits) before
/measure writes.

Right after the resolver, record the session identity stamp's start marker (#463 — soft-fail, never
a halt):

```
python3 scripts/session_stamp.py --phase start \
    --marker "{stm_base}_realize/measure/status/session-stamp-measure.json" \
    --cwd "$(pwd)" --branch "$(git branch --show-current)"
```

**Resume check:** if `{stm_base}_realize/measure/status/<slice-id>.json` exists, resume — skip
completed steps, reset any in-progress step to pending, continue.

## Task DAG

Create ALL tasks immediately after resolving config — before any domain work.

Write-then-review (ADR 026): the FULL model delta — the LLM doc AND the keyed persist's decisions +
realized stamp — is written to the live model BEFORE the checkpoint, so the guard, the change-shape,
and the human all see the real delta. Nothing is COMMITTED before the gate resolves; cancel reverts
the uncommitted writes.

```
[T0] start-change (injected — start head)            blockedBy: []
[T1] Draft the lens (doc to live)                    blockedBy: [T0]
[T2] Validate the live doc                           blockedBy: [T1]
[T3] Persist (keyed, in place — decisions + stamp)   blockedBy: [T2]
[T4] Guard the full delta + classify the shape       blockedBy: [T3]
[T5] Checkpoint (approval over the full git diff)     blockedBy: [T4]
[T6] Commit the model delta                          blockedBy: [T5]
[TE1] commit-change   (injected — end #1)            blockedBy: [T6]
[TE2] propose-change  (injected — end #2)            blockedBy: [TE1]
[TE3] review-change   (injected — end #3)            blockedBy: [TE2]
[TE4] merge-change    (injected — end #4)            blockedBy: [TE3]
[T7] Scenario Validation                             blockedBy: [TE4]
[T8] Close                                           blockedBy: [T7]
```

Mark each task in-progress before its step and completed right after its eval passes. No runtime
reordering. On resume, skip completed and reset in-progress to pending.

## Workflow

### Phase: Start (injected — D2 position: start)

**Step 0 — start-change** · Owner: `start-change` (sub-play) · Depends on: pre-flight
Run the start-of-pipeline member as a sub-play, dispatched with `parent_run_id` so it emits only its
own C1 evidence and this play's close absorbs it. It resolves or creates the deliver-pipe issue, cuts a
fresh branch off main, sets up a worktree iff config calls for it, and initializes the STM workspace.

    { "play": "start-change", "parent_run_id": "<this run id>", "inputs": { "title": "realize (deliver): <slice>" }, "outputs": { "result": "{stm_base}_realize/measure/start/start-change.json" } }

start-change owns its own evals (issue anchored, branch off latest main, worktree per config, STM
initialized); they are not re-checked here. Immediately after it returns, run the clean-tree assertion
(pre-flight, C14/F15) so the branch base is a correct reference for the guard and the change-shape.
**SE-14 (F15/C14):** the product-os tree was clean once start-change had cut the branch — the assertion
(`git status --porcelain -- <product_base>product-os` empty) passed before any write; a dirty model
tree halts (REC15), so the change-shape and the scoped guard reflect only this run's delta.

### Phase: Draft (write the lens doc to the live model, ADR 026)

**Step 1 — Draft the lens (doc to live)** · Owner: `product-os-keeper` · Depends on: Step 0
The agent invokes `author-measure-lens` to author the slice's `measure.md` (focus / metrics / out of
scope, per the Measure lens template) from the hub (the functionality grounding docs + the profile) and
KB measurement-frame grounding. Per ADR 026 the skill writes the doc **straight to the live model** at
its lens path under `<product_base>product-os/`, and emits the shared-file deltas — the grounds, any
material choices, the material decision records, and the doc record — as structured data in
`measure-manifest.yaml`. It writes NO shared model file (`_spine.yaml`, the profile, a decision record)
— the keyed persist (Step 3) applies the manifest's decisions and the realized stamp:

    {
      "task":    "author the slice's measure lens (focus / metrics baseline-target-proof / out-of-scope) from its hub, in place on the live model; ground each metric in the functionalities + profile and the frames in the KB; emit the grounds, decisions, and doc record into the manifest",
      "inputs":  { "slice_ref": "<domain>/<slice>",
                   "slice_file": "<slice record>",
                   "functionality_groundings": "<from check_ready_slice>",
                   "profile": "<spine profile>", "product_base": "<product_base>",
                   "lens_rel": "product-os/<domain>/slices/<slice>/lens/measure.md",
                   "manifest_path": "<working>/measure-manifest.yaml",
                   "proposals_dir": "<working>/proposals" },
      "outputs": { "manifest": "<working>/measure-manifest.yaml" }
    }

The skill reads the hub read-only, writes `measure.md` IN PLACE under `<product_base>product-os/`, and
writes `measure-manifest.yaml` under `<working>` (STM) with the shared-file deltas as structured data.
It returns the contract with the output paths on disk — never inline content.
**SE-1 (F1/C1):** `check_ready_slice.py` passed at pre-flight — the slice is ready and its hub
resolves; an unready slice halted (REC1).

### Phase: Validate

**Step 2 — Validate the live doc** · Owner: play · Depends on: Step 1
Run the guards over the LIVE `measure.md` this run wrote, before the checkpoint — shape first, then
content, then grounding. Under direct-model-write the doc is already written in place, and the spine
has NOT yet been mutated for this run (the keyed persist runs in Step 3):

```
python3 scripts/lint_grounding.py --doc <product_base>/product-os/<domain>/slices/<slice>/lens/measure.md
python3 scripts/validate_measure.py --manifest <working>/measure-manifest.yaml --slice-file <product_base>/<slice_file>
python3 scripts/check_kb_grounding.py --manifest <working>/measure-manifest.yaml --kb-root <kb_root> --proposals-dir <working>/proposals
```

Then run the **content-quality eval** over the live `measure.md`: spawn an isolated, clean-context
sub-agent handed the judge prompt (`standards/rules/grounding-eval.md`), the doc at its live path, and
the Measure lens per-section guidance, on the model from `grounding-eval.judge.model`. Gate the
verdict:

```
python3 scripts/grounding_gate.py --verdict <verdict.json>
```

**SE-2 (F3/C3):** `lint_grounding.py` exits 0 — `measure.md` conforms to the Measure lens template
(Focus / Metrics / Out of scope), no missing/extra/empty section.
**SE-3 (F4/C4):** the content-quality eval gate (`grounding_gate.py`) passes — `measure.md` is
self-explaining and clears the stranger test.
**SE-4 (F5/C5):** `validate_measure.py` — every metric grounds in a functionality's acceptance or a
profile outcome (the manifest grounds), and a material choice names a decision that resolves in the
manifest's `decisions:` list.
**SE-5 (F6/C6):** `validate_measure.py` — every functionality the slice bundles is considered.
**SE-6 (F7/C7):** `validate_measure.py` — the metrics ground on no other realize lens.
**SE-7 (F12/C12):** `check_kb_grounding.py` exits 0 — the measurement-frame choices trace to a KB
learning or a recorded proposal.
On any GAP, apply the matching recovery (REC3–REC7, REC12) and re-run before the checkpoint.

### Phase: Persist (write the full delta first, ADR 026 write-then-review)

**Step 3 — Persist (keyed, in place — decisions + stamp)** · Owner: play · Depends on: Step 2
Write-then-review (ADR 026): the FULL model delta is written to the live model BEFORE the checkpoint, so
the guard, the change-shape, and the human all see the real delta. The lens doc is already on the live
model (Step 1). First run the **lines-up gate** over the LIVE slice — does it now carry every one of the
seven lens docs? — capturing the result; then `persist_measure.py` writes the SHARED files in place: the
new decision records (`{slice}/decisions/<id>.yaml`, skip-if-exists) and, ONLY when the lines-up capture
reads ok, this slice's `status` → `realized` on the spine (keyed to the slice, one field). It ALWAYS
writes the stamp record either way, and REFUSES another slice, another field, another collection, or an
edit to an accepted decision (the node-level containment the file-level guard cannot provide). No draft,
no doc copy. Nothing is COMMITTED yet — the commit (Step 6) happens only after the gate approves; on
cancel the whole delta is reverted (Step 5):

```
python3 scripts/lines_up.py --product-base <product_base> --slice <slice-id> > <working>/lines-up.json || true
python3 scripts/persist_measure.py --manifest <working>/measure-manifest.yaml \
        --product-base <product_base> --slice <slice-id> \
        --lines-up <working>/lines-up.json --decided-by /measure --date "$(date -u +%Y-%m-%d)" \
        --record <working>/stamp-record.json --out-manifest <working>/persist-manifest.json
```

`persist_measure.py` writes the **machine persist record** (C13/#464): `persist-manifest.json` carries
`applied: true` alongside the written/changed lists — this field, not prose, is what the close's
stop-condition gate (D2) reads. The stamp record (`stamp-record.json`, the D4 input) reads
`{stamp_resolved: true, stamped: true}` when the lines-up gate passed and the slice was stamped, or
`{stamp_resolved: true, stamped: false, missing: [...]}` when a lens is missing and the stamp was
explicitly skipped — both are resolved outcomes; an unwritten record blocks the close (C13).
**SE-8 (F8/C8):** the slice is stamped `realized` only when `lines_up.py` reports every one of the
seven lens docs present; a missing lens leaves the status unchanged and is reported — and either outcome
is recorded in `stamp-record.json` (`stamp_resolved: true`, `stamped` true/false with the missing lenses).
**SE-9 (F2/F9/C2/C9):** the keyed persist mutated only this slice's `status` on the spine (and only on
lines-up) and added only its decisions — no other slice, field, or collection changed, and no accepted
decision was edited in place; the persist refuses any other mutation by construction.

### Phase: Guard + Classify (over the full delta)

**Step 4 — Guard the full delta + classify the shape** · Owner: play · Depends on: Step 3

**The run's write scope (the per-play guard policy, ADR 026).** The old `apply_measure.py` +
`stamp_slice.py` encoded /measure's write scope by construction — the lens doc re-derived, decisions
added skip-if-exists, and the one realized status field on the spine; under direct-model-write that same
scope is the `scoped_write_guard.py` policy:

    --allow    'product-os/*/slices/*/lens/measure.md'      # the re-derived measure lens doc (added or modified)
    --add-only 'product-os/*/slices/*/decisions/*.yaml'     # new decision records (added, never modified — append-only, C10)
    --allow    'product-os/_spine.yaml'                     # the shared spine — the keyed persist stamps the one status field in place

(fnmatch `*` crosses `/`, so `product-os/*/slices/*/lens/measure.md` matches the nested slice lens.)
Node-level containment inside the shared spine — only this slice's `status`, only on lines-up — is kept
by the keyed persist (Step 3), not the guard.

**Guard ONCE over the full delta (C9/C10, F10).** After ALL writes (the LLM doc from Step 1 and the
keyed persist's decisions + realized stamp from Step 3), run the scoped guard a single time over the
whole delta against the branch base. Capture its report — its `ok` field is the stop condition's D3
input:

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --allow 'product-os/*/slices/*/lens/measure.md' \
        --add-only 'product-os/*/slices/*/decisions/*.yaml' \
        --allow 'product-os/_spine.yaml' \
        --out <working>/guard-report.json
```

If the guard exits non-zero (a path outside the write scope changed, or an accepted decision was
modified), re-run with `--restore` to revert the offending paths, apply REC10, and re-persist before
the checkpoint.

**Classify the full working-tree delta (C11).** Classify the model tree's diff vs HEAD — now the FULL
delta (the lens doc + decisions + the realized stamp), per ADR 026 write-then-review (no draft dir):

```
python3 scripts/classify_change.py --play measure \
        --product-base <product_base> --base-ref HEAD --out <working>/shape.json
```

**SE-10 (F10/C10):** the scoped-write guard report reads `ok: true` — every changed model path fell
inside the declared write scope, and no accepted decision file was modified (add-only held); the run is
non-destructive.

### Phase: Checkpoint (conditional gate, class: standard, C11)

**Step 5 — Human review (conditional gate, class: standard)** · Owner: play · Depends on: Step 4
**This is the single checkpoint (C11) — the agent never skips it on its own judgment.** It is a
**conditional gate** per `standards/rules/gate-config.md` (#467 — /measure is one of the eleven
conditional document plays). Resolve, first match wins: pinned (n/a here) → `gates.plays.measure` →
the learned policy → `gates.classes.standard` → `gates.default` (absent ⇒ on). For the policy lookup,
use the shape key classified in Step 4.

Look the shape key up in the config-resolved learned policy (`gates.conditional.policy` →
`gate-policy.yaml`): **auto-pass** iff the shape is in the policy's `auto:` block AND not in
`never_auto:` AND Step 2 + Step 4 stand with no blocking finding (a `lint_grounding.py` gap, a
`grounding_gate.py` content-eval fail, or a guard violation). On auto-pass, do NOT wait: record `gate
auto-passed by learned policy (shape: <shape-key>, policy v<version>)` as a Checkpoint Decisions row,
include the working-tree diff summary (the axis counts from `shape.json`) in the run record, append the
crossing's live-eval ledger line, and proceed to Step 6 (commit):

```
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play measure \
    --issue <issue> --shape <shape-key> --predicted auto --human auto_pass \
    --ts <run ts> --policy-version <policy version>
```

Anything else resolves the gate on (an explicit `gates.plays.measure: off` instead records `gate
skipped by config (<resolution path>)` as a Checkpoint Decisions row and proceeds). When on, present
the proposed lens **inline over the real model git diff** — the focus, metrics, and out-of-scope, plus
any decision, AND the realized stamp this run made (or, if a lens doc is missing, the lenses still
outstanding, the slice left un-realized) — render the approval prompt
(`standards/templates/approval-prompt.md`) and wait for the typed response. Approve → continue to
Step 6 (commit). **Cancel → revert the working tree (ADR 026 step 6):** the full delta is already on
disk, so run the guard with `--restore` and an EMPTY allow set to `git restore` the modified model
paths and remove the new ones (byte-clean back to the branch base), then halt — nothing was committed,
and cancel means "revert what was written" (the branch, issue, and STM start-change created are its own
committed side effects and are left as-is):

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --restore --out <working>/guard-report.json   # empty --allow ⇒ every model path reverted
```

Then append the crossing's live-eval ledger line with the human's real action:

```
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play measure \
    --issue <issue> --shape <shape-key> --predicted gate \
    --human approved_clean|approved_edited|rejected --ts <run ts>
```

`<gates.conditional.ledger>` / `<gates.conditional.policy>` resolve from config `gates.conditional`
(defaults `.garura/core/gate-evals.jsonl` / `.garura/core/gate-policy.yaml`); `<policy version>` is the
policy file's `version:` field. `<run ts>` is the run's own UTC timestamp, derived the same way the
close derives `ts` (`date -u`), passed by the orchestrator — the script never reads the wall clock.
EVERY crossing appends exactly one live-eval ledger line, gated or auto.
**SE-11 (F11/C11):** the model delta was written to the live model by Steps 1 + 3 but is COMMITTED
(made durable) only at Step 6 on approval — so no product-model change is COMMITTED before the gate
resolves (a typed approval, a recorded config skip, or a recorded policy auto-pass); on cancel the whole
working-tree delta is reverted before any commit, so nothing is left on the tree.
**SE-13 (F14/C11):** every conditional-gate crossing appended exactly one live-eval ledger line
(`gate_eval.py append`), and an auto-pass fired only for a shape the policy lists in `auto:` (and not in
`never_auto:`) with no blocking finding.

### Phase: Commit (make the delta durable, ADR 026 step 7)

**Step 6 — Commit the model delta** · Owner: play · Depends on: Step 5
The gate approved (or auto-passed / was skipped by config). Commit the full model delta on the branch
(C14, ADR 026 step 7) — a lightweight persist step that makes the writes durable and advances HEAD, run
BEFORE the injected close sequence so the subsequent `commit-change` handles only what remains
uncommitted (STM evidence, ADRs), not the model delta this play already committed. A cancelled
checkpoint never reaches this step — its tree was already restored in Step 5:

```
git add -- <product_base>product-os
git commit -m "feat(model): measure lens for <slice> — lens, decisions, realized stamp (#<issue>)"
```

**SE-12 (F13/C13):** the close is stop-condition gated — `check_stop_condition.py` over the baked
`stop-condition.yaml` (D1 the persist record `persist-manifest.json` exists; D2 it stamps
`applied: true`; D3 the captured `guard-report.json` reads `ok: true`; D4 the `stamp-record.json` reads
`stamp_resolved: true`) must read **held** before any COMPLETED close, and the model delta is committed
(C14); a run whose keyed persist, scoped guard, or stamp did not land closes HALTED, never COMPLETED
(REC13).

### Phase: End sequence (injected — D2 position: end)

After the model delta is committed, the D2 rule injects the close sequence — each a sub-play dispatched
with `parent_run_id`, resolving its own context — to commit any remaining change, raise the PR, take
the verdict, and merge the realized slice to main.

**Step E1 — commit-change** · blockedBy: Step 6

    { "play": "commit-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_realize/measure/end/commit-change.json" } }

**Step E2 — propose-change** · blockedBy: E1

    { "play": "propose-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_realize/measure/end/propose-change.json" } }

**Step E3 — review-change** · blockedBy: E2

    { "play": "review-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_realize/measure/end/review-change.json" } }

**Step E4 — merge-change** · blockedBy: E3

    { "play": "merge-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_realize/measure/end/merge-change.json" } }

Each end member owns its own evals (commit grouped by concern, PR opened, verdict posted, branch merged
+ cleaned); they are not re-checked here. A review-change reject stops the chain before merge.

### Phase: Scenario Validation

**Step 7 — Scenario evals** · Owner: play · Depends on: the end sequence
- **SCE-1 (S1 — delivery analyst, first run):** `measure.md` is a valid Measure Lens doc clearing the
  linter + the content eval, grounded in the hub, written in place on the live model.
- **SCE-2 (S2 — delivery owner, the realized stamp):** with all six other lens docs present, the slice
  is stamped `realized` on the spine and that is the only spine change (the keyed persist + the guard
  report prove it).
- **SCE-3 (S3 — reviewer, not-yet-lined-up):** with a lens missing, `measure.md` is written but the
  slice is NOT stamped; the missing lens is named in the stamp record and the status unchanged.
- **SCE-4 (S4 — architect, hub-only):** every metric grounds in a functionality or the profile, never
  another lens (`validate_measure.py` clean).
- **SCE-5 (S5 — delivery owner, re-run):** a re-run re-derives only `measure.md` and re-affirms the
  stamp; everything else byte-identical; no accepted decision edited in place (the guard report reads
  ok; add-only held on decisions).
- **SCE-6 (S6 — reviewer, the checkpoint):** the Step 5 checkpoint showed the lens and the realized
  stamp inline over the real model git diff, and no product-model file was COMMITTED before that gate
  resolved — on cancel the working tree returns byte-clean to the branch base — or, on the auto-pass
  path (a policy-listed shape), the gate resolved with no wait and the recorded auto-pass, the appended
  ledger line, and the diff summary stand in for the wait (nothing COMMITTED before the gate resolved).

### Phase: Evidence & Close

**Step 8 — Close** · Owner: play · Depends on: Step 7
Run the Standard Play Close. /measure is a slice-realize play — record evidence per the D1 rule.
**SE-12 (F13/C13):** the stop-condition verdict is held before the run closes COMPLETED — including
D4, the resolved stamp record (either outcome); a close over an unmet or unevaluable verdict reads
HALTED, never COMPLETED (REC13).

```bash
# --- Standard Play Close (canonical; see standards/rules/play-close.md) ---
# Path tokens resolved at pre-flight (resolve here if not already):
#   ltm_project_target  = yq '.ltm.project-target' .garura/core/config.yaml
#   evidence_base, slug:
#     project-scoped play : evidence_base="${stm_base}${issue}/evidence/measure/"   ; slug="#${issue}"
#     product-scoped play : evidence_base="${product_base}_evidence/measure/"        ; slug="${slice_slug}"
evidence_template=$(cat "${ltm_project_target}standards/templates/evidence-file.md")
delivery_template=$(cat "${ltm_project_target}standards/templates/delivery-report.md")
ts=$(date -u +%Y%m%d-%H%M%S)
evidence_dest="${evidence_base}${ts}.md"
mkdir -p "$(dirname "$evidence_dest")"
# Session identity stamp (#463) — close phase; start phase ran at pre-flight
session_stamp=$(python3 scripts/session_stamp.py --phase close \
    --marker "${stm_base}_realize/measure/status/session-stamp-measure.json")
# Stop-condition gate (#464) — Step C0: this play carries a baked manifest, so the
# gate is LIVE. Evaluate the Done means as the close's authoritative input.
python3 scripts/check_stop_condition.py \
    --manifest "<play-dir>/stop-condition.yaml" \
    --base "${stm_base}_realize/measure/" \
    --out "${stm_base}_realize/measure/status/stop-condition-measure.yaml"
sc_exit=$?   # 0 held · 1 unmet · 2 error
# Conditional-gate policy refresh (#467) — soft: a distill failure never blocks the close.
#   gates_ledger / gates_policy / gates_streak = yq '.gates.conditional.ledger|.policy|.streak'
#   project_name = yq '.project.name' .garura/core/config.yaml
python3 scripts/distill_gate_policy.py --ledger "${gates_ledger}" --policy "${gates_policy}" \
    --streak "${gates_streak}" --project "${project_name}" || true
```

`/measure` opens its own deliver-pipe issue (position start), so it is project-scoped:
`evidence_base="${stm_base}${issue}/evidence/measure/"` and `slug="#${issue}"`.

**Step C0 — bind the verdict.** `sc_exit == 0` (held) permits `status: COMPLETED`. Anything else
closes `HALTED` with `exit_reason: stop_condition_unmet` and the evidence's Stop Condition section
names every unmet clause. A not-stamped run whose record names the missing lenses is a DONE run (D4
held); an UNRESOLVED stamp — no record — is not; fix the state per REC13 (re-run `persist_measure.py`
over the approved manifest so the persist record carries the machine `applied` field and the stamp
record names one of the two outcomes, and re-capture the `scoped_write_guard.py` report) and
re-evaluate; the close stays HALTED until the verdict reads held. An unevaluable verdict is never a
pass.

**Step C1 — Write evidence file.** Gated by the resolved `evidence.record` flag. When false, skip and
record `evidence skipped (record=false)`. Otherwise fill the `evidence-file.md` slots (play `measure`,
run_id `measure-${ts}`, slice slug, started/completed, status per C0, exit_reason; artifacts: the
slice's `measure.md` at its live path, the `measure-manifest.yaml`, any decision, the lines-up result,
the keyed persist record (`persist-manifest.json`), the captured `guard-report.json`, the stamp record
(stamped or explicitly not-stamped with the missing lenses), the model-delta commit sha, the
stop-condition verdict; the content-eval verdict; step + scenario evals SE-1…SE-14 / SCE-1…SCE-6;
checkpoint decision (incl. any `gate skipped by config` or `gate auto-passed by learned policy` row,
with the diff summary and the ledger line); the end-sequence results; the session identity stamp fields
from $session_stamp (#463): session_id, ledger_file, ledger_start_offset, ledger_end_offset (null when
unresolved — never blocks the close); and stop_condition per C0 with the Stop Condition section filled)
and write to `$evidence_dest`. Do NOT hand-author the body.

**Step C2 — Render delivery report.** Also render the **Next** line: resolve this play in `standards/rules/pipeline-next.md` and emit `**Next:** /<command> — <why>. Or run /next to see all recommended actions.` (only /next pointer, or omit, when the mapped command is null), per `play-close.md`. Fill the `delivery-report.md` slots: `## measure Delivered —
${slug}`, the Run Summary table, the Pipeline Steps table, the Artifacts Produced table (the measure
lens + any decision + whether the slice was stamped realized + the model-delta commit), Next Steps (if
realized: run /grill to cut this slice into epics; else: run the missing lens pipe), and a pointer to
`$evidence_dest`. Always emitted.

```bash
# --- end Standard Play Close ---
```

## Scenario Validation

| Scenario | Persona | Eval |
|----------|---------|------|
| S1 — first run | delivery analyst | SCE-1 |
| S2 — the realized stamp | delivery owner | SCE-2 |
| S3 — not-yet-lined-up | reviewer | SCE-3 |
| S4 — hub-only | architect | SCE-4 |
| S5 — re-run | delivery owner | SCE-5 |
| S6 — the checkpoint | reviewer | SCE-6 |

## Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | the slice is absent, a functionality does not resolve, or the profile is not firmed | halt and route to /shape or /understand before /measure runs | human |
| F2 | a write touched something beyond this slice's measure.md, a decision, or the one realized status field | revert the out-of-scope write; /measure writes only those | autonomous |
| F3 | measure.md fails the template/shape | re-emit to the Measure lens template (Focus / Metrics / Out of scope only) | autonomous |
| F4 | measure.md fails the content-quality eval | rewrite the failing section to the judge's cited fixes and re-judge until the gate passes | autonomous |
| F5 | a metric lacks a baseline/target/proof or grounds in nothing the slice delivers | re-draft the metric as a concrete baseline + target + proof tied to the hub | autonomous |
| F6 | a functionality is neither measured nor named out of scope | add a metric for it or name it in out-of-scope with the reason | autonomous |
| F7 | the assessment read or grounded on another lens | remove the dependency; derive only from the slice's hub | autonomous |
| F8 | the slice was stamped realized when a lens doc was missing | revert the stamp, report the missing lens, route to the pipe that owns it | human |
| F9 | the keyed persist changed more than this slice's status field on the spine | restore the spine and re-run `persist_measure.py` so only the single status flip on this slice is applied | human |
| F10 | the scoped-write guard reports an out-of-scope path, or an accepted decision was modified rather than added | the guard's `--restore` already reverted the offending paths; re-run writing only the allowlisted scope, after a human confirms the restore | human |
| F11 | a model delta was COMMITTED before the checkpoint gate resolved | revert the premature commit and the working-tree writes (guard `--restore`, empty allow set) and re-present the checkpoint; commit only after the gate resolves | human |
| F12 | a measurement frame with no KB learning and no recorded proposal | search the KB via kb-search and ground the frame, or raise a KB-learning-gap proposal | autonomous |
| F13 | the run is about to close COMPLETED with the Done means unmet | close HALTED (`stop_condition_unmet`) with the unmet clauses named; fix the state — re-run `persist_measure.py` so the persist record carries `applied` and the stamp record names one of the two outcomes, re-capture the guard report — and re-evaluate; the close stays HALTED until the verdict reads held | autonomous |
| F14 | a conditional-gate crossing left no live-eval ledger line, or an auto-pass fired for a shape the policy does not list as auto (or that carried a blocking finding) | re-append the missing ledger line from the recorded crossing; when the auto-pass was unearned, re-run the gate as a live wait (render the prompt, take the typed verdict) and append the corrected line | autonomous |
| F15 | the product-os tree is dirty once start-change has cut the branch (uncommitted model edits present) | halt and ask for a clean model tree — commit or revert the pending model edits — before /measure writes | human |

## Pause and Resume

Steps run top to bottom. On entry, resolve config, resolve the target slice, check the status marker,
skip completed steps, reset any in-progress step to pending, and continue. A fresh start with no marker
runs everything. The clean-tree assertion (F15) is scoped to a FRESH start right after start-change — a
resume that already wrote the model doc continues its own in-progress delta.

## Compilation Metadata

| Field | Value |
|-------|-------|
| fingerprint | sha256:ab8ca118cc1472e70f6dc858bf561d47712c179e0c54ee723c1fbd5ac2541f27 (of `reference/ice.md`) |
| compiled_by | play-editor (#500 direct-model-write, ADR 026); prior: play-editor (#466 Batch C; #467 Batch B — conditional learned gate) |
| pipeline_position | both (deliver pipe — injects start-change head and commit → propose → review → merge close) |
| position_exception | model-writing both play — writes the model on the started branch and commits its own model delta (C14) BEFORE the injected close sequence, which then handles only what remains uncommitted |
| workflow_structure | A (single checkpoint — conditional learned gate, class: standard, per gate-config.md #467; direct-model-write WRITE-THEN-REVIEW per ADR 026 — persist + guard + classify before the gate, commit after; stop-condition gated close) |
| model_writes | yes |
| stop_condition | stop-condition.yaml (D1–D4; D4 counts both stamp outcomes), gate live at Step C0 |
| domain_agents | 1 (product-os-keeper) |
| utility_agents | 0 (start-change is the injected head, not a domain agent) |
| skills_used | kb-search, author-measure-lens |
| scripts | 13 (preflight, check_ready_slice, lint_grounding, grounding_gate, validate_measure, check_kb_grounding, lines_up, persist_measure — keyed in-place persist writing the machine `applied` field + the lines-up-gated realized stamp, scoped_write_guard — post-write containment, check_stop_condition, session_stamp, classify_change + gate_eval + distill_gate_policy — #467 conditional gate) |
| step_evals | 14 (SE-1…SE-14) |
| scenario_evals | 6 (SCE-1…SCE-6) |
| recovery_entries | 15 (one per failure condition; 9 autonomous / 6 human) |

**Recompiled note (#500, direct-model-write / ADR 026):** migrated from draft-then-apply to
direct-model-write. The old draft model tree and the `apply_measure.py` (draft copier) + `stamp_slice.py`
(separate stamper) + `check_measure.py` (before/after verify) scripts are removed; the authoring skill
(`author-measure-lens`) writes the per-node `measure.md` straight to the live model and emits the
grounds + decisions + doc record as manifest data; the new keyed `persist_measure.py` writes the shared
files (the slice's decisions skip-if-exists, and the lines-up-gated realized `status` stamp on the
spine — stamp_slice's logic folded onto the keyed persist path) in place, keyed to the slice, and always
writes the stamp record; containment is the post-write `scoped_write_guard.py` (the lens doc `--allow`,
the slice decisions `--add-only`, the spine `--allow`; its `guard-report.json` is D3); `classify_change.py`
reads the working-tree git diff (`--product-base`/`--base-ref HEAD`, byte-identical canonical git-mode).
Order is **write-then-review** (ADR 026 "Order of operations"): the full delta — the LLM doc AND the
keyed persist's decisions + realized stamp — is written to the live model FIRST (Steps 1+3), then
guarded ONCE and classified over the full delta (Step 4), then the gate resolves over the real git diff
(Step 5), and only an approved (or auto-passed / config-skipped) gate COMMITS (Step 6). The stamp is a
status change on the spine, so it is written BEFORE the gate — the change-shape and the human see it.
Nothing is COMMITTED before the gate; cancel reverts the uncommitted writes via
`scoped_write_guard.py --restore`. The play asserts a clean product-os tree once start-change has cut the
branch (F15) and commits its own `feat(model)` delta after the checkpoint (C14), BEFORE the injected
`commit-change`. Done means: D1/D2 the persist record + `applied`; D3 the guard report `ok`; D4 the
resolved stamp record. See `standards/rules/direct-model-write.md`.

**Recompiled note (#467 Batch B):** checkpoint upgraded to a conditional learned gate; see
`gate-config.md`.

**Direct-edit deviation note (#500) — INTENT CHANGE, HAND-COMPILED, CONVERGENCE UNVERIFIED:**
This SKILL was updated to the direct-model-write write-then-review shape (ADR 026) by a **hand-compile
from `reference/ice.md`**, NOT by a `/play-editor` run. This is an intent change (it alters the write
path, the containment guarantee, the checkpoint cancel semantics, and the step order), so the sanctioned
path is recompile-via-`/play-editor`; play-editor is interactive-only (fully gated, human-checkpoint)
and cannot run headless in this environment, so the compiled output was produced by hand to match what
play-editor would emit from the current `reference/ice.md` (fingerprint above). **The `compiled_by` line
names play-editor for provenance intent, but no play-editor run actually occurred and convergence is
UNVERIFIED.** An interactive `/play-editor` convergence run against `reference/ice.md` is **REQUIRED** —
confirming the emitted SKILL matches this hand-compiled body and refreshing the fingerprint. This mirrors
the same caveat on /understand's #498 migration (the ratified reference implementation) and the /vision,
/grill, /learn fan-out of that pattern.
