---
name: rite-plan
description: "Re-plan existing work when reality invalidates the plan: reslice a slice that is too big, repair drift, reorder dependencies, split boundaries, or unblock work. Not first-pass decomposition."
argument-hint: "[mode: decompose|reslice|repair|reorder|split|unblock|course-correct|revise]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/acceptance-preserving-reslice.md","devrites-lib/reference/standards/tooling.md","devrites-lib/reference/standards/agents.md","rite-plan/reference/slicing.md","rite-plan/reference/replan-and-repair.md","rite-plan/reference/dependency-graph.md","rite-plan/reference/task-breakdown.md","rite-plan/reference/anti-patterns.md","rite-define/reference/plan-template.md"],"triggers":{"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"one-shot":["devrites-lib/reference/standards/one-shot-actions.md"],"assumption-delta":["devrites-lib/reference/standards/assumption-checkpoints.md"],"workflow":["devrites-lib/reference/standards/development-workflow.md"],"workflow-artifacts":["devrites-lib/reference/standards/workflow-artifacts.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","drift.md"],"workspaceByRole":{"evidence-scout":["spec.md","architecture.md","decisions.md","state.md"],"plan-drafter":["brief.md","spec.md","plan.md","tasks.md","decision-coverage.md","questions.md","decisions.md","assumptions.md","architecture.md","state.md","drift.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/tooling.md","devrites-lib/reference/standards/workflow-artifacts.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .pi/skills <slug> --phase plan` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-plan: (re)plan an active feature

Update a plan invalidated by evidence, drift, or user decision. **Read the active workspace
first.** Missing `.devrites/ACTIVE`/workspace stops to `/rite-spec <feature>`. **Revise is
artifact-only**: reconcile
`spec.md` / `architecture.md` / `plan.md` / `tasks.md` / `traceability.md` without
editing source code.

## Rules consulted (read on demand from `.pi/skills/devrites-lib/reference/standards/`)
Pull [`development-workflow.md`](../devrites-lib/reference/standards/development-workflow.md) via `Read` when reshaping slice cadence or DoD
criteria.
Load [`repository-topology.md`](../devrites-lib/reference/standards/repository-topology.md), [`data-integrity.md`](../devrites-lib/reference/standards/data-integrity.md), or [`integration-reliability.md`](../devrites-lib/reference/standards/integration-reliability.md)
when the spec applicability map or observed drift triggers them.
Load [`assumption-checkpoints.md`](../devrites-lib/reference/standards/assumption-checkpoints.md) (trigger `assumption-delta`)
when scope introduces a second case, an optional field, or a chosen-over-derived value.
Before classifying any Reslice, read `.pi/skills/devrites-lib/reference/standards/acceptance-preserving-reslice.md`.

<!-- BEGIN RESLICE ROUTE-TO-ACTION -->
- `FOLD` → reconcile `architecture.md`, `plan.md`, `tasks.md`, and `traceability.md` atomically; invalidate Vet/readiness; Vet.
- `GUARD_AND_REPAIR` → no planning writes; Spec Drift Guard → Clarify → Plan repair → Vet.
- `BLOCKED_INPUT` → no planning writes; exact diagnostic; recover input; reclassify.
<!-- END RESLICE ROUTE-TO-ACTION -->

## Operating rules
- Update the spec when needed, but never plan around a known-wrong assumption.
- Keep each slice small enough for one focused build → prove cycle.
- **Derive slice count:** reslice when work cannot build+prove in one cycle, not to hit a
  requested tally. Treat counts as hints and explain honest differences; see
  [`slicing.md`](reference/slicing.md).
- **Size by complexity, order by dependency.** A slice carries a `Complexity: N/5` score (from
  `/rite-define`); a slice scoring **>3** is a reslice trigger unless its inline reason justifies
  the irreducible complexity. Honor each slice's `depends_on:`: the next *buildable* slice is the
  lowest pending one whose dependencies are all built. This preserves one-slice-at-a-time execution.
- **Root writes; drafter proposes.** Follow
  [`agents.md`](../devrites-lib/reference/standards/agents.md). The controlling chat owns
  human questions, decisions, reconciliation, and planning writes.
- **Nested repair preserves its caller.** When `state.md` contains a valid
  technical-backtracking return cursor, preserve any valid return cursor
  byte-for-byte. `/rite-vet` is the next internal prerequisite, not a command to
  hand back to the human.

## Workflow
0. Read `.pi/skills/devrites-lib/reference/standards/core.md` (operating rules) before reshaping anything.
   Then resolve the explicit or active slug, require its `state.md`, and read
   the cursor directly.
1. Read `spec.md`, `decision-coverage.md`, `plan.md`, `tasks.md`, `state.md`, `drift.md`,
   `eng-review.md`, and the current `git diff` (if a repo). Read `decisions.md` and
   `assumptions.md`. Require `Decision coverage: CLEAR`; otherwise STOP → `/rite-clarify`.
   Apply `.pi/skills/devrites-lib/reference/standards/code-navigation.md`:
   codebase-memory `trace_path` for dependencies and blast radius, no repeat queries
   for reassurance. For an external
   dependency's current API surface, consult context7 if available.
2. **Pick the mode** (`$ARGUMENTS` or infer): Apply the marked action before writes and
   retain its decision/coverage evidence.
   - **decompose:** break an already-sliced feature into vertical slices again. With no
     `SLICE-###` in `tasks.md`, stop and route to `/rite-define`; first-pass decomposition is its.
   - **reslice:** a slice is too large; split into thinner end-to-end slices.
   - **repair:** a Spec Drift Guard event; fold the resolution into plan + tasks.
   - **reorder:** fix the dependency order.
   - **split:** separate backend/frontend contracts (see `devrites-api-interface`).
   - **unblock:** a verification failed; re-route around the blocker.
   - **course-correct:** mid-build user pivot; apply the marked action, choose
     rollback/forward-fix, and update permitted artifacts atomically (`MVP cut` is the named retreat).
   - **revise:** reconcile a requested artifact revision; propose/confirm its file set and
     **never edit source**. A neutral workspace edit is authorized by explicit `/rite-upgrade` with a
     `repairable` assessment naming rule, evidence, gate, paths, and delta, or, for budget relocation
     only, by the phase owner when `orient` reports `over: true`—never source or history rewording.
     **Revise or new?** Same intent? >50% scope survives? Original not completable without it?
     Two “no” answers mean new work: seal/ship current scope (`MVP cut` if named), then
     `/rite-spec`, and stop.
   See [replan-and-repair](reference/replan-and-repair.md) for each mode's steps.
2a. **Draft fresh.** Dispatch `devrites-plan-drafter` in `repair` mode with frozen mode,
   affected artifacts, settled contract, and failure/drift; a slice-bound repair
   builds its bundle with `--slice <SLICE-ID>` per affected slice. Await one atomic, read-only
   the drafter's `candidate_files` bundle; human choices return separately.
   When the observed failure is missing or ambiguous consumptive-action evidence,
   require the drafter to apply [`one-shot-actions.md`](../devrites-lib/reference/standards/one-shot-actions.md) and return the bounded
   diagnostic-amplification design, injective boundary map, per-seam fixtures, and
   collision mutant. Past evidence loss is not terminal. The drafter supplies no bodies.
   A repair candidate carries a delta self-check scoped to what the patch
   touches: which intersected invariants it re-verified, with evidence of no
   correction-created regression. Global re-derivation (ID/edge/HZN counts,
   acyclicity) runs on materialized artifacts at the step-7 gate — the drafter
   never re-derives them by exhaustive search. It also carries a bounded
   self-attack over the delta (`self_attack_exposures`), catching the shallow
   next-round findings before Vet's dispatch rather than after a full loop.
   During recovery, a non-Critical exposure off the failing fingerprint's causal
   path goes to `eng-review.md` `## Deferred findings` (Review gives it a verdict;
   Seal blocks without one), so a repair never widens past its fingerprint.
   Root dispositions every other exposure — fold as a finding, accept as a declared
   residual, or reject with reason; none silently drops.
   Packet mechanics: dedupe at assembly — findings with an identical
   required-fix and site set merge into one entry that closes all their
   fingerprints. The packet may carry digest-pinned site excerpts so the
   drafter spot-verifies anchors instead of re-scanning whole files. Root
   partitions findings into anchor-disjoint clusters — findings sharing any
   anchor or mirrored clause stay in one cluster — and, with two or more,
   dispatches one drafter per cluster in one parallel wave within the scale
   limits. Every cluster pins the same base; their bundles apply together in
   one `state apply-bundle` call, and an overlap refusal merges those clusters
   for the re-dispatch. A `partial`-
   continuation re-dispatch continues the same packet; it does not advance the
   same-seam counter. Count consecutive repair packets whose findings' cited clause sets overlap
   the immediately previous packet's — the overlap is the seam. Carry it as an explicit
   integer `same_seam_count` in every packet (previous value + 1 when the seam repeats,
   else 1) so the threshold is counted rather than judged; a packet that reports the same
   seam without the counter is malformed. At the third
   same-seam packet, mark it `convergence_pressure: true` with the seam named.
   Under pressure the drafter first asks whether a different mechanism removes the
   recurring failure class (read content-addressed Git objects instead of walking a live
   directory; a bounded parser instead of hand checks) and proposes that swap before
   another pin; acceptance stays unchanged. Accreting checks on one seam is the loop.
   Under pressure the drafter may close a finding marked as a refinement of an
   already-pinned clause by folding an explicit, bounded declared
   residual/limitation into the contract text instead of another precision
   pin — never for a `new_failure_mode` finding. Every finding still gets one
   disposition; none is skipped. A fourth same-seam packet that still carries
   `new_failure_mode` findings means the seam is under-specified, not
   under-repaired: route a declare-limitation-or-continue choice to
   `/rite-clarify`. AFK records the suspect seam in `state.md` and continues
   within budgets — a coverage limitation is a product decision and is never
   auto-declared.
   Bind exact active `.devrites/work/<slug>/` targets and executable contract; after Vet READY, root
   materializes the exact vetted workflow-artifact paths under
   [`workflow-artifacts.md`](../devrites-lib/reference/standards/workflow-artifacts.md)
   without dispatching the product wright.
3. Reason about dependencies: [dependency-graph](reference/dependency-graph.md).
   Reconcile the horizon register against `../rite-define/reference/plan-template.md`.
   Preserve every `HZN-###` and unresolved item. Cite evidence when reclassifying the earliest
   honest decision point; resolution or supersession also needs evidence. Never silently delete
   an item. Planning choices resolve from source evidence or become bounded risk spikes with
   discriminating criteria and fallback branches; local/checkpoint entries retain their owner,
   trigger, bounds/fallback, and proof. A new human-owned blocker stops to `/rite-clarify`.
   Reconcile `plan.md`'s canonical `Shared contract proof`: changed provider/consumer
   boundaries keep one reused contract artifact ahead of both asserting tests, and unaffected
   plans retain the specific no-impact statement. Missing, one-sided, duplicated-contract, vague, or
   non-consuming proof routes to `/rite-vet` only after repair.
   Reconcile the spec applicability map and retain every applicable standard's required
   topology/data/integration owner, failure/recovery, deployment order, and proof output.
   **Completion:** the slice graph is cycle-free and every dependency names an existing slice.
4. Re-slice using vertical-slice rules: [slicing](reference/slicing.md) and
   [task-breakdown](reference/task-breakdown.md). Prefer thin, shippable, verifiable.
   **Completion:** every slice is independently shippable/provable or carries an irreducibility reason.
5. Reconcile the candidate's meaning against steps 3 and 4, save each bundle
   under `packets/`, and apply its hunks with `devrites-engine state apply-bundle
   <slug> <bundle.json>...` (all-or-nothing; `--dry-run` previews); never
   hand-copy hunks or stage file copies. Rewrite each owning clause in place; never
   append a dated delta or fold section beside the clause it supersedes (apply-bundle
   refuses one). Then update `state.md` and append
   rationale to `decisions.md`. A rejected candidate
   (malformed bundle, stale or non-unique anchor, any apply-bundle refusal) or a drafter `Outcome: gap`
   is one no-progress outcome on every open fingerprint in the fold; the
   re-dispatch packet must name the rejection so the same hunks don't recur.
   A gap naming genuinely human-owned information routes to `/rite-clarify`.
   A drafter `Outcome: partial` is progress: materialize its complete findings,
   then re-dispatch a narrowed packet for `remaining_findings` with anchors
   re-derived from the just-updated files — same repair pass, fresh context.
   A partial covering zero findings counts as no-progress. Findings in
   `blocked_findings` route to `/rite-clarify`, never the re-dispatch.
   Any change to `architecture.md`, `plan.md`, `tasks.md`, or `traceability.md` invalidates
   the previous vet verdict: set `Phase: plan`, `Next step: /rite-vet`, and, when
   `eng-review.md` exists, set `Implementation readiness: NEEDS REPLAN`. Never retain READY
   across changed planning inputs. Preserve `Plan approved` only for behavior/acceptance-neutral
   technical repair; clear it for a contract-changing or newly blocking horizon item and
   reconfirm only after Clarify and Vet close it. If you stopped for drift,
   mark the `drift.md` entry resolved. Never remove or overwrite a valid caller
   return cursor while writing the Plan checkpoint.
6. After editing `brief.md`, `spec.md`, `decisions.md`, `assumptions.md`, or `questions.md`,
   re-scan affected coverage, assumptions, uncertainty, and gates. `open` rows, unowned
   material assumption, or open blocking/escalating question routes `/rite-clarify`/HITL.
   Restore `CLEAR` only from current evidence.
7. **Done when:** every slice is sized (builds + proves in one cycle; no slice scoring >3
   left unjustified), the dependency order is acyclic, every open `drift.md` entry
   was folded in one pass and marked resolved, the delta self-check is recorded,
   revised artifacts agree with each other, no source files changed in
   `revise` mode, the marked action is complete, and every changed
   plan ends at `/rite-vet` rather than returning directly to build; horizon IDs stay stable,
   reclassifications cite evidence, and no unresolved item vanished. The `Shared contract proof`
   table or justified no-impact statement must still match the revised boundary set.
   If any check fails, loop back: don't hand off a half-reshaped plan.

When invoked inline by a controlling rite, return the completed Plan checkpoint
to that caller so it can invoke Vet immediately. The phase boundary is not a
user-facing stop unless a genuine HITL, safety/access, or parked-recovery
condition was recorded.

When invoked directly with no controlling caller and a planning artifact
changed, become the caller for the mandated next step: save a return cursor
(`return_phase`/`return_next_action`) naming this Plan pass as the caller —
a direct Plan has no caller above it, so without the saved cursor Vet reads
itself as top-level and its verdict becomes a user-facing command. Invoke
`/rite-vet` inline and consume its results — `NEEDS REPLAN` re-enters repair
internally under the fingerprint caps and is never emitted as a user-facing
command; `NEEDS CLARIFICATION` and human-owned gates still reach the user.
Stop only at Vet's boundary (READY readback; next step `/rite-build`). An
unchanged plan keeps its recorded next step.

> **Mid-flight discipline.** Do not change product behavior without confirmation or
> absorb drift silently. See [`anti-patterns`](reference/anti-patterns.md).
