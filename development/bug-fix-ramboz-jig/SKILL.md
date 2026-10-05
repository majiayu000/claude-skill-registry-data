---
name: bug-fix
description: >
  Drive the teeth-gated lifecycle for reported defects: diagnose root cause,
  prove it, and prevent regression through REPORTED → DIAGNOSING → ROOT_CAUSED
  → FIXING → REVIEWED → DONE, with VERIFIED, ESCALATED, and RESOLVED_ON_MAIN
  paths where needed. Auto-fires on fix this bug, debug this, root-cause this,
  this regressed, this broke again, why is this failing, diagnose before
  fixing, or investigate this failure. Two modes: `diagnose` stops at
  ROOT_CAUSED; `diagnose_and_fix` runs through DONE. Uses a durable bug record,
  multiple hypotheses, a fresh-main recheck, and a witnessed red→green test.
  Do not use for spec-shaped work (use `spec-workflow`) — including a pure
  visual design-fidelity gap against an agreed mockup, which is spec-shaped, not
  a bug (see "Design-fidelity triage" below) — or trivial one-liners (use
  `tdd-loop`).
user-invocable: true
---

> **Working posture ([ADR-0056](../../docs/decisions/adr-0056-adversarial-register-quarantine.md)).**
> Adversarial review is a *named, bounded operation.* This workflow invokes
> review passes (bug-review / craft), whose skeptical register belongs *inside*
> those isolated reviewer subagents. Outside a review, default to collaborative
> and solution-forward; don't carry the adversarial stance into ordinary
> conversation.

> Spec 058 / [ADR-0016](../../docs/decisions/adr-0016-bug-fix-lifecycle.md)
> built this workflow. The deterministic state mutations and teeth gates live
> in `bug.py`; this SKILL.md drives the judgment layer. It is a **peer of
> `spec-workflow`** — a first-class jig workflow that owns its orchestration,
> not a deferring baseline.

## What this skill does

- Routes a reported bug to the **proportional** path: `triage` bows out of
  trivial work, reserving the record + gates for standard/gnarly tiers.
- Drives the bug lifecycle state transitions via `bug.py transition`, which
  enforces the teeth gates (diagnose-before-fix; red→green).
- Coordinates reviewer-subagent passes (bug-review, craft, conditional
  security) at `→ REVIEWED`, validated by the ADR-0014 evidence gate.
- Rechecks fresh main after `ROOT_CAUSED` and before `FIXING` so a stale
  parallel session does not re-fix a bug already solved on trunk.
- Provides the first-class escalation seam (`bug.py escalate`) for when a bug
  turns out to be a missing or under-specified behaviour.
- Imports the diagnose-first discipline (the diagnostic question,
  anti-anchoring, evidence-accruing re-entry) borrowed from
  diagnose-first debugging — see [ADR-0016 §9](../../docs/decisions/adr-0016-bug-fix-lifecycle.md).

## The diagnostic question (read first, every time)

> **Is this a problem with the output, or the process that created the
> output? Fixing the output is a treadmill.**

This is the heart of DIAGNOSING. A fix that patches the symptom — the bad
value, the wrong pixel, the failing assertion — without finding the process
that produced it does not close the bug; it relocates it. The bug-review pass
exists to catch exactly this (`fix_class: workaround` honestly labelled is
fine; a workaround disguised as a `structural_fix` is a blocker).

## Modes

- **`diagnose`** — stop at `ROOT_CAUSED`. Use when you (or the user) want the
  root cause established and reviewed before committing to a fix, or when the
  fix belongs to someone else. This is the default for "diagnose before
  fixing" / "root-cause this".
- **`diagnose_and_fix`** — run through `FIXING → REVIEWED → … → DONE`. Use
  when the fix is yours to land now.

The mode is a posture, not a flag — both run the same `bug.py transition`
gates; `diagnose` simply stops the forward walk at `ROOT_CAUSED`.

## Tiers — proportionality enforced *downward*

`bug.py triage` is the de-escalation gate. The antidote to ceremony is a
workflow that **refuses** to build ceremony for a one-liner.

