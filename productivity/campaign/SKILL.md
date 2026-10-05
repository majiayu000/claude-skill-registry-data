---
name: campaign
description: |
  SOP for the architect-tier campaign workflow (/campaign): exhaustive
  survey, mitigation planning, tiered orchestration, and reconciliation.
  Trigger when:
  - Running a multi-workstream initiative where an expensive architect-tier
    council surveys, plans, emits worker prompts, and judges landed work.
  - Conducting production-readiness assessments that fan out into
    autonomous mitigation dispatches across model tiers.
  - Prompt contains: /campaign, campaign workflow, survey, orchestrate,
    reconcile, premise freshness, tier routing, worker IBC, scratch.
---

# Campaign Protocol v1.0: Architect-Tier Orchestration

**Absorb → Survey → Plan → Orchestrate → Dispatch ⇄ Reconcile → Close**

This workflow defines the `/campaign` execution loop for architect-class
(expensive, long-horizon) walkers coordinating heterogeneous model tiers
across a multi-workstream goal. The council's primary output genre is
not code — it is **boundary conditions for cheaper walks**, and judgment
on the work that returns.

---

## Philosophy

### The Hourglass

Expensive tokens belong at the waist, not the edges:

```
  wide:   cheap tier + human  — boundary refinement (/boundary → IBC*)
  narrow: one council pass    — exhaustive survey, planning, orchestration
  wide:   cheap tier          — disciplined worker execution (/refine, /core)
          deterministic evaluators between every layer
```

The council ingests an approved $\text{IBC}^*$ (manufactured by the
[boundary](../boundary/SKILL.md) loop), saturates its shared context through
an exhaustive multi-agent survey, and emits a graph of saturated worker
IBCs routed to the cheapest capable tier. Error-correction iterations run
in cheap space; the council re-enters only to judge and realign.

### The Plan Is a DAG of Boundary Conditions

A campaign plan is not a task list. It is a **dependency graph of IBCs
whose premises reference world state that sibling executions mutate**.
When worker P3 lands an unexpected fix, the premises baked into pending
prompts P4–P9 may now describe a world that no longer exists. An open-loop
dependency graph drifts exactly like an open-loop token walk, only at a
coarser timescale. Hence two central invariants that are examined together
at every `RECONCILE` boundary:

> **Premise Freshness:** before dispatching any pending node, re-verify
> its IBC's premises (S1 tripwires) against current `HEAD`. A stale
> premise marks the node `INVALIDATED`; its IBC is realigned before
> dispatch.

> **Goal Supremacy / Mutable DAG:** execution yields exponentially more
> context than planning — the higher-level goal reigns over the
> pre-specified DAG skeleton, not the reverse. At every `RECONCILE`
> boundary the composer runs the cheap DAG-vs-goal check; the moment it
> suggests the graph no longer serves the goal, the architect seat is
> convened (this, not routine per-node review, is what summons it). DAG
> amendments — adding, editing, or removing nodes — are the
> **norm**, not a deviation; staying faithful to an arbitrary initial
> structure while overlooking what execution revealed is the failure mode
> this guards against. Each amendment routes to the architect seat and is
> TIERED by the contract (§Amendment tiers under RECONCILE): a MECHANICAL
> amendment proceeds on the architect's recorded single assent; a
> LOAD-BEARING amendment is ratified by the **head** before any affected
> node is re-dispatched.

Both checks are mechanical and cheap — they SHOULD themselves run on a cheap tier.

### The Council as Final Judge

Workers execute under their assigned discipline workflows, but
**no worker self-certifies**. Every landed changeset returns to the
council's `RECONCILE` state, which judges it with
[git-review](../git-review/SKILL.md) semantics against the worker's own
IBC: acceptance evaluators re-run, coherence checklist applied, commit
hygiene verified. The council is constantly judging whether the campaign
has proceeded correctly — that judgment, not code emission, is what the
expensive tokens buy.

### Readiness Is Measurable

Campaign failure is almost never the worker model failing to write code;
it is the *context* the code was written against — thin doctrine at the
point of work, prose seams two workers read differently, identity-bearing
surfaces with no machine gate, premises that drifted. All of that is
preparable, and preparation quality is **gaugeable before dispatch**:

1. **Evaluator coverage** — of the acceptance criteria on the DAG's
   path, what fraction carries a pre-built *machine* evaluator (a
   violation fixture, golden vector, lint, or law test) rather than an
   agent-check? Target ~100%; every agent-check residue is justified in
   the routing table.
2. **Comprehension-probe score** — every worker IBC passes the
   zero-context probe ([boundary §Comprehension Probe](../boundary/SKILL.md)):
   unanswered questions ~0, plan-vs-intent divergence resolved, canary
   traps not bitten.
