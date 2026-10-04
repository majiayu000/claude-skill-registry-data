---
name: sflow-recover
description: Diagnose publication, artifact, projection, generation, branch, and transport blockers and explicitly apply only hash-bound safe recovery.
disable-model-invocation: true
argument-hint: "[WORK-ID]"
---
# Recover governed work safely

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** CLI validates/mutates; preserve exact results, warnings, publication status, artifacts/actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. `singularity-flow recover $ARGUMENTS --fetch --json` (optional `--phase <phase>`): blockers, preservation, `planId`; never inspect with `--apply`.
2. Follow action classifications, not blanket dirty-tree stops. Review `applicationPaths`: open drafts recheck prepublish; published changes require rollover. Preserve untracked `.sflow/results/**`; tracked/staged reports and source require review. Stop for divergence, remote failure or human authority. `repair-publication-authority:<phase>`/`repair-generation-change-set:<phase>` require their diagnostic before rollover; never waive them.
3. Preserve generations/bytes/pins. `repair-repository-test-runner:<phase>` routes repair to `/sf-code`. For `resolve-code-delivery-test-policy:<phase>` or unavailable inference, preview `singularity-flow story test-policy amend <WORK-ID> --reason "<reason>" --json`. Returned apply requires live human terminal review. Relay preparation/fresh-validation routes without executing. Approval refusal ends its turn; `/sf-reject` later for changed bytes. Post-commit telemetry/session failures are advisory.
4. Human-confirm `planId`, then `singularity-flow recover $ARGUMENTS --fetch --apply --confirm <planId>`. Reinspect stale plans.
5. Guided `begin-new-generation:<phase>` requires `generation.intent.consumed-changed`, current branch/phase, authenticated publication and no lifecycle/transport blocker. Inspect `git status --porcelain=v1 --untracked-files=all`, diffs and all untracked content, including README. `manual` `working-tree` requires human review/confirmation of owned, in-scope changes, not automatic refusal. Stop for protected, unrelated, unowned, conflicted, removed or symlink paths.
6. Preview with `singularity-flow phase rollover <phase> --json`. Compare work ID, phase, command and `confirmation` digest with fresh recovery. On mismatch, re-inspect. After user confirmation of exact digest, run the returned `singularity-flow phase rollover <phase> --confirm <digest>` once. Never route to `/sf-code` before rollover succeeds.
7. Read `testExecution.commands`. Use `requiredTestExecution`/logs for argv/cwd, exit, stderr, report/guidance. Authorized dependency repair permits retry without republishing unchanged source; prove the environment changed, not only source hashes. Open-intent authoring uses its producer; resume `/sf-code` after rollover clears recovery. Stop on unchanged conditions or three distinct repairs. Never submit/approve, reset, rebase, force-push, stash or discard. Report effects/preservation. Integrity cannot be risk-accepted; deviations require separate authorization.

TRP: `singularity-flow explain test-recovery`; returned actions only. Exceptions need delegated live review. Never answer approval cards or report failed/skipped/unavailable checks passed.
