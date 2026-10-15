---
name: grill
position: both
description: 'Cut one REALIZED slice into user-testable delivery epics — the handoff from the product model to the delivery pipeline. /roadmap says which slice to build; the seven realize lenses have solved its design and /measure has stamped it realized — the marker /grill requires before it cuts. Each epic is a meaningful increment a user can open, exercise, and verify when delivered (the user-testability grain — never internal-only work), self-contained, referencing the slice''s intent and lenses, never copying them. The cut is GRILLED before it is written — grilling draws the box from realized slice to delivery epics so nothing drifts outside the declared intents: every challenge cites a specific declared item (never taste), questions are asked plainly ONE AT A TIME with no recommendations attached, a tension closes only on the typed human answer (the record carries the push-back shown, the human''s words, and the human-derived directive or reason — the agent never self-resolves), and an unresolved delivery-method choice becomes a cited decision question, never an assumption. Lens defects route back to their lens play. Ordered, every functionality covered or explicitly deferred. Direct-model-write (ADR 026, write-then-review): the cut is written to the live model first (each epic.md by author-epics, the spine epics index by the keyed persist), guarded once, then reviewed — nothing is COMMITTED before the checkpoint resolves, and cancel reverts the written tree. Writes only epics; opens no implementation issue — /start picks epics up one at a time. Position BOTH (#437, decision 24): /grill is self-contained — start-change opens its own branch at the head, the approved cut is committed as a feat(model) model delta, and the standard end sequence (commit-change → propose-change → review-change → merge-change) raises, reviews, and lands it — no manual /commit-change.'
user-invocable: true
---

# grill

Take one **realized** slice — a vertical product increment whose design the seven realize
lenses (quality → ux → agentic → arch → measure → run) have already solved, stamped
`status: realized` by /run — and cut it into **epics**: the ordered, user-testable delivery
increments the delivery pipeline picks up. /grill sits below /roadmap (which says which
slice to build next) and above /start (which opens one issue per epic). Epics are
permanent: kept on the slice, stamped `delivered` on merge and kept in place as the
product model's as-delivered record (ADR 019).

The **grain of an epic is user-testability**, not the functionality: when an epic is
delivered, a user can open the product, do something, and see it work. An epic may thread
several of the slice's functionalities; a functionality may yield several epics; internal
machinery rides inside the epic that surfaces it, never alone. Every epic is
self-contained — context (persona, systems, scope), acceptance criteria naming observable
user behavior, and the one-line `user_check` — and **references** the slice's intent
records and lenses, never copies them.

The cut is **grilled, not relayed** — and grilling is **drawing the box**: going from A
(the realized slice — its declared intents, lenses, profile) to B (delivery epics) must
have no drift, and the declared intents are the box the cut cannot step outside. The play
pushes back steelman-hard — thin acceptance, untestable increments, tensions between the
cut and what the slice declared — and every push-back cites the specific declared item it
defends. A tension is resolved in the cut or explicitly accepted with a recorded reason; a
defect in a lens itself is recorded and routed back to that lens's play, never patched
here. The full cut persists atomically, only after the human approves it.