3. **Seam-type completeness** — every DAG edge between nodes crosses a
   *committed, compiling* contract (type, trait, schema, fixture),
   never prose. Two workers meeting in the middle of a sentence is a
   defect class; count the edges.
4. **Red-test / golden-vector inventory** — nodes whose acceptance
   tests exist-and-fail before dispatch; serialization and identity
   surfaces with byte-exact golden vectors (where wrong is silent,
   vectors make it loud).

The counterweight is the **anti-over-preparation rule: prepare
evaluators and seams, never solutions.** Pre-written implementation code
goes stale and becomes premise-drift liability; the metrics above gauge
walls and rails, not pre-walked paths. The end-state test: every failure
available to a worker is either caught by a machine gate inside its own
loop, or is a genuine design discovery worth escalating — the metrics
exist to squeeze out the third category, the anticipatable stupidity.

### Working Set vs Flight Recorder

The campaign maintains two stores with different mutability and durability:

| Store | Role | Git status |
| :--- | :--- | :--- |
| `.scratch/<topic>/` | **Controller's live state** — the current boundary conditions, mutable and realigned as the campaign evolves | Ignored, never committed |
| `.ledger/log/` | **Flight recorder** — the trace from which the trajectory is reconstructed | Committed in the `.ledger/` subrepo |

```
.scratch/<topic>/
├── REVIEW.md           # Survey report (evidence-grounded findings)
├── PLAN.md             # Mitigation plan: the campaign DAG, living
├── ORCHESTRATION.md    # Routing table: node → tier → discipline
└── prompts/
    ├── P1-<slug>.md    # Worker IBCs per templates/IBC.md
    └── ...
```

> **Checkpoint Durability Invariant:** at every `RECONCILE` boundary the
> sketch records a checkpoint sufficient to regenerate the scratch state —
> which nodes dispatched/accepted/invalidated, what realignments occurred
> and why. A crash mid-campaign may cost working files, never the
> campaign: resume MUST derive from sketch + git alone.

---

## Scope

> [!IMPORTANT]
> `/campaign` is for multi-workstream initiatives where survey, routing,
> and reconciliation across model tiers pay for themselves. A single
> well-scoped change goes straight to `/core`; a single-artifact polish
> goes to `/refine`. Do not stand up a campaign for work one disciplined
> walker can finish — the orchestration overhead is itself a token cost.

---

## Grammar

The controller's session state — the live topic, phase, and context:

```yaml
# METADATA
TOPIC: "topic-slug"
STATUS: [ABSORB | CLARIFY | SURVEY | PLAN | ORCHESTRATE | DISPATCH | RECONCILE | CLOSE | HALT]

# CONTEXT
CTX:
  IBC_PATH: "path/to/approved/campaign/IBC"  # The boundary this campaign launches from
  GOAL: "Verbatim objective from the IBC"
  MODE: [INTERACTIVE | AUTONOMOUS]
  SCRATCH_PATH: ".scratch/<topic>"
```

The persistent campaign artifacts — the findings ledger, the campaign DAG, the
reconcile log, and the live context map — are **not** redefined here. Their
schemas are the locked Nickel contracts under
[`ledger/contracts/`](../../ledger/contracts), each authored as a pure-data YAML
instance and gated by a single `nickel export … --apply-contract` pass; the
contracts stay Nickel, the instances are YAML.

> [!IMPORTANT]
> **These four are STATE, and state lives in the RECORDER — never in
> scratch.** Each instance is authored under `.ledger/state/` and committed
> in the recorder sub-repo at every checkpoint. Findings especially are the
> surface the campaign re-derives context from ("did we miss anything?"):
> a findings ledger written to `.scratch/` is a findings ledger LOST to
> every future context, since scratch is disposable by law. Field campaigns
> diverged on this exact point — some wrote findings to the recorder, some
> to scratch — so the store is now explicit: `.scratch/<topic>/` holds only
> the narrative working set (REVIEW.md, PLAN.md, ORCHESTRATION.md,
> prompts/); the four contract-gated state instances live in
> `.ledger/state/`.

