---
name: sf-scratch-orgs-sandboxes
description: Covers provisioning and lifecycle management of Salesforce development environments — Dev Hub setup, scratch org definition files (edition, features, settings, objectSettings, snapshot, sourceOrg, release, hasSampleData), sf org create scratch / resume scratch / delete scratch, org shapes and scratch org snapshots, sandbox types and licenses, sf org create sandbox / refresh sandbox / resume sandbox / delete sandbox, sandbox definition files, Apex post-copy scripts, source tracking in scratch orgs and sandboxes, and ephemeral CI orgs. Use this skill when a task mentions project-scratch-def.json, "spin up a scratch org", scratch org allocations or expiry, snapshot, org shape, Dev Hub, sandbox refresh or clone, SandboxInfo, sandbox templates, source tracking conflicts, tracksSource, sf project reset tracking, or when deciding whether work belongs in a scratch org, a Developer sandbox, or a Full sandbox.
---

# Salesforce Scratch Orgs and Sandboxes

Environment provisioning for the vibe-force delivery harness. Every wave-0 scout run and every
wave-4 verification run needs a known-shape org; this skill decides which org, defines it
declaratively, and scripts its whole lifecycle.

API version for all examples: `67.0` (Summer '26), the `apiVersion` value in
`config/vibe-force.defaults.json`. Do not hardcode another version in project files.

## When to use

- Choosing between scratch org, Developer/Developer Pro sandbox, Partial Copy, and Full sandbox.
- Authoring or repairing `config/*-scratch-def.json` / `config/*-sandbox-def.json`.
- Creating, resuming, seeding, verifying, and deleting an org from a script or CI job.
- Diagnosing `sf org create scratch` failures (feature not enabled, allocation exhausted,
  snapshot expired, org shape stale).
- Deciding source tracking on/off, and resolving or resetting tracking state.
- Not for deploying metadata (skill `sf-deployment-strategies`), not for seeding strategy itself
  (skill `sf-data-management`), not for `sf` auth basics (skill `sf-cli-operations`).

## Decision table: which org

| Need | Use | Why |
| --- | --- | --- |
| Feature branch build + local gate + throwaway verification | scratch org | Declarative shape, source tracking on, 1–30 day expiry, free from Dev Hub allocation |
| Per-developer long-lived workspace tied to production metadata | Developer sandbox | Metadata copy of production, source tracking supported, 200 MB data |
| Same, but needs more room for seeded test data | Developer Pro sandbox | 1 GB data, source tracking supported |
| UAT against a representative slice of production data | Partial Copy sandbox | Template-driven data subset; source tracking **not** supported |
| Performance/integration rehearsal, full data, release staging | Full sandbox | Full data copy; source tracking **not** supported |
| Package installation smoke test | scratch org (no namespace) | `--no-namespace` avoids namespace clash when installing a packaged version |
| Package or metadata you cannot untangle from production config | Developer/Developer Pro sandbox + org-dependent unlocked package | Dependencies validate at install time; see skill `sf-packaging-release` |

Source tracking is supported and on by default in scratch orgs and in Developer / Developer Pro
sandboxes. It cannot be enabled for Partial Copy sandboxes, Full sandboxes, or Developer Edition
orgs.

## Dev Hub and allocations

Enable Dev Hub in Developer, Enterprise, Unlimited, or Performance edition. The Dev Hub edition
sets the allocations:

| Dev Hub edition | Active scratch orgs | Daily scratch orgs (rolling 24 h) | Snapshots (active and daily) |
| --- | --- | --- | --- |
| Developer Edition or trial | 3 | 6 | 3 |
| Enterprise Edition | 40 | 80 | 40 |
| Unlimited Edition | 100 | 200 | 100 |
| Performance Edition | 100 | 200 | 100 |

Scratch org storage: 500 MB data, 50 MB files. Snapshots carry a 200 MB data storage limit,
expire after 90 days, and their data is retained 100 days from creation.

```bash
# Remaining allocations on the Dev Hub
sf limits api display --target-org vf-devhub          # ActiveScratchOrgs / DailyScratchOrgs
sf org list limits --target-org vf-devhub             # ActiveOrgSnapshots / DailyOrgSnapshots
sf org list --all --skip-connection-status            # find orphaned scratch orgs to reclaim
```

CI rule: always `sf org delete scratch --no-prompt` in a trap/`finally`. An abandoned org burns
an active allocation until it expires (default 7 days).

## Core patterns

### 1. Definition file is the contract

`config/project-scratch-def.json` is the single declaration of org shape. `edition` is the only
required key; everything else defaults. Full option table and ready-to-use files:
[references/scratch-org-definition.md](references/scratch-org-definition.md).

```json
{
  "orgName": "vibe-force dev",
  "edition": "Developer",
  "hasSampleData": false,
  "features": ["EnableSetPasswordInApi", "AuthorApex", "DebugApex"],
  "settings": {
    "lightningExperienceSettings": { "enableS1DesktopEnabled": true },
    "mobileSettings": { "enableS1EncryptedStoragePref2": false }
  }
}
```

### 2. Create with explicit Dev Hub, alias, and duration

```bash
sf org create scratch \
  --definition-file config/project-scratch-def.json \
  --target-dev-hub vf-devhub \
  --alias vf-dev \
  --duration-days 7 \
  --wait 15
```

`--duration-days` accepts 1–30, default 7. `--target-dev-hub` (`-v`) is required unless the
`target-dev-hub` config variable is set. `--edition`, `--snapshot`, and `--source-org` are
mutually exclusive. Command-line overrides (`--name`, `--description`, `--username`,
`--admin-email`, `--release`) win over the definition file.

### 3. Long creations: async plus resume

```bash
JOB=$(sf org create scratch -f config/project-scratch-def.json -v vf-devhub --async --json \
      | jq -r '.result.scratchOrgInfo.Id')
sf org resume scratch --job-id "$JOB" --wait 20
```

`sf org resume scratch` also recovers a creation that timed out. Use `--use-most-recent` when the
job id was lost.

### 4. Snapshots for expensive shapes

When a shape needs installed packages plus manual setup, build it once and snapshot it. Scratch
org creation from a snapshot is slower than from an edition, so raise `--wait`.

```bash
sf org create snapshot --source-org vf-seed --name VFBase \
  --description "PkgA 1.4.0 + seed data @ $(git rev-parse --short HEAD)" --target-dev-hub vf-devhub
sf org get snapshot  --snapshot VFBase --target-dev-hub vf-devhub   # wait for Status = Active
sf org list snapshot --target-dev-hub vf-devhub
sf org create scratch --snapshot VFBase --alias vf-dev --target-dev-hub vf-devhub --wait 20
```

Snapshots cannot be created from a namespaced scratch org or from an org that was itself created
from a snapshot. Connected apps, named credentials, and external credentials are never copied.

### 5. Org shape when production config is the source of truth

```bash
sf org create shape --target-org vf-prod       # requires Org Shape enabled in the source org
sf org list shape
sf org create scratch --source-org 00DB1230000Ifx5 --alias vf-shaped --target-dev-hub vf-devhub
```

`Chatbot`, `DevOpsCenter`, `MultiCurrency`, and `PersonAccounts` are intentionally not captured
by an org shape — add them back through `features`/`settings` in the definition file.

### 6. Full lifecycle loop (the shape agents and CI both run)

Create -> deploy source -> assign permission sets -> seed data -> run tests -> destroy. Scripted
end to end in [references/org-lifecycle-scripts.md](references/org-lifecycle-scripts.md).

```bash
set -euo pipefail
ALIAS="vf-ci-$(git rev-parse --short HEAD)"
trap 'sf org delete scratch --target-org "$ALIAS" --no-prompt || true' EXIT

sf org create scratch -f config/ci-scratch-def.json -v vf-devhub -a "$ALIAS" -y 1 -w 15 --no-track-source
sf project deploy start --target-org "$ALIAS" --source-dir force-app --wait 30
sf org assign permset --name VF_App_Admin --target-org "$ALIAS"
sf data import tree --plan data/plan.json --target-org "$ALIAS"
node "$VF_ROOT/scripts/checks/vf-check.mjs" apex --target-org "$ALIAS" --json
```

`--no-track-source` is the right call for CI: tracking costs `SourceMember` polling and file
system work that a throwaway org never benefits from.

### 7. Sandbox creation and refresh

```bash
sf org create sandbox --definition-file config/dev-sandbox-def.json \
  --alias vf-int --target-org vf-prod --set-default --wait 30
sf org refresh sandbox --name vfint --target-org vf-prod --wait 60
sf org resume sandbox --name vfint --target-org vf-prod --wait 30
sf org delete sandbox --target-org vf-int --no-prompt
```

`--target-org` on every sandbox command is the **production org that holds the sandbox licenses**,
not the sandbox. Sandbox names are 10 or fewer alphanumeric characters and cannot be changed on
refresh. Default `--wait` is 6 minutes, which is almost always too short — pass 30–60. Full
flag tables, definition options, and the post-refresh checklist:
[references/sandbox-operations.md](references/sandbox-operations.md).

### 8. Post-copy automation

`apexClassName` in the sandbox definition names an Apex class implementing `SandboxPostCopy`; it
runs after every create, clone, and refresh. Use it for the deterministic parts of post-refresh
work (deactivating integration users, rewriting endpoints, blanking emails).

```apex
public with sharing class VFSandboxPostCopy implements SandboxPostCopy {
    public void runApexClass(SandboxContext ctx) {
        List<VF_Integration_Setting__c> settings = [
            SELECT Id, Endpoint__c, Active__c
            FROM VF_Integration_Setting__c
            WITH USER_MODE
            LIMIT 200
        ];
        for (VF_Integration_Setting__c s : settings) {
            s.Endpoint__c = 'https://sandbox.example.invalid/api';
            s.Active__c = false;
        }
        if (!settings.isEmpty()) {
            update as user settings;
        }
        System.debug(LoggingLevel.INFO, 'Post-copy done for org ' + ctx.organizationId());
    }
}
```

### 9. Source tracking hygiene

```bash
sf project deploy preview   --target-org vf-dev     # conflicts, deletions, ignored files
sf project retrieve preview --target-org vf-dev
sf project deploy start  --metadata ApexClass:WidgetClass --ignore-conflicts --target-org vf-dev
sf project retrieve start --metadata ApexClass:WidgetClass --ignore-conflicts --target-org vf-dev
sf project reset tracking  --target-org vf-dev --no-prompt   # destructive: wipes tracking state
sf project delete tracking --target-org vf-dev --no-prompt   # local tracking files only
```

`sf project reset tracking --revision <n>` rewinds to a specific `SourceMember.RevisionCounter`;
get the number with
`sf data query --query "SELECT MemberName, MemberType, RevisionCounter FROM SourceMember" --use-tooling-api --target-org vf-dev`.
There is no `--dry-run` flag on `sf project retrieve start`; use `sf project retrieve preview`.

## Anti-patterns

| Anti-pattern | Failure | Fix |
| --- | --- | --- |
| `sf org create scratch -e developer` with no definition file for feature work | Features and settings the code needs are absent; deploy fails on unrelated metadata | Keep a checked-in definition file; `--edition` only for throwaway probes |
| Omitting `--target-dev-hub` in CI | Job picks up whatever `target-dev-hub` the runner happens to have | Always pass `-v <alias>` explicitly |
| No `trap`/`finally` delete in CI | Allocation exhausted by abandoned orgs for up to 30 days | `trap 'sf org delete scratch -o "$ALIAS" -p' EXIT` |
| Source tracking left on in CI scratch orgs | Slower deploys, spurious conflict checks | `--no-track-source` for ephemeral orgs |
| `sf project reset tracking` to "fix" a conflict | Real divergence silently hidden; the next deploy overwrites org work | Resolve with `deploy preview` then targeted `--ignore-conflicts` |
| Expecting source tracking in a Full or Partial Copy sandbox | `deploy preview` reports nothing; conflicts undetected | Use manifest-driven deploys there; see skill `sf-deployment-strategies` |
| Treating a snapshot as version control | Snapshot expires in 90 days; shape drifts from the repo | Repo is the source of truth; snapshot only caches dependencies |
| Reusing a sandbox name right after delete | `The sandbox name ... could not be found` / name-in-use error | Wait for deletion to finish, or pick a new 10-character name |

```json
// WRONG - Experience Cloud needs both the feature and its setting
{ "edition": "Enterprise", "features": ["Communities"] }

// RIGHT
{
  "edition": "Enterprise",
  "features": ["Communities"],
  "settings": { "communitiesSettings": { "enableNetworksEnabled": true } }
}
```

## Verification

```bash
# 1. Org exists, is the right shape, and is authenticated
sf org display --target-org vf-dev --verbose
sf org list --all --skip-connection-status

# 2. Shape assertions: features and edition actually applied
sf data query --query "SELECT OrganizationType, InstanceName, TrialExpirationDate FROM Organization" \
  --target-org vf-dev
sf limits api display --target-org vf-dev

# 3. Source landed and tracking is clean
sf project deploy preview --target-org vf-dev        # expect "No local changes to deploy"

# 4. Harness gates
node "$VF_ROOT/scripts/checks/vf-check.mjs" local
node "$VF_ROOT/scripts/checks/vf-check.mjs" apex  --target-org vf-dev
node "$VF_ROOT/scripts/checks/vf-check.mjs" smoke --target-org vf-dev
```

`vf-check apex`, `smoke`, and `verify` require an org and honour `--target-org`; `local` never
touches an org. Every run writes `<project>/.vibeforce/reports/<check>-<ISO>.json`.

vibe-force hooks never provision or delete an org. The Claude Code lifecycle hooks guard
destructive and production operations only (`blockDestructive`, `blockProductionDeploy`); a
scratch org delete against an alias listed in `productionAliases` is refused unless
`VF_ALLOW_PROD=1` is set.

## References

- [references/scratch-org-definition.md](references/scratch-org-definition.md) — every definition
  file option, feature/setting pairs, four ready definition files.
- [references/org-lifecycle-scripts.md](references/org-lifecycle-scripts.md) — bash scripts for
  create/seed/test/destroy, snapshot refresh, CI matrix orgs.
- [references/sandbox-operations.md](references/sandbox-operations.md) — sandbox types, CLI flag
  tables, definition options, post-refresh runbook.
- [references/org-troubleshooting.md](references/org-troubleshooting.md) — signup error codes,
  allocation and snapshot failures, tracking recovery.

Sibling skills: `sf-cli-operations` (auth, aliases, JWT), `sf-project-structure`
(`sfdx-project.json`, package directories), `sf-data-management` (seeding and `data import tree`),
`sf-deployment-strategies` (deploy into these orgs), `sf-post-deploy-verification` (smoke probes),
`sf-workflow-orchestration` (which wave provisions what).

Official documentation used:

- Salesforce DX Developer Guide — Supported Scratch Org Editions and Allocations:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs_editions_and_allocations.htm>
- Build Your Own Scratch Org Definition File:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs_def_file.htm>
- Create Scratch Orgs:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_scratch_orgs_create.htm>
- Scratch Org Snapshots:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_snapshots_intro.htm>
- Create a Sandbox Definition File:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_sandbox_definition.htm>
- Create, Clone, or Refresh a Sandbox:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_dev_create_clone_sandboxes.htm>
- Enable Source Tracking in Sandboxes:
  <https://developer.salesforce.com/docs/atlas.en-us.262.0.sfdx_dev.meta/sfdx_dev/sfdx_setup_enable_source_tracking_sandboxes.htm>
- Salesforce CLI command reference (`org create scratch`, `org create sandbox`,
  `org refresh sandbox`, `org resume scratch|sandbox`, `org delete scratch|sandbox`,
  `project reset tracking`): <https://github.com/salesforcecli/cli/blob/main/README.md> and
  <https://github.com/salesforcecli/plugin-org/tree/main/messages>
- Snapshot and shape commands:
  <https://github.com/salesforcecli/plugin-signups/blob/main/README.md>
- Scratch org definition JSON schema:
  <https://github.com/forcedotcom/schemas/blob/main/project-scratch-def.schema.json>
