---
name: tempofastlane
description: >-
  Unified delegation and temporal-calibration protocol. Use when delegating
  bounded implementation work to a worker model such as GPT-5.3-Codex,
  GPT-5.3-Codex-Spark, or a GPT-5.4 low/mini lane while the high-reasoning
  parent preserves cognitive budget for architecture, synthesis, proof,
  integration, and final verification. Embeds TEMPONIZER into effort,
  abort/iterate, and parallelism decisions.
---

# TempoFastlane

## Purpose

Convert a worker model into a fast, bounded implementer while the parent agent
owns architecture, acceptance criteria, proof integrity, integration, and final
verification. Eliminate Temporal Inheritance Bias (TIB) from every delegation,
scoping, and iteration decision so that the worker is dispatched on empirical
wall-clock grounds rather than on human-derived planning priors inherited from
the training corpus.

The worker is excellent at quickly producing a patch when the task is bounded
and the context is complete. It is a high-speed implementer, not the final gate.
The parent enforces ownership, proof, integration, and hardening.

## Operating Rule

**Delegate construction; centralize judgment and integration. Apply temporal
calibration before any delegation, scoping, or iteration decision is made.**

The parent protects its cognitive budget. A frontier parent may run on a
premium high-reasoning model, but it should spend that reasoning on translating
the human idea into mission, architecture, lane contracts, proof design,
integration, and synthesis. It should write routine code only when the edit is
smaller than delegation overhead or when it is repairing an integration gap
found during final proof.

The parent agent must:

- decide whether model control or full-history fork matters more;
- choose the smallest capable worker lane for the task;
- take a baseline snapshot before delegation;
- define the exact mission and write scope;
- include all critical context and constraints;
- provide exact verification commands, not guessed script names;
- require causal proof, not merely "tests passed";
- monitor for scope drift while the worker runs;
- inspect the returned patch;
- integrate the returned work into the surrounding system;
- perform wiring and hardening before reporting acceptance;
- run independent verification;
- harden gaps before accepting;
- record actual wall-clock duration (`Te`) per phase to recalibrate temporal
  priors used by future delegations.

## Temporal Operating Rule (TEMPONIZER)

Pre-execution duration estimates produced by language model agents are
calibrated to human workflows present in training corpora rather than to the
agent's effective runtime behavior. This is Temporal Inheritance Bias (TIB).
Across repeated operational sessions, agents predict durations such as
"approximately 30 minutes" or "approximately 3 hours" while measured wall-clock
completion times are minutes or seconds, yielding large estimate-to-actual
ratios. TIB corrupts effort selection, abort/iterate decisions, parallelism, and
overall delegation strategy.

Correction heuristic: apply `Tc = alpha(phi) * Tp` for every duration claim,
where `Tp` is the inherited intuitive estimate, `phi` is the operational phase,
`alpha(phi)` is the phase-aware scalar, and `Tc` is the corrected prediction.

Operational phases:

- `GEN`: pure text or code generation, no external I/O.
- `IO`: tool calls, API requests, disk or network operations.
- `DBG`: integration work, debugging, multi-file reasoning.
- `PAR`: parallel execution of independent subtasks.

Initial prior: `alpha(phi) ~= 0.05` as a starting point. Recalibrate online
from measured `Te` per phase.

Calibration loop: estimate -> execute -> measure -> recalibrate. Every
execution emits a measured `Te` from initiation to final output, which updates
`alpha(phi)` for future runs. Without the loop, TIB persists.

Behavioral rules:

- Never assert a duration in minutes or hours without first identifying `phi`,
  applying `alpha(phi)`, and reporting the corrected figure in the smallest unit
  that fits.
- When uncertain, prefer underestimating and measuring over inheriting human
  intuition.
- Treat parallelism as the default execution shape, not as an advanced
  optimization. Issue independent tool calls in the same batch.
- The wall-clock is authoritative. The intuitive duration is a corpus artifact,
  not a measurement.

## Repository-Agnostic Rule

TempoFastlane is universal. Never assume a specific repository, framework,
artifact name, proof format, docs layout, branch policy, or release ritual.

Before delegation, infer the current repo's conventions from local files and
commands. Use repo-native names, such as its test scripts, proof artifacts,
changelog, release notes, checkpoint docs, snapshots, screenshots, and generated
outputs, only after discovering them locally.

If the repo has no docs, changelog, checkpoint, scorecard, or proof artifact
convention, do not invent one as part of the delegated task unless the user
explicitly asks. Instead, report what was verified and what artifact sync would
be useful.

## Glossary

- **Worker lane**: operational name for the delegated model tasked with
  construction, audit, research, or support work under a parent-owned contract.
- **Spark**: `gpt-5.3-codex-spark`, a research preview lane for near-instant
  compact text/code iteration when available.
