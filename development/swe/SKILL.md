---
name: swe
description: Apply software-engineering standards when authoring or reviewing project plans, build/spec/PRD documents, architecture RFCs, or agent governance. Use for "write a plan", "review this build doc", "apply our SWE standards", or "is this plan ready to build"; also apply before drafting a project plan. Grades grounded recon, minimal scope, diagnosis, blast radius, and verifiable acceptance. This is a planning rubric, not a debugging or execution pipeline.
---

# SWE

Vibe the build; engineer the plan. This lens is the discipline that lets a fast v1.x ship without becoming a liability.

A governance overlay for **build/spec documents** — the "build v1.x" doc, the implementation spec, the architecture RFC. It does not debug code or pick a tradeoff in the moment; it reads the *plan* and asks whether the plan already embodies the engineering standards before a single line is written. Run it two ways: as an **authoring gate** (write the doc against it) or as a **review rubric** (read a doc, emit findings + a verdict). The whole bet: most plans fail not on the feature but on the five things below, smuggled past in prose — starting with Pillar 0, where the plan is grounded (or not) in the system as it actually exists.

## Pillar 0: Recon — is the plan grounded in a system anyone actually read?

The four pillars grade what the document *says*. Pillar 0 grades its **provenance**: was it written against the system as it exists, or from the prompt plus three grepped files? This pillar is about evidence, not consequences — what breaks when a *step* runs is Blast's job, below.

- [ ] The current system was traced before the first plan heading: entry points and call paths in, every read *and write* site of the state involved, the contracts crossed, the failure and rollback paths today.
- [ ] Claims about what the change touches cite code somebody read — `file:line`, not "various downstream."
- [ ] What could not be verified is listed as an explicit unknown with the command or file that would settle it, never smoothed into the findings.

**Applicability first.** Pillar 0 does not apply to greenfield work, a non-code plan, or a change contained to files the doc already quotes — mark it N/A and say why. Where it does apply, grade the *evidence*, not the artifact: a [recon](../recon/SKILL.md) Recon Map is the standard form, but a trace embedded in the doc or supplied by the author counts. **Block** only when the doc makes claims about an existing system that nothing behind it verifies; a thin trace on a genuinely small change is a **Fix**, not a Block.

**Pillar 0 feeds Blast; it does not satisfy it.** The trace establishes the *current-state* radius — who depends today on what the plan touches. Blast then asks what each proposed step *adds*: new systems, new data, new people, the shield, the tripwire, the undo class. Copying the map's radius into the Blast section unchanged understates the plan's own impact and fails Blast on its own terms.

## The four pillars

Each pillar is a lens on the document. A v1.x doc that satisfies a pillar contains the thing explicitly; a doc that "implies" it fails the pillar — implied is unbuilt.

### 1. Minimal (Ponytail) — does the plan earn each part it adds?

The plan's default answer to "add a thing" is *no*. Scope, dependencies, and abstractions are all liabilities until justified in the doc.

- [ ] Every new component answers "does this need to exist?" (YAGNI) — speculative scope is cut or deferred, not built.
- [ ] Sourcing ladder is honored to minimize mechanism, not requirements: stdlib → native platform feature → already-installed dep → one line of our own. A new dep names what it buys that the rung above does not. (Security and observability requirements are never simplified away, only implemented via the laziest viable mechanism).
- [ ] No premature abstraction — the plugin layer / framework / generic engine is justified by ≥2 concrete present uses, not one hypothetical future one.
- [ ] Bias is stated: delete > add, boring > clever, shortest diff that works. A complexity cap is named (e.g. stdlib-only, ~600-line ceiling) where it applies.

*Planning translation:* this is the editor pass on scope. Most v1.x bloat is decided here, in the doc, long before code.

### 2. Diagnosable (Mantra) — does the plan say how it will fail and be found?

A build doc that provisions zero observability is a debugging session deferred to production. Bake the diagnosis path into v1.x, not v1.next.

- [ ] Instrumentation is right-sized but explicit: a single actionable error log is better than an unread ELK stack, but silent failures are blocked. The plan names the exact log, metric, or alert that fires when it breaks.
- [ ] Every iterate/retry loop has a **stop condition** (e.g. 5-failure hard stop, 10-total cap). An unbounded "retry until it works" is a defect in the plan.
- [ ] Failures are made reproducible: the plan names how a failure is repro'd, and treats intermittent failure as a *signal* (concurrency / ordering / env / TOCTOU), not noise to retry away.
- [ ] State changes are auditable — append-only event log over in-place mutation where the history matters.
- [ ] **The plan names debug-mantra as its execution-time debugging protocol** — "we'll figure it out when it breaks" is a Diagnosable failure.

