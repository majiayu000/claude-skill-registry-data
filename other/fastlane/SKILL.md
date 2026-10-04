---
name: fastlane
description: >-
  Use when delegating fast implementation work to a bounded Codex worker lane
  such as GPT-5.3-Codex, GPT-5.3-Codex-Spark, or a GPT-5.4 low/mini lane,
  especially when a high-reasoning parent should preserve cognitive budget for
  architecture, synthesis, proof, integration, and final acceptance. Treat
  Fastlane as a living universal workflow: after repeated use, propose skill
  updates when reusable delegation lessons emerge.
---

# Fastlane

## Purpose

Use this workflow to turn a bounded worker model into a fast implementation
lane while the parent agent stays responsible for architecture, acceptance
criteria, proof integrity, integration, and final verification.

Worker lanes are excellent for quickly producing a patch when the task is
bounded and the context is complete. Treat them as high-speed implementers, not
as the final gate.

## Operating Rule

**Delegate construction; centralize judgment and integration.**

The parent protects its cognitive budget. A frontier parent may run on a
premium high-reasoning model, but it should spend that reasoning on translating
the human idea into mission, architecture, lane contracts, proof design,
integration, and synthesis. It should write routine code only when the edit is
smaller than delegation overhead or when it is repairing an integration gap
found during final proof.

The parent agent must:

- choose whether model control or full-history fork matters more;
- choose the smallest capable worker lane for the task;
- take a baseline snapshot before delegation;
- define the exact mission and write scope;
- include all critical context and constraints;
- provide exact verification commands, not guessed script names;
- require causal proof, not just "tests passed";
- monitor for scope drift while the worker works;
- inspect the returned patch;
- integrate the returned work into the surrounding system;
- perform wiring and hardening before reporting acceptance;
- run independent verification;
- harden gaps before accepting.

## Repository-Agnostic Rule

Fastlane is universal. Never assume a specific repository, framework, artifact
name, proof format, docs layout, branch policy, or release ritual.

Before delegation, infer the current repo's conventions from local files and
commands. Use repo-native names such as its test scripts, proof artifacts,
changelog, release notes, checkpoint docs, snapshots, screenshots, or generated
outputs only after discovering them locally.

If the repo has no docs, changelog, checkpoint, scorecard, or proof artifact
convention, do not invent one as part of the fastlane task unless the user
explicitly asks. Instead, report what was verified and what artifact sync would
be useful.

## Glossary

- **Worker lane**: a bounded sidecar model tasked with construction, audit,
  research, or support work under a parent-owned contract.
- **Spark**: short operational name for the `gpt-5.3-codex-spark` research
  preview lane, used for near-instant compact iteration when available.
- **Coder lane**: `gpt-5.3-codex` for substantial bounded code-only work when
  Spark is not needed.
- **xhigh / high / medium / low**: reasoning effort tiers. Use the lowest tier
  that can satisfy the proof contract without increasing parent rework.
- **fork_context**: spawn flag controlling whether the worker inherits the
  parent's full conversation history. `true` inherits and forces parent model
  settings; `false` allows explicit model/effort overrides but requires the
  parent to embed all needed context in the prompt.
- **Proof artifact**: any repo-native file that records observable runtime
  behavior: log, screenshot, JSON status file, generated output snapshot.
- **Artifact Sync Gate**: the parent's final pass to align repo-native public
  docs, changelog, or evidence files with the verified behavior, run only
  when those conventions already exist or the user explicitly asks.

## Living Skill Loop

Fastlane is a living skill. When the parent agent uses Fastlane several times
in a row, or sees the same failure mode more than once, it should look for
improvements to the universal workflow.

Propose a Fastlane skill update when a pattern is:

- repeated across multiple delegated tasks or likely to recur in other repos;
- about delegation quality, model/effort selection, proof integrity, runtime
  preflight, artifact sync, handoff format, ownership boundaries, or
  anti-false-positive checks;
- expressible without project-specific names, paths, domains, or one-off
  commands.

Do not update the skill for:

- a repo-specific convention that belongs in that repo's docs;
- a one-off bug fix;
- a preference that has not improved proof or reduced rework;
- a memory that only makes sense with private conversation context.

Update protocol:

1. Name the reusable lesson in one sentence.
2. Explain why it belongs in Fastlane rather than the current repo.
3. Propose the smallest universal wording change.
4. If the lesson is already covered by existing wording, edit it. Do not
   append a duplicate.
5. Apply the update only if the user explicitly asks, or if the current
   instruction already authorizes updating the skill.