- **Coder lane**: `gpt-5.3-codex` for substantial bounded code-only work when
  Spark is not needed.
- **xhigh / high / medium / low**: reasoning effort tiers. Use the lowest tier
  that can satisfy the proof contract without increasing parent rework.
- **fork_context**: spawn flag controlling whether the worker inherits the
  parent's full conversation history. `true` inherits and forces parent model
  settings. `false` allows explicit model and effort overrides but requires the
  parent to embed all needed context in the prompt.
- **Proof artifact**: any repo-native file that records observable runtime
  behavior: log, screenshot, JSON status file, generated output snapshot.
- **Artifact Sync Gate**: the parent's final pass to align repo-native public
  docs, changelog, or evidence files with verified behavior. Run only when those
  conventions already exist or the user explicitly asks.
- **TIB**: Temporal Inheritance Bias.
- **Tp / Tc / Te**: inherited estimate, corrected estimate, measured execution
  time.
- **alpha(phi)**: phase-aware temporal scalar.

## Living Skill Loop

TempoFastlane is a living skill. When the parent agent uses it several times in
a row, or sees the same failure mode more than once, it should look for
improvements to the universal workflow.

Propose a skill update when a pattern is:

- repeated across multiple delegated tasks or likely to recur in other repos;
- about delegation quality, model and effort selection, proof integrity, runtime
  preflight, artifact sync, handoff format, ownership boundaries,
  anti-false-positive checks, or temporal calibration;
- expressible without project-specific names, paths, domains, or one-off
  commands.

Do not update the skill for:

- a repo-specific convention that belongs in that repo's docs;
- a one-off bug fix;
- a preference that has not improved proof or reduced rework;
- a memory that only makes sense with private conversation context.

Update protocol:

1. Name the reusable lesson in one sentence.
2. Explain why it belongs in TempoFastlane rather than in the current repo.
3. Propose the smallest universal wording change.
4. If the lesson is already covered by existing wording, edit it. Do not append
   a duplicate.
5. Apply the update only if the user explicitly asks, or if the current
   instruction already authorizes updating the skill.
6. At most one skill update proposal per session, to prevent drift.
7. Validate frontmatter, template consistency, and absence of repo-specific
   names before reporting completion.

Temporal feedback into the loop: when measured `Te` diverges from `Tp` in a
stable per-phase pattern across runs, propose updating the default
`alpha(phi)` prior used in this skill. Subject to the one-proposal-per-session
limit.

## When To Use

Use this skill when the user asks to:

- use Codex Spark, GPT-5.3-Codex, a worker, subagent, xhigh, high, medium, or
  low for fast implementation;
- test a delegated implementation workflow;
- split implementation from verification;
- make a bounded code change where the parent can continue as quality gate.

Avoid this workflow when:

- the task is unclear or exploratory only;
- the next step is immediately blocked on analysis the parent should do locally;
- the write scope cannot be isolated;
- a false positive would be expensive and no runtime proof is possible.

## Model And Effort Selection

Effort is chosen on temporal-corrected grounds, not on intuitive task size.
Compute `Tc = alpha(phi) * Tp` and assess parental rework risk before selecting
a tier.

Choose the worker by lane fit first, then reasoning effort:

- `coder`: `gpt-5.3-codex` medium/high for bounded code-only implementation,
  debugging, focused refactors, tests, and repo-native patches.
- `spark`: `gpt-5.3-codex-spark` medium/xhigh for near-instant compact
  iteration when Spark is available.
- `fastworker`: `gpt-5.4` low or `gpt-5.4-mini` medium for low-risk mechanical
  support lanes.
- `auditer`: `gpt-5.4` high or `gpt-5.5` high for proof-gap hunting, edge-case
  review, and security-shaped checks.
- `parent`: `gpt-5.5` or `gpt-5.4` high/xhigh for mission synthesis,
  architecture, final proof, and integration judgment.

Use low or medium only when all of these are true:

- the task is bounded and mechanical;
- the write set is small and explicitly owned;
- the existing pattern is clear;
- acceptance criteria are observable;
- the parent can cheaply inspect and rerun verification;
- the worker is not being asked to make product, architecture, model-selection,
  or proof-policy decisions.

Low and medium are cost-control lanes, not context-control lanes. Give them the
same full task context, baseline dirty state, file ownership, forbidden
surfaces, proof criteria, and final handoff requirements as high or xhigh.
**Reduce task size, not instruction quality.**

Escalate model or effort when:

- the worker must infer missing architecture;
- the patch crosses ownership boundaries;
- the proof path is subtle or easy to fake;
- the first attempt produces broad rewrites, guessed commands, or vague handoff
  claims;
- parent review finds a causal proof gap.

Never change the parent or global model mode to test a fast lane. Model and
effort experiments happen only inside the sidecar worker.