| Tier | Behaviour |
|---|---|
| **trivial** (typo, one-liner, mechanical) | `triage --tier trivial` **deletes the record** and tells you to write the failing test with `tdd-loop`, fix, and commit. The workflow bows out. |
| **standard** | Single-file record + diagnose gate + red→green teeth + bug-review + craft. ≥2 hypotheses advisory. |
| **gnarly** (cross-layer, security, regression that didn't stick, design **malfunction** — *not* a pure visual fidelity gap, which is spec-shaped; see "Design-fidelity triage") | Full rigor: ≥2 hypotheses **mandatory**, keeps the `VERIFIED` step, conditional security pass, `new --push` reserves the number on `origin/main`. May escalate to a spec. |

When in doubt about whether a bug is trivial, ask: would a regression test for
it be worth keeping? If yes, it is at least standard.

### Design-fidelity triage — malfunction vs. fidelity gap ([ADR-0049](../../docs/decisions/adr-0049-design-fidelity-routing-to-originating-spec.md))

A design complaint is `bug-fix` **only when the UI malfunctions**: a control
that looks active but isn't, or a layout that overlaps so content is
unreadable. A pure visual gap against an agreed mockup — the screen works, it
just hasn't reached the agreed look — is **fidelity work on the spec spine**,
not `bug-fix`. Route it:

- **An originating spec exists** (the gap surfaced under a spec whose slice
  built the screen) → continue that slice if still open, or open a follow-up
  slice **under the same spec**, carrying the mockup forward as design-value ACs.
- **No originating spec exists** (a mockup-first / cross-platform rebuild that
  never entered spec-workflow) → open a **new spec** via `spec-workflow`'s
  greenfield path, with the mockup as design-value ACs. A mockup-first rebuild is
  never dead-ended into `bug-fix` for lack of an owning spec.

**Ambiguous-case tie-breaker:** an issue that "looks broken, but maybe just
mis-styled" (a control that mis-signals its state, or overlap that only *might*
block interaction) is decided by a quick behavioral check — does it actually
*do* the wrong thing? An ambiguous-but-functional gap (it behaves correctly,
only looks off) defaults to the **spine**, not `bug-fix`; reserve `bug-fix` for
a confirmed behavioral malfunction.

**Fidelity vs. refinement — does the visual target change?** If the mockup is
still the agreed target and the build simply hasn't reached it yet, that is
**fidelity**: carry the *existing* mockup forward as the AC, don't re-decide the
target. If we now want a *different* look than the mockup, that is a genuine
**refinement** (a new target), authored as such — not smuggled in as mere
unfinished work.

## Lifecycle

```
REPORTED → DIAGNOSING → ROOT_CAUSED → FIXING → REVIEWED → (VERIFIED) → DONE
                  │              └─ main already clean → RESOLVED_ON_MAIN
                  └──────────────── escalate → ESCALATED (→ spec NNN)
```

`(VERIFIED)` is gnarly/security-tier only — trivial/standard collapse
`REVIEWED → DONE`. Back-edges relax status and are ungated: `REVIEWED →
FIXING` (review needs changes), and a failed green-check or a
"symptom-not-cause" verdict routes back to `DIAGNOSING`, carrying the failed
attempt forward as new evidence (append it to `## Already tried` — it flows
into `learnings.md` at close).

`RESOLVED_ON_MAIN` is terminal: after the root cause is understood, the
session checks fresh `origin/main` before starting the fix. If the original
reported repro no longer fails there, another session already solved it; the
bug record is closed as resolved on main instead of generating a duplicate
patch.

### The teeth gates