| Artifact | Apply-contract | Load-bearing invariant |
| :--- | :--- | :--- |
| Findings ledger (SURVEY) | [`findings_apply.ncl`](../../ledger/contracts/findings_apply.ncl) | **authored as YAML** (`.ledger/state/<topic>-findings.yaml`), validated via `nickel export <topic>-findings.yaml --apply-contract ledger/contracts/findings_apply.ncl`; a resolved finding (`'mitigated`/`'accepted_risk`) MUST name the `evaluator` that closed it; instances are YAML |
| Campaign DAG (PLAN/ORCHESTRATE) | [`dag_apply.ncl`](../../ledger/contracts/dag_apply.ncl) (`Dag ∘ DagNoConflict`) | the DAG is **authored as YAML** (`.ledger/state/dag.yaml` — the path the active-dag pointer and the orchestration driver's `DAG` input bind) and validated via `nickel export dag.yaml --apply-contract ledger/contracts/dag_apply.ncl`; each node's `discipline` is one of `core`/`refine`/`doc`/`form`/`spec`; the graph is acyclic, referentially whole, and concurrent nodes carry disjoint `file_surface` or a `serialize` marker; contracts stay Nickel, instances are YAML |
| Context map (tracker) | [`context_map_apply.ncl`](../../ledger/contracts/context_map_apply.ncl) | **authored as YAML** (`.ledger/state/<topic>-context_map.yaml`), validated via `nickel export <topic>-context_map.yaml --apply-contract ledger/contracts/context_map_apply.ncl`; every item MUST carry non-empty `grounding`, `last_validated`, and `signpost`; instances are YAML |
| Reconcile log (RECONCILE) | [`reconcile_apply.ncl`](../../ledger/contracts/reconcile_apply.ncl) | **authored as YAML** (`.ledger/state/<topic>-reconcile_log.yaml`), validated via `nickel export <topic>-reconcile_log.yaml --apply-contract ledger/contracts/reconcile_apply.ncl`; an `'accept` judgment MUST name the `evaluator` that justified it; instances are YAML |

The `evaluator` field and the `discipline` enum are the campaign's two
load-bearing couplings to these contracts: SURVEY and RECONCILE depend on the
Verification Dual being unforgeable (no resolution or acceptance without a named
evaluator), and ORCHESTRATE depends on `discipline` resolving to exactly one
surviving worker workflow. Read the contracts directly for field shapes; do not
restate them here.

---

## State Transitions

```
ABSORB ──→ CLARIFY      (premise audit fails or ambiguity found)
       └─→ SURVEY       (IBC* premises verified, scratch initialized)

CLARIFY ─→ SURVEY        (resolved; or rejection report returned to /boundary)
        └─→ HALT         (frame rejected; boundary loop must reconsider)

SURVEY ──→ PLAN          (findings ledger complete and evidence-grounded)

PLAN ───→ ORCHESTRATE    (human approves plan in interactive mode)
     └──→ HALT           (goal unreachable within appetite; report)

ORCHESTRATE ─→ DISPATCH  (worker IBCs emitted, routing table approved)

DISPATCH ──→ RECONCILE   (one or more nodes land, or a worker freezes)

RECONCILE ─→ DISPATCH    (accepted; fresh pending nodes remain)
          ├─→ ORCHESTRATE (realignment requires new/revised worker IBCs)
          ├─→ PLAN        (structural fault: the plan itself was wrong)
          ├─→ CLOSE       (all findings MITIGATED or ACCEPTED_RISK; DAG complete)
          └─→ HALT        (reserved predicate tripped, or budget exhausted)

CLOSE ──→ end            (final sweep passes; human accepts the report)
      └─→ RECONCILE      (final sweep finds regressions)
```

---

## States

### 1. ABSORB

Ingest the approved campaign $\text{IBC}^*$.

- **Premise Audit (boundary S2):** the council's first obligation is to
  verify the IBC's tripwires against primary sources. On contradiction,
  emit the rejection report and transition to `CLARIFY`/`HALT` — rejecting
  the frame early is a success condition, not a failure.
- Initialize `.scratch/<topic>/` and ensure `.scratch/` is git-ignored.
- Open the campaign sketch in `.ledger/log/` (flight recorder) and commit.
- **Run the environment setup** ([orchestration §Campaign setup](../orchestration/SKILL.md)):
  repo-scoped shared build output + parallelism cap for compiled
  toolchains, and the permission preflight (allowlist the campaign's
  foreseeable sensitive actions, above all the head-authorized final push)
  — proactively, never reactively after a disk-full or classifier block.
- **Detect the forge and LOAD the discipline.** The test is mechanical:
  does the origin remote resolve to a forge the project accepts
  contributions through? If yes, INVOKE the [forge skill](../forge/SKILL.md)
  NOW — named disciplines load, they are not remembered, and every forge
  reference in the states below assumes its law is in context. The
  discipline is REQUIRED wherever a forge exists; it is never deferred
  until a PR happens to come up.
- **Where the project has a forge, bootstrap the forge surface**: push
  the shared integration branch and open the campaign's **meta tracking
  issue** ([forge §6](../forge/SKILL.md)) — the durable index every
  out-of-scope finding will link from. The tracking PR is NOT opened
  here: it follows the bootstrap sequence ([forge §1](../forge/SKILL.md))
  and opens only once the first node's merge gives the shared branch
  content — a PR against an empty branch is the recurring field failure.

### 2. CLARIFY

Standard ambiguity gate. Interactive: surface to the head. Autonomous:
log a conservative assumption per [refine](../refine/SKILL.md) CLARIFY
semantics — except premise failures, which always freeze: a campaign MUST
NOT proceed from a refuted frame.

### 3. SURVEY

The expensive waist: saturate the council's shared context via exhaustive
multi-agent review of the target system.

- Fan out independent subagents — **survey-worker personas at cheap tier**
  (locate-and-excerpt with the remainder reported; never generic agents
  where the persona exists) — in mutually isolated contexts (MBSS
  semantics from [refine](../refine/SKILL.md)) across orthogonal angles
  spanning the goal's risk surface (correctness, security, proofs/specs,
  testing, docs-drift, performance — as the goal demands).