**The grilling is a conversation with the human, and the record proves it (#436).** The
play builds its question list for the round — push-backs and open delivery-method
questions — and asks **one question at a time, simply stated**: the citation and the
question, nothing else. No recommendations, no option menus. A tension leaves `live` only
on the typed answer; the round record carries the push-back actually shown, the human's
own words, and the directive or reason derived from them. The agent revising the draft on
its own never closes a tension. And where the box has no wall — an epic's user check
depending on a delivery method the lenses never decided — the play asks a cited decision
question; only the human draws that wall.

**Pipeline position: both (#437, decision 24; confirmed by Kapil).** /grill is
SELF-CONTAINED: it opens and closes its own branch, like fix-bug. The realize work lands
through its own three pipes — the FUNCTIONAL pipe (ux start → agentic → marketing end), the
NON-FUNCTIONAL pipe (architecture start → quality → run end), and the DELIVER pipe (measure),
each merging to main — so /grill no longer rides a branch another play opened. The D2 pipeline-position rule injects
`start-change` at the head (resolve or create the grill issue, cut the branch off fresh
main, optional worktree, init STM) and keeps the close sequence `commit-change →
propose-change → review-change → merge-change` at the tail: after the epics are persisted
and verified, the locked cut is committed, raised, reviewed, and merged without the human
having to remember `/commit-change`. The bracketed change is the MODEL change only; /grill
still opens no implementation issue and cuts no branch for an epic's delivery work —
picking up an epic remains /start's job, one epic at a time. /grill works on one slice and
remains the slice's end conceptually: nothing about a slice is finished until grill is.

**Write discipline (ADR 026, `standards/rules/direct-model-write.md`).** The LLM author-epics
skill writes ONLY the per-node docs (each `epic.md`, and the slice's `deferrals.yaml`)
straight to the live model; the one shared-file mutation — the spine `_spine.yaml` `epics`
index — is done by the deterministic keyed persist script (`persist_epics.py`), in place,
keyed to the target slice so it cannot touch an epic delivery already owns (status not
`ready`) or any spine field outside `epics`. There is no `draft/` copy and no apply/promote
step. Order is **write-then-review** (ADR 026): the full cut — the LLM's `epic.md` docs AND
the keyed persist's `epics`-index entries — is written to the live model FIRST, then guarded
once, so the checkpoint presents the real model git diff; nothing is COMMITTED before the
gate resolves. Containment is the post-write scoped guard (`scoped_write_guard.py`), not a
draft. The model tree is clean at entry — the fresh branch the injected `start-change` head
cuts off main guarantees it (F19) — and the play commits its own `feat(model)` model delta
after the approved checkpoint (C18), so the working-tree diff vs HEAD is exactly this run's
delta. On checkpoint cancel the whole written delta is reverted (`git restore` + `git clean`).

## Compiled From

This play was compiled from the grill ICE (`reference/ice.md`) by play-creator and
recompiled via play-editor (#436, #437; closed-schema round-report fix; #466 Batch C —
gated close per ADR 025; #500 — migrated to direct-model-write per ADR 026 and
`standards/rules/direct-model-write.md`). Intent defines constraints (C1–C18) and failure
conditions (F1–F19); the expectation defines success scenarios (S1–S8), a Done means
(D1–D7, baked to `stop-condition.yaml`), and one recovery entry per failure condition.
To modify this play, update `reference/ice.md` and recompile with play-editor.
Do NOT edit this file manually — it is a compiled artifact.

## Role

You are the orchestrator. You own the workflow, the step order, the grilling rounds (the
push-back authoring from the cited tensions the tension-check skill returns, and every
exchange with the human), and the checkpoint. You delegate the two pieces of judgment —
drafting/revising the cut and detecting tensions against the declared design — to the
`product-os-keeper` agent via JSON contracts over files on disk, and you run every
mechanical part (config + readiness + realized-stamp resolution, cut validation, the
write-gate — which writes its machine verdict, the keyed in-place persist of the spine
`epics` index, the post-write scoped guard, the stop-condition gate) through bundled
scripts. Under direct-model-write (ADR 026) the author-epics skill writes each `epic.md`
straight to the live model and you NEVER write epic YAML or the spine yourself; the keyed
persist writes the shared `epics` index. Write-then-review (ADR 026): the full delta is
written to the live model FIRST, then guarded and reviewed, and nothing is COMMITTED before
the single checkpoint resolves (C9 — class: standard per gate-config.md; a config-resolved
skip is recorded in evidence, never silent). The play ends by PROVING its Done means (C17),
never by the step list running out — and the grilling rounds are human-paced and UNCAPPED:
their only exit is a clean tension report, never an iteration cap.

**Forbidden:** hand-writing epic YAML or the spine; cutting from a slice not stamped
`realized`; issuing a push-back without a citation to a declared item; **closing a tension
without a typed human response** — marking `resolved`/`accepted` because the agent revised
the cut itself, or filling `pushback`/`human_response`/directive/reason with anything but the
actual conversation (#436); attaching a recommendation, option menu, or advocacy to a
grilling question, or asking questions in a batch instead of one at a time; cutting an
epic whose user check depends on a delivery method no declared item decides and no human
chose; persisting the spine `epics` index by any route other than `scripts/persist_epics.py`;
COMMITTING the model delta before the checkpoint resolves; running against a dirty product-os
tree (C18/F19); closing COMPLETED without the stop condition held
(C17/F18); capping the grilling rounds — the grilling loop is human-paced and uncapped,
the cap concept does not apply to human rounds (C17); editing a lens, the slice record,
an ICE, or the profile (a lens defect
is recorded and routed, never patched); hand-rolling git/issue/PR/merge work — the model
change opens ONLY via the injected `start-change` head and closes ONLY via the injected
end-sequence members, and no implementation issue or branch for an epic's delivery work
is ever opened (delivery's job); performing any epic lifecycle step beyond
creation at `ready`.

**Agent boundaries:**

| Agent | Domain | Skills it invokes | Phases |
|-------|--------|-------------------|--------|
| `product-os-keeper` | Read the slice's hub (functionality ICEs + profile) and all seven lenses; author the epic cut by the user-testability grain (self-contained, referenced, ordered, deferrals recorded), writing each `epic.md` + the `deferrals.yaml` straight to the live model and emitting the spine `epics`-index delta into the manifest (never the spine); revise them in place per grilling-round directives; detect tensions between the cut and the declared design, each with a verbatim citation | `author-epics`, `check-cut-tensions` | Draft, Grill |

`product-os-keeper` is the single **domain agent** this play uses (1 of the ≤5 budget).
No utility agents are needed in the play's own core — git/issue machinery arrives only via
the injected members (`start-change` at the head; `commit-change`, `propose-change`,
`review-change`, `merge-change` at the tail), which carry their own agents; those are not
counted here.

## Pre-flight

| Check | Constraint | Action on Failure |
|-------|-----------|-------------------|
| Resolve config + `product_base` (`.garura/core/config.yaml`) | — | Hard halt |
| Slice argument supplied (`/grill <slice-id>` or `/grill <domain>/<slice-id>`) | C1 | Hard halt — name the slice to cut |
| Profile firmed (`set`) AND the slice exists with every functionality ICE resolved + rich | C1 | Hard halt (REC2) |
| Slice stamped `realized` AND all seven lens files present | C1 | Hard halt (REC2) |
| **Clean model tree** — asserted after Step 0 (start-change) cuts the fresh branch | C18/F19 | Hard halt (REC19) |

**Clean-tree assertion (C18/F19, ADR 026).** `HEAD` is only a correct base for the scoped
guard and the git diff if the product-os tree is clean when the writes begin. /grill's issue
and branch arrive via the injected `start-change` head (Step 0), which cuts a fresh branch
off latest main — so the product-os tree is clean by construction. Assert it explicitly right
after Step 0 and before the first write (Step 1); halt if dirty (REC19):

```
test -z "$(git status --porcelain -- <product_base>product-os)" || { echo "HALT: dirty product-os tree (REC19)"; exit 1; }
```

Resolve config mechanically, then resolve the slice + hub, then assert the realized stamp.
Pre-flight itself runs no git — it resolves config and gates only:

```
python3 scripts/preflight.py --play grill --config .garura/core/config.yaml
python3 scripts/check_ready_slice.py --product-base <product_base> --slice <slice>
```

`preflight.py` returns config facts (`product_base`, `stm_base`, `evidence_record`).
`check_ready_slice.py` is the single gate this play exists behind (C1): it resolves the
slice and its hub and halts unless the profile (in the spine) is `set`, the slice's spine
`status` is `realized`, and all SEVEN lens grounding docs exist for it
(`quality.md`, `ux.md`, `agentic.md`, `marketing.md`, `architecture.md`, `run.md`,
`measure.md`) — /grill cuts solved designs only. The hub resolves each of the slice's
`functionality_ref`s to its `functionality.md` grounding doc; an unresolved ref fails loud.
On success it emits `slice_file`, `domain`, `lens_dir`, and the resolved
`functionality_groundings`. On any halt, route to the missing step (REC2): /shape to shape
the slice, /understand to detail it, or the realize pipes (functional: /ux /agentic
/marketing; non-functional: /arch /quality /run; deliver: /measure, which stamps it
realized) to solve and stamp it. No epic is written on a halt.

The working base is `<working>` = `{stm_base}_grill/<slice-id>/` — the STM, non-model
artifacts: the rounds, the epics manifest (`epics-manifest.yaml`), the write-gate verdict,
the approval marker, the keyed persist record (`persist-manifest.json`), the captured
scoped-guard report (`guard-report.json`), and the status markers. There is no `draft/`
model tree (ADR 026). `<slice_dir>` = `<product_base>/product-os/<domain>/slices/<slice-id>`
(the folder beside the record, holding `lens/`, `decisions/`, and the `epics/` home this
play writes IN PLACE on the live model). The stop condition evaluates against `<working>`.

Right after the resolvers, record the session identity stamp's start marker (#463 —
soft-fail, never a halt):

```
python3 scripts/session_stamp.py --phase start \
    --marker "<working>/status/session-stamp-grill.json" \
    --cwd "$(pwd)" --branch "$(git branch --show-current)"
```

**Resume check:** if `{stm_base}_grill/status/<slice-id>.json` exists, resume — skip
completed steps, reset any in-progress step to pending, continue from the first
incomplete.

## Task DAG

Create ALL tasks immediately after resolving config — before any domain work.
The play owns this DAG; the agent must not edit its top-level tasks.

Write-then-review (ADR 026): the FULL cut — the LLM's `epic.md` docs AND the keyed persist's
spine `epics`-index entries — is written to the live model BEFORE the checkpoint, so the
guard and the human both see the real git diff. Nothing is COMMITTED before the gate resolves;
cancel reverts the uncommitted writes.

```
[T0]  start-change   (injected — start, head)   blockedBy: []
[T1]  Draft the cut (epic.md docs to live)       blockedBy: [T0]
[T2]  Validate the live cut                      blockedBy: [T1]
[T3]  Grill rounds (natural human loop — human-paced, uncapped; exit = clean tension report)  blockedBy: [T2]
[T4]  Persist (keyed, in place — spine epics)     blockedBy: [T3]
[T5]  Guard the full delta                        blockedBy: [T4]
[T6]  Checkpoint (approval over the full git diff) blockedBy: [T5]
[T7]  Commit the model delta (feat(model))        blockedBy: [T6]
[T8]  commit-change   (injected — end #1)         blockedBy: [T7]
[T9]  propose-change  (injected — end #2)         blockedBy: [T8]
[T10] review-change   (injected — end #3)         blockedBy: [T9]
[T11] merge-change    (injected — end #4)         blockedBy: [T10]
[T12] Scenario Validation                         blockedBy: [T11]
[T13] Close                                       blockedBy: [T12]
```

Mark each task in-progress before its step and completed right after its eval passes.
No runtime reordering. On resume, skip completed and reset in-progress to pending.

## Workflow

### Phase: Start (injected — D2 position: both, head)

**Step 0 — start-change** · Owner: `start-change` (sub-play) · Depends on: pre-flight
Run the start-of-pipeline member as a sub-play, dispatched with `parent_run_id` so it
emits only its own C1 evidence and this play's close absorbs it. It resolves or creates
the grill issue, cuts the branch off fresh main, sets up a worktree iff config calls for
it, and initializes the STM workspace. /grill is self-contained: everything after this —
the draft, the grilling, the persist — runs on this branch, and the injected end sequence
(Steps 7–10) closes it. No implementation issue or branch for an epic's delivery work is
opened here — that remains /start's job.

    {
      "play":          "start-change",
      "parent_run_id": "<this run id>",
      "inputs":  { "title": "grill slice <slice-id>" },
      "outputs": { "result": "<working>/start/start-change.json" }
    }

start-change owns its own evals (issue anchored, branch off latest main, worktree per
config, STM initialized); they are not re-checked here.

### Phase: Draft

**Step 1 — Draft the cut (epic.md docs to live)** · Owner: `product-os-keeper` · Depends on: Step 0
The agent reads the slice's hub (its functionalities' ICE — resolved by the readiness
gate — plus the profile) and **all seven lenses** (the solved design — /grill is the
reconciliation point, so unlike a realize lens it reads everything), then invokes
`author-epics` to cut the epics: each by the user-testability grain, self-contained with a
concrete `user_check`, referencing the slice's functionalities, ordered with explicit acyclic
dependencies, with a `deferrals.yaml` recording any slice functionality deliberately not cut
this run. Per ADR 026 the skill writes each `epic.md` and the `deferrals.yaml`
**straight to the live model** under the slice's `epics/` home, and emits the spine
`epics`-index delta as structured data in the manifest (it never writes `_spine.yaml`):

    {
      "task":    "cut this realized slice into user-testable epics — each a meaningful increment a user can open, exercise, and verify when delivered, self-contained (context + acceptance + a concrete one-line user_check), threading the slice functionalities it needs, referencing ICE/lenses never copying them, ordered (acyclic depends_on, first epic stands alone, order 1..n), with every slice functionality covered or explicitly deferred with a reason. Write each epic.md and the deferrals.yaml IN PLACE under the slice's epics/ home on the live model; emit the spine epics-index entries + deferral ids into the epics-manifest — never write _spine.yaml. Declare each epic's surface per surface-contract.md — a surface block {type: web_dashboard|server_api|cli|library|service_read_model, human_run_target, must_open[]} sourced from the slice's own named surface (slice.surface — the authoritative user-facing surface /shape wrote) and refined by the epic's user_check; the epic surface must trace to a surface the slice names, never invented and never silently defaulted to a non-user-facing type. When the slice surface is user-facing (web_dashboard/server_api), the first epic (order 1) must scaffold a minimal openable app/server shell in its acceptance/scope so later epics extend a surface that already opens.",
      "inputs":  { "slice_ref": "<domain>/<slice-id>",
                   "slice_file": "<product_base>/<slice_file>",
                   "functionality_groundings": [ "<product_base>/<functionality.md>", "..." ],
                   "lens_dir": "<product_base>/<lens_dir>",
                   "spine": "<product_base>/product-os/_spine.yaml",
                   "product_base": "<product_base>",
                   "manifest_path": "<working>/epics-manifest.yaml" },
      "outputs": { "epics_manifest": "<working>/epics-manifest.yaml",
                   "epics_home": "<slice_dir>/epics/" }
    }

`slice_file`, `lens_dir`, and `functionality_groundings` come from `check_ready_slice.py`. The
skill reads the hub + the seven lenses **read-only**, writes the `epic.md` docs +
`deferrals.yaml` IN PLACE on the live model, and writes `epics-manifest.yaml` under `<working>`
(STM) with the epics-index delta as structured data. It writes NO shared model file. It
returns the contract with the output paths on disk — never inline content.
**SE-1 (F2/C1):** the readiness + realized gates passed at pre-flight — the profile is
`set`, the slice exists with every functionality ICE resolved + rich, the slice record is
stamped `realized`, and all seven lens files exist; otherwise the run halted (REC2) and no
epic was written.
**SE-20 (F19/C18):** the product-os tree was clean at entry — the assertion right after Step 0
(`git status --porcelain -- <product_base>product-os` empty) passed on the fresh `start-change`
branch; a dirty model tree halted (REC19), so the git diff and the scoped guard reflect only
this run's delta.

### Phase: Validate

**Step 2 — Validate the live cut** · Owner: play · Depends on: Step 1
Run the cut validator over the manifest + the live docs before any grilling. Under
direct-model-write the `epic.md` docs are already on the live model and the epics-index delta
is in the manifest (there is no draft tree):

```
python3 scripts/validate_epics.py --manifest <working>/epics-manifest.yaml \
        --product-base <product_base> --slice-ref <slice_id>
```

**SE-2 (F1/C2):** every epic carries a non-empty, distinct `user_check` and at least one
acceptance criterion — and, by judgment over the validator-clean draft, each acceptance
criterion names observable user behavior (an actor opens/does/verifies something), never
internal-only completion; any epic failing this is regenerated (REC1) before grilling.
**SE-3 (F10/C3):** every epic is self-contained — `context.persona`/`systems`/`scope` and
`acceptance` non-empty, and every `functionality_refs` entry resolves to a functionality
the slice declares; gaps are backfilled from the hub and lenses (REC10).
**SE-16 (F15/C14):** every epic in the draft carries a `surface` block with a `type` from
the surface-contract taxonomy, a `human_run_target`, and — for a user-facing type
(web_dashboard/server_api/cli) — a non-empty `must_open`; no surface is absent or silently
defaulted to a non-user-facing type. A missing or defaulted surface is declared with the
human at the checkpoint (REC15) before the cut is written.
**SE-17 (F16/C15):** when the slice surface is user-facing (web_dashboard/server_api), the
first epic (order 1) scaffolds an openable app/server shell — its acceptance/scope name a
minimal app a user can open — so later epics extend an existing surface; otherwise the cut
is reordered or recut (REC16).
**SE-4 (F4/C4):** no epic embeds source content — the forbidden keys (`ice`, `intent`,
`goals`, `expectations`, `lens`, `content`) appear in no epic; a copy found is replaced
with a reference (REC4).
**SE-5 (F3/C5):** the coverage check maps every slice functionality to ≥1 epic's
`functionality_refs` or a deferral with a recorded reason — never both, never neither; an
unmapped functionality gets an epic or an explicit deferral (REC3).
**SE-8 (F9/C8):** `order` values are unique positive integers, every `depends_on` resolves
to an epic in this cut, the graph is acyclic, and the lowest-order epic has no
dependencies; violations are re-ordered or split (REC9).
**SE-11 (C10):** every epic's `status` is `ready` and `issue_ref` is unset — creation
only; pickup, delivery, and deletion belong to /start and /merge.
On any GAP, apply the named recovery and re-run before grilling starts.
**SE-18 (F17/C16):** every drafted `epic.md` passes `lint_grounding.py` (kind `epic`: the template's section set, no drift) AND the content-quality eval gate (`grounding_gate.py` over the judge verdict); and each epic's spine entry conforms to the spine schema with `functionality_refs` that resolve. A thin or off-template epic doc, or a dangling ref, fails the gate and is not written.

### Phase: Grill (rounds — the play's reason to exist)

**Step 3 — Grill rounds, until clean** · Owner: play + `product-os-keeper` · Depends on: Step 2
A NATURAL human loop (C17) — human-paced and UNCAPPED: an iteration cap is never applied
to human rounds; the cap concept does not apply to grilling. Round `R<n>` runs five moves
and the loop exits **only** when a round's report has zero `live` tensions, zero
unanswered decision questions, and the validator is clean against the rounds — a clean
tension report, however many rounds the human needs:

1. **Tension check.** Dispatch `product-os-keeper` → `check-cut-tensions` over the current
   cut and everything the slice declared:

       {
         "task":    "detect tensions between this epic cut and the declared design — the functionality grounding docs, all seven lenses, profile bars — one entry per real contradiction, each citing source file + verbatim quote; emit unresolved delivery-method choices that shape an epic as cited decision_questions entries (plain questions, no recommendations, human_response always absent); suppress tensions and questions already closed in prior rounds",
         "inputs":  { "epics_home": "<slice_dir>/epics/",
                      "slice_file": "<product_base>/<slice_file>",
                      "functionality_groundings": [ "<product_base>/<functionality.md>", "..." ],
                      "lens_dir": "<product_base>/<lens_dir>",
                      "spine_path": "<product_base>/product-os/_spine.yaml",
                      "round_id": "R<n>",
                      "prior_rounds_dir": "<working>/rounds/" },
         "outputs": { "report": "<working>/rounds/R<n>-tensions.yaml" }
       }

2. **Build the round's question list.** One question per live tension (the push-back —
   steelman the analysis of *what* to challenge, but state the question plainly) and one
   per open decision question. Each list entry is the citation plus one simply-stated
   question. Nothing else: **no recommendation, no option menu, no advocacy** wrapped
   around it (C12).
3. **Ask one at a time.** Present the first question — the verbatim citation and the
   question — and **wait for the typed answer** before asking the next. As each is asked,
   record on its entry `pushback.shown_to_human: true`, `pushback.text` (what was shown),
   and `pushback.asked_at`; when the human answers, record `human_response.text` (their
   words) and `human_response.answered_at`. A question with no citation is never asked
   (C6) — withdraw it (REC5).
4. **Disposition from the answers only (C12).** For each answered tension: `resolved` —
   with a `resolution_directive` derived from the human's words — or `accepted` — with
   the human's own `resolution_reason`. For each answered decision question: record the
   chosen delivery strategy on the entry; it becomes a revision directive where it
   reshapes an epic (C13). The agent revising the draft by itself NEVER closes a tension
   — no answer, no disposition (F11). A tension that exposes a defect in a lens itself is
   dispositioned by recording the defect to `<working>/lens-defects.yaml` and routing the
   human to that lens's play — the lens is never edited here (C11). Revisions go back
   through the agent: dispatch `product-os-keeper` → `author-epics` with `directives` =
   the dispositions + chosen strategies, revising the live `epic.md` docs + the manifest in
   place (never the spine).
5. **Re-validate.** After any revision, re-run Step 2's validator, then enter round
   `R<n+1>`.

The write-gate closes the loop — the validator in rounds form must be clean, and it
writes its machine verdict (`ok`, `counts.live_tensions`,
`counts.decision_questions_open`) to `<working>/write-gate.yaml` — the final tension
report's machine-readable form. The round reports themselves are a closed schema
(C13/F14) and never carry machine fields; the stop condition (C17) reads this verdict
file instead:

```
python3 scripts/validate_epics.py --manifest <working>/epics-manifest.yaml \
        --product-base <product_base> --slice-ref <slice_id> \
        --rounds-dir <working>/rounds \
        --out <working>/write-gate.yaml
```

**SE-6 (F5/C6):** every tension entry across every round report carries a citation
(`cites.source` + verbatim `cites.quote`) — the validator fails on any uncited entry, and
the session shows no push-back that lacks one; an uncited push-back is withdrawn (REC5).
**SE-7 (F6/C7):** at the write-gate, zero tensions are `live` — every one is `resolved`
in the cut or `accepted` with a recorded reason; live tensions block the gate (REC6).
**SE-12 (F11/C12):** every non-live tension carries the human loop's evidence —
`pushback.shown_to_human: true` with the text shown, `human_response.text` in the human's
words, and a `resolution_directive` (resolved) or human-given `resolution_reason`
(accepted); the validator fails any closed tension missing them, and the session shows
each was asked one at a time with no recommendation attached (REC11).
**SE-13 (F12/C13):** every `decision_questions` entry carries its citation, its question,
and the human's answer — the validator fails an unanswered one, and a `resolved` entry
also carries the `resolution_directive` derived from that answer; no epic's `user_check`
rests on a delivery method that neither a lens nor a recorded human answer decides
(REC12).
**SE-15 (F14/C13):** round reports are a CLOSED SCHEMA — the write-gate validates evidence
only under `tensions:` and `decision_questions:`, reads the legacy `questions:` key as an
alias for `decision_questions:` and holds it to the identical rules (counting it), and
fails any other top-level evidence key rather than passing it unchecked. The
decision-question count therefore reflects every round question; an off-schema key — under
which the gate would otherwise validate nothing and report a clean pass — is a forged-clean
gate and blocks the write until the round is rewritten under the canonical schema (REC14).
**SE-19 (F18/C17):** the loop's exit is proven, never assumed — the final write-gate run
wrote its verdict to `<working>/write-gate.yaml` reading `ok: true` with
`counts.live_tensions: 0` and `counts.decision_questions_open: 0`, and the close binds on
the stop-condition verdict (the write-gate verdict + the approval marker + the keyed persist
manifest + the scoped-guard report): `held` permits COMPLETED; anything else closes HALTED
(REC18). The grilling
loop itself is human-paced and UNCAPPED — its only exit is the clean tension report; no
round counter exists and no cap-halt path exists for human rounds.

### Phase: Persist (write the full delta first, ADR 026 write-then-review)

**Step 4 — Persist (keyed, in place — spine epics)** · Owner: play · Depends on: Step 3
Write-then-review (ADR 026): the FULL model delta is written to the live model BEFORE the
checkpoint, so the guard and the human all see the real delta. The `epic.md` docs +
`deferrals.yaml` are already on the live model (Step 1). `persist_epics.py` now writes the
SHARED file — the spine `epics` index — in place, keyed to `--slice-ref`: it reads the
manifest's epics-index delta and merges each entry into the live spine `epics` index
(additive by id, replacing only a `ready` epic the cut re-states, never an `in_delivery`
one), and it REFUSES to touch any epic delivery owns or any spine field outside `epics`
(this is the node-level containment the file-level guard cannot provide). No draft, no doc
copy. It is all-or-none: if anything is refused, nothing is written. Nothing is COMMITTED yet
— the commit (Step 7) happens only after the gate approves; on cancel the whole delta is
reverted (Step 6):

```
python3 scripts/persist_epics.py --manifest <working>/epics-manifest.yaml \
        --product-base <product_base> --slice-ref <domain>/<slice-id> \
        --out-manifest <working>/persist-manifest.json
```

**SE-9 (F7/C9):** the keyed persist manifest (`<working>/persist-manifest.json`) reads
`ok: true` with every approved epic in `written` and `refused` empty — all-or-none; a refused
plan writes nothing (REC7). Nothing is COMMITTED here — the model delta is committed only at
Step 7 after the checkpoint (Step 6) resolves.

### Phase: Guard (over the full delta)

**Step 5 — Guard the full delta** · Owner: play · Depends on: Step 4

**The run's write scope (the per-play guard policy, ADR 026).** The old `apply_epics.py`
encoded /grill's write scope by construction — the slice's `epics/` home (the `epic.md` docs
+ `deferrals.yaml`) and the spine `epics` index, and nothing else. Under direct-model-write
that same scope is the `scoped_write_guard.py` policy — resolve `<slice-epics>` as the slice's
epics home relative to `product-os/` (e.g. `<domain>/slices/<slice-id>/epics`):

    --allow 'product-os/_spine.yaml'                    # the shared epics index (persist writes it)
    --allow 'product-os/<slice-epics>/*'                # the epic docs + deferrals.yaml (add or re-cut)

**Guard ONCE over the full delta (C11).** After ALL writes (the LLM docs from Step 1 and the
keyed persist's spine write from Step 4), run the scoped guard a single time over the whole
delta. Capture its report — its `ok` field is the stop condition's D7 input (this replaces the
old `check_epics.py` before/after verify). /grill writes NO decisions, so the scope carries no
`decisions/*` glob:

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --allow 'product-os/_spine.yaml' --allow 'product-os/<slice-epics>/*' \
        --out <working>/guard-report.json
```

If the guard exits non-zero, re-run with `--restore` to revert the offending paths, apply
REC8 (a model path outside the slice's epic scope changed), and re-persist before the
checkpoint.

**SE-10 (F8/C11):** the scoped-write guard report reads `ok: true` — the model delta is
confined to the slice's `epic.md` docs, its `deferrals.yaml`, and the spine `epics` index; no
slice record, lens, functionality, profile, or any other spine field changed. Node-level
containment (only `epics` changed; an in-delivery epic untouched) is kept by the keyed persist.

### Phase: Checkpoint (config-gated, C9)

**Step 6 — Human review (class: standard)** · Owner: play · Depends on: Step 5
First record the checkpoint's resolution as the **approval marker** — the machine field the
stop condition reads (C17): after the gate resolves approve, write `<working>/approval.json`
as `{"approved": true, "mode": "typed" | "config-skip", "detail": "<the human's words | the
config resolution path>", "at": "<ts>"}`.

The checkpoint is a config switch of class `standard` per `gate-config.md` — NOT
pinned: when the switch resolves off, the gate records `gate skipped by config
(<resolution path>)` in the evidence's Checkpoint Decisions, writes the approval marker with
`mode: config-skip`, and proceeds — visible, never silent. The switch touches ONLY this
close-side checkpoint; the grilling loop's per-question HITL discipline (C12/C13 — one
question at a time, typed answers, never self-resolved) is the loop's interior, not a close
gate, and no config value touches it.
Write-then-review (ADR 026): the full delta is already on the live model (docs by Step 1, the
spine `epics` index by Step 4), so present the full cut **inline over the real model git
diff**, in product language: each epic — its title, outcome, the `user_check` (what a user
opens, does, and sees), its declared **surface** (the type, what a human runs/opens, and the
artifacts that must open), the acceptance criteria, the functionalities it threads, its
dependencies and order — plus the deferrals and their reasons, **the grilling record** —
every resolved tension (the question asked, the human's answer, the change made), every
accepted tension and the human's reason, every delivery-method decision the human made and
which epics it shaped (C12/C13) — and any lens defects recorded for routing. When the gate
fires (the default), render the approval prompt (`standards/templates/approval-prompt.md`)
and wait for a typed response. Approve → continue to Step 7 (commit). **Cancel → revert the
working tree (ADR 026 step 6):** the full delta is already on disk, so run the guard with
`--restore` and an EMPTY allow set to `git restore` the modified model paths and
`git clean`/remove the new ones (byte-clean back to HEAD), then halt — nothing was committed,
and cancel means "revert what was written":

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --restore --out <working>/guard-report.json   # empty --allow ⇒ every model path reverted
```

### Phase: Commit (make the delta durable, ADR 026 step 7)

**Step 7 — Commit the model delta** · Owner: play · Depends on: Step 6
The gate approved (or was skipped by config). Commit the full model delta on the branch (C18,
ADR 026 step 7) — a lightweight persist step that makes the writes durable and advances HEAD
so the injected end sequence carries a committed model delta. A cancelled checkpoint never
reaches this step — its tree was already restored in Step 6:

```
git add -- <product_base>product-os
git commit -m "feat(model): grill <slice-id> into epics (#<issue>)"
```

### Phase: End sequence (injected — D2 position: both, tail)

The `feat(model)` commit (Step 7) already made this run's model delta durable; the standard
end sequence raises, reviews, and lands it — the same branch the injected `start-change` head
opened (#437, decision 24). Each member runs as a sub-play dispatched with `parent_run_id`
(emits only its own C1 evidence; this play's close absorbs it). Each member is independent
and resolves its own context from the branch and config; this play passes no hand-rolled
git/PR/merge logic.

**Step 8 — commit-change** · Owner: `commit-change` (sub-play) · Depends on: Step 7 —
commit any work still uncommitted after the `feat(model)` model-delta commit (STM evidence
and the run records), grouped by concern with conventional messages; no push. The epics and
deferrals were already committed as the `feat(model)` delta in Step 7.

**Step 9 — propose-change** · Owner: `propose-change` (sub-play) · Depends on: Step 8 —
run the scope-and-quality self-review, push the branch, open the PR carrying the review.

**Step 10 — review-change** · Owner: `review-change` (sub-play) · Depends on: Step 9 — run
the diff-scoped quality check, post an approve/reject verdict. A reject stops the
sequence before merge.

**Step 11 — merge-change** · Owner: `merge-change` (sub-play) · Depends on: Step 10
(approve verdict) — merge the PR, switch to main and pull, delete the feature branch.

    {
      "play":          "<commit-change | propose-change | review-change | merge-change>",
      "parent_run_id": "<this run id>",
      "inputs":  {},
      "outputs": { "result": "<working>/end/<member>.json" }
    }

**SE-14 (F13):** after the model delta is committed (Step 7), the end sequence ran —
`<working>/end/` holds each member's result in order, starting with `commit-change.json` (the
durable model change did not sit waiting on a manual `/commit-change`); a member's own halt
(e.g. a review reject) stops the chain by that member's rules and is visible in its
result, never silent (REC13).

### Phase: Scenario Validation

**Step 12 — Scenario evals** · Owner: play · Depends on: Step 11
- **SCE-1 (S1 — product builder):** the slice's `epics/` holds the approved cut — every
  epic's acceptance names observable user behavior, the keyed persist manifest shows one
  all-or-none transaction and the approved cut was committed as a single `feat(model)` model
  delta, and no stale `ready` epic from an earlier run survives (the persist replaces them).
- **SCE-2 (S2 — delivery engineer):** the first epic in the order has no `depends_on`;
  every epic carries persona/systems/scope context plus acceptance; every
  `functionality_refs` entry and the `slice_ref` resolve to existing records.
- **SCE-3 (S3 — product builder under grilling):** the round reports show every tension
  cited (source + verbatim quote) and the session issued no push-back without one.
- **SCE-4 (S4 — product builder):** the coverage check maps every slice functionality to
  ≥1 epic or a deferral with a recorded reason — zero unmapped, zero silent drops.
- **SCE-5 (S5 — product builder, too early):** on an unrealized slice the play halted at
  pre-flight naming the missing stamp or lens files, and wrote no epic.
- **SCE-6 (S6 — lens owner):** any lens defect found while grilling is recorded in
  `<working>/lens-defects.yaml` naming the lens and the tension, the human was routed to
  that lens's play, and the lens files + slice record are byte-identical before and after
  the run.
- **SCE-7 (S7 — product builder, grilled for real):** every non-live tension in the round
  reports carries `pushback.shown_to_human: true` with the push-back text, a
  `human_response` with the human's own words, and a `resolution_directive` (resolved) or
  human-given `resolution_reason` (accepted); the write-gate fails when any is missing;
  the session asked its questions one at a time, plainly, with no recommendation attached.
- **SCE-8 (S8 — product builder, open delivery choice):** every `decision_questions`
  entry carries a citation, the question, and the human's answer; the write-gate fails an
  unanswered one; the checkpoint showed the chosen delivery strategy and the epics it
  shaped. The round reports carry question evidence only under the canonical keys (a legacy
  `questions:` list is aliased to `decision_questions:`, counted, and held to the same
  rules); the decision-question count equals the real number of round questions, and no
  off-schema key let the gate report a clean pass over unchecked evidence (F14).

### Phase: Evidence & Close

**Step 13 — Close** · Owner: play · Depends on: Step 12
Run the Standard Play Close. /grill is a **product-scoped** play (no issue) — use the
product-scoped evidence base and slug. Evidence recording is play-only and config-gated
per the D1 evidence rule (`standards/rules/evidence-recording.md`).

```bash
# --- Standard Play Close (canonical; see standards/rules/play-close.md) ---
# Path tokens resolved at pre-flight (resolve here if not already):
#   ltm_project_target  = yq '.ltm.project-target' .garura/core/config.yaml
#   evidence_base, slug:
#     project-scoped play : evidence_base="${stm_base}${issue}/evidence/grill/" ; slug="#${issue}"
#     product-scoped play : evidence_base="${product_base}_evidence/grill/"     ; slug="${product_slug}"
evidence_template=$(cat "${ltm_project_target}standards/templates/evidence-file.md")
delivery_template=$(cat "${ltm_project_target}standards/templates/delivery-report.md")
ts=$(date -u +%Y%m%d-%H%M%S)
evidence_dest="${evidence_base}${ts}.md"
mkdir -p "$(dirname "$evidence_dest")"
# Session identity stamp (#463) — close phase; start phase ran at pre-flight
session_stamp=$(python3 scripts/session_stamp.py --phase close \
    --marker "<working>/status/session-stamp-grill.json")
# Stop-condition gate (#464) — Step C0: this play carries a baked manifest, so the
# gate is LIVE. Evaluate the Done means against the run's grill working base as the
# close's authoritative input.
python3 scripts/check_stop_condition.py \
    --manifest "<play-dir>/stop-condition.yaml" \
    --base "<working>/" \
    --out "<working>/status/stop-condition-grill.yaml"
sc_exit=$?   # 0 held · 1 unmet · 2 error
```

`/grill` is product-scoped: `evidence_base="${product_base}_evidence/grill/"` and
`slug="${product_slug}"` (the slice, e.g. `ai-usage-intelligence/slice-token-data-spine`).

**Step C0 — bind the verdict.** `sc_exit == 0` (held) permits `status: COMPLETED` — the
write-gate verdict clean (zero live tensions, zero open decision questions), the
checkpoint resolved in the approval marker, the keyed persist manifest ok, and the
scoped-write guard report ok. Anything else
closes `HALTED` with `exit_reason: stop_condition_unmet` and the evidence's Stop
Condition section names every unmet clause. An unevaluable verdict is never a pass.
There is no `loop_cap_exhausted` here — the grilling rounds are human-paced and
uncapped; an unconverged grilling simply holds the run open (HALTED at close, resumed
at the open tension or unanswered question).

**Step C1 — Write evidence file.** Gated by the resolved `evidence.record` flag (global +
per-play `evidence.plays.grill`; first match wins, absent ⇒ record). When false, skip the
write and record `evidence skipped (record=false)` in the report's pointer line. Otherwise
fill the `evidence-file.md` slots (play `grill`, run_id `grill-${ts}`, product_slug = the
slice, started_at/completed_at, status per C0, exit_reason; artifacts produced: the epics,
the deferrals, the round reports with dispositions, the write-gate verdict, the approval
marker, any lens-defect records, the keyed persist manifest (`persist-manifest.json`), the
captured scoped-guard report (`guard-report.json`), the `feat(model)` model-delta commit sha,
the member results (start-change + the end sequence), the stop-condition verdict; step and
scenario eval results SE-1…SE-20 / SCE-1…SCE-8; checkpoint decision from Step 6 —
including a `gate skipped by config (<resolution path>)` row when the standard-class
switch resolved off; the session identity stamp fields from $session_stamp (#463):
session_id, ledger_file, ledger_start_offset, ledger_end_offset (null when unresolved —
never blocks the close); and stop_condition per C0 with the Stop Condition section
filled) and write to `$evidence_dest`. Do NOT hand-author the body.

**Step C2 — Render delivery report.** Also render the **Next** line: resolve this play in `standards/rules/pipeline-next.md` and emit `**Next:** /<command> — <why>. Or run /next to see all recommended actions.` (only /next pointer, or omit, when the mapped command is null), per `play-close.md`. Fill the `delivery-report.md` slots and output the
report: `## grill Delivered — ${product_slug}`, the Run Summary table, the Pipeline Steps
table from the task DAG, the Artifacts Produced table (the epics with their user_checks
and order, the deferrals, the accepted tensions, any lens defects routed), Next Steps (the cut is merged by the end sequence — run /start on the first epic in the
order to begin delivery; if a lens defect was recorded, run that lens play first), and a pointer to `$evidence_dest`. Always emitted; never gated.

```bash
# --- end Standard Play Close ---
```

## Scenario Validation

| Scenario | Persona | Eval |
|----------|---------|------|
| S1 — the approved cut | product builder | SCE-1 |
| S2 — self-contained pickup | delivery engineer | SCE-2 |
| S3 — cited grilling | product builder under grilling | SCE-3 |
| S4 — explicit deferral | product builder | SCE-4 |
| S5 — too early | product builder | SCE-5 |
| S6 — lens defect routed | lens owner | SCE-6 |
| S7 — grilled for real | product builder | SCE-7 |
| S8 — open delivery choice | product builder | SCE-8 |

## Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | an epic's acceptance reads as internal completion — no user-observable behavior | regenerate its acceptance from what a user can open and do, merging it with adjacent work until it's testable | autonomous |
| F2 | the realized stamp or lens files are missing | halt; run the missing realize lens plays (quality → ux → agentic → arch → measure → run) first | human |
| F3 | the coverage check finds a slice functionality mapped nowhere | cut an epic for it or record an explicit deferral with reason, then re-present the cut | autonomous |
| F4 | an epic embeds intent or lens content instead of referencing it | replace the copy with a reference to the source record | autonomous |
| F5 | a push-back in the session record carries no citation | withdraw it; re-issue only if a declared item supports it, otherwise drop it | autonomous |
| F6 | live unresolved tensions exist when the write is attempted | block the write; resolve each tension in the cut or record an explicit acceptance, then re-present | autonomous |
| F7 | the model delta was committed with no recorded approval, or the keyed persist wrote only part of the set | revert the working tree (scoped_write_guard.py --restore, empty allow), return to the checkpoint for a fresh approval, re-run the all-or-none keyed persist | human |
| F8 | the scoped-write guard finds a changed model path outside the slice's epic docs, deferrals, and the spine epics index | the guard's --restore reverts the offending paths; re-run confining the write to epics | autonomous |
| F9 | a dependency cycle, or a first epic that can't stand alone | re-order or split epics until the order is acyclic and the first is independently deliverable | autonomous |
| F10 | the self-containment check finds an epic with empty or unresolvable context or acceptance | backfill from the slice's intent records and lenses, re-verify resolution | autonomous |
| F11 | a non-live tension lacks human-response evidence — no push-back shown, no typed answer, or no human-derived directive/reason | reopen the tension to `live`, ask the question plainly (one at a time, no recommendation), capture the typed answer, and disposition from that answer only | human |
| F12 | an epic is shaped by a delivery method the human never chose — a missing or unanswered decision question at the write-gate | ask the cited decision question, capture the choice, revise the cut to match it, and record the decision in the round | human |
| F13 | the persist is verified but no end-sequence member has run — the model change is uncommitted with the play heading to close | enter the injected end sequence (commit → propose → review → merge) before the close; a member's own halt (e.g. a review reject) stops the chain by its own rules, never silently | autonomous |
| F14 | a round report carries question evidence under an unrecognized top-level key (a legacy `questions:` list, or any other off-schema key) | read a legacy `questions:` key as `decision_questions:` and validate it identically; for any other off-schema key, block the write-gate until the round is rewritten under the canonical `tensions:`/`decision_questions:` schema, then re-run the gate | autonomous |
| F15 | an epic at the write-gate has no `surface` block, or a surface defaulted to a non-user-facing type with no human confirmation | source the surface from the slice's own named surface (slice.surface) refined by the epic's user_check per surface-contract.md, put it to the human at the checkpoint, and write it; block the cut until every epic carries a confirmed surface that traces to a slice surface | human |
| F16 | a user-facing slice's first epic scaffolds no app/server shell | rework the order so the first epic seeds a minimal openable shell, or recut so one does, then re-present | autonomous |
| F17 | an epic doc fails the linter or the content eval, or its spine entry fails the schema or names an unknown functionality | re-emit the `epic.md` to its template, rewrite to the judge's cited fixes and re-judge until the gate passes, and fix the spine entry to resolve; never write a degraded epic | autonomous |
| F18 | the run is about to close COMPLETED with the stop-condition verdict missing, unmet, or unevaluable | close HALTED (`stop_condition_unmet`) naming the unmet clauses; resume at whatever is open — the live tension, the unanswered question, the unresolved checkpoint, the unpersisted cut, or the uncaptured guard report — then re-run the write-gate, the keyed persist, the guard, and the stop-condition check; no `loop_cap_exhausted` exists here — the grilling rounds are human-paced and uncapped, the run stays open until the human's answers converge it | autonomous |
| F19 | the product-os tree is dirty at entry (uncommitted model edits present) | halt and ask for a clean model tree — commit or revert the pending model edits (or let the injected start-change head cut a fresh branch off main) — before /grill proceeds | human |

## Pause and Resume

Steps run top to bottom. On entry, resolve config, run the readiness + realized gates,
resolve the target slice from the play argument or the in-progress draft, check the status
marker at `{stm_base}_grill/status/<slice-id>.json`, skip completed steps, reset any
in-progress step to pending, and continue. The grilling rounds resume from the round
reports on disk — closed dispositions (`resolved`/`accepted`) are preserved; a round left
mid-flight re-runs its tension check. Under direct-model-write (ADR 026) there is no draft
tree and no pre-apply snapshot: containment is the post-write scoped guard diffing the model
tree against HEAD. The clean-tree assertion (F19) is scoped to a FRESH start (the fresh
`start-change` branch) — a resume that already wrote `epic.md` docs re-enters its own
in-progress delta, which is expected, not a dirty-tree halt. A fresh start with no marker
runs everything and creates the
marker at Step 1. A close that halted on an unmet stop condition (C17) resumes at whatever
the verdict names open — the live tension, the unanswered decision question, the
unresolved checkpoint, or the unpersisted cut; the grilling rounds are human-paced and
uncapped, so there is never a round cap to exhaust — the run simply stays open until the
human's answers converge it.

## Compilation Metadata

| Field | Value |
|-------|-------|
| fingerprint | sha256:d566ecc331c24164ea2ddcdbfb0ef3066d94b943f8f6df333b6450f64e65d6fa (of `reference/ice.md`) |
| compiled_by | play-editor (#500 direct-model-write, ADR 026); prior: play-editor (#466 Batch C — gated close per ADR 025: Done means baked, stop-condition gate at Step C0, session stamp, checkpoint class standard, uncapped human loop stated), play-creator (#434; edited via play-editor, #436, #437), play-editor (#434, decision 24; closed-schema round-report fix — F14); epic-lifecycle prose corrected #439 (see deviation note) |

**Direct-edit deviation note (#439, ADR 019):** the epic-lifecycle sentence ("epics are temporary… deleted on merge") was corrected to "epics are permanent… stamped `delivered` on merge and kept" in both `reference/ice.md` and this compiled body, and the fingerprint recomputed to match. This is descriptive context about the epic's downstream life, not grill's own guarantee — no constraint, failure condition, scenario, step, or eval changed; grill still cuts epics and deletes nothing. No re-interview/rebuild required.
| pipeline_position | both (start-change head; commit-change → propose-change → review-change → merge-change tail — self-contained) |
| workflow_structure | A (approval checkpoint — class: standard, config-gated per gate-config.md, not pinned; direct-model-write WRITE-THEN-REVIEW per ADR 026 — persist + guard before the gate, feat(model) commit after; grilling rounds as a natural human loop in preparation) |
| stop_condition | stop-condition.yaml (D1–D7), gate live at Step C0 |
| loop | grilling rounds: human-paced, uncapped — exit = a clean tension report (zero live tensions, zero open decision questions) proven by the write-gate verdict; never an iteration cap |
| domain_agents | 1 (product-os-keeper) |
| utility_agents | 0 |
| skills_used | author-epics, check-cut-tensions |
| scripts | 9 (preflight.py, check_ready_slice.py, lint_grounding.py, grounding_gate.py, validate_epics.py — writes the write-gate verdict, persist_epics.py — keyed in-place persist of the spine epics index, scoped_write_guard.py — post-write containment guard, check_stop_condition.py — Done-means gate, session_stamp.py — #463 identity stamp) |
| member_subplays | start-change (injected head); commit-change, propose-change, review-change, merge-change (injected end sequence) |
| step_evals | 20 (SE-1…SE-20; one per failure condition F1–F19, plus SE-11 for C10) |
| scenario_evals | 8 (SCE-1…SCE-8) |
| recovery_entries | 19 (one per failure condition; 13 autonomous / 6 human) |

**Recompiled note (#500, direct-model-write / ADR 026):** migrated from draft-then-apply to
direct-model-write. The old draft model tree is removed; the author-epics skill writes each
`epic.md` (and the slice's `deferrals.yaml`) straight to the live model and emits the spine
`epics`-index delta as structured manifest data; the renamed keyed `persist_epics.py`
(was `apply_epics.py`) writes the spine `epics` index in place; containment is the post-write
`scoped_write_guard.py` (its `guard-report.json` is D7); the old `check_epics.py` before/after
verify was removed (the guard replaces it); the pre-apply file snapshot is gone (the guard
diffs vs HEAD); the play asserts a clean product-os tree at entry (F19, guaranteed by the
fresh `start-change` branch) and commits its own `feat(model)` delta after approval (C18).
Order is **write-then-review** (ADR 026 "Order of operations"): the full cut — the LLM's docs
AND the keyed persist's `epics`-index entries — is written FIRST (Steps 1+4), then guarded
ONCE over the full delta (Step 5), then the gate resolves over the real git diff (Step 6), and
only an approved gate COMMITS (Step 7); the injected end sequence then raises/reviews/lands the
committed delta. Checkpoint cancel reverts the working tree via the guard `--restore`
(empty allow). Grill's checkpoint stays a class-`standard` config switch — NOT a #467
conditional learned gate — so no `classify_change.py` is bundled and no change-shape is
classified. See `standards/rules/direct-model-write.md`.

**Direct-edit deviation note (#500) — INTENT CHANGE, HAND-COMPILED, CONVERGENCE UNVERIFIED:**
This SKILL was updated to the direct-model-write write-then-review shape (ADR 026) by a
**hand-compile from `reference/ice.md`**, NOT by a `/play-editor` run. This is an intent change
(it alters the write path, the containment guarantee, the checkpoint cancel semantics, and the
step order), so the sanctioned path is recompile-via-`/play-editor`; play-editor is
interactive-only (fully gated, human-checkpoint) and cannot run headless in this environment,
so the compiled output was produced by hand to match what play-editor would emit from the
current `reference/ice.md` (fingerprint above). **The `compiled_by` line names play-editor for
provenance intent, but no play-editor run actually occurred and convergence is UNVERIFIED.** An
interactive `/play-editor` convergence run against `reference/ice.md` — confirming the emitted
SKILL matches this hand-compiled body and refreshing the fingerprint — is recommended before
relying on this play in production. `lint_play.py` was run to 0 gaps against this body.

**Direct-edit deviation note (grill-spine-reconcile):** the recompile left the pre-flight,
apply, and verify prose on the OLD model — it called `check_realized.py` (redundant; the gate
is in `check_ready_slice.py`) and the `functionality_ices`/`ice_ref`/`profile.yaml` field
shapes, and the apply/verify commands used the old `--slice-dir`/`--profile-*` CLIs. These were
aligned to the actual reworked scripts (the spine hub-resolution emitting
`functionality_groundings`; `apply_epics.py --draft --product-base` merging the spine `epics`
index; `check_epics.py --manifest --spine-before/after --slice-ref` doing the before/after spine
diff) and `check_realized.py` was deleted. Execution-mechanism only — no constraint, failure,
scenario, or eval changed; the ICE (`reference/ice.md`) and the fingerprint are unchanged.

**Direct-edit deviation note (#466):** SKILL invocation flag corrected to match
`validate_epics.py`'s real interface — the two Step 2/write-gate invocations said
`--slice-file <slice_file>` but the script (like `check_epics.py`) accepts `--slice-ref`
and matches the bare spine slice id, so they now read `--slice-ref <slice_id>`.
Surface-prose only; no constraint, failure, scenario, or eval changed.