`bug.py transition` enforces presence/shape, never quality (quality is the
reviewer's job). Each gate is bypassable as a deliberate act
(ADR-0011 lineage) — separate env vars so one gate can be relaxed without
silently relaxing the others.

| Transition | Gate | Bypass |
|---|---|---|
| `→ ROOT_CAUSED` | ≥2 candidate hypotheses + a leading one + an evidence pointer | `JIG_BUG_DIAGNOSE_GATE=0` |
| `ROOT_CAUSED → FIXING` | fresh-main recheck recorded as `main_repro_result: reproduces`; `fix_class` declared; `regression_test` runs **red** (shells to `tdd.py`, expects exit 1; stamps `red_confirmed_at`); **repository-closure inventory** present for new standard/gnarly records | `JIG_BUG_MAIN_CHECK_GATE=0` (main recheck), `JIG_BUG_TEST_GATE=0` (test), `JIG_BUG_CLOSURE_GATE=0` (closure) |
| `→ REVIEWED` | the same `regression_test` now runs **green** (shells to `tdd.py`, expects exit 0; stamps `green_confirmed_at`); **call-site closure** recorded for new records; **and** the required review verdicts pass | `JIG_BUG_TEST_GATE=0` (test), `JIG_BUG_CLOSURE_GATE=0` (closure), `JIG_REVIEW_EVIDENCE_GATE=0` (verdicts) |
| `→ VERIFIED` | original reported repro re-run clean (gnarly/security only), attested in the record | — |
| `→ DONE` | required review verdicts pass + a learning recorded in `docs/memory/learnings.md` | `JIG_REVIEW_EVIDENCE_GATE=0` |

**The distinctive gates** are the diagnose gate (the ≥2-hypotheses
anti-anchoring rule), the fresh-main recheck after root cause, the
**red→green teeth**, and the **repository-closure gates** (ADR-0037). The
red→green teeth: the helper itself witnesses the test fail before the fix and
pass after, so "there is a regression test" is machine-attested, not claimed. A
bug already clean on fresh main becomes `RESOLVED_ON_MAIN`; a test already green
without the fix does not capture the bug — the `→ FIXING` gate refuses it. A
`tdd.py` env error (exit 2) **fails closed** (gate not satisfied), distinct from
red. The repository-closure gates make reuse/history discovery and call-site
closure durable evidence (see the **Repository-closure inventory** subsection
under step 2 below).

`fix_class` (declared at `→ FIXING`) is one of `workaround` / `local_patch` /
`structural_fix` / `guardrail` / `observability`.

## How to use

### 0. Confirm the project is scaffolded

Like `spec-workflow`, the bug record lives under `docs/bugs/`. If the project
is greenfield, route to `/jig:scaffold-init` first; if it has a spec layout
but no `scaffold.json`, route to `/jig:migrate`. Don't hand-roll `docs/bugs/`.

### 1. Create and triage the record

Before creating a new bug from a feedback/triage batch, scan
`docs/specs/README.md` for an overlapping active slice. If the work is already
owned by a spec, link that slice from the bug record or escalate/route instead
of creating a second owner.

```bash
# Reserve the number. Local by default; --push reserves on origin/main
# (gnarly tier), --pr via PR. Works from any branch/worktree (ADR-0015).
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" new <slug> [--push|--pr]

# Classify. trivial → record deleted, bows out to tdd-loop + commit.
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" triage <id> \
  --tier trivial|standard|gnarly [--severity <level>]
```

If `triage` bows out, **stop here** — write the failing test with
`/jig:tdd-loop`, fix, commit. Do not re-create the record.

Claim/release reuses the spec 049 machinery: `bug.py pickup <id>` claims;
`bug.py pickup <id> --release --reason "<why>"` force-releases a stale claim
(logged to the record's `## Release log`). `pickup` also stamps the working-tree
`.jig/spec-ref` marker naming this bug (slice 098-04) — the signal that tells
jig's lifecycle entry gate a bug fix is in flight, so ad-hoc-edit nudges stay
silent while you work. Release and terminal transitions clear it.

### 2. Diagnose (`→ DIAGNOSING → ROOT_CAUSED`)

Fill the record body — `## Symptom`, `## Repro`, `## Evidence`,
`## Hypotheses`, `## Root cause`. **Anti-anchoring: write ≥2 candidate
hypotheses** with confirm/falsify framing and mark the leading one (mandatory
for gnarly, advisory for standard, but always good practice — the first
explanation is rarely the right one). Write the hypotheses as a Markdown list
under `## Hypotheses` — any marker works (`-`, `*`, `+`, or `1.`) and the gate
counts **top-level** items only, so indented `- Confirm:` / `- Falsify:`
sub-bullets read as notes, not as extra hypotheses. Mark the leading one with
`[x]`, an inline `(leading)` tag, or a `Leading:` line.

**Ground a `## Root cause` claim; enumerate a universal one
([ADR-0052](../../docs/decisions/adr-0052-grounding-enumeration-for-universal-claims.md)).**
A root-cause claim of *universal or negative* shape — "**nothing else** calls
this", "**only** this path writes the column", "this is the **one** place the
value is set" — is established by an **enumeration** (a search you can show
returns the *complete* set: `grep` every caller / writer / call-site), **not**
by a single citation of one example. One true example says nothing about the
rest of the set, and a false "only/nothing" here sends the fix to the wrong
place. To claim it, **state why the search is exhaustive** — what closes the set
so nothing escapes. Many sets only *look* `grep`-bounded: a column written
through an ORM, a string-built query, reflection, config-wiring, codegen, or an
external consumer is invisible to `grep` (illustrative, not a checklist), so an
empty result is **absence of evidence, not proof nothing writes it**. When you
cannot show the search closes the set, weaken the claim or record it under
`## Already tried` / the record's assumptions rather than asserting it as the
root cause — the bug-review pass treats an empty search as *un*grounded until you
have shown what closes the set. Then:

```bash
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" transition <id> DIAGNOSING
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" transition <id> ROOT_CAUSED
```

In **`diagnose` mode, stop here** and present the root cause.

#### Repository-closure inventory (before `→ FIXING`) — [ADR-0037](../../docs/decisions/adr-0037-bug-fix-repository-closure-evidence.md)

Before you write the fix, fill the `## Repository closure inventory` section
(new standard/gnarly records gate `ROOT_CAUSED → FIXING` on it — a fresh
`bug.py new` record carries the section and the `closure_schema:` marker; a
legacy pre-091 record has neither and is exempt). This exists because a narrow
patch that duplicates an existing helper passes TDD while leaving a
convergent path unfixed — the closure question has to be asked *before* the
code shapes the change, not at review.

- **Equivalent / convergent logic searched** — look for an existing
  implementation of the same contract, possibly under a different name.
  **Tool-neutral:** prefer a configured semantic index when one is available;
  the portable floor every project has is targeted text search plus
  `git log -S` / `git grep`. Record the *terms you tried*, not just a verdict.
- **Relevant history inspected** — `git log`/`git blame` on the touched
  surface: when and why did this logic arrive, and did the same change land
  elsewhere?
- **Affected call sites** — enumerate the sites that share this contract.
- **Reuse decision** — reuse the existing implementation, or duplicate with an
  explicit reason.

This is an **effort-and-protocol standard, not a completeness standard**. You
cannot prove a differently-named helper does *not* exist, and the gate does not
ask you to. What it refuses is a **bare verdict** — "none found" with no
recorded search behind it. When the set genuinely cannot be closed by a name
search, apply the **same enumeration standard as the `## Root cause` grounding
above** ([ADR-0052](../../docs/decisions/adr-0052-grounding-enumeration-for-universal-claims.md)):
state what you searched and why it does not close the set, and record the
residual as an assumption *with that protocol*. Do not restate the enumeration
rule here — it has one home, in the diagnose grounding block above. `bug-review`
judges whether the search was real; the transition gate only checks the
prompts are answered and not vacuous.

### 3. Fix (`→ FIXING → REVIEWED`), `diagnose_and_fix` mode

1. Declare `fix_class:` and name the `regression_test:` in the record.
   Before `→ REVIEWED`, fill `## Call-site closure`: account for every site the
   inventory named as **changed, tested, or intentionally left alone** (with a
   reason). This is *accounting*, not a mandate to widen the fix — a site can be
   correctly left untouched. New records gate `→ REVIEWED` on it; legacy records
   are exempt.
2. Recheck fresh main before writing the fix. Fetch/inspect `origin/main`
   (usually from a detached worktree) and re-run the original reported repro.
   Then record the outcome:

   ```bash
   python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" main-check <id> \
     --result reproduces \
     --ref origin/main@<sha> \
     --evidence "<original repro command + observed failure>"
   ```

   If the bug no longer reproduces on fresh main, record the terminal off-ramp
   and stop:

   ```bash
   python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" main-check <id> \
     --result resolved-on-main \
     --ref origin/main@<sha> \
     --evidence "<original repro command + observed clean result>"
   ```

3. Write the regression test FIRST (it must fail without the fix — that is
   what the `→ FIXING` gate witnesses). Use `/jig:tdd-loop` for the red→green
   loop.
4. `transition <id> FIXING` — the gate requires the fresh-main recheck above,
   then shells to `tdd.py` and expects the test **red**; it stamps
   `red_confirmed_at`.
5. Implement the smallest change the diagnosis supports. Make the test green.
6. Run the review passes (below), record their verdicts, then
   `transition <id> REVIEWED` — the gate shells to `tdd.py` and expects the
   test **green** (stamps `green_confirmed_at`), then validates the verdicts.

### 4. Review passes (at `→ REVIEWED`)

Two required + one conditional, run as reviewer-subagent passes by the
host/orchestrator and validated by the ADR-0014 evidence gate. The reviewer
is read-only — `bug.py` validates the durable verdict artifacts they produce
(`docs/bugs/reviews/bug-NNN-<pass>.md`).

1. **bug-review** (always) — the compliance analogue, jig's own. Build the
   prompt with `review.py bug-review`:

   ```bash
   PROMPT=$(python3 "${PLUGIN_ROOT}/skills/independent-review/review.py" \
     bug-review "docs/bugs/NNN-<slug>.md" "<deliverable-path>" ...)
   ```

   It asks: does the fix address root cause or paper over the symptom? is
   there a regression test that fails without the fix? blast radius? scope
   creep? If `fix_class: workaround`, is it honestly labelled and justified?

2. **craft** (`pr-review`, always) — **defers** to a richer installed
   `pr-review` skill on disk; falls back to jig's baseline `pr-review` skill.
   Run that skill's methodology against the bug's deliverables — it is
   diff-shaped, not spec-shaped, so there is **no** `review.py pr-review` call
   for a bug (that builder requires a spec + slice). Record the verdict with
   `prompt_source: pr-review skill craft pass` (as bugs 001–003 did).
   **A configured `review.pr_review_skill` (scaffold.json) is NOT read here.**
   Spec 096-01 / ADR-0040 D1 wired config honoring into `review.py`'s craft-pass
   builder, but this pass makes no such call, so the config key does not reach
   it — deferral here stays disk/router-based. Making bug-fix's craft (and
   security) passes config-honoring is a tracked follow-up (ADR-0040 OQ1).

