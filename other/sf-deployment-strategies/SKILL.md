---
name: sf-deployment-strategies
description: Covers how Salesforce metadata reaches an org — source deploy versus Metadata API versus change sets versus DevOps Center versus packaging, the full sf project deploy start flag surface, validate plus quick deploy as the production path, test levels and coverage rules, destructive changes, per-metadata-type deployment gotchas (Profiles, Flows, custom settings, record types, picklists, sharing rules, layouts, translations), environment promotion pipelines with git branching, drift and conflict detection, rollback reality, zero-downtime schema and Apex change patterns, CI/CD wiring, and the deployment error catalogue. Use this skill when a task mentions sf project deploy start, deploy validate, deploy quick, --test-level, RunLocalTests, destructiveChanges.xml, package.xml manifests, quick deploy job ids, deployment failures, promoting to production, rollback, or the vf-check deploy-validate / deploy-quick / verify checks.
---

# Salesforce Deployment Strategies

How vibe-force gets metadata into an org safely. Wave 3 of the harness workflow is exactly two
serial steps — `deploy-validate` then `deploy-quick` — and this skill explains why, what they
enforce, and everything that goes wrong around them.

API version for all examples: `67.0` (Summer '26), the `apiVersion` value in
`config/vibe-force.defaults.json`.

## When to use

- Building or debugging any `sf project deploy *` invocation.
- Deciding a test level and proving the coverage rule that applies to it.
- Deleting metadata (destructive changes) or deploying a type with known gotchas.
- Designing dev -> integration -> UAT -> production promotion and its git branching.
- Detecting drift between repo and org, or resolving source-tracking conflicts at deploy time.
- Planning a rollback, a forward-fix, or a zero-downtime schema/Apex change.
- Wiring CI/CD gates around `vf-check deploy-validate` / `deploy-quick` / `verify`.
- Not for scratch org or sandbox provisioning (skill `sf-scratch-orgs-sandboxes`), not for
  package versions (skill `sf-packaging-release`), not for writing the tests themselves
  (skill `sf-apex-testing`).

## Decision table: which delivery mechanism

| Mechanism | Use when | Avoid when |
| --- | --- | --- |
| `sf project deploy start` (source format) | Default for everything in this harness: dev, integration, UAT | You need a validated-then-quick production deploy |
| `sf project deploy validate` + `sf project deploy quick` | **Production.** Long test runs you cannot afford to fail at the end of a change window | Sandboxes — validate/quick are documented as production-only |
| `sf project deploy start --metadata-dir <dir>` | You hold a metadata-format ZIP/dir from another tool | Source-format projects (the normal case) |
| Change sets | Admin-only, one-off, click-path change with no repo | Anything the repo owns; there is no review, diff, or replay |
| DevOps Center | Org-centric teams that want a UI over git work items | Agent-driven pipelines that need deterministic CLI exit codes |
| Unlocked / managed packages | Versioned, installable artifacts with an upgrade path | Fast iteration inside one org; see skill `sf-packaging-release` |

## Test levels

| Level | Runs | Coverage rule | Allowed on |
| --- | --- | --- | --- |
| `NoTestRun` | nothing | none | Development environments only (sandbox, DE, trial). Default for development environments. **Not** accepted by `deploy validate` |
| `RunSpecifiedTests` | only `--tests` | each class **and each trigger in the deployment package** must reach 75% individually | any |
| `RunLocalTests` | all org tests except those from installed managed and unlocked packages | org-wide 75% overall, and Apex triggers must have some coverage | any; default for production deploys that include Apex, and the default for `deploy validate` |
| `RunAllTestsInOrg` | all tests including managed package tests | as `RunLocalTests` | any |
| `RunRelevantTests` (Beta) | tests Salesforce infers from the payload and its dependencies | each class and trigger in the package must reach 75% individually | any |

Default behaviour when `--test-level` is omitted depends on the payload and the target org. For a
production deploy, all non-managed tests run if the package contains Apex classes or triggers; if
the package has no Apex components, no tests run (API 34.0 and later). Never rely on that
inference in automation — always pass `--test-level` explicitly. `config/vibe-force.defaults.json`
pins `testLevels.sandbox` and `testLevels.production` to `RunLocalTests`.

`--tests` is space- or repeat-separated, **not** comma-separated:
`--tests AccountServiceTest ContactServiceTest "Test With Space"`.

## Core patterns

### 1. Everyday deploy (dev / integration / UAT)

```bash
sf project deploy start \
  --target-org vf-int \
  --source-dir force-app \
  --test-level RunLocalTests \
  --wait 45 \
  --coverage-formatters json --results-dir .vibeforce/reports/coverage \
  --concise
```

Full flag table: [references/deploy-command-reference.md](references/deploy-command-reference.md).

### 2. Narrow the payload

```bash
# by directory (repeat or space-separate)
sf project deploy start --source-dir force-app/main/default/classes force-app/main/default/objects --target-org vf-dev

# by type, by name, by wildcard (quote the wildcard)
sf project deploy start --metadata ApexClass --target-org vf-dev
sf project deploy start --metadata ApexClass:AccountService --target-org vf-dev
sf project deploy start --metadata 'ApexClass:Account*' --target-org vf-dev
sf project deploy start --metadata "Profile:My Profile" --metadata ApexClass --target-org vf-dev

# by manifest (children are included automatically)
sf project deploy start --manifest manifest/package.xml --target-org vf-uat
```

`--source-dir`, `--metadata`, and `--manifest` are mutually exclusive within one command.

### 3. Preview and dry run before you commit

```bash
sf project deploy preview --target-org vf-int                  # conflicts, deletions, ignored files
sf project deploy start --dry-run --test-level RunLocalTests --target-org vf-int --source-dir force-app
```

`--dry-run` validates and runs Apex tests but never saves. This — not `deploy validate` — is the
supported way to validate against a sandbox. There is no `--dry-run` flag on
`sf project retrieve start`; use `sf project retrieve preview` to see incoming drift.

### 4. Production: validate, then quick deploy

```bash
# Step 1 (long): validate. Returns a job id, saves nothing.
sf project deploy validate \
  --target-org vf-prod \
  --source-dir force-app \
  --test-level RunLocalTests \
  --coverage-formatters json --results-dir .vibeforce/reports/coverage \
  --wait 180 --verbose

# Step 2 (short): deploy the validated payload, skipping tests.
sf project deploy quick --job-id 0Af0x000017yLUFCA2 --target-org vf-prod --wait 60
```

The validation job id is valid for **10 days**. Quick deploy succeeds only if the validation
succeeded, its Apex tests passed, and coverage requirements were met. `--use-most-recent` on
`deploy quick` only searches validations from the **past 3 days**, so automation must persist the
job id rather than rely on it. Runbook, state-file contract, and hook interaction:
[references/validate-quick-deploy.md](references/validate-quick-deploy.md).

`vf-check deploy-validate` writes `{jobId, targetOrg, testLevel, validatedAt, expiresAt, sha}` to
`<project>/.vibeforce/state/deploy-jobs.json`; `vf-check deploy-quick` reads the newest
non-expired entry for the target org. The vibe-force hooks refuse a `deploy-quick` (and a raw
`sf project deploy start`) against any alias in `productionAliases` unless
`hooks.blockProductionDeploy` is `false` or `VF_ALLOW_PROD=1` is exported. `VF_HOOK_MODE=off`
disables the guard entirely and should never be used in CI.

### 5. Async, report, resume, cancel

```bash
sf project deploy validate --source-dir force-app --target-org vf-prod --async --test-level RunLocalTests
sf project deploy report --job-id 0Af0x000017yLUFCA2 --target-org vf-prod --wait 30
sf project deploy resume --job-id 0Af0x000017yLUFCA2 --wait 60      # also updates source tracking
sf project deploy cancel --job-id 0Af0x000017yLUFCA2 --target-org vf-prod --wait 10
```

`deploy report` does not update source tracking; `deploy resume` does. Exit codes:
`Succeeded` 0, `Canceled` 1, `Failed` 1, `SucceededPartial` 68, `InProgress`/`Pending`/`Canceling`
69.

### 6. Destructive changes

Deletions travel in a manifest alongside a `package.xml`. Wildcards are **not** supported in
destructive manifests.

```xml
<!-- manifest/destructiveChangesPost.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Account.Legacy_Score__c</members>
        <name>CustomField</name>
    </types>
</Package>
```

```xml
<!-- manifest/package.xml - required even for a delete-only deploy -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <version>67.0</version>
</Package>
```

```bash
sf project deploy start \
  --target-org vf-int \
  --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChangesPost.xml \
  --purge-on-delete \
  --ignore-warnings \
  --test-level RunLocalTests --wait 60
```

`--pre-destructive-changes` deletes before additions, `--post-destructive-changes` after — use
post when the additions remove the dependency that blocks the delete (for example, updating an
Apex class to stop referencing a field, then deleting the field in the same deploy).
`--purge-on-delete` bypasses the Recycle Bin. `--ignore-warnings` is the one legitimate CI use of
that flag: deleting a component that no longer exists in the org raises a warning that would
otherwise mark the deploy unsuccessful.

The vibe-force hooks block any command carrying `--pre-destructive-changes`,
`--post-destructive-changes`, or `--purge-on-delete` when `hooks.blockDestructive` is `true`
(the default) unless the run is explicitly approved.

### 7. Per-type gotchas

Profiles, Flows, custom settings, record types, picklists, sharing rules, layouts, and
translations each fail in their own way. One example, then the full table in
[references/metadata-gotchas.md](references/metadata-gotchas.md):

```bash
# WRONG: the flow's own <status>Active</status> is overridden by the flowDefinition
sf project deploy start --metadata Flow:VF_Lead_Router --target-org vf-int

# RIGHT: control activation explicitly through FlowDefinition.activeVersionNumber
sf project deploy start --metadata Flow:VF_Lead_Router FlowDefinition:VF_Lead_Router --target-org vf-int
```

If a `FlowDefinition` is part of the deployment, its `activeVersionNumber` wins over the `status`
field in the flow. Deploying `flowDefinitions` with a stale number silently activates the wrong
version.

### 8. Drift detection

```bash
# Does the org contain anything the repo does not know about?
sf project retrieve preview --target-org vf-int          # tracked orgs only
sf project deploy start --dry-run --manifest manifest/package.xml --target-org vf-prod

# Untracked orgs (production, Full/Partial sandboxes): retrieve and diff
sf project retrieve start --manifest manifest/package.xml --target-org vf-prod --output-dir /tmp/prod-snapshot
diff -ru force-app /tmp/prod-snapshot | head -200
```

Production never allows source tracking, so drift there is a git question, not a CLI question:
keep a scheduled job that retrieves the manifest and fails the build on a non-empty diff.

### 9. Environment promotion

`main` is what production runs. Feature branches build in scratch orgs; merges promote forward
through integration and UAT; production is a validate + quick deploy off the release tag. Branch
model, GitHub Actions YAML, JWT auth, and per-stage gates:
[references/pipeline-and-cicd.md](references/pipeline-and-cicd.md).

| Stage | Org | Command | Gate |
| --- | --- | --- | --- |
| feature | scratch | `deploy start --source-dir force-app` | `vf-check local` |
| integration | `vf-int` | `deploy start --test-level RunLocalTests` | `vf-check local` + `vf-check apex` |
| UAT | `vf-uat` | `deploy start --manifest ... --test-level RunLocalTests` | `vf-check verify` |
| production | `vf-prod` | `deploy validate` then `deploy quick` | `vf-check deploy-validate` -> `deploy-quick` -> `verify` |

### 10. Rollback reality

Salesforce has no native rollback. A failed deploy rolls back *itself* (unless
`--ignore-errors`), but a *successful* deploy that turns out to be wrong cannot be undone by the
platform. Four real options, in order of preference:

1. **Forward-fix.** Deploy the corrected source. Fastest, and the only option for data changes.
2. **Validated rollback package.** Before promoting, validate the *previous* release's payload
   against production and keep the job id. If the release goes wrong inside the 10-day window,
   `sf project deploy quick --job-id <rollback-job>` restores it in minutes with no test run.
3. **Destructive change plan.** For releases that add components, pre-author the
   `destructiveChangesPost.xml` that removes exactly what the release added.
4. **Backup retrieve.** Always retrieve the pre-deploy state of the affected manifest and commit
   it as an artifact, so the rollback payload exists even if the validated job expires.

```bash
# Pre-deploy backup + pre-validated rollback, both from the release job
sf project retrieve start --manifest manifest/package.xml --target-org vf-prod \
  --target-metadata-dir .vibeforce/reports/prod-backup --zip-file-name pre-$(git rev-parse --short HEAD).zip
git checkout "$PREVIOUS_TAG" -- force-app
sf project deploy validate --source-dir force-app --target-org vf-prod --test-level RunLocalTests --async
git checkout "$RELEASE_TAG" -- force-app
```

### 11. Zero-downtime change patterns

| Change | Wrong (breaks in flight) | Right |
| --- | --- | --- |
| Rename a field | rename in one deploy | add new field -> dual-write -> backfill -> switch readers -> delete old field in a later release |
| Remove a field | delete immediately | two-phase: stop writing and reading in release N, delete in release N+1 after verification |
| Tighten a required field | make required in the same deploy that adds it | add optional -> backfill -> add validation rule -> mark required |
| Change an Apex method signature | edit in place | add the overload, migrate callers, delete the old overload next release |
| Flip behaviour | deploy behaviour change directly | ship behind a custom permission or custom metadata flag, deploy dark, enable per-profile |
| Replace an active Flow | deploy new version and hope | deploy the new version inactive, then activate via `FlowDefinition.activeVersionNumber` |

Feature flags belong in custom permissions (checked with `FeatureManagement` or
`Schema.SObjectType`-free `Permission` checks) or custom metadata types, never in a hardcoded
boolean:

```apex
public with sharing class VFFeature {
    private static final Map<String, Boolean> CACHE = new Map<String, Boolean>();

    public static Boolean isEnabled(String flagName) {
        if (!CACHE.containsKey(flagName)) {
            VF_Feature_Flag__mdt flag = VF_Feature_Flag__mdt.getInstance(flagName);
            Boolean on = flag != null && flag.Is_Enabled__c;
            // A custom permission lets admins widen a flag per profile without a deploy.
            CACHE.put(flagName, on || FeatureManagement.checkPermission(flagName));
        }
        return CACHE.get(flagName);
    }
}
```

## Anti-patterns

| Anti-pattern | Consequence | Fix |
| --- | --- | --- |
| `--ignore-errors` on a production deploy | Components with errors are skipped and the org is left inconsistent | Never use it against production; fix the errors |
| `--ignore-conflicts` as a habit | Silently overwrites org changes a colleague made | `deploy preview`, resolve, then targeted `--ignore-conflicts` |
| `--test-level NoTestRun` to "make the deploy pass" | No safety net; rejected outright by `deploy validate` | Fix the failing test; see skill `sf-apex-testing` |
| `sf project deploy validate` against a sandbox | Documented as production-only; sandboxes do not run tests on deploy by default | `sf project deploy start --dry-run --test-level RunLocalTests` |
| `deploy quick --use-most-recent` in CI | Only finds validations from the past 3 days; picks up the wrong job on a busy org | Persist the job id in `.vibeforce/state/deploy-jobs.json` |
| Deploying the whole `force-app` to production every release | Multi-hour test runs, unrelated failures, huge blast radius | Manifest-scoped releases plus validate/quick |
| Re-running `deploy validate` because quick deploy failed | Another full test run; the original job may still be valid | `sf project deploy report --job-id` first; quick deploy again |
| Wildcards in `destructiveChanges.xml` | Silently ignored; nothing is deleted | List every member explicitly |
| `--purge-on-delete` by default | Deleted components skip the Recycle Bin and are unrecoverable | Only with an approved destructive plan |
| Deploying Profiles as whole files | Profile content depends on what else is in the payload; you get surprise permission changes | Permission sets for grants; deploy Profiles only with the components they reference |
| Treating a successful deploy as a verified release | Deploy success says nothing about behaviour | `vf-check verify` (org Apex tests + smoke), skill `sf-post-deploy-verification` |

## Verification

```bash
# Local gate first - never spend an org round trip on lint failures
node "$VF_ROOT/scripts/checks/vf-check.mjs" local --changed

# Sandbox: validate behaviour without saving
sf project deploy start --dry-run --source-dir force-app --test-level RunLocalTests --target-org vf-int --wait 60

# Production: the only sanctioned path
node "$VF_ROOT/scripts/checks/vf-check.mjs" deploy-validate --target-org vf-prod --json
node "$VF_ROOT/scripts/checks/vf-check.mjs" deploy-quick    --target-org vf-prod --json
node "$VF_ROOT/scripts/checks/vf-check.mjs" verify          --target-org vf-prod --json

# Evidence
sf project deploy report --job-id "$(jq -r '.jobs[-1].jobId' .vibeforce/state/deploy-jobs.json)" \
  --target-org vf-prod --verbose
ls .vibeforce/reports/
```

`deploy-validate` exits `1` on a gate failure (test failure or coverage below
`gates.apexOrgCoverageMin` / `gates.apexClassCoverageMin`), `2` on misconfiguration (no manifest,
unknown alias), `3` on an org or network error. `deploy-quick` exits `2` when no unexpired job id
exists for the target org — the correct response is to run `deploy-validate`, not to fall back to
`deploy start`.

## References

- [references/deploy-command-reference.md](references/deploy-command-reference.md) — every flag of
  every `sf project deploy *` command, exit codes, env vars.
- [references/validate-quick-deploy.md](references/validate-quick-deploy.md) — end-to-end
  production runbook, `deploy-jobs.json` contract, hook interaction, rollback windows.
- [references/metadata-gotchas.md](references/metadata-gotchas.md) — per-type deployment
  behaviour and the workaround for each.
- [references/pipeline-and-cicd.md](references/pipeline-and-cicd.md) — branching model, GitHub
  Actions YAML, JWT auth, promotion gates, coverage gating.
- [references/deployment-errors.md](references/deployment-errors.md) — error string -> cause ->
  fix catalogue.

Sibling skills: `sf-cli-operations` (auth, JWT, aliases), `sf-project-structure` (manifests,
package directories, `.forceignore`), `sf-apex-testing` (what `RunLocalTests` actually runs),
`sf-code-analyzer-quality` (the static gate ahead of deploy), `sf-scratch-orgs-sandboxes` (deploy
targets), `sf-packaging-release` (versioned artifacts instead of raw deploys),
`sf-post-deploy-verification` (wave 4), `sf-workflow-orchestration` (wave sequencing).

Official documentation used:

- Metadata API Developer Guide — Running Tests in a Deployment:
  <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_running_tests.htm>
- `deployRecentValidation()`:
  <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deployRecentValidation.htm>
- Deleting Components from an Organization:
  <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_deleting_files.htm>
- FlowDefinition:
  <https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_flowdefinition.htm>
- Salesforce DX Developer Guide — Release Your App to Production:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_build_mdapi_production.htm>
- Resolve Conflicts Between Your Local Project and Org:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_tracking_resolve_conflicts.htm>
- Salesforce CLI command reference and plugin messages:
  <https://github.com/salesforcecli/cli/blob/main/README.md>,
  <https://github.com/salesforcecli/plugin-deploy-retrieve/tree/main/messages>
