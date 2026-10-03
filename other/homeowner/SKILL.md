---
name: homeowner
description: Autonomous build orchestrator — takes a written brief to verified code without a human gate, sequencing scaffold, architect, foreman, builder, and inspector. Halts and surfaces when a spec has Open Questions, a builder gets stuck, or an inspection fails. The build-mode counterpart to walkthrough (maintain mode).
version: 1.0
---

## Contract terms — read first

Before anything else, read your slice of the Plumbline contract at **`${CLAUDE_PLUGIN_ROOT}/terms/homeowner.md`** — generated from the root `TERMS.md`, it holds every shared token, status line, and file-naming pattern this skill reads or writes. Reproduce them **verbatim**. **If you cannot load it, stop and report; do not guess the contract.**

---

## When to use this skill
When you want to take a written brief to verified code in one unattended pass — no interview, no
spec-approval gate. Homeowner is the build-mode loop that runs without a human in the seat: it
sequences the same single-responsibility skills, routes on their reported status, and **halts and
surfaces** rather than guessing whenever a stage reports a gap it can't safely cross.

**Not for supervised builds.** When a human is available to interview and approve the spec, run the
skills by hand — `architect` in interview mode, review the spec yourself, then `foreman` → `builder`
→ `inspector`. That keeps the human spec gate. Homeowner removes that gate and stands its own
Phase 3 spec review in its place.

---

## Rules
- **Sequence, don't reimplement.** Homeowner calls the single-responsibility skills; it never does
  their work. Every skill stays independently runnable.
- **Route on reported status, don't second-guess the artifact.** Read each stage's returned status
  and sequence on it. Do not re-read the spec, blueprint, or code to overrule a skill's own report —
  judgment stays in the skills, sequencing stays here.
- **Halt and surface, never improvise around a gap.** Open Questions, a builder Stuck, or a failed
  inspection stop the run. Report exactly where and why; wait for human input.