3. **security** (`security-review`, conditional on `security_surface: true` in
   the record — mirrors how `arch_review: true` gates the arch pass) —
   **defers** to a richer installed `security-review` skill (Adobe's
   `adobe-security-*`, the user's own, or jig's baseline).

There is **no arch pass** — bugs carry no design.

Record each verdict with `review.py record-review --bug NNN --pass <name>
--verdict pass --reviewer <src> --summary-file <path>` (or `--summary-file -`
to pipe the body in — the body is required, and stdin is never read
implicitly, bug 017). The `REVIEWED` gate requires `bug-review` +
`craft` (+ `security` when `security_surface: true`), each `verdict: pass`.

### 5. Verify (gnarly/security only) and close

```bash
# Gnarly/security: re-run the ORIGINAL reported repro (not just the proxy
# test), attest it in the record, then:
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" transition <id> VERIFIED

# Record the learning in docs/memory/learnings.md (the → DONE gate checks it),
# commit the work, then:
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" transition <id> DONE
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" status-board
```

Run `/jig:memory-sync` to consolidate any new learnings. Land the change with
`/jig:slice-land` if a formal landing checklist helps.

**Before landing, audit the board.** `docs/bugs/README.md` is derived — every
column is computed from the records — so it is regenerated, never hand-edited,
and a merge conflict on it is resolved by re-running `status-board` rather than
by picking a side:

```bash
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" check-board
```

Read-only; exits non-zero on either problem it can find. **Stale board** — the
records changed and `status-board` wasn't re-run. **Duplicate id** — two records
claim one number, which is what parallel branches produce when the number was
never reserved on the trunk. The renderer emits both rows without complaint and
a staleness check can't see it (both rows *are* faithfully derived), so this is
the only thing that catches it. Wire it into CI if the project lands work from
more than one branch at a time.

### Escalation (`→ ESCALATED`)

When diagnosis reveals the "bug" is a missing or under-specified
*behaviour* — not a defect in existing behaviour — escalate instead of
fixing:

```bash
python3 "${PLUGIN_ROOT}/skills/bug-fix/bug.py" escalate <id> [--slug <spec-slug>]
```

This calls `workflow.py new`, stamps `escalated_to: NNN` on the bug and
"originated from bug NNN" on the new spec, and parks the bug in terminal
**ESCALATED** (not DONE — it was not fixed as a bug). Continue in
`spec-workflow`.

## De-escalation guidance

The single most important judgment in this workflow is **down-shifting**:

- A typo, a copy-paste error, a one-line off-by-one, a mechanical rename — let
  `triage --tier trivial` delete the record. Write the test, fix, commit.
  Creating a numbered record for a one-liner is the ceremony this workflow
  exists to refuse.