6. At most one skill update proposal per Fastlane session, to prevent drift.
7. Validate frontmatter, template consistency, and absence of repo-specific
   names before reporting completion.

## When To Use

Use this skill when the user asks to:

- use Codex Spark, GPT-5.3-Codex, a worker, subagent, xhigh, high, medium, or
  low for fast implementation;
- test a delegated implementation workflow;
- split implementation from verification;
- make a bounded code change where the parent can continue as quality gate.

Avoid this workflow when:

- the task is unclear or exploratory only;
- the next step is immediately blocked on analysis that the parent should do
  locally;
- the write scope cannot be isolated;
- a false positive would be expensive and no runtime proof is possible.

## Model And Effort Selection

Choose the worker by lane fit first, then reasoning effort.

- Use `gpt-5.3-codex` as the default coder lane for bounded code-only
  implementation, debugging, focused refactors, tests, and repo-native patches.
- Use `gpt-5.3-codex-spark` when near-instant compact text/code iteration
  matters and Spark is available.
- Use `gpt-5.4` low or `gpt-5.4-mini` medium for low-risk mechanical support
  lanes where speed and cost matter.
- Use `gpt-5.4` high or `gpt-5.5` high for audit lanes, proof-gap hunting, and
  edge-case review.
- Keep `gpt-5.5` high/xhigh primarily as the parent or rare frontier worker for
  ambiguous, long-context, high-stakes synthesis.

Use medium or low only when all of these are true:

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

Escalate effort or model when:

- the worker must infer missing architecture;
- the patch crosses ownership boundaries;
- the proof path is subtle or easy to fake;
- the first attempt produces broad rewrites, guessed commands, or vague
  handoff claims;
- parent review finds a causal proof gap.

Never change the parent/global model mode to test a fast lane. Model/effort
experiments happen only inside the sidecar worker.

## Delegation Protocol

### Before spawning the worker

1. Inspect enough local context to write a precise task.
2. Capture a baseline: `git status -sb`, relevant focused diff/grep, and known
   command names from `package.json` or repo scripts.
3. Decide spawn mode:
   - To force a specific worker model or effort, spawn with
     `fork_context: false` and embed full task context in the prompt.
   - When full conversation history matters more, use `fork_context: true`
     and omit model/effort overrides because forked agents inherit the parent
     settings.
4. State the implementation goal in one paragraph.
5. Give explicit file ownership and forbidden surfaces.
6. Tell the worker it is not alone in the codebase and must not revert unrelated
   changes.
7. Define acceptance criteria in terms of observable proof.
8. Require final handoff with files changed, commands run, proof artifacts,
   exact proof fields, model/effort rationale, limitations, and concerns.

### Parent Integration Loop

1. Read the changed files or focused diff.
2. Compare the result against the baseline: distinguish files the worker actually
   changed from files already dirty before delegation.
3. Integrate the patch with adjacent code paths the worker did not own: CLI
   wiring, imports, registry entries, docs hooks, fixtures, schemas,
   adapters, generated-contract surfaces, or artifact plumbing when those
   are required for the feature to be usable.
4. Harden obvious gaps immediately: path safety, compatibility fallbacks,
   error handling, deterministic artifacts, anti-false-positive checks, and
   contract drift guards.
5. Look for false positives where the test may not exercise the new path.
6. Run unit tests yourself.
7. Run runtime or integration proof yourself.
8. Inspect generated proof artifacts, screenshots, logs, or browser output.
9. Add any final hardening found by proof inspection.
10. Close the worker once accepted or superseded.

The parent should not hand back a raw worker patch when local wiring or
hardening is clearly needed. A Fastlane is complete only after the parent has
converted the worker's slice into an integrated, verifiable repo state.

### When To Abort vs. Iterate

Discard the patch and re-delegate with smaller scope (do not try to salvage)
when any of these appear:

- gross ownership violation (worker wrote outside declared owned files);
- fabricated proof (claimed artifacts that do not exist or use the legacy
  path);
- broad unauthorized rewrite of files the patch was not supposed to touch;
- handoff claims pre-existing dirty files as newly created;
- repeated guessed command names after the parent supplied the real ones.

Iterate (ask the worker to refine) when:

- ownership was respected but proof signal is weak;
- wiring is missing but the core slice is correct;
- a single anti-false-positive check needs adding.

### While the worker is still running

- Do useful non-overlapping review setup locally.
- If the worker runs longer than expected, inspect `git status`, focused
  diffs, or proof artifacts without redoing its assigned implementation.
- Stop or redirect only if it touches forbidden surfaces, changes ownership
  boundaries, or appears to be solving the wrong problem.

## Proof Contract

