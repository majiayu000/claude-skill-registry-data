---
name: orchestration
description: |
  Runnable driver for the deterministic campaign-execution protocol — the
  automaton that takes a validated campaign DAG to a correctly merged branch.
  Trigger when:
  - A campaign has a validated DAG + worker IBCs and the composer (or a
    cheap-tier runner) must DRIVE dispatch ⇄ reconcile as a loop rather than
    by hand.
  - Resuming a partially-executed campaign from its git history + sketch
    checkpoint after a halt or crash.
  - Prompt contains: /orchestrate, orchestration, drive the DAG, run the
    campaign, layer schedule, reconcile-and-merge, resume campaign.
---

# Orchestration: Driving the Campaign Execution Protocol

`/orchestrate` is the **runnable layer** that executes
[`docs/orchestration-protocol.md`](../../docs/orchestration-protocol.md) over a
live validated DAG. The protocol document is the **spec** — the exact procedure,
the exit-code routing, the four `[HUMAN SEAM]`s. This skill does not restate that
procedure; it *lifts it to a state machine a runner walks* and wires its abstract
steps to concrete repo commands. Where the spec says "assert the structural gate
exits 0," this skill says which command, with which arguments, and what each exit
code branches to.

It slots between [campaign](../campaign/SKILL.md)'s §DISPATCH and §RECONCILE —
the two steps campaign already delegates *by reference* to the protocol. Until
this skill is invoked, the composer drives the protocol by hand; invoked, it
drives DISPATCH ⇄ RECONCILE as a loop a cheap-tier runner can replay.

> [!IMPORTANT]
> **Non-duplication pointer.** This skill does **not** re-specify campaign
> mechanics. [campaign/SKILL.md §6 DISPATCH and §7 RECONCILE](../campaign/SKILL.md)
> own the *narrative* (what the council decides, the tier routing, the worker
> IBC contract); [docs/orchestration-protocol.md](../../docs/orchestration-protocol.md)
> owns the *deterministic procedure* (the pseudocode + exit-code rules). This
> skill is strictly the **driver**: it names protocol steps and sequences their
> commands. If you find yourself explaining *why* a step exists or *how the
> council judges*, you have left orchestration space — that prose lives in
> campaign and the protocol, link to it.

---

## Inputs (the driver's contract)

The protocol declares the inputs an orchestrator needs
([protocol §"inputs"](../../docs/orchestration-protocol.md), lines 19-24). This
skill makes them an explicit, **parameterized** contract — the protocol's
pseudocode and `ledger/derive/layers.ncl` reference the *project-state* DAG by a
fixed path; a driver run binds that path, it does not hardcode it.

