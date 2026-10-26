---
name: rite-vet
description: Review a defined engineering plan before code. Use for plan vetting or lock-in; not for implementation review or final readiness sealing.
argument-hint: "[slug] [--cross-model] [--full]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/parallel-dispatch.md","devrites-lib/reference/standards/gates.md","rite-vet/reference/review-axes.md","rite-vet/reference/artifacts.md","rite-vet/reference/depth.md","rite-vet/reference/eng-lenses.md","rite-vet/reference/anti-patterns.md"],"triggers":{"afk":["devrites-lib/reference/standards/afk-hitl.md"],"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"assumption-delta":["devrites-lib/reference/standards/assumption-checkpoints.md"],"cross-model":["rite-vet/reference/cross-model.md"],"devex":["devrites-lib/reference/standards/developer-experience.md"],"dod":["devrites-lib/reference/standards/definition-of-done.md"],"elicitation":["devrites-lib/reference/standards/elicitation.md"],"errors":["devrites-lib/reference/standards/error-handling.md"],"grammar":["devrites-lib/reference/standards/spec-grammar.md"],"one-shot":["devrites-lib/reference/standards/one-shot-actions.md"],"performance":["devrites-lib/reference/standards/performance.md"],"principles":["devrites-lib/reference/standards/principles.md"],"reslice":["devrites-lib/reference/standards/acceptance-preserving-reslice.md"],"testing":["devrites-lib/reference/standards/testing.md"],"workflow":["devrites-lib/reference/standards/development-workflow.md"],"workflow-artifacts":["devrites-lib/reference/standards/workflow-artifacts.md"],"yagni":["devrites-lib/reference/standards/patterns.md","devrites-lib/reference/standards/coding-style.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","strategy.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md"],"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/afk-hitl.md","devrites-lib/reference/standards/elicitation.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/parallel-dispatch.md","devrites-lib/reference/standards/workflow-artifacts.md"],"workspaceByRole":{"doubt-reviewer":["spec.md","architecture.md","plan.md","tasks.md","test-plan.md","decisions.md","state.md"],"devex-reviewer":["spec.md","plan.md","tasks.md","decisions.md","state.md"],"plan-reviewer":["spec.md","plan.md","tasks.md","test-plan.md","decision-coverage.md","architecture.md","decisions.md","state.md"],"strategy-reviewer":["brief.md","spec.md","plan.md","decisions.md","decision-coverage.md","strategy.md","state.md"]}} -->
> Read-set manifest: `devrites-engine context --skills-root .omp/skills <slug> --phase vet` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-vet: review the plan before build

Vet every plan's scope, architecture, quality, proof, performance, failures and writer
safety. Fold cited technical findings; design Build tests. Temper owns product;
Vet owns implementation; current `$ARGUMENTS` (`--full`) feeds the depth triggers in
`reference/depth.md`; profiles never remove the exact plan-reviewer gate
([orchestration-profiles.md](skill://devrites-lib/reference/orchestration-profiles.md)).

## Rules

Read the active standard from: [`principles.md`](skill://devrites-lib/reference/standards/principles.md), [`patterns.md`](skill://devrites-lib/reference/standards/patterns.md) + [`coding-style.md`](skill://devrites-lib/reference/standards/coding-style.md) (over-engineering / YAGNI rubric, trigger `yagni`),
[`testing.md`](skill://devrites-lib/reference/standards/testing.md), [`spec-grammar.md`](skill://devrites-lib/reference/standards/spec-grammar.md), [`performance.md`](skill://devrites-lib/reference/standards/performance.md), [`error-handling.md`](skill://devrites-lib/reference/standards/error-handling.md) (trigger `errors`),
[`development-workflow.md`](skill://devrites-lib/reference/standards/development-workflow.md), [`afk-hitl.md`](skill://devrites-lib/reference/standards/afk-hitl.md), [`one-shot-actions.md`](skill://devrites-lib/reference/standards/one-shot-actions.md),
[`developer-experience.md`](skill://devrites-lib/reference/standards/developer-experience.md), [`elicitation.md`](skill://devrites-lib/reference/standards/elicitation.md), and [`definition-of-done.md`](skill://devrites-lib/reference/standards/definition-of-done.md) (trigger `dod`). Load
repository topology, data integrity, and integration reliability only when
triggered (trigger `applicability`). When the plan's scope generalizes an existing boundary — a second
platform/tenant/source of truth, a newly optional field, a constant turned parameter —
confirm the [`assumption-checkpoints.md`](skill://devrites-lib/reference/standards/assumption-checkpoints.md) question (trigger `assumption-delta`)
was answered and recorded, not skipped-as-negative.
Before classifying any Reslice, read `.omp/skills/devrites-lib/reference/standards/acceptance-preserving-reslice.md`.
When a
plan declares a root-authored executable workflow file, read
[`workflow-artifacts.md`](skill://devrites-lib/reference/standards/workflow-artifacts.md).

<!-- BEGIN RESLICE ROUTE-TO-ACTION -->
- `FOLD` → fold technical topology; invalidate Vet/readiness; affected Vet before Build.
- `GUARD_AND_REPAIR` → no planning writes; Spec Drift Guard → Clarify → Plan repair → affected Vet.
- `BLOCKED_INPUT` → no planning writes; exact diagnostic; recover input; reclassify.
<!-- END RESLICE ROUTE-TO-ACTION -->

## Invariants

- Review implementation, not ambition. Challenge creep, complexity, proof, and
  risk without changing accepted product scope.
- Root owns decisions/writes/readiness; reviewers judge without route policy.
  Cite findings/confidence; suppress
  unverified or confidence ≤4 findings under `review-axes.md`.
  Lens arrows in `eng-lenses.md` are heuristics; band findings only under the
  four `review-axes.md` names.
- Auth, migration, public API, and data-model changes use maximum caution and the
  irreversible-risk stop. Project principles never become trade-offs.
- **Governance-protected paths** (`.devrites/**`, pack skill/agent trees,
  `NOTICE.md` generator regions, CI/hook config named in repo docs) require explicit
  human approval before plan slices may edit them. A slice touching a protected path
  without approval → Vet **NEEDS CLARIFICATION**.
- Use the lowest axis band; never average or round thin to ready. Search before
  asking and resolve reversible technical choices. Ask only human-owned choices.
- Preserve a valid technical return cursor. Agent-owned `NEEDS REPLAN` returns
  internally to its caller, not to the human; on a direct invocation there is
  no caller, so Vet becomes it — save a return cursor
  (`return_phase`/`return_next_action`) naming this Vet pass as the caller and
  invoke `/rite-plan` repair inline under the same fingerprint caps. An
  agent-owned verdict with budget remaining is never a user-facing command.
- **Recovery recheck is bounded and batched.** A valid cursor plus open
  fingerprints enters Recovery recheck; it does not start another Full Vet or
  repeat unaffected axes/reviewers. One dispatch covers every open fingerprint
  of the fold — each checked individually — with a mandatory correction-created
  regression audit.
- Refuse the rationalizations in [`anti-patterns`](reference/anti-patterns.md).
<!-- workflow-artifact-adapter: {"module":"devrites-lib/reference/standards/workflow-artifacts.md","entry":"plan declares root-authored executable workflow file","action":"emit exact admission; stale/missing authority uses PLAN_VET_REPAIR","return":"Vet READY cursor or exact technical replan"} -->
## Workflow

0. **Orient.** Read core. Resolve active slug, require state, and read plan,
   tasks, spec, decision coverage, optional strategy/design brief, decisions,
   assumptions, and state. Require approved Plan and `Decision coverage: CLEAR`;
   otherwise stop for Define or Clarify. Check placement (`get_architecture`),
   blast radius (`trace_path`), and reuse (`search_graph`) per [`code-navigation.md`](skill://devrites-lib/reference/standards/code-navigation.md).
1. **Select depth.** Apply `reference/depth.md` exactly; never skip. Every initial
   pass records an engineering verdict and test-plan coverage. A valid Recovery
   recheck retains prior depth and enters 1b.
1a. **Independent initial pass.** Freeze candidate and dispatch the exact fresh
   read-only plan reviewer — plus developer-experience reviewer for developer
   surfaces (trigger `devex`) and the current strategy reviewer after significant
   Temper — in
   parallel under `skill://devrites-lib/reference/parallel-dispatch.md`; they are
   independent read-only passes on one frozen candidate. Missing
   required account blocks. Run root steps 2–4, including step 3's preflight
   commands, on the same frozen candidate while the wave is out; reconcile the
   accounts when they return.
1b. **Recovery recheck.** Require valid return cursor, accepted prior finding,
   exact fingerprint/reproduction, repaired candidate identity, changed
   paths/criteria, affected drift/evidence, and the recorded delta self-check.
   Freeze that packet and dispatch each exact owning reviewer once,
   fresh/read-only, limited to it — all its open fingerprints in that dispatch.
   Do not rerun broad inventory or unaffected reviewers. Close the prior
   fingerprint only with discriminating evidence plus an explicit
   correction-created regression verdict on the touched invariants (acyclic
   deps, traceability, contract proof, sizing) and every region depending on a
   changed clause — enumerate dependents via the dep graph and traceability
   refs, not only patched sites. Otherwise record one no-progress outcome. A
   different Critical/Important invariant needs exact evidence and a new
   fingerprint; a Suggestion, Nit, or FYI cannot keep recovery open. Reviewer
   `Late:` rows on unchanged clauses follow the canonical
   [late-finding rule](skill://devrites-lib/reference/standards/afk-hitl.md#retry-cap-no-progress-loops-and-self-resolve):
   Critical with a failure path → new fingerprint; otherwise `eng-review.md`
   `## Deferred findings` (mechanism rows become one proof row at step 6). A packet
   marked `convergence_pressure` accepts an explicit, bounded declared
   residual/limitation folded into the contract text as closure for a finding
   marked as a refinement of an already-pinned clause; the recheck may re-raise
   it only by naming a concrete failure path the declaration omits. A
   `new_failure_mode` finding is never residual-eligible. A fold whose
   findings are all `mechanism` kind or Suggestion-or-lower rechecks mechanically at the
   materialization gate — anchors applied (a clean `state apply-bundle`), mirrors consistent, invariants
   pass — without a dispatched reviewer; sub-Important findings already
   cannot keep recovery open. Reconcile
   shared artifact/readiness gates, then enter step 8 or the next repair.
   Do not fall through to steps 2–7. Retain evidenced unchanged coverage; changed
   global contract/uncertain impact requires full applicable review. Reopen historical
   findings only for affected invariants/dependencies.
2. **Challenge scope.** Apply review-axes §0 and search accepted decisions.
   Harden to the smallest contract-complete plan, using marked topology action.
   Then verify bidirectional ID-and-meaning traceability across spec/plan/
   tasks/test-plan/traceability, acceptance, terms, principles, anti-slop,
   and conventions; every slice and test-plan row maps to a live requirement
   and vice versa. Critical gaps and
   unexcepted principle breaches block; record the challenge result in `eng-review.md`
   §2 (Scope challenge) after recheck.
3. **Preflight Build entry.** Under `reference/artifacts.md`, verify exact
   command/cwd/tool/version/prerequisite; output filters must preserve upstream
   failure. Verify dependencies from authoritative source plus nearest manifest.
   Run parser-sensitive syntax only in isolated fixtures. Remeasure mutable facts;
   live evidence wins, conflict marks stale, and unmeasurable conflict is a gap.
   Record complete SHA-256 provenance. Every behavioral mapping names a positive
   discriminating assertion and decisive signal, never only exit zero.

   For each consumptive action, bind every `reference/artifacts.md` Consumptive
   action gates column; every fingerprint identifies one actionable seam; aliasing multiple
   emit sites is a gap. Preflight observes but need not make future behavior pass,
   except that a manifest/lockfile edit is dry-run now: before READY run
   `devrites-engine check preconditions <slug>` (rows with `Run at` `vet`, including each
   `dependency-dry-run` and preserve-baseline row). A failure folds into Plan repair; only an
   owner-owned decision becomes a question, batched under the afk-hitl decision-chain rule.
4. **Audit readiness.** Goal-backward map every requirement, criterion, NFR,
   interaction, edge/prohibition, and decision row to one slice and executable
   proof. Verify UX/spec/architecture alignment, contracts, dependency order,
   slice independence/wiring, prerequisites, failure/observability/rollback, and
   ownership. The plan's `Shared contract proof` names one reused boundary
   artifact plus two consuming tests for every changed API/event/schema/provider-
   consumer seam, or an explicit no-impact statement. Missing, one-sided,
   duplicated-contract, vague, or non-consuming proof fails closed. Each slice
   names a fast writer-safe check its wright can run; proof reachable only through
   root-owned full gates is a `mechanism` finding.

   Technical gaps are `NEEDS REPLAN` and Plan repair — each finding marks
   itself `new_failure_mode` or names the already-pinned clause/fingerprint
   it refines, making alias-detection and `convergence_pressure` eligibility
   mechanical — and carries `kind: contract | mechanism`
   (`review-axes.md` § Finding kind). Only `contract` findings open a Plan
   repair; a `mechanism` finding is closed by one `test-plan.md` proof row
   at step 6 and leaves readiness intact when nothing else is open.
   Product/risk gaps are
   `NEEDS CLARIFICATION` and Clarify. Neither becomes a Build qid.
5. **Review axes.** Apply `review-axes.md` through `eng-lenses.md`. Fold verified
   behavior-preserving technical findings; walk only human-owned decisions.
   Profile gate ceiling and Reslice marked action remain authoritative.
6. **Write outputs.** Produce every artifact in `reference/artifacts.md`. After
   editing intent/decision/assumption/question owners, re-scan affected coverage,
   assumptions, uncertainty, and gates. Keep state non-READY. Every scenario and
   criterion needs positive, discriminating proof; every slice must be one-pass
   implementable; developer plans (trigger `devex`) write the devex reviewer's
   predicted scorecard to `devex.md`. Durable commands
   are portable repository commands, not host wrappers — resolve them with
   `devrites-engine detect commands` (Makefile/package.json/manifests, no
   execution) and cite the resolved text verbatim; an `unresolved` slot means
   name the concrete command in the plan, never guess one.
   Once the `## Build-entry preflight` table is final, run
   `devrites-engine gates scaffold <slug>` to seed `gates.md` (one pending gate
   per `AC-###`; never clobber an existing ledger), then author each gate's
   `CHECK`/`EXPECT`/`CWD` per artifacts.md §`gates.md` so every runnable oracle
   is an approved preflight row. Run
   `devrites-engine gates lint <slug> --strict` and resolve every finding before
   READY; the readiness check refuses a missing or malformed ledger but does not
   replace this oracle-quality gate.
7. **Narrow recheck after edits.** A slice-bound recheck builds its bundle and
   opens its wave with `--slice <SLICE-ID>` per affected slice (every 5 rechecks
   per slice need a reslice review, as in Build). **Workflow Artifact bytes-only:**
   after `OFFLINE_RECOVERY`, a correction leaving every admission/`WA-*` row
   unchanged records `Workflow Artifact reviewed identity: <re-preflight identity
   digest>` below the admission block; when `check drift` reports only
   `reviewed-identity-only`, the reviewer is one fresh `devrites-code-reviewer` on
   the prior-source→re-preflight diff against those rows (no drafter or plan
   reviewer); green proceeds to step 8. Otherwise dispatch the exact plan reviewer once per
   fold — one dispatch covering every open fingerprint, preserving
   per correction/fingerprint accounting (each checked individually with its
   accepted findings, changed paths/criteria, new identity, and recorded delta
   self-check); it must return an explicit correction-created regression
   verdict over touched invariants plus every dependent of each changed clause
   (dep-graph and traceability lookup), not only fingerprint closure. Within one correction, no broad
   third loop. If it changes plan, fold again. A closed input plus a distinct Critical/Important invariant returns
   that new fingerprint as progress. Then close matrix and rerun ID/meaning audit.
8. **Build readback and readiness.** Add a cited five-line readback to
   `eng-review.md` (artifacts.md §7 rows 1–5): outcome/ACs; IN/OUT/must-NOT; UI direction and architecture/
   critical flow; slice order/first slice; decisive proof/action-time gates. No implementer should need to invent product, architecture, or proof.
   Contradiction, ownerlessness, or material ambiguity blocks via Clarify or Plan.

   Write exactly one `Implementation readiness: READY`, `NEEDS CLARIFICATION`,
   or `NEEDS REPLAN`. Root sets READY after every account, checklist,
   preflight, and sweep is green, including the
   [`spec-grammar.md`](skill://devrites-lib/reference/standards/spec-grammar.md) marker sweep whose
   `marker sweep:` line is recorded in `eng-review.md`; a kept hit blocks READY. Write phase/next step and emit one
   `Readiness inputs SHA-256` with
   `devrites-engine check readiness --emit-binding <slug>`; normal readiness check
   must pass, and it replays Build-entry `check slice` on every unbuilt slice, so
   READY needs each to pass (fix failures in `/rite-plan`). READY also needs every
   unbuilt slice's write set closed against the live tree (plan-reviewer
   dimension 6), so frontier gaps fold in one Plan repair, not one per slice; an
   affected recheck also closes every unbuilt slice and never defers a closure row. A `sequence_lookahead: yes` workspace also records one
   `Predecessor readiness: <predecessor> <digest>` line from the predecessor's
   `--emit-binding` hex; readiness re-checks it. Record the per-input drift baseline alongside it:
   `devrites-engine check drift <slug> --record` — a later stale binding then
   names the exact artifact that moved instead of "something changed". An `ADVISORY
   proportion:` line names a slice whose proof outgrew its ACs: move its rows without a
   `Proves` spec line to `Deferred hardening` before READY, never deepen them. Technical failure records reproduction, not qid. Human gap awaits
   Clarify. Optional cross-model follows `reference/cross-model.md` (trigger `cross-model`).

   With READY, no pending remediation, and a valid technical return cursor,
   restore and consume the return cursor instead of defaulting to Build. Preserve
   it through admitted remediation. Only a real stop reaches the human.
9. **Stop at the Vet boundary.** Show Build readback, scope verdict, lowest axis,
   closed gaps, preflight, action checkpoints, and critical failures. Recommend
   Build only when READY.

> Do not replace interactive review with artifacts, change acceptance through
> hardening, score without source evidence, or ignore unexplained complexity.

## Phase exit

**Complete when:** `eng-review.md` records exactly one readiness verdict, readiness
binding SHA-256 passes, and every required reviewer account is admitted.

**Failing case:** READY written while a required reviewer returned `Outcome: gap` →
not complete; restore NEEDS REPLAN or dispatch missing reviewer.
