---
name: sflow-start
description: Explicitly choose a remote base, intake source, and workflow; create and publish the canonical Story branch.
disable-model-invocation: true
argument-hint: "<WORK-ID> [--jira | manual story details] [documents and URLs]"

---
# Start work

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Explicit choices; no preselection; preserve errors/artifacts/actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Require WORK-ID. Read `singularity-flow workspace current --json`. If the selected repository is `missing`/`empty`, run `singularity-flow workspace repair <WORKSPACE-PATH> --repository <REPOSITORY-ID> --level readiness --json`. Re-read; use ready `repositoryPath`, else opened Git root. Run `singularity-flow version` and `git status --short`; stop on failure or dirt.
2. Run `singularity-flow workspace branches --json --intake --work-id <WORK-ID>`. Unless `existingWork.status` is `new`, run `singularity-flow session candidates --json`; an existing ID routes to `/sf-session` or `singularity-flow resume <WORK-ID>`; never restart it.
3. Require its `repositories`. Check `singularity-flow workspace status <WORKSPACE-PATH> --level readiness --json`; repair required `missing`/`empty` members before preflight. On authority failure show Shell `singularity-flow workspace reinitialize --dry-run --json` and Copilot `/sf-admin`; never run `init` for an absent local workflow file.
4. Never preselect. Choose `<BASE>`. Unless `intake.workflowCatalogScope` is `approved-configuration`, run step 6's command without `--work-type`. Choose `<WORKFLOW>` from its exact-base `intake.storyWorkflows`.
5. With `ask_user`, collect Jira/manual outcome, acceptance criteria, scope, risks, uniquely named documents. Read-only references need ID, credential-free URL and branch: `--reference-repository ID=URL --reference-branch ID=BRANCH`. Never search for inputs. Pass `--jira`/`--story-file`; pair `--document`/`--document-url` with `--document-name`/`--document-url-name`.
6. Run `singularity-flow workspace branches --json --intake --preflight-story <WORK-ID> --from-branch <BASE> --work-type <WORKFLOW> --selected-base-only --mint-intake-receipt`. World Model, AST, model, telemetry, and Copilot availability are advisory. On missing/stale readiness, stop and show `/sf-ready` plus `singularity-flow precheck --run --scope dependency-test --json`. Never apply a persistent configuration upgrade here.
7. Start with the same base/workflow; never change the workflow choice. Start recomputes readiness before mutation. Add `--intake-receipt <preflight.intakeReceipt.id>` when issued. `poc-workflow` needs `--target-url`; the phase-default agent is automatic. If `ask_user` is unavailable, use step 8 or stop.
8. Without `ask_user`, require pinned configuration: `singularity-flow choices begin start <WORK-ID> --json`, `singularity-flow choices answer <TOKEN>`, then pass `--selection-receipt <TOKEN>` (15-minute, single-use).
9. After preflight passes, report readiness/base/receipt; offer `/sf-next`.

TRP: read `singularity-flow explain test-recovery`. Separate baseline disposition from test scope. Known failures require native evidence and delegated live review; never answer approval cards. Returned actions only.