For every delegated feature, define two paths whenever possible:

1. Legacy path still works.
2. New path is exercised and leaves a different observable mark.

Examples:

- Generated smoke path: proof contains `runtime_smoke.source=generated`.
- Fallback smoke path: proof contains
  `runtime_smoke.source=generated-fallback` and `fallback_generated=true`.
- Cache miss path: log/proof contains `cache=miss`.
- Migration path: DB schema version changes and migrated data is still
  readable.

If existing behavior can mask the new path, require a force flag or
deterministic setup that makes the new path unavoidable.

### When there is no runtime path

For pure refactor, docs, or typing tasks where no runtime mark exists,
substitute the runtime contract with a **structural diff snapshot**: a
before/after capture of a public signature, exported API surface, fixture
shape, or generated contract file. The structural snapshot replaces
"observable runtime mark" as the causal proof.

## Anti-False-Positive Rules

Do not accept:

- "I removed X" if the generator recreates X before the relevant stage.
- "Unit tests cover it" when the claim is about runtime behavior.
- "Smoke passed" if the smoke used the old path.
- "Smoke failed" without checking whether the app/server/runtime prerequisite
  was running.
- A guessed command name when the repo has a different script in
  `package.json`.
- A handoff that claims already-dirty files were newly created by the worker.
- Docs claiming success before proof artifacts confirm it.

Ask the worker to explicitly answer:

- What proves the new code path ran?
- Which proof file contains it?
- Which field, log line, status, or output confirms it?
- What could still be masking a false positive?
- Which commands were copied from repo scripts, and which were inferred?
- Which files were already dirty before it started?
- Which model and effort were used, and why was that lane chosen?
- Did this run reveal a reusable Fastlane workflow improvement the parent
  should consider?

## Command And Runtime Preflight

Fastlane tasks often fail for boring reasons: wrong script name, no dev
server, stale port, missing env, or a worker assuming a runtime is alive.

Before delegation, the parent should give the worker:

- exact command names copied from `package.json`, Makefile, task runner, or
  docs;
- required services and ports, for example `npm run dev` serving
  `http://127.0.0.1:7777`;
- whether the worker may start background services or should leave runtime proof
  to the parent;
- expected artifact paths for browser screenshots, logs, or proof JSON.

If a runtime command fails, the worker must classify it:

- `code-failure`: the patch broke behavior;
- `environment-blocker`: service, port, credential, or external runtime
  missing;
- `command-error`: command name or invocation was wrong.

The parent still reruns the final runtime proof independently.

## Prompt Template

Read `references/delegation-template.md` when preparing a worker task. It
contains a reusable prompt with context, ownership, acceptance criteria,
verification, and handoff sections.

Use the template as a starting point, then fill in project-specific paths,
commands, proof fields, and risk notes.

## Case Notes

Field-tested lessons from real Fastlane runs are kept in
`references/case-notes.md`. Read them when designing a new delegation,
especially for generator work, runtime/browser proof, or medium-tier worker
runs. The examples there are illustrative; adapt to the artifacts native to
the current repo.

## Parent Gate Checklist

Group A: **Pre-acceptance (mandatory before any sign-off)**

- [ ] Parent used the correct spawn mode for the goal: model override
      without full fork, or full fork without override.
- [ ] Baseline dirty state was captured before delegation.
- [ ] Worker changed only owned files or justified exceptions.
- [ ] Worker did not claim pre-existing dirty/new files as newly created by
      its patch.
- [ ] Verification command names match actual repo scripts.
- [ ] Unit tests pass locally.
- [ ] Integration/runtime proof passes locally.
- [ ] The new behavior has a distinct proof signal (or a structural diff
      snapshot when no runtime path exists).
- [ ] Proof artifacts are named in the final report.
- [ ] Limitations are honest and not reframed as success.

Group B: **Integration**

- [ ] Parent integrated the returned work with adjacent wiring required by
      the feature.
- [ ] Parent performed local hardening before declaring the lane accepted.
- [ ] The patch preserves existing CLI/API compatibility unless explicitly
      allowed.

Group C: **Post-acceptance (conditional)**

- [ ] Repo-specific docs, changelog, release notes, checkpoints, scorecards,
      or public artifacts match the verified behavior **when those
      conventions exist**.
- [ ] For a major checkpoint or category uplevel, the Artifact Sync Gate
      ran: update only the repo-native public/method docs and evidence files
      that exist or are explicitly requested.
- [ ] If several Fastlane runs exposed a repeated workflow pattern, the
      parent proposed a universal skill update or recorded why no update is
      warranted (max one proposal per session).
