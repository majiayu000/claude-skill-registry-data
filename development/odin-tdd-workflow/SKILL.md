---
name: odin-tdd-workflow
description: Orchestration doctrine for the TDD workflow — gather behavioral context when it is not established, plan the packages, the execution shape, and the commits, execute reviewed red-green-refactor packages, and commit each planned batch only after its reviews pass. Standalone; run to completion as a stage of a larger plan.
---

# TDD Workflow

## Purpose

Define the orchestration doctrine for the TDD workflow — a trigger-gated workflow that turns work packages into reviewed, committed code. It packages the pattern `[Context → Review] │ Plan │ Checkpoint │ ( Package → Review )… │ [Integrate → Review] │ ( Commit → Review )… │ Response`.

**Judgment and mechanics have separate owners.** Kvasir authors one plan Workfile in the workspace and touches no project file; Brokk implementation sessions change the tree and never commit; a fresh Brokk commit session records one planned batch strictly by its plan row and the reviews that gate it, and decides nothing. No role writes in another's medium.

**The plan step receives no review — permanently, for this one step.** Its gates are the plan checkpoint, where the user or adoption ratifies it, and the reviews of every session that executes it. The standing per-Subtask review applies to every Brokk and Mimir session, **the commit session included**: it is a Brokk session, and no exception is claimed for it.

This skill is dispatch doctrine only. `mimir-tdd-context`, `kvasir-tdd-planning`, `brokk-test-driven-development`, `brokk-tdd-commit`, and `heimdall-tdd-review` are the per-step methodologies, loaded by the dispatched sessions themselves. Briefs name the skill, the inputs, and the output to write — **never the method**.

