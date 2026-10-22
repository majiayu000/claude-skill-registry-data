---
name: sdlc-pipeline
description: Guided orchestrator that shepherds a project through the full SPEAKMAN.AI SDLC — Phase 1 architecture through Phase 4 infrastructure, then UAT, environment promotion, and pentest gates — invoking each phase skill in turn and carrying state (output paths, tech stack, promotion level, UAT results) between them so you are not re-asked what a prior phase already answered.
---

# sdlc-pipeline — SPEAKMAN.AI SDLC Shepherd

You drive a project through the full pipeline documented in `PIPELINE.md` at the root of this
repo: Phase 0 (Idea Intake, optional) → Phase 1 (Architecture) → Phase 2 (Requirements) →
Phase 3 (Code Generation) → Phase 4 (Infrastructure) → Promotion Gate 1 (local→DEV) →
Promotion Gate 2 (DEV→STG) → Pentest + UAT (both against **STG**) → Promotion Gate 3
(STG→PROD).

**You do not reimplement any phase's logic.** Each phase already exists as its own skill
(`generate-project-brief`, `generate-sad`, `generate-requirements`, `generate-speakmanai-code`,
`generate-infrastructure`, `promote-environment`, `pentest`, `generate-uat-tests`). Your job is
sequencing, state hand-off, and knowing where the pipeline must legitimately stop for a human.

**Three hard stops you cannot automate past:**
1. **Pentest gate approvals** happen only in the pentest companion app's UI (Gate 2, 3, 4). You dispatch the engagement, then wait.
2. **UAT execution** is a human working through `uat_test_cases.md` in a real browser. You generate the file, then stop.
3. **A BLOCKED promotion report** must be resolved by the developer. You never silently continue past a FAIL.

**One rule that isn't a stop but is just as easy to get wrong:** pentest and UAT run against
**STG**, not DEV — STG is the more stable, closer-to-production target. And any code change
made to fix a pentest or UAT finding **invalidates every promotion gate already passed**.
There is no such thing as "just re-run Level 3" after a fix — Level 1 and Level 2 validated
a version of the code that no longer exists. Re-run from Level 1, redeploy through DEV and
STG again, then re-test against the fresh STG deployment.

---

## Step 0 — Checkpoint Detection

Ask the user for the project's working directory (the parent dir passed to Phase 1/2, or
the Phase 3 `REPO_PATH` if you already have a codebase). Check for an existing checkpoint:

```
{PROJECT_ROOT}/.sdlc_pipeline/checkpoint.json
```

If found, read it and display:
```
══════════════════════════════════════════════════
  SDLC PIPELINE — CHECKPOINT FOUND
══════════════════════════════════════════════════
Project      : {checkpoint.repo_name}
Last phase   : {checkpoint.last_step_completed}
Saved at     : {checkpoint.checkpoint_at}
══════════════════════════════════════════════════
Resume from checkpoint? (yes / no — no starts a fresh pipeline here)
```

If yes, load **STATE** from the checkpoint (see the fields listed in Step 1) and jump to the
step matching `last_step_completed`. If no, or no checkpoint exists, continue to Step 1.

If the user doesn't know which phases they've already run, ask them to point you at any
existing `outputs/*/raw/` directories or an existing codebase — infer what's already done
from what's on disk rather than assuming a fresh start.

---

## Step 1 — Collect Pipeline-Wide Inputs

Ask only what no phase skill will ask on its own:

> "What is the project/repo name?"
> "Where should everything live? (parent directory — Phase 1/2 outputs and the Phase 3 repo will be created under here)"
> "What's the target tech stack? (e.g. `Go 1.22, chi, SQLite` or `Python, FastAPI, Postgres`) — this drives the Phase 3 variant and is confirmed again during Phase 2's tech-stack gate, but tell me now so I can carry it forward without you repeating it"
> "Target cloud for Phase 4? (GCP / AWS / Azure — press Enter to decide later)"

Store as **STATE**:
```json
{
  "repo_name": "",
  "project_root": "",
  "tech_stack": "",
  "target_cloud": "",
  "phase0_brief": null,
  "phase1_dir": null,
  "phase2_dir": null,
  "phase25_dir": null,
  "repo_path": null,
  "uat_file": null,
  "fix_cycles": 0,
  "last_step_completed": null,
  "checkpoint_at": null
}
```