- The **Grounded Critique Invariant** ([rules.md](../../rules.md) §4)
  applies in full: findings without reproducible evidence are filtered.
- **The ruled-out space is part of the deliverable.** `REVIEW.md` and the
  findings ledger record not only what was found but what was considered
  and EXCLUDED — each ruled-out risk with the grounds that killed it and
  the condition that would reverse the exclusion. An analysis that cannot
  name what it ruled out has not established its coverage; the exclusions
  are what let RECONCILE and CLOSE distinguish "checked and clean" from
  "never looked".
- The council synthesizes `REVIEW.md` and the `FINDINGS` ledger. The
  council reads primary sources directly (boundary S5) — subagents
  locate and excerpt; they do not paraphrase on the council's behalf.

### 4. PLAN

Derive the mitigation plan from the findings ledger.

- Decompose into nodes sized for single-discipline worker walks, with
  explicit `DEPENDS_ON` edges and `MITIGATES` mappings back to findings.
- **Batch by default; justify splitting, never merging.** Per-node ceremony
  (IBC authoring, worktree, dispatch, merge-gate review, ledger round) is a
  large, mostly size-independent fixed cost — in the field it was the
  dominant driver of campaign wall-clock. One-node-per-finding is therefore
  a smell, not a discipline: batch every finding that shares a discipline
  and a compatible file surface into one node, with each finding keeping
  its own premise/constraint/acceptance entries inside that node's IBC (no
  loss of per-finding rigor or evaluator traceability). Split only when
  (a) surfaces are genuinely disjoint and parallelism pays, (b) a finding
  is large or risky enough to deserve isolated review attention, or
  (c) findings arrive at different times and batching would block ready
  work.
- For each node, decide what is **meaningful to verify** — the acceptance
  invariants (property statements, metamorphic relations, theorem
  statements where formal models exist). The architect seat owns the *what* of
  testing; workers implement the minutiae under TDD discipline.
- **Front-load the gates: layer 0 manufactures evaluators, not
  features.** The DAG's earliest nodes build the campaign's own
  verification surface — conformance fixtures, seam types/contracts,
  golden vectors, red acceptance tests — *before* any implementation
  node consumes them (§Readiness Is Measurable). Implementation nodes
  then cite these artifacts in their S4 evaluator commands. The
  **test-worker persona** is the dispatch vehicle for the red acceptance
  tests: it derives test invariants from the acceptance criteria and
  verifies each fails for the right reason, and the dispatching loop's
  red-baseline gate ([orchestration §JIT step 2d](../orchestration/SKILL.md))
  makes tests-before-implementation a protocol step no implementation
  worker can skip.
- Write `PLAN.md`. In `INTERACTIVE` mode, **HALT for the head's approval** of
  the plan before any orchestration.

### 5. ORCHESTRATE

Manufacture the worker boundaries.

- Emit one IBC per node into `prompts/`, using
  [templates/IBC.md](../../templates/IBC.md). Every worker IBC MUST
  satisfy the seven sufficiency conditions in
  [boundary](../boundary/SKILL.md) — in particular:
  - **S7 Discipline Proportion:** exactly one disciplining workflow
    (e.g. `/refine` for polish nodes, `/core` for feature nodes), with
    only the load-bearing rules inlined. A cheap walker under the refine
    loop is a powerhouse; the same walker under the full ambient rule
    mass silently drops invariants.
  - **S1 Premises:** each node's world-state assumptions stated as
    falsifiable tripwires — these become the freshness keys RECONCILE
    re-verifies.
  - **S4 Evaluators:** acceptance criteria carry their evaluator commands
    so RECONCILE can re-run them without trusting worker claims.
- Write `ORCHESTRATION.md`: the routing table mapping each node to the
  **cheapest tier whose capability bounds the task**, with rationale.
