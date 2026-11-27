---
name: hermes-runtime-repairs
description: >-
  Fix a generated Hermes wrapper, cron routine or profile at its repository-owned template or
  generator. When a patch is in Git but the running job is stale, check the staged output,
  materialize it through the owning repo and read back the authorized deployment. Not for
  hermes-updates.
metadata:
  revision: "2"
  areas: "software-development,work-management"
  targets: "hermes"
  summary: "repair the template/generator, prove the staged artifact, then deploy and read back the live runtime"
  summary_zh: "修模板/生成器、验证暂存产物，再部署并回读线上运行时"
  kind: "entry"
---

# Hermes runtime repairs

Repair repository-owned wrappers and scheduled routines without confusing source correctness with
deployment to Hermes profiles. Load the repository contract for its supported materializer commands.

## When to Use

- A repo owns a template/routine that is materialized into agent profiles, cron jobs, or wrapper
  scripts.
- A generated file misbehaves and the fix must go to the template/generator, not the generated copy.
- A reviewed candidate patch must be landed into a shared checkout and/or deployed to the live
  runtime.

## 1. Freeze scope and current inputs

- Verify relayed permission changes against the operator's primary record and current contract.
  Classify source edits, Git publication, and live runtime writes separately; standing commit/push
  authorization does not authorize profile/config/cron/session writes.
- Fetch and fast-forward before source work. Inspect current status/diff and patch applicability
  immediately before landing; peers and scheduled publishers can invalidate an earlier clean-tree
  report. When landing a candidate built against an earlier base, prove each target file
  byte-identical to that base (`git show <base>:<path>` piped to `cmp` against the working copy) —
  the shared HEAD moving on does not by itself invalidate the candidate, but a clean
  `git apply --check` alone does not prove the base content did not drift.
- Read the generator, template/routine, and actual consumer record. Enumerate all writes a broad
  apply performs before selecting an operation; role-limited apply may still reconcile identity,
  jobs, config, or databases.
- Trace routine text into stored prompts. If changing the body changes the expected cron prompt,
  include that exact prompt-only write in the runtime decision or report it as undeployed. Do not
  promise both "cron untouched" and "no new prompt drift".

## 2. Reproduce and repair at the source

- Reproduce through the existing generated wrapper under the reported PATH and cwd. An
  unmaterialized template with unresolved placeholders fails for a different reason and is not a
  valid reproduction.
- Discover masked interpreter paths from globs, not abbreviated tool output. Compare the same real
  payload under the reported interpreter and a capability-bearing interpreter.
- Build a red-capable focused test before editing the generator. Assert the exact output and return
  code; shell-pipeline success is not the payload's exit status.
- Fix the template and generator, never only the generated file. Probe required capabilities rather
  than Python versions; pin the selected launcher, preserve a runtime override, and fail explicitly
  before executing the payload.

## 3. Prove the staged artifact

- Regenerate an isolated fixture home through the actual generator and check it again. Exercise its
  wrapper under the hostile environment; label fixture results and staged real-payload smoke tests
  separately from live-profile results.
- Inspect lease lookup before gate tests. Release only your own editing lease before tests that
  observe it; a fixture registry may still consult a module-level checkout lease and suppress
  expected work. Do not change gate logic or release another writer's lease to manufacture green
  tests.
- Run focused regressions before required full-suite and portability/validation gates. Report
  `ran / failures / errors / skipped`; distinguish the historical baseline total from the patched
  suite with new cases. Skipped cases are not executed passes.
- If shared source changes during verification, test the repair with a fresh snapshot in isolation.
  Never overwrite the other writer's changes or label a failed unchanged-source comparison as
  preservation proof.

## 4. Land source without mixing other writers' work

- Follow the actual standing publication contract and publisher guards. An `add -A` sweep does not
  preserve hunk isolation: make an authorized explicit selective commit before its sweep, or
  coordinate the publication boundary. Never stash, stage, or rewrite another writer's work to
  manufacture a clean landing.
- Stage explicit paths/hunks, run the required validation and secret scan, and preserve history.
  After an authorized push, re-fetch and compare the exact local and remote refs before claiming
  synchronization.
- A role-scoped write checker flags role-definition and test files as out-of-surface violations by
  design — they are no role's runtime write surface, and their acceptance runs through the
  generator's contract tests. Report the expected violation as such instead of routing the write
  through a role, widening the checker, or reading it as a failed gate.
- For change-only routines, keep the canonical baseline in persistent state, never scratch; read it
  before replacement. With no old baseline, record the first observation and state that comparison
  is unavailable, not "no changes". Preserve the existing comparison dimensions.
- Express baseline paths relative to the owning agent's persistent state home in portable
  instructions; keep harness-specific resolution in the binding. Verify that the scheduled consumer
  receives the new instructions, not just that the source file contains them.

## 5. Deploy only approved targets and read them back

- Refresh the exact live targets and back them up immediately before approved writes. Earlier
  backups may predate another writer's changes.
- Use the generator's narrow operation when only a script is approved; prove it in isolation before
  live use. Do not invoke broader role reconciliation for convenience.
- End-to-end command recipe for a generator that materializes into profiles (gate → lease → apply →
  sandbox → commit → materialize → read-back): `references/landing-and-deploy-recipe.md`.
- For an approved prompt-only job update, save that target's original prompt, use the supported
  scheduler interface, and preserve every other job field. Read back the exact job and compare
  non-prompt fields to the pre-write record.
- Compare the deployed wrapper to fresh generator output, execute that actual wrapper under the
  reported environment, and re-run drift checks against a fresh predeployment baseline. Separate
  intentional undeployed drift from unrelated findings; never clear excluded session/config state to
  make a checker silent.
- Stop when the approved acceptance proof is complete. Report source landed, staged payload verified,
  live deployed, or awaiting authorization explicitly; a clean Git tree and passing tests do not
  prove deployment.

## 6. Close the handoff without chatter

- If only an operator's decision remains, stop peer acknowledgement ping-pong. A corrected authority
  claim is not a new authorization.
- When the operator explicitly asks for status or continuation, provide a substantive checkpoint:
  landed artifact and proof, remaining gated actions, and the single required decision. Do not answer
  a direct request with silence or call source-only work "done".