**Fixed Deliverable (per § Deliverables and § Deliverable Determination in your system prompt):** a Response (drafted by Bragi, step 7) and an Artifact (the code and tests, committed on the plan's branch):

```text
Deliverable: response=yes, artifact=yes — code and tests committed in the target project on the plan's branch (left uncommitted in the working tree only when a review blocked the run before that batch's commit), source=workflow-fixed
```

**Kvasir Consultation Check:** this workflow is exempt (`Kvasir check: substantive Subtasks=<n>, criteria=<…> → skip — packaged workflow`). Its strategic consultation is internal — the plan step — and its plan checkpoint is the user's steering point. Mid-Execution Consultation and Failed Review Classification remain in force inside the workflow.

## When to Use

- When the TDD check verdict is **invoke** — via the `/yggdrasil/tdd` command, explicit test-driven-development, test-first, or red-green-refactor language without requirements-analysis or architecture-before-implementation intent, or a user-accepted suggestion, per the Trigger Thresholds in your Communication Policy.
- **As a stage of a larger plan:** run this workflow to completion, exactly as you run Research or Deliberation. No request line and no result line exist.
- **Inputs it consumes from the conversation:** the objective; the architecture Workfile when one exists (its §5 interfaces are the contracts, its Appendix B the packages); the requirements Workfile when one exists; and a test command and executed baseline when the conversation already established them. Standalone, none of the three Workfiles usually exists: the context step then supplies the test command and the baseline, and the plan step derives exactly one package from the objective, its criteria restated from the request and labelled derived.

**Firing criteria** — when test-first implementation by this workflow is warranted at all. It fires when ANY: test-driven development, test-first implementation, or red-green-refactor is asked for; a bounded change that fits the existing structure states its behavior testably — a bug with a reproduction, a feature with stated behavior, a behavior-preserving refactor wanting characterization tests; the user asks that a change land as reviewed commits. It fires **without exception as the Software Engineering workflow's implementation stage** — that workflow writes code no other way. It **never** fires for a change expected to introduce structure or to split into two or more work packages: the split is an architecture decision, and that request is the Engineering check's, which runs this workflow inside it. Skip when the change is trivial — a typo, a constant, a rename, documentation — or the user asks for direct implementation.

A bounded implementation request with stated, testable behavior and no test-first language is the *suggestion candidate*; a pure research request or a question is a **skip**.

## Workflow

1. **Context (conditional).** Skip Mimir only when the current behavior of the touched paths, the engineering conventions beside them, and the test infrastructure — runner, exact commands, layout, fixtures, and an **executed** baseline — are already established in the conversation, by the user or by a reviewed `NN-context-tdd-*.md` from this session, or when the objective is greenfield. An architecture-context Workfile is **never** a skip reason: structure establishes neither behavior nor a baseline. Record the skip as `Context: skipped — <reason>`, never silently. Otherwise dispatch.

    Brief: the objective; the declared scope — the write sets and consumed contracts of the architecture Workfile's Appendix B when it exists, else the objective's touched paths; the acceptance criteria the work owns; and the requirement that the output be **fact-rich and framing-poor**, with proofs per finding and the baseline **executed**. Writes `NN-context-tdd-<area>.md`; its standing review is `Focus: context`.

2. **Plan (unreviewed).** Dispatch Kvasir with `kvasir-tdd-planning`, the objective, the path of the Workfile to **create** (`NN-plan-tdd.md`), and the paths of the architecture, requirements, and context Workfiles that exist — or, when no context Workfile exists, the test command and baseline the conversation established. Record from its report: the `TDD plan:` line, the `Package check:` line, the commit plan one line per batch, the `Branch:` and `Tree at planning:` facts, the baseline, and the risks and gaps. **Every plan ships at `Status: Proposed`**; the checkpoint ratifies it.

    Two preconditions the plan checks and reports rather than guesses. A test command it cannot source means the step-1 skip was wrong: fire the context step and re-dispatch planning. More than one package needed with no architecture Workfile stops the run before any implementation dispatch. As a stage of the Software Engineering workflow, its shape verdict was wrong and the Architecture stage must fire. **Standalone**, the run ends with a Response that names the route — the Software Engineering workflow (`/yggdrasil/engineer`), whose architecture stage makes the split this workflow does not — and nothing is left in the tree.

3. **Plan checkpoint (no dispatch).** Surface exactly: the context review verdict, or `Context: skipped — <reason>`; the baseline result; the packages with their owned criteria, kind, and mode; the execution shape and any waves; the **commit plan** — batches, order, types, subjects, the branch (current or to be created), and any baseline-dirty paths; the risks and gaps; and the dispatch cost, qualitatively, with the formula on request. Whether to pause for steering or auto-proceed is governed by your Communication Policy.

    When pausing, the user may adjust the packages, the mode, the batches, the subjects, or the branch. Record each change as `Plan amended: <field>=<value> — <reason>`, carry the amended values in the briefs, and leave the Workfile as drafted — the plan is a record of what was proposed, and the amendments are the record of what was steered. When auto-proceeding, ratify by adoption and let the summary ride the Deliverable disclosure.

4. **Execute (per package, in plan order).** Dispatch Brokk per package with `brokk-test-driven-development`: the plan Workfile path and the package name; the architecture and requirements Workfile paths when they exist; the `Phase:` and `Mode:` control lines; and the reviewed-but-uncommitted paths already in the tree from the current batch (`none` when the batch is starting).

    **Every session stops uncommitted, reporting `Commits: none`.** Its standing review is `Focus: package`, echoing that session's `Phase:` and `Mode:` lines; supply the evidence block, the write set, the pinned `HEAD`, and the reviewed-but-uncommitted list with the dispatch.

    - **Integrated mode (default):** one session per package runs red → green → refactor. Two dispatches per package.
    - **Split-phase mode (opt-in, per the plan):** a `Phase: red` session and its review, then a **fresh** `Phase: green+refactor` session and its review. Four dispatches per package.
    - **Parallel wave:** the scaffold package completes, passes review, **and is committed (step 6) before fan-out**; wave sessions carry `Mode: parallel`, run their own test subset only, and never leave their write set. Two to four per wave.
    - **Sequential:** `Mode: solo`; a session whose batch already holds reviewed uncommitted work receives that path list as read-only.

5. **Integrate (iff a parallel wave ran).** Dispatch one Brokk session with `brokk-test-driven-development`, `Mode: solo`, `Phase: full`, the plan's integration package (its write set is the union of the wave's plus the scaffold's), briefed with the seams the wave's evidence blocks reported. It runs the full suite; a seam fix that changes behavior gets a failing test first, by the skill's own rule; it stops uncommitted. Its standing review is `Focus: integration`. **Not fired for a sequential plan:** each solo session's baseline and final runs are already the full suite, and the commit step re-runs it.

6. **Commit (per batch).** When every review the batch's `Gate` names reads PASS or PASS-WITH-NOTES — and never before, never on BLOCKED — dispatch a **fresh** Brokk session with `brokk-tdd-commit`: the plan Workfile path and the batch number, the paths of the gating review Workfiles, and the pinned pre-commit `HEAD`. It verifies the gate itself, verifies or creates the branch, stages exactly the reviewed paths by name, **re-runs the full suite on the combined tree**, commits with the plan row's type and subject, and returns the commit record. Its standing review is `Focus: commit`.

    **Interleaving rule** — the one sequencing rule you apply mechanically: *a batch commits as soon as its last gating review passes, and before the first package of the next batch is dispatched.* So `HEAD` is always the clean reference for the next package's diff, the reviewed-but-uncommitted list a brief carries only ever names packages of the *current* batch, and a wave's commit follows its integration review. A red combined tree at this step commits nothing and goes to Mid-Execution Consultation.

7. **Deliverable (Response).** Dispatch Bragi to draft the user-facing response from the reviewed outputs: the packages, their owned criteria covered and not covered, and their test evidence; **the commits — hash, type, subject, branch, and whether the branch was created**; the baseline and the final suite result; the assumptions adopted; the risks and gaps; what the user should verify; and any work left uncommitted, with the reason. Writes `NN-response-draft.md`. **When this workflow is a stage of a larger plan, these items ride the enclosing plan's Response and this step is folded into it.**

**Failure handling (one rule, two specifics).** A `BLOCKED` context, package, or integration review goes through § Failed Review Classification: resume the producing session **once** for an execution defect; a plan-level mismatch, or a second `BLOCKED`, ends the run — that batch is not committed, the uncommitted work stays in the tree and is disclosed, and **this workflow never reverts, stashes, or deletes working-tree changes**.

A `BLOCKED` commit review is the one different case: the commit is already history and this workflow never rewrites it. Resume the commit session **once** to land a corrective commit for a staging omission, and disclose both commits; anything else ends the run with the review path named. A red suite at commit time is not a review failure at all — it is Mid-Execution Consultation, re-dispatching the affected package.

**Review-skill assignment:** every review gate dispatches a fresh Heimdall session with `heimdall-tdd-review` and exactly one `Focus:` line.

| Reviewed node | Brief line | Workfile |
| --- | --- | --- |
| Context session (step 1) | `Focus: context` | `NN-review-context-tdd-<area>.md` |
| Each package or phase session (step 4) | `Focus: package`, echoing that session's `Phase:` and `Mode:` lines | `NN-review-package-<name>.md` |
| Integration session (step 5) | `Focus: integration` | `NN-review-integration.md` |
| Each commit session (step 6) | `Focus: commit` | `NN-review-commit-<n>.md` |

Supply the originating brief, the artifact paths, the pinned `HEAD` and baseline, and the reviewed-but-uncommitted list with every dispatch. The Kvasir and Bragi sessions receive no dedicated review.

## Quality Criteria

- **The plan is recorded before any implementation dispatch** — the `TDD plan:` and `Package check:` lines both, as the plan step reported them.
- **The plan checkpoint always happens**; only whether it pauses is policy-governed.
- **Parallel only when the plan's `Package check:` reads all `yes`**, with the scaffold committed before fan-out and the wave capped at four.
- **No session other than a `brokk-tdd-commit` session commits**, in any mode.
- **Every commit is preceded by PASS or PASS-WITH-NOTES on everything it contains, and is itself reviewed afterwards.**
- **Every commit is a green state**, proven by a suite run at commit time and re-run at its review.
- **The committed path set equals the reviewed set** — no unreviewed path lands, and no reviewed path is left behind.
- **A batch commits before the next batch starts**, so `HEAD` is always the clean reference for the next package's diff.
- **Every acceptance criterion traces to a test** that was observed failing first, at a named location.
- **Every skip and every amendment is recorded** with its reason, never taken silently.
- **The Deliverable discloses** the commits landed, the criterion coverage, and anything left uncommitted.
- **Cost (total dispatches, including the standing reviews):** `T = 2C + 1 + 2N·(1+S) + 2K`, where C is 1 when the context step fires, N is the package count including any scaffold and integration package, S is 1 in split-phase mode, and K is the number of commits in the plan; add 2 when this workflow runs standalone — the Response and the Final Review Gate. Minimum 5 (N=1, K=1); a sequential medium run (C=1, N=2, K=1) is 9; a full parallel run (C=1, N=4, K=2) is 15. Disclose it qualitatively at the checkpoint and quantitatively on request.

## Anti-Patterns

- **An implementing session committing "to save a dispatch."** Every commit goes through the commit step, after its review.
- **Committing on a BLOCKED review, or on no review at all.** The gate is a verdict line, not a sense that the work is done.
- **Committing while a wave is in flight.** The tree holds other sessions' partial work; the batch is the whole wave plus its integration.
- **Splitting a wave across batches**, or **batching packages whose write sets intersect** — neither boundary is a verifiable green tree state.
- **`git add .` in the commit session.** The reviewed union is the staged set, path by path.
- **Re-deriving or reshaping packages the plan (or Appendix B) already fixed.** The checkpoint is where a plan changes.
- **Two packages without an architecture document.** The split is an architecture decision; return to the enclosing plan, or — standalone — end the run and name `/yggdrasil/engineer`.
- **Guessing a test command** instead of firing the context step.
- **Re-introducing a review of the plan step "to be safe."** It was removed by design; the checkpoint and the execution reviews are its gates.
- **Rewriting history to repair a bad commit.** The fix is a corrective commit, disclosed.
- **Restating a specialist's method in a brief.** Name the skill, the inputs, and the output.
- **Skipping the Final Review Gate.** The Deliverable — the committed code and tests, and the Response — is user-facing output and must pass the gate like any other.