- **Classify every node's review tier in the routing table** — ROUTINE or
  EXCEPTIONAL, decided by a four-trigger checklist run at IBC authoring,
  never re-judged at reconcile. The row records the tier, the fired
  trigger, and the seat it convenes; absent a fired trigger the node is
  ROUTINE and its reconcile convenes the lead-maintainer's merge gate
  ONLY. The triggers:

  | Trigger | Fires when | Convenes |
  | :--- | :--- | :--- |
  | T1 shared contract | `file_surface` contains a public API, wire format/schema, or a type/contract imported by files outside the surface | architect |
  | T2 trust boundary | surface or goal touches authn/authz, crypto, secret handling, or parsing of input crossing the trust boundary | security lens (+ hacker seat when the node changes what the system guarantees) |
  | T3 irreversible | the effect cannot be undone by reverting the node's commits (data migration, data destruction, released-format change) | architect + head flagged at dispatch |
  | T4 downstream pivot | two or more later nodes name this node in `depends_on` (counted from the validated DAG) | architect |

  Uncertainty about whether a trigger fires is a fact question about the
  surface or the DAG — resolve it by reading them (or one survey
  dispatch), never by seating a review "to be safe."
- **Probe before dispatch:** each emitted IBC passes the zero-context
  comprehension probe ([boundary §Comprehension Probe](../boundary/SKILL.md));
  probe failures route back to the IBC (or to the committed docs it
  leans on), never forward to dispatch.
- **Lint the surface before dispatch:** every path-bearing `context_map`
  entry falls under the node's `file_surface` or carries an explicit
  `(read-only)` marker (`authorized.py --ibc-surface-check`). The gap this
  closes — a worker blocked by its own commit gate on a file the IBC told
  it to read but the surface forgot to grant — was the most frequent
  IBC-authoring defect in the field; the lint is mechanical and runs at
  authoring time, never relying on the worker's HALT.
- **Report the readiness numbers** (§Readiness Is Measurable) alongside
  the routing table: evaluator coverage with justified residue,
  seam-type completeness over DAG edges, red-test and golden-vector
  inventories, probe results. The numbers are part of what the head
  approves — dispatching on unmeasured readiness is open-loop.