| Parameter | Binds | Default (this repo) |
| :--- | :--- | :--- |
| `DAG` | the validated DAG artifact (YAML instance) — must pass `ledger/contracts/dag_apply.ncl` (`Dag ∘ DagNoConflict`) via `nickel export DAG --apply-contract ledger/contracts/dag_apply.ncl` | `.ledger/state/dag.yaml` |
| `LAYERS` | the Kahn-layering derivation that imports `DAG` | `ledger/derive/layers.ncl` |
| `PLAN` | the campaign plan (node intents, tier routing) | the campaign working set's `PLAN.md` |
| `PROMPTS` | the per-node worker IBCs handed at DISPATCH | `prompts/<node-id>-*.md` |
| `TOPIC` | the campaign topic — names the integration branch `campaign/<TOPIC>` and the sketch | the active flight-recorder slug |
| `MODE` | `AUTONOMOUS` (resolve seams by policy / escalate) or `INTERACTIVE` (surface seams to the head) | `INTERACTIVE` |
| `FORGE` | whether the origin remote resolves to a forge the project accepts contributions through — when present, the [forge skill](../forge/SKILL.md) is INVOKED at driver start (a named discipline loads, it is not remembered) and the [forge wiring](#forge-wiring) below applies | auto-detected |

`layers.ncl` imports `DAG` internally; pointing the driver at a different DAG
(e.g. a demonstration graph) means binding the import that `LAYERS` resolves, not
editing the derivation. The driver never improvises a schedule — it `nickel
export`s `LAYERS` and reads the result.

### Where the driver lives — the flight-recorder convention (machine-known)

The driver must LOCATE its own recorder and REACH neighboring context. The
convention is fixed, so both are mechanical, not discovered:

- **One sketch/ledger repo per org/project-umbrella.** The recorder is a git
  repo (here `.ledger/`, a nested repo) — not loose files.
- **Each project's history is a distinct branch** of that repo. The active
  campaign's project is the **current branch** of the recorder
  (`git -C <recorder> branch --show-current`; in this repo, the branch named
  for the project umbrella).
- **Sibling-project context is sibling branches.** A driver reaches "neighboring
  context" — a related project under the same umbrella — by reading another
  branch of the same recorder (`git -C <recorder> log <sibling-branch> -- log/`),
  never by leaving the repo or guessing paths.
- **Flight-recorder files live under `log/`** of the recorder; project-state
  artifacts (the DAG, reconcile log) under `state/`.

This lets the driver resolve its recorder, its branch, and its siblings by query
— and lets it *enforce* the convention (a campaign that writes loose sketch files
outside the recorder repo is malformed).

---

## Campaign setup (once, before the first dispatch)

Three environment hazards recur in worktree-per-node campaigns; each is
foreseeable, so each is closed at setup, never discovered under pressure:

- **Shared build output for compiled toolchains.** A campaign spawns many
  concurrent worktrees; a compiled-language project (Cargo, Go, …) left to its
  defaults builds a full per-worktree artifact tree and can silently consume
  the disk mid-campaign. Configure a **repository-scoped** shared build-output
  directory (e.g. a `.cargo/config.toml` at the project root — inherited by
  every nested worktree via config resolution) plus a build-parallelism cap
  that leaves the head's own concurrent work headroom. Repo-scoped, never
  machine-global: a machine-global cache collides with unrelated projects the
  head is developing on the same box.
- **Permission preflight.** Enumerate the sensitive actions the campaign will
  foreseeably need — above all the head-authorized final push of the
  integration branch — and ensure the harness permission environment allows
  them, so a mid-campaign classifier block never becomes the arbiter. A block
  that fires anyway is surfaced to the head as an environment gap; it is never
  routed around (in particular, never through a forge merge API).
- **Hook content runs from the main checkout.** Installed hooks are symlinks
  into the main checkout's tracked sources, live in every worktree with no
  reinstall — but a campaign branch that *edits* hook or gate sources is not
  live until those edits reach the main checkout. Nodes depending on changed
  gate behavior must account for that.

## State

The orchestrator's entire state is reconstructable from git + the sketch
checkpoint (rules.md §2 Prime Invariant 5; [protocol §State](../../docs/orchestration-protocol.md)).
Per node: `STATUS ∈ {PENDING, DISPATCHED, LANDED, ACCEPTED, REWORK, QUARANTINED, INVALIDATED}`,
its `worktree` and `branch`. Globally: `shared_branch` (the integration branch),
`tip` (the commit the current layer branches from), `layers` (the derived Kahn
schedule). No state lives only in the runner's memory — every transition lands in
git or the sketch.

### Resume = log-first temporal hygiene

Resuming a partial campaign is **reconstruction, not recall** (rules.md §7,
sharpened for episodic memory). The procedure is **log-first** and it is a hard
rule, not a convenience:

1. **The git log of the recorder is the index — the timeline.** Read
   `git -C <recorder> log --oneline -- log/` and the live `git log` (project
   tree). The recorder's campaign-lifecycle commits are subject-tagged: an
   episode opens with a `log: open <topic> …` commit and closes with a
   `log: close <topic> …` commit (the convention the sketch discipline writes).
   The log says *what happened, when, with what status* — which layers landed,
   which nodes are ACCEPTED, where the run halted.
2. **Discriminate CLOSED from in-flight by the log, not by reading the sketch.**
   A topic is **closed** iff its `log:` history contains a `close` commit for it
   with no later `open`:
   `git -C <recorder> log --grep='^log: \(open\|close\) <topic>' --format='%s'`
   — if the most recent matching subject is a `close`, the episode is finished
   (index entry only); if it is an `open` (or the topic has an open with no
   close), the episode is **in-flight**. This is the field the gate keys on; the
   sketch is never opened to decide it.
3. **Open ONLY the active campaign's sketch.** For the single in-flight episode
   (the topic whose latest `log:` marker is `open`, matching `TOPIC` / the
   current branch), full-read *that* sketch alone. Reconstruct `STATUS`, `tip`,
   `shared_branch`, and the RECONCILE_LOG cursor from it + git.
4. **Never exhaustively read prior sketches.** A *completed* campaign's flight
   recorder reads as in-flight to a naive walker — absorbing a finished goal's
   sketch as if it were live is a **context-pollution defect**. The log marker
   (step 2) *gates* whether a sketch is even opened: a sketch whose latest `log:`
   marker is `close` is an index entry, not working context. Only the in-flight
   episode is loaded.
5. **Boot-gate the reconstruction before resuming.** A reconstructed state is
   a CLAIM about history; validate it against the record before any dispatch:
   (a) the bound `DAG` still exports under `dag_apply.ncl`; (b) the reconcile
   log still exports under `reconcile_apply.ncl` — every recorded ACCEPT
   names its evaluator; (c) `adherence_audit.sh <baseline> <shared_branch>`
   exits 0 — every non-merge commit traces to a node branch; (d) status↔git
   coherence — every ACCEPTED node's branch is merged into `shared_branch`
   (`git merge-base --is-ancestor`), every DISPATCHED node's worktree exists.
   Any check failing → **HALT** and surface to the head: resuming past a
   corrupted or tampered record compounds the corruption. (Prior art:
   librecode's journal boot-gate, which replays the whole trajectory against
   its model invariants before any resume.)

The log is the map; exactly one sketch is the territory. (Prime Invariant 5,
"reconstruct, don't recall.")

---

## The driver state machine

The protocol's pseudocode (`DRIVE` / `RUN_LAYER` / `RECONCILE_AND_MERGE` /
`SURFACE_EXCEED` / `CLOSE`) lifts to a state machine: each protocol step is a
state, each exit-code rule is a transition. The runner walks the table; it never
chooses the next action — the table + the exit code compute it.