Temporal note: a task that "feels large" is often `GEN` with `alpha ~= 0.05`
and suits medium. A task that "feels small" but contains `DBG` phases requires
xhigh. Size intuition is `Tp` inflated by TIB; do not let it drive tier choice.

## Delegation Protocol

### Before Spawning The Worker

1. Inspect enough local context to write a precise task.
2. Capture a baseline: `git status -sb`, relevant focused diff or grep, and
   known command names from `package.json` or repo scripts.
3. Decide spawn mode:
   - To force a specific worker model or effort, spawn with
     `fork_context: false` and embed full task context in the prompt.
   - When full conversation history matters more, use `fork_context: true` and
     omit model/effort overrides because forked agents inherit parent settings.
4. State the implementation goal in one paragraph.
5. Give explicit file ownership and forbidden surfaces.
6. Tell the worker it is not alone in the codebase and must not revert unrelated
   changes.
7. Define acceptance criteria in terms of observable proof.
8. Require final handoff with files changed, commands run, proof artifacts,
   exact proof fields, limitations, concerns, and per-phase `Te` if measurable.
9. Issue independent preparation calls in parallel: spawn, baseline capture,
   adjacent grep, and command discovery in one batch unless logically dependent.

### While The Worker Runs

- Do useful non-overlapping review setup locally.
- If the worker runs longer than the corrected `Tc` would predict, inspect git
  status, focused diffs, or proof artifacts without redoing its assigned
  implementation.
- Stop or redirect only if it touches forbidden surfaces, changes ownership
  boundaries, or appears to be solving the wrong problem.

### Parent Integration Loop

After the worker returns:

1. Read the changed files or focused diff.
2. Compare the result against the baseline. Distinguish files the worker
   actually changed from files already dirty before delegation.
3. Integrate the patch with adjacent code paths the worker did not own: CLI
   wiring, imports, registry entries, docs hooks, fixtures, schemas, adapters,
   generated-contract surfaces, or artifact plumbing when required.
4. Harden obvious gaps immediately: path safety, compatibility fallbacks, error
   handling, deterministic artifacts, anti-false-positive checks, and contract
   drift guards.
5. Look for false positives where the test may not exercise the new path.
6. Run unit tests yourself.
7. Run runtime or integration proof yourself.
8. Inspect generated proof artifacts, screenshots, logs, or browser output.
9. Add any final hardening found by proof inspection.
10. Record measured `Te` per phase and update local `alpha(phi)` priors.
11. Close the worker once accepted or superseded.

The parent must not hand back a raw worker patch when local wiring or hardening
is clearly needed. A TempoFastlane run is complete only after the parent has
converted the worker's slice into an integrated, verifiable repo state.

## When To Abort vs Iterate

Before abandoning a patch on the grounds that "iteration would take too long",
compute the corrected `Tc` for the iteration step. Iteration is almost always
cheaper than re-delegation because `Tp` is inflated by TIB.

Discard the patch and re-delegate with smaller scope when any of these appear:

- gross ownership violation;
- fabricated proof;
- broad unauthorized rewrite of files the patch was not supposed to touch;
- handoff claims pre-existing dirty files as newly created;
- repeated guessed command names after the parent supplied the real ones.

Iterate when:

- ownership was respected but proof signal is weak;
- wiring is missing but the core slice is correct;
- a single anti-false-positive check needs adding.

## Proof Contract

For every delegated feature, define two paths whenever possible:

1. Legacy path still works.
2. New path is exercised and leaves a different observable mark.

Examples:

- Generated smoke path: proof contains `runtime_smoke.source=generated`.
- Fallback smoke path: proof contains
  `runtime_smoke.source=generated-fallback` and `fallback_generated=true`.
- Cache miss path: log or proof contains `cache=miss`.
- Migration path: DB schema version changes and migrated data is still readable.

If existing behavior can mask the new path, require a force flag or
deterministic setup that makes the new path unavoidable.

When there is no runtime path, substitute the runtime contract with a
**structural diff snapshot**: a before/after capture of a public signature,
exported API surface, fixture shape, or generated contract file.

Temporal note on proof: do not reject a proof artifact on the grounds that it
executed too quickly. A smoke that completes in seconds is the wall-clock truth
correcting TIB, not a suspicious signal. Reject on causal content, not on speed.

## Anti-False-Positive Rules

Do not accept:

- "I removed X" if the generator recreates X before the relevant stage.
- "Unit tests cover it" when the claim is about runtime behavior.
- "Smoke passed" if the smoke used the old path.
- "Smoke failed" without checking whether the app, server, or runtime
  prerequisite was running.
- A guessed command name when the repo has a different script in `package.json`.
- A handoff that claims already-dirty files were newly created by the worker.
- Docs claiming success before proof artifacts confirm it.
- A duration claim stated without phase classification and `alpha(phi)` applied.

