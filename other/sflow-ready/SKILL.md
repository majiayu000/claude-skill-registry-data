---
name: sflow-ready
description: Prove locked packages, installation health, test-framework setup, and existing unit tests before a Story worktree; optionally repair only reviewed dependency/test setup.
disable-model-invocation: true
argument-hint: "[--repair] [--full]"

---
# Make a repository ready before Story work

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Setup only: Never change product behavior, weaken tests, skip checks, upgrade versions, install
global tools, record secrets, or enter a Story worktree. Build, quality, application-start,
end-to-end are forbidden unless `--full` and approved policy permit them.

1. Require exact Git root/clean tree. Run `singularity-flow init --check --json`, then `singularity-flow precheck --quick --json`.
   Report test tools, adapters, and launcher availability.
2. Select `dependency-test` unless `--full` is requested. Run
   `singularity-flow precheck --run --scope <SCOPE> --json` once for its plan only. Show base,
   manifest digest, locked dependencies or frozen restore, test commands, structured test adapter,
   timeouts, omissions, and `planId`. For blockers, do not confirm or repeat
   the plan. Use `singularity-flow precheck --quick --json` to identify the native script,
   package-manager ambiguity, or missing reporter; offer the smallest reviewed setup repair.
3. Use `ask_user` to confirm the exact `planId`; otherwise stop with Copilot `/sf-ready` and Shell
   `singularity-flow precheck --run --scope <SCOPE> --confirm-plan <PLAN-ID> --json`. Execute once.
4. Report receipt or failed baseline: exact base/plan, exit, report hash, failing testcase IDs.
   Missing reports remain unavailable. Never commit local dependency directories, build output,
   test reports, or receipts.
5. Classify cache, setup, or existing failures. Use advertised TRP repair admission; feature coding
   waits for every required repository. Otherwise an existing unit failure needs a separate Bug-fix Story if not setup.
   For eligible JUnit/Jest/Vitest/Node TAP baselines, inspect with
   `singularity-flow precheck --risk-status --json`. Only on explicit choice record digest,
   reason, and expiry (at most 30 days) via `singularity-flow precheck --accept-test-risk
   --confirm-baseline <SHA256> --reason <TEXT> --expires <ISO-8601> --json`. Exact-base acceptance
   may allow Story creation, never marks tests passed or waives later publication checks.
6. Without `--repair`, stop. With it, ask before committable setup, create
   `sflow/readiness/<PLAN-DIGEST-PREFIX>`, edit only confirmed paths, and show full diff.
7. After explicit diff approval, rerun and commit only the reviewed paths. Do not push or
   merge unless separately requested. A commit changes the base; obtain a new `planId`,
   confirmation, and receipt.
8. Report the commit/blockers and handoffs: Copilot `/sf-start`; Shell
   `singularity-flow start <WORK-ID>`. A Git refusal retains the setup branch and creates no Story.

TRP: read and follow `singularity-flow explain test-recovery`; returned legal actions only.