Write the checkpoint after every step below — this pipeline routinely spans multiple
sessions (architecture review, a requirements gate, days of Phase 3 implementation).
Never lose STATE between turns.

---

## Step 1a — Phase 0: Idea Intake (optional)

Ask: "Is the business idea already a clear description you could hand an architect, or is it
still rough — a pitch, a Slack thread, a half-formed idea?"

- **Already clear** — skip this step. Phase 1 accepts the raw text/file/URL directly.
- **Still rough** — invoke `generate-project-brief` in Create mode. Let it run its own
  discovery (fast path or coaching path is the user's call, not yours to preempt). When it
  reports `brief.md`'s path, store as `STATE.phase0_brief`.

Update checkpoint: `last_step_completed: "PHASE0_DONE"` (or skip straight to `"PHASE1_DONE"`
bookkeeping if this step was skipped — no separate marker needed for a no-op).

---

## Step 2 — Phase 1: Architecture

Ask: "Run Phase 1 now with `/generate-sad`, or do you already have a SAD output directory?"

- **Already have one** — collect the path, store as `STATE.phase1_dir`, skip invocation.
- **Run it** — invoke the `generate-sad` skill. If `STATE.phase0_brief` is set, pre-answer its
  Step 1 business-input question with that file path instead of asking the user to restate the
  idea. Let it run the rest of its own Step 0–6 exactly as written. When it reports its output
  directory (`outputs/YYYY-MM-DD_{slug}/`), store as `STATE.phase1_dir`.

Update checkpoint: `last_step_completed: "PHASE1_DONE"`.

Ask: "Continue to Phase 2 now, or pause here? (You can resume this pipeline any time — the checkpoint is saved.)" If pause, stop and remind the user how to resume (re-invoke `/sdlc-pipeline` and point at `{PROJECT_ROOT}`).

---

## Step 3 — Phase 2: Requirements

Invoke `generate-requirements`. Pre-answer what you already know instead of letting it
re-ask:
- Phase 1 source → `STATE.phase1_dir` (skip its "where is Phase 1 output" question)
- Output parent → `STATE.project_root`

Let it drive its own `MCP_REQUIREMENTS_ENGINEERING_V1` session and human-in-the-loop gates
(tech stack confirmation, naming review, field definitions review) — these require real
judgment calls you should surface to the user verbatim, not pre-approve on their behalf.

When it reports its output directory, store as `STATE.phase2_dir`. If it reports any
`[DECISION REQUIRED]` items or deferred reviewer gates, surface them now — don't silently
carry an incomplete contract set into Phase 3.

Update checkpoint: `last_step_completed: "PHASE2_DONE"`.

---

## Step 3a — Phase 2.5: UX Design (optional)

Ask: "Run Phase 2.5 (`/generate-ux-design`) now? It maps the architecture and requirements
into a screen inventory and produces mockups for you to review before code generation — skip
it and Phase 3 will infer UI decisions on its own instead of building toward a reviewed target."

- **Skip** — no state change, continue to Step 4.
- **Run it** — invoke `generate-ux-design`. Pre-answer:
  - Phase 1 source → `STATE.phase1_dir`
  - Phase 2 source → `STATE.phase2_dir`
  - Output parent → `STATE.project_root`
  Let it drive its own delegate step (mockup design — this is real work you do yourself when
  the pause reaches you) and its human review gate exactly as written — **never self-approve
  the design review on the user's behalf**, surface every mockup individually. When it reports
  its output directory, store as `STATE.phase25_dir`.

Update checkpoint: `last_step_completed: "PHASE25_DONE"` (or leave at `"PHASE2_DONE"` if skipped
— no separate marker needed for a no-op).

---

## Step 4 — Phase 3: Code Generation

Invoke `generate-speakmanai-code`. Pre-answer:
- Phase 2 source → `STATE.phase2_dir`
- Phase 2.5 UX mockups (if `STATE.phase25_dir` is set) → point it at the `mockups/` directory as a visual reference target, not code to copy verbatim
- Project root / repo name → `STATE.project_root` / `STATE.repo_name`
- Tech stack → `STATE.tech_stack` (still let the router confirm the derived VARIANT — if it
  doesn't match what you expected, surface that mismatch to the user before proceeding)

This phase commits at every milestone gate (domain → application → infrastructure →
interface → UI styling → E2E). **If any gate fails, stop the pipeline here** — do not
attempt Phase 4 against a codebase with a broken milestone. Report the failure and wait for
the user to fix it, then resume.

When it reports `REPO_PATH`, store it in `STATE.repo_path`.

Update checkpoint: `last_step_completed: "PHASE3_DONE"`.

---

## Step 5 — Phase 4: Infrastructure

Invoke `generate-infrastructure`. Pre-answer:
- SAD dir → `STATE.phase1_dir`
- Requirements dir → `STATE.phase2_dir`
- Project root (codebase) → `STATE.repo_path`
- Target cloud → `STATE.target_cloud` (ask now if it wasn't given in Step 1)

This produces Terraform files and applies in-place hardening fixes — it does not deploy.
Tell the user the manual next steps it reports (state bucket creation, `build.sh`,
`deploy.sh` plan/apply) are theirs to run outside this pipeline; do not run them yourself.

Update checkpoint: `last_step_completed: "PHASE4_DONE"`.

---

## Step 6 — Gate: Promotion Level 1 (local → DEV)

Invoke `promote-environment` with level = `local-dev` and project root = `STATE.repo_path`.

- **BLOCKED** → stop. Report the FAILURES verbatim. Do not proceed to Level 2 against a
  codebase this gate rejected. Wait for the user to fix and re-run this step.
- **PASS** → continue.

Update checkpoint: `last_step_completed: "GATE1_PASSED"`.

Tell the user: "Deploy to DEV now (via `infra/scripts/deploy.sh dev apply`, run manually),
then confirm when it's live so we can run the DEV→STG gate."

---

## Step 7 — Gate: Promotion Level 2 (DEV → STG)

Invoke `promote-environment` with level = `dev-stg` and project root = `STATE.repo_path`.
Same BLOCKED/PASS handling as Step 6 — do not proceed to STG deployment against a rejected
codebase.

Update checkpoint: `last_step_completed: "GATE2_PASSED"`.

Tell the user: "Deploy to STG now (via `infra/scripts/deploy.sh stg apply`, run manually),
then confirm when it's live — pentest and UAT both target STG, not DEV, because it's the
more stable, closer-to-production environment."

---

## Step 8 — Gate: Pentest (against STG)

Ask: "Is there an approved engagement for this project in the pentest companion app
(status `GATE_1_APPROVED`), scoped at the **STG** URL? Paste the engagement ID, or say
'skip' to defer this gate."

- **Engagement ID given** — invoke `pentest` with that engagement ID. It will dispatch
  workers, upload logs, and then **poll for human gate approvals in the companion app**.
  This is a genuine stop: do not attempt to move to the UAT step while `/pentest` is
  mid-poll. When `/pentest` reports Gate 4 approved and complete, continue.
- **Skip** — note in STATE that pentest was deferred. Warn the user this gate must run
  against STG before STG→PROD promotion (Level 3 does not itself check for a completed
  pentest, but shipping without one defeats the purpose of Phase 4's hardening work).

Update checkpoint: `last_step_completed: "GATE_PENTEST_DONE"` (or `"GATE_PENTEST_SKIPPED"`).

If the pentest report contains findings that require a code change, **do not fix them and
continue on the assumption Level 1/2 still hold.** Go to Step 9a (Fix Loop) once UAT is also
done, or immediately if UAT was already run — either way, a fix here means Level 1 and 2
must be re-run before Level 3.

---

## Step 9 — Gate: UAT (against STG)

Invoke `generate-uat-tests`. Pre-answer:
- Phase 1 dir → `STATE.phase1_dir`
- Phase 2 dir → `STATE.phase2_dir` (required)
- Project root → `STATE.repo_path`
- Output path → `{STATE.project_root}/uat` (matches where `promote-environment` level 3
  looks by default)
- Application URL → the live **STG** URL — ask for it explicitly, do not default to DEV or
  `localhost`

Store the resulting file path as `STATE.uat_file`.

**This is a hard stop.** Tell the user:
> "UAT test cases are ready at `{STATE.uat_file}`. Work through every test case against the
> STG environment, then re-run `/sdlc-pipeline` and I'll pick up from here once the file
> shows no blank Status cells."

Update checkpoint: `last_step_completed: "UAT_GENERATED"`. Do not proceed further in this
same run — this always requires a new invocation after the human finishes testing.

On resume at this step: read `STATE.uat_file` and check whether any Status cell is blank.
If any are blank, repeat the stop message above. If all are filled, continue to Step 9a.

---

## Step 9a — Fix Loop Check

Ask: "Did the pentest report or any UAT test case surface something that required, or will
require, a code change?"

- **No** — continue to Step 10.
- **Yes** — this is the point people skip and shouldn't. Tell the user:
  > "Since the code is changing, Level 1 and Level 2 promotion no longer describe the
  > current codebase. Once the fix is committed: re-run this pipeline from Level 1
  > (`/promote-environment 1`), redeploy DEV and STG, and re-run pentest/UAT against the
  > **fresh** STG deployment — not just the specific test case or finding that failed."

  Update checkpoint: `last_step_completed: "GATE1_PASSED"` (reset — Level 1/2 are no longer
  valid) and store a note in STATE (`STATE.fix_cycles += 1`) so the final report shows how
  many times the pipeline looped here. Jump back to Step 6.

---

## Step 10 — Gate: Promotion Level 3 (STG → PROD)

Invoke `promote-environment` with level = `stg-prod`, project root = `STATE.repo_path`, and
UAT file = `STATE.uat_file`. This re-runs every Level 1 and 2 check plus hardening and the
functionality score computed from the UAT file.

- **BLOCKED** → report verbatim, including any failing/not-run UC-IDs from the
  functionality report. Stop.
- **PASS** → the project is cleared for PROD.

Update checkpoint: `last_step_completed: "GATE3_PASSED"`.

---

## Step 11 — Final Report

```
══════════════════════════════════════════════════
  SDLC PIPELINE — {STATE.repo_name}
══════════════════════════════════════════════════
Phase 0  Idea Intake        : {done | skipped} → {STATE.phase0_brief}
Phase 1  Architecture      : {done | skipped} → {STATE.phase1_dir}
Phase 2  Requirements       : done → {STATE.phase2_dir}
Phase 2.5 UX Design         : {done | skipped} → {STATE.phase25_dir}
Phase 3  Code Generation    : done → {STATE.repo_path}
Phase 4  Infrastructure     : done → {STATE.repo_path}/infra
Gate     Promotion 1 (DEV)  : PASS
Gate     Promotion 2 (STG)  : PASS
Gate     Pentest (STG)      : {done | skipped}
Gate     UAT (STG)          : done → {STATE.uat_file}
Fix cycles                  : {STATE.fix_cycles}
Gate     Promotion 3 (PROD) : PASS
══════════════════════════════════════════════════
Cleared for production promotion.
```

Delete the checkpoint file — the pipeline is complete:
```bash
rm -f "{PROJECT_ROOT}/.sdlc_pipeline/checkpoint.json"
```

---

## Rules

- **Never re-derive what a phase skill already produces.** Pass forward paths and confirmed
  decisions; let each phase skill drive its own contract generation, code, or checklist.
- **Never pre-approve a human-in-the-loop gate on the user's behalf** (Phase 2 reviewer
  gates, pentest companion-app gates, UAT execution). Surface them; do not skip them.
- **Never proceed past a BLOCKED or FAILED gate.** Stop, report verbatim, wait for a fix.
- **Checkpoint after every step.** This pipeline is expected to span multiple sessions.
- **UAT and pentest are always hard stops**, even when everything else in the run is
  fully automatable — they require a human or an external app, respectively.
- **Pentest and UAT always target STG, never DEV.** STG is the more stable,
  closer-to-production environment both gates should be exercising.
- **A code fix invalidates every gate already passed.** There is no such thing as "just
  re-run the one that failed" — a pentest or UAT finding fixed locally means Level 1 and
  Level 2 validated code that no longer exists. Always loop back to Level 1, not to
  wherever the finding surfaced.
- **Infrastructure apply is always manual.** `generate-infrastructure` produces files; you
  never run `terraform apply` or `deploy.sh` yourself.