*Planning translation:* the runtime debugging ritual, pulled forward. If the doc can't say how you'll see it break, you'll see it break in prod.

### 3. Blast — does the plan price its irreversible moves before committing?

For every wide-impact or hard-to-undo step, the doc must already carry the cost. Don't dress a one-way door as a tweak.

- [ ] Each risky step names its **undo class**: easy / costly / one-way door. One-way doors are flagged, never silent.
- [ ] **Blast radius** is named — the exact systems, data, and people that break if this step goes wrong (not "various downstream").
- [ ] A **shield** is specified — flag, adapter, pilot/canary, dual-write, or an explicit "none."
- [ ] A **tripwire** exists for anything costly or one-way: *how* you'll know to pull it and *by when* (the point of no return). A shield with no tripwire is a brake with no warning light.

For the full per-decision accounting, defer to the **blast-radius** skill — this pillar only enforces that the v1.x doc *contains* that accounting for its irreversible steps.

### 4. Proof (Done) — can the plan prove it's finished, separately from claiming it?

Editor and grader are different roles. The plan must define "done" in terms something other than the author can check.

- [ ] Every task has a **measurable done-criterion** — a checkable output or metric, not "works" / "improved" / "robust."
- [ ] Tests are specified *and the plan requires they actually run* — "tests pass" means an execution artifact, not an assertion.
- [ ] **No orphan tasks**: every step maps to a success criterion, and every success criterion is covered by a step.
- [ ] **Closed loop**: For medium/large efforts, backend/data work must explicitly connect to a user-facing UI plane or final consumer. Fetching data without surfacing it to the user is an incomplete loop.
- [ ] **Observed vs. predicted is kept separate** — the doc never launders a projection ("this will reduce load 40%") as evidence. Predictions are labeled as such.

*Planning translation:* PlanProof's editor/grader separation at document scale. The grader reads only what's written, not what the author meant.

## House invariants

Non-negotiable conventions a v1.x doc must satisfy regardless of pillar. These are cheap to check and expensive to skip.

- [ ] **FSM threshold** — model an explicit state machine only past ~4 states; below that a flag or enum is leaner. Past it, an ad-hoc tangle of booleans is the defect.
- [ ] **Single write path** — one writer per piece of state. Multiple write paths to the same table/file are a race waiting to happen; name the single path.
- [ ] **Append-only event log** only when audit or history is an explicit business requirement (JSONL or equivalent); otherwise, simple in-place updates are the default.
- [ ] **UTC-only** time handling end to end; local time only at the display edge. "Nightly," "daily," "expires in 24h" all imply a timezone — pin it.
- [ ] **Crash-safe / idempotent jobs** — cron and background work are resumable and safe to run twice. A job that corrupts state on a mid-run crash is unshipped.
- [ ] **Checklist standard** — actionable items use the `- [ ]` hyphen prefix in GitHub-flavored Markdown, never bare `[ ]` in tables or lists.
- [ ] **Agent contract current** — for agent-built work, AGENTS.md / CLAUDE.md exists and matches the plan (conventions, loop caps, honesty constraints). The project's AGENTS.md must name SOLID compliance as a coding standard; if it doesn't, the plan has no enforceable code-design contract.

## Zero-Downtime Expand-Contract Schema & State Migration Rubric

When planning online schema changes, state re-encodings, or persistent data migrations across rolling deployments or mixed-version clients, the plan must budget lock/backfill rates, define stop/rollback tripwires, and enforce the 6-stage lifecycle:

1. **Stage 1 — Expand:** Add the new column, field, or data store as nullable or optional, with concurrent write synchronization in place so new writes populate both shapes without breaking existing readers.
2. **Stage 2 — Backfill & Continuous Sync:** Execute an idempotent, rate-limited background backfill. Any concurrent updates occurring during the backfill and mixed-version window MUST reach the new representation with an explicit conflict/ordering strategy.
3. **Stage 3 — Convergence Gate:** Run an automated parity/reconciliation assertion verifying data convergence across old and new representations before cutting over read traffic.
4. **Stage 4 — Switch Reads:** Redirect query and read paths to the new representation, retaining graceful fallback to the legacy shape if read errors occur.
5. **Stage 5 — Dual-Write & Mixed-Version Support:** Continue bidirectional synchronization / updating both representations for every representation still read by active versions, offline clients, or needed by application rollback throughout the entire mixed-version window.
6. **Stage 6 — Contract & Retire:** Ending legacy updates and dropping legacy fields/columns is strictly gated on:
   - (a) Full retirement and migration of all legacy writers.
   - (b) Full retirement of all legacy readers.
   - (c) Full retirement of delayed, queued, or asynchronous consumers.
   - (d) Closure of the application rollback window (or verified reverse synchronization if rollback occurs).