- In `INTERACTIVE` mode the head approves the routing table and prompt
  set (the boundary skill's HUMAN_DISPATCH_GATE, applied in batch).

> [!NOTE]
> **JIT per-layer IBC authoring.** Not all worker IBCs are emitted upfront.
> Layer 0 (the earliest, dependency-free layer) IBCs are authored here, at
> the initial ORCHESTRATE pass, and approved in batch. IBCs for **later
> layers** are authored JIT — at the `DISPATCH` step for that layer, with
> premises (S1) re-verified against the current integration-branch `HEAD`
> (the `tip` advanced by the preceding RECONCILE round). Authoring a
> later-layer IBC before its prerequisite nodes land means the S1 premises
> describe a world that does not yet exist; re-verifying at dispatch time is
> what makes the "Premise Freshness" invariant mechanically sound rather than
> aspirational. The routing table (`ORCHESTRATION.md`) records the node-to-
> tier mapping for all layers upfront; only the full IBC text is deferred.
> Each JIT-authored IBC still passes the WorkerIBC contract before dispatch
> (`nickel export` gate); the contract is the sufficiency check, and it runs
> at the point of authoring, not at ORCHESTRATE.

### 6. DISPATCH

Launch workers on fresh nodes whose dependencies are `ACCEPTED`. The
deterministic team-execution model — the Kahn-derived layer schedule, a
worktree per node branched from the layer's start tip, the conflict-free set
dispatched in parallel with the rest serialized, each reconciled node merged
into the shared branch and the tip advanced per layer — is the
[orchestration protocol](../../docs/orchestration-protocol.md). That protocol
is the *mechanics*; the runnable workflow that drives DISPATCH ⇄ RECONCILE as an
automaton is the **orchestration skill** (`skills/orchestration/SKILL.md`),
which packages the protocol's evaluator commands and exit-code routing into a
loop a cheap-tier runner can execute. Invoke it (named disciplines load,
not linger) rather than driving the protocol by hand. The narrative:

- Workers run autonomously (e.g. under a `/goal`-style runner) inside
  their assigned discipline workflow, committing to the repository per
  [commit-hygiene](../commit-hygiene/SKILL.md).
- Parallel dispatch is permitted for nodes with disjoint file surfaces; the
  `DagNoConflict` contract proves the parallel set conflict-free, so the
  partition is a read of the validated DAG, not a fresh judgment. Nodes sharing
  surfaces carry a `serialize` marker and run one at a time, each isolated in
  its own worktree.
- A worker that trips a reserved predicate or rejects its boundary
  freezes and returns its report — that is the IBC working as designed. A
  surface-exceed halt and a refuted premise have deterministic resolutions
  (the surface-exceed protocol; realignment); any other reserved halt escalates
  to the head.

### 7. RECONCILE

The council re-enters to judge. The mechanical form of every step below —
its evaluator command and exit-code routing — is the
[orchestration protocol](../../docs/orchestration-protocol.md); that document
is what makes RECONCILE drivable by an automaton. For every `LANDED` node, in a
fixed (node-id) order, before merging it and before trusting the next node's
premises:

1. **Judge the changeset** with [git-review](../git-review/SKILL.md)
   semantics — `PURPOSE: verify node Pn's commits satisfy its IBC's
   acceptance criteria`. Apply the coherence checklist (scope alignment,
   atomicity, hygiene).
2. **Re-run the evaluators** named in the node's acceptance criteria
   (S4). Worker claims are not evidence; evaluator output is.
3. **Surface honesty.** Derive the node's *actual* touched set from its diff
   and reconcile it against its declared `file_surface`
   (`authorized.py --reconcile-node`). An undeclared touch routes through the
   **surface-exceed protocol** (collision-check vs concurrent surfaces →
   authorize-and-widen if disjoint, serialize if not), so the conflict
   guarantee stays honest rather than trusting a stale declaration.
4. **Bidirectional coherence-impact** — the per-landing drift gate, explicit:
   does this landing break an **already-landed** artifact, or invalidate a
   **pending** one? Machine-check it where an evaluator exists — re-run the
   orphan, link, and contract gates over the affected surface
   (`coherence_impact.sh`); for any concern no evaluator covers (meaning-level
   coherence), dispatch a decorrelated review (the Verification Dual's
   adversarial path). Breakage is caught at *this* boundary, not deferred to
   `CLOSE`.
5. **Verdict:**
   - `ACCEPT` — steps 1–4 clean and any dispatched review converged-pass.
     For a **routine node** this decision lives entirely in the
     lead-maintainer's merge gate: his **affirmative merge-consent** is the
     `reconcile-accept` (the delegation table routes both to him), and it is
     the ONLY seat a routine node's reconcile requires — green evaluators
     necessary, his consent the accepting act. Additional seats join a
     node's review only when its routing-table row says so — the node was
     classified **EXCEPTIONAL** at authoring because a review-tier trigger
     fired (§5 ORCHESTRATE), and the row names the convened seat; nothing
     is re-judged at reconcile, and the full bench convenes only at CLOSE.
     Inside his gate the maintainer may summon specialized review
     assistance (the test-reviewer persona on a test-touching diff, a
     security lens on a trust boundary) — his call,
     and the verdict remains his. On consent the node merges and is marked
     `ACCEPTED` with its mitigated findings. Where the project has a forge,
     the composer runs the [forge audit](../forge/SKILL.md) over the
     surfaced PR(s) alongside the merge-consent — the audit is the
     composer's (communication is conducting); the maintainer's gate is
     the code.
   - `REWORK` — an evaluator, surface, or coherence check failed: emit a
     corrective delta IBC (error feedback in cheap space) and re-dispatch;
     the node returns to `PENDING`.
   - `QUARANTINE` — an acceptance evaluator **cannot run** (absent or
     broken checker — an absence, not a failure): the landed work is
     retained and recorded, the node is NOT accepted, and its dependents
     do not dispatch. Exit only by explicit DISCHARGE — evaluator restored
     and re-run, or a converged decorrelated review recorded by the
     adversarial path — to `ACCEPT`, or a failed discharge to `REWORK`;
     never silently aged into acceptance
     ([orchestration §QUARANTINE](../orchestration/SKILL.md)).
   - `ESCALATE` — the fault is structural (the plan's, not the
     worker's): return to `PLAN` or `ORCHESTRATE` and realign.

Then, for **every** `PENDING` node, re-run the explicit **premise freshness
check** against the new `HEAD` (`premise_fresh.sh`, cheap tier): re-verify the
node's S1 tripwires; a flipped verdict marks the node `INVALIDATED` and its IBC
is realigned before any dispatch. Running this at *every* boundary — not once up
front — is what kills cross-node drift at the boundary instead of letting it
accumulate to `CLOSE`.

#### Amendment tiers — the contract decides, not feel

The head's PLAN approval ratified a CONTRACT: the set of node goals and
acceptance criteria — *what* is being built and what *done* means. Every
DAG amendment is classified against that contract, recorded either way:

- **MECHANICAL** (`dag-amendment-mechanical` — the architect's recorded
  single assent suffices; no head seam). The closed kind-list:
  - **M1** surface widen/narrow that passes the collision check (the
    surface-exceed protocol — already autonomous).
  - **M2** premise realignment against the new `HEAD` (REALIGN — already
    autonomous).
  - **M3** node SPLIT preserving the union of surfaces and criteria —
    none added, removed, or weakened.
  - **M4** node MERGE (batching) preserving all criteria, per the
    batching default.
  - **M5** sequencing/`serialize`-marker changes — schedule, not scope.
  - **M6** cutting a node made VACUOUS by landed work — provable: run its
    acceptance evaluators against the tip; all green means the work
    already exists.
- **LOAD-BEARING** (`dag-amendment` — head-ratified, exactly as always):
  anything that touches the contract — a criterion added, removed, or
  weakened; a node goal changed; genuinely new work; a surface where a
  review-tier trigger (T1–T4) fires; a coupled design decision.
- **Uncertainty defaults UP** — the opposite of the review-tier default,
  deliberately: an over-reviewed node wastes tokens, but a wrongly
  auto-applied amendment silently moves what is being built. Unclear =
  load-bearing.
- **Accountability, both tiers**: every amendment lands in the decision
  ledger with its classification and claimed kind; the process-auditor
  SAMPLES the classifications (a misclassification is a finding, a
  pattern is a bar trigger); and a THIRD mechanical amendment touching
  the same node is a drift tripwire — surfaced to the head even though
  each passed alone, because scope creep arrives as a series of
  individually-reasonable rescopes. The CLOSE retrospective reports
  every amendment's classification.

Finally: append the `RECONCILE_LOG` round, write the **sketch
checkpoint**, and commit it in the `.ledger/` subrepo. Reserved-predicate
breaches and appetite exhaustion route to the head (`HALT`).

### 8. CLOSE

> [!IMPORTANT]
> **Dual-CLOSE Invariant.** CLOSE requires two paths to close — not one.
> **(a)** the full deterministic gate suite exits green; **(b)** a
> decorrelated, context-free adversarial sufficiency review finds the
> machinery wired in and sufficient. A green gate suite is necessary but
> not sufficient: it proves execution, not coverage. The procedure is
> [docs/orchestration-protocol.md §CLOSE](../../docs/orchestration-protocol.md#close).

> [!IMPORTANT]
> **Fix beats accept-risk — the default is more nodes.** When residual
> findings remain at CLOSE, the composer's default proposal is **DAG
> amendment nodes that fix them**. `ACCEPTED_RISK` is the exception, not
> the offered default: it is argued per item, each with its named reason,
> and only for findings genuinely outside the campaign's stated scope (a
> different subsystem or repository, a deliberately deferred design
> question already on record) — never bundled into a blanket "accept
> these". Where the project has a forge, every accepted item gets its own
> tracked issue linked from the campaign's meta tracking issue
> ([forge §6](../forge/SKILL.md)): acceptance is a routing decision with a
> durable address, never a silent drop.

When all findings are `MITIGATED` or head-accepted as `ACCEPTED_RISK`
and the DAG is complete:

1. Run the full deterministic verification surface (complete test suite,
   linters, proof checkers where present) — the commit-gate scope, not
   the targeted-loop scope. **(Dual-CLOSE path (a).)**
2. Run one final adversarial sweep (MBSS) over the campaign's cumulative
   diff to catch cross-node integration drift no single worker could see.
3. **Run the sufficiency review.** **(Dual-CLOSE path (b).)** Dispatch
   decorrelated, context-free reviewers to audit whether the gate
   machinery is wired in and sufficient. Their question: "what does no
   gate check, what is defined-but-unwired, what claim is hollow?" —
   and their verdict includes the ruled-out space: the failure modes
   they considered and excluded, with grounds and reversal conditions,
   so a SUFFICIENT verdict is earned by visible attack rather than
   asserted. Route findings to follow-up nodes or tech-debt records
   before acceptance.
   When reviewers do not converge on a SUFFICIENT verdict, escalate to the
   head — this is a `[HUMAN SEAM]` at CLOSE.
4. **Emit a retrospective to the flight recorder** (`.ledger/log/`) before
   presenting the report to the head. The retrospective captures the
   hard-won context that survives context loss and compaction. It MUST
   include: original goal and what actually landed; execution-model and
   intellectual-capital lessons (surprises, realignments, what the initial
   DAG missed); open watch-items or residual risks; every DAG amendment
   with its tier classification (the mechanical kind it claimed, or its
   head ratification); a durability map
   (which artifacts are durable, which scratch is disposable); and a
   **`## Sufficiency Review` section** (reviewers, convergence verdict,
   and any findings routed to follow-up nodes or tech-debt records — the
   durable trace of path (b); the orchestrator's content responsibility).
   Commit in the `.ledger/` subrepo tagged `log: close <topic> retrospective`.
   The `recorder_close_check` gate enforces the structural floor: the close
   entry must exist **and** the `## Sufficiency Review` section must be
   present with non-empty content (at least one substantive line beneath
   the heading). A hollow heading fails. Content quality — genuine
   reviewers, honest convergence — is the adversarial reviewer's
   responsibility, not the gate's.
5. Produce the campaign report from `REVIEW.md` → outcomes: findings
   table with mitigation evidence, DAG execution trace, reconcile rounds,
   realignments, residual risks. Where the project has a forge, the
   composer runs the [forge audit](../forge/SKILL.md) over the campaign's
   whole forge surface — prose accuracy against final state,
   self-containment, the review record's visibility, tracking-issue
   completeness. The audit is the composer's own duty at CLOSE; the
   maintainer's attention stays on the code.
6. **HALT for the head's final acceptance.** Scratch MAY then be discarded;
   the sketch and git history carry the durable record.

---

## Prime Directives

1. **BOUNDARY_SUFFICIENCY:** The campaign launches only from a
   head-approved $\text{IBC}^*$, and every emitted worker IBC satisfies
   sufficiency conditions S1–S7. An insufficient boundary is not
   dispatched, ever.
2. **PREMISE_FRESHNESS + GOAL_SUPREMACY:** At every `RECONCILE` boundary,
   re-verify two things: (a) every pending node's premises against current
   `HEAD` (stale premise → `INVALIDATED`); (b) whether the DAG as a whole
   still serves the goal. DAG amendments are normal — mechanical ones
   applied on the architect's recorded assent, load-bearing ones
   head-approved (§Amendment tiers) — and open-loop dispatch of a stale
   or goal-misaligned DAG is a protocol violation.
3. **RETROSPECTIVE_AT_CLOSE:** Before the head's final acceptance, emit a
   retrospective to the flight recorder (`.ledger/log/`). Every campaign's
   hard-won context — what landed vs the goal, execution-model lessons,
   open watch-items, durability map — must survive context loss. The
   retrospective is a `CLOSE` step, not an afterthought. The retrospective
   MUST include a `## Sufficiency Review` section with substantive content
   (at least one non-blank, non-heading line beneath the heading) — a
   hollow heading or absent section fails the `recorder_close_check`
   structural floor and halts CLOSE. Content quality (genuine reviewers,
   honest convergence) is the adversarial reviewer's responsibility; the
   gate enforces presence and a non-empty floor only.
4. **DUAL_CLOSE:** A CLOSE that runs only the deterministic gate suite is
   incomplete. CLOSE terminates only when BOTH (a) the full gate suite
   exits green AND (b) a decorrelated sufficiency review finds the
   machinery wired in and sufficient. A green gate proves execution; it
   cannot prove coverage. Procedure:
   [docs/orchestration-protocol.md §CLOSE](../../docs/orchestration-protocol.md#close).
5. **COUNCIL_AS_JUDGE, PROPORTIONALLY:** No worker output is accepted without
   a `RECONCILE` judgment grounded in re-run evaluators — for a routine node
   that judgment is the lead-maintainer's affirmative merge-consent, the one
   hard-required seat; exceptional nodes additionally convene the seats or
   guests the composer judged warranted, and the full council (guests
   included) convenes only at CLOSE. Worker self-certification is void;
   so is reflexively convening the whole bench per node.
6. **LIVING_PLAN:** `PLAN.md`, `ORCHESTRATION.md`, and pending prompts
   are living documents — realignment when reality diverges is
   mandatory, and every realignment is logged with its why.
7. **TIER_ECONOMY:** Route every node to the cheapest tier whose
   capability bounds it. The architect-tier seats do not emit code for
   worker-shaped tasks; workers do not make architecture decisions.
8. **CHECKPOINT_DURABILITY:** `.scratch/` is never committed; the sketch
   checkpoints at every reconcile boundary so resume derives from
   sketch + git alone.
9. **DELEGATED_TDD:** The architect seat specifies the invariants worth
   verifying; workers implement tests and code under their discipline's
   closed loop, baseline failure included.
10. **READINESS_GATE:** No dispatch on unmeasured readiness. Layer 0
    manufactures the campaign's evaluators and seams; the readiness
    numbers (evaluator coverage, probe scores, seam completeness,
    red-test/vector inventories) are reported with the routing table and
    approved with it. Prepare evaluators and seams, never solutions.
11. **FORWARD_MOTION:** Between the enumerated human seams the campaign
    proceeds autonomously — node after node, layer after layer, without
    pausing to ask permission to continue. `INTERACTIVE` mode changes
    where the enumerated seams surface (to the head rather than resolved
    by policy), never the cadence of asking: "shall I continue?" on
    unblocked work is approval theatre, a proportionality violation. The
    seam list is CLOSED — a decision the delegation table does not route
    to the head is the council's to make and record, not the head's to
    be interrupted by.
12. **FORGE_WHEN_PRESENT:** Projects with a forge follow the
    [forge discipline](../forge/SKILL.md) — INVOKED at ABSORB when the
    mechanical forge test passes, never left to be requested (a named
    discipline loads, it is not remembered): self-contained PR prose,
    the bootstrap sequence, review-on-record, consent-to-merge, issue
    tagging, the forge audit at merge-consent and CLOSE. Projects
    without a forge owe nothing here.