Require the worker to explicitly answer:

- What proves the new code path ran?
- Which proof file contains it?
- Which field, log line, status, or output confirms it?
- What could still be masking a false positive?
- Which commands were copied from repo scripts, and which were inferred?
- Which files were already dirty before it started?
- What was the measured `Te` per phase?
- Did this run reveal a reusable workflow improvement the parent should
  consider?

## Command And Runtime Preflight

Delegated tasks often fail for boring reasons: wrong script name, no dev server,
stale port, missing env, or a worker assuming a runtime is alive.

Before delegation, the parent should give the worker:

- exact command names copied from `package.json`, Makefile, task runner, or docs;
- required services and ports, for example `npm run dev` serving
  `http://127.0.0.1:7777`;
- whether the worker may start background services or should leave runtime proof
  to the parent;
- expected artifact paths for browser screenshots, logs, or proof JSON.

If a runtime command fails, the worker must classify it:

- `code-failure`: the patch broke behavior;
- `environment-blocker`: service, port, credential, or external runtime missing;
- `command-error`: command name or invocation was wrong.

The parent still reruns the final runtime proof independently.

## Coupling Rules: TEMPONIZER x Delegation

- Effort selection is a function of `alpha(phi) * Tp` and parental rework risk,
  not of intuitive task size. Reclassify before selecting a tier.
- Abort versus iterate is decided after computing corrected iteration cost. Most
  restart reflexes are TIB artifacts.
- Parallelism is mandatory for independent preparation steps. Spawn, baseline,
  grep, and command discovery share a single batch.
- Handoff requires `Te`. Per-phase wall-clock measurements feed the Living Skill
  Loop. "Done" without `Te` is an incomplete handoff when measurement was
  feasible.
- Proof speed is not a defect. Anti-false-positive review evaluates causal
  content, not duration.
- Skill updates are temporal-aware. Stable `Te` versus `Tp` drift per phase is
  itself grounds for proposing an `alpha(phi)` update, subject to the
  one-proposal-per-session limit.

## Prompt Template

Read `references/delegation-template.md` when preparing a worker task. It
contains a reusable prompt with context, ownership, acceptance criteria,
verification, handoff, and `Te` reporting sections.

Use the template as a starting point, then fill in project-specific paths,
commands, proof fields, risk notes, and expected phase classification.

## Case Notes

Field-tested lessons from real runs are kept in `references/case-notes.md`.
Read them when designing a new delegation, especially for generator work,
runtime or browser proof, medium-tier worker runs, or temporal recalibration
events. The examples there are illustrative; adapt to the artifacts native to
the current repo.

## Parent Gate Checklist

Group A: **Pre-acceptance**

- [ ] Parent used the correct spawn mode: model override without full fork, or
      full fork without override.
- [ ] Baseline dirty state was captured before delegation.
- [ ] Worker changed only owned files or justified exceptions.
- [ ] Worker did not claim pre-existing dirty or new files as newly created.
- [ ] Verification command names match actual repo scripts.
- [ ] Unit tests pass locally.
- [ ] Integration or runtime proof passes locally.
- [ ] The new behavior has a distinct proof signal, or a structural diff
      snapshot when no runtime path exists.
- [ ] Proof artifacts are named in the final report.
- [ ] Limitations are honest and not reframed as success.
- [ ] Per-phase `Te` was recorded when measurement was feasible.
- [ ] Any duration claim in the handoff was reported as `Tc` after applying
      `alpha(phi)`, not as raw `Tp`.

Group B: **Integration**

- [ ] Parent integrated the returned work with adjacent wiring required by the
      feature.
- [ ] Parent performed local hardening before declaring the lane accepted.
- [ ] The patch preserves existing CLI or API compatibility unless explicitly
      allowed.

Group C: **Post-acceptance**

- [ ] Repo-specific docs, changelog, release notes, checkpoints, scorecards, or
      public artifacts match verified behavior when those conventions exist.
- [ ] For a major checkpoint or category uplevel, the Artifact Sync Gate ran:
      update only repo-native public or method docs and evidence files that
      exist or are explicitly requested.
- [ ] If several runs exposed a repeated workflow pattern, the parent proposed a
      universal skill update or recorded why no update is warranted.
- [ ] If stable `Te` versus `Tp` drift was observed across runs, the parent
      considered an `alpha(phi)` prior update for this skill.

## Master Rule

Velocity without proof is a regression. Proof without temporal calibration is
TIB performing as discipline. TempoFastlane resolves both: temporal
self-correction unlocks empirically grounded velocity, and the delegation
protocol enforces ownership, causal proof, integration, and hardening over that
velocity. Apply both layers to every delegation, every effort selection, every
iterate-or-abort decision, and every handoff.