The `DERIVE` state writes the active-dag pointer (`$root/.ledger/active-dag`,
one line = the bound `DAG` path, relative-to-`$root` or absolute) once the
structural gate exits 0 — from that point every worker-worktree commit and
integration-branch commit enforces authority against the active plan (the commit
gate's authority overlay, `hooks/pre-commit §4`, reads line 1 of this file).
`CLOSE` — and any campaign-ending halt — clears it (`rm -f $root/.ledger/active-dag`)
so post-campaign ordinary commits revert to structural-only.

| State | Lifts (protocol) | Action (the wired command) | Transition |
| :--- | :--- | :--- | :--- |
| `DERIVE` | `DRIVE` head, "Derived schedule" | `nickel export DAG --apply-contract ledger/contracts/dag_apply.ncl` (structural gate — `DAG` is a `.yaml` instance); then `nickel export LAYERS` → `{layer_count, layers}`; on rc 0: `printf '%s\n' "$DAG" > $root/.ledger/active-dag` | export rc≠0 → **HALT** (the DAG is malformed; not a driver decision). rc 0 → create `shared_branch` from HEAD, `tip := HEAD`, `k := 0` → `RUN_LAYER` |
| `RUN_LAYER` | `RUN_LAYER` step 1 (`PARTITION`) | read `layers[k]`; split into `serial` (nodes with `serialize=true`) and `parallel := layer \ serial` — a *read of the validated DAG*, not a fresh conflict computation (`DagNoConflict` already proved the parallel set disjoint) | → `DISPATCH` for the parallel set |
| `DISPATCH` | `RUN_LAYER` step 2, `DISPATCH` | per node: `git worktree add .scratch/worktrees/<id> -b node/<descriptive-slug> <base>` — the worktree **directory** stays the generic node `<id>` (so dirs don't proliferate), but the **branch** is a descriptive slug so stacked branches/PRs self-describe; hand the worker ONLY `PROMPTS/<id>-*.md` + its discipline, opened with the [dispatch header](#the-dispatch-header-mandatory) — verbatim, every dispatch; `STATUS := DISPATCHED` | all dispatched → `AWAIT` |
| `AWAIT` | `RUN_LAYER` step 2, `AWAIT` | workers run autonomously, commit in their worktree under their discipline's commit gate, never push; collect each return under the [supervision invariants](#supervision-during-await) (idle = stopped; verify state directly; stalled → fresh handoff) | a worker FREEZE (surface-exceed) → `SURFACE_EXCEED`; FREEZE (refuted premise) → `REALIGN`; any other reserved halt → **[HUMAN SEAM]**; all returned → `RECONCILE` |
| `SURFACE_EXCEED` | `SURFACE_EXCEED` | `authorized.py --collision-check --path <req> --against-surfaces <concurrent surfaces>` | rc 0 (WIDEN) → widen node surface, re-validate DAG (`nickel export dag.yaml --apply-contract ledger/contracts/dag_apply.ncl`), resume worker → `AWAIT`. rc 3 (SERIALIZE) → mark `serialize: true` in the YAML, re-validate, re-schedule into `serial` → `RUN_LAYER` |
| `RECONCILE` | `RECONCILE_AND_MERGE` (1)-(5) | for each LANDED node in **node-id order**, run the boundary checks (below); compute `VERDICT`. **Process-adherence gate (first node only):** `bash ledger/gate/adherence_audit.sh <baseline> <shared_branch>` — rc 1 → **HALT** (accidental flat-commits detected — commits with no node/* branch witness; surface diagnostic to human before any merge proceeds) | `ACCEPT` → `MERGE`; `REWORK` → emit corrective delta IBC, re-dispatch from current tip, `STATUS := PENDING` → `DISPATCH`; `ESCALATE` → `REALIGN` or **[HUMAN SEAM]** |
| `MERGE` | `RECONCILE_AND_MERGE` (5) ACCEPT | **Merge-consent gate (before any `git merge`):** `bash ledger/gate/council_consent.sh <decision-ledger.yaml>` — rc≠0 → **HALT** (a `'merge` decision lacks the lead maintainer's recorded assent; green gates are necessary but never sufficient — the maintainer must affirmatively consent before the branch lands). Then merge the accepted node branch(es) into `shared_branch` with the strategy the situation calls for: a standard merge, or an **octopus** merge when a concurrent sibling layer lands together (the octopus legitimately makes a node branch the first parent — this is correct, not a bypass). Any merge strategy is valid; the adherence audit verifies worktree isolation by **branch reachability** (every non-merge first-parent commit traces to a node/* branch), not by merge shape. `STATUS := ACCEPTED`; mark mitigated findings | → `CHECKPOINT` |
| `BOUNDARY` | `LAYER_BOUNDARY` | (1) **cumulative-diff coherence gate**: `coherence_impact.sh --removed <cut-set>` over the layer's cumulative diff. (2) **DAG vs goal re-examination** ([campaign §Goal Supremacy](../campaign/SKILL.md)): does the remaining DAG still serve the goal? Warranted amendments are TIERED by the contract ([campaign §Amendment tiers](../campaign/SKILL.md)): MECHANICAL (closed M-list; contract provably preserved) applies on the architect's recorded assent; LOAD-BEARING surfaces as **[HUMAN SEAM]** — new work is a boundary the human signs off on before any affected node is re-dispatched; uncertainty defaults load-bearing. | coherence rc 1 → `ESCALATE`. rc 0, no amendment → advance the tip. rc 0, mechanical amendment → apply, record in the decision ledger, re-export `DAG + LAYERS`, advance the tip (third mechanical amendment on one node → tripwire, surface to the head). rc 0, load-bearing amendment → **[HUMAN SEAM]**: halt, surface; on ratification re-export `DAG + LAYERS`, then advance the tip. |
| `CHECKPOINT` | `RECONCILE_AND_MERGE` (6) | append a RECONCILE_LOG round (judged verdicts, freshness, realignments) to the active sketch; commit it in the recorder (`git -C <recorder> commit`) | more nodes in layer → `RECONCILE`; layer done → `BOUNDARY`; `BOUNDARY` rc 0 and `k+1 < layer_count` → `tip := shared_branch HEAD`, `k++` → `RUN_LAYER`; last layer → `CLOSE`. `BOUNDARY` rc 1 → `ESCALATE` → architect seat realigns the plan/DAG (PLAN), then re-dispatch |
| `REALIGN` | `REALIGN` | rewrite the node's premises/surface to current HEAD; if topology/surfaces change, re-export DAG + LAYERS (schedule may change); `STATUS := PENDING`; log it | → `DISPATCH` (or `RUN_LAYER` if the schedule changed) |
| `CLOSE` | `CLOSE` ([Dual-CLOSE Invariant](../../docs/orchestration-protocol.md#close)) | **(a) Deterministic path:** assert every finding MITIGATED/accepted + every node ACCEPTED; run the full deterministic surface over `shared_branch`, including `gates/check_internal_ids.sh <baseline>..<shared_branch>` (the whole-campaign ID-leak sweep over every line the campaign added — per-node checks cannot see a leak a later rework re-introduced); **process-adherence gate:** `bash ledger/gate/adherence_audit.sh <baseline> <shared_branch>` — rc 1 → **HALT** (accidental flat-commits in history — commits with no node/* branch witness). **(b) Adversarial path — sufficiency review:** dispatch decorrelated, context-free reviewers to audit whether the gate machinery is wired in and sufficient ("what does no gate check, what is defined-but-unwired, what claim is hollow?") — route findings to follow-up nodes or tech-debt records before acceptance. **Integration-drift sweep:** ONE final decorrelated MBSS sweep over the cumulative diff for cross-node integration drift no single boundary could see. **Retrospective + close record:** **emit the retrospective** to `.ledger/log/` (commit `log: close <topic> retrospective` — content per [campaign §CLOSE](../campaign/SKILL.md)); the retrospective MUST include a `## Sufficiency Review` section with substantive content (reviewers, convergence, findings — the orchestrator's content responsibility). **recorder-close gate:** `bash ledger/gate/recorder_close_check.sh <topic>` — rc≠0 → **HALT** (verifies BOTH the close entry AND that its `## Sufficiency Review` section is present with non-empty content; a hollow heading fails the structural floor — content quality is the adversarial reviewer's job, not the gate's); produce the campaign report; `rm -f $root/.ledger/active-dag` | → **[HUMAN SEAM]**: HALT for human final acceptance + any push |

`sort` is node-id order throughout: a fixed reconcile order makes the run
**replayable** — re-running from a checkpoint reproduces the same sequence.

### The dispatch header (mandatory)

Every dispatch prompt OPENS with this header — a literal template the
composer fills with the node's values, never prose re-derived per node
(inconsistent application is exactly how workers end up acting in a stale
sibling worktree):

```
WORKSPACE — confirm before any other action:
  cd <exact absolute worktree path>
  git branch --show-current          # MUST print: node/<slug>
  git merge-base --is-ancestor <base-tip-sha> HEAD   # MUST exit 0
  Any mismatch: HALT and report. Do not proceed under an assumed identity.

SANCTION: you run unattended in auto mode; no human is at your console —
the composer is your only channel. This dispatch under the active campaign
DAG is your standing authorization to commit at every logical boundary
within your declared file_surface. Leaving finished work uncommitted at
handoff is a protocol violation.

EVALUATORS: capture every exit code explicitly (`cmd; echo EXIT=$?`);
never report a status read through a pipe.

REPORT: end your walk by SENDING your final report through the channel
this dispatch arrived on — findings, verdicts, captured exit codes, and
where your artifacts and deposits live. Nothing you write is visible to
the composer unless you send it; a deposit does not deliver itself, and
stopping without a delivered report reads as a stall.
```

### Supervision during AWAIT

Three hard invariants govern the wait — each a recurring field failure when
left to judgment:

- **Idle means stopped.** An idle notification from an agent that has not
  delivered its final report means the agent has STOPPED and is waiting.
  Respond with an immediate status/report request — no lookback heuristic,
  no deferral. There is no "idle but still computing."
- **Verify state directly.** Before trusting any status message — and before
  accepting any "green"/"done" self-report — inspect the worktree: `git log`,
  `git status`, process state, disk timestamps. Piped exit codes and worker
  self-reports are not evidence; the header's explicit-capture rule exists
  because the piped-status failure recurred across independent workers.
- **A stalled worker gets a fresh handoff.** No report despite pings, and
  direct inspection shows no progress → dispatch a NEW agent into the same
  worktree and branch with a handoff brief (what is committed, what was
  claimed but unconfirmed, what remains). The composer never finishes or
  verifies the work itself — the role boundary holds precisely when breaking
  it looks small.

### JIT per-layer IBC authoring

The `DISPATCH` state hands each dispatched worker `PROMPTS/<id>-*.md` — but
not all IBCs are authored at the initial ORCHESTRATE pass. The rule:

- **Layer 0 IBCs** (nodes with no dependencies) are authored at the campaign's
  ORCHESTRATE step and approved in batch before the driver starts.
- **Later-layer IBCs** are authored **just-in-time at `DISPATCH` for that
  layer**, with the node's S1 premises re-verified against the layer's current
  `tip` (the integration-branch HEAD after the preceding `BOUNDARY` step).

**Why.** A later-layer IBC authored at ORCHESTRATE time makes S1 claims about
a world that does not yet exist — the upstream nodes have not landed. By the
time the driver reaches layer k, the integration branch carries k-1 layers
of accepted work; the JIT IBC describes *that* world, not the pre-campaign
snapshot. This is what makes the Premise Freshness invariant
([campaign §Premise Freshness](../campaign/SKILL.md)) mechanically honest at
the IBC-authoring boundary, not only at the RECONCILE freshness-check.

**What the driver does.** At `BOUNDARY`, after `tip` is advanced and before
`k++`:

1. For each node in `layers[k+1]` (the next layer), author or finalize its
   IBC with S1 premises verified against the new `tip` (cheapest tier — this
   is a mechanical freshness check, not a council judgment).
2. Gate each authored IBC: `nickel export` with `-I ledger/contracts` against
   `worker_ibc.ncl` (`Worker ∘ WorkerIBC`) must exit 0. An insufficient IBC
   is not dispatched.
2b. **Probe each authored IBC** ([boundary §Comprehension Probe](../boundary/SKILL.md)):
   a zero-context cheap-tier dry run against the new `tip` — unanswered
   questions or canary bites route the IBC back to authoring, never
   forward to dispatch. The contract gate (2) checks shape; the probe
   checks that a stranger can actually walk it.
2c. **Lint the surface**: `python3 ledger/gate/authorized.py --dag
   <exported-DAG.json> --ibc-surface-check <id> --ibc <exported-ibc.json>`
   — every path-bearing `context_map` entry must fall under the node's
   `file_surface` or carry an explicit `(read-only)` marker. rc 1 routes
   the IBC back to authoring (widen the surface or mark the entry), never
   forward to dispatch: this was the single most common IBC-authoring
   defect in the field, and every occurrence cost a worker HALT plus a
   full widen/re-dispatch round-trip that this lint closes for free.
2d. **Classify the review tier**: run the four review-tier triggers
   ([campaign §5 ORCHESTRATE](../campaign/SKILL.md)) against the node's
   surface and the validated DAG; record tier + fired trigger + convened
   seat in the routing-table row. No trigger → ROUTINE → the
   lead-maintainer's merge gate is the node's entire seat list.
2e. **Red-baseline check (implementation nodes)**: for each acceptance
   criterion whose evaluator is a test command, run the evaluator against
   the pre-node tip (`cmd; echo EXIT=$?`) and require FAILURE — a
   criterion already green before the work exists is not testing the
   work. Tests that do not yet exist route a **test-worker dispatch
   BEFORE the implementation dispatch, into the node's own worktree and
   branch** — the same workspace the implementer will then enter. The
   sequence is exact: test-worker commits the red suite on the node
   branch and returns → red-baseline gate confirms failure at that tip →
   implementation worker dispatches into the SAME worktree and branch,
   its workspace header naming the post-test-commit tip as its base. The
   two walks never run concurrently in the worktree; the sequence is the
   isolation, and the node's `file_surface` covers the test paths from
   authoring. (Shared campaign fixtures/golden vectors that multiple
   nodes cite are the exception — they belong to a fronted layer-0
   evaluator node with its own worktree and merge.) Drafting the failing
   acceptance tests is a protocol step, not implementation-worker
   discretion, so it cannot be skipped by a worker that "forgot" TDD.
   The implementation worker then receives the red suite as part of its
   boundary and must earn green without weakening it — a weakened or
   deleted acceptance test is a REWORK verdict at RECONCILE step (1),
   not a judgment call.
3. In `INTERACTIVE` mode, surface next-layer IBCs to the head before
   `k++` advances to `RUN_LAYER` for that layer.

The routing table (`ORCHESTRATION.md`) records tier assignments for all layers
upfront; only the full IBC text is deferred. A driver resuming from a
checkpoint re-reads the routing table and re-authors any pending IBCs against
the reconstructed `tip`.

### RECONCILE — the per-node boundary checks (the wired commands)

For each LANDED node (in node-id order), the `RECONCILE` state runs, in order
([protocol §RECONCILE_AND_MERGE](../../docs/orchestration-protocol.md)):

```bash
# (1) JUDGE THE CHANGESET — the worker's self-report is not evidence.
#     Re-run the evaluators the node's IBC names in its acceptance criteria
#     against its worktree. Any evaluator non-zero -> VERDICT := REWORK.

# (2) SURFACE HONESTY — derive the actual touched set, reconcile vs declared.
touched=$(git -C .scratch/worktrees/<id> diff --name-only <base>..HEAD)
python3 ledger/gate/authorized.py --dag <exported-DAG.json> \
    --reconcile-node <id> $(printf -- '--path %s ' $touched)
#   rc 0 -> stayed within declared surface
#   rc 1 -> undeclared touches: run SURFACE_EXCEED on each before proceeding

# (3) BIDIRECTIONAL COHERENCE-IMPACT — does this landing break landed/pending?
bash ledger/gate/coherence_impact.sh <repo-root> [--removed <workflow> ...]
#   rc 1 -> INCOHERENT (a machine-check failed): VERDICT := REWORK
#   rc 0 -> machine-surface coherent; record any decorrelated-review DISPATCH
#           lines and their converged verdict before ACCEPT (adversarial path)

# (3b) INTERNAL-ID LEAK — no campaign token in the lines this node ADDS.
bash gates/check_internal_ids.sh <base>..HEAD   # run in the node's worktree
#   rc 1 -> an added line cites a node/finding token: VERDICT := REWORK
#           (rewrite in repository terms; the record lives in .ledger, not
#           the artifact). Range mode scans added lines only — prior debt in
#           a touched file is not this node's verdict. Standing gate, not an
#           ad hoc close-time grep.

# (4) PREMISE-FRESHNESS — re-verify EVERY pending node against the new HEAD.
for p in <pending nodes>; do
  bash ledger/gate/premise_fresh.sh <p-id> <p's tripwire spec>
  #   rc 1 -> p INVALIDATED: REALIGN p's IBC before it dispatches
  #   rc 0 -> p stays FRESH
done

# (5) VERDICT: ACCEPT (1-4 incl. 3b clean, reviews converged) -> MERGE;
#     an acceptance evaluator that CANNOT RUN (absent or broken checker —
#     an absence, not a red result) -> QUARANTINE (see below);
#     else REWORK/ESCALATE.
```

### QUARANTINE — the degraded-gate path

A landed node whose acceptance evaluator **cannot run** — the checker is
absent, broken, or its fixture is missing; an *absence*, not a red result —
is neither accepted nor reworked. It is **QUARANTINED**: the landed work is
retained and the quarantine durably recorded in the reconcile log, but the
node is NOT proven. Two consequences, both hard:

- **A quarantined node blocks its dependents.** The dispatch precondition is
  dependencies ACCEPTED, and quarantine is not acceptance — the schedule
  genuinely does not advance past a pending gate.
- **The only exits are explicit.** DISCHARGE — the evaluator restored and
  re-run green, or the criterion closed by a converged decorrelated review
  (the adversarial path, reviewers named in the record) — routes to ACCEPT;
  a failed discharge routes to REWORK. Quarantine is never silently aged
  into acceptance, and no dependent's deadline argues it into one.

(Prior art: librecode's reference state machine, where this path is
property-tested — a pending deposit can never be marked proven, and a
dependent cannot dispatch past a quarantined parent.)

### BOUNDARY — semantic coherence over the cumulative diff (not just file-surface)

> [!IMPORTANT]
> **File-surface disjointness ≠ semantic independence.** `DagNoConflict` proves
> the parallel set's *file surfaces* are disjoint — it cannot see that a node's
> **cut or rename** orphaned a reference living in a *surviving* file owned by
> nobody in this layer. This campaign learned it the hard way: removing a
> workflow left dangling references the conflict gate was structurally blind to,
> and they surfaced at CLOSE instead of at a boundary. So the `LAYER_BOUNDARY`
> step ([protocol §LAYER_BOUNDARY](../../docs/orchestration-protocol.md)) runs a
> **semantic/reference-coherence gate over the layer's cumulative diff**, for the
> campaign's whole cut-set — not merely the per-node surface honesty of RECONCILE
> step (2). This is a genuine evolution of the protocol the spec now carries.

At each layer edge, before advancing the tip, `BOUNDARY` runs **one** command —
`coherence_impact.sh` already runs the contract export, the orphan gate
(`check_orphans` over the cut-set, internally at `coherence_impact.sh:88`), and
the markdown-link gate, so no separate `check_orphans` call is needed:

```bash
# coherence-impact over the LAYER's cumulative diff for the campaign's cut-set.
# Internally: contract export + orphan gate (over --removed) + link gate.
bash ledger/gate/coherence_impact.sh <repo-root> --removed <cut-1> --removed <cut-2> ...
#   rc 0 -> the layer is semantically coherent; advance the tip.
#   rc 1 -> INCOHERENT: a cut/rename orphaned a cross-node reference. The fault
#           is NOT localizable to one node (the broken ref and the cut that broke
#           it live in DIFFERENT nodes' surfaces), so it does NOT route to
#           single-node REWORK. It routes to ESCALATE -> PLAN: the architect
#           seat realigns the plan/DAG for the cross-node coupling, then
#           re-dispatches the affected nodes. (This campaign's own cross-node
#           couplings were resolved exactly this way — an architect-seat
#           plan-fault, not a node fault.)
```

This is a **boundary** gate (cumulative diff, whole cut-set), not the per-node
check — it catches cross-node orphaning a single node's reconcile cannot see.
Because index-sensitive evaluators give false failures while a worker has
uncommitted changes, `BOUNDARY` runs only at a **quiescent layer edge** (all of
this layer's worktrees merged or idle).

---

## Forge wiring

When `FORGE` is present, the driver surfaces the campaign per the
[forge skill](../forge/SKILL.md) — that skill owns the prose rules; this
section wires its acts to driver states:

| Driver state | Forge act |
| :--- | :--- |
| `DERIVE` (after gate rc 0) | create the shared integration branch from the baseline and **push it** (covered by the campaign's recorded push authorization — preflighted at setup). **Open NO PR** — a PR needs content to merge and the branch is empty until the first node lands; opening one here is the recurring bootstrap failure (forge §1) |
| `MERGE` / `CHECKPOINT` | surface each finished node as a **node PR targeting the shared branch** (forge MCP preferred; `gh` CLI fallback — forge §0); its consented merge lands in git and the push closes it. At the **first** node merge, open the **tracking PR** (draft, shared → default) with its checklist body (forge §2 — one `#N` item per node PR, checked as each merges), the first item already checked; thereafter keep the checklist and body accurate against the branch's *current* state, and post review findings + triage as PR comments (forge §3) as they occur, not retrospectively |
| `CLOSE` | mark the PR ready; the composer runs the **forge audit** (forge §5) over the final forge surface — the maintainer's consent covers the code, never the prose; the merge lands per forge §4 (in git, on the head's say-so; any push only under the head's recorded per-campaign authorization — rules.md §3's one exception) — the driver never merges or pushes |

No forge → this table is skipped in full; nothing else changes.

## Demonstration (the example test)

[`demo/`](demo/) is a recorded end-to-end run of this driver over a small
synthetic DAG ([`demo/dag.yaml`](demo/dag.yaml): 2 layers, a conflict-free parallel
pair, one `serialize` edge), with [`demo/layers.ncl`](demo/layers.ncl) the live
schedule derivation bound to that fixture. [`demo/TRANSCRIPT.md`](demo/TRANSCRIPT.md)
records every command and its actual gate exit code: schedule derivation →
worktree dispatch → the `authorized.py` reconcile checks → the `--collision-check`
serialize/widen routing (rc 3 / rc 0) → `premise_fresh.sh` → the node branch merge →
the `LAYER_BOUNDARY` coherence gate (GREEN rc 0 and a RED rc 1 → ESCALATE). A
reviewer reproduces the schedule with the `nickel export` commands at the top of
the transcript (YAML DAG validated via `--apply-contract dag_apply.ncl`).

---

## Outputs (the driver's deliverables)

- A merged `campaign/<TOPIC>` integration branch — every ACCEPTED node arriving
  via a merge into `shared_branch` (any strategy — octopus, fast-forward, or
  standard merge; isolation is verified by branch reachability, not merge shape),
  in layer-then-node-id order, branched from the advancing tip.
- An appended **RECONCILE_LOG** in the recorder (`state/reconcile_log.ncl` /
  the sketch): one round per boundary — judged verdicts, freshness results,
  realignments, the gate that justified each ACCEPT.
- **Sketch checkpoints** committed in the recorder after every reconcile: a
  crash resumes from sketch + git alone.
- A **CLOSE report** (the campaign report from REVIEW.md → outcomes) plus the
  final MBSS sweep verdict — produced at CLOSE, withheld of any push.

---

## The hermes seam — AUTONOMOUS vs INTERACTIVE

This skill carries the autonomy *seam* as an abstraction point; it is **not** a
programmatic hermes engine (out of scope). The protocol marks exactly four
`[HUMAN SEAM]`s ([protocol §automatability boundary](../../docs/orchestration-protocol.md));
everything else is deterministic-or-dispatched. **The table is EXHAUSTIVE:
between seams the driver advances node after node, layer after layer,
without pausing for permission — "continue to the next layer?" is not a
seam, it is approval theatre (a proportionality violation; campaign
§FORWARD_MOTION).** At each seam, `MODE` decides:

| Seam | Where (state) | `AUTONOMOUS` | `INTERACTIVE` |
| :--- | :--- | :--- | :--- |
| Final acceptance + push | `CLOSE` | resolve-by-policy is **forbidden** — a release is a sovereignty decision; HALT and escalate regardless | HALT; surface the CLOSE report; the head accepts, and any push runs only under the head's explicit per-campaign authorization — the law's one push exception (rules.md §3) |
| Non-resolvable reserved halt | `AWAIT`/`DISPATCH` | escalate to the head (a reserved predicate is, by definition, a head call) | surface the worker's freeze report |
| Decision-rights realignment | `RECONCILE`/`REALIGN` | resolve only if inside the IBC's declared sovereignty gates; else escalate | surface the realignment question |
| Non-converging adversarial review | `RECONCILE` step (3) | escalate (the dual escalates to human when decorrelated reviewers do not converge — rules.md §2 Invariant 1) | surface the divergence |

Push and final acceptance are **never** resolved by policy in either mode:
remotes belong to the human, and an agent pushes only under the head's
explicit per-campaign authorization (rules.md §3). The other three seams resolve by
policy in `AUTONOMOUS` *only when the call is inside a declared sovereignty
gate*, and surface in `INTERACTIVE`.

---

## Prior art (OSR1)

The worktree-isolated, dependency-layered, merge-at-boundary execution pattern
this driver implements is a well-established production pattern, not a novelty.
The grounding references are recorded in the **active campaign's flight recorder**
(the in-flight sketch under the recorder's `log/`, located by the resume
procedure above — `<recorder>/log/<active-topic>.md`, its OSR1 prior-art block)
per the [Outward-Search Reflex](../../ambient.md) and the
[prior-art](../prior-art/SKILL.md)
procedure: parallel `make -j` and Apache Airflow (DAG-derived independent units
run concurrently, dependents wait on upstreams) anchor the layering; Bazel's
per-action `execroot/` sandbox and `git-worktree` (one repo, many isolated
working trees from a common object store) anchor the per-unit isolation. The
driver's contribution is binding that pattern to git worktrees as the isolation
primitive and the Verification Dual's gates as the merge-boundary check (the
prior art integrates by artifact, not by a coherence-gated isolation check).

---

## See also

- [docs/orchestration-protocol.md](../../docs/orchestration-protocol.md) — the
  **spec** this skill drives (packaged-as note there points back here).
- [campaign/SKILL.md](../campaign/SKILL.md) — the architect-tier workflow whose
  §DISPATCH/§RECONCILE this skill makes runnable (the non-duplication anchor).
- [forge/SKILL.md](../forge/SKILL.md) — the conditional forge discipline
  the [forge wiring](#forge-wiring) table drives.
- the gate scripts the states name: `ledger/gate/authorized.py`,
  `ledger/gate/coherence_impact.sh`, `ledger/gate/premise_fresh.sh`,
  `gates/check_orphans.sh`.
