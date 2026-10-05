---
name: boundary
description: |
  Normative sufficiency conditions for Initial Boundary Conditions (IBCs)
  and the SOP for the cheap-tier boundary refinement loop (/boundary).
  Trigger when:
  - Crafting, auditing, or refining a prompt/IBC destined for an expensive
    (architect-class) model or an autonomous worker dispatch.
  - Evaluating whether a task frame is sufficient to bound an agent walk.
  - Prompt contains: /boundary, IBC, initial boundary condition, boundary
    contract, sufficiency conditions, worker prompt, prompt refinement.
---

# Boundary Protocol v1.0: IBC Sufficiency & Refinement

This skill defines what every Initial Boundary Condition (IBC) MUST possess
before an expensive walk is launched from it, and the cheap-tier refinement
loop that manufactures such boundaries.

The key words "MUST", "MUST NOT", "SHOULD", and "MAY" are to be interpreted
as described in BCP 14 (RFC 2119, RFC 8174).

---

## Philosophy: Optimize for Cheap Rejection

A good IBC is **not** one that maximizes the probability the walk succeeds.
It is one that makes the failure modes **cheap and early**. A wrong frame
can never be fully prevented at authoring time; what can be guaranteed is
that the walk detects and rejects it in its first few hundred tokens
instead of its last fifty thousand.

This follows from the cost asymmetry of cascade control: iterating in
boundary-space (cheap models + human revising a prompt document) costs
orders of magnitude less than iterating in trajectory-space (re-running an
architect-class walk). Error-correction iterations therefore belong in the
cheap outer loop. The expensive walk should launch from a fixed point
$\text{IBC}^*$ of the cheap refinement mapping and run as close to one-shot
as the task allows.

The most expensive failure mode of a high-capability walker is a
**confidently-wrong frame**: long-horizon coherence builds a large,
internally consistent structure on a false premise without the local error
signals that would trip a weaker model into visible incoherence. Premise
verification *before* the expensive call has the highest leverage-per-token
of any activity in the system.

### Trust as an Anti-Goodhart Mechanism

A micro-specified boundary induces a compliance posture: the walk optimizes
for letter-satisfaction of the rubric and produces rubric-satisfying,
goal-missing output. A boundary that grants explicit discretion over its
delegated questions ("these calls are yours; log your reasoning") shifts
the optimization target from *satisfy the spec* to *achieve the goal under
constraints*. The partnership dyad is structural, not sentimental:

- **Trust** = a non-empty delegated set with genuine discretion.
- **Focus** = a strictly bounded one, with halt predicates at the edges.

An IBC whose delegated set is empty wastes an architect on typist work. An
IBC whose delegated set is unbounded is a gamble, not a delegation.

---

## The Sufficiency Conditions

An IBC is **sufficient** when it satisfies all seven conditions below. Each
condition is independently checkable; adversarial reviewers in the
refinement loop MUST cite the violated condition by ID when raising an
objection.

### S1 — FALSIFIABILITY

Every premise the IBC asserts about the world MUST be stated so that the
receiving walker can verify or refute it against primary sources at low
token cost, and SHOULD name the exact check (command, file:line, document
section).

> ❌ "The auth module is well-tested."
> ✅ "`auth/session_test.go` covers token expiry; verify with
>   `go test ./auth/ -run TestExpiry`."

Rationale: what reliably triggers early fallback in a capable walker is a
*verifiable contradiction* between frame and world — vague unease does not.
A falsifiable premise is a manufactured tripwire.

The floor renders a premise as a CLOSED claim entry
(`ledger/contracts/entry.ncl`'s `Entry`, narrowed by `worker_ibc.ncl`'s
`PremiseChecked`): its `backing` names the evidence species (corroborated |
vouched | unclosed | residual), its `signer` designates who is asserting it,
and its `axes` records the author's own assessment of the claim's
coordinates (determined, certifiable, monotone) — required on every
premise, since an IBC author is obligated to assess the ground the dispatch
will stand on.

### S2 — REJECTION_GENRE

The IBC MUST state that rejecting the frame is a success condition, and
MUST define the rejection report format: which premise failed, the
refuting evidence, and what the boundary loop should reconsider. The
receiving walker's first obligation is a premise audit against S1's
tripwires; on failure it MUST emit the rejection report and freeze rather
than proceed.

Rationale: if halting has no genre, the walk invents continuation. An
explicit low-energy path to "no" is what makes early fallback reachable.

### S3 — DECISION_RIGHTS

Every question in scope MUST belong to exactly one of three sets:

| Set | Meaning | Obligation |
| :--- | :--- | :--- |
| **RESOLVED** | Answered during boundary refinement | Evidence attached (S1-grade) |
| **DELEGATED** | The walker's to answer — where the expensive tokens go | Discretion granted; reasoning logged |
| **RESERVED** | The human's to decide | Encountering one is a halt predicate, stated as a predicate |

A question that fits none of the sets is an unresolved unknown: the IBC is
not sufficient and MUST NOT be dispatched. Genuinely architectural
questions MUST NOT be fake-resolved at the cheap tier; ambiguities MUST NOT
be left for the expensive tier.

A question the refinement loop cannot yet resolve is carried forward in the
floor as an `unknowns` entry (`worker_ibc.ncl`'s `UnknownChecked`): a
question entry that MUST carry both a `discharge` condition (what would
close it) and a `closer` (who can) — a question missing either is not
routable, which is the same insufficiency this table already names.

### S4 — EVALUATOR_ATTACHMENT

Every constraint and every acceptance criterion MUST name the strongest
affordable deterministic evaluator that checks it, selected from the
evaluator hierarchy:

**machine-checked proof > type system > property test > example test >
linter > decorrelated adversarial review > [human: escalation only]**

In domains with formal models, a theorem statement is the perfectly
saturated acceptance criterion — the boundary contains its own evaluator
(see [formal-foundations](../formal-foundations/SKILL.md)). A constraint
with no evaluator attached is an exhortation, not a constraint, and MUST be
either grounded or moved to the rubric as a qualitative goal.

### S5 — CURATION_INTEGRITY

Context MUST be supplied as **pointers and verbatim excerpts** — file
paths, line ranges, exact commands, quoted spec clauses — never as
paraphrase. The boundary author's job is *selection*; the walker reads
primary sources directly. A summary written by a cheaper model injects its
misreadings as ground truth, moving the hallucination upstream where the
walker cannot detect it.

**Every context pointer declares its edit status.** A `context_map` entry
naming a file the walker may plausibly need to EDIT must be covered by the
node's declared `file_surface`; an entry that is context only carries an
explicit `(read-only)` marker. The mismatch — a file granted to the
walker's eyes but not its hands — is the most frequent IBC-authoring
defect observed in the field, and it fails at the worst point: the
walker's own commit gate, after the work is done. It is mechanically
checkable at authoring time (`authorized.py --ibc-surface-check`), and the
dispatching loop MUST run that lint before any dispatch
([orchestration §JIT authoring](../orchestration/SKILL.md)).

### S6 — AMENDMENT_PROTOCOL

The IBC MUST partition its clauses into:

- **Load-bearing:** amendment requires returning to the human (these
  overlap heavily with RESERVED decision rights and the goal itself).
- **Plastic:** the walker MAY revise under logged justification (tactics,
  sequencing, internal structure).

A boundary with no plastic region cannot survive contact with reality; a
boundary with no load-bearing region is not a boundary. Amendments to
plastic clauses MUST be logged where the dispatching loop can read them
(see [campaign](../campaign/SKILL.md) RECONCILE).

### S7 — DISCIPLINE_PROPORTION

Boundary mass MUST scale inversely with walker capability. Weaker walkers
do not need fewer constraints — they need a **smaller, prioritized
boundary**: rule overload causes silent prioritization failure (the walker
drops invariants it cannot rank).

- Each worker-tier IBC MUST name **exactly one** disciplining predicate
  workflow as its control loop (e.g. [refine](../refine/SKILL.md) for
  polish tasks, [core](../core/SKILL.md) TDD execution for feature steps)
  and MUST inline only the load-bearing rules for the task, omitting the
  rest of the global rule mass. A fast, cheap walker under the refine loop
  is a powerhouse; the same walker under forty ambient rules is a coin
  flip.
- Architect-tier IBCs MAY carry the full normative surface, but SHOULD
  still rely on gate-time boundary reconstruction (re-reading the live
  ledger) over initial rule mass: periodic reconstruction beats initial
  saturation for long horizons.

---

## Where approval attaches

Prime Invariant 6 requires a sufficient, **human-approved** boundary before
an expensive or autonomous walk. It does not say at what granularity that
approval attaches, and this skill and
[orchestration](../orchestration/SKILL.md) had drifted apart in the gap —
this document gating every IBC while the machinery that actually dispatches
approves layer-0 in batch, authors later-layer IBCs just-in-time, and names
pausing between layers approval theatre.

**The head ruled the granularity** (`.ledger/state/decisions-dispatch-granularity.yaml`,
`DG1`): approval attaches to the **frame that was discussed and agreed**,
never to each IBC. Inside an agreed frame, purely mechanical execution
proceeds autonomously and needs no further gate.

**What escalates is divergence, not cost.** "Expensive or autonomous" fires
on every dispatch and therefore discriminates nothing. A seam is genuine
when the work carries outstanding nuance, or when the path could depart
from what was agreed — S3's RESERVED set is this same predicate stated per
question. Encountering one is a halt, exactly as S3 says.

So the loop below runs where the frame itself is in question: the goal is
open, the premises are unverified, or the walk could reasonably diverge
from what was agreed. It does not run over a mechanical step inside a
frame the human already approved — there the IBC is checked against the
sufficiency conditions and dispatched.

## The Boundary Refinement Loop

`/boundary` manufactures $\text{IBC}^*$ as the fixed point of a cheap
contraction mapping. It is a meta-application of the
[refine](../refine/SKILL.md) loop where `CTX.TARGET_ARTIFACTS` is the IBC
document itself; the machinery (ledger discipline, adversarial sweeps,
grounded critique, convergence bounds) is inherited rather than restated.

```
DRAFT ──→ ATTACK     (adversarial sweep against S1–S7)
ATTACK ─→ REVISE     (grounded objections found)
       └─→ APPROVE   (zero grounded objections; human gate)
REVISE ─→ ATTACK     (loop)
APPROVE ─→ DISPATCH  (human approves IBC*; expensive walk launches)
        └─→ DRAFT    (human rejects; reframe)
```

1. **DRAFT:** Author the candidate IBC using
   [templates/IBC.md](../../templates/IBC.md). Drafting SHOULD run on a
   cheap tier; the human supplies the goal verbatim.
2. **ATTACK:** Spawn independent cheap-tier adversarial reviewers in
   mutually isolated contexts (MBSS semantics from refine). Each objection
   MUST cite the sufficiency condition it violates and the evidence;
   ungrounded objections are filtered exactly as in refine's verifier
   grounding. For contested framings — where reviewers disagree about the
   goal itself — apply the cross-model
   [dialectic principle](../../ambient.md#the-dialectic-principle) to the
   proposition "this IBC is sufficient to bound the walk."
3. **REVISE:** Resolve each objection by amending the IBC or rebutting
   with evidence. Premises raised to RESOLVED status MUST carry their
   verification evidence.
4. **APPROVE:** The loop converges when an attack sweep yields zero
   grounded objections. The human reviews $\text{IBC}^*$ and makes the
   dispatch decision. **This gate is mandatory:** no expensive walk
   launches from an unapproved boundary.

## The Comprehension Probe — empirical sufficiency

The ATTACK sweep argues about an IBC; the probe **simulates its
consumer**. Before an IBC dispatches an autonomous worker (campaign
worker IBCs especially — [campaign §ORCHESTRATE](../campaign/SKILL.md),
[orchestration §JIT authoring](../orchestration/SKILL.md)), run a
zero-context dry run:

- A cheap-tier agent receives ONLY the IBC plus the repository's
  committed record — no conversation history, no scratch, nothing the
  real worker won't have — and produces an implementation **plan**
  (never code) plus an explicit list of every question it cannot answer
  from those inputs.
- Score three things:
  1. **Unanswered questions** — each one is a boundary or documentation
     gap found for pennies instead of a mid-campaign freeze. Target ~0;
     iterate the IBC (or the committed docs it leans on) until the
     count flatlines.
  2. **Plan-vs-intent divergence** — the probe's plan is compared to
     the author's intended approach; divergence means the boundary
     underdetermines the walk (or the intent is wrong — both are
     findings).
  3. **Canary traps** — seed the probe with the project's known
     temptations (the doctrine traps its records name) and count the
     bites; a bite means the IBC's inline rules don't neutralize a trap
     the worker will face.
- The probe is an *empirical validator* of S1–S7, not an eighth
  condition: a failing probe always localizes to a violated S-condition
  (usually S1 premises assumed-not-stated, or S7 rules that didn't make
  the inline cut).

Probe cost is a cheap-tier read; skipping it trades pennies now for a
frozen worker later. For JIT-authored later-layer IBCs the probe runs at
authoring time, against the tip the worker will actually see.

---

## Prime Directives

1. **CHEAP_REJECTION_PRIMACY:** Never optimize an IBC for persuasiveness
   or completeness theater. Optimize for the receiving walker's ability to
   refute it cheaply.
2. **NO_EMPTY_DELEGATION:** An IBC for an architect-class walker MUST
   delegate at least one genuine question. If nothing is delegated, route
   the task to a cheaper tier.
3. **NO_PARAPHRASED_CONTEXT:** Violating S5 invalidates the boundary
   regardless of other conditions; summaries are not context.
4. **CONDITION_CITED_CRITIQUE:** Refinement-loop objections that do not
   cite a sufficiency condition ID and concrete evidence are filtered, per
   the Grounded Critique Invariant in [rules.md](../../rules.md).
5. **HUMAN_DISPATCH_GATE:** $\text{IBC}^*$ MUST receive human approval
   before an expensive or autonomous walk launches from it. Per `DG1` that
   approval attaches to the agreed frame, not to each IBC: a walk executing
   mechanically inside a frame the human approved carries it already, and a
   walk that could diverge from that frame does not — the latter is the
   seam, and dispatching it unapproved is the violation this directive
   names.

---

## AGENTS.md — the project-scope boundary

AGENTS.md is the **persistent project-scope boundary**: the durable anchor a
zero-context agent orients from before any walk begins. It is the slow-changing
record of goal, requirements, constraints, and known-unknowns that the per-
dispatch IBC (S1–S7 above) is projected from.

### Invariants (soundness — violation makes the file actively harmful)

- **Self-contained entrypoint.** A zero-context agent orients from this file
  plus its in-repo links. No assumed external knowledge; every pointer resolves
  in-repo or carries a URL.
- **Authoritative ⇒ true.** The *goal* is the desired end state (it steers the
  walk, not a status report). Factual/status claims are true, or marked **WIP**.
  Never conflate the two.
- **Single source.** Reference authorities ([rules.md](../../rules.md),
  [ambient.md](../../ambient.md), specs); never copy their text.
- **Agent-guiding only.** If removing a line changes no agent action, cut it.

### Required content

- **Goal** — the desired end state; why this exists.
- **Requirements / Invariants / Constraints** — the project's own (referenced
  if authoritative elsewhere).
- **Unknowns** — first-class, treated like requirements: the live
  known-unknowns, so the agent knows where the map is incomplete rather than
  assuming false certainty. Each unknown carries a **signpost** — what would
  resolve or invalidate it.
- **Operational entrypoint** — what to read first; build/test/validate; arsenal.
- **Structure** — what is core vs context-sensitive.
- **Alignment-to-parent** (non-root only) — how this component serves the
  parent goal (the defeater substrate).

### Anti-rot constraints

- **Minimal surface area** — every line is a liability kept true; brevity is
  anti-drift.
- **Freeform within the contract** — required content present; everything else
  is project-specific. A contract, not a template.
- **Stable / synced** — absorbs only reconciled truth; volatile context lives
  in `.scratch` and is promoted deliberately at reconcile boundaries.
- **Nesting-aware** — a subdirectory earns its own AGENTS.md only when it has
  a goal *distinct from and serving* the root; do not proliferate.

### Carrier roles

Unknowns and requirements both move forward via the same carrier stack:

| Carrier | Role | Cadence |
| :--- | :--- | :--- |
| **AGENTS.md** | Persistent anchor — goal, R/I/C, unknowns | Slow-changing; synced at reconcile |
| **Nickel context-map** | Live carrier — active requirements + unknowns with `grounding`, `last_validated`, `signpost` markers; fail-loud on omission (`last_validated` staleness is enforced against the HEAD commit date by [`tracker_fresh.sh`](../../ledger/gate/tracker_fresh.sh)) | Per-walk |
| **Flight log (`.ledger/log/`)** | Narrative/history — decisions, findings, pivots and their why | Append-only |
| **`.scratch` + sync** | Volatile draft; promotes validated changes → AGENTS.md | Ephemeral |

---

## Boundary Cadence

Boundary-setting is the **recurring self-conditioning operation**, not a
pre-flight checklist run once per campaign. It operates at three cadences:

- **Macro** (per-dispatch IBC) — the S1–S7 sufficiency conditions above; the
  human dispatch gate; the expensive walk launches from $\text{IBC}^*$.
- **Meso** (per-step reconstruction) — at the start of every step in a long
  walk, re-read the governing invariants and the active ledger rather than
  trusting accumulated context. Procedure in
  [ambient.md](../../ambient.md#boundary-reconstruction).
- **Micro** (per-decision query-shaping) — a standing disposition: before
  generating any substantive output, verify that the operative constraints are
  present in context. This is not a machinery step; it is the boundary skill
  applied as an attentional prior.