- **Inspector runs as a fresh, separate subagent.** Independence is structural where it matters
  most — the loop cannot grade its own final result. (Homeowner reviews the *spec* itself in Phase 3;
  that's the principal checking the plans against the brief it holds, not self-grading a build.)

---

## Execution Order

**Run start — open the log first.** Before any phase, open
`Plumbline/homeowner/HomeownerLog_YYYY-MM-DD_HH-MM.md` and record the brief verbatim (create
`Plumbline/homeowner/` if absent — on a greenfield run it won't exist until Phase 1 scaffolds it).
Every phase appends to this log; opening it first means even a Phase 1 or Phase 2 halt is captured.

### Phase 1 — Scaffold (greenfield only)

**Greenfield or existing?** Check the project root:
- **Existing** — `Planning/` and `CLAUDE.md` already present → **skip this phase.** Treat the brief as
  a new feature on an existing codebase and go to Phase 2.
- **Greenfield** — neither present → run scaffold.

**Spawn scaffold.** It lays the folder skeleton, inits git, and writes `CLAUDE.md` from the template —
**structure only.** You pass it nothing about the stack or commands: scaffold makes no such decisions
and leaves them as `[pending — architect]` for Phase 2 to fill. This is why Phase 1 needs no
command-passing and no scaffold blocking status — the one gap scaffold used to hit ("no real run
command") is now architect's to raise as an **Open Question** in Phase 2, caught by the Phase 3 gate.

**Route:**

| Scaffold result | Homeowner does |
|-----------------|----------------|
| Skeleton + git + contract created | Proceed to **Phase 2**. |
| Scaffold stops (it found substantial existing code) | **Halt.** Your greenfield check and scaffold disagree about the root — surface it rather than scaffolding over something. (Shouldn't occur: you already classified the root above.) |

Then append the Phase 1 block to the run log.

### Phase 2 — Spec

Spawn **architect** as a subagent in **autonomous mode**. It cannot ask questions; it expands the
brief and routes every gap to one of two lists — **Assumptions** (low-surprise defaults it built
against; non-blocking) or **Open Questions** (genuine forks it couldn't safely default; blocking).

**Pass it:**
- the written brief (the idea Homeowner was started with),
- the autonomous-mode signal — i.e. a brief is present and no interactive human is available.

**It produces:**
- `Planning/specs/[feature]_spec.md`
- `Plumbline/decisions/[feature]_YYYY-MM-DD.md`
- a **status** reported back to you.

**Route on the returned status — do not read the spec to second-guess it:**

| Status | Homeowner does |
|--------|----------------|
| `READY` | Proceed to **Phase 3 (spec self-review)**. |
| `READY · ASSUMPTIONS: N` | Proceed to **Phase 3** — the assumptions are **non-blocking**. Carry the N assumptions forward: Phase 3 sanity-checks them and the closing report surfaces them for the human. A low-surprise default is not a reason to stop an unattended run. |
| `+ SIZE_FLAGGED` | Append to either of the above; proceed. The size question is handled in Phase 3; the flag never blocks on its own. |
| `OPEN_QUESTIONS: N` | **Halt.** Surface the spec path and the N questions verbatim. A human resolves them before the build resumes. Do **not** answer them yourself, do **not** run the spec review, do **not** proceed. |

**Why `ASSUMPTIONS` proceeds but `OPEN_QUESTIONS` halts:** the two lists differ by the contract's
cost test (§6) — an Assumption is cheap to change if wrong; an Open Question forks the build.
Halting an unattended run over a cheap default defeats the point of homeowner; building through a
fork risks a rebuild. Phase 3 gives the assumptions a second look, so a misclassified fork still
gets caught before the build.

### Phase 3 — Spec self-review (the gate)

Homeowner holds the brief; architect produced the spec. Here Homeowner stands in for the human
spec-approval gate — the one judgment it makes *itself* rather than delegating to a subagent, because
"is this what I asked for?" is the principal's call. It must be logged (see below), or the gate is
invisible.

**Read both:**
- the original brief (what was asked),
- `Planning/specs/[feature]_spec.md` (what architect produced).

**Ask, in order:**

1. **Faithfulness — does the spec do what the brief asked?**
   - Everything the brief asked for appears in the spec — nothing dropped.
   - The spec adds nothing the brief didn't ask for and that isn't a necessary, conventional
     implication — no hallucinated scope.
   - Every default architect made is recorded — in `## Assumptions` or `## Open Questions` — not
     silently baked in. A gap filled in *neither* list is a silent guess, and that is drift.
2. **Assumptions — is a fork hiding among them?** This is the second check that makes the
   non-blocking Assumptions path safe (Phase 2 let `ASSUMPTIONS` proceed without a halt). Read each
   assumption with the cost test: *if this default is wrong, is it a cheap edit or a partial
   rebuild / an architecture fork?* A genuinely build-forking item mis-filed as an Assumption is
   exactly what this catches — treat it as drift: the verdict is `DRIFTED`, kicking the spec back so
   architect re-files it as an Open Question (which then halts). Cheap, low-surprise defaults pass.
3. **Tractability — is it too big to build in one autonomous pass?**
   - Weigh architect's `SIZE_FLAGGED` signal plus your own read against the size thresholds
     (6 features / ~500 lines / a ~150-line feature).
   - **You do not split it yourself.** Splitting a spec into per-feature specs + a reference tier is
     an architecture decision, and Homeowner never makes one unattended.

**Verdict — exactly one:**

| Verdict | Meaning | Homeowner does |
|---|---|---|
| `FAITHFUL` | Spec matches the brief and is tractable | Proceed to **Phase 4 (foreman)**. |
| `DRIFTED` | Spec drops, adds, or distorts what the brief asked | **Halt.** Log each drift specifically. A human reconciles (re-run architect, or amend the brief) before the build resumes. |
| `TOO_BIG` | Spec is faithful but past the size thresholds | **Halt with a split recommendation** — name what should be split out. A human decides on restructure; Homeowner never splits unattended. |

A spec can be both faithful and too-big; `TOO_BIG` wins (halt). **Only `FAITHFUL` proceeds.**

**Then log the verdict.** Append to the run log `Plumbline/homeowner/HomeownerLog_YYYY-MM-DD_HH-MM.md`. The
verdict and its reasoning are the auditable record of the gate Homeowner stood in for. The skeleton
below is the **whole run's** log format — every phase appends its block as it completes.

```
# Homeowner Run — [feature] · YYYY-MM-DD

## Brief
[The original brief, verbatim.]

## Phase 1 — Scaffold (greenfield only)
Greenfield: yes → scaffold ran | no → skipped (existing project)
[greenfield] Skeleton + git + CLAUDE.md created; Stack/Commands left pending for Phase 2.

## Phase 2 — Spec
Architect status: READY | READY · ASSUMPTIONS: N | OPEN_QUESTIONS: N  (+ SIZE_FLAGGED)
Spec: Planning/specs/[feature]_spec.md
[ASSUMPTIONS: list the N assumptions verbatim — carried to the closing report for the human.]

## Phase 3 — Spec self-review
Verdict: FAITHFUL | DRIFTED | TOO_BIG
- Faithfulness: [what was checked; any drift found]
- Assumptions: [N reviewed; none hides a fork | item X is actually a fork → DRIFTED]
- Tractability: [size read; split recommendation if TOO_BIG]
[On DRIFTED / TOO_BIG: exactly what a human must resolve before resuming.]

## Phase 4 — Blueprint
Foreman status: BLUEPRINT_READY | BLUEPRINT_BLOCKED: <reason>
Blueprint: Plumbline/blueprints/[feature]_BP.md  (or part files _p-1, _p-2, …)
- Slices: [count; which are [inspect]-flagged]
[On BLUEPRINT_BLOCKED: the reason verbatim, and whether it's a contract gap or a Phase-3 gate miss.]

## Phase 5 — Build til green
Inspection level: flagged
- Slice [N] [inspect]: PASS | FAIL → fixed (cycle k of K) → PASS | HALTED after K cycles
  [one line per inspected slice]
Builder final status: BUILD_COMPLETE | STUCK: <where/why> | HALTED: <slice, reason>
Deviations: Plumbline/deviations/Deviations_[feature]_[date]_[HH-MM].md ([N] / none)
[On STUCK / HALTED: exactly what a human must resolve before resuming.]

## Phase 6 — Independent sign-off
Inspector (fresh subagent) status: PASS · needs-human: [Z] | FAIL: [N] → fixed (cycle k of 3) → PASS | HALTED | BLOCKED: <reason>
Final report: Plumbline/inspect/Inspect_[feature]_Final_[date]_[HH-MM].md
- Automated: [X] passed / [Y] failed
- Human sign-off owed: [Z] items (listed in the report)
Blueprint: Fully inspected [x]
Outcome: SIGNED OFF (pending [Z] human items) | HALTED: <reason>
```

### Phase 4 — Blueprint

Only a `FAITHFUL` spec reaches here. Spawn **foreman** as a subagent against it. Foreman is
mode-agnostic — it doesn't need to know an orchestrator called it; it reads the spec and the
contract, writes the blueprint, and reports a status. You pass the path and route on what comes
back.

**Pass it:**
- the spec path Phase 3 marked `FAITHFUL` — `Planning/specs/[feature]_spec.md`,
- the start slice (Slice 1, unless resuming).

(Foreman reads `CLAUDE.md` itself for the stack and the real test command — you don't supply those.)

**It produces:**
- `Plumbline/blueprints/[feature]_BP.md` — or, for a build over 10 slices, the part files
  `[feature]_BP_p-1.md`, `[feature]_BP_p-2.md`, … (foreman splits mechanically; this is **not** a
  halt — a long build is just a long build),
- a **status** reported back to you.

**Route on the returned status — do not read the blueprint to second-guess it:**

| Status | Homeowner does |
|--------|----------------|
| `BLUEPRINT_READY` | Proceed to **Phase 5 (build til green)**. Carry forward every blueprint path — there may be more than one part file. |
| `BLUEPRINT_BLOCKED: <reason>` | **Halt.** Surface the reason verbatim. A human resolves it before the build resumes. |

**Reading a block.** Phase 3 already guaranteed the spec exists, is faithful, carries `**Done when:**`
items, and has no Open Questions — so foreman's spec-side stop conditions should never fire here. The
one block that legitimately can is **no real test command in `CLAUDE.md`** — a contract/scaffold gap
foreman can't write real `Test:` lines against. That's a genuine human fix, not a gate failure.
If instead a block cites a spec reason (missing spec, Open Questions, no Done-when), that means the
Phase 3 gate let something through — surface it as a **gate miss**, don't paper over it by re-running.

Then append the Phase 4 block to the run log.

### Phase 5 — Build til green

Drive **builder** to `BUILD_COMPLETE`, spawning the independent **inspector** at each risky slice
and looping fix⇄inspect within a bound. This is where the unattended early-catch lives: no human is
watching between slices, so a flagged slice is proven *before* code stacks on it.

**Inspection level: `flagged`** — never `none`. Homeowner always inspects `[inspect]` slices; that
mandatory early-catch is the whole reason an unattended build is safe. (A human run may choose `none`;
Homeowner may not.)

**Spawn builder** with: the blueprint (Slice 1 of part 1, unless resuming), inspection level
`flagged`. Builder flows slice-to-slice on its own — part-file boundaries are invisible to you, it
crosses them itself — and returns only at a status that needs you:

| Builder status | Homeowner does |
|----------------|----------------|
| `SLICE_DONE_INSPECT: N` | Inspection is due. **Spawn inspector** (fresh subagent) scoped to slice N; route on its result (below). |
| `BUILD_COMPLETE` | Carry the deviations path forward; proceed to **Phase 6 (final sign-off)**. |
| `STUCK: <where/why>` | **Halt.** Surface verbatim; the codebase is in a known state. A human resolves before resuming. |

(You never see `SLICE_DONE` — that's builder's internal "keep flowing" between unflagged slices.
`FIXES_COMPLETE` appears only inside the fix loop below.)

**On `SLICE_DONE_INSPECT` — spawn inspector, then route on its result:**

| Inspector result | Homeowner does |
|------------------|----------------|
| `PASS` | Resume **builder** from the next slice. |
| `FAIL: N` | Enter the **fix loop** (below) — there are findings to repair. |
| `BLOCKED: <reason>` | **Halt** — a precondition is missing (run command won't launch, no run command). There's nothing for builder to fix, so **never route this into the fix loop**; surface for a human. |
| `[human-required]` items | **Collect, don't grade, don't block.** Homeowner can't get human sign-off mid-run — carry these to the final report; the automated items decide whether the slice passes. |

**The fix loop (bounded).** A failed slice inspection routes back to builder, governed — never
improvised:

1. Spawn **builder in fix mode**. For a mid-slice fail the findings live in the inspector's `❌ FAIL`
   stamp on the slice (mid-slice checks write no report); for a final fail, in the final report. Its
   failure items are the step list.
2. Builder returns `FIXES_COMPLETE` (suite green) or `STUCK`. On `STUCK`, **halt** — surface it.
3. **Re-spawn a fresh inspector** on slice N.
   - `PASS` → resume builder from the next slice.
   - `FAIL` → loop from step 1, counting the cycle.
4. **Cycle bound: 3 fix⇄inspect rounds per slice** (tunable). If the slice still fails after the
   bound, **halt** — `HALTED: <slice N>, <why it won't pass>`. A slice that can't be made to pass
   in three governed rounds needs a human; spinning further just burns the build. Builder's own
   three-attempt-per-test cap sits *inside* each fix run — this bound is the outer limit on whole
   inspect-fix rounds (it catches the oscillation a per-test cap can't: fixes that go green yet keep
   failing inspection, e.g. a low-fidelity test the inspector won't accept).

Every inspector is a **fresh subagent** — the one spawned to re-check a fix never saw the build
*or* the previous inspection — and **only Homeowner ever spawns inspector**; builder reports a
status and never grades its own work.

Then append the Phase 5 block to the run log — every inspected slice, every fix cycle, the builder's
final status, and the deviations path.

### Phase 6 — Independent sign-off

`BUILD_COMPLETE` reaches here. This is the proof the whole run exists for: an independent inspector
verifies the running software against the **spec's `**Done when:**` items** — the actual acceptance
criteria, which Phase 5's per-slice checks never touched (mid-slice verifies slice scope, not spec
items). Nothing is signed off until this passes.

**Spawn inspector as a fresh subagent**, scope **final** — not a continuation of the build *or*
of any Phase 5 mid-build inspection. Pass it the feature, `final`, and the run/demo command (it
reads the spec, searches the blueprint parts for what's owed, and reads `CLAUDE.md` itself).

It verifies every spec Done-when item, judges test fidelity, captures evidence, writes
`Plumbline/inspect/Inspect_[feature]_Final_[date]_[HH-MM].md`, and — on a clean pass — ticks the
blueprint's **Fully inspected** box. (Homeowner ran Phase 5 at `flagged`, so every `[inspect]` slice
already carries a PASS stamp; the inspector's deferred-sweep finds nothing owed.)

**Route on the returned status:**

| Status | Homeowner does |
|--------|----------------|
| `PASS · needs-human: Z` | **Run signed off.** The Z `[human-required]` items are *not* a halt — they can't be auto-graded and there's no human mid-run, so carry them to the final report for the human to sign off async. Then write the closing report. |
| `FAIL: N` | Enter the **same bounded fix loop as Phase 5** (3 fix⇄inspect rounds; builder fix mode reads the **final report**; a **fresh** inspector re-checks each round; HALT on exceed or builder `STUCK`). |
| `BLOCKED: <reason>` | **Halt.** A precondition is missing (run command won't launch) — nothing to fix, so never route to the fix loop. Surface for a human. |

**`PASS` with human-required items is success, not a stall.** An unattended run *cannot* close those
itself; finishing with evidence captured and the items listed is the correct terminal state, not a
failure. The human signs them off on their own time.

**Commit the signed-off build (git mode).** On `SIGNED OFF` in **git** mode, honor the contract's
*every change ends in a commit*: nothing has been committed since scaffold, so stage the whole verified
build and commit it once — `git add -A`, then a message like `Build [feature]: signed off (Plumbline)`.
This is the autonomous stand-in for the human who would otherwise commit per the Change rules, and it
commits *verified* work (the build just passed independent sign-off). **Only on success** — a halted
run commits nothing, leaving the working tree intact for resume. In **none** mode, skip: the files on
disk are the record.

Then append the Phase 6 block to the run log and write the closing report.

---

## Closing report

End every run — signed off or halted — with a **short summary and the links**, so whoever started it can act without opening the log.

**Always:**
- **Outcome**, one line: `SIGNED OFF` (pending [Z] human items), or `HALTED at Phase [N] — [why]`.
- **Run log:** `Plumbline/homeowner/HomeownerLog_[date]_[HH-MM].md` — the full phase-by-phase trail.

**On `SIGNED OFF`, give the deliverable at a glance:**
- **Files created / changed by the build** — in **git** mode, from the sign-off commit: `git diff --stat --name-status <scaffold-commit>..HEAD` (run *after* the commit above — `git diff` against the working tree alone misses the still-untracked build files, which is exactly why the build is committed first). In **none** mode (no git), aggregate the **Files written/modified** that builder reported at each slice — that is the build's own record.
- **Tests:** [N] tests, [N] passed (from the final inspection).
- **Inspection issues:** `none` for a clean PASS — otherwise note what wasn't clean: weak-fidelity tests that were fixed, slices that needed fix cycles, or anything still owed.
- **Human sign-off owed:** the [Z] `[human-required]` items, listed — these are the human's to verify (`none` if zero).
- **Assumptions to confirm:** the low-surprise defaults architect made (Phase 2 `ASSUMPTIONS`), so the human can override any before relying on the build (`none` if zero).
- **Deviations:** [N] logged (`Plumbline/deviations/…`) or none · **Final inspection:** `Plumbline/inspect/Inspect_[feature]_Final_[date]_[HH-MM].md`.

**On `HALTED`, give the resume path instead** (no file list — the deliverable isn't done):
- Which phase halted and the failing status verbatim (Open Questions · builder `STUCK` · `HALTED` after the fix bound · inspector `BLOCKED`).
- Exactly what input a human must provide to resume, and the artifact to look at (the spec, the stuck step, the failing criterion).