---

## How this differs from the sibling skills

- **swe** — "Does this *plan* embody our engineering standards before we build?" The standard/rubric, applied to a whole document.
- **recon** — "What is actually there?" The read-only trace of the current system that Pillar 0 grades the doc against. It supplies the current-state radius; Blast extends that radius per proposed step. Run recon first in author mode when the plan changes an existing system.
- **phase-0-spike** (an external workflow at `~/.claude/workflows/phase-0-spike.js`, not a skill in this repo) — the deep seam map, contract owners, and rollout invariants for a refactor that is already committed to. `recon` is the cheap universal pass before any plan; phase-0-spike is the expensive one after the refactor is approved. A v1.x doc for a subsystem refactor cites one or the other, never neither.
- **plan-adversarial-serial** — the *pipeline* (generate → review → revise → review → judge). It is the machinery; `swe` is one of the standards the machinery can enforce. Compose them: run the adversarial pipeline with `swe` as the lens content.
- **blast-radius** — "How big is *this one decision* and what breaks?" `swe`'s Blast pillar defers per-decision accounting to it.
- **iron-triangle** — "Which of speed/cost/quality is *this choice* trading?" When a plan forces fast/cheap/good tension, hand that node to it.
- **debug-mantra** — the four-step runtime debugging discipline (reproduce → fail path → falsify → breadcrumb). Diagnosable enforces the plan names it; debug-mantra governs live execution — composing across the doc/session boundary.
- **take-a-step-back** — "Is this the right problem/frame at all?" Runs *before* there is a plan to govern.
- **bottom-line** / **linear** — compress or sequence output. `swe` evaluates a plan's substance; those reshape its presentation.

Reach for `swe` the moment there is a build/spec document to hold to a standard — authoring one or judging one.

## How to apply

**Author mode** — you are writing the v1.x doc. Clear Pillar 0 first (run recon, or state why it was skipped), then use the four pillars and house invariants as the doc's skeleton: each feature passes Minimal before it earns a section; each risky step ships with its Blast block; each task ships with its Proof criterion. The lens is the gate, not a later edit.

**Review mode** — you are handed a v1.x doc. Walk Pillar 0, then the four pillars, then the invariants. For each gap, emit one finding keyed to the doc location (`§section`, or `file:line` for code-adjacent specs), tagged by severity, with the *cheapest* fix first. Close with a verdict. Do not rewrite the doc unless asked — surface the checkable gaps and let the author act.

## Project plan scaffold (Author mode)

When the ask is "write a project plan" / "write a plan" (authoring, not reviewing), clear Pillar 0 first, build the doc against the four pillars **and** lay it out in the fixed structure below. The structure is load-bearing, not decoration: the status table forces an honest "where are we" at a glance, the Table of contents keeps a long plan navigable, observable checklist items *are* the Proof done-criteria, and the per-phase QA checklist is the grader pass made mechanical. Implied is unbuilt — so every field below is written down, not assumed.

Required order, top to bottom: **frontmatter → status table → table of contents → phases (each with observable todos) → per-phase QA checklist**.

````markdown
---
title: <Project> — Build Plan
status: Not started | In progress | Blocked | Shipped
owner: <name>
created: <YYYY-MM-DD>   # UTC
updated: <YYYY-MM-DD>   # UTC — bump every time the plan changes
reversibility: Easy | Costly | One-way door — <one line of why>
---

# <Project> — Build Plan

| Most recently completed phase | What's next |
| --- | --- |
| — (not started) | Phase 1: <name> |