- A standard bug does **not** need the `VERIFIED` step or a security pass —
  `REVIEWED → DONE` is the path.
- Reach for gnarly only for genuinely cross-layer, security-surfaced,
  regression-that-didn't-stick, or design-**malfunction** bugs (a control that
  looks active but isn't; overlap that makes content unreadable — *not* a pure
  visual fidelity gap, which is spec-shaped; see "Design-fidelity triage"). If a
  "gnarly" bug is really a missing behaviour, **escalate** — don't grind it
  through the bug gates.

## Routing — bug-shaped vs spec-shaped

This is the bookend to `spec-workflow`'s "do not use for bug-shaped work"
clause. See [docs/workflow.md](../../docs/workflow.md) for the canonical
routing rule. In short: a reported defect → `jig:bug-fix` (proportional to
tier); a hard-to-reverse decision, cross-layer change, or ambiguous-scope new
behaviour → `spec-workflow`; a trivial one-liner → straight to `tdd-loop` +
commit.

## Gotchas

- **The `→ FIXING` gate refuses an already-green test.** A regression test
  that passes without the fix does not capture the bug. Write the test to fail
  first.
- **The `→ FIXING` gate also refuses a stale trunk check.** After
  `ROOT_CAUSED`, record `bug.py main-check … --result reproduces` against
  fresh `origin/main`; if the repro is clean there, mark
  `RESOLVED_ON_MAIN` and stop.
- **`tdd.py` env error fails the gate closed** (exit 2 ≠ red). Fix the
  environment; don't bypass blindly.
- **Bypass env vars are deliberateness escapes, not the default.**
  `JIG_BUG_DIAGNOSE_GATE=0` / `JIG_BUG_MAIN_CHECK_GATE=0` /
  `JIG_BUG_TEST_GATE=0` / `JIG_REVIEW_EVIDENCE_GATE=0` are for out-of-band
  flows — using them silently defeats the teeth.
- **Escalate, don't grind.** A bug whose fix introduces new routing/landing
  semantics or a missing behaviour is a spec — use the escalation seam.
- **`ESCALATED` and `RESOLVED_ON_MAIN` are terminal — closed, not
  unfinished.** A bug in a terminal non-`DONE` state was reclassified to a
  spec (`ESCALATED`) or already fixed on trunk (`RESOLVED_ON_MAIN`); it was
  never fixed as a bug, so its blank fix/test columns are *expected*. Don't
  flag it as stale or try to advance it to `DONE`. The status board
  segregates these rows under a `## Terminal` section (parity with the spec
  board's `## Deferred slices` / `## Abandoned slices`) so closure is legible.
- **`bug.py` never spawns subagents.** The host/orchestrator runs the reviewer
  passes; `bug.py` only validates the recorded verdict artifacts (ADR-0016
  Scope).