## Table of contents
- [Phase 1: <name>](#phase-1-name)
- [Phase 2: <name>](#phase-2-name)
- [Phase 3: <name>](#phase-3-name)

## Phase 1: <name>
**Goal:** <one observable outcome this phase delivers — not "work on X">

- [ ] <observable todo: names a checkable output or artifact>
- [ ] <observable todo>
- [ ] <observable todo>

### Phase 1 — QA checklist
- [ ] Every todo above produced its checkable output (no orphan tasks)
- [ ] Tests written **and run** — point to the execution artifact, not an assertion
- [ ] Diagnosable: logs + correlation id present; every loop has a stop condition
- [ ] Blast: each risky step names undo-class + shield + tripwire (or explicit "none")
- [ ] Status table and `updated:` date refreshed before this phase is marked done

## Phase 2: <name>
...
````

Filling it:

- **Frontmatter** — the at-a-glance contract. Keep `status`, `updated`, and `reversibility` honest; a stale `updated` date is the first sign the plan drifted from reality.
- **Status table** — exactly two columns, one row. It is the single source of truth for "where are we"; update it as the *last* step of finishing a phase, never before. Don't expand it into a multi-row log — that's what phases are for.
- **Phases** — split by observable milestone, not by calendar. Apply the Minimal pillar to phase count too: only as many phases as the work earns. Each phase has one `**Goal:**` line stating the outcome it delivers.
- **Observable todos** — every `- [ ]` names a checkable output, not an activity. "Add retry cap of 5 to the reconciler loop" passes; "improve reliability" fails. Use the `- [ ]` hyphen prefix (house Checklist standard), never bare `[ ]`.
- **Per-phase QA checklist** — closes each phase against the four pillars. It is Proof's editor/grader separation per phase: the boxes are checked by running things, not by the author asserting done. A phase isn't complete until its QA checklist is.

## Output format (Review mode)

Lead with the verdict in one line. Then findings, ordered by severity, then quick wins first within a severity. Keep it tight — clean plans get a short list, not a manufactured one.

**Verdict:** **Ship** · **Ship with conditions** · **Block** — [one sentence: the load-bearing reason].

**Findings:**

| Loc | Pillar | Severity | What breaks | Cheapest fix |
| --- | --- | --- | --- | --- |
| §x.y | Blast | Block | One-way migration with no rollback named | Add a dual-write window + a row-count tripwire before cutover |
| §x.z | Proof | Fix | "Improves sync" has no done-criterion | State the measurable signal (e.g. drift count → 0 over 3 runs) |

Severity: **Block** (cannot build safely as written — unguarded one-way door, no done-criteria, unbounded loop) · **Fix** (change before v1.x ships) · **Note** (improvement, optional).

**Quick wins:** [the 1–3 findings fixable in a line of doc, listed as `- [ ]` so the author can tick them off.]

## Principles

**Implied is unbuilt.** A plan gets credit only for what it states. "Obviously we'll log it" is a Diagnosable failure; write it down or it won't exist.

**Editor and grader are different roles.** The strongest constraint in the whole lens is Proof's separation: done is defined by something the author can't fudge. Keep them apart.

**Price the one-way doors loudest.** Reversible mistakes are cheap; irreversible ones are the only ones worth slowing down for. A tweak that can't be undone is not a tweak.

**Cut scope before breaking a corner.** When the plan is overloaded, the Minimal pillar and scope-reduction beat heroics. Defer to `iron-triangle` when the tension is explicitly fast/cheap/good.

**Stop conditions are not optional.** Any loop in the plan — retry, fix-iterate, agent relay — names its cap. Unbounded means undefined.

**Separate what you saw from what you expect.** Observed evidence and predicted behavior are different epistemic objects; a plan that blends them is lying to its future reader.

**Don't manufacture findings.** A genuinely clean v1.x doc gets "Ship" and a short list. The lens enforces a standard, not a quota of objections.

## Example — reviewing a v1.x build doc excerpt

Input (abridged):

> **§3 Nightly order reconciler.** A cron job runs each night to reconcile order state against the upstream system. For each order it pulls upstream status and updates `wp_orders` to match. On mismatch it retries until the write succeeds. This makes order state reliable.

Output:

> **Verdict:** **Block** — a nightly DELETE/UPDATE against the orders table with an unbounded retry, no tripwire, and no measurable "reliable" can corrupt order state with no way to know or stop it.
>
> **Findings:**
>
> | Loc | Pillar | Severity | What breaks | Cheapest fix |
> | --- | --- | --- | --- | --- |
> | §3 | Diagnosable | Block | "retries until the write succeeds" is an unbounded loop | Add a 5-failure hard stop / 10-total cap, then dead-letter the order |
> | §3 | Blast | Block | Bulk overwrite of `wp_orders` is costly-to-one-way with no shield/tripwire | Run in observe mode first; add a row-count + mismatch-rate tripwire before any write mode |
> | §3 | Proof | Fix | "makes order state reliable" has no done-criterion | Define it: drift count → 0 across 3 consecutive runs, logged |
> | §3 | House (UTC) | Fix | "each night" has no timezone | Pin the schedule to UTC; document the local display offset separately |
> | §3 | House (write path) | Note | Reconciler is a second writer to `wp_orders` | Name the single write path, or gate the reconciler behind the same one |
>
> **Quick wins:**
> - [ ] Add the loop cap (§3) — one clause.
> - [ ] Pin "each night" to UTC (§3) — one word.
> - [ ] Replace "reliable" with the drift-count criterion (§3) — one sentence.

## What success looks like

The author sees, before any code exists, exactly where the plan is a wish rather than a build: the loop with no cap, the migration with no rollback, the task that can't prove it's done. The best outcome is a v1.x doc that ships fast *because* its risky parts were priced up front — not one that ships fast and pays later.
